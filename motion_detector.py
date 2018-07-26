import threading
from subprocess import call
from datetime import datetime
import calendar
import RPi.GPIO as GPIO

class MotionDetector:
    _timer_thread = None
    _config_data = None
    _motion_detected = False
    _input_signal = 0

    def __init__(self, config_data, lock):
        self._config_data = config_data
        self._lock = lock
        self.gpio_pir = self._config_data['motion_input_pin']

    def motion_detection_event(self):
        self._lock.acquire()
        if self._timer_thread != None:
            self._timer_thread.cancel()

        self._timer_thread = None

        self._input_signal = GPIO.input(self.gpio_pir)
        if self._is_no_motion_detected_anymore_condition():
            self._timer_thread = threading.Timer( \
                self._config_data['motion_detected_duration_in_seconds'], \
                self._no_motion_detected_action \
                )

        if self._is_new_motion_detetected_condition():
            self._timer_thread = threading.Timer( \
                self._config_data['no_motion_detected_duration_in_seconds'], \
                self._motion_detected_action \
                )

        if not self._timer_thread is None and not self._timer_thread.is_alive():
            self._timer_thread.start()
        self._lock.release()

    def _no_motion_detected_action(self):
        self._motion_detected = False
        call(self._config_data["no_motion_action"], shell=True)

    def _motion_detected_action(self):
        self._motion_detected = True
        call(self._config_data["motion_action"], shell=True)

    def _is_no_motion_detected_anymore_condition(self):
        return self._input_signal == 0 and self._motion_detected

    def _is_new_motion_detetected_condition(self):
        if not self._is_motion_detection_time():
            return False
        return self._input_signal == 1 and not self._motion_detected

    def _is_motion_detection_time(self):
        motion_detection_time = self._get_motion_detection_time()
        detection_start_time = datetime.strptime(motion_detection_time[0], '%H:%M').time()
        detection_stop_time = datetime.strptime(motion_detection_time[1], '%H:%M').time()
        current_time = datetime.now().time()
        return current_time >= detection_start_time and current_time <= detection_stop_time

    def _get_motion_detection_time(self):
        week_day_name = calendar.day_name[datetime.now().weekday()].lower()
        motion_detection_time_of_today = self._config_data['motion_detection_time'][week_day_name]
        return motion_detection_time_of_today.split()
