import threading
from subprocess import call
import RPi.GPIO as GPIO

class MotionDetector:
    _timer_thread = None
    _config_data = None

    def __init__(self, config_data):
        self._motion_detected = False
        self._config_data = config_data
        self.gpio_pir = self._config_data['motion_input_pin']

    def motion_detection_event(self, channel):
        del channel
        if self._timer_thread != None:
            self._timer_thread.cancel()

        self._input_signal = GPIO.input(self.gpio_pir)
        if self._is_turn_on_condition():
            self._timer_thread = threading.Timer( \
                self._config_data['display_turn_on_duration_in_seconds'], \
                self._no_motion_detected_action \
                )

        if self._is_turn_off_condition():
            self._timer_thread = threading.Timer( \
                self._config_data['display_turn_off_duration_in_seconds'], \
                self._motion_detected_action \
                )

            if not self._timer_thread.is_alive():
                self._timer_thread.start()

    def _no_motion_detected_action(self):
        self._motion_detected = False
        call(self._config_data["no_motion_action"], shell=True)

    def _motion_detected_action(self):
        self._motion_detected = True
        call(self._config_data["motion_action"], shell=True)

    def _is_turn_on_condition(self):
        return self._input_signal == 0 and self._motion_detected

    def _is_turn_off_condition(self):
        return self._input_signal == 1 and not self._motion_detected
