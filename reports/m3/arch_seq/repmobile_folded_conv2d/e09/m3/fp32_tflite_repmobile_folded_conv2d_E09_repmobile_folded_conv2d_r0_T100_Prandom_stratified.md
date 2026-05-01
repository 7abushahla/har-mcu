# FP32_TFLITE_REPMOBILE_FOLDED_CONV2D_E09_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_seq/repmobile_folded_conv2d/e09/repmobile_folded_conv2d_T100_Prandom_stratified_E09_repmobile_folded_conv2d_r0_fp32.tflite`
- Model size: 93.38 KB
- Accuracy: 0.9791
- Macro-F1: 0.9792

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.113 ms/sample
- Inference latency p95: 0.140 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e09/m3/confusion_fp32_tflite_repmobile_folded_conv2d_E09_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=1.0000, F1=0.9925, support=264
- Jogging: P=1.0000, R=0.9886, F1=0.9943, support=263
- Upstairs: P=0.9088, R=0.9811, F1=0.9435, support=264
- Downstairs: P=0.9876, R=0.9053, F1=0.9447, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
