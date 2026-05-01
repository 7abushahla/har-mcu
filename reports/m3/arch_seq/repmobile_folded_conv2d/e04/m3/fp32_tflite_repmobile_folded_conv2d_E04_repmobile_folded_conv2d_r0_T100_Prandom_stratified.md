# FP32_TFLITE_REPMOBILE_FOLDED_CONV2D_E04_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/repmobile_folded_conv2d/e04/repmobile_folded_conv2d_T100_Prandom_stratified_E04_repmobile_folded_conv2d_r0_fp32.tflite`
- Model size: 93.38 KB
- Accuracy: 0.4867
- Macro-F1: 0.4424

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.114 ms/sample
- Inference latency p95: 0.128 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e04/m3/confusion_fp32_tflite_repmobile_folded_conv2d_E04_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5000, R=0.3939, F1=0.4407, support=264
- Jogging: P=0.9935, R=0.5817, F1=0.7338, support=263
- Upstairs: P=0.4128, R=0.4394, F1=0.4257, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.4300, R=1.0000, F1=0.6014, support=264
- Standing: P=0.4105, R=0.5057, F1=0.4532, support=263
