# Arduino Failure-Focus Delta Summary: V1/V2/V3

Means are across all E00/E03-E12 Arduino eval rows. Positive recall deltas are good. Negative confusion-pair deltas are good.

| Run set | Model | Tier | dAcc | dMacro-F1 | dStand recall | dWalk recall | dUp recall | dDown recall | dStand->Walk | dWalk->Stairs |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | fp32 | -0.0045 | +0.0053 | -0.0449 | +0.0523 | -0.0947 | -0.0150 | +0.0000 | -0.0523 |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | ptq | +0.0137 | +0.0223 | -0.0909 | +0.0535 | -0.0773 | -0.0181 | +0.0000 | -0.0539 |
| v1_uniform_p050 | daghero_cnn_2layer_conv2d | qat | +0.0045 | +0.0096 | +0.0000 | +0.0678 | -0.1066 | -0.0134 | +0.0000 | -0.0675 |
| v1_uniform_p050 | deepconv_lstm_conv2d | fp32 | -0.0255 | -0.0394 | -0.2016 | -0.1181 | +0.1624 | -0.1095 | -0.0930 | +0.2302 |
| v1_uniform_p050 | deepconv_lstm_conv2d | ptq | -0.0197 | -0.0335 | -0.1625 | -0.0908 | +0.1607 | -0.1140 | -0.0660 | +0.2204 |
| v1_uniform_p050 | deepconv_lstm_conv2d | qat | -0.1439 | -0.1579 | -0.3215 | -0.0234 | -0.1104 | -0.1649 | +0.0560 | +0.0456 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | fp32 | +0.0101 | +0.0132 | -0.2268 | +0.0067 | -0.0150 | +0.0050 | +0.0000 | -0.0076 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | ptq | +0.0133 | +0.0123 | -0.2900 | +0.0064 | -0.0160 | +0.0041 | +0.0000 | -0.0079 |
| v2_bounded20_p025 | daghero_cnn_2layer_conv2d | qat | +0.0034 | +0.0071 | -0.3636 | +0.0029 | -0.0176 | +0.0152 | +0.0000 | -0.0036 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | fp32 | -0.0130 | -0.0189 | -0.1495 | -0.0732 | -0.0907 | -0.0568 | -0.1096 | -0.0406 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | ptq | -0.0113 | -0.0180 | -0.1379 | -0.0733 | -0.0900 | -0.0548 | -0.1092 | -0.0444 |
| v2_bounded20_p025 | deepconv_lstm_conv2d | qat | -0.0217 | -0.0279 | -0.0499 | -0.0647 | -0.2203 | -0.0331 | -0.0657 | -0.1973 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | fp32 | -0.0005 | -0.0008 | +0.0000 | -0.0014 | -0.0074 | -0.0053 | +0.0000 | +0.0012 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | ptq | -0.0014 | +0.0001 | -0.0055 | +0.0003 | -0.0072 | -0.0045 | +0.0000 | -0.0005 |
| v3_target_clusters_p025 | daghero_cnn_2layer_conv2d | qat | +0.0087 | +0.0139 | +0.0259 | +0.0432 | -0.0181 | -0.0046 | +0.0000 | -0.0425 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | fp32 | -0.0113 | -0.0321 | +0.1484 | -0.1911 | +0.0165 | +0.0155 | -0.1115 | +0.1474 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | ptq | -0.0109 | -0.0319 | +0.1579 | -0.1911 | +0.0150 | +0.0181 | -0.1099 | +0.1422 |
| v3_target_clusters_p025 | deepconv_lstm_conv2d | qat | -0.0435 | -0.0504 | -0.1167 | -0.0882 | -0.0551 | +0.0391 | -0.0465 | +0.0730 |
