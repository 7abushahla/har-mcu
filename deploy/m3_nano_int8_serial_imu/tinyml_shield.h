// API-compatible with Harvard TinyMLShield: initializeShield() + readShieldButton(),
// D13, no TensorFlow, no camera — use with Arduino_TensorFlowLite only.
#ifndef TINYML_SHIELD_H
#define TINYML_SHIELD_H

void initializeShield();
bool readShieldButton();
// True while shield button is held (D13, active low). For release/short- vs long-press in sketches.
bool readShieldButtonDown();

#endif
