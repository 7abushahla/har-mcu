# PTQ_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5360
- Macro-F1: 0.5583

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.251 ms/sample
- Inference latency p95: 4.336 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e04/m3/confusion_ptq_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6071, R=0.5152, F1=0.5574, support=264
- Jogging: P=1.0000, R=0.3916, F1=0.5628, support=263
- Upstairs: P=0.2288, R=0.3068, F1=0.2621, support=264
- Downstairs: P=0.2945, R=0.5644, F1=0.3870, support=264
- Sitting: P=0.9635, R=1.0000, F1=0.9814, support=264
- Standing: P=0.9504, R=0.4373, F1=0.5990, support=263
