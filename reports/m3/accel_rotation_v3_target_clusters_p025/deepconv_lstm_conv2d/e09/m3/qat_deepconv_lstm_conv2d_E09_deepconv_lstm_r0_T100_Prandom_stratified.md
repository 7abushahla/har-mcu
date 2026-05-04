# QAT_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.7554
- Macro-F1: 0.7451

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.250 ms/sample
- Inference latency p95: 4.292 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e09/m3/confusion_qat_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6359, R=0.9924, F1=0.7751, support=264
- Jogging: P=0.9867, R=0.8441, F1=0.9098, support=263
- Upstairs: P=0.7131, R=0.6780, F1=0.6951, support=264
- Downstairs: P=0.6241, R=0.6856, F1=0.6534, support=264
- Sitting: P=0.8361, R=0.9470, F1=0.8881, support=264
- Standing: P=0.9619, R=0.3840, F1=0.5489, support=263
