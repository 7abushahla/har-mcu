# ON_FP32_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9827
- Macro-F1: 0.9737

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e05/confusion_on_fp32_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9952, R=0.9938, F1=0.9945, support=2723
- Jogging: P=0.9901, R=0.9957, F1=0.9929, support=2109
- Upstairs: P=0.9169, R=0.9671, F1=0.9413, support=730
- Downstairs: P=0.9741, R=0.8978, F1=0.9344, support=587
- Sitting: P=0.9921, R=0.9895, F1=0.9908, support=381
- Standing: P=0.9901, R=0.9868, F1=0.9885, support=304
