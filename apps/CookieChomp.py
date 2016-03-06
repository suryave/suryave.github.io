
import turtle

class Cookie(turtle.Turtle):
    '''represents a Chomp cookie'''

    def __init__(self,x,y,poison):
        '''Cookie(x,y,poison) -> Cookie
        creates a Cookie at (x,y)
        poison cookie if poison is True, regular otherwise'''
        # initialize a new turtle
        turtle.Turtle.__init__(self)
        # make it cookie-shaped
        self.shape('circle')
        self.width(20)
        # move into position
        self.speed(0)
        self.penup()
        self.goto(x,y)
        # non-poison cookies are brown
        if not poison:
            self.color('brown')

class ChompGame:
    '''represents a game of Chomp'''

    def __init__(self,width,height):
        '''ChompGame(width,height) -> ChompGame
        plays a game of Chomp on a width-by-height board'''
        # set up window
        self.window = turtle.Screen()
        self.window.title('Chomp')
        # set up game data
        self.gamewidth = width
        self.gameheight = height
        self.cookies = {}  # store the cookies
        for i in range(width):
            for j in range(height):
                self.cookies[(i,j)] = Cookie(40*i,40*j,i==0 and j==0)
        # set up turtle to write game messages
        self.messenger = turtle.Turtle()
        self.messenger.hideturtle()
        self.messenger.penup()
        self.messenger.goto(0,-100)
        # set up player
        self.player = 1
        self.print_player()
        # start the game
        self.window.onclick(self.chomp)  # listen for clicks
        self.window.listen()
        self.window.mainloop()

    def print_player(self):
        '''ChompGame.print_player()
        print the current player's turn information'''
        self.messenger.clear()
        self.messenger.write("Player "+str(self.player)+"'s turn",
                             font=("Arial",36,"normal"))

    def chomp(self,x,y):
        '''ChompGame.chomp(x,y)
        listener for mouse clicks'''
        # get the cookie that was just clicked on
        x = round(x/40)
        y = round(y/40)
        # make sure it's a valid click
        if (0 <= x < self.gamewidth) and (0 <= y < self.gameheight) \
           and self.cookies[(x,y)].isvisible():
            # remove all cookies above and/or to the right
            for i in range(x,self.gamewidth):
                for j in range(y,self.gameheight):
                    self.cookies[(i,j)].hideturtle()
            # check for the poison cookie
            if x+y == 0:
                print("Player "+str(self.player)+" loses!")
                self.window.bye()
                return
            # go to the other player
            self.player = 3 - self.player
            self.print_player()
ChompGame(7, 7)
