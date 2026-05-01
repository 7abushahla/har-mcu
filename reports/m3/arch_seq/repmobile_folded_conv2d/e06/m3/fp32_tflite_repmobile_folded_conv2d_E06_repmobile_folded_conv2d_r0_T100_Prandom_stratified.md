# FP32_TFLITE_REPMOBILE_FOLDED_CONV2D_E06_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E06_no_norm_matched/arch_seq/repmobile_folded_conv2d/e06/repmobile_folded_conv2d_T100_Prandom_stratified_E06_repmobile_folded_conv2d_r0_fp32.tflite`
- Model size: 93.38 KB
- Accuracy: 0.1669
- Macro-F1: 0.0477

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.114 ms/sample
- Inference latency p95: 0.140 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e06/m3/confusion_fp32_tflite_repmobile_folded_conv2d_E06_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1669, R=1.0000, F1=0.2860, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
