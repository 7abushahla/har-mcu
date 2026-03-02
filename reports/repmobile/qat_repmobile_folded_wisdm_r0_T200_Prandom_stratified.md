# QAT_REPMOBILE_FOLDED_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 46.77 KB
- Accuracy: 0.8095
- Macro-F1: 0.6120

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.183 ms/sample
- Inference latency p95: 0.198 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_qat_repmobile_folded_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7375, R=0.9866, F1=0.8440, support=1344
- Jogging: P=0.9727, R=0.9624, F1=0.9675, support=1037
- Upstairs: P=0.4857, R=0.1037, F1=0.1709, support=328
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=256
- Sitting: P=0.8450, R=0.9286, F1=0.8848, support=182
- Standing: P=0.6970, R=0.9517, F1=0.8047, support=145
