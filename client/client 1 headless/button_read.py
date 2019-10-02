# Code that will write to raspberry pi zero

import RPi.GPIO as gpio

#gpio.setmode(gpio.BCM)
#gpio.setup(18, gpio.OUT)

# add rising edge detection on a channel
#GPIO.add_event_detect(17, GPIO.RISING) # For fire
#GPIO.add_event_detect(27, GPIO.RISING) # For shooter

class Button():

    def listen_for_press():
        while True:
            if GPIO.input(20):
                print('Button 1 pressed')
            if GPIO.event_detected(21):
                print('Button 2 pressed')
                # return and send shooter message to server
            time.sleep(0.0001)


def main ():
    Button.listen_for_press()
    GPIO.setupmode(GPIO.BCM)
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(21, GPIO.IN)

if __name__ == '__main__':
    main()
