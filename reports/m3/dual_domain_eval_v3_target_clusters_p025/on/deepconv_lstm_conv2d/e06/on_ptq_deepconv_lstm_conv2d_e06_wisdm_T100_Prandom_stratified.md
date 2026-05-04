# ON_PTQ_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9783
- Macro-F1: 0.9680

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e06/confusion_on_ptq_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9869, R=0.9934, F1=0.9901, support=2723
- Jogging: P=0.9947, R=0.9853, F1=0.9900, support=2109
- Upstairs: P=0.9272, R=0.9425, F1=0.9348, support=730
- Downstairs: P=0.9322, R=0.9370, F1=0.9346, support=587
- Sitting: P=0.9843, R=0.9895, F1=0.9869, support=381
- Standing: P=0.9965, R=0.9474, F1=0.9713, support=304
