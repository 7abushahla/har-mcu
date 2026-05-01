# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E00_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/xtinyhar_student_conv2d/e00/xtinyhar_student_conv2d_T100_Prandom_stratified_E00_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1103.78 KB
- Accuracy: 0.9570
- Macro-F1: 0.9443

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.189 ms/sample
- Inference latency p95: 0.209 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e00/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E00_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9615, R=0.9824, F1=0.9718, support=2723
- Jogging: P=0.9843, R=0.9810, F1=0.9827, support=2109
- Upstairs: P=0.8791, R=0.8863, F1=0.8827, support=730
- Downstairs: P=0.8811, R=0.7956, F1=0.8362, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9934, R=0.9967, F1=0.9951, support=304
