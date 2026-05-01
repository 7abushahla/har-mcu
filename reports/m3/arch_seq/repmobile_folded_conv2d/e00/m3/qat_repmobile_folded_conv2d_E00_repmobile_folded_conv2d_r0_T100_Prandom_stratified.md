# QAT_REPMOBILE_FOLDED_CONV2D_E00_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/repmobile_folded_conv2d/e00/repmobile_folded_conv2d_T100_Prandom_stratified_E00_repmobile_folded_conv2d_r0_qat.tflite`
- Model size: 43.26 KB
- Accuracy: 0.9536
- Macro-F1: 0.9340

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.327 ms/sample
- Inference latency p95: 0.367 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e00/m3/confusion_qat_repmobile_folded_conv2d_E00_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9772, R=0.9919, F1=0.9845, support=2723
- Jogging: P=0.9990, R=0.9483, F1=0.9730, support=2109
- Upstairs: P=0.8778, R=0.8562, F1=0.8669, support=730
- Downstairs: P=0.7828, R=0.8842, F1=0.8304, support=587
- Sitting: P=1.0000, R=0.9659, F1=0.9826, support=381
- Standing: P=0.9354, R=1.0000, F1=0.9666, support=304
