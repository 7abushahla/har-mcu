# ON_FP32_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9470
- Macro-F1: 0.9474

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e12/confusion_on_fp32_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9861, R=0.9357, F1=0.9602, support=529
- Jogging: P=0.9845, R=0.9640, F1=0.9742, support=528
- Upstairs: P=0.8848, R=0.8998, F1=0.8922, support=529
- Downstairs: P=0.8621, R=0.8996, F1=0.8804, support=528
- Sitting: P=0.9962, R=0.9830, F1=0.9895, support=528
- Standing: P=0.9760, R=1.0000, F1=0.9878, support=528
