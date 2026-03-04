# QAT_XTINYHAR_STUDENT_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 119.59 KB
- Accuracy: 0.7657
- Macro-F1: 0.6526

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 19
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'GATHER', 'GELU', 'MEAN', 'MUL', 'PACK', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.177 ms/sample
- Inference latency p95: 0.219 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/xtinyhar/confusion_qat_xtinyhar_student_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.8560, R=0.7847, F1=0.8188, support=1333
- Jogging: P=0.9667, R=0.9538, F1=0.9602, support=1126
- Upstairs: P=0.4568, R=0.5388, F1=0.4944, support=412
- Downstairs: P=0.2526, R=0.1684, F1=0.2021, support=285
- Sitting: P=0.9391, R=0.8504, F1=0.8926, support=127
- Standing: P=0.3951, R=0.8898, F1=0.5472, support=127
