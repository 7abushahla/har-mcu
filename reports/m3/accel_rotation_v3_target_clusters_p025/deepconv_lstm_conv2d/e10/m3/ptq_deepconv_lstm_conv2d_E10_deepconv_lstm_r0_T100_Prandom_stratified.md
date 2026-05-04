# PTQ_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9804
- Macro-F1: 0.9805

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.256 ms/sample
- Inference latency p95: 4.369 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e10/m3/confusion_ptq_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9924, R=0.9924, F1=0.9924, support=264
- Jogging: P=0.9961, R=0.9696, F1=0.9827, support=263
- Upstairs: P=0.9307, R=0.9659, F1=0.9480, support=264
- Downstairs: P=0.9692, R=0.9545, F1=0.9618, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9962, R=1.0000, F1=0.9981, support=263
