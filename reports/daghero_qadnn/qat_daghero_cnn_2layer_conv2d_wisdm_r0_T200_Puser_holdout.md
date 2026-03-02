# QAT_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 29.41 KB
- Accuracy: 0.8493
- Macro-F1: 0.8191

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.117 ms/sample
- Inference latency p95: 0.140 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_qat_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9739, R=0.8402, F1=0.9021, support=1333
- Jogging: P=0.9758, R=0.8970, F1=0.9348, support=1126
- Upstairs: P=0.5569, R=0.8786, F1=0.6817, support=412
- Downstairs: P=0.5344, R=0.6000, F1=0.5653, support=285
- Sitting: P=0.9818, R=0.8504, F1=0.9114, support=127
- Standing: P=0.8621, R=0.9843, F1=0.9191, support=127
