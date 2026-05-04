# ON_FP32_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9807
- Macro-F1: 0.9694

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e07/confusion_on_fp32_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9945, R=0.9945, F1=0.9945, support=2723
- Jogging: P=0.9920, R=0.9953, F1=0.9936, support=2109
- Upstairs: P=0.8986, R=0.9712, F1=0.9335, support=730
- Downstairs: P=0.9788, R=0.8671, F1=0.9196, support=587
- Sitting: P=0.9894, R=0.9843, F1=0.9868, support=381
- Standing: P=0.9837, R=0.9934, F1=0.9885, support=304
