# QAT_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_conv2d_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.8483
- Macro-F1: 0.8545

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.038 ms/sample
- Inference latency p95: 2.068 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/deepconv_lstm_conv2d/e12/m3/confusion_qat_deepconv_lstm_conv2d_E12_deepconv_lstm_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9525, R=0.7958, F1=0.8671, support=529
- Jogging: P=0.9634, R=0.8977, F1=0.9294, support=528
- Upstairs: P=0.5959, R=0.8166, F1=0.6890, support=529
- Downstairs: P=0.7561, R=0.8163, F1=0.7851, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=0.9782, R=0.7633, F1=0.8574, support=528
