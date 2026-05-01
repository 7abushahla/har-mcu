# PTQ Export (T=100, protocol=random_stratified, variant=default)

- Checkpoint: `/shared/b00088568/github/har-mcu/checkpoints/m3/E00_wisdm_m2_anchor/full_e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0.keras`
- TFLite: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/full_e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_ptq_int8.tflite`
- PTQ size: 136.92 KB
- Status: `ok`
- PTQ status alias: `ok`
- Deployable full integer: `True`
- Full integer I/O: `True`
- TFLM compatible: `True`
- Compatibility scope: `micro_mutable_main`
- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Accepted integer I/O dtypes: `['int8', 'uint8']`
- Allowed ops profile (legacy, non-gating): `micro_mutable_main`
- Representative source: `train`
- Representative samples: `256`
- Allowed ops used: `['ADD', 'ARG_MAX', 'ARG_MIN', 'AVERAGE_POOL_2D', 'BATCH_MATMUL', 'BATCH_TO_SPACE_ND', 'CAST', 'CEIL', 'CIRCULAR_BUFFER', 'CONCATENATION', 'CONV_2D', 'COS', 'CUMSUM', 'DEPTHWISE_CONV_2D', 'DEPTH_TO_SPACE', 'DEQUANTIZE', 'DIV', 'ELU', 'EQUAL', 'ETHOSU', 'EXP', 'EXPAND_DIMS', 'FILL', 'FLOOR', 'FLOOR_DIV', 'FLOOR_MOD', 'FULLY_CONNECTED', 'GATHER', 'GATHER_ND', 'GREATER', 'GREATER_EQUAL', 'HARD_SWISH', 'IF', 'L2_NORMALIZATION', 'L2_POOL_2D', 'LEAKY_RELU', 'LESS', 'LESS_EQUAL', 'LOG', 'LOGICAL_AND', 'LOGICAL_NOT', 'LOGICAL_OR', 'LOGISTIC', 'LOG_SOFTMAX', 'MAXIMUM', 'MAX_POOL_2D', 'MEAN', 'MINIMUM', 'MIRROR_PAD', 'MUL', 'NEG', 'NOT_EQUAL', 'PACK', 'PAD', 'PADV2', 'PRELU', 'QUANTIZE', 'READ_VARIABLE', 'REDUCE_MAX', 'REDUCE_MIN', 'RELU', 'RELU6', 'RELU_0_TO_1', 'RELU_N1_TO_1', 'RESHAPE', 'RESIZE_BILINEAR', 'RESIZE_NEAREST_NEIGHBOR', 'ROUND', 'RSQRT', 'SELECT_V2', 'SHAPE', 'SIN', 'SLICE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'SPACE_TO_DEPTH', 'SPLIT', 'SPLIT_V', 'SQRT', 'SQUARE', 'SQUARED_DIFFERENCE', 'SQUEEZE', 'STRIDED_SLICE', 'SUB', 'SVDF', 'TANH', 'TRANSPOSE', 'TRANSPOSE_CONV', 'UNIDIRECTIONAL_SEQUENCE_LSTM', 'UNPACK', 'VAR_HANDLE', 'WHILE', 'ZEROS_LIKE']`

## Notes

- Converted with builtin TFLite ops path
