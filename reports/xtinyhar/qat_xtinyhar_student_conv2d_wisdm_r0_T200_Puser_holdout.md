# QAT_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 119.59 KB
- Accuracy: 0.7669
- Macro-F1: 0.6544

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.183 ms/sample
- Inference latency p95: 0.203 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_qat_xtinyhar_student_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.8547, R=0.7854, F1=0.8186, support=1333
- Jogging: P=0.9667, R=0.9547, F1=0.9607, support=1126
- Upstairs: P=0.4607, R=0.5413, F1=0.4978, support=412
- Downstairs: P=0.2606, R=0.1719, F1=0.2072, support=285
- Sitting: P=0.9474, R=0.8504, F1=0.8963, support=127
- Standing: P=0.3937, R=0.8898, F1=0.5459, support=127
