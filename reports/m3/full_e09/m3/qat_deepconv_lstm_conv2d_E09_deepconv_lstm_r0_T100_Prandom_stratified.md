# QAT_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8066
- Macro-F1: 0.8026

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.253 ms/sample
- Inference latency p95: 4.307 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e09/m3/confusion_qat_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7988, R=0.9773, F1=0.8790, support=264
- Jogging: P=0.9921, R=0.9582, F1=0.9749, support=263
- Upstairs: P=0.5448, R=0.8523, F1=0.6647, support=264
- Downstairs: P=0.8687, R=0.8523, F1=0.8604, support=264
- Sitting: P=0.8926, R=0.4091, F1=0.5610, support=264
- Standing: P=0.9811, R=0.7909, F1=0.8758, support=263
