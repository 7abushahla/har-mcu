# M3 Rotation Ablation Summary

- Source: `reports/m3/dual_domain_eval/dual_domain_eval_master.csv`
- Rows: `264`
- Values below are means across the 11 M3 experiments E00/E03-E12. Deltas are augmentation on minus off.

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| daghero_cnn_2layer_conv2d | fp32 | wisdm | 0.7636 | 0.7348 | -0.0288 | 0.7077 | 0.6445 | -0.0632 |
| daghero_cnn_2layer_conv2d | fp32 | arduino | 0.5286 | 0.5241 | -0.0045 | 0.4641 | 0.4695 | +0.0053 |
| daghero_cnn_2layer_conv2d | ptq | wisdm | 0.7511 | 0.7349 | -0.0162 | 0.6815 | 0.6453 | -0.0361 |
| daghero_cnn_2layer_conv2d | ptq | arduino | 0.5274 | 0.5411 | +0.0137 | 0.4628 | 0.4851 | +0.0223 |
| daghero_cnn_2layer_conv2d | qat | wisdm | 0.7505 | 0.7376 | -0.0129 | 0.6796 | 0.6499 | -0.0297 |
| daghero_cnn_2layer_conv2d | qat | arduino | 0.5286 | 0.5331 | +0.0045 | 0.4636 | 0.4732 | +0.0096 |
| deepconv_lstm_conv2d | fp32 | wisdm | 0.7398 | 0.7188 | -0.0210 | 0.6715 | 0.6106 | -0.0609 |
| deepconv_lstm_conv2d | fp32 | arduino | 0.5425 | 0.5170 | -0.0255 | 0.4971 | 0.4577 | -0.0394 |
| deepconv_lstm_conv2d | ptq | wisdm | 0.7386 | 0.7187 | -0.0199 | 0.6675 | 0.6100 | -0.0575 |
| deepconv_lstm_conv2d | ptq | arduino | 0.5361 | 0.5164 | -0.0197 | 0.4941 | 0.4606 | -0.0335 |
| deepconv_lstm_conv2d | qat | wisdm | 0.7004 | 0.4606 | -0.2398 | 0.6127 | 0.3198 | -0.2929 |
| deepconv_lstm_conv2d | qat | arduino | 0.4495 | 0.3057 | -0.1439 | 0.4018 | 0.2439 | -0.1579 |
