# QAT Export (T=200, protocol=random_stratified, variant=default)

- QAT checkpoint: `/home/dellio/github/har-mcu/checkpoints/tcn_inception_conv2d_T200_Prandom_stratified_wisdm_r0_qat.keras`
- QAT tflite: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- QAT training time: 396.786 s
- QAT history JSON: `/home/dellio/github/har-mcu/checkpoints/history_tcn_inception_conv2d_T200_Prandom_stratified_wisdm_r0_qat.json`
- Error: `Unsupported TFLM ops: BATCH_TO_SPACE_ND, CONCATENATION, MAX_POOL_2D, MEAN, PAD, SPACE_TO_BATCH_ND`
- Unsupported ops: `BATCH_TO_SPACE_ND, CONCATENATION, MAX_POOL_2D, MEAN, PAD, SPACE_TO_BATCH_ND`

## Notes

- QAT strategy: annotate_policy_all_supported
- Exported with builtin TFLite ops path
