# PTQ_DEEPCONV_LSTM_CONV2D_E11_DEEPCONV_LSTM_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_conv2d_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9653
- Macro-F1: 0.9655

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.041 ms/sample
- Inference latency p95: 2.076 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/deepconv_lstm_conv2d/e11/m3/confusion_ptq_deepconv_lstm_conv2d_E11_deepconv_lstm_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9904, R=0.9735, F1=0.9819, support=529
- Jogging: P=0.9905, R=0.9830, F1=0.9867, support=528
- Upstairs: P=0.8822, R=0.9490, F1=0.9144, support=529
- Downstairs: P=0.9384, R=0.8939, F1=0.9156, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=1.0000, R=0.9924, F1=0.9962, support=528
