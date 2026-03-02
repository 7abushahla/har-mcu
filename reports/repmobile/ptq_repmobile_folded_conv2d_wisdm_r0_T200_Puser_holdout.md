# PTQ_REPMOBILE_FOLDED_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 43.41 KB
- Accuracy: 0.7284
- Macro-F1: 0.5315

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.408 ms/sample
- Inference latency p95: 0.441 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_ptq_repmobile_folded_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.6146, R=1.0000, F1=0.7613, support=1333
- Jogging: P=0.9815, R=0.8481, F1=0.9100, support=1126
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=412
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=285
- Sitting: P=0.9107, R=0.8031, F1=0.8536, support=127
- Standing: P=0.6026, R=0.7402, F1=0.6643, support=127
