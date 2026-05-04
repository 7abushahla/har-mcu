# QAT_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.8508
- Macro-F1: 0.8570

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.040 ms/sample
- Inference latency p95: 2.065 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/m3/confusion_qat_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9524, R=0.7940, F1=0.8660, support=529
- Jogging: P=0.9657, R=0.9053, F1=0.9345, support=528
- Upstairs: P=0.5978, R=0.8318, F1=0.6957, support=529
- Downstairs: P=0.7661, R=0.8125, F1=0.7886, support=528
- Sitting: P=0.9981, R=0.9981, F1=0.9981, support=528
- Standing: P=0.9829, R=0.7633, F1=0.8593, support=528
