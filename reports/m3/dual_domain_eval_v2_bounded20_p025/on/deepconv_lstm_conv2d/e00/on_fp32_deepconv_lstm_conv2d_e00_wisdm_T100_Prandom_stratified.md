# ON_FP32_DEEPCONV_LSTM_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9678
- Macro-F1: 0.9333

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e00/confusion_on_fp32_deepconv_lstm_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=0.9963, F1=0.9907, support=2723
- Jogging: P=0.9943, R=0.9929, F1=0.9936, support=2109
- Upstairs: P=0.8301, R=0.9507, F1=0.8863, support=730
- Downstairs: P=0.9636, R=0.9029, F1=0.9323, support=587
- Sitting: P=0.9895, R=0.9869, F1=0.9882, support=381
- Standing: P=0.9952, R=0.6809, F1=0.8086, support=304
