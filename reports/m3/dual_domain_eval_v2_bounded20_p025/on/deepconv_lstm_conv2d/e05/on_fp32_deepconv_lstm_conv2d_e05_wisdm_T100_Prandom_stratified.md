# ON_FP32_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9690
- Macro-F1: 0.9399

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e05/confusion_on_fp32_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9848, R=0.9974, F1=0.9911, support=2723
- Jogging: P=0.9957, R=0.9915, F1=0.9936, support=2109
- Upstairs: P=0.8401, R=0.9575, F1=0.8950, support=730
- Downstairs: P=0.9567, R=0.8654, F1=0.9088, support=587
- Sitting: P=0.9921, R=0.9895, F1=0.9908, support=381
- Standing: P=0.9914, R=0.7599, F1=0.8603, support=304
