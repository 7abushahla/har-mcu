// TinyML kit: shield button on D13 (P0.13). Same nRF init/read pattern as
// Harvard_TinyMLx/src/TinyMLShield.h, without linking that package (TFLite fork conflict).

#include "tinyml_shield.h"
#include <Arduino.h>
#include <nrf_gpio.h>

// Arduino D13 = P0.13 (LED + shield button, active low; see NANO 33 BLE variant).
static const uint32_t kShieldButtonPinNrf = NRF_GPIO_PIN_MAP(0, 13);
static const int kShieldButtonPinArduino = 13;

static void nrf_gpio_cfg_out_with_input(uint32_t pin_number) {
  nrf_gpio_cfg(
      pin_number, NRF_GPIO_PIN_DIR_OUTPUT, NRF_GPIO_PIN_INPUT_CONNECT, NRF_GPIO_PIN_PULLUP,
      NRF_GPIO_PIN_S0S1, NRF_GPIO_PIN_NOSENSE);
}

// Harvard TinyMLShield.h debounce, verbatim logic (pin via nrf, not digitalPinToPinName).
static unsigned long lastDebounceTime = 0;
static const unsigned long debounceDelay = 50;
static bool lastButtonState = true;
static bool buttonState = true;

void initializeShield() {
  pinMode(kShieldButtonPinArduino, OUTPUT);
  digitalWrite(kShieldButtonPinArduino, HIGH);
  nrf_gpio_cfg_out_with_input(kShieldButtonPinNrf);
}

bool readShieldButton() {
  const bool buttonRead = (nrf_gpio_pin_read(kShieldButtonPinNrf) != 0U);

  if (buttonRead != lastButtonState) {
    lastDebounceTime = millis();
  }

  if (millis() - lastDebounceTime >= debounceDelay) {
    if (buttonRead != buttonState) {
      buttonState = buttonRead;
      if (!buttonState) {
        lastButtonState = buttonRead;
        return true;
      }
    }
  }
  lastButtonState = buttonRead;
  return false;
}

bool readShieldButtonDown() {
  // Pull-up: pin reads high when not pressed, low when pressed.
  return (nrf_gpio_pin_read(kShieldButtonPinNrf) == 0U);
}
