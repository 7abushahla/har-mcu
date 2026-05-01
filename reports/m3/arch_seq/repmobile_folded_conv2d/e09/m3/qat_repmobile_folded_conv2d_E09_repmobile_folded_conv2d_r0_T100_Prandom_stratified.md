# QAT_REPMOBILE_FOLDED_CONV2D_E09_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_seq/repmobile_folded_conv2d/e09/repmobile_folded_conv2d_T100_Prandom_stratified_E09_repmobile_folded_conv2d_r0_qat.tflite`
- Model size: 43.26 KB
- Accuracy: 0.9703
- Macro-F1: 0.9703

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.324 ms/sample
- Inference latency p95: 0.365 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e09/m3/confusion_qat_repmobile_folded_conv2d_E09_repmobile_folded_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=1.0000, F1=0.9962, support=264
- Jogging: P=1.0000, R=0.9810, F1=0.9904, support=263
- Upstairs: P=0.8638, R=0.9848, F1=0.9204, support=264
- Downstairs: P=0.9826, R=0.8561, F1=0.9150, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
