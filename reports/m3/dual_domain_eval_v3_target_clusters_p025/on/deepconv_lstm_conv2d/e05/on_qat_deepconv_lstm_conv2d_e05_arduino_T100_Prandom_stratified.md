# ON_QAT_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4798
- Macro-F1: 0.4684

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e05/confusion_on_qat_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3251, R=0.5985, F1=0.4213, support=264
- Jogging: P=0.8273, R=0.4373, F1=0.5721, support=263
- Upstairs: P=0.3090, R=0.3371, F1=0.3225, support=264
- Downstairs: P=0.1129, R=0.0530, F1=0.0722, support=264
- Sitting: P=0.6420, R=0.8561, F1=0.7338, support=264
- Standing: P=0.8135, R=0.5970, F1=0.6886, support=263
