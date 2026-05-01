# PTQ_DAGHERO_CNN_2LAYER_CONV2D_E11_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/daghero_cnn_2layer_conv2d/e11/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E11_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9864
- Macro-F1: 0.9864

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.044 ms/sample
- Inference latency p95: 0.051 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/daghero_cnn_2layer_conv2d/e11/m3/confusion_ptq_daghero_cnn_2layer_conv2d_E11_daghero_cnn_2layer_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9906, R=0.9981, F1=0.9944, support=529
- Jogging: P=1.0000, R=0.9905, F1=0.9952, support=528
- Upstairs: P=0.9657, R=0.9584, F1=0.9620, support=529
- Downstairs: P=0.9625, R=0.9716, F1=0.9670, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
