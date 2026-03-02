# QAT Export (T=200, protocol=random_stratified, variant=default)

- QAT checkpoint: `/home/dellio/github/har-mcu/checkpoints/repmobile_folded_conv2d_T200_Prandom_stratified_wisdm_r0_qat.keras`
- QAT tflite: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- QAT training time: 43.362 s
- QAT history JSON: `/home/dellio/github/har-mcu/checkpoints/history_repmobile_folded_conv2d_T200_Prandom_stratified_wisdm_r0_qat.json`
- Error: `Unsupported TFLM ops: DEPTHWISE_CONV_2D, MEAN`
- Unsupported ops: `DEPTHWISE_CONV_2D, MEAN`

## Notes

- QAT strategy: annotate_policy_all_supported
- Exported with builtin TFLite ops path
