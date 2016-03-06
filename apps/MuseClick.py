
from liblo import *
import sys
import time
#import win32con
#from win32 import win32api
import turtle
# Global Constant(s)
UPPER_ZERO_RANGE = 8
LOWER_ZERO_RANGE = -8
MAX_DELAY_COUNT = 50
MOUSE_MOVE_INCREMENT = 3
STATES = {0: "STATIONARY",
          1: "LEFT",
          2: "RIGHT",
          3: "UP",
          4: "DOWN"}

class MuseServer(ServerThread):
    
    # Listen for messages on port 5001
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.x = 0
        self.y = 0           # indicates position of mouse cursor, initialized at (0, 0)
        self.delay_counter = 0          # delay counter used to eliminate false positives/negatives
        self.state = 0                  # indicates current state
        self.turtle = Cursor(self.x, self.y)
        self.move_cursor()

    # Callback method to handle accelerometer data 
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        print(100)              

        if self.delay_counter == MAX_DELAY_COUNT:         
          
            # Finite State Machine used to determine direction of movement of mouse cursor            

            # STATE 0: Stationary
            # STATE 1: Move cursor left
            # STATE 2: Move cursor right
            # STATE 3: Move cursor up
            # STATE 4: Move cursor down
            print(1)
            print(STATES[self.state])

            change_in_acceleration = args[0] - self.previous_acceleration 

            # If user shakes head to the left ...
            if change_in_acceleration < LOWER_ZERO_RANGE:
                if self.state == 0:
                    self.state = 1
                
                elif self.state == 1:
                    self.state = 4
                
                elif self.state == 2:
                    self.state = 0
                
                elif self.state == 3:
                    self.state = 0
                
                elif self.state == 4:
                    self.state = 0
                
                self.delay_counter = 0 

            # If user shakes head to the right ...
            elif change_in_acceleration > UPPER_ZERO_RANGE:
                if self.state == 0:
                    self.state = 2
                
                elif self.state == 1:
                    self.state = 0
                
                elif self.state == 2:
                    self.state = 3
                
                elif self.state == 3:
                    self.state = 0
                
                elif self.state == 4:
                    self.state = 0
                
                self.delay_counter = 0 

            # Move mouse cursor depending on which state program is in
            if self.state == 1:
                self.x -= MOUSE_MOVE_INCREMENT
            elif self.state == 2:
                self.x += MOUSE_MOVE_INCREMENT
            elif self.state == 3:
                self.y -= MOUSE_MOVE_INCREMENT
            elif self.state == 4:
                self.y += MOUSE_MOVE_INCREMENT
            print(1)
            self.move_cursor()
                
            self.previous_acceleration = args[0]

        else:
            # set up delay to eliminate false positives/negatives
            self.delay_counter += 1
            self.previous_acceleration = args[0]


    def move_cursor(self):
        self.turtle.move(self.x, self.y)

class Cursor(turtle.Turtle):
    
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.penup()
        self.goto(x, y)

    def move(self,  x, y):
        self.goto(x, y)


def main():
    while True:
          try:
                    print(10)
                    server = MuseServer()
          except ServerError as e:
                    print(str(e))
                    sys.exit()
          
          server.start()

    while True:
        time.sleep(1)
        

if __name__ == "__main__":
    window = turtle.Screen()
    window.title('Title')
    main()
    window.mainloop()

