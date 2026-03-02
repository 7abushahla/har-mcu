# QAT_REPMOBILE_FOLDED_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 46.91 KB
- Accuracy: 0.7628
- Macro-F1: 0.5184

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.540 ms/sample
- Inference latency p95: 0.657 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/repmobile/confusion_qat_repmobile_folded_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.7061, R=0.9895, F1=0.8241, support=1333
- Jogging: P=0.9814, R=0.9378, F1=0.9591, support=1126
- Upstairs: P=0.8571, R=0.0146, F1=0.0286, support=412
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=285
- Sitting: P=0.7347, R=0.8504, F1=0.7883, support=127
- Standing: P=0.3590, R=0.8819, F1=0.5103, support=127
