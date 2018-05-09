#!/usr/bin/python3

import os
import RPi.GPIO as GPIO
import time
import threading
import json
from subprocess import call
from config import configuration

config_data = configuration().get_config_data()

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = config_data['motion_input_pin']
GPIO.setup(GPIO_PIR, GPIO.IN)

timer_thread = None
hdmi_on = 0

def motion_detection_event(channel):
    global timer_thread
    if timer_thread != None:
        timer_thread.cancel()

    if is_turn_on_condition():
        timer_thread = threading.Timer(config_data['display_turn_on_duration_in_seconds'], turn_hdmi_off)

    if is_turn_off_condition():
        timer_thread = threading.Timer(config_data['display_turn_off_duration_in_seconds'], turn_hdmi_on)

    if timer_thread is not None:
        if not timer_thread.is_alive():
            timer_thread.start()

def turn_hdmi_off():
    global hdmi_on
    hdmi_on = 0
    call(config_data["turn_off_action"], shell=True)

def turn_hdmi_on():
    global hdmi_on
    hdmi_on = 1
    call(config_data["turn_on_action"], shell=True)

def is_turn_on_condition():
    global hdmi_on
    input_signal = GPIO.input(GPIO_PIR)
    return input_signal == 0 and hdmi_on == 1

def is_turn_off_condition():
    global hdmi_on
    input_signal = GPIO.input(GPIO_PIR)
    return input_signal == 1 and hdmi_on == 0

GPIO.add_event_detect(GPIO_PIR, GPIO.BOTH, callback = motion_detection_event, bouncetime = 250)

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    GPIO.cleanup()
