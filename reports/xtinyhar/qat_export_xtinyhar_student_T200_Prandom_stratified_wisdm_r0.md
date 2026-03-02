# QAT Export (T=200, protocol=random_stratified, variant=default)

- QAT checkpoint: `/home/dellio/github/har-mcu/checkpoints/xtinyhar_student_T200_Prandom_stratified_wisdm_r0_qat.keras`
- Status: `failed`
- Deployable full integer: `False`
- Full integer I/O: `False`
- TFLM compatible: `False`
- Input dtype: `None`
- Output dtype: `None`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Representative source: `train`
- Representative samples: `128`
- Error: `Unable to construct QAT model: Layer patch_embed:<class 'keras.src.layers.convolutional.conv1d.Conv1D'> is not supported. You can quantize this layer by passing a `tfmot.quantization.keras.QuantizeConfig` instance to the `quantize_annotate_layer` API.`

## Notes

- Unable to construct QAT model: Layer patch_embed:<class 'keras.src.layers.convolutional.conv1d.Conv1D'> is not supported. You can quantize this layer by passing a `tfmot.quantization.keras.QuantizeConfig` instance to the `quantize_annotate_layer` API.
