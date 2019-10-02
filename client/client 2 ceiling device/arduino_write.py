# This is the code to test writing to the pins on an arduino
# To get path to device in linux, run 'ls -lha /dev/tty* > plugged.txt' while it is plugged in
# Then unplug to device and run 'ls -lha /dev/tty* > noplug.txt'
# Then do a vim diff ``vimdiff plugged.txt np.txt`` to find the device

import pyfirmata
import time

path_to_device = "/dev/tty.usbmodem144301"
board = pyfirmata.Arduino(path_to_device)
print(board)
it = pyfirmata.util.Iterator(board)
it.start()

# specify pin and input/output mode
led = board.get_pin('d:7:o')
print(led)

# write to pin with led
led.write(1)
time.sleep(10)
