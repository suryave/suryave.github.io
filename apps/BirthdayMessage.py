import turtle
import random

class Birthday(turtle.Turtle):
    def __init__(self, x, y, color):
        turtle.Turtle.__init__(self)
        self.shape('circle')
        self.width = 10
        self.speed = 0
        self.penup()
        self.goto(x, y)
        self.color(color)
class CircleBox:
    def __init__(self, width, height):
        self.window = turtle.Screen()
        self.window.title('Happy Birthday!')
        self.width = width
        self.height = height
        self.circles = [[0 for x in range(width)] for x in range(height)]
        self.negcircles = [[0 for x in range(width)] for x in range(height)]
        for i in range(1, width):
            for j in range(height):
                self.negcircles[i][j] = Birthday(-40*i, 40*j + 50, colors[j])
        for i in range(width):
            for j in range(height):
                self.circles[i][j] = Birthday(40*i, 40*j +50, colors[j])
        for i in range(1, 6):
            for j in range(1, 6):
                self.negcircles[i][j].hideturtle()
        for i in range(0, 6):
            for j in range(1, 6):
                self.circles[i][j].hideturtle()
        self.messenger = turtle.Turtle()
        self.messenger.hideturtle()
        self.messenger.penup()
        self.writehb()
        self.colorchange()
        self.window.mainloop()
    def writehb(self):
        self.messenger.goto(-222, 190)
        self.messenger.write("Happy Birthday!", font=("Arial", 32, "normal"))
        self.messenger.goto(-200, 130)
        self.messenger.write("-Have a Great Day!", font=("Arial", 20, "normal"))
        self.startup()

    def startup(self):
        t = self.messenger
        t.speed(0)
        t.penup()
        t.goto(-200,-310)
        t.pendown()
        sierpinski(t, 400, 5)
        t.ht()
        self.colorchange()
    def colorchange(self):
        while True:
            for i in range(1, 7):
                for j in range(0, 7):
                    if i == 6 or j == 0 or i == 6:
                        self.negcircles[i][j].color(colors[random.randint(0, 6)])
            for i in range (0, 7):
                for j in range (0, 7):
                    if j == 0 or j == 6 or i == 6:
                        self.circles[i][j].color(colors[random.randint(0, 6)])


def sierpinski(t, size,depth):
    '''sierpinski(t,size,depth) -> None
    uses turtle t to draw a sierpinski triangle
    size is the overall side length
    depth is the depth'''
    # base case
    if depth == 0:
        # draw an equilateral triangle
        for i in range(3):
            t.forward(size)
            t.left(120)
    else:  # recursive step
        # draw first smaller one
        #   in lower-left (current position)
        sierpinski(t,size/2,depth-1)
        # move into position and draw
        #   2nd smaller one in lower-right
        t.forward(size/2)
        sierpinski(t,size/2,depth-1)
        # move into position and draw
        #   3rd smaller one on top
        t.left(120)
        t.forward(size/2)
        t.right(120)
        sierpinski(t,size/2,depth-1)
        # move back to starting position
        t.left(60)
        t.back(size/2)
        t.right(60)

colors = ['red', 'blue', 'green', 'yellow', 'pink', 'purple', 'brown']
#CircleBox(7, 7)
t = turtle.Turtle()
t.speed(0)
t.penup()
t.goto(-200,-310)
t.pendown()
sierpinski(t, 400, 5)
t.ht()

    