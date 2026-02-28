# Real-Time Human Activity Recognition on Microcontrollers: A Quantization-Aware Deep Learning Approach

_Hamza A. Abushahla, Ariel Justine N. Panopio, Layth Al-Khairulla, and Dr. Mohamed Hassan_

This repository contains the full implementation and supplementary materials for our research project, **"Real-Time Human Activity Recognition on Microcontrollers: A Quantization-Aware Deep Learning Approach,"** completed as part of the COE 59413 Tiny Machine Learning course at the American University of Sharjah.

## Dataset 

This work uses the **Wireless Sensor Data Mining (WISDM)** dataset as our primary public benchmark for human activity recognition (HAR). The dataset consists of **1,073,623 labeled samples** of motion data collected from **36 users** performing **six activities** over specific time periods: walking, jogging, sitting, standing, and ascending and descending stairs. The signals were recorded using smartphone accelerometers, which measure linear acceleration along three axes and can indirectly capture device orientation. Data were sampled at **20 Hz** (1 sample every 50 ms), yielding 20 samples per second.

Each record in the raw dataset contains:

- **User ID**: integer identifier of the subject (1–36).
- **Activity label**: one of `Walking`, `Jogging`, `Upstairs`, `Downstairs`, `Sitting`, or `Standing`.
- **Timestamp**: nanosecond-resolution time at which the sample was recorded.
- **X-axis acceleration**: acceleration along the x dimension (in device coordinates).
- **Y-axis acceleration**: acceleration along the y dimension.
- **Z-axis acceleration**: acceleration along the z dimension.
