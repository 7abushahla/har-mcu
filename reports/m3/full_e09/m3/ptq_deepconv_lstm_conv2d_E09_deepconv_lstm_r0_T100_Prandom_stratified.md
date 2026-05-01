# PTQ_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9842
- Macro-F1: 0.9842

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.238 ms/sample
- Inference latency p95: 4.289 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e09/m3/confusion_ptq_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9962, R=0.9848, F1=0.9905, support=264
- Jogging: P=0.9962, R=0.9886, F1=0.9924, support=263
- Upstairs: P=0.9326, R=0.9962, F1=0.9634, support=264
- Downstairs: P=0.9920, R=0.9356, F1=0.9630, support=264
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
