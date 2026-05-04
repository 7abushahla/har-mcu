# M3 Rotation V3 Ablation Summary

- Source: `reports/m3/dual_domain_eval_v3_target_clusters_p025/dual_domain_eval_master.csv`
- Rows: `264`
- Values are means across E00/E03-E12. Deltas are target-gravity rotation on minus clean no-augmentation v2 baseline.

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
