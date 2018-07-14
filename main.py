#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import threading
from config import Configuration
from motion_detector import MotionDetector
from event_thread import EventThread

CONFIG_DATA = Configuration().get_config_data()
LOCK = threading.Lock()
MOTION_DETECTOR = MotionDetector(CONFIG_DATA, LOCK)

def execute_event_thread(channel):
    del channel
    _event_thread = EventThread(MOTION_DETECTOR.motion_detection_event)

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = CONFIG_DATA['motion_input_pin']
GPIO.setup(GPIO_PIR, GPIO.IN)
GPIO.add_event_detect( \
    GPIO_PIR, \
    GPIO.BOTH, \
    callback=execute_event_thread, \
    bouncetime=250 \
    )

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    GPIO.cleanup()
