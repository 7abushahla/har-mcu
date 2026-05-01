# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E05_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_attention_har_teacher_conv2d/e05/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E05_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.40 KB
- Accuracy: 0.5917
- Macro-F1: 0.5987

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.603 ms/sample
- Inference latency p95: 8.878 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e05/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E05_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6667, R=0.3409, F1=0.4511, support=264
- Jogging: P=0.8588, R=0.8555, F1=0.8571, support=263
- Upstairs: P=0.3327, R=0.6742, F1=0.4456, support=264
- Downstairs: P=0.1878, R=0.1742, F1=0.1807, support=264
- Sitting: P=0.9851, R=1.0000, F1=0.9925, support=264
- Standing: P=0.9708, R=0.5057, F1=0.6650, support=263
