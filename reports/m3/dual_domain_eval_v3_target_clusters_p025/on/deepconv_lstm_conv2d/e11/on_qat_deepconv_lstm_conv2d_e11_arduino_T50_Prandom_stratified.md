# ON_QAT_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.8962
- Macro-F1: 0.8976

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e11/confusion_on_qat_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8897, R=0.9452, F1=0.9166, support=529
- Jogging: P=0.9939, R=0.9280, F1=0.9598, support=528
- Upstairs: P=0.8441, R=0.8393, F1=0.8417, support=529
- Downstairs: P=0.7480, R=0.9053, F1=0.8192, support=528
- Sitting: P=0.9733, R=0.9659, F1=0.9696, support=528
- Standing: P=0.9836, R=0.7936, F1=0.8784, support=528
