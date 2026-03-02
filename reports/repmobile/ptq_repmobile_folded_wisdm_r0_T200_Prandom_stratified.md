# PTQ_REPMOBILE_FOLDED_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 46.66 KB
- Accuracy: 0.7688
- Macro-F1: 0.5749

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.186 ms/sample
- Inference latency p95: 0.240 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_ptq_repmobile_folded_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6522, R=0.9918, F1=0.7869, support=1344
- Jogging: P=0.9649, R=0.9026, F1=0.9327, support=1037
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=328
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=256
- Sitting: P=0.9408, R=0.8736, F1=0.9060, support=182
- Standing: P=0.9810, R=0.7103, F1=0.8240, support=145
