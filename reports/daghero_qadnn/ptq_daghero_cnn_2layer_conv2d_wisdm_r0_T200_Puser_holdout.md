# PTQ_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 27.37 KB
- Accuracy: 0.8381
- Macro-F1: 0.8020

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.091 ms/sample
- Inference latency p95: 0.106 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_ptq_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9746, R=0.7779, F1=0.8652, support=1333
- Jogging: P=0.8839, R=0.9734, F1=0.9265, support=1126
- Upstairs: P=0.7005, R=0.6699, F1=0.6849, support=412
- Downstairs: P=0.5107, R=0.7544, F1=0.6091, support=285
- Sitting: P=0.9558, R=0.8504, F1=0.9000, support=127
- Standing: P=0.7079, R=0.9921, F1=0.8262, support=127
