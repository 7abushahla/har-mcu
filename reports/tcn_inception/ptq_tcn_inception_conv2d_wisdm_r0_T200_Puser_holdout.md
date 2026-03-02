# PTQ_TCN_INCEPTION_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 379.45 KB
- Accuracy: 0.7689
- Macro-F1: 0.6967

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 3.282 ms/sample
- Inference latency p95: 3.823 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_inception/confusion_ptq_tcn_inception_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9288, R=0.7539, F1=0.8323, support=1333
- Jogging: P=0.9795, R=0.8890, F1=0.9320, support=1126
- Upstairs: P=0.3863, R=0.8204, F1=0.5253, support=412
- Downstairs: P=0.4812, R=0.2246, F1=0.3062, support=285
- Sitting: P=0.9818, R=0.8504, F1=0.9114, support=127
- Standing: P=0.5638, R=0.8346, F1=0.6730, support=127
