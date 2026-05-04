# M3 Axis EDA

- Config: `configs/m3/E04_wisdm_to_g_arduino_g.yaml`
- Window size: `100` samples
- `wisdm`: rows `1073623`, users `36`, unit mode `wisdm_to_g`, total scale `0.10197162129779283`, downsample `False`
- `arduino`: rows `240620`, users `2`, unit mode `arduino_g`, total scale `4.0`, downsample `False`

## Window Energy Summary

| Activity | WISDM dynamic RMS | Arduino dynamic RMS | Arduino-WISDM | WISDM mean-vector norm | Arduino mean-vector norm |
| --- | ---: | ---: | ---: | ---: | ---: |
| Downstairs | 0.6310 | 0.7836 | +0.1527 | 1.0029 | 1.0077 |
| Jogging | 1.2839 | 1.4987 | +0.2147 | 0.8986 | 1.0782 |
| Sitting | 0.0242 | 0.0068 | -0.0174 | 1.0034 | 0.9979 |
| Standing | 0.0466 | 0.0118 | -0.0348 | 0.9992 | 0.9955 |
| Upstairs | 0.5983 | 0.8188 | +0.2205 | 0.9906 | 0.9891 |
| Walking | 0.7150 | 0.6788 | -0.0362 | 1.0309 | 1.0144 |

Interpretation notes:

- `mean-vector norm` is a window-level gravity/pose proxy when acceleration includes gravity.
- `dynamic RMS` is the residual motion energy after subtracting each window's mean vector.
- Compare static classes first. If Arduino Standing has dynamic energy closer to WISDM Walking than to WISDM Standing, the live Standing-to-Walking failure is likely not solved by orientation augmentation alone.
