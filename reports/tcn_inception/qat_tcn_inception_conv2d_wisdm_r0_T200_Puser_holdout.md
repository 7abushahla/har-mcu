# QAT_TCN_INCEPTION_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 384.81 KB
- Accuracy: 0.8320
- Macro-F1: 0.8111

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 3.389 ms/sample
- Inference latency p95: 3.597 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_inception/confusion_qat_tcn_inception_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9815, R=0.7164, F1=0.8283, support=1333
- Jogging: P=0.9735, R=0.9458, F1=0.9595, support=1126
- Upstairs: P=0.5082, R=0.9029, F1=0.6503, support=412
- Downstairs: P=0.6443, R=0.7754, F1=0.7038, support=285
- Sitting: P=0.9815, R=0.8346, F1=0.9021, support=127
- Standing: P=0.7375, R=0.9291, F1=0.8223, support=127
