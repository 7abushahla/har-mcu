# QAT Export (T=200, protocol=user_holdout, variant=default)

- QAT checkpoint: `/home/dellio/github/har-mcu/checkpoints/xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_qat.keras`
- QAT tflite: `/home/dellio/github/har-mcu/models_tflite/xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `True`
- TFLM compatible: `False`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- QAT training time: 15.397 s
- QAT history JSON: `/home/dellio/github/har-mcu/checkpoints/history_xtinyhar_student_conv2d_T200_Puser_holdout_wisdm_r0_qat.json`
- Error: `Unsupported TFLM ops: BATCH_MATMUL, CONCATENATION, GATHER, GELU, MEAN, REDUCE_PROD, RSQRT, SQUARED_DIFFERENCE, SUB`
- Unsupported ops: `BATCH_MATMUL, CONCATENATION, GATHER, GELU, MEAN, REDUCE_PROD, RSQRT, SQUARED_DIFFERENCE, SUB`

## Notes

- QAT strategy: annotate_policy_auto
- Exported with builtin TFLite ops path
