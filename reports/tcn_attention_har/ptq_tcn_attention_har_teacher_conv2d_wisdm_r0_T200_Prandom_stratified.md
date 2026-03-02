# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 623.99 KB
- Accuracy: 0.9948
- Macro-F1: 0.9901

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 11.638 ms/sample
- Inference latency p95: 12.103 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_ptq_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9993, F1=0.9989, support=1344
- Jogging: P=0.9990, R=0.9971, F1=0.9981, support=1037
- Upstairs: P=0.9818, R=0.9848, F1=0.9833, support=328
- Downstairs: P=0.9806, R=0.9883, F1=0.9844, support=256
- Sitting: P=0.9890, R=0.9835, F1=0.9862, support=182
- Standing: P=0.9931, R=0.9862, F1=0.9896, support=145
