# QAT_REPMOBILE_FOLDED_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 46.91 KB
- Accuracy: 0.8071
- Macro-F1: 0.6032

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.542 ms/sample
- Inference latency p95: 0.600 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_qat_repmobile_folded_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7361, R=0.9881, F1=0.8437, support=1344
- Jogging: P=0.9689, R=0.9624, F1=0.9657, support=1037
- Upstairs: P=0.4808, R=0.0762, F1=0.1316, support=328
- Downstairs: P=0.5000, R=0.0078, F1=0.0154, support=256
- Sitting: P=0.8284, R=0.9286, F1=0.8756, support=182
- Standing: P=0.6818, R=0.9310, F1=0.7872, support=145
