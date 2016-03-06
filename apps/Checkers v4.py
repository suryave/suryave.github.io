from tkinter import*
import random
import time

class CheckerTile(Canvas):
    '''represents a checker tile'''
    def __init__(self, master, x, y, color, Checker, checkercolor = ''):
        '''CheckerTile(master) -> CheckerTile
        creates a checker tile to be placed on the initial grid'''
        Canvas.__init__(self, master, width = 60, height = 60, bg = color)
        self.checker = Checker #whether or not a checker is present
        self.color = color# backgroundcolor
        # tell the tile its location
        self.x = x
        self.y = y
        self.disabled = False # if the cell can be clicked on
        self.king = False # king checker
        self.checkerColor = checkercolor # color of the checker, if present
        if not self.checker:
            self.checkerColor = '' #this cleans up the incorrect assignment in the master class
        if self.x != 8 and self.y != 8: #within the grid
            # listener
            self.bind('<Button-1>', self.clicked)
        if self.checker:
            self.draw(checkercolor)

    def draw(self, color):
        '''CheckerTile.draw(color)
        draws a checker with the appropriate color'''
        self.checkerColor = color
        # draw the checker
        (centerx, centery) = (30, 30)
        self.create_oval(centerx-20, centery-20, centerx+20, centery+20, fill = color)

    def draw_king(self):
        '''CheckerTile.draw_king()
        draws the * to signify a king'''
        self.create_text(30, 38, text = '*', font = ('Arial', 30))

    def erase(self):
        '''CheckerTile.erase()
        erases the checker'''
        self.checker = False
        self.checkerColor = ''
        self.delete("all")

    def clicked(self, event):
        '''CheckerTile.clicked(event)
        handler function for a click'''
        #tell the master function
        if not self.disabled:
            self.master.clicked_on(self.x, self.y)

class CheckerGrid(Frame):
    '''Checker GRid object'''
    def __init__(self, master, cpu, cpucolor):
        '''CheckerGrid(master)
        creates the default checkers grid'''
        #new Frame
        Frame.__init__(self, master)
        self.grid()
        # color lists for the background and checkers themelves
        self.colorList = ['beige', 'green'] # background
        self.checkerList = ['white', 'red'] # checkers
        # set up optional cpu option
        self.cpu = cpu # whether or not a cpu is playing
        # set cpu color (optional for user)
        for i in range(2):
            if cpucolor != self.checkerList[i]:
                self.cpuColor = self.checkerList[i]
        # create the tiles
        self.cells = [[0 for x in range(8)] for x in range(8)]
        self.checkerColorList = ['red', 'red', 'red', '', '', 'white' ,'white', 'white']
        for i in range (8):
            for j in range (8):
                self.cells[i][j] = CheckerTile(self, i, j, self.colorList[(i + j) % 2], (i != 4 and i != 3 and (i + j) % 2 == 1), self.checkerColorList[i])
                self.cells[i][j].grid(row = i, column = j)
                self.cells[i][j]['highlightbackground'] = self.cells[i][j].color
        # create the tiles designating the turn
        self.turnTileList = []
        for i in range(2):
            self.turnTileList.append(CheckerTile(self, 8, 0, 'gray', True, self.checkerList[i]))
        self.turnTileList[0].grid(row = 8, column = 1)
        self.turnTileList[0]['highlightbackground'] = 'blue'
        self.turnTileList[1]['highlightbackground'] = 'blue'
        self.turn = 0 # turn (0 = white, 1 = red)
        self.turnLabel = Label(self, text = 'Turn:', font = ('Arial', 18))
        self.turnLabel.grid(row = 8, column = 0)
        self.pieceCount = [12, 12] # pieces ([red, white])
        self.jumpInProgress = False # designates whether or not a player is in the middle of a turn
        self.jumpx = 8 # first click.x
        self.jumpy = 8 # first click.y
        self.reset_options() 
        self.doubleJump = False # if a second jump is possible
        self.jumpOption = False # if the player can jump
        self.gameOver = False # whether or not the game has ended
        # if the user chose for cpu and chose their color to be white, cpu takes the first turn
        if self.cpu and self.cpuColor == self.checkerList[self.turn]:
            self.after(500, self.cpu_turn)                           
        
    def clicked_on(self, x, y):
        '''CheckerGtid.clicked_on(x, y)
        performs the necessary action on a click on position (x, y). (Any click)'''
        if not self.jumpInProgress: # the player has just started their turn
            # if the player can jump, they MUST jump
            if self.jumpOption and self.cells[x][y].checkerColor == self.checkerList[self.turn]:
                self.check_for_double_jump(x, y) # checks if the click can lead to a jump
                if self.doubleJump: 
                    self.cells[x][y]['highlightbackground'] = 'blue'
                    self.jumpInProgress = True
                    self.jumpx = x
                    self.jumpy = y
            # the player cannot jump
            elif self.cells[x][y].checker and self.cells[x][y].checkerColor == self.checkerList[self.turn] and self.options(x, y) > 0:
                self.cells[x][y]['highlightbackground'] = 'blue'
                self.jumpInProgress = True
                self.jumpx = x
                self.jumpy = y
        else: # a jump is in progress
            # if the user selected the same cell, which deselects the cell
            if self.jumpx == x and self.jumpy == y and (not self.doubleJump or self.jumpOption):
                self.jumpx = 8
                self.jumpy = 8
                self.jumpInProgress = False
                self.reset_background()
                self.reset_options()
            else: # the user attempted to finish/continue their turn
                if not self.doubleJump: # jump not possible
                    # check if the user's choice is legal
                    for i in range(self.firstJumpCount):
                        if x == self.firstJumpList[i][0] and y == self.firstJumpList[i][1]:
                            self.update(x, y) # move the cell
                            self.check_for_king(x, y) # check to see if a king status is achieved
                            self.end_turn() #end the turn
                            break
                for i in range(self.secondJumpCount): # jump
                    # check for legal choice
                    if x == self.secondJumpList[i][0] and y == self.secondJumpList[i][1]:
                        # erase the checker jumped over and subtract from the counter
                        self.cells[int((x + self.jumpx)/2)][int((y+self.jumpy)/2)].erase()
                        self.pieceCount[1-self.turn] -= 1
                        self.check_for_loss() # check if the other player lost
                        self.update(x, y) # make the jump
                        self.check_for_king(x, y) #check for king status
                        if not self.kinged: 
                            self.check_for_double_jump(x, y)
                        if self.kinged or not self.doubleJump: # a king or no continuation ends the turn
                            self.end_turn()
                        break

    def cpu_turn(self):
        '''CheckerGrid.cpu_turn()
        The cpu takes a turn, if the user desired'''
        if self.jumpOption: # if the cpu can jump
            # check for all options
            optionList = []
            count = 0
            for i in range(8):
                for j in range(8):
                    if self.cells[i][j].checkerColor == self.checkerList[self.turn]:
                        self.check_for_double_jump(i, j)
                        if self.doubleJump:
                            optionList.append([i,j])
                            count += 1
            self.doubleJump = False
            # choose a random legal option
            choice = random.randint(0, count-1)
            self.reset_background()
            self.clicked_on(optionList[choice][0], optionList[choice][1])
            self.after(1000, self.cpu_finish_turn)
        else: #cpu cannot jump
            # list the options and choose a random one
            optionList = []
            count = 0
            for i in range(8):
                for j in range(8):
                    if self.cells[i][j].checkerColor == self.checkerList[self.turn]:
                        if self.options(i, j) > 0:
                            optionList.append([i, j])
                            count += 1
                        self.reset_options()
            if len(optionList) > 0:
                choice = random.randint(0, count - 1)
                self.reset_background()
                self.clicked_on(optionList[choice][0], optionList[choice][1])
                self.after(1000, self.cpu_finish_turn)
                
    def cpu_finish_turn(self):
        '''CheckerGrid.cpu_finish_turn()
        chooses where to land'''
        if self.jumpOption:
            # choose where to land
            landChoice = random.randint(0, self.secondJumpCount-1)
            x = self.secondJumpList[landChoice][0]
            y = self.secondJumpList[landChoice][1]
            self.clicked_on(self.secondJumpList[landChoice][0], self.secondJumpList[landChoice][1])
            while self.doubleJump: # keep taking turns if possible
                ignore = self.options(x, y)
                landChoice = random.randint(0, self.secondJumpCount-1)
                x = self.secondJumpList[landChoice][0]
                y = self.secondJumpList[landChoice][1]
                self.clicked_on(self.secondJumpList[landChoice][0], self.secondJumpList[landChoice][1])
        else:
            landChoice =  random.randint(0, self.firstJumpCount-1)
            self.clicked_on(self.firstJumpList[landChoice][0], self.firstJumpList[landChoice][1])
            

    def options(self, x, y):
        '''CheckersGrid.options(x, y)
        returns the number of moves possible from the given spot, and compiles the possibilities into lists.'''
        # list all adjacent diagonal squares for all moves
        self.nearbyList = [[x-1, y-1], [x-1, y+1], [x+1, y-1], [x+1, y+1]]
        self.nearbyJumpList = [[x-2, y-2], [x-2, y+2], [x+2, y-2], [x+2, y+2]]
        if not self.cells[x][y].king: # the checker is restricted to moving only up or down
            if self.cells[x][y].checkerColor == 'white': # can only move up
                up = 0
                down = 2
            elif self.cells[x][y].checkerColor == 'red': # can only move down
                up = 2
                down = 4
            else: # no checker on tile
                up = 0
                down = 0
        else: # the checker is free to move anywhere
            up = 0
            down = 4
        for i in range(up, down):
            # check list for any non-jump options (adjacent cell empty)
            if self.in_range(self.nearbyList[i][0], self.nearbyList[i][1]) and not self.cells[self.nearbyList[i][0]][self.nearbyList[i][1]].checker:
                self.cells[self.nearbyList[i][0]][self.nearbyList[i][1]]['highlightbackground'] = 'black'
                self.firstJumpCount += 1
                self.firstJumpList.append([self.nearbyList[i][0], self.nearbyList[i][1]])
            else: # check for any jump possibilities (adjacent cell full, but the second adjacent cell empty)
                if self.in_range(self.nearbyJumpList[i][0], self.nearbyJumpList[i][1]) and self.cells[self.nearbyList[i][0]][self.nearbyList[i][1]].checkerColor == self.checkerList[1 - self.turn] and not self.cells[self.nearbyJumpList[i][0]][self.nearbyJumpList[i][1]].checker:
                    self.cells[self.nearbyJumpList[i][0]][self.nearbyJumpList[i][1]]['highlightbackground'] = 'red'
                    self.secondJumpCount += 1
                    self.secondJumpList.append([self.nearbyJumpList[i][0], self.nearbyJumpList[i][1]])
        return self.firstJumpCount + self.secondJumpCount # return the total number of options

    def reset_options(self):
        '''CheckerGrid.reset_options()
        clears the options variables'''
        # clear the lists
        self.firstJumpList = []
        self.secondJumpList = []
        # reset the counts
        self.firstJumpCount = 0
        self.secondJumpCount = 0

    def update(self, x, y):
        '''CheckerGrid.update(x, y)
        swaps the old cell and the new cell
        a more efficient alternative than copying over all of each cell's attributes'''
        # remove the two cells to be swapped
        self.cells[x][y].grid_remove()
        self.cells[self.jumpx][self.jumpy].grid_remove()
        # swap the cells using a temp variable
        temp = self.cells[self.jumpx][self.jumpy]
        self.cells[self.jumpx][self.jumpy] = self.cells[x][y]
        self.cells[x][y] = temp
        # re-grid the two cells
        self.cells[x][y].grid(row = x, column = y)
        self.cells[self.jumpx][self.jumpy].grid(row = self.jumpx, column = self.jumpy)
        # tell the cells their new locations
        self.cells[x][y].x = x
        self.cells[x][y].y = y
        self.cells[self.jumpx][self.jumpy].x = self.jumpx
        self.cells[self.jumpx][self.jumpy].y = self.jumpy

    def check_for_double_jump(self, x, y):
        '''CheckerGrid.check_for_double_jump(x, y)
        check is a second jump is possible'''
        self.reset_background()
        self.reset_options()
        ignore = self.options(x, y)
        # only display double jump options
        for i in range(8):
            for j in range(8):
                if self.cells[i][j]['highlightbackground'] != 'red':
                    self.cells[i][j]['highlightbackground'] = self.cells[i][j].color
        if self.secondJumpCount > 0: # is a second jump is possible
            self.doubleJump = True
            self.jumpx = x
            self.jumpy = y
        else:
            self.doubleJump = False

    def check_all(self):
        '''CheckerGrid.check_all()
        checks if the player can jump or not'''
        for i in range(8):
            for j in range(8):
                if self.cells[i][j].checkerColor == self.checkerList[self.turn]:
                    ignore = self.options(i, j)
                    if self.secondJumpCount > 0: # a jump is possible
                        self.jumpOption = True
                        break
                self.reset_options()
        self.reset_background()

    def in_range(self, x, y):
        '''CheckerGrid.in_range(x, y)
        checks if a location is within the 8 by 8 checkers grid'''
        if x < 0 or y < 0 or x > 7 or y > 7:
            return False
        else:
            return True
                        
    def check_for_king(self, x, y):
        '''CheckerGrid.ckeck_for_king(x, y)
        determines if a piece has achieved kingly status'''
        self.kinged = False
        if not self.cells[x][y].king:
            num = -1
            # determines if the top or bottom of the grid needs to be reached
            if self.cells[x][y].checkerColor == 'red':
                num = 7
            elif self.cells[x][y].checkerColor == 'white':
                num = 0
            if x == num:
                self.cells[x][y].king = True
                self.cells[x][y].draw_king()
                self.kinged = True
                    
    def reset_background(self):
        '''CheckerGrid.reset_background()
        resets the backgroundhighlighted attribute to default'''
        for i in range(8):
            for j in range(8):
                self.cells[i][j]['highlightbackground'] = self.cells[i][j].color

    def end_turn(self):
        '''CheckerGrid.end_turn()
        concludes a player's turn'''
        # reset variables
        self.jumpInProgress = False
        self.doubleJump = False
        # change turn and display the appropriate turn tile
        self.turnTileList[self.turn].grid_remove()
        self.turn = 1 - self.turn
        self.turnTileList[self.turn].grid(row = 8, column = 1)
        # reset more variables
        self.reset_options()
        self.start = False
        self.jumpOption = False
        self.reset_background()
        self.check_all() # check is the next player can jump
        self.check_for_possible_moves() # check whether or not the player isn't blocked
        # cpu option
        if self.cpu and self.cpuColor == self.checkerList[self.turn]:
            self.after(1000, self.cpu_turn)

    def check_for_possible_moves(self):
        '''CheckerGrid.check_for_possible_moves()
        checks if a player can move'''
        self.reset_options()
        total = 0
        for i in range(8):
            for j in range(8):
                if self.cells[i][j].checkerColor == self.checkerList[self.turn]:
                    total += self.options(i, j)
                    self.reset_options()
        # if there are no possible moves, the game is over
        if total == 0: 
            self.game_over(self.turn)
        self.reset_background()

    def check_for_loss(self):
        '''CheckerGrid.check_for_loss()
        check if a player has run out of pieces'''
        for i in range(2):
            if self.pieceCount[i] == 0: # this player has no more checkers left
                self.game_over(i)

    def game_over(self, i):
        '''CheckerGrid.game_over(i)
        ends the game'''
        capitalCheckerList = ['White', 'Red']
        winnerText = capitalCheckerList[1-i] + ' ' + 'wins!'
        self.lossLabel = Label(self, text = winnerText, font = ('Arial', 18)).grid(row = 8, column = 6, columnspan = 6)
        for i in range(8):
            for j in range(8):
                self.cells[i][j].disabled = True # disable all cells

class StartGame(Frame):
    def __init__(self):
        self.cpuRoot = Tk()
        self.cpuRoot.title('CPU Option')
        Frame.__init__(self, self.cpuRoot, bg = 'white')
        self.grid()
        self.label = Label(self, text = 'Play against CPU?', font = ('Arial', 12), bg = 'white').grid(row = 0, column = 0, columnspan = 20)
        self.yesButton = Button(self, text = 'Yes', command = self.yes_pressed, bg = 'white').grid(row = 1, column = 9)
        self.noButton = Button(self, text = 'No', command = self.no_pressed, bg = 'white').grid(row = 1, column = 11)

    def yes_pressed(self):
        self.colorlabel = Label(self, text = 'Choose your color:', font = ('Arial', 12), bg = 'white').grid(row = 0, column = 0, columnspan = 20)
        self.redButton = Button(self, text = 'Red', command = self.red_pressed, bg = 'white').grid(row = 1, column = 9)
        self.whiteButton = Button(self, text = 'White', command = self.white_pressed, bg = 'white').grid(row = 1, column = 11)
        
    def white_pressed(self):
        self.cpuRoot.destroy()
        playCheckers(True, 'white')

    def red_pressed(self):
        self.cpuRoot.destroy()
        playCheckers(True, 'red')
        
    def no_pressed(self):
        self.cpuRoot.destroy()
        playCheckers(False)

def playCheckers(cpu, color = ''):
    root = Tk()
    root.title('Checkers by Kunal Adhia')
    game = CheckerGrid(root, cpu, color)
    game.mainloop()
    
StartGame()
