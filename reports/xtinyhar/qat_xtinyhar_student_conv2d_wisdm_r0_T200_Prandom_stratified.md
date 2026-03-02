# QAT_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 119.59 KB
- Accuracy: 0.9350
- Macro-F1: 0.9060

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.179 ms/sample
- Inference latency p95: 0.249 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_qat_xtinyhar_student_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9473, R=0.9628, F1=0.9550, support=1344
- Jogging: P=0.9781, R=0.9884, F1=0.9832, support=1037
- Upstairs: P=0.8152, R=0.7530, F1=0.7829, support=328
- Downstairs: P=0.7819, R=0.7422, F1=0.7615, support=256
- Sitting: P=0.9889, R=0.9780, F1=0.9834, support=182
- Standing: P=0.9474, R=0.9931, F1=0.9697, support=145
