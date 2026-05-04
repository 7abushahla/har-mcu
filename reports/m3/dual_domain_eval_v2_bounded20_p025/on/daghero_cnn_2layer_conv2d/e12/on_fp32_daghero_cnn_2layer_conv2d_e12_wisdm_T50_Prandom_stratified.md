# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.3844
- Macro-F1: 0.2417

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e12/confusion_on_fp32_daghero_cnn_2layer_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=5482
- Jogging: P=0.4508, R=0.9781, F1=0.6171, support=4250
- Upstairs: P=0.2053, R=0.5704, F1=0.3020, support=1541
- Downstairs: P=0.2857, R=0.0016, F1=0.0032, support=1249
- Sitting: P=0.7603, R=0.4041, F1=0.5277, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
