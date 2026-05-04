# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9851
- Macro-F1: 0.9801

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e08/confusion_on_fp32_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9861, R=0.9962, F1=0.9911, support=5482
- Jogging: P=0.9946, R=0.9967, F1=0.9957, support=4250
- Upstairs: P=0.9655, R=0.9442, F1=0.9547, support=1541
- Downstairs: P=0.9621, R=0.9351, F1=0.9484, support=1249
- Sitting: P=0.9923, R=0.9936, F1=0.9929, support=777
- Standing: P=0.9952, R=1.0000, F1=0.9976, support=624
