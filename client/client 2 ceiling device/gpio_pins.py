import RPi.GPIO as GPIO


# Emergency Type 1, write to pin 9
# Emergency Type 2, write to pin 10
# Emergency Type 3, write to pin 11
# Emergency Type 4, write to pin 12

# Smoke Detector will be attacked to two pins, pin 13 and 14.
# Will be listening for input on pin 13, if triggered there is a fire, trigger emergency type 1 and write to pin 9




class CeilingDeviceGPIO:

    def init():
        # Use BCM layout
        GPIO.setmode(GPIO.BCM)

        # setup emergency type pins
        GPIO.setup(9, GPIO.OUT) # Fire
        GPIO.setup(10, GPIO.OUT) # Shooter
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)

        # setup smoke detector listener pin
        GPIO.setup(13, GPIO.IN)

    def listen_for_smoke():

        while True:
            if GPIO.input(13):
                print('Smoke Detected')
                GPIO.Output(9) # Trigger fire alert
            time.sleep(0.0001)

    def write_to_GPIO(emergency_type):

        try:
            if emergency_type == 1:
                GPIO.Output(9)
            if emergency_type == 2:
                GPIO.Output(10)
            if emergency_type == 3:
                GPIO.Output(11)
            if emergency_type == 4:
                GPIO.Output(12)
        except:
            print("Failed to write to GPIO pins")
