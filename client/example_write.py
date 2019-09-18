# Code that will write to raspberry pi zero

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)

while True:
    gpio.output(18, gpio.HIGH)
