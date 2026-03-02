# PTQ_XTINYHAR_STUDENT_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 116.09 KB
- Accuracy: 0.9171
- Macro-F1: 0.8715

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.187 ms/sample
- Inference latency p95: 0.222 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_ptq_xtinyhar_student_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9171, R=0.9717, F1=0.9436, support=1344
- Jogging: P=0.9716, R=0.9884, F1=0.9799, support=1037
- Upstairs: P=0.7687, R=0.6890, F1=0.7267, support=328
- Downstairs: P=0.7701, R=0.5625, F1=0.6501, support=256
- Sitting: P=1.0000, R=0.9505, F1=0.9746, support=182
- Standing: P=0.9119, R=1.0000, F1=0.9539, support=145
