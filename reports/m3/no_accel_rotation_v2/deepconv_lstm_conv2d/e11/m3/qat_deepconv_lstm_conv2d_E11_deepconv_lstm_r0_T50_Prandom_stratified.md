# QAT_DEEPCONV_LSTM_CONV2D_E11_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9662
- Macro-F1: 0.9664

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.037 ms/sample
- Inference latency p95: 2.072 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/m3/confusion_qat_deepconv_lstm_conv2d_E11_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9734, R=0.9679, F1=0.9706, support=529
- Jogging: P=0.9942, R=0.9773, F1=0.9857, support=528
- Upstairs: P=0.9071, R=0.9225, F1=0.9147, support=529
- Downstairs: P=0.9358, R=0.9394, F1=0.9376, support=528
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=528
- Standing: P=0.9962, R=0.9905, F1=0.9934, support=528
