# ON_QAT_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8565
- Macro-F1: 0.8214

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e07/confusion_on_qat_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9249, R=0.8597, F1=0.8911, support=2723
- Jogging: P=0.9968, R=0.8881, F1=0.9393, support=2109
- Upstairs: P=0.5636, R=0.7767, F1=0.6532, support=730
- Downstairs: P=0.6658, R=0.8313, F1=0.7394, support=587
- Sitting: P=0.8778, R=0.8294, F1=0.8529, support=381
- Standing: P=0.8246, R=0.8816, F1=0.8521, support=304
