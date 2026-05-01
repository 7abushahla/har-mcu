# QAT_DAGHERO_CNN_2LAYER_CONV2D_E05_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.5070
- Macro-F1: 0.4459

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.075 ms/sample
- Inference latency p95: 0.091 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/daghero_cnn_2layer_conv2d/e05/m3/confusion_qat_daghero_cnn_2layer_conv2d_E05_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6923, R=0.0341, F1=0.0650, support=264
- Jogging: P=1.0000, R=0.5095, F1=0.6751, support=263
- Upstairs: P=0.2886, R=0.9848, F1=0.4464, support=264
- Downstairs: P=0.2857, R=0.0076, F1=0.0148, support=264
- Sitting: P=0.6701, R=1.0000, F1=0.8024, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
