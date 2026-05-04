# ON_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9657
- Macro-F1: 0.9442

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e08/confusion_on_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9794, R=0.9885, F1=0.9839, support=5482
- Jogging: P=0.9938, R=0.9828, F1=0.9883, support=4250
- Upstairs: P=0.8782, R=0.9260, F1=0.9015, support=1541
- Downstairs: P=0.9180, R=0.9055, F1=0.9117, support=1249
- Sitting: P=0.9625, R=0.9897, F1=0.9759, support=777
- Standing: P=0.9831, R=0.8365, F1=0.9039, support=624
