# PTQ_REPMOBILE_FOLDED_CONV2D_E08_REPMOBILE_FOLDED_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E08_T50_window/arch_seq/repmobile_folded_conv2d/e08/repmobile_folded_conv2d_T50_Prandom_stratified_E08_repmobile_folded_conv2d_r0_ptq_int8.tflite`
- Model size: 42.12 KB
- Accuracy: 0.1669
- Macro-F1: 0.0477

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'DEPTHWISE_CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.171 ms/sample
- Inference latency p95: 0.213 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/repmobile_folded_conv2d/e08/m3/confusion_ptq_repmobile_folded_conv2d_E08_repmobile_folded_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=529
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=528
- Upstairs: P=0.1669, R=1.0000, F1=0.2860, support=529
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=528
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=528
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=528
