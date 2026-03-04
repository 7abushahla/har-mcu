# PTQ_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 119.15 KB
- Accuracy: 0.9186
- Macro-F1: 0.8741

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 19
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'GATHER', 'GELU', 'MEAN', 'MUL', 'PACK', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.178 ms/sample
- Inference latency p95: 0.274 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_ptq_xtinyhar_student_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9197, R=0.9717, F1=0.9450, support=1344
- Jogging: P=0.9716, R=0.9884, F1=0.9799, support=1037
- Upstairs: P=0.7729, R=0.6951, F1=0.7319, support=328
- Downstairs: P=0.7737, R=0.5742, F1=0.6592, support=256
- Sitting: P=1.0000, R=0.9505, F1=0.9746, support=182
- Standing: P=0.9119, R=1.0000, F1=0.9539, support=145
