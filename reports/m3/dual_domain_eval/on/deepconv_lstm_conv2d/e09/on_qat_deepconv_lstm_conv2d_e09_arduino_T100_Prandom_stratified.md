# ON_QAT_DEEPCONV_LSTM_CONV2D_E09_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4912
- Macro-F1: 0.4203

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e09/confusion_on_qat_deepconv_lstm_conv2d_e09_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4451, R=0.8750, F1=0.5900, support=264
- Jogging: P=0.9868, R=0.8517, F1=0.9143, support=263
- Upstairs: P=0.2916, R=0.7235, F1=0.4157, support=264
- Downstairs: P=0.7191, R=0.4848, F1=0.5792, support=264
- Sitting: P=1.0000, R=0.0114, F1=0.0225, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
