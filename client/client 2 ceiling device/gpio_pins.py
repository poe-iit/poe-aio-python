import RPi.GPIO as GPIO
import time


# Emergency Type 1, write to pin 9
# Emergency Type 2, write to pin 10
# Emergency Type 3, write to pin 11
# Emergency Type 4, write to pin 12

# Smoke Detector will be attacked to two pins, pin 13 and 14.
# Will be listening for input on pin 13, if triggered there is a fire, trigger emergency type 1 and write to pin 9




class CeilingDeviceGPIO:

    def __init__(self):
        # Use BCM layout
        self.GPIO.setmode(GPIO.BCM)

        # setup emergency type pins
        self.GPIO.setup(9, GPIO.OUT) # Fire
        self.GPIO.setup(10, GPIO.OUT) # Shooter
        self.GPIO.setup(11, GPIO.OUT)
        self.GPIO.setup(12, GPIO.OUT)

        # setup smoke detector listener pin
        self.GPIO.setup(13, GPIO.IN)

    def listen_for_smoke(self):
        smoke_count = 0

        while smoke_count < 1:
            if not GPIO.input(13):
                print('Smoke Detected')
                GPIO.output(9, GPIO.HIGH) #trigger fire alert
                smoke_count+=1
            time.sleep(1)
        print("Smoke detected from ceiling client, notifying server and turning on fire lights")
        self.listen_for_smoke() #start listening again

    def write_to_GPIO(self, emergency_type):

        try:
            if emergency_type == 1:
                GPIO.output(9, GPIO.HIGH)
            if emergency_type == 2:
                GPIO.output(10, GPIO.HIGH)
            if emergency_type == 3:
                GPIO.output(11, GPIO.HIGH)
            if emergency_type == 4:
                GPIO.output(12, GPIO.HIGH)
        except:
            print("Failed to write to GPIO pins")
