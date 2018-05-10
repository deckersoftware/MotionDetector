#!/usr/bin/python3

import time
import threading
import RPi.GPIO as GPIO
from config import Configuration
from display import Display

CONFIG_DATA = Configuration().get_config_data()
DISPLAY_OBJECT = Display(CONFIG_DATA)

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = CONFIG_DATA['motion_input_pin']
GPIO.setup(GPIO_PIR, GPIO.IN)

TIMER_THREAD = None

def motion_detection_event():
    global TIMER_THREAD
    if TIMER_THREAD != None:
        TIMER_THREAD.cancel()

    input_signal = GPIO.input(GPIO_PIR)
    if DISPLAY_OBJECT.is_turn_on_condition(input_signal):
        TIMER_THREAD = threading.Timer(CONFIG_DATA['display_turn_on_duration_in_seconds'], DISPLAY_OBJECT.turn_display_off)

    if DISPLAY_OBJECT.is_turn_off_condition(input_signal):
        TIMER_THREAD = threading.Timer(CONFIG_DATA['display_turn_off_duration_in_seconds'], DISPLAY_OBJECT.turn_display_on)

    if TIMER_THREAD is not None:
        if not TIMER_THREAD.is_alive():
            TIMER_THREAD.start()

GPIO.add_event_detect(GPIO_PIR, GPIO.BOTH, callback=motion_detection_event, bouncetime=250)

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    GPIO.cleanup()
