# ON_FP32_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9791
- Macro-F1: 0.9792

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e10/confusion_on_fp32_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9924, R=0.9924, F1=0.9924, support=264
- Jogging: P=0.9961, R=0.9658, F1=0.9807, support=263
- Upstairs: P=0.9270, R=0.9621, F1=0.9442, support=264
- Downstairs: P=0.9655, R=0.9545, F1=0.9600, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9962, R=1.0000, F1=0.9981, support=263
