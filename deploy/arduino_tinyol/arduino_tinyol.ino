#include <Arduino.h>

#include "model_data.h"
#include "norm_stats.h"

#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#ifndef EMBEDDING_DIM
#define EMBEDDING_DIM 128
#endif

#ifndef NUM_CLASSES
#define NUM_CLASSES 6
#endif

constexpr int kTensorArenaSize = 64 * 1024;

float head_w[NUM_CLASSES][EMBEDDING_DIM];
float head_b[NUM_CLASSES];

namespace {
tflite::MicroErrorReporter micro_error_reporter;
tflite::ErrorReporter* error_reporter = &micro_error_reporter;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;
TfLiteTensor* output = nullptr;
uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

void init_head() {
  for (int c = 0; c < NUM_CLASSES; ++c) {
    head_b[c] = 0.0f;
    for (int i = 0; i < EMBEDDING_DIM; ++i) {
      head_w[c][i] = 0.0f;
    }
  }
}

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
  output = interpreter->output(0);  // expected embedding output for TinyOL variant
}

int predict_head(const float* emb) {
  int best = 0;
  float best_score = -1e9f;
  for (int c = 0; c < NUM_CLASSES; ++c) {
    float s = head_b[c];
    for (int i = 0; i < EMBEDDING_DIM; ++i) {
      s += head_w[c][i] * emb[i];
    }
    if (s > best_score) {
      best_score = s;
      best = c;
    }
  }
  return best;
}

void sgd_update(const float* emb, int label, float lr) {
  for (int c = 0; c < NUM_CLASSES; ++c) {
    float target = (c == label) ? 1.0f : 0.0f;
    float pred = (c == label) ? 1.0f : 0.0f;  // simple perceptron-style update baseline
    float grad = (pred - target);
    for (int i = 0; i < EMBEDDING_DIM; ++i) {
      head_w[c][i] -= lr * grad * emb[i];
    }
    head_b[c] -= lr * grad;
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }
  init_head();
  setup_model();
  Serial.println("tinyol_ready");
  Serial.println("send: label=<0..5> to apply one online update using last embedding");
}

float last_embedding[EMBEDDING_DIM];
bool has_last_embedding = false;

void loop() {
  // Placeholder: feed real normalized window input into model and invoke.
  // Here we only react to serial updates for TinyOL head demonstration.
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();
    if (line.startsWith("label=")) {
      int label = line.substring(6).toInt();
      if (label >= 0 && label < NUM_CLASSES && has_last_embedding) {
        uint32_t t0 = micros();
        sgd_update(last_embedding, label, 0.01f);
        uint32_t dt = micros() - t0;
        Serial.print("tinyol_update_us=");
        Serial.println(dt);
      }
    }
  }
}
