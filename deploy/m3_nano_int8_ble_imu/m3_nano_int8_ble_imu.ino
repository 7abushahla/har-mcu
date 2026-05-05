// M3 HAR INT8 (BLE + LIVE IMU) — Nano 33 BLE. BLE UI remote control.
// Session → windowing matches offline pipeline.
//
// BLE service "HAR Control" (UUID 19B10000-E8F2-537E-4F6C-D104768A1214):
//   cmd  characteristic (write, UUID ...0001): 0x01=toggle START/STOP, 0x02=average, 0x10..0x15=set GT, 0x1F=clear GT
//   status characteristic (notify, UUID ...0002): 1 byte state + 1 byte last pred class
//     byte[0]: 0=idle, 1=recording  byte[1]: last predicted class index (0–5, 0xFF if none)
//
// Desktop app: deploy/m3_nano_int8_ble_imu/ble_controller.py (Python + bleak + tkinter).
//
// Preprocessing (matches har-mcu `train_zscore` + `raw_no_conversion` in norm_stats JSON):
//   1) Optional unit scale: accel * UNIT_PRE_MULTIPLY * UNIT_SCALE (from norm header; usually 1).
//   2) Z-score **per sample** (per timestep, per axis): (x - kNormMean[a]) / kNormStd[a].
//      Same global mean/std for every sample in every window — NOT mean/std computed inside each window.
// M3 deploy: all m3_*.h live next to this .ino. Re-export: deploy/m3_int8_headers then
//   cp deploy/m3_int8_headers/m3_*.h deploy/m3_nano_int8_ble_imu/

#include <math.h>
#include <string.h>
#include <ArduinoBLE.h>
#include <TensorFlowLite.h>
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include <Arduino_LSM9DS1.h>

// -------- BLE service / characteristic UUIDs --------
#define BLE_SERVICE_UUID  "19B10000-E8F2-537E-4F6C-D104768A1214"
#define BLE_CMD_UUID      "19B10001-E8F2-537E-4F6C-D104768A1214"
#define BLE_STATUS_UUID   "19B10002-E8F2-537E-4F6C-D104768A1214"
#define BLE_INFO_UUID     "19B10003-E8F2-537E-4F6C-D104768A1214"  // read-only: model config string
// cmd values from desktop app:
#define BLE_CMD_CLICK     0x01   // toggle START / STOP
#define BLE_CMD_LONGHOLD  0x02   // average buffered trials
#define BLE_CMD_GT_BASE    0x10   // 0x10..0x15 set ground-truth class 0..5
#define BLE_CMD_GT_CLEAR   0x1F   // clear ground-truth class
// status byte[0] values sent to desktop app:
#define BLE_STATE_IDLE    0x00
#define BLE_STATE_REC     0x01
#define BLE_STATE_AVG     0x02   // average-result notification — not a live window

// ======== Edit these three lines, then compile + flash ============================
#include "daghero_accel_rotation_v2_bounded20_p025_qat.h"
#define M3_MODEL_SYM    daghero_accel_rotation_v2_bounded20_p025_qat
#define M3_KWINDOW_SIZE 100  // ← T: 100 or 50 
// ==================================================================================

// Norm header is chosen from T above — no need to touch this block.
#if M3_KWINDOW_SIZE == 100
#include "m3_norm_finetune_t100.h"
#else
#include "m3_norm_finetune_t50.h"
#endif

// Derived — do not edit.
#define M3_MODEL_BYTES     M3_MODEL_SYM
#define _M3_LEN_PASTE(x)   x##_len
#define _M3_LEN_EXPAND(x)  _M3_LEN_PASTE(x)   // extra level forces expansion of x before ##
#define M3_MODEL_LEN_VAR   _M3_LEN_EXPAND(M3_MODEL_SYM)
#define M3_KWINDOW_HOP     (M3_KWINDOW_SIZE / 2)
#define _M3_STR_INNER(x)   #x
#define _M3_STR_EXPAND(x)  _M3_STR_INNER(x)       // extra level forces expansion before #
#define M3_MODEL_SYM_STR   _M3_STR_EXPAND(M3_MODEL_SYM)

// Live IMU sampling rate (Hz) for `loop()` timing. Norm header still carries training
// `SAMPLE_RATE_HZ` (20) for metadata; models were trained on 20 Hz windows — using 100 Hz here
// changes real window duration vs training unless you retrain / resample to match.
#ifndef LIVE_SAMPLE_RATE_HZ
#define LIVE_SAMPLE_RATE_HZ 100
#endif

// WINDOW_SIZE / kNorm* come from m3_norm_finetune_t*.h; live stream uses LIVE_SAMPLE_RATE_HZ above.
const int NUM_FEATURES = 3;
const int NUM_CLASSES = 6;

// Unit scale fused (matches norm_stats JSON); z-score uses 1/std once at compile time (no per-sample div).
static constexpr float kUnitProduct = UNIT_PRE_MULTIPLY * UNIT_SCALE;
#if APPLY_NORMALIZATION
static constexpr float kNormInvStd[NUM_FEATURES] = {
    1.0f / kNormStd[0], 1.0f / kNormStd[1], 1.0f / kNormStd[2]};
#endif

#define BAUDRATE 115200
// Match serial/live TFLM path; model flatbuffer must be alignas(16) in the .h (export script does this).
const int kTensorArenaSize = 50 * 1024;
const int kWindowHop = M3_KWINDOW_HOP;
// Max length of one START…STOP run. ArduinoBLE library + TFLM arena leave very little
// SRAM on Nano 33 BLE — keep this small. 500 samples = 25 s @ 20 Hz (or 5 s @ 100 Hz).
// 500 * 3 * 4 = 6 KB.
const int kMaxSessionSamples = 1500;
// Cumulative logit cap (multiple STOP batches stack until full). 16 * 6 * 4 = 0.4 KB.
const int kMaxSessionTrials = 64;
const int kSampleRateHz = LIVE_SAMPLE_RATE_HZ;
const uint32_t kSamplePeriodMs = 1000U / static_cast<uint32_t>(kSampleRateHz);
const bool kUseImuContinuousMode = false;
// Training CSV came from tf4micro-motion-kit captures: stored accelerometer = readAcceleration(g) / 4.
// Arduino_LSM9DS1::readAcceleration() returns g, so divide by 4 before applying train z-score.
const float kAccelScaleDivisor = 4.0f;


static const char* const kClassNames[NUM_CLASSES] = {
    "Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"};
// Short labels for confusion matrix columns (rows = true GT, cols = pred).
static const char* const kClassAbr[NUM_CLASSES] = {"Walk", "Jog", "Upsz", "Dnsz", "Sit", "Stnd"};

// Ground truth: set by BLE UI before START; Serial input remains as a debug fallback. Snapshot at START.
static int8_t g_ground_truth = -1;
// Copy of g_ground_truth at REC start; used for each window in the following sliding pass.
static int8_t g_session_gt = -1;
// Cumulative counts since last long-hold report: rows=GT, cols=pred.
static uint16_t g_confusion[NUM_CLASSES][NUM_CLASSES];

namespace {
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
alignas(16) uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// BLE state — declared early so inference functions can reference them.
static uint8_t g_ble_last_pred_class = 0xFF;
// Confidence for BLE notify: tenths of a percent (996 => 99.6%). 0 when pred unknown.
static uint16_t g_ble_conf_tenths = 0;
static bool     g_ble_is_avg_result = false;  // set before ble_update_status() for average
static void ble_update_status();  // forward declaration; defined in BLE globals block below

// Live session: raw (normalized) accel stream between START and STOP
float g_session_buffer[kMaxSessionSamples][NUM_FEATURES];
int g_session_n = 0;
// Temp: one window in row-major time order; fill_int8_input_from_ring reads oldest at ring_head
float ring_buffer[WINDOW_SIZE][NUM_FEATURES];
int ring_head = 0;
int g_infer_trial = 0;
uint32_t next_sample_ms = 0;
bool g_ready_banner = false;
bool g_recording = false;
// Cumulative: each STOP+sliding appends; long-hold averages then clears (g_n_trials_buffered = 0).
float g_trial_logit[kMaxSessionTrials][NUM_CLASSES];
float g_trial_invoke_ms[kMaxSessionTrials];
float g_trial_window_conf[kMaxSessionTrials];  // softmax conf % for that window’s argmax class
uint8_t g_trial_pred_class[kMaxSessionTrials];  // per-window argmax (0..NUM_CLASSES-1)
int g_n_trials_buffered = 0;
// While run_sliding_session_inference runs, save logits per window.
static bool g_trial_saving = false;

static int confusion_matrix_total() {
  int t = 0;
  for (int r = 0; r < NUM_CLASSES; ++r) {
    for (int c = 0; c < NUM_CLASSES; ++c) {
      t += static_cast<int>(g_confusion[r][c]);
    }
  }
  return t;
}

static void clear_confusion_matrix() {
  for (int r = 0; r < NUM_CLASSES; ++r) {
    for (int c = 0; c < NUM_CLASSES; ++c) {
      g_confusion[r][c] = 0;
    }
  }
}

static char ascii_to_lower(const char c) {
  if (c >= 'A' && c <= 'Z') {
    return static_cast<char>(c + 32);
  }
  return c;
}

// ASCII-only case-insensitive equality, whole strings.
static bool strieq(const char* a, const char* b) {
  while (*a && *b) {
    if (ascii_to_lower(*a) != ascii_to_lower(*b)) {
      return false;
    }
    a++;
    b++;
  }
  return *a == *b;
}

// Trim in place. Modifies the buffer; returns the effective string pointer.
static void trim_cstring(char* s) {
  if (s == nullptr || s[0] == '\0') {
    return;
  }
  char* start = s;
  while (*start == ' ' || *start == '\t') {
    start++;
  }
  if (start > s) {
    memmove(s, start, strlen(start) + 1);
  }
  int len = static_cast<int>(strlen(s));
  while (len > 0 && (s[len - 1] == ' ' || s[len - 1] == '\t' || s[len - 1] == '\n' ||
                    s[len - 1] == '\r')) {
    s[--len] = '\0';
  }
  for (int i = 0; s[i]; ++i) {
    s[i] = ascii_to_lower(s[i]);
  }
}

// 0..NUM_CLASSES-1 or -1. Expects null-terminated, trimmed, lowercased.
static int parse_ground_truth_label(char* s) {
  if (s == nullptr || s[0] == '\0') {
    return -1;
  }
  if (strlen(s) == 1) {
    const char d = s[0];
    if (d >= '0' && d < static_cast<char>('0' + NUM_CLASSES)) {
      return d - '0';
    }
  }
  for (int k = 0; k < NUM_CLASSES; ++k) {
    if (strieq(s, kClassNames[k])) {
      return k;
    }
  }
  if (strieq(s, "w")) {
    return 0;
  }
  if (strieq(s, "j")) {
    return 1;
  }
  if (strieq(s, "u")) {
    return 2;
  }
  if (strieq(s, "d")) {
    return 3;
  }
  if (strieq(s, "s") || strieq(s, "si") || strieq(s, "sit")) {
    return 4;
  }
  if (strieq(s, "st") || strieq(s, "stnd") || strieq(s, "stand")) {
    return 5;
  }
  return -1;
}

// --- Confusion matrix (fixed width for monospace serial monitor) ---
static const int kCmLColW = 12;  // "T" + abbr (fits "Upsz")
static const int kCmCellW = 4;  // 0-9999

static int uint10_width(uint32_t n) {
  if (n == 0) {
    return 1;
  }
  int w = 0;
  while (n) {
    n /= 10U;
    w++;
  }
  return w;
}

static void print_padded_int_u32(uint32_t n, int width) {
  const int len = uint10_width(n);
  for (int i = len; i < width; ++i) {
    Serial.print(' ');
  }
  Serial.print(n);
}

// "T " + 4-char row label, padded to kCmLColW
static void print_confusion_left_label(const char* ab) {
  Serial.print(F("T "));
  for (int i = 0; i < 4; ++i) {
    if (ab[i] != '\0' && ab[i] != 0) {
      Serial.print(ab[i]);
    } else {
      Serial.print(' ');
    }
  }
  for (int k = 6; k < kCmLColW; ++k) {
    Serial.print(' ');
  }
}

// Rows=ground, cols=pred; uniform columns, ASCII rules (set Serial Monitor to monospace)
static void print_confusion_matrix_text() {
  const int tot = confusion_matrix_total();
  if (tot <= 0) {
    return;
  }
  const int kTableBodyW = NUM_CLASSES * (1 + kCmCellW);  // " " + 4-char wide each column
  Serial.println();
  Serial.println(F("========== CONFUSION: rows = true (T), columns = pred =========="));
  for (int k = 0; k < kCmLColW; ++k) {
    Serial.print(' ');
  }
  Serial.print(F("  |"));
  for (int c = 0; c < NUM_CLASSES; ++c) {
    Serial.print(' ');
    for (int i = 0; kClassAbr[c][i] && i < 4; ++i) {
      Serial.print(kClassAbr[c][i]);
    }
    for (int p = static_cast<int>(strlen(kClassAbr[c])); p < kCmCellW; ++p) {
      Serial.print(' ');
    }
    if (c + 1 < NUM_CLASSES) {
      Serial.print(' ');
    }
  }
  Serial.print(F(" |  n   r%  "));
  Serial.println();
  {
    for (int a = 0; a < kCmLColW; ++a) {
      Serial.print(' ');
    }
    Serial.print(F("  +"));
    for (int t = 0; t < kTableBodyW; ++t) {
      Serial.print(F("-"));
    }
    Serial.print(F("+----------------+"));
    Serial.println();
  }
  for (int r = 0; r < NUM_CLASSES; ++r) {
    int row_sum = 0;
    print_confusion_left_label(kClassAbr[r]);
    Serial.print(F("  |"));
    for (int c = 0; c < NUM_CLASSES; ++c) {
      const uint32_t v = g_confusion[r][c];
      row_sum += static_cast<int>(v);
      Serial.print(' ');
      print_padded_int_u32(v, kCmCellW);
    }
    const uint32_t d = g_confusion[r][r];
    if (row_sum == 0) {
      Serial.print(F(" |   0  --  "));
    } else {
      Serial.print(F(" |  "));
      print_padded_int_u32(static_cast<uint32_t>(row_sum), 3);
      const float rcall = 100.0f * (static_cast<float>(d) / static_cast<float>(row_sum));
      Serial.print(F("  "));
      if (d == 0U) {
        Serial.print(F("0%  "));
      } else if (d == static_cast<uint32_t>(row_sum)) {
        Serial.print(F("100%  "));
      } else {
        Serial.print(rcall, 1);
        Serial.print(F("%  "));
      }
    }
    Serial.println();
  }
  {
    for (int a = 0; a < kCmLColW; ++a) {
      Serial.print(' ');
    }
    Serial.print(F("  +"));
    for (int td = 0; td < kTableBodyW; ++td) {
      Serial.print(F("-"));
    }
    Serial.print(F("+----------------+"));
    Serial.println();
  }
  Serial.print(F("  total = "));
  Serial.print(tot);
  Serial.println(F(" window(s)  (r% = diagonal / n for that true class)"));
  Serial.println(F("====================================================================="));
  Serial.println();
}

static const int kMaxSerialLine = 48;
// Non-blocking: read a line, set g_ground_truth, or help.
static void poll_serial_ground_truth() {
  static char sbuf[kMaxSerialLine + 1];
  static int slen = 0;
  while (Serial.available() > 0) {
    const int c = Serial.read();
    if (c < 0) {
      break;
    }
    if (c == '\n' || c == '\r') {
      if (slen > 0) {
        sbuf[slen] = '\0';
        trim_cstring(sbuf);
        if (sbuf[0] != '\0' &&
            (strieq(sbuf, "help") || strieq(sbuf, "?") || strieq(sbuf, "h"))) {
          Serial.println(
              F("[help] Set ground truth: Walking, Jogging, Upstairs, Downstairs, Sit, Standing, "
                "or 0-5, then START/REC before recording."));
          Serial.println(
              F("[help] Short: w j u d si st  |  long-hold 2.5s: mean+confusion, clears buffer+CM."));
        } else if (sbuf[0] != '\0') {
          char work[kMaxSerialLine + 1];
          strncpy(work, sbuf, kMaxSerialLine);
          work[kMaxSerialLine] = '\0';
          const int p = parse_ground_truth_label(work);
          if (p >= 0) {
            g_ground_truth = static_cast<int8_t>(p);
            Serial.print(F(">>> [GT] ground truth = "));
            Serial.print(kClassNames[p]);
            Serial.print(F(" ("));
            Serial.print(p);
            Serial.println(F(")  —  press START/REC, then same as before."));
          } else {
            Serial.print(F(">>> [GT] unknown: \""));
            Serial.print(sbuf);
            Serial.println(F("\"  (type help)"));
          }
        }
        slen = 0;
      }
      if (c == '\r' && Serial.peek() == '\n') {
        (void)Serial.read();
      }
    } else if (slen < kMaxSerialLine) {
      sbuf[slen++] = static_cast<char>(c);
    } else {
      slen = 0;  // overflow, reset line
    }
  }
}

static void set_activity_busy_led(const bool on) {
  digitalWrite(LED_BUILTIN, on ? HIGH : LOW);
}

static void init_status_leds() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

static void clear_tensor_arena() {
  for (size_t i = 0; i < kTensorArenaSize; ++i) {
    tensor_arena[i] = 0;
  }
}

// One IMU reading: same as har-mcu `apply_axis_stats` — (v - mean) / std, with v = raw * unit product.
// Called once per sample at REC → g_session_buffer holds z-scored floats; sliding windows reuse them
// (no duplicate norm on overlaps). INT8 input: quantize those floats (fill_int8_input_from_ring).
static float preprocess_accel_axis(const float raw_accel, const int axis) {
  const float v = raw_accel * kUnitProduct;
#if APPLY_NORMALIZATION
  return (v - kNormMean[axis]) * kNormInvStd[axis];
#else
  (void)axis;
  return v;
#endif
}

// Copy one window [start .. start+WINDOW_SIZE) into ring, ring_head=0 so time runs t=0..T-1
static void copy_session_window_to_ring(const int start) {
  for (int t = 0; t < WINDOW_SIZE; ++t) {
    for (int c = 0; c < NUM_FEATURES; ++c) {
      ring_buffer[t][c] = g_session_buffer[start + t][c];
    }
  }
  ring_head = 0;
}

static void fill_int8_input_from_ring() {
  const float scale = input->params.scale;
  const int32_t zp = input->params.zero_point;

  int idx = ring_head;  // oldest
  for (int t = 0; t < WINDOW_SIZE; ++t) {
    for (int c = 0; c < NUM_FEATURES; ++c) {
      const float v = ring_buffer[idx][c];
      const float scaled = (v / scale) + static_cast<float>(zp);
      int32_t q = static_cast<int32_t>(scaled + (scaled >= 0.0f ? 0.5f : -0.5f));
      if (q < -128) {
        q = -128;
      }
      if (q > 127) {
        q = 127;
      }
      input->data.int8[t * NUM_FEATURES + c] = static_cast<int8_t>(q);
    }
    idx = (idx + 1) % WINDOW_SIZE;
  }
}

static void output_to_logits(const TfLiteTensor* out, float* logits) {
  if (out->type == kTfLiteInt8) {
    const float scale = out->params.scale;
    const int32_t zp = out->params.zero_point;
    for (int k = 0; k < NUM_CLASSES; ++k) {
      logits[k] = (static_cast<float>(out->data.int8[k]) - static_cast<float>(zp)) * scale;
    }
  } else {
    for (int k = 0; k < NUM_CLASSES; ++k) {
      logits[k] = out->data.f[k];
    }
  }
}

static int argmax_class(const float* logits) {
  int best = 0;
  for (int k = 1; k < NUM_CLASSES; ++k) {
    if (logits[k] > logits[best]) {
      best = k;
    }
  }
  return best;
}

static bool looks_like_probabilities(const float* scores) {
  float sum = 0.0f;
  for (int k = 0; k < NUM_CLASSES; ++k) {
    if (scores[k] < -0.02f || scores[k] > 1.02f) {
      return false;
    }
    sum += scores[k];
  }
  return sum > 0.95f && sum < 1.05f;
}

static float confidence_percent(const float* scores, const int class_idx) {
  // M3 exported classifiers end with SOFTMAX. For those, dequantized int8 output is already
  // probabilities (output scale often 1/256, zero-point -128). Do NOT softmax probabilities
  // again, or a 0.9 class probability becomes only ~33% after exp/renormalization.
  if (looks_like_probabilities(scores)) {
    return 100.0f * scores[class_idx];
  }

  float m = scores[0];
  for (int k = 1; k < NUM_CLASSES; ++k) {
    if (scores[k] > m) {
      m = scores[k];
    }
  }
  float s = 0.0f;
  for (int k = 0; k < NUM_CLASSES; ++k) {
    s += expf(scores[k] - m);
  }
  return 100.0f * (expf(scores[class_idx] - m) / s);
}

// Boot diagnostics: input/output shape and int8 quant params (like notebook “tensor layout”).
static void print_tensor_dims_scale(const char* tag, const TfLiteTensor* t) {
  Serial.print(F("[tensor] "));
  Serial.print(tag);
  Serial.print(F(" type="));
  Serial.print(static_cast<int>(t->type));
  Serial.print(F(" dims="));
  if (t->dims != nullptr && t->dims->size > 0) {
    for (int i = 0; i < t->dims->size; ++i) {
      if (i > 0) {
        Serial.print('x');
      }
      Serial.print(t->dims->data[i]);
    }
  } else {
    Serial.print('?');
  }
  if (t->type == kTfLiteInt8) {
    Serial.print(F(" quant_scale="));
    Serial.print(t->params.scale, 7);
    Serial.print(F(" zp="));
    Serial.println(static_cast<int>(t->params.zero_point));
  } else if (t->type == kTfLiteFloat32) {
    Serial.println(F(" (float)"));
  } else {
    Serial.println();
  }
}

static void setup_interpreter() {
  static tflite::AllOpsResolver resolver;
  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;
}

// Fill input from ring, Invoke, logits out. false = bad type or failed Invoke.
static bool run_invoke_get_logits(float* logits, float* invoke_ms_out) {
  if (input->type == kTfLiteInt8) {
    fill_int8_input_from_ring();
  } else if (input->type == kTfLiteFloat32) {
    int idx = ring_head;
    for (int t = 0; t < WINDOW_SIZE; ++t) {
      for (int c = 0; c < NUM_FEATURES; ++c) {
        input->data.f[t * NUM_FEATURES + c] = ring_buffer[idx][c];
      }
      idx = (idx + 1) % WINDOW_SIZE;
    }
  } else {
    Serial.print(F("Unsupported input type: "));
    Serial.println(static_cast<int>(input->type));
    return false;
  }
  set_activity_busy_led(true);
  const uint32_t t_us = micros();
  if (interpreter->Invoke() != kTfLiteOk) {
    set_activity_busy_led(false);
    Serial.println(F("Invoke() failed"));
    return false;
  }
  *invoke_ms_out = (micros() - t_us) / 1000.0f;
  set_activity_busy_led(false);
  output_to_logits(output, logits);
  return true;
}

// One window already in ring order (after copy_session_window_to_ring)
static void run_one_invoke(
    const int win_idx,
    const int n_wins,
    const int start_sample) {
  float logits[NUM_CLASSES];
  float invoke_ms;
  if (!run_invoke_get_logits(logits, &invoke_ms)) {
    return;
  }
  const int best = argmax_class(logits);
  const float conf = confidence_percent(logits, best);
  if (g_trial_saving) {
    if (g_session_gt >= 0 && g_session_gt < NUM_CLASSES) {
      g_confusion[static_cast<int>(g_session_gt)][best]++;
    }
    if (g_n_trials_buffered < kMaxSessionTrials) {
      const int idx = g_n_trials_buffered;
      for (int k = 0; k < NUM_CLASSES; ++k) {
        g_trial_logit[idx][k] = logits[k];
      }
      g_trial_invoke_ms[idx] = invoke_ms;
      g_trial_window_conf[idx] = conf;
      g_trial_pred_class[idx] = static_cast<uint8_t>(best);
      g_n_trials_buffered++;
    }
  }
  g_infer_trial++;

  if (!g_ready_banner) {
    g_ready_banner = true;
    Serial.println();
    Serial.println(F("========== START / STOP, then sliding windows =========="));
    Serial.print(F("Window length T="));
    Serial.print(WINDOW_SIZE);
    Serial.print(F(" @ "));
    Serial.print(kSampleRateHz);
    Serial.print(F(" Hz, hop="));
    Serial.print(kWindowHop);
    Serial.println(F(" (50% overlap, matches E11 yaml overlap: 0.5)."));
    Serial.print(F("Buffer max "));
    Serial.print(kMaxSessionSamples);
    Serial.print(F(" samples ("));
    const float ssec =
        (static_cast<float>(kMaxSessionSamples) * static_cast<float>(kSamplePeriodMs)) / 1000.0f;
    Serial.print(ssec, 0);
    Serial.print(F(" s @ "));
    Serial.print(kSampleRateHz);
    Serial.println(F(" Hz (full buffer)."));
    Serial.println(
        F("After STOP, each [start, start+T) runs once until start+T > length."));
    Serial.println(
        F("================================================================"));
  }

  Serial.print(F("trial="));
  Serial.print(g_infer_trial);
  Serial.print(F(" win="));
  Serial.print(win_idx);
  Serial.print(F("/"));
  Serial.print(n_wins);
  Serial.print(F(" start_sample="));
  Serial.print(start_sample);
  Serial.print(F(" invoke_ms="));
  Serial.print(invoke_ms, 4);
  Serial.print(F(" pred="));
  Serial.print(kClassNames[best]);
  Serial.print(F(" conf="));
  Serial.print(conf, 1);
  Serial.print(F("%"));
  // Top-2 and top-3 runners-up appended on same line.
  {
    int r2 = -1, r3 = -1;
    for (int k = 0; k < NUM_CLASSES; ++k) {
      if (k == best) continue;
      if (r2 < 0 || logits[k] > logits[r2]) { r3 = r2; r2 = k; }
      else if (r3 < 0 || logits[k] > logits[r3]) { r3 = k; }
    }
    if (r2 >= 0) {
      Serial.print(F("  ["));
      Serial.print(kClassNames[r2]);
      Serial.print(F("="));
      Serial.print(confidence_percent(logits, r2), 1);
      Serial.print(F("%"));
      if (r3 >= 0) {
        Serial.print(F("  "));
        Serial.print(kClassNames[r3]);
        Serial.print(F("="));
        Serial.print(confidence_percent(logits, r3), 1);
        Serial.print(F("%"));
      }
      Serial.print(F("]"));
    }
  }
  Serial.println();
  g_ble_last_pred_class = static_cast<uint8_t>(best);
  g_ble_conf_tenths     = conf_percent_to_tenths(conf);
  ble_update_status();
}

// After STOP: all sliding windows, each Invoke once
static void run_sliding_session_inference() {
  const int n = g_session_n;
  if (n < WINDOW_SIZE) {
    Serial.print(F("Need at least "));
    Serial.print(WINDOW_SIZE);
    Serial.print(F(" samples (~"));
    const float wsec = (static_cast<float>(WINDOW_SIZE) * static_cast<float>(kSamplePeriodMs)) /
                       1000.0f;
    Serial.print(wsec, 1);
    Serial.print(F(" s at "));
    Serial.print(kSampleRateHz);
    Serial.println(
        F(" Hz) — your segment was too short. Record longer, then press STOP again."));
    return;
  }

  const int n_buf_before = g_n_trials_buffered;
  g_trial_saving = true;

  int n_wins = 0;
  for (int s = 0; s + WINDOW_SIZE <= n; s += kWindowHop) {
    n_wins++;
  }
  if (n_buf_before + n_wins > kMaxSessionTrials) {
    int can_add = kMaxSessionTrials - n_buf_before;
    if (can_add < 0) {
      can_add = 0;
    }
    Serial.print(F(">>> WARNING: only the first "));
    Serial.print(can_add);
    Serial.print(F(" of "));
    Serial.print(n_wins);
    Serial.print(F(" windows in this batch will be saved (cumulative cap "));
    Serial.print(kMaxSessionTrials);
    Serial.println(F("). Increase kMaxSessionTrials or long-hold to average, then record again. <<<"));
  }

  Serial.print(F("--- segment_len="));
  Serial.print(n);
  Serial.print(F(" samples, windows (hop "));
  Serial.print(kWindowHop);
  Serial.print(F(") = "));
  Serial.print(n_wins);
  Serial.println(F(" —"));

  int win = 0;
  for (int s = 0; s + WINDOW_SIZE <= n; s += kWindowHop) {
    BLE.poll();  // keep connection alive during long inference; each invoke ~150ms
    copy_session_window_to_ring(s);
    run_one_invoke(win + 1, n_wins, s);
    win++;
  }

  g_trial_saving = false;
  {
    const int added = g_n_trials_buffered - n_buf_before;
    Serial.print(F("--- +"));
    Serial.print(added);
    Serial.print(F(" this run → "));
    Serial.print(g_n_trials_buffered);
    Serial.println(
        F(" total in RAM. Long-hold: average all; short press+release: START/STOP (adds to buffer) "
          "---"));
  }
  Serial.println(F("--- end of session batch ---\n"));
}

// -------- BLE globals --------
BLEService g_ble_service(BLE_SERVICE_UUID);
BLEByteCharacteristic g_ble_cmd(BLE_CMD_UUID, BLEWrite);
// 4-byte status: [state, pred_class, conf_tenths_le_lo, conf_tenths_le_hi]
// conf: uint16 LE, tenths of a percent (996 = 99.6%). 0 if pred_class == 0xFF (state-only).
// state: BLE_STATE_IDLE=0, BLE_STATE_REC=1, BLE_STATE_AVG=2 (average result, not a window)
BLECharacteristic g_ble_status(BLE_STATUS_UUID, BLERead | BLENotify, 4);
// Read-only config: "T=100 hop=50 model=m3_daghero_finetune_t100_qat_int8" written at boot
BLECharacteristic g_ble_info(BLE_INFO_UUID, BLERead, 96);

static uint16_t conf_percent_to_tenths(float conf_pct) {
  if (conf_pct <= 0.0f) {
    return 0;
  }
  if (conf_pct >= 100.0f) {
    return 1000;
  }
  return static_cast<uint16_t>(conf_pct * 10.0f + 0.5f);
}

static void ble_update_status() {
  const uint8_t state = g_ble_is_avg_result ? BLE_STATE_AVG :
                        (g_recording ? BLE_STATE_REC : BLE_STATE_IDLE);
  const uint16_t tenths = g_ble_conf_tenths;
  uint8_t buf[4] = {
      state,
      g_ble_last_pred_class,
      static_cast<uint8_t>(tenths & 0xFF),
      static_cast<uint8_t>((tenths >> 8) & 0xFF)};
  g_ble_status.writeValue(buf, 4);
  g_ble_is_avg_result = false;  // auto-reset after each notify
}

// Called from loop() — handles BLE connect/poll and translates cmd writes to click/longhold.
static void poll_ble_commands() {
  BLEDevice central = BLE.central();
  if (!central) {
    return;
  }
  if (!g_ble_cmd.written()) {
    return;
  }
  const uint8_t cmd = g_ble_cmd.value();
  if (cmd >= BLE_CMD_GT_BASE && cmd < (BLE_CMD_GT_BASE + NUM_CLASSES)) {
    const int gt = static_cast<int>(cmd - BLE_CMD_GT_BASE);
    g_ground_truth = static_cast<int8_t>(gt);
    Serial.print(F(">>> [BLE] GT = "));
    Serial.print(kClassNames[gt]);
    Serial.print(F(" ("));
    Serial.print(gt);
    Serial.println(F(")"));
  } else if (cmd == BLE_CMD_GT_CLEAR) {
    g_ground_truth = -1;
    Serial.println(F(">>> [BLE] GT cleared <<<"));
  } else if (cmd == BLE_CMD_CLICK) {
    if (!g_recording) {
      g_session_n = 0;
      g_session_gt = g_ground_truth;
      g_recording = true;
      Serial.println();
      if (g_session_gt < 0) {
        Serial.println(F(">>> [BLE] REC — GT not set. Type class in Serial or set via BLE. <<<"));
      } else {
        Serial.print(F(">>> [BLE] REC — GT = "));
        Serial.print(kClassNames[static_cast<int>(g_session_gt)]);
        Serial.println(F(" <<<"));
      }
    } else {
      g_recording = false;
      Serial.print(F(">>> [BLE] STOP — "));
      Serial.print(g_session_n);
      Serial.println(F(" samples, windowing + inference..."));
      run_sliding_session_inference();
      g_session_n = 0;
    }
    // State-only notify: each window already called ble_update_status() with pred+conf.
    // Sending last pred again here duplicates the final window; on START we would send a
    // stale pred/conf from the previous segment — both confuse the desktop UI tally.
    g_ble_last_pred_class = 0xFF;
    g_ble_conf_tenths     = 0;
    ble_update_status();
  } else if (cmd == BLE_CMD_LONGHOLD) {
    Serial.println(F(">>> [BLE] long-hold: averaging buffered trials <<<"));
    run_averaging_of_buffered_trials();
    // ble_update_status() already called inside with BLE_STATE_AVG; don't call again
    // (a second call would look like a window pred to the Python UI).
  }
}

// Long-hold: optional mean of saved logits + confusion matrix, then clear buffers.
static void run_averaging_of_buffered_trials() {
  const int ctot0 = confusion_matrix_total();
  const int n0 = g_n_trials_buffered;

  Serial.println();
  if (n0 <= 0 && ctot0 <= 0) {
    Serial.println(
        F(">>> Long-hold: nothing to report. Type a class in Serial, START/STOP, or stack trials, "
          "then long-hold again."));
    return;
  }

  if (n0 > 0) {
    Serial.print(F(">>> AVERAGING "));
    Serial.print(n0);
    Serial.println(F(" window logits in buffer (mean → argmax)…"));

    float mean[NUM_CLASSES];
    for (int k = 0; k < NUM_CLASSES; ++k) {
      mean[k] = 0.0f;
    }
    for (int i = 0; i < n0; ++i) {
      for (int k = 0; k < NUM_CLASSES; ++k) {
        mean[k] += g_trial_logit[i][k];
      }
    }
    const float invn = 1.0f / static_cast<float>(n0);
    for (int k = 0; k < NUM_CLASSES; ++k) {
      mean[k] *= invn;
    }
    const int best = argmax_class(mean);
    const float conf = confidence_percent(mean, best);

    float sum_ms = 0.0f;
    float sum_conf = 0.0f;
    int vote_count[NUM_CLASSES];
    for (int k = 0; k < NUM_CLASSES; ++k) {
      vote_count[k] = 0;
    }
    for (int i = 0; i < n0; ++i) {
      sum_ms += g_trial_invoke_ms[i];
      sum_conf += g_trial_window_conf[i];
      const int c = static_cast<int>(g_trial_pred_class[i]);
      if (c >= 0 && c < NUM_CLASSES) {
        vote_count[c]++;
      }
    }
    const float mean_ms = sum_ms / static_cast<float>(n0);
    const float mean_win_conf = sum_conf / static_cast<float>(n0);
    int majority = 0;
    for (int k = 1; k < NUM_CLASSES; ++k) {
      if (vote_count[k] > vote_count[majority]) {
        majority = k;
      }
    }

    set_activity_busy_led(true);
    BLE.poll();  // averaging + serial printing can be slow; keep connection alive
    g_ble_last_pred_class = static_cast<uint8_t>(best);
    g_ble_conf_tenths     = conf_percent_to_tenths(conf);
    g_ble_is_avg_result   = true;   // tells Python: this is the averaged result, not a new window
    ble_update_status();
    Serial.print(F(">>> HOLD_AVERAGE: n="));
    Serial.print(n0);
    Serial.print(F(" mean_logits → pred="));
    Serial.print(kClassNames[best]);
    Serial.print(F(" conf="));
    Serial.print(conf, 1);
    Serial.print(F("%  (softmax of mean logits)"));
    // Top-3 from mean logits
    {
      int r2 = -1, r3 = -1;
      for (int k = 0; k < NUM_CLASSES; ++k) {
        if (k == best) continue;
        if (r2 < 0 || mean[k] > mean[r2]) { r3 = r2; r2 = k; }
        else if (r3 < 0 || mean[k] > mean[r3]) { r3 = k; }
      }
      if (r2 >= 0) {
        Serial.print(F("  ["));
        Serial.print(kClassNames[r2]);
        Serial.print(F("="));
        Serial.print(confidence_percent(mean, r2), 1);
        Serial.print(F("%"));
        if (r3 >= 0) {
          Serial.print(F("  "));
          Serial.print(kClassNames[r3]);
          Serial.print(F("="));
          Serial.print(confidence_percent(mean, r3), 1);
          Serial.print(F("%"));
        }
        Serial.print(F("]"));
      }
    }
    Serial.println();
    Serial.print(F("    per_trial: invoke_ms="));
    Serial.print(mean_ms, 2);
    Serial.print(F("  window_conf="));
    Serial.print(mean_win_conf, 1);
    Serial.print(F("%  majority="));
    Serial.print(kClassNames[majority]);
    Serial.print(F(" ("));
    Serial.print(vote_count[majority]);
    Serial.print(F("/"));
    Serial.print(n0);
    // Vote breakdown for all classes that got at least 1 vote
    Serial.print(F(")  votes:"));
    for (int k = 0; k < NUM_CLASSES; ++k) {
      if (vote_count[k] > 0) {
        Serial.print(F(" "));
        Serial.print(kClassNames[k]);
        Serial.print(F("="));
        Serial.print(vote_count[k]);
      }
    }
    Serial.println();
    set_activity_busy_led(false);
    g_n_trials_buffered = 0;
    Serial.println(F(">>> trial buffer cleared. <<<"));
  }
  if (ctot0 > 0) {
    print_confusion_matrix_text();
    clear_confusion_matrix();
    Serial.println(F(">>> confusion matrix cleared (for next data collection). <<<"));
  }
}

void setup() {
  Serial.begin(BAUDRATE);
  const uint32_t t0 = millis();
  while (!Serial && (millis() - t0 < 8000)) {
    delay(10);
  }

  // ---- BLE is brought up AFTER TFLM (see end of setup). The Cordio/HCI
  // background thread on Nano 33 BLE preempts main during AllocateTensors()
  // and hard-faults it; keeping BLE off until TFLM is done avoids that.

  init_status_leds();

  if (!IMU.begin()) {
    Serial.println(F("IMU.begin() failed"));
    while (true) {
      delay(1000);
    }
  }
  if (kUseImuContinuousMode) {
    IMU.setContinuousMode();
  }
  {
    const float driver_hz = IMU.accelerationSampleRate();
    Serial.print(F("IMU: LSM9DS1, driver ~"));
    Serial.print(driver_hz, 0);
    Serial.print(F(" Hz; session stream @ "));
    Serial.print(kSampleRateHz);
    Serial.println(F(" Hz."));
  }
  Serial.println(F("Accel 3ch."));

  Serial.println(F("[boot] tflite init..."));
  tflite::InitializeTarget();
  Serial.println(F("[boot] clear arena..."));
  clear_tensor_arena();

  Serial.println(F("[boot] get model..."));
  model = tflite::GetModel(M3_MODEL_BYTES);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.print(F("[boot] model schema mismatch: got "));
    Serial.print(model->version());
    Serial.print(F(", expected "));
    Serial.println(TFLITE_SCHEMA_VERSION);
    MicroPrintf("Model schema %d, expected %d.",
                model->version(), TFLITE_SCHEMA_VERSION);
    while (true) {
      delay(1000);
    }
  }
  Serial.println(F("[boot] setup interpreter..."));
  setup_interpreter();
  Serial.println(F("[boot] allocate tensors..."));
  if (interpreter->AllocateTensors() != kTfLiteOk) {
    Serial.println(F("[boot] AllocateTensors() failed; raise kTensorArenaSize or choose smaller model."));
    MicroPrintf("AllocateTensors() failed, raise kTensorArenaSize.");
    while (true) {
      delay(1000);
    }
  }
  Serial.println(F("[boot] tensors allocated."));
  input = interpreter->input(0);
  output = interpreter->output(0);

  print_tensor_dims_scale("input", input);
  print_tensor_dims_scale("output", output);

  // ---- RAM breakdown -------------------------------------------------------
  // arena_used_bytes() is exact: how much AllocateTensors() consumed.
  const size_t arena_used   = interpreter->arena_used_bytes();
  const size_t arena_alloc  = static_cast<size_t>(kTensorArenaSize);
  const size_t arena_slack  = arena_alloc - arena_used;
  // Static buffers in BSS (compile-time known).
  const size_t buf_session  = sizeof(g_session_buffer);   // float[kMaxSamples][3]
  const size_t buf_logits   = sizeof(g_trial_logit);      // float[kMaxTrials][6]
  const size_t buf_misc     = sizeof(g_trial_invoke_ms)
                            + sizeof(g_trial_window_conf)
                            + sizeof(g_trial_pred_class)
                            + sizeof(g_confusion);
  const size_t model_flash  = static_cast<size_t>(M3_MODEL_LEN_VAR);
  // nRF52840 has 256 KB SRAM; rough static total (arena + named buffers).
  const size_t static_total = arena_alloc + buf_session + buf_logits + buf_misc;

  Serial.println(F("[mem] --- SRAM breakdown (nRF52840 = 262144 B total) ---"));
  Serial.print(F("[mem]   tensor arena : "));
  Serial.print(static_cast<unsigned long>(arena_alloc));
  Serial.print(F(" B alloc, "));
  Serial.print(static_cast<unsigned long>(arena_used));
  Serial.print(F(" B used, "));
  Serial.print(static_cast<unsigned long>(arena_slack));
  Serial.println(F(" B slack"));
  Serial.print(F("[mem]   session buf  : "));
  Serial.print(static_cast<unsigned long>(buf_session));
  Serial.println(F(" B  (float accel stream)"));
  Serial.print(F("[mem]   trial logits : "));
  Serial.print(static_cast<unsigned long>(buf_logits));
  Serial.println(F(" B  (cumulative window logits)"));
  Serial.print(F("[mem]   trial misc   : "));
  Serial.print(static_cast<unsigned long>(buf_misc));
  Serial.println(F(" B  (invoke_ms, conf, pred_class, confusion)"));
  Serial.print(F("[mem]   static total : "));
  Serial.print(static_cast<unsigned long>(static_total));
  Serial.println(F(" B  (arena + named buffers, excl. stack/BLE)"));
  Serial.print(F("[mem]   model flash  : "));
  Serial.print(static_cast<unsigned long>(model_flash));
  Serial.println(F(" B  (.rodata, not SRAM)"));
  Serial.println(F("[mem] --------------------------------------------------"));
  // --------------------------------------------------------------------------

  Serial.println(F("--- m3_nano_int8_ble_imu ---"));
  Serial.print(F("model_flatbuffer_len="));
  Serial.println(M3_MODEL_LEN_VAR);
  Serial.print(F("config: T="));
  Serial.print(M3_KWINDOW_SIZE);
  Serial.print(F("  model="));
  Serial.println(F(M3_MODEL_SYM_STR));
  Serial.print(F("Control: BLE UI. T="));
  Serial.print(WINDOW_SIZE);
  Serial.print(F(" hop="));
  Serial.print(kWindowHop);
  Serial.println();
  Serial.println();
  Serial.println(
      F("BLE UI: choose GT, START/STOP, then AVERAGE for mean + CM. Serial class input is debug fallback. "
        "Cumulative STOP batches; kMaxSessionTrials cap."));

  // ---- Bring up BLE now (TFLM is fully allocated; BLE/HCI threads can run safely).
  Serial.println(F("[boot] BLE init..."));
  if (!BLE.begin()) {
    Serial.println(F("[BLE] init failed — continuing without BLE."));
  } else {
    BLE.setLocalName("HAR-Nano");
    BLE.setDeviceName("HAR-Nano");
    BLE.setAdvertisedService(g_ble_service);
    g_ble_service.addCharacteristic(g_ble_cmd);
    g_ble_service.addCharacteristic(g_ble_status);
    g_ble_service.addCharacteristic(g_ble_info);
    BLE.addService(g_ble_service);
    {
      uint8_t init_status[4] = {BLE_STATE_IDLE, 0xFF, 0, 0};
      g_ble_status.writeValue(init_status, 4);
    }
    {
      char info_buf[96];
      snprintf(info_buf, sizeof(info_buf), "T=%d hop=%d model=%s",
               WINDOW_SIZE, static_cast<int>(kWindowHop), M3_MODEL_SYM_STR);
      g_ble_info.writeValue(reinterpret_cast<uint8_t*>(info_buf), strlen(info_buf));
    }
    BLE.advertise();
    Serial.print(F("[BLE] advertising as \"HAR-Nano\" ("));
    Serial.print(BLE.address());
    Serial.println(F(")"));
    Serial.println(F("[BLE] cmds: 0x01=START/STOP  0x02=average  0x10..0x15=set GT  0x1F=clear GT"));
  }

  next_sample_ms = millis();
}

void loop() {
  poll_serial_ground_truth();
  poll_ble_commands();

  const uint32_t now = millis();
  if (now < next_sample_ms) {
    return;
  }
  next_sample_ms += kSamplePeriodMs;

  float x, y, z;
  if (!IMU.accelerationAvailable()) {
    return;
  }
  IMU.readAcceleration(x, y, z);

  if (g_recording) {
    if (g_session_n >= kMaxSessionSamples) {
      g_recording = false;
      Serial.println(F("Session buffer full — auto STOP."));
      Serial.println(F("Windowing + inference..."));
      run_sliding_session_inference();
      g_session_n = 0;
      return;
    }
    g_session_buffer[g_session_n][0] = preprocess_accel_axis(x / kAccelScaleDivisor, 0);
    g_session_buffer[g_session_n][1] = preprocess_accel_axis(y / kAccelScaleDivisor, 1);
    g_session_buffer[g_session_n][2] = preprocess_accel_axis(z / kAccelScaleDivisor, 2);
    g_session_n++;
    if (g_session_n == 1 || (g_session_n % WINDOW_SIZE) == 0) {
      const float tsec = (static_cast<float>(g_session_n) * static_cast<float>(kSamplePeriodMs)) /
                         1000.0f;
      Serial.print(F("[REC] n="));
      Serial.print(g_session_n);
      Serial.print(F(" (~"));
      Serial.print(tsec, 0);
      Serial.println(F(" s)"));
    }
  }
}