# ON_QAT_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.8902
- Macro-F1: 0.8943

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e11/confusion_on_qat_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9505, R=0.9433, F1=0.9469, support=529
- Jogging: P=0.9901, R=0.9470, F1=0.9681, support=528
- Upstairs: P=0.6588, R=0.8469, F1=0.7411, support=529
- Downstairs: P=0.8607, R=0.8542, F1=0.8574, support=528
- Sitting: P=0.9960, R=0.9470, F1=0.9709, support=528
- Standing: P=0.9770, R=0.8030, F1=0.8815, support=528
