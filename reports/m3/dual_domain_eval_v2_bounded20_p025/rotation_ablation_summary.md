# M3 Rotation V2 Ablation Summary

- Source: `reports/m3/dual_domain_eval_v2_bounded20_p025/dual_domain_eval_master.csv`
- Rows: `264`
- Values are means across E00/E03-E12. Deltas are bounded rotation on minus no-augmentation v2 baseline.

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| daghero_cnn_2layer_conv2d | fp32 | arduino | 0.5286 | 0.5387 | +0.0101 | 0.4643 | 0.4775 | +0.0132 |
| daghero_cnn_2layer_conv2d | fp32 | wisdm | 0.7626 | 0.7629 | +0.0003 | 0.7099 | 0.7069 | -0.0030 |
| daghero_cnn_2layer_conv2d | ptq | arduino | 0.5269 | 0.5402 | +0.0133 | 0.4623 | 0.4745 | +0.0123 |
| daghero_cnn_2layer_conv2d | ptq | wisdm | 0.7503 | 0.7472 | -0.0031 | 0.6777 | 0.6760 | -0.0017 |
| daghero_cnn_2layer_conv2d | qat | arduino | 0.5283 | 0.5317 | +0.0034 | 0.4630 | 0.4700 | +0.0071 |
| daghero_cnn_2layer_conv2d | qat | wisdm | 0.7523 | 0.7488 | -0.0035 | 0.6873 | 0.6812 | -0.0061 |
| deepconv_lstm_conv2d | fp32 | arduino | 0.5350 | 0.5219 | -0.0130 | 0.4890 | 0.4700 | -0.0189 |
| deepconv_lstm_conv2d | fp32 | wisdm | 0.7416 | 0.7282 | -0.0134 | 0.6756 | 0.6396 | -0.0360 |
| deepconv_lstm_conv2d | ptq | arduino | 0.5325 | 0.5212 | -0.0113 | 0.4874 | 0.4694 | -0.0180 |
| deepconv_lstm_conv2d | ptq | wisdm | 0.7380 | 0.7312 | -0.0068 | 0.6687 | 0.6444 | -0.0243 |
| deepconv_lstm_conv2d | qat | arduino | 0.4726 | 0.4509 | -0.0217 | 0.4276 | 0.3997 | -0.0279 |
| deepconv_lstm_conv2d | qat | wisdm | 0.6899 | 0.7105 | +0.0206 | 0.6048 | 0.6163 | +0.0115 |
