# FP32_TFLITE_DAGHERO_CNN_2LAYER_CONV2D_E05_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.5088
- Macro-F1: 0.4498

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.040 ms/sample
- Inference latency p95: 0.048 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/daghero_cnn_2layer_conv2d/e05/m3/confusion_fp32_tflite_daghero_cnn_2layer_conv2d_E05_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6500, R=0.0492, F1=0.0915, support=264
- Jogging: P=1.0000, R=0.5133, F1=0.6784, support=263
- Upstairs: P=0.2897, R=0.9811, F1=0.4473, support=264
- Downstairs: P=0.1667, R=0.0038, F1=0.0074, support=264
- Sitting: P=0.6701, R=1.0000, F1=0.8024, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
