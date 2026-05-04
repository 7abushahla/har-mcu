# ON_QAT_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9775
- Macro-F1: 0.9650

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e06/confusion_on_qat_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9894, R=0.9930, F1=0.9912, support=2723
- Jogging: P=0.9952, R=0.9844, F1=0.9897, support=2109
- Upstairs: P=0.9212, R=0.9452, F1=0.9331, support=730
- Downstairs: P=0.9228, R=0.9370, F1=0.9298, support=587
- Sitting: P=0.9842, R=0.9816, F1=0.9829, support=381
- Standing: P=0.9862, R=0.9408, F1=0.9630, support=304
