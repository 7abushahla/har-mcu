# PTQ_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 119.23 KB
- Accuracy: 0.7707
- Macro-F1: 0.6107

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.185 ms/sample
- Inference latency p95: 0.213 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_ptq_xtinyhar_student_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.8170, R=0.8710, F1=0.8431, support=1333
- Jogging: P=0.9721, R=0.9583, F1=0.9651, support=1126
- Upstairs: P=0.4347, R=0.3714, F1=0.4005, support=412
- Downstairs: P=0.2679, R=0.0526, F1=0.0880, support=285
- Sitting: P=0.9730, R=0.8504, F1=0.9076, support=127
- Standing: P=0.3111, R=0.8819, F1=0.4600, support=127
