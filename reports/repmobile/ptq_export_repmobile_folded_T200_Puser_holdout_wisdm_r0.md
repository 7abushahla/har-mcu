# PTQ Export (T=200, protocol=user_holdout, variant=default)

- Checkpoint: `/home/dellio/github/har-mcu/checkpoints/repmobile_folded_T200_Puser_holdout_wisdm_r0.keras`
- TFLite: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- PTQ size: 46.66 KB
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- Error: `Unsupported TFLM ops: DELEGATE, DEPTHWISE_CONV_2D, EXPAND_DIMS, MEAN`
- Unsupported ops: `DELEGATE, DEPTHWISE_CONV_2D, EXPAND_DIMS, MEAN`

## Notes

- Converted with builtin TFLite ops path
