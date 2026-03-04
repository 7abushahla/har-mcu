# QAT_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 119.59 KB
- Accuracy: 0.9365
- Macro-F1: 0.9083

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 19
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'GATHER', 'GELU', 'MEAN', 'MUL', 'PACK', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.177 ms/sample
- Inference latency p95: 0.210 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_qat_xtinyhar_student_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9494, R=0.9635, F1=0.9564, support=1344
- Jogging: P=0.9781, R=0.9884, F1=0.9832, support=1037
- Upstairs: P=0.8224, R=0.7622, F1=0.7911, support=328
- Downstairs: P=0.7796, R=0.7461, F1=0.7625, support=256
- Sitting: P=0.9889, R=0.9780, F1=0.9834, support=182
- Standing: P=0.9536, R=0.9931, F1=0.9730, support=145
