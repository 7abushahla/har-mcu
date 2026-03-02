# PTQ Export (T=200, protocol=random_stratified, variant=default)

- Checkpoint: `/home/dellio/github/har-mcu/checkpoints/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0.keras`
- TFLite: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- PTQ size: 623.99 KB
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- Error: `Unsupported TFLM ops: BATCH_MATMUL, BATCH_TO_SPACE_ND, CONCATENATION, FILL, MEAN, PAD, REDUCE_PROD, RSQRT, SPACE_TO_BATCH_ND, SQUARED_DIFFERENCE, SUB`
- Unsupported ops: `BATCH_MATMUL, BATCH_TO_SPACE_ND, CONCATENATION, FILL, MEAN, PAD, REDUCE_PROD, RSQRT, SPACE_TO_BATCH_ND, SQUARED_DIFFERENCE, SUB`

## Notes

- Converted with builtin TFLite ops path
