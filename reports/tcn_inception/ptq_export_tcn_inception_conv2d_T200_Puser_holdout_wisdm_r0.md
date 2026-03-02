# PTQ Export (T=200, protocol=user_holdout, variant=default)

- Checkpoint: `/home/dellio/github/har-mcu/checkpoints/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0.keras`
- TFLite: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- PTQ size: 379.45 KB
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- Error: `Unsupported TFLM ops: BATCH_TO_SPACE_ND, CONCATENATION, MAX_POOL_2D, MEAN, PAD, SPACE_TO_BATCH_ND`
- Unsupported ops: `BATCH_TO_SPACE_ND, CONCATENATION, MAX_POOL_2D, MEAN, PAD, SPACE_TO_BATCH_ND`

## Notes

- Converted with builtin TFLite ops path
