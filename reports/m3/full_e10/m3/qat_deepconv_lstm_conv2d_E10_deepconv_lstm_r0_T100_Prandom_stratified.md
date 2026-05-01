# QAT_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/full_e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.3382
- Macro-F1: 0.3124

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.245 ms/sample
- Inference latency p95: 4.281 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e10/m3/confusion_qat_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3845, R=0.8068, F1=0.5208, support=264
- Jogging: P=1.0000, R=0.1217, F1=0.2169, support=263
- Upstairs: P=0.1292, R=0.2348, F1=0.1667, support=264
- Downstairs: P=0.3658, R=0.4697, F1=0.4113, support=264
- Sitting: P=1.0000, R=0.1023, F1=0.1856, support=264
- Standing: P=0.5133, R=0.2928, F1=0.3729, support=263
