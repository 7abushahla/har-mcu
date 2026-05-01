# QAT_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5215
- Macro-F1: 0.5304

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.249 ms/sample
- Inference latency p95: 4.344 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e04/m3/confusion_qat_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5279, R=0.5379, F1=0.5328, support=264
- Jogging: P=0.9756, R=0.3042, F1=0.4638, support=263
- Upstairs: P=0.2667, R=0.3485, F1=0.3021, support=264
- Downstairs: P=0.2850, R=0.4545, F1=0.3504, support=264
- Sitting: P=0.9135, R=1.0000, F1=0.9548, support=264
- Standing: P=0.7216, R=0.4829, F1=0.5786, support=263
