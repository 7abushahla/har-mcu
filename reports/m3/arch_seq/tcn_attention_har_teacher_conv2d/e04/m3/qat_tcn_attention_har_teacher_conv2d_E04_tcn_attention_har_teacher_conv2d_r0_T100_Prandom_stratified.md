# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_E04_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/tcn_attention_har_teacher_conv2d/e04/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E04_tcn_attention_har_teacher_conv2d_r0_qat.tflite`
- Model size: 585.59 KB
- Accuracy: 0.5215
- Macro-F1: 0.4864

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.280 ms/sample
- Inference latency p95: 8.715 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e04/m3/confusion_qat_tcn_attention_har_teacher_conv2d_E04_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4495, R=0.1856, F1=0.2627, support=264
- Jogging: P=0.7683, R=0.9582, F1=0.8528, support=263
- Upstairs: P=0.2297, R=0.3864, F1=0.2881, support=264
- Downstairs: P=0.3378, R=0.0947, F1=0.1479, support=264
- Sitting: P=0.5366, R=1.0000, F1=0.6984, support=264
- Standing: P=0.9852, R=0.5057, F1=0.6683, support=263
