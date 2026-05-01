# PTQ_REPMOBILE_FOLDED_CONV2D_E05_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/repmobile_folded_conv2d/e05/repmobile_folded_conv2d_T100_Prandom_stratified_E05_repmobile_folded_conv2d_r0_ptq_int8.tflite`
- Model size: 42.12 KB
- Accuracy: 0.4633
- Macro-F1: 0.4181

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.326 ms/sample
- Inference latency p95: 0.342 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e05/m3/confusion_ptq_repmobile_folded_conv2d_E05_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5000, R=0.3977, F1=0.4430, support=264
- Jogging: P=1.0000, R=0.4373, F1=0.6085, support=263
- Upstairs: P=0.3779, R=0.4394, F1=0.4063, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.4251, R=1.0000, F1=0.5966, support=264
- Standing: P=0.4118, R=0.5057, F1=0.4539, support=263
