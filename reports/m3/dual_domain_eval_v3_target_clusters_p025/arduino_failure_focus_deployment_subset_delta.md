# Arduino Failure-Focus Delta Summary: E09-E12 Only, V1/V2/V3

Means are limited to Arduino-adapted deployment-relevant experiments E09/E10/E11/E12. Positive recall deltas are good. Negative confusion-pair deltas are good.

| Run set | Model | Tier | dAcc | dMacro-F1 | dStand recall | dWalk recall | dUp recall | dDown recall | dStand->Walk | dWalk->Stairs |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | fp32 | -0.0150 | -0.0151 | +0.0000 | +0.0000 | -0.0520 | -0.0346 | +0.0000 | -0.0009 |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | ptq | -0.0139 | -0.0140 | +0.0000 | -0.0005 | -0.0374 | -0.0440 | +0.0000 | -0.0005 |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | qat | -0.0102 | -0.0102 | +0.0000 | -0.0009 | -0.0270 | -0.0322 | +0.0000 | +0.0000 |
| v1_uniform_p050 | deepconv_lstm_conv2d | fp32 | -0.0079 | -0.0089 | +0.0417 | +0.0369 | -0.0809 | -0.0294 | -0.0047 | -0.0374 |
| v1_uniform_p050 | deepconv_lstm_conv2d | ptq | -0.0096 | -0.0106 | +0.0388 | +0.0336 | -0.0780 | -0.0350 | -0.0047 | -0.0341 |
| v1_uniform_p050 | deepconv_lstm_conv2d | qat | -0.2459 | -0.2561 | -0.4584 | -0.2773 | -0.0120 | -0.2888 | +0.0038 | +0.2806 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | fp32 | -0.0037 | -0.0037 | +0.0000 | -0.0005 | -0.0175 | -0.0043 | +0.0000 | +0.0000 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | ptq | -0.0038 | -0.0038 | +0.0000 | -0.0005 | -0.0204 | -0.0019 | +0.0000 | +0.0000 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | qat | -0.0010 | -0.0010 | +0.0000 | -0.0005 | -0.0009 | -0.0047 | +0.0000 | +0.0005 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | fp32 | +0.0014 | +0.0014 | -0.0071 | -0.0033 | -0.0175 | +0.0426 | +0.0048 | +0.0114 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | ptq | +0.0020 | +0.0020 | -0.0066 | -0.0038 | -0.0156 | +0.0445 | +0.0038 | +0.0123 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | qat | -0.0352 | -0.0278 | -0.1324 | +0.0114 | -0.0633 | -0.0246 | +0.0789 | +0.0123 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | fp32 | -0.0041 | -0.0041 | +0.0000 | -0.0009 | -0.0109 | -0.0099 | +0.0000 | +0.0005 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | ptq | -0.0032 | -0.0032 | +0.0000 | -0.0009 | -0.0076 | -0.0076 | +0.0000 | +0.0005 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | qat | -0.0033 | -0.0033 | +0.0000 | -0.0014 | -0.0052 | -0.0118 | +0.0000 | +0.0014 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | fp32 | +0.0195 | +0.0184 | +0.0469 | +0.0463 | -0.0312 | +0.0587 | -0.0005 | -0.0426 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | ptq | +0.0204 | +0.0193 | +0.0445 | +0.0473 | -0.0298 | +0.0630 | +0.0019 | -0.0435 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | qat | -0.0502 | -0.0535 | -0.3276 | +0.0293 | -0.0662 | +0.0019 | +0.0878 | -0.0099 |
