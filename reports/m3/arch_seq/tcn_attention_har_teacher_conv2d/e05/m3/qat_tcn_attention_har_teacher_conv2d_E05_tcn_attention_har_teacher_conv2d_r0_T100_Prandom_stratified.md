# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_E05_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_attention_har_teacher_conv2d/e05/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E05_tcn_attention_har_teacher_conv2d_r0_qat.tflite`
- Model size: 585.59 KB
- Accuracy: 0.5695
- Macro-F1: 0.5338

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.592 ms/sample
- Inference latency p95: 8.751 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e05/m3/confusion_qat_tcn_attention_har_teacher_conv2d_E05_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5727, R=0.2386, F1=0.3369, support=264
- Jogging: P=0.8131, R=0.8935, F1=0.8514, support=263
- Upstairs: P=0.3198, R=0.7159, F1=0.4421, support=264
- Downstairs: P=0.2698, R=0.0644, F1=0.1040, support=264
- Sitting: P=0.6804, R=1.0000, F1=0.8098, support=264
- Standing: P=0.9433, R=0.5057, F1=0.6584, support=263
