# FP32_TFLITE_TCN_ATTENTION_HAR_TEACHER_CONV2D_E00_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/tcn_attention_har_teacher_conv2d/e00/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E00_tcn_attention_har_teacher_conv2d_r0_fp32.tflite`
- Model size: 1883.36 KB
- Accuracy: 0.9943
- Macro-F1: 0.9915

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 2.066 ms/sample
- Inference latency p95: 2.109 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e00/m3/confusion_fp32_tflite_tcn_attention_har_teacher_conv2d_E00_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9989, R=0.9967, F1=0.9978, support=2723
- Jogging: P=0.9972, R=0.9986, F1=0.9979, support=2109
- Upstairs: P=0.9889, R=0.9753, F1=0.9821, support=730
- Downstairs: P=0.9667, R=0.9881, F1=0.9773, support=587
- Sitting: P=0.9974, R=0.9974, F1=0.9974, support=381
- Standing: P=0.9967, R=0.9967, F1=0.9967, support=304
