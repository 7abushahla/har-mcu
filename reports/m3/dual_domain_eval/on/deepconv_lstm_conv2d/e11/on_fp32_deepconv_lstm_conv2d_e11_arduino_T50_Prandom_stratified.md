# ON_FP32_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9224
- Macro-F1: 0.9227

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e11/confusion_on_fp32_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9215, R=0.9546, F1=0.9378, support=529
- Jogging: P=0.9767, R=0.9545, F1=0.9655, support=528
- Upstairs: P=0.8108, R=0.8507, F1=0.8303, support=529
- Downstairs: P=0.8625, R=0.8314, F1=0.8467, support=528
- Sitting: P=0.9796, R=1.0000, F1=0.9897, support=528
- Standing: P=0.9901, R=0.9432, F1=0.9661, support=528
