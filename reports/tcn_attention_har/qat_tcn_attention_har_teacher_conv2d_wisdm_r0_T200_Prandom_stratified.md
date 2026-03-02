# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 631.39 KB
- Accuracy: 0.9961
- Macro-F1: 0.9929

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 11.380 ms/sample
- Inference latency p95: 13.508 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_qat_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9985, F1=0.9985, support=1344
- Jogging: P=0.9990, R=0.9981, F1=0.9986, support=1037
- Upstairs: P=0.9849, R=0.9939, F1=0.9894, support=328
- Downstairs: P=0.9882, R=0.9844, F1=0.9863, support=256
- Sitting: P=0.9945, R=0.9890, F1=0.9917, support=182
- Standing: P=0.9931, R=0.9931, F1=0.9931, support=145
