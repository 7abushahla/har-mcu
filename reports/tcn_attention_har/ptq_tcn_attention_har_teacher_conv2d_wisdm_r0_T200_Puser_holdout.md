# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 623.99 KB
- Accuracy: 0.8645
- Macro-F1: 0.7985

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 11.328 ms/sample
- Inference latency p95: 11.872 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_ptq_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9784, R=0.8140, F1=0.8886, support=1333
- Jogging: P=0.9727, R=0.9822, F1=0.9775, support=1126
- Upstairs: P=0.6919, R=0.6650, F1=0.6782, support=412
- Downstairs: P=0.6148, R=0.9018, F1=0.7312, support=285
- Sitting: P=0.8060, R=0.8504, F1=0.8276, support=127
- Standing: P=0.5463, R=0.9291, F1=0.6880, support=127
