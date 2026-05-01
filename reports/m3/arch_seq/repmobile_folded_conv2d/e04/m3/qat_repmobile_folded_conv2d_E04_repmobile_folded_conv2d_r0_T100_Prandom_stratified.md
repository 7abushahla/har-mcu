# QAT_REPMOBILE_FOLDED_CONV2D_E04_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/repmobile_folded_conv2d/e04/repmobile_folded_conv2d_T100_Prandom_stratified_E04_repmobile_folded_conv2d_r0_qat.tflite`
- Model size: 43.26 KB
- Accuracy: 0.4223
- Macro-F1: 0.3733

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.327 ms/sample
- Inference latency p95: 0.361 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e04/m3/confusion_qat_repmobile_folded_conv2d_E04_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8710, R=0.2045, F1=0.3313, support=264
- Jogging: P=1.0000, R=0.3726, F1=0.5429, support=263
- Upstairs: P=0.2729, R=0.4508, F1=0.3400, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.3970, R=1.0000, F1=0.5684, support=264
- Standing: P=0.4169, R=0.5057, F1=0.4570, support=263
