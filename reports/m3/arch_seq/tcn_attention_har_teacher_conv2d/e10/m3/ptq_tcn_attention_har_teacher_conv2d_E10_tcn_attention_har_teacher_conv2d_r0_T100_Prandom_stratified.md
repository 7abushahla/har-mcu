# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E10_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/tcn_attention_har_teacher_conv2d/e10/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E10_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.40 KB
- Accuracy: 0.9924
- Macro-F1: 0.9924

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.055 ms/sample
- Inference latency p95: 8.357 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e10/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E10_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=1.0000, F1=0.9962, support=264
- Jogging: P=1.0000, R=0.9924, F1=0.9962, support=263
- Upstairs: P=0.9847, R=0.9773, F1=0.9810, support=264
- Downstairs: P=0.9774, R=0.9848, F1=0.9811, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
