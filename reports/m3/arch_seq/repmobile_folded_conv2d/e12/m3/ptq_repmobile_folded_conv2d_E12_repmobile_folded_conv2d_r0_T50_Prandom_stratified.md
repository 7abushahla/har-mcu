# PTQ_REPMOBILE_FOLDED_CONV2D_E12_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/repmobile_folded_conv2d/e12/repmobile_folded_conv2d_T50_Prandom_stratified_E12_repmobile_folded_conv2d_r0_ptq_int8.tflite`
- Model size: 42.12 KB
- Accuracy: 0.9489
- Macro-F1: 0.9489

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.172 ms/sample
- Inference latency p95: 0.192 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e12/m3/confusion_ptq_repmobile_folded_conv2d_E12_repmobile_folded_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9759, R=0.9943, F1=0.9850, support=529
- Jogging: P=0.9885, R=0.9792, F1=0.9838, support=528
- Upstairs: P=0.8263, R=0.8904, F1=0.8571, support=529
- Downstairs: P=0.9106, R=0.8295, F1=0.8682, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
