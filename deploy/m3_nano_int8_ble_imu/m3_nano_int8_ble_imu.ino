// M3 HAR INT8 (BLE + LIVE IMU) — Nano 33 BLE. BLE remote control + optional TinyML shield button.
// Session → windowing matches offline pipeline.
//
// BLE service "HAR Control" (UUID 19B10000-E8F2-537E-4F6C-D104768A1214):
//   cmd  characteristic (write, UUID ...0001): 0x01=click(toggle START/STOP), 0x02=long-hold avg
//   status characteristic (notify, UUID ...0002): 1 byte state + 1 byte last pred class
//     byte[0]: 0=idle, 1=recording  byte[1]: last predicted class index (0–5, 0xFF if none)
//
// Physical button still works alongside BLE (set kUseTinyMLShield = true/false as before).
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
#include <mbed.h>
#include <rtos.h>
#include <ArduinoBLE.h>
#include <TensorFlowLite.h>
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_log.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include <Arduino_LSM9DS1.h>
#include "tinyml_shield.h"

// -------- BLE service / characteristic UUIDs --------
#define BLE_SERVICE_UUID  "19B10000-E8F2-537E-4F6C-D104768A1214"
#define BLE_CMD_UUID      "19B10001-E8F2-537E-4F6C-D104768A1214"
#define BLE_STATUS_UUID   "19B10002-E8F2-537E-4F6C-D104768A1214"
// cmd values from desktop app:
#define BLE_CMD_CLICK     0x01   // toggle START / STOP
#define BLE_CMD_LONGHOLD  0x02   // average buffered trials
// status byte[0] values sent to desktop app:
#define BLE_STATE_IDLE    0x00
#define BLE_STATE_REC     0x01

// ======== Edit these three lines, then compile + flash ============================
#include "m3_daghero_finetune_t100_qat_int8.h"
#define M3_MODEL_SYM    m3_daghero_finetune_t100_qat_int8
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
const int kTensorArenaSize = 70 * 1024;
const int kWindowHop = M3_KWINDOW_HOP;
// Max length of one START…STOP run. ArduinoBLE library + TFLM arena leave very little
// SRAM on Nano 33 BLE — keep this small. 500 samples = 25 s @ 20 Hz (or 5 s @ 100 Hz).
// 500 * 3 * 4 = 6 KB.
const int kMaxSessionSamples = 300;
// Cumulative logit cap (multiple STOP batches stack until full). 16 * 6 * 4 = 0.4 KB.
const int kMaxSessionTrials = 16;
// Press+release < this → one START/STOP **toggle** (on release, not on down).
const uint32_t kShortClickMaxMs = 350U;
// Hold this long to trigger “average last session trials” (mean logits) once per hold.
const uint32_t kLongPressAvgMs = 2500U;

const int kSampleRateHz = LIVE_SAMPLE_RATE_HZ;
const uint32_t kSamplePeriodMs = 1000U / static_cast<uint32_t>(kSampleRateHz);
const bool kUseTinyMLShield = true;
const int kUserButtonPin = 7;
const uint32_t kButtonDebounceMs = 50;
const bool kUseImuContinuousMode = false;
// Training CSV came from tf4micro-motion-kit captures: stored accelerometer = readAcceleration(g) / 4.
// Arduino_LSM9DS1::readAcceleration() returns g, so divide by 4 before applying train z-score.
const float kAccelScaleDivisor = 4.0f;


static const char* const kClassNames[NUM_CLASSES] = {
    "Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"};
// Short labels for confusion matrix columns (rows = true GT, cols = pred).
static const char* const kClassAbr[NUM_CLASSES] = {"Walk", "Jog", "Upsz", "Dnsz", "Sit", "Stnd"};

// Ground truth: set in Serial (class name or 0–5) **before** START. Snapshot at each START.
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
// Arena lives on the HEAP (allocated in setup), not BSS — frees up static memory
// and avoids BSS layout collisions with ArduinoBLE's static buffers on Nano 33 BLE.
uint8_t* tensor_arena = nullptr;
}  // namespace

// Approximate free-heap probe (works on mbed-os via the libc sbrk hook).
extern "C" char* sbrk(int incr);
static int free_heap_bytes() {
  char top;
  return &top - reinterpret_cast<char*>(sbrk(0));
}

// BLE state — declared early so inference functions can reference them.
static uint8_t g_ble_last_pred_class = 0xFF;
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
  if (kUseTinyMLShield || kUserButtonPin == 13) {
#if defined(LEDR)
    pinMode(LEDR, OUTPUT);
    digitalWrite(LEDR, on ? LOW : HIGH);
#endif
  } else {
    digitalWrite(LED_BUILTIN, on ? HIGH : LOW);
  }
}

static void init_status_leds() {
  if (kUseTinyMLShield || kUserButtonPin == 13) {
#if defined(LEDR)
    pinMode(LEDR, OUTPUT);
    digitalWrite(LEDR, HIGH);
#endif
  } else {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
  }
}

static void clear_tensor_arena() {
  if (tensor_arena == nullptr) {
    return;
  }
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
  // Minimal op set for Daghero (CNN) and DeepConvLSTM (CNN + LSTM) INT8 models.
  // MicroMutableOpResolver is much lighter than AllOpsResolver — important when
  // ArduinoBLE is linked, since the BLE/HCI stack steals RAM at runtime.
  static tflite::MicroMutableOpResolver<20> resolver;
  resolver.AddConv2D();
  resolver.AddDepthwiseConv2D();
  resolver.AddFullyConnected();
  resolver.AddMaxPool2D();
  resolver.AddAveragePool2D();
  resolver.AddReshape();
  resolver.AddSoftmax();
  resolver.AddRelu();
  resolver.AddLogistic();
  resolver.AddTanh();
  resolver.AddQuantize();
  resolver.AddDequantize();
  resolver.AddUnidirectionalSequenceLSTM();
  resolver.AddTransposeConv();
  resolver.AddMean();
  resolver.AddPad();
  resolver.AddAdd();
  resolver.AddMul();
  resolver.AddConcatenation();
  resolver.AddStridedSlice();

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
  Serial.println(F("%"));
  g_ble_last_pred_class = static_cast<uint8_t>(best);
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
BLECharacteristic g_ble_status(BLE_STATUS_UUID, BLERead | BLENotify, 2);

static void ble_update_status() {
  uint8_t buf[2] = {
      g_recording ? BLE_STATE_REC : BLE_STATE_IDLE,
      g_ble_last_pred_class};
  g_ble_status.writeValue(buf, 2);
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
  if (cmd == BLE_CMD_CLICK) {
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
    ble_update_status();
  } else if (cmd == BLE_CMD_LONGHOLD) {
    Serial.println(F(">>> [BLE] long-hold: averaging buffered trials <<<"));
    run_averaging_of_buffered_trials();
    ble_update_status();
  }
}

// -------- Debounced: true while the physical button is held (shield D13: active low; manual: LOW).
static bool read_button_steady_pressed() {
  const int r =
      kUseTinyMLShield ? (readShieldButtonDown() ? LOW : HIGH) : digitalRead(kUserButtonPin);
  static int last_raw = r;
  static int steady = r;
  static uint32_t last_raw_ch = 0;
  const uint32_t now = millis();
  if (r != last_raw) {
    last_raw = r;
    last_raw_ch = now;
  }
  if (static_cast<uint32_t>(now - last_raw_ch) < kButtonDebounceMs) {
    return (steady == LOW);
  }
  if (r != steady) {
    steady = r;
  }
  return (steady == LOW);
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
    g_ble_last_pred_class = static_cast<uint8_t>(best);
    ble_update_status();
    Serial.print(F(">>> HOLD_AVERAGE: n="));
    Serial.print(n0);
    Serial.print(F(" mean_logits → pred="));
    Serial.print(kClassNames[best]);
    Serial.print(F(" conf="));
    Serial.print(conf, 1);
    Serial.println(F("%  (softmax of mean logits)"));
    Serial.print(F("    per_trial mean: invoke_ms="));
    Serial.print(mean_ms, 2);
    Serial.print(F("  window_conf="));
    Serial.print(mean_win_conf, 1);
    Serial.print(F("%  majority="));
    Serial.print(kClassNames[majority]);
    Serial.print(F(" ("));
    Serial.print(vote_count[majority]);
    Serial.print(F("/"));
    Serial.print(n0);
    Serial.println(F(")"));
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

// Short press+release: toggle START / STOP+sliding. Long hold: average buffered trials;
// does not run START/STOP.
static void poll_shield_holds_and_clicks() {
  const bool down = read_button_steady_pressed();
  static bool prev = false;
  static uint32_t t_down = 0;
  static bool long_fired = false;
  const uint32_t now = millis();

  if (down && !prev) {
    t_down = now;
    long_fired = false;
  }
  if (down) {
    if (!long_fired && (uint32_t)(now - t_down) >= kLongPressAvgMs) {
      long_fired = true;
      run_averaging_of_buffered_trials();
    }
  } else if (prev) {
    const uint32_t dur = (uint32_t)(now - t_down);
    if (!long_fired && dur < kShortClickMaxMs) {
      if (!g_recording) {
        g_session_n = 0;
        g_session_gt = g_ground_truth;
        g_recording = true;
        Serial.println();
        if (g_session_gt < 0) {
          Serial.println(
              F(">>> [GT] not set: confusion matrix will not count this run. Type class name, "
                "e.g. Walking, then START again, or type help. <<<"));
        } else {
          Serial.print(F(">>> [GT] for this record = "));
          Serial.print(kClassNames[static_cast<int>(g_session_gt)]);
          Serial.println();
        }
        Serial.println(
            F(">>> REC — move, then short press+release to STOP and run sliding windows. <<<"));
      } else {
        g_recording = false;
        Serial.print(F(">>> STOP — "));
        Serial.print(g_session_n);
        Serial.println(F(" samples, windowing + inference..."));
        run_sliding_session_inference();
        g_session_n = 0;
      }
    }
  }
  prev = down;
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

  if (kUseTinyMLShield) {
    initializeShield();
  } else {
    pinMode(kUserButtonPin, INPUT_PULLUP);
  }
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

  // ---- Allocate the tensor arena on the HEAP (not BSS).
  Serial.print(F("[boot] free heap before arena malloc = "));
  Serial.println(free_heap_bytes());
  Serial.print(F("[boot] mallocing arena = "));
  Serial.print(static_cast<unsigned long>(kTensorArenaSize));
  Serial.println(F(" bytes (16-byte aligned)..."));
  Serial.flush();

  // 16-byte aligned malloc (TFLM requires the arena be aligned).
  void* raw = malloc(kTensorArenaSize + 16);
  if (raw == nullptr) {
    Serial.println(F("[boot] FATAL: malloc(tensor_arena) returned NULL"));
    Serial.flush();
    while (true) {
      delay(1000);
    }
  }
  uintptr_t addr = reinterpret_cast<uintptr_t>(raw);
  uintptr_t aligned = (addr + 15) & ~uintptr_t(15);
  tensor_arena = reinterpret_cast<uint8_t*>(aligned);
  Serial.print(F("[boot] arena malloc OK at 0x"));
  Serial.println(static_cast<unsigned long>(aligned), HEX);
  Serial.print(F("[boot] free heap after arena malloc  = "));
  Serial.println(free_heap_bytes());
  Serial.flush();

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
  Serial.println(F("[boot] allocate tensors (on 24KB-stack worker thread)..."));
  Serial.flush();
  delay(50);

  // Main mbed-os thread stack on Nano 33 BLE is ~4KB — TFLM's op-planner can
  // recurse deeper than that on models with MEAN / DepthwiseConv / etc., which
  // hard-faults silently. Spawn a dedicated thread with a larger stack just
  // for AllocateTensors().
  static volatile TfLiteStatus alloc_rc = kTfLiteError;
  static volatile bool alloc_started = false;
  static volatile bool alloc_finished = false;
  rtos::Thread alloc_thread(osPriorityNormal, /* stack */ 24 * 1024);
  alloc_thread.start([]() {
    alloc_started = true;
    alloc_rc = interpreter->AllocateTensors();
    alloc_finished = true;
  });

  // Poll while AllocateTensors runs so we can tell if it's making progress
  // or stuck. Time out after 30 s and report.
  const uint32_t t_alloc0 = millis();
  while (!alloc_finished && (millis() - t_alloc0 < 30000)) {
    rtos::ThisThread::sleep_for(500);
    Serial.print(F("[boot]   ... still running (started="));
    Serial.print(alloc_started ? 1 : 0);
    Serial.print(F(", elapsed="));
    Serial.print(millis() - t_alloc0);
    Serial.println(F(" ms)"));
    Serial.flush();
  }

  if (!alloc_finished) {
    Serial.println(F("[boot] AllocateTensors() TIMED OUT after 30 s — likely hard fault"));
    Serial.print(F("[boot]   thread started? "));
    Serial.println(alloc_started ? F("yes") : F("no"));
    Serial.flush();
    while (true) {
      delay(1000);
    }
  }
  alloc_thread.join();

  Serial.print(F("[boot] AllocateTensors() returned rc="));
  Serial.println(static_cast<int>(alloc_rc));
  Serial.flush();
  if (alloc_rc != kTfLiteOk) {
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
  Serial.print(F("[tensor] arena_bytes="));
  Serial.println(static_cast<unsigned long>(kTensorArenaSize));

  Serial.println(F("--- m3_nano_int8_live_imu ---"));
  Serial.print(F("model_flatbuffer_len="));
  Serial.println(M3_MODEL_LEN_VAR);
  Serial.print(F("config: T="));
  Serial.print(M3_KWINDOW_SIZE);
  Serial.print(F("  model="));
  Serial.println(F(M3_MODEL_SYM_STR));
  if (kUseTinyMLShield) {
    Serial.print(F("Shield: tinyml_shield (not Harvard TFL package). T="));
  } else {
    Serial.print(F("Button: D"));
    Serial.print(kUserButtonPin);
    Serial.print(F("  T="));
  }
  Serial.print(WINDOW_SIZE);
  Serial.print(F(" hop="));
  Serial.print(kWindowHop);
  Serial.println();
  Serial.println();
  Serial.println(
      F("Serial: type class name (Walking… or 0-5) before START, then long-hold for mean + CM. "
        "Cumulative STOP batches; kMaxSessionTrials cap."));

  // ---- Bring up BLE now (TFLM is fully allocated; BLE/HCI threads can run safely).
  Serial.println(F("[boot] BLE init..."));
  if (!BLE.begin()) {
    Serial.println(F("[BLE] init failed — continuing without BLE."));
  } else {
    BLE.setLocalName("HAR-Nano");
    BLE.setAdvertisedService(g_ble_service);
    g_ble_service.addCharacteristic(g_ble_cmd);
    g_ble_service.addCharacteristic(g_ble_status);
    BLE.addService(g_ble_service);
    {
      uint8_t init_status[2] = {BLE_STATE_IDLE, 0xFF};
      g_ble_status.writeValue(init_status, 2);
    }
    BLE.advertise();
    Serial.print(F("[BLE] advertising as \"HAR-Nano\" ("));
    Serial.print(BLE.address());
    Serial.println(F(")"));
    Serial.println(F("[BLE] cmds: 0x01=START/STOP toggle  0x02=long-hold avg"));
  }

  next_sample_ms = millis();
}

void loop() {
  poll_serial_ground_truth();
  poll_ble_commands();
  poll_shield_holds_and_clicks();

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
