# PTQ_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9435
- Macro-F1: 0.8863

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.244 ms/sample
- Inference latency p95: 4.303 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e00/m3/confusion_ptq_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9890, R=0.9864, F1=0.9877, support=2723
- Jogging: P=0.9947, R=0.9796, F1=0.9871, support=2109
- Upstairs: P=0.7057, R=0.9658, F1=0.8155, support=730
- Downstairs: P=0.9435, R=0.8535, F1=0.8962, support=587
- Sitting: P=0.9895, R=0.7428, F1=0.8486, support=381
- Standing: P=0.9200, R=0.6809, F1=0.7826, support=304
