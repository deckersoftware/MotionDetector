#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import threading
from config import configuration
from display import display

config_data = configuration().get_config_data()
display_object = display(config_data)

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = config_data['motion_input_pin']
GPIO.setup(GPIO_PIR, GPIO.IN)

timer_thread = None

def motion_detection_event(channel):
    global timer_thread
    if timer_thread != None:
        timer_thread.cancel()

    input_signal = GPIO.input(GPIO_PIR)
    if display_object.is_turn_on_condition(input_signal):
        timer_thread = threading.Timer(config_data['display_turn_on_duration_in_seconds'], display_object.turn_display_off)

    if display_object.is_turn_off_condition(input_signal):
        timer_thread = threading.Timer(config_data['display_turn_off_duration_in_seconds'], display_object.turn_disply_on)

    if timer_thread is not None:
        if not timer_thread.is_alive():
            timer_thread.start()

GPIO.add_event_detect(GPIO_PIR, GPIO.BOTH, callback = motion_detection_event, bouncetime = 250)

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    GPIO.cleanup()
