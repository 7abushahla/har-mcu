# QAT Export (T=200, protocol=random_stratified, variant=default)

- QAT checkpoint: `/home/dellio/github/har-mcu/checkpoints/repmobile_folded_T200_Prandom_stratified_wisdm_r0_qat.keras`
- QAT tflite: `/home/dellio/github/har-mcu/models_tflite/repmobile_folded_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `False`
- TFLM compatible: `False`
- Input dtype: `None`
- Output dtype: `None`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- QAT history JSON: `/home/dellio/github/har-mcu/checkpoints/history_repmobile_folded_T200_Prandom_stratified_wisdm_r0_qat.json`
- Error: `Unable to construct QAT model: Requested the deserialization of a Lambda layer with a Python `lambda` inside it. This carries a potential risk of arbitrary code execution and thus it is disallowed by default. If you trust the source of the saved model, you can pass `safe_mode=False` to the loading function in order to allow Lambda layer loading.`

## Notes

- Experimental native SeparableConv1D QAT attempt enabled. If conversion fails, fallback to Conv2D-safe RepMobile variant.
- Unable to construct QAT model: Requested the deserialization of a Lambda layer with a Python `lambda` inside it. This carries a potential risk of arbitrary code execution and thus it is disallowed by default. If you trust the source of the saved model, you can pass `safe_mode=False` to the loading function in order to allow Lambda layer loading.
