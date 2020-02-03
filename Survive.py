import module_manager
module_manager.review()
import random
from tkinter import *
from PIL import Image, ImageTk, ImageSequence, ImageOps
import pyaudio,sys,wave,threading
from mazeNode import *
from definitions import *


# code from https://stackoverflow.com/questions/6951046/pyaudio-help-play-a-file
# and https://stackoverflow.com/questions/2846653/how-to-use-threading-in-python
class PlayThread(threading.Thread):
    def __init__(self, file):
        super(PlayThread,self).__init__()
        self.file=file
    
    def run(self):
        CHUNK=1024
        wf=wave.open(self.file,'rb')
        p=pyaudio.PyAudio()
        stream=\
        p.open(format=p.get_format_from_width(wf.getsampwidth()),\
         channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
        data=wf.readframes(CHUNK)
        while len(data)>0:
            stream.write(data)
            data=wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()

def main(maze, start, end):
    path = astar(maze, start, end)
    return path

#class for user character
class Character(object):
    def __init__(self, cx, cy, maze, life, numsoda):
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.maze = maze
        self.maxBall = 1
        self.lives = life
        self.numSoda = numsoda
        
    def draw(self, canvas, icon):
        canvas.create_image(self.cx, self.cy, image=icon)
        
    def moveX(self, num):
        self.cx += num
    
    def moveY(self, num):
        self.cy += num
    
    def inreaseMaxBall(self):
        self.maxBall += 1
        return self.maxBall
        
    def loseLife(self):
        self.lives -= 1
        return self.lives
        
    def obtainRange(self):
        self.numSoda += 1
        return self.numSoda

#class for AI character which is being used in the second level
class AICharacter(object):
    #has the same features as user
    def __init__(self, cx, cy, maze, life, numsoda):
        self.cx = cx
        self.cy = cy
        self.r = 5
        self.colL = 90
        self.rowL = 85
        self.maze = maze
        self.maxBall = 1
        self.lives = life
        self.numSoda = numsoda
        
    def draw(self, canvas, icon):
        canvas.create_image(self.cx, self.cy, image=icon)
        
    def move(self, x, y):
        self.cx = x*self.colL+45
        self.cy = y*self.rowL+43.5
    
    def inreaseMaxBall(self):
        self.maxBall += 1
        return self.maxBall
        
    def loseLife(self):
        self.lives -= 1
        return self.lives
        
    def obtainRange(self):
        self.numSoda += 1
        return self.numSoda

#class for Monsters which are being used in the first level
class Monster(object):
    def __init__(self, chrcx, chrcy, maze, coord):
        self.chrcx = chrcx
        self.chrcy = chrcy
        self.maze = maze
        self.r = 5
        self.colL = 90
        self.rowL = 85
        self.coord = coord
        self.cx = self.coord[1]*self.colL+45
        self.cy = self.coord[0]*self.rowL+43.5
        
    def draw(self, canvas, icon):
        canvas.create_image(self.cx, self.cy, image=icon)
    
    def move(self, x, y):
        self.cx = x*self.colL+45
        self.cy = y*self.rowL+43.5
    
    #monster collision with other characters
    def collidesWithChar(self, other):
        if(not isinstance(other, Character)):
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r
    


#This class is being used when user or AI place balloon 
class Balloon(object):
    def __init__(self, cx, cy, speed, maze, numSoda):
        self.cx = cx
        self.cy = cy
        self.speed = speed
        self.r = 24
        self.timer = 3
        self.count = 6
        self.maze = maze
        self.colL = 90
        self.rowL = 85
        self.obtainSoda = numSoda

    def draw(self, canvas, icon):
        coorX = (self.cx//self.colL)*self.colL+self.colL//2
        coorY = (self.cy//self.rowL)*self.rowL+self.rowL//2
        canvas.create_image(coorX, coorY, image=icon)

    #This function destroys the boxes nearby waterballoon if it hits them
    def reactToBlock(self, coordinate):
        coorX = coordinate[0]//self.colL
        coorY = coordinate[1]//self.rowL
        indexBlock = "456789"
        if self.obtainSoda == 0:
            if coorX+1 < 13:
                if str(self.maze[coorY][coorX+1]) in indexBlock:
                    self.maze[coorY][coorX+1] = 0
            if coorX-1 > -1:
                if str(self.maze[coorY][coorX-1]) in indexBlock:
                    self.maze[coorY][coorX-1] = 0
            if coorY-1 > -1:
                if str(self.maze[coorY-1][coorX]) in indexBlock:
                    self.maze[coorY-1][coorX] = 0
            if coorY+1 < 8:
                if str(self.maze[coorY+1][coorX]) in indexBlock:
                    self.maze[coorY+1][coorX] = 0
        elif self.obtainSoda == 1:
            if coorX+1 < 13:
                if str(self.maze[coorY][coorX+1]) in indexBlock:
                    self.maze[coorY][coorX+1] = 0
                elif coorX+2 < 13:
                    if str(self.maze[coorY][coorX+2]) in indexBlock:
                        self.maze[coorY][coorX+2] = 0
            if coorX-1 > -1:
                if str(self.maze[coorY][coorX-1]) in indexBlock:
                    self.maze[coorY][coorX-1] = 0
                elif coorX-2 > -1:
                    if str(self.maze[coorY][coorX-2]) in indexBlock:
                        self.maze[coorY][coorX-2] = 0
            if coorY-1 > -1:
                if str(self.maze[coorY-1][coorX]) in indexBlock:
                    self.maze[coorY-1][coorX] = 0
                elif coorY-2 > -1:
                    if str(self.maze[coorY-2][coorX]) in indexBlock:
                        self.maze[coorY-2][coorX] = 0
            if coorY+1 < 8:
                if str(self.maze[coorY+1][coorX]) in indexBlock:
                    self.maze[coorY+1][coorX] = 0
                elif coorY+2 < 8:
                    if str(self.maze[coorY+2][coorX]) in indexBlock:
                        self.maze[coorY+2][coorX] = 0
        elif self.obtainSoda == 2:
            if coorX+1 < 13:
                if str(self.maze[coorY][coorX+1]) in indexBlock:
                    self.maze[coorY][coorX+1] = 0
                elif coorX+2 < 13:
                    if str(self.maze[coorY][coorX+2]) in indexBlock:
                        self.maze[coorY][coorX+2] = 0
                elif coorX+3 < 13:
                    if str(self.maze[coorY][coorX+3]) in indexBlock:
                        self.maze[coorY][coorX+3] = 0
            if coorX-1 > -1:
                if str(self.maze[coorY][coorX-1]) in indexBlock:
                    self.maze[coorY][coorX-1] = 0
                elif coorX-2 > -1:
                    if str(self.maze[coorY][coorX-2]) in indexBlock:
                        self.maze[coorY][coorX-2] = 0
                elif coorX-3 > -1:
                    if str(self.maze[coorY][coorX-3]) in indexBlock:
                        self.maze[coorY][coorX-3] = 0
            if coorY-1 > -1:
                if str(self.maze[coorY-1][coorX]) in indexBlock:
                    self.maze[coorY-1][coorX] = 0
                elif coorY-2 > -1:
                    if str(self.maze[coorY-2][coorX]) in indexBlock:
                        self.maze[coorY-2][coorX] = 0
                elif coorY-3 > -1:
                    if str(self.maze[coorY-3][coorX]) in indexBlock:
                        self.maze[coorY-3][coorX] = 0
            if coorY+1 < 8:
                if str(self.maze[coorY+1][coorX]) in indexBlock:
                    self.maze[coorY+1][coorX] = 0
                elif coorY+2 < 8:
                    if str(self.maze[coorY+2][coorX]) in indexBlock:
                        self.maze[coorY+2][coorX] = 0
                elif coorY+3 < 8:
                    if str(self.maze[coorY+3][coorX]) in indexBlock:
                        self.maze[coorY+3][coorX] = 0
        return self.maze
    

#This class is being used for waterballoon item
class waterBalloon(object): 
    def __init__(self, maze, coord):
        self.maze = maze
        self.col = 13
        self.row = 8
        self.width = 1172
        self.height = 680
        self.colL = 90.5
        self.rowL = 85
        self.r = 5
        self.cx = coord[1]*self.colL+45
        self.cy = coord[0]*self.rowL+43.5

    def draw(self,canvas, icon):
        canvas.create_image(self.cx, self.cy, image=icon)
        
    def collidesWithChar(self,other):
        if(not isinstance(other, Character)):
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r
    
    def collidesWithCharAI(self,other):
        if(not isinstance(other, AICharacter)):
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r

#This class is being used for soda item
class Soda(object):
    def __init__(self, maze, coordinate):
        self.maze = maze
        self.col = 13
        self.row = 8
        self.width = 1172
        self.height = 680
        self.colL = 90.5
        self.rowL = 85
        self.possibleLoc = coordinate
        self.index = random.randint(0,len(self.possibleLoc)-1)
        self.r = 5
        coord = self.possibleLoc[self.index]
        self.cx = coord[1]*self.colL+45
        self.cy = coord[0]*self.rowL+43.5

    def draw(self,canvas, icon):
        canvas.create_image(self.cx, self.cy, image=icon)
        
    def collidesWithChar(self,other):
        if(not isinstance(other, Character)):
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r

    def collidesWithCharAI(self,other):
        if(not isinstance(other, AICharacter)):
            return False
        else:
            dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
            return dist < self.r + other.r
            
#This class forms map of the game
class Map(object):
    def __init__(self,maze):
            self.col = 13
            self.row = 8
            self.width = 1180
            self.height = 650
            self.colL = 90.5
            self.rowL = 85
            self.maze = maze

    def draw(self, canvas, icon):
        for i in range(self.row):
            for j in range(self.col):
                if self.maze[i][j] == 3:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+23, image=icon[6])
                if self.maze[i][j] == 4:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[0])
                if self.maze[i][j] == 5:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[1])
                if self.maze[i][j] == 6:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[2])
                if self.maze[i][j] == 7:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[3])
                if self.maze[i][j] == 8:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[4])
                if self.maze[i][j] == 9:
                    canvas.create_image(self.colL*j+45, \
                    self.rowL*i+43.5, image=icon[5])



def init(data):
    data.isGameOver = True
    data.startGame = False
    data.instruction = False
    data.showLives = False
    data.levelOneFinish = False
    data.levelInfo = False
    data.levelTwo = False
    data.searchingState = False
    data.huntingState = False
    data.end = False
    data.showAI = True
    
    data.levelTwoMaze = [\
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,4,0,7,0,7,0,8,0,6,0,6,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,5,0,5,0,6,0,7,0,5,0,7,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,6,0,6,0,5,0,6,0,4,0,8,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,7,0,8,0,4,0,5,0,6,0,9,0]]
   
    data.maze = [\
    [0,0,5,8,9,0,0,0,9,8,7,0,0],
    [0,0,7,8,0,0,4,0,0,6,6,0,7],
    [3,5,6,0,0,4,7,4,0,0,9,8,3],
    [5,0,0,0,4,8,3,6,4,0,0,0,7],
    [3,5,6,0,0,4,5,4,0,0,7,8,3],
    [5,9,7,6,0,0,4,0,0,0,6,9,7],
    [0,0,8,7,9,0,0,0,7,8,8,0,0],
    [0,0,6,7,9,0,0,0,9,6,3,0,0]]
  
    data.itemLoc = [\
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]]
  
    data.map = Map(data.maze)
    data.cx = 45
    data.cy = 43
    data.difficulty = 1
    data.colL = 90
    data.rowL = 85
    data.width = 1172
    data.height = 680
    data.numSoda = 0
    data.count = 0
    data.character = Character(data.cx, data.cy, data.maze, 3, data.numSoda)
    
    #Init for AI character
    data.AInumSoda = 0
    data.AIcx = 1127
    data.AIcy = 637
    data.AIcount = 0
    data.AICharacter = []
    data.AICharacterLives = 3
    data.AIballoons = []
    data.balloons = []
    

    data.seconds = 5
    data.levelOneCount = 3
    data.countLives = 30
    data.tempLevelOneFinish = 1
    data.coordinate = getCoordinateBlock(data.maze, 8, 13)
    data.wBall = []
    data.soda = []
    #items being placed 
    for i in range(4):
        index = random.randint(0,len(data.coordinate)-1)
        coord = data.coordinate[index]
        if data.itemLoc[coord[0]][coord[1]] != 2:
            data.wBall.append(waterBalloon(data.maze, coord))
        data.itemLoc[coord[0]][coord[1]] = 2
    for i in range(3):
        index = random.randint(0,len(data.coordinate)-1)
        coord = data.coordinate[index]
        if data.itemLoc[coord[0]][coord[1]] != 2:
            data.soda.append(Soda(data.maze, data.coordinate))
        data.itemLoc[coord[0]][coord[1]] = 2
        
    
    #Init for monsters
    data.mazeEnemies = [\
    [5,5,5,8,9,0,0,0,9,8,7,5,5],
    [5,5,7,8,0,0,4,0,0,6,6,5,7],
    [3,5,6,0,0,4,7,4,0,0,9,8,3],
    [5,0,0,0,4,8,3,6,4,0,0,0,7],
    [3,5,6,0,0,4,5,4,0,0,7,8,3],
    [5,9,7,6,0,0,4,0,0,0,6,9,7],
    [5,5,8,7,9,0,0,0,7,8,8,5,5],
    [5,5,6,7,9,0,0,0,9,6,3,5,5]]
    data.monster = []
    data.spawnIndex = getCoordinateNotBlock(data.mazeEnemies, 8, 13)
    for i in range(2):
        monsterCount = 0
        index = random.randint(0,len(data.spawnIndex)-1)
        data.monsterIndex = data.spawnIndex[index]
        data.spawnIndex.pop(index)        
        monsterCy = data.monsterIndex[0]
        monsterCx = data.monsterIndex[1]
        start = (data.monsterIndex[0], data.monsterIndex[1])
        end = (data.cy//85, data.cx//90)
        monsterCoord = main(data.maze, start, end)
        data.monster.append(\
        [Monster(data.cx, data.cy, data.maze, data.monsterIndex),\
         monsterCy, monsterCx, monsterCoord, monsterCount])
        data.visited = []
    
    #images from http://bnb.sdo.com/web5/daoju/daoju_1.asp?CategoryID=2993
    data.bazziFront = PhotoImage(file="Image/BazziFront.png")
    data.bazziBack = PhotoImage(file='Image/BazziBack.png')
    data.bazziRight = PhotoImage(file='Image/BazziRight.png')
    data.bazziLeft = PhotoImage(file='Image/BazziLeft.png')
    data.waterbaloonRed = PhotoImage(file='Image/waterbaloonRed.png')
    data.balloonUp = PhotoImage(file='Image/balloonUp.png')
    data.balloonDown = PhotoImage(file='Image/balloonDown.png')
    data.balloonImagelst = [data.balloonUp, data.balloonDown]
    data.background = PhotoImage(file='Image/background.png')
    data.wBallImage = PhotoImage(file='Image/waterBall.png')
    data.singleWater = PhotoImage(file='Image/singleWater.png')
    data.doubleWater = PhotoImage(file='Image/doubleWater.png')
    data.directionCharacter = data.bazziFront
    data.monsterImage = PhotoImage(file='Image/monster.png')
    data.sodaImage = PhotoImage(file='Image/soda.png')
    data.AIfront = PhotoImage(file='Image/AIfront.png')
    data.AIright = PhotoImage(file='Image/AIright.png')
    data.AIback = PhotoImage(file='Image/AIback.png')
    data.AIleft = PhotoImage(file='Image/AIleft.png')
    data.AIimageState = None
    
    
    #images from nexon.com
    data.box = PhotoImage(file='Image/Box.png')
    data.blockR = PhotoImage(file='Image/blockR.png')
    data.blockM = PhotoImage(file='Image/blockM.png')
    data.blockX = PhotoImage(file='Image/blockX.png')
    data.blockY = PhotoImage(file='Image/blockY.png')
    data.greenBox = PhotoImage(file='Image/greenBox.png')
    data.snowman = PhotoImage(file='Image/snowman.png')
    data.blocks = [data.box, data.blockR, data.blockM, \
    data.blockX, data.blockY, data.greenBox, data.snowman]
    
    #images from google.com
    data.loseScreen = PhotoImage(file='Image/loseScreen.png')
    data.livestate = PhotoImage(file='Image/livestate.png')
    data.startGameScreen = PhotoImage(file='Image/startGameScreen.png')
    data.instructionScreen = PhotoImage(file='Image/instructionScreen.png')
    data.levelOneFinishScreen = \
    PhotoImage(file='Image/levelOneFinishScreen.png')
    data.levelScreen = PhotoImage(file='Image/levelScreen.png')
    data.blackScreen = PhotoImage(file='Image/blackScreen.png')
    data.winScreen = PhotoImage(file='Image/WinScreen.png')
    

#User can start game, see what level they are on abd instruction using mouse
def mousePressed(event, data):
    if data.startGame == False:
        if 264 < event.x < 565 and 535 < event.y < 617:
            data.startGame = True
            data.levelInfo = True
            data.isGameOver = False
        elif 606 < event.x < 907 and 536 < event.y < 618:
            data.instruction = True
    if data.instruction == True:
        if 513 < event.x < 670 and 481 < event.y < 535:
            data.instruction = False
    if data.isGameOver == True:
        if 381 < event.x < 791 and 583 < event.y < 654:
            init(data)
    if data.end == True:
        if 370 < event.x < 735 and 527 < event.y < 623:
            init(data)
        
#character can move around with directional keyboard
def keyPressed(event, data):
    if data.isGameOver == False:
        if event.keysym == "Right":
            data.directionCharacter = data.bazziRight
            moveChar(data,90,0)
        elif event.keysym == "Left":
            data.directionCharacter = data.bazziLeft
            moveChar(data,-90,0)
        elif event.keysym == "Up":
            data.directionCharacter = data.bazziBack
            moveChar(data,0,-85)
        elif event.keysym == "Down":
            data.directionCharacter = data.bazziFront
            moveChar(data,0,85)
        elif event.keysym == "space":
            if len(data.balloons) < data.character.maxBall:
                data.balloons.append(\
                Balloon(data.cx, data.cy, 5, data.maze, data.numSoda))


def timerFired(data):
    data.timerDelay = 50
    if data.isGameOver == False:
        data.map = Map(data.maze)
        data.count += 1
        if len(data.balloons) > 0:  
        #interactions between user's balloon to other things
            for balloon in data.balloons:
                if balloon.cx//data.colL != data.character.cx//data.colL and\
                 balloon.cy//data.rowL != data.character.cy//data.rowL:
                    data.maze[balloon.cy//data.rowL][balloon.cx//data.colL] = 1
                if data.count % 3 == 0:
                    balloon.count -= 1
                if data.count % 6 == 0:
                    balloon.timer -= 1
                if balloon.timer == 0:
                    data.balloons.remove(balloon)
                    data.maze = balloon.reactToBlock([balloon.cx, balloon.cy])
                    data.maze[balloon.cy//data.rowL][balloon.cx//data.colL] = 0
                    for monster in data.monster:
                        if reactToBalloon(\
                        [balloon.cx//data.colL, balloon.cy//data.rowL],\
                         [monster[2],monster[1]], data.numSoda, data.maze)\
                          == True:
                            data.monster.remove(monster)
                    #characters are respawned if they get hit by the balloon
                    if reactToBalloon(\
                    [balloon.cx//data.colL, balloon.cy//data.rowL],\
                    [data.character.cx//data.colL, \
                    data.character.cy//data.rowL], data.numSoda, data.maze) \
                    == True:
                        data.character.loseLife()
                        data.cx = 45
                        data.cy = 43
                        data.showLives = True
                        data.numSoda = 0
                        data.character = \
                        Character(data.cx, data.cy, data.maze, \
                        data.character.lives,data.numSoda)
                        if data.character.lives == 0:
                            data.isGameOver = True
                    if data.levelTwo == True:
                        if reactToBalloon(\
                        [balloon.cx//data.colL, balloon.cy//data.rowL], [data.AICharacter[0].cx//data.colL, data.AICharacter[0].cy//data.rowL], \
                        data.AInumSoda, data.maze) == True:
                            data.AIcx = 1127
                            data.AIcy = 637
                            data.AICharacterLives -= 1
                            data.AICharacter = \
                            [AICharacter(data.AIcx, data.AIcy, data.maze, \
                            data.AICharacterLives, data.AInumSoda), \
                            data.AIcy//85, data.AIcx//90, data.AImaze, \
                            data.AIcount]
                            if data.AICharacterLives == 0:
                                data.end = True
                                data.showAI = False
                            
        if len(data.AIballoons) > 0:
            #interactions between AI's balloons and other things
            for balloon in data.AIballoons:
                if balloon.cx//data.colL != data.character.cx//data.colL and\
                 balloon.cy//data.rowL != data.character.cy//data.rowL:
                    data.maze[balloon.cy//data.rowL][balloon.cx//data.colL] = 1
                if data.count % 6 == 0:
                    balloon.timer -= 1
                #when timer expiers, ballon explodes and either break or kill
                #nearby things
                if balloon.timer == 0:
                    data.AIballoons.remove(balloon)
                    data.maze = balloon.reactToBlock([balloon.cx, balloon.cy])
                    data.maze[balloon.cy//data.rowL][balloon.cx//data.colL] = 0
                    if reactToBalloon(\
                    [balloon.cx//data.colL, balloon.cy//data.rowL], \
                    [data.character.cx//data.colL, \
                    data.character.cy//data.rowL], data.numSoda, data.maze) \
                    == True:
                        data.character.loseLife()
                        data.cx = 45
                        data.cy = 43
                        data.showLives = True
                        data.character = \
                        Character(data.cx, data.cy, data.maze, \
                        data.character.lives,data.numSoda)
                        #game is over when character loses all of its lives
                        if data.character.lives == 0:
                            data.isGameOver = True
                    #These lines are only relevent when user is on second level
                    if data.levelTwo == True:
                        if reactToBalloon(\
                        [balloon.cx//data.colL, balloon.cy//data.rowL], [data.AICharacter[0].cx//data.colL, data.AICharacter[0].cy//data.rowL], \
                        data.AInumSoda, data.maze) == True:
                            data.AIcx = 1127
                            data.AIcy = 637
                            data.AICharacterLives -= 1
                            data.AICharacter = \
                            [AICharacter(data.AIcx, data.AIcy, data.maze, \
                            data.AICharacterLives, data.AInumSoda), \
                            data.AIcy//85, data.AIcx//90, data.AImaze, \
                            data.AIcount]
                            if data.AICharacterLives == 0:
                                data.end = True
                                data.showAI = False
        #for each waterballoon item...
        for wBall in data.wBall:
            if wBall.collidesWithChar(data.character):
                data.wBall.remove(wBall)
                data.character.inreaseMaxBall()
            if data.levelTwo == True:    
                if wBall.collidesWithChar(data.AICharacter[0]):
                    data.wBall.remove(wBall)
                    data.AICharacter[0].inreaseMaxBall()

        #for each soda item...
        for soda in data.soda:
            if soda.collidesWithChar(data.character):
                data.soda.remove(soda)
                data.numSoda += 1
            if data.levelTwo == True:
                if soda.collidesWithChar(data.AICharacter[0]):
                    data.soda.remove(soda)
                    data.AInumSoda += 1

        #monster moves to index that was obtained from main function 
        #every mod 2 of data.count
        if data.count % 2 == 0:
            for monster in data.monster:
                if monster[3] != None:
                    (monster_cy, monster_cx) = monster[3][monster[4]]
                    monster[0].move(monster_cx, monster_cy)
                    monster[2] = monster_cx
                    monster[1] = monster_cy
                    if monster[4] < (len(monster[3])-1):
                        monster[4] += 1

        #moster's path is being updated every mod 3 of data.count
        if data.count % 3 == 0:
            for monster in data.monster:
                start = (monster[1], monster[2])
                end = (data.cy//85, data.cx//90)
                monster[3] = main(data.maze, start, end)
                monster[4] = 0
                if monster[3] == None:
                    start = (monster[1], monster[2])
                    possible = getCoordinateNotBlock(data.mazeEnemies, 8, 13)
                    index = random.randint(0,len(possible)-1)
                    end = (possible[index][0], possible[index][1])
                    monster[3] = main(data.maze, start, end)
        
        #if monster collides with the user, user loses life
        for monster in data.monster:
            if monster[0].collidesWithChar(data.character):
                data.character.loseLife()
                data.cx = 45
                data.cy = 43
                data.showLives = True
                data.character = \
                Character(data.cx, data.cy, data.maze, data.character.lives,\
                data.numSoda)
                if data.character.lives == 0:
                    data.isGameOver = True
                    
        
        if data.showLives == True:
            data.countLives -= 5
            if data.countLives == 0:
                data.showLives = False
                data.countLives = 30
        
        if data.tempLevelOneFinish == 1:    
            if len(data.monster) == 0:
                data.levelOneFinish = True
                data.tempLevelOneFinish = 0
        
        #when level 2 begins, all of the init that are being used in level 2 
        #are being reset with additional features added to it
        if data.levelOneFinish == True:
            if (data.count % 3 == 0):
                data.levelOneCount -= 1
                if (data.levelOneCount == 0):
                    data.levelTwo = True
                    data.isGameOver = False
                    data.levelOneFinish = False
                    data.maze = data.levelTwoMaze
                    data.difficulty += 1
                    data.levelInfo = True
                    data.seconds = 5
                    data.coordinate = getCoordinateBlock(data.maze, 8, 13)
                    data.wBall = []
                    data.soda = []
                    data.itemLoc = [\
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0]]
                    for i in range(4):
                        index = random.randint(0,len(data.coordinate)-1)
                        coord = data.coordinate[index]
                        if data.itemLoc[coord[0]][coord[1]] != 2:
                            data.wBall.append(waterBalloon(data.maze, coord))
                        data.itemLoc[coord[0]][coord[1]] = 2
                    for i in range(3):
                        index = random.randint(0,len(data.coordinate)-1)
                        coord = data.coordinate[index]
                        if data.itemLoc[coord[0]][coord[1]] != 2:
                            data.soda.append(Soda(data.maze, data.coordinate))
                        data.itemLoc[coord[0]][coord[1]] = 2
                    data.cx = 45
                    data.cy = 43
                    data.showLives = True
                    data.numSoda = 0
                    data.count = 0
                    data.character = \
                    Character(data.cx, data.cy, data.maze, \
                    data.character.lives,data.numSoda)
                    location = findNearestBox(data.AIcy//data.rowL, \
                    data.AIcx//data.colL, data.maze)
                    if location != None:
                        start = (data.AIcy//data.rowL, data.AIcx//data.colL)
                        end = (location[0]-1, location[1])
                        data.AImaze = main(data.maze, start, end)
                    else:
                        start = (data.AIcy//data.rowL, data.AIcx//data.colL)
                        possible = getCoordinateNotBlock(data.maze, 8, 13)
                        index = random.randint(0,len(possible)-1)
                        end = (possible[index][0], possible[index][1])
                        data.AImaze = main(data.maze, start, end)
                    data.AICharacter = [AICharacter(data.AIcx, data.AIcy, \
                    data.maze, data.AICharacterLives, data.AInumSoda), \
                    data.AIcy//85, data.AIcx//90, data.AImaze, data.AIcount]
                    data.levelOneFinish == False
 
        #If user is far away from AI, AI tries to find nearest box and 
        #obtain item
        if data.levelTwo == True:
            if data.count % 15 == 0:
                if abs((data.character.cx//data.colL) - \
                (data.AICharacter[0].cx//data.colL)) >= 1 and \
                abs((data.character.cy//data.rowL) - \
                (data.AICharacter[0].cy//data.rowL)) >= 1 and \
                boxAvailable(data.maze) != 0:
                    data.searchingState = True
                    data.huntingState = False
                    location = findNearestBox(\
                    int(data.AICharacter[0].cy//data.rowL), \
                    data.AICharacter[0].cx//data.colL, data.maze)
                    if location != None and location not in data.visited:
                        data.visited.append(location)
                        start = (data.AICharacter[1], data.AICharacter[2])
                        end = (location[0]-1, location[1])
                        data.AICharacter[3] = main(data.maze, start, end)
                        data.AICharacter[4] = 0
                    else:
                        start = (data.AICharacter[1], data.AICharacter[2])
                        possible = getCoordinateNotBlock(data.maze, 8, 13)
                        index = random.randint(0,len(possible)-1)
                        end = (possible[index][0], possible[index][1])
                        data.AICharacter[3] = main(data.maze, start, end)
                        data.AICharacter[4] = 0
                #if not, then AI goes toward the user and tries to kill him/her
                else:
                    data.huntingState = True
                    data.searchingState = False
                    start = (data.AICharacter[1], data.AICharacter[2])
                    end = (data.character.cy//85, data.character.cx//90)
                    data.AICharacter[3] = main(data.maze, start, end)
                    data.AICharacter[4] = 0
            
        #depending on what state AI is, AI moves either aggressively or 
        #carefully
        if data.levelTwo == True:
            if data.count % 2 == 0:
                if data.searchingState == True:
                    if data.AICharacter[3] != None:
                        (AI_cy, AI_cx) = \
                        data.AICharacter[3][data.AICharacter[4]]
                        data.AICharacter[0].move(AI_cx, AI_cy)
                        if AI_cx == data.AICharacter[2] and \
                        AI_cy < data.AICharacter[1]:
                            data.AIimageState = data.AIback
                        elif AI_cx > data.AICharacter[2] and \
                        AI_cy == data.AICharacter[1]:
                            data.AIimageState = data.AIright
                        elif AI_cx < data.AICharacter[2] and \
                        AI_cy == data.AICharacter[1]:
                            data.AIimageState = data.AIleft
                        else:
                            data.AIimageState = data.AIfront
                        data.AICharacter[2] = AI_cx
                        data.AICharacter[1] = AI_cy
                        if data.AICharacter[4] < (len(data.AICharacter[3])-1):
                            data.AICharacter[4] += 1
                        if data.AICharacter[4] == (len(data.AICharacter[3])-1):
                            if len(data.AIballoons)<data.AICharacter[0].maxBall:
                                if data.count % 3:
                                    data.AIballoons.append(\
                                    Balloon(data.AICharacter[2]*data.colL, data.AICharacter[1]*data.rowL, 5, data.maze, data.AInumSoda))
                                    start = (data.AICharacter[1], \
                                    data.AICharacter[2])
                                    coord = farFromPlayer(\
                                    data.character.cx//data.colL, \
                                    data.character.cy//data.rowL)
                                    end = (coord[1], coord[0])
                                    data.AICharacter[3] = main(\
                                    data.maze, start, end)
                                    data.AICharacter[4] = 0
                elif data.huntingState == True:
                    (AI_cy, AI_cx) = data.AICharacter[3][data.AICharacter[4]]
                    data.AICharacter[0].move(AI_cx, AI_cy)
                    if AI_cx == data.AICharacter[2] and AI_cy < \
                    data.AICharacter[1]:
                        data.AIimageState = data.AIback
                    elif AI_cx > data.AICharacter[2] and AI_cy == \
                    data.AICharacter[1]:
                        data.AIimageState = data.AIright
                    elif AI_cx < data.AICharacter[2] and AI_cy == \
                    data.AICharacter[1]:
                        data.AIimageState = data.AIleft
                    else:
                        data.AIimageState = data.AIfront
                    data.AICharacter[2] = AI_cx
                    data.AICharacter[1] = AI_cy
                    if data.AICharacter[4] < (len(data.AICharacter[3])-1):
                        data.AICharacter[4] += 1
                    if abs((data.character.cx//data.colL) - \
                    (data.AICharacter[0].cx//data.colL)) >= 1 and \
                    abs((data.character.cy//data.rowL) - \
                    (data.AICharacter[0].cy//data.rowL)) >= 1:
                        if len(data.AIballoons) < data.AICharacter[0].maxBall:
                            data.AIballoons.append(\
                            Balloon(data.AICharacter[2]*data.colL, \
                            data.AICharacter[1]*data.rowL, 5, \
                            data.maze, data.AInumSoda))
                            start = (data.AICharacter[1], data.AICharacter[2])
                            coord = farFromPlayer(data.character.cx//data.colL, data.character.cy//data.rowL)
                            end = (coord[1], coord[0])
                            data.AICharacter[3] = main(data.maze, start, end)
                            data.AICharacter[4] = 0

        #from 15-112 website
        #timer for the user to prepare
        if data.levelInfo == True:  
            if (data.count % 4 == 0):
                data.seconds -= 1
                if (data.seconds < 1):
                    data.levelInfo = False

    else:
        pass
    
def redrawAll(canvas, data):
    #when game is not over, all the items, characters, etc are being drawn
    if data.isGameOver == False:
        canvas.create_image(590, 340, image=data.background)
        for wBall in data.wBall:
            wBall.draw(canvas, data.wBallImage)
        for soda in data.soda:
            soda.draw(canvas, data.sodaImage)
        data.map.draw(canvas, data.blocks)
        for balloon in data.balloons:
            if balloon.count%2 == 0:
                balloon.draw(canvas, data.balloonUp)
            else:
                balloon.draw(canvas, data.balloonDown)
        data.character.draw(canvas, data.directionCharacter)
        if data.levelTwo == True:
            if data.showAI == True:    
                for balloon in data.AIballoons:
                    if balloon.count%2 == 0:
                        balloon.draw(canvas, data.balloonUp)
                    else:
                        balloon.draw(canvas, data.balloonDown)
                data.AICharacter[0].draw(canvas, data.AIimageState)
        for monster in data.monster:
            monster[0].draw(canvas, data.monsterImage)
        if data.showLives == True:
            canvas.create_image(data.width//2, data.height//2, \
            image=data.livestate)
            canvas.create_text(3*data.width//5, data.height//2, \
            font = "Arial 40 bold", text= str(data.character.lives), \
            fill='white')
    if data.startGame == False:
        canvas.create_image(data.width//2, data.height//2, \
        image=data.startGameScreen)
    if data.instruction == True:
        canvas.create_image(data.width//2, data.height//2, \
        image=data.instructionScreen)
    if data.levelInfo == True:
        canvas.create_image(data.width//2, data.height//2, \
        image=data.blackScreen)
        canvas.create_image(data.width//2, data.height//2, \
        image=data.levelScreen)
        canvas.create_text(data.width//5*3-70, data.height//3+43, \
        text=str(data.difficulty), font="Arial 40", fill='white')
        canvas.create_text(data.width//5*3-25, data.height//2, \
        text=str(data.seconds), font="Arial 40", fill='white')
    if data.levelOneFinish == True:
        canvas.create_image(data.width//2, data.height//2, \
        image=data.levelOneFinishScreen)
    #when game is over, game over screen pops up
    if data.isGameOver == True and data.character.lives == 0:
        canvas.create_image(586,340,image=data.loseScreen)    
    if data.end == True:
        canvas.create_image(data.width//2, data.height//2, image=data.winScreen)

#################################################################
# use the run function as-is
#################################################################

#from 112 website https://www.cs.cmu.edu/~112/index.html
def run(width=300, height=300):
    
    threadMusic=PlayThread("bgm.wav")
    threadMusic.start()
    
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    
    timerFiredWrapper(canvas, data)    
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1172, 680)
