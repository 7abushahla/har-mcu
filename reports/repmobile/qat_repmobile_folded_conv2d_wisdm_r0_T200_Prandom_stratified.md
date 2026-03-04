# QAT_REPMOBILE_FOLDED_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 46.91 KB
- Accuracy: 0.8074
- Macro-F1: 0.6037

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 11
- Interpreter ops: `['ADD', 'CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PACK', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'STRIDED_SLICE']`
- Inference latency median: 0.528 ms/sample
- Inference latency p95: 0.548 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_qat_repmobile_folded_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7345, R=0.9881, F1=0.8426, support=1344
- Jogging: P=0.9690, R=0.9634, F1=0.9662, support=1037
- Upstairs: P=0.5000, R=0.0823, F1=0.1414, support=328
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=256
- Sitting: P=0.8244, R=0.9286, F1=0.8734, support=182
- Standing: P=0.6995, R=0.9310, F1=0.7988, support=145
