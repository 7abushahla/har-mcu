# FP32_TFLITE_REPMOBILE_FOLDED_CONV2D_E00_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/repmobile_folded_conv2d/e00/repmobile_folded_conv2d_T100_Prandom_stratified_E00_repmobile_folded_conv2d_r0_fp32.tflite`
- Model size: 93.38 KB
- Accuracy: 0.9416
- Macro-F1: 0.9152

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.114 ms/sample
- Inference latency p95: 0.147 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e00/m3/confusion_fp32_tflite_repmobile_folded_conv2d_E00_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9471, R=0.9930, F1=0.9695, support=2723
- Jogging: P=0.9893, R=0.9640, F1=0.9765, support=2109
- Upstairs: P=0.8439, R=0.8000, F1=0.8214, support=730
- Downstairs: P=0.8396, R=0.7581, F1=0.7968, support=587
- Sitting: P=1.0000, R=0.9580, F1=0.9786, support=381
- Standing: P=0.9021, R=1.0000, F1=0.9485, support=304
