# Code that will write to raspberry pi zero

import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)

# add rising edge detection on a channel
GPIO.add_event_detect(17, GPIO.RISING) # For fire
GPIO.add_event_detect(27, GPIO.RISING) # For shooter


class Button():

    def listen_for_press():
        while True:
            if GPIO.event_detected(17):
                print('Button 1 pressed')
                return 1
            if GPIO.event_detected(27):
                print('Button 2 pressed')
                # return and send shooter message to server
                return 2
            time.sleep(0.0001)
