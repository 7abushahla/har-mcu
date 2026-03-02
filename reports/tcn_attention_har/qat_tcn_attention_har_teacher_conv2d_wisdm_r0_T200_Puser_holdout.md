# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 631.39 KB
- Accuracy: 0.8718
- Macro-F1: 0.8207

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 11.950 ms/sample
- Inference latency p95: 12.351 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_qat_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9809, R=0.8095, F1=0.8870, support=1333
- Jogging: P=0.9726, R=0.9769, F1=0.9747, support=1126
- Upstairs: P=0.6446, R=0.7573, F1=0.6964, support=412
- Downstairs: P=0.6649, R=0.8982, F1=0.7642, support=285
- Sitting: P=0.7347, R=0.8504, F1=0.7883, support=127
- Standing: P=0.7239, R=0.9291, F1=0.8138, support=127
