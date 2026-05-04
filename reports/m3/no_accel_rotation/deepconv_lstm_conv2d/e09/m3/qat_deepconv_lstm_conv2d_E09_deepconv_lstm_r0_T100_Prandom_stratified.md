# QAT_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8793
- Macro-F1: 0.8796

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.257 ms/sample
- Inference latency p95: 4.327 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e09/m3/confusion_qat_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8600, R=0.9773, F1=0.9149, support=264
- Jogging: P=0.9916, R=0.8935, F1=0.9400, support=263
- Upstairs: P=0.8033, R=0.7424, F1=0.7717, support=264
- Downstairs: P=0.7456, R=0.7992, F1=0.7715, support=264
- Sitting: P=0.9366, R=0.9508, F1=0.9436, support=264
- Standing: P=0.9600, R=0.9125, F1=0.9357, support=263
