import sys, pygame, random, threading, time
import numpy as np
import math
from PIL import Image

pygame.init()

array = [0,2,4,8,16,32,64,128,256,512,1024,2048]
files = ["square{}.png".format(s) for s in array]


screen = pygame.display.set_mode((450, 450))
restart = False

class tile(object):
    def __init__(self,x,y,name):
        self.mergedOnce = False
        self.value = 0
        self.x = x
        self.y = y        
        self.image = pygame.image.load("images/{}".format(name))
        self.rect = self.image.get_rect()
    def render(self):
        screen.blit(self.image, (self.x,self.y))
        
class gameManager(object):
    def __init__(self):        
        self.size = 16
        self.playing = False
        self.score = 0        
        #value, merged once?
        self.grid = [[tile(10,10,"square0.png"),tile(120,10,"square0.png"),tile(230,10,"square0.png"),tile(340,10,"square0.png")],
                     [tile(10,120,"square0.png"),tile(120,120,"square0.png"),tile(230,120,"square0.png"),tile(340,120,"square0.png")],
                     [tile(10,230,"square0.png"),tile(120,230,"square0.png"),tile(230,230,"square0.png"),tile(340,230,"square0.png")],
                     [tile(10,340,"square0.png"),tile(120,340,"square0.png"),tile(230,340,"square0.png"),tile(340,340,"square0.png")]]
        
    def gridValues(self):
        printedLis = [[self.grid[0][0].value,self.grid[0][1].value,self.grid[0][2].value,self.grid[0][3].value],
                     [self.grid[1][0].value,self.grid[1][1].value,self.grid[1][2].value,self.grid[1][3].value],
                     [self.grid[2][0].value,self.grid[2][1].value,self.grid[2][2].value,self.grid[2][3].value],
                     [self.grid[3][0].value,self.grid[3][1].value,self.grid[3][2].value,self.grid[3][3].value]]

        string_image = pygame.image.tostring(screen, 'RGB')
        temp_surf = pygame.image.fromstring(string_image,(450, 450),'RGB' )
        window_to_array = pygame.surfarray.array3d(temp_surf)
        im = Image.fromarray(window_to_array)
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        im = im.transpose(Image.ROTATE_90)
        im = im.resize((64,64))
        #im.save('image.jpeg')
        image_array = np.array(im)
        
        
        return printedLis, image_array
    
    def setGrid(self, gridValues):
        for rowIndex, row in enumerate(self.grid):
            for tileIndex, thisTile in enumerate(row):
                thisTile.value = gridValues[rowIndex][tileIndex]
        self.updateGrid()
    def restart(self):
        for row in self.grid:
            for thisTile in row:
                thisTile.value = 0
                thisTile.mergedOnce = False
        
        self.playing = False
        self.updateGrid()
        self.addRandomTile([])       
        self.addRandomTile([])
        return self.gridValues()[0], self.playing
    def addRandomTile(self,seed):
        count = 0
        while True:
            if not seed:
                randomN = random.choice([2,4])
                randomX = random.randint(0,3)
                randomY = random.randint(0,3)
            else:
                randomN = seed[0]
                randomX = seed[1]
                randomY = seed[2]
            if self.grid[randomX][randomY].value == 0:
                self.grid[randomX][randomY].value = randomN
                if self.grid[randomX][randomY].value == 2:
                    self.grid[randomX][randomY].image = pygame.image.load("images/{}".format(files[1]))
                else:
                    self.grid[randomX][randomY].image = pygame.image.load("images/{}".format(files[2]))
                return [randomN, randomX, randomY], 0
                
            else:###FIX THIS MESS
                count += 1
                if count >= 20:#catch too long loop
                    avalableSpace = False
                    for r in range(4):
                        for c in range(4):
                            if self.grid[r][c].value == 0:
                                seed = [random.choice([2,4]),r,c]
                                avalableSpace = True
                                break
                                
                    if avalableSpace:
                        #print("pass")
                        pass
                    else:
                        return [], -1000
                continue
            


    def updateGrid(self):
        for rowIndex, row in enumerate(self.grid):
                for tileIndex, thisTile in enumerate(row):
                    if thisTile.value == 0:                        
                        thisTile.image = pygame.image.load("images/{}".format(files[0]))                    
                        thisTile.render()
                    elif thisTile.value == 2:
                        thisTile.image = pygame.image.load("images/{}".format(files[1]))                    
                        thisTile.render()
                    elif thisTile.value == 4:
                        thisTile.image = pygame.image.load("images/{}".format(files[2]))                    
                        thisTile.render()
                    elif thisTile.value == 8:
                        thisTile.image = pygame.image.load("images/{}".format(files[3]))                    
                        thisTile.render()
                    elif thisTile.value == 16:
                        thisTile.image = pygame.image.load("images/{}".format(files[4]))                    
                        thisTile.render()
                    elif thisTile.value == 32:
                        thisTile.image = pygame.image.load("images/{}".format(files[5]))                    
                        thisTile.render()
                    elif thisTile.value == 64:
                        thisTile.image = pygame.image.load("images/{}".format(files[6]))                    
                        thisTile.render()
                    elif thisTile.value == 128:
                        thisTile.image = pygame.image.load("images/{}".format(files[7]))                    
                        thisTile.render()
                    elif thisTile.value == 256:
                        thisTile.image = pygame.image.load("images/{}".format(files[8]))                    
                        thisTile.render()
                    elif thisTile.value == 512:
                        thisTile.image = pygame.image.load("images/{}".format(files[9]))                    
                        thisTile.render()
                    elif thisTile.value == 1024:
                        thisTile.image = pygame.image.load("images/{}".format(files[10]))                    
                        thisTile.render()
                    elif thisTile.value == 2048:
                        thisTile.image = pygame.image.load("images/{}".format(files[11]))                    
                        thisTile.render()
    def keepToCorner(self):
        reward = 0
        orderedvalues = np.partition(np.ravel(self.gridValues()[0]).flatten(), -2)
        if orderedvalues[-1] == self.gridValues()[0][0][0]:
            reward = 300
            if orderedvalues[-2] == self.gridValues()[0][0][1]:
                reward = 400
                if orderedvalues[-3] == self.gridValues()[0][0][2]:
                    reward = 500
        return reward
    def moveTiles(self,vector,seed):#good luck mate
        ##########MOVEMENT###################
        reward = 0
        pre_state = self.gridValues()[0]
        def keepInRange(l):#keep in range of list
            for i in l:
                if i <= -1:
                    l[l.index(i)] = 0
                if i >= 4:
                    l[l.index(i)] = 3
            return l
        
        for turn in range(3):
            #print("turn: "  + str(turn))
            for rowIndex, row in enumerate(self.grid):#loop through tiles
                for tileIndex, thisTile in enumerate(row):
                    
                    if thisTile.value != 0:#if the tile is not empty/zero
                        
                        next = [rowIndex-vector[0],tileIndex-vector[1]]#create var for next position index/coordianations
                        next = keepInRange(next)#bounce indexes back in to the square 
                    
                        
                        if self.grid[next[0]][next[1]].value == thisTile.value:#Merge -- if next.value == current.value 
                            if thisTile.mergedOnce == False and self.grid[next[0]][next[1]].mergedOnce == False:#check if already merged this move both current spot and next
                            
                                if tileIndex != next[1] or rowIndex != next[0]:#0-0-0-4 --> 0-0-0-4 NOT THIS 0-0-0-8
                                    nextNext = [next[0]-vector[0],next[1]-vector[1]]#2-2-2-0 --> 0-0-2-4 NOT THIS 0-0-4-2
                                    #check 2 steps ahead
                                    
                                    if nextNext[0] > -1 and nextNext[1] > -1 and nextNext[0] < 4 and nextNext[1] < 4:
                                        if self.grid[nextNext[0]][nextNext[1]].value == thisTile.value:
                                            continue
                                        
                                        else:
                                            #print("merged")
                                            self.grid[next[0]][next[1]].value = thisTile.value*2
                                            self.score += thisTile.value*2
                                            reward += thisTile.value*2
                                            self.grid[next[0]][next[1]].mergedOnce = True
                                            thisTile.mergedOnce = False
                                            thisTile.value = 0
                                        
                                    else:
                                        #print("merged")
                                        self.grid[next[0]][next[1]].value = thisTile.value*2
                                        self.score += thisTile.value*2
                                        reward += thisTile.value*2
                                        self.grid[next[0]][next[1]].mergedOnce = True
                                        thisTile.mergedOnce = False
                                        thisTile.value = 0
                                        
                                    
                                    
                        elif self.grid[next[0]][next[1]].value == 0:#if next space == empty
                            #print("moved")
                            self.grid[next[0]][next[1]].value = thisTile.value
                            self.grid[next[0]][next[1]].mergedOnce = thisTile.mergedOnce 
                            thisTile.value = 0
                        else:
                            pass
                            #print("next")
        for rowIndex, row in enumerate(self.grid):#loop through tiles
                for tileIndex, thisTile in enumerate(row):
                    self.grid[rowIndex][tileIndex].mergedOnce = False
        self.updateGrid()


        ###########REWARDS################
        new_seed = []
        running = True
        rewardDeduction = 0
        if pre_state == self.gridValues()[0]:# if made the same move
            return 0, [], False        
        else:
            new_seed, rewardDeduction = self.addRandomTile(seed)
            
        nt = 0
        for t in np.ravel(self.gridValues()[0]):# check how many empty tiles
            if t > 0:
                nt += 1
        n_tiles_coef = (1 - nt/16) * 800

        rewardforbeingincorner = self.keepToCorner() #try to keep highest values in corner
        
        
        return reward+n_tiles_coef+rewardDeduction+rewardforbeingincorner, new_seed, running
        



    

    


    
