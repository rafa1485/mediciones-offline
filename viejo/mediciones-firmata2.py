import pyfirmata2
from threading import Timer

class Mediciones():
    def __init__(self, board, seconds):
        # pin 13 which is connected to the internal LED
        #self.digital_0 = board.get_pin('d:13:o')

        self.analog_0 = board.get_pin('a:0:i')

        # flag that we want the timer to restart itself in the callback
        self.timer = None

        # delay
        self.DELAY = seconds

    # callback function which toggles the digital port and
    # restarts the timer
    def readCallback(self):
        # call itself again so that it runs periodically
        self.timer = Timer(self.DELAY,self.readCallback)

        # start the timer
        self.timer.start()
        
        valor = self.analog_0.read()
        print(valor)

    # starts the blinking
    def start(self):
        # Kickstarting the perpetual timer by calling the
        # callback function once
        self.readCallback()

    # stops the blinking
    def stop(self):
        # Cancel the timer
        self.timer.cancel()

# main program

# Adjust that the port match your system, see samples below:
# On Linux: /dev/ttyACM0,
# On Windows: COM1, COM2, ...
PORT =  pyfirmata2.Arduino.AUTODETECT

# Creates a new board
board = pyfirmata2.Arduino(PORT)

t = Mediciones(board,1)
t.start()

print("To stop the program press return.")
# Just blocking here to do nothing.
input()

t.stop()

# close the serial connection
board.exit()