# ON_QAT_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9146
- Macro-F1: 0.8877

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e08/confusion_on_qat_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9748, R=0.9329, F1=0.9534, support=5482
- Jogging: P=0.9947, R=0.9238, F1=0.9579, support=4250
- Upstairs: P=0.7168, R=0.8559, F1=0.7802, support=1541
- Downstairs: P=0.7184, R=0.8863, F1=0.7935, support=1249
- Sitting: P=0.9915, R=0.8958, F1=0.9412, support=777
- Standing: P=0.8841, R=0.9167, F1=0.9001, support=624
