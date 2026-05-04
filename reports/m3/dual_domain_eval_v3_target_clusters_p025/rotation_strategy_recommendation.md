# M3 Rotation Strategy Recommendation

- Sources: v1 uniform, v2 bounded, and v3 target-gravity dual-domain eval masters.
- Recommendation: do not deploy a rotation-augmented model by default yet; use Daghero E09 no-augmentation QAT as the first on-device candidate, with PTQ as backup.
- Reason: v3 does not beat the no-augmentation baseline on the deployment-relevant E09-E12 subset, and stored Arduino standing/walking recall is already saturated for the best Daghero baselines.

## V3 Mean Ablation

# M3 Rotation V3 Ablation Summary

- Source: `reports/m3/dual_domain_eval_v3_target_clusters_p025/dual_domain_eval_master.csv`
- Rows: `264`
- Deltas are target-gravity on minus clean no-augmentation v2 baseline.

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| daghero_cnn_2layer_conv2d | fp32 | arduino | 0.5286 | 0.5281 | -0.0005 | 0.4643 | 0.4635 | -0.0008 |
| daghero_cnn_2layer_conv2d | fp32 | wisdm | 0.7626 | 0.7457 | -0.0169 | 0.7099 | 0.6630 | -0.0469 |
| daghero_cnn_2layer_conv2d | ptq | arduino | 0.5269 | 0.5255 | -0.0014 | 0.4623 | 0.4624 | +0.0001 |
| daghero_cnn_2layer_conv2d | ptq | wisdm | 0.7503 | 0.7433 | -0.0070 | 0.6777 | 0.6608 | -0.0169 |
| daghero_cnn_2layer_conv2d | qat | arduino | 0.5283 | 0.5370 | +0.0087 | 0.4630 | 0.4768 | +0.0139 |
| daghero_cnn_2layer_conv2d | qat | wisdm | 0.7523 | 0.7421 | -0.0102 | 0.6873 | 0.6567 | -0.0306 |
| deepconv_lstm_conv2d | fp32 | arduino | 0.5350 | 0.5236 | -0.0113 | 0.4890 | 0.4569 | -0.0321 |
| deepconv_lstm_conv2d | fp32 | wisdm | 0.7416 | 0.7363 | -0.0053 | 0.6756 | 0.6505 | -0.0250 |
| deepconv_lstm_conv2d | ptq | arduino | 0.5325 | 0.5217 | -0.0109 | 0.4874 | 0.4555 | -0.0319 |
| deepconv_lstm_conv2d | ptq | wisdm | 0.7380 | 0.7358 | -0.0021 | 0.6687 | 0.6488 | -0.0199 |
| deepconv_lstm_conv2d | qat | arduino | 0.4726 | 0.4291 | -0.0435 | 0.4276 | 0.3773 | -0.0504 |
| deepconv_lstm_conv2d | qat | wisdm | 0.6899 | 0.6681 | -0.0218 | 0.6048 | 0.5680 | -0.0368 |

## Deployment-Subset Failure-Focus Deltas

# Arduino Failure-Focus Delta Summary: E09-E12 Only, V1/V2/V3

Positive recall deltas are good. Negative confusion-pair deltas are good.

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
