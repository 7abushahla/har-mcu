# QAT_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 29.41 KB
- Accuracy: 0.9951
- Macro-F1: 0.9888

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Inference latency median: 0.116 ms/sample
- Inference latency p95: 0.133 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_qat_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9993, R=0.9985, F1=0.9989, support=1344
- Jogging: P=0.9971, R=0.9990, F1=0.9981, support=1037
- Upstairs: P=0.9909, R=0.9909, F1=0.9909, support=328
- Downstairs: P=0.9922, R=0.9961, F1=0.9942, support=256
- Sitting: P=1.0000, R=0.9505, F1=0.9746, support=182
- Standing: P=0.9539, R=1.0000, F1=0.9764, support=145
