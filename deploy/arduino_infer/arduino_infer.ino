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

constexpr int kSampleRateHz = 20;
constexpr int kHopSize = WINDOW_SIZE / 2;
constexpr int kTensorArenaSize = 64 * 1024;

const char* kClassNames[NUM_CLASSES] = {
  "Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"
};

float ring_buffer[WINDOW_SIZE][NUM_FEATURES];
int ring_head = 0;
int samples_seen = 0;
int samples_since_last_infer = 0;

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

  static tflite::MicroMutableOpResolver<16> resolver;
  resolver.AddConv2D();
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
  return (v - kNormMean[axis]) / kNormStd[axis];
}

void push_sample(float x, float y, float z) {
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
  float end_to_end_ms = buffering_ms + (invoke_us / 1000.0f);

  Serial.print("label=");
  Serial.print(kClassNames[best_idx]);
  Serial.print(",confidence=");
  Serial.print(conf, 4);
  Serial.print(",invoke_ms=");
  Serial.print(invoke_us / 1000.0f, 3);
  Serial.print(",e2e_ms=");
  Serial.println(end_to_end_ms, 3);
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
  Serial.println("ready");
}

void loop() {
  float x, y, z;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);
    push_sample(x, y, z);
    run_inference();
  }
}
