#include <Arduino.h>
#include <Arduino_LSM9DS1.h>

#include "model_data.h"
#include "norm_stats.h"

#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#ifndef WINDOW_SIZE
#define WINDOW_SIZE 100
#endif

#ifndef NUM_FEATURES
#define NUM_FEATURES 3
#endif

#ifndef NUM_CLASSES
#define NUM_CLASSES 6
#endif

#ifndef SAMPLE_RATE_HZ
#define SAMPLE_RATE_HZ 20
#endif

#ifndef APPLY_NORMALIZATION
#define APPLY_NORMALIZATION 1
#endif

#ifndef UNIT_PRE_MULTIPLY
#define UNIT_PRE_MULTIPLY 1.0f
#endif

#ifndef UNIT_SCALE
#define UNIT_SCALE 1.0f
#endif

constexpr int kSampleRateHz = SAMPLE_RATE_HZ;
constexpr uint32_t kSamplePeriodUs = 1000000UL / SAMPLE_RATE_HZ;
constexpr int kHopSize = WINDOW_SIZE / 2;
constexpr int kTensorArenaSize = 64 * 1024;

// If your Arduino TFLM package is older and misses one of the methods below,
// set this to 0 and rebuild. The deploy gate in Python follows upstream
// micro_mutable_op_resolver.h capability semantics.
#ifndef HAR_TFLM_ENABLE_MICRO_MUTABLE_ONLY_EXTRA_OPS
#define HAR_TFLM_ENABLE_MICRO_MUTABLE_ONLY_EXTRA_OPS 1
#endif

const char* kClassNames[NUM_CLASSES] = {
  "Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"
};

float ring_buffer[WINDOW_SIZE][NUM_FEATURES];
int ring_head = 0;
int samples_seen = 0;
int samples_since_last_infer = 0;
uint32_t next_sample_us = 0;
uint32_t inference_count = 0;
float invoke_ms_sum = 0.0f;

namespace {
tflite::MicroErrorReporter micro_error_reporter;
tflite::ErrorReporter* error_reporter = &micro_error_reporter;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

void setup_model() {
  model = tflite::GetModel(g_model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    error_reporter->Report("Model schema mismatch");
    return;
  }

  static tflite::MicroMutableOpResolver<36> resolver;
  resolver.AddConv2D();
  resolver.AddDepthwiseConv2D();
  resolver.AddMaxPool2D();
  resolver.AddMean();
  resolver.AddReshape();
  resolver.AddFullyConnected();
  resolver.AddSoftmax();
  resolver.AddStridedSlice();
  resolver.AddPack();
  resolver.AddShape();
  resolver.AddTranspose();
  resolver.AddMul();
  resolver.AddAdd();
  resolver.AddLogistic();
  resolver.AddTanh();
  resolver.AddQuantize();
  resolver.AddDequantize();
  resolver.AddUnidirectionalSequenceLSTM();
#if HAR_TFLM_ENABLE_MICRO_MUTABLE_ONLY_EXTRA_OPS
  resolver.AddBatchMatMul();
  resolver.AddBatchToSpaceND();
  resolver.AddSpaceToBatchNd();
  resolver.AddConcatenation();
  resolver.AddFill();
  resolver.AddPad();
  resolver.AddRsqrt();
  resolver.AddSquaredDifference();
  resolver.AddSub();
#endif

  static tflite::MicroInterpreter static_interpreter(
      model, resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    error_reporter->Report("AllocateTensors failed");
    return;
  }

  input = interpreter->input(0);
  output = interpreter->output(0);

  Serial.print("tensor_arena_bytes=");
  Serial.println(kTensorArenaSize);
}

float normalize_value(float v, int axis) {
#if APPLY_NORMALIZATION
  return (v - kNormMean[axis]) / kNormStd[axis];
#else
  (void)axis;
  return v;
#endif
}

void push_sample(float x, float y, float z) {
  x = x * UNIT_PRE_MULTIPLY * UNIT_SCALE;
  y = y * UNIT_PRE_MULTIPLY * UNIT_SCALE;
  z = z * UNIT_PRE_MULTIPLY * UNIT_SCALE;
  ring_buffer[ring_head][0] = normalize_value(x, 0);
  ring_buffer[ring_head][1] = normalize_value(y, 1);
  ring_buffer[ring_head][2] = normalize_value(z, 2);
  ring_head = (ring_head + 1) % WINDOW_SIZE;
  samples_seen++;
  samples_since_last_infer++;
}

void fill_model_input_from_ring() {
  const int input_zero_point = input->params.zero_point;
  const float input_scale = input->params.scale;

  int idx = ring_head;
  for (int t = 0; t < WINDOW_SIZE; ++t) {
    for (int a = 0; a < NUM_FEATURES; ++a) {
      float v = ring_buffer[idx][a];
      int q = static_cast<int>(round(v / input_scale) + input_zero_point);
      if (q < -128) q = -128;
      if (q > 127) q = 127;
      input->data.int8[t * NUM_FEATURES + a] = static_cast<int8_t>(q);
    }
    idx = (idx + 1) % WINDOW_SIZE;
  }
}

void run_inference() {
  if (samples_seen < WINDOW_SIZE || samples_since_last_infer < kHopSize) {
    return;
  }

  samples_since_last_infer = 0;
  fill_model_input_from_ring();

  const uint32_t invoke_start = micros();
  TfLiteStatus status = interpreter->Invoke();
  const uint32_t invoke_us = micros() - invoke_start;

  if (status != kTfLiteOk) {
    Serial.println("invoke_failed");
    return;
  }

  int best_idx = 0;
  int8_t best_q = output->data.int8[0];
  for (int i = 1; i < NUM_CLASSES; ++i) {
    if (output->data.int8[i] > best_q) {
      best_q = output->data.int8[i];
      best_idx = i;
    }
  }

  float conf = (static_cast<float>(best_q - output->params.zero_point)) * output->params.scale;
  float buffering_ms = 1000.0f * static_cast<float>(WINDOW_SIZE) / static_cast<float>(kSampleRateHz);
  float invoke_ms = invoke_us / 1000.0f;
  float end_to_end_ms = buffering_ms + invoke_ms;

  inference_count++;
  invoke_ms_sum += invoke_ms;

  Serial.print(millis());
  Serial.print(",");
  Serial.print(kClassNames[best_idx]);
  Serial.print(",");
  Serial.print(conf, 4);
  Serial.print(",");
  Serial.print(invoke_ms, 3);
  Serial.print(",");
  Serial.println(end_to_end_ms, 3);

  if (inference_count == 50 || (inference_count > 50 && inference_count % 50 == 0)) {
    Serial.print("avg_invoke_ms=");
    Serial.print(invoke_ms_sum / static_cast<float>(inference_count), 3);
    Serial.print(",inferences=");
    Serial.println(inference_count);
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  if (!IMU.begin()) {
    Serial.println("imu_init_failed");
    while (1) {
      delay(1000);
    }
  }

  setup_model();
  Serial.print("sample_rate_hz=");
  Serial.println(kSampleRateHz);
  Serial.print("unit_pre_multiply=");
  Serial.println(UNIT_PRE_MULTIPLY, 6);
  Serial.print("unit_scale=");
  Serial.println(UNIT_SCALE, 6);
  Serial.print("apply_normalization=");
  Serial.println(APPLY_NORMALIZATION);
  Serial.println("timestamp_ms,label,confidence,invoke_ms,e2e_ms");
  Serial.println("ready");
  next_sample_us = micros();
}

void loop() {
  const uint32_t now = micros();
  if (static_cast<int32_t>(now - next_sample_us) < 0) {
    return;
  }
  next_sample_us += kSamplePeriodUs;

  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    push_sample(x, y, z);
    run_inference();
  }
}
