"""
KENDRIYA VIDYALAYA SHALIMAR BAGH-110088
CLASS XII A COMPUTER SCIENCE PROJECT

MEMBERS:
1) NIKHIL KADIYAN (Roll no. 24) - Programming, testing, assets

The following project is a game made in Python using the tkinter module.

tkinter is used as it is mentioned in Appendix B of Computer Science with Python
by Sumita Arora, Class XII

The following project is a farming game in which the player starts a small farm and then
slowly builds it to an exotic green heaven.
There is also a small market at the bottom left.

CONTROLS:
W/A/S/D or Up/Left/Down/Right arrow keys to move
Mouse Click to plant seeds, harvest etc.
Escape key to escape to Main Menu

INSTRUCTIONS:
Go to market at bottom left to buy some seeds : Cost $1(in game money)
Click on green land to make a farm plot
Click again to plant seed(if available)
Wait 10 seconds for seeds to grow to plant
Click to harvest plant
Go to market, Sell plant for $2
Buy seeds again
Buy banks
...

Inspired by the game Forager, by game developer hopfrog.
Buy: https://store.steampowered.com/app/751780/Forager/
Demo: https://hopfrog.itch.io/forager-demo

ASSETS:
Character Images(Sprites) downloaded from https://jesse-m.itch.io/jungle-pack
All the other art and sound effects are self made.

FEATURES:
1. Basic UI
2. Movement and collsions
3. Nearly 15 minutes long gameplay
4. Saving highscore

Concepts of syllabus used:
1. Python basics
2. Recursion
3. Importing modules
4. Functions
5. File handling
6. 2-Dimensional arrays
7. Error handling

CLARIFICATION:
This is an original project, and is not 'copy-pasted'. Help was taken from the internet to note basic tkinter
functions.

Searching for pyRager on google only gives the result of some Reddit user. This project is not related to that
person in any way.

MODULES USED:
1. tkinter (based heavily on it, installed on standard python. If not, reinstall python with tcl/tk selected)
2. random (Used for starting quotes)
3. winsound (only for Windows, error handling used if not found)
4. math (only used once for fabs() and pow() functions)

SOFTWARE USED:
1. IDLE
2. Paint.net(since ms paint doesnt support transparent images)  https://www.getpaint.net/index.html
3. BFXR(Free software to generate algorithm driven sounds)  https://www.bfxr.net/

I have tried to explain by comments all the tkinter functions used.
Further help can be taken from http://effbot.org/tkinterbook/ and
https://www.tutorialspoint.com/python/python_gui_programming.htm
"""
try :
    import tkinter
except ImportError:
    print("tkinter not installed. Reinstall python with tcl/tk selected")

import random

winsoundFound=True

try:
    import winsound
except ImportError:
    print("winsound not found, sounds won't play.")
    winsoundFound=False

import math#used a few times

###########CONSTANTS#########################
spriteSize=64
#The size of images ON screen(not of actual file)

fontName="Impact"
#font available in Winodws 7, 8 and 10, IF NOT AVAILABLE CHANGE TO Arial

bgColor="#4e81d4"#the bg color is hex code for light blue
uiColor="#3f6299"#the ui color is darkish blue

plantGrowTime=10000#in miliseconds, i.e. 10 seconds
bankWaitTime=5000#in miliseconds
##############################################

#root is the window that opens
root=tkinter.Tk()
root.title("pyRogue")
#Make a window of size 640x640 at x=300 and y=0 pixels on  screen
root.geometry("640x640+300+0")
root.resizable(0,0)
#window is not resizable in both axis, because resizing breaks the look of this project

#icon of the window
iconImage=tkinter.PhotoImage(file="Images/icon.png")
root.iconphoto(True,iconImage)

farmImage=tkinter.PhotoImage(file="Images/farm.png")
farmImage=farmImage.zoom(2)
#image has now size 64 pixels

grassImage=tkinter.PhotoImage(file="Images/grass.png")
grassImage=grassImage.zoom(2)

mouseImage=tkinter.PhotoImage(file="Images/mouseLook.png")
mouseImage=mouseImage.zoom(4)

plantImage=tkinter.PhotoImage(file="Images/plant.png")
plantImage=plantImage.zoom(2)

plantGrownImage=tkinter.PhotoImage(file="Images/plantGrown.png")
plantGrownImage=plantGrownImage.zoom(2)

marketImage=tkinter.PhotoImage(file="Images/market.png")
marketImage=marketImage.zoom(2)#128x128 pixels

bankImage=tkinter.PhotoImage(file="Images/bank.png")
bankImage=bankImage.zoom(2)

roadImage=tkinter.PhotoImage(file="Images/road.png")
roadImage=roadImage.zoom(2)

menuClickSound="Sound/menuClick.wav"
startGameSound="Sound/start.wav"
plantGrownSound="Sound/plantGrown.wav"
plantPlaceSound="Sound/plantPlace.wav"

#player - run and idle animations (6 frame) in an array

playerIdleImage=[]
for x in range(6):
    curImage=tkinter.PhotoImage(file=("Images/playeridle/idle"+str(x+1)+".png"))
    curImage=curImage.zoom(2)
    playerIdleImage.append(curImage)

playerRunImage=[]
for x in range(6):
    curImage=tkinter.PhotoImage(file=("Images/playerrun/run"+str(x+1)+".png"))
    curImage=curImage.zoom(2)
    playerRunImage.append(curImage)


#Functions for the project. Many functions call other functions.
def playSound(sound):
    if winsoundFound:
        #play the sound once and dont stop the program to play sound
        winsound.PlaySound(sound,winsound.SND_FILENAME|winsound.SND_ASYNC)

def placeImg(cnvs,x,y,img):
    #function to make this repeated process small
    imageObject=cnvs.create_image(x*spriteSize,y*spriteSize,image=img,anchor="nw")
    return imageObject


#Just like global keyword is used to call variables outside functions
#nonlocal keyword is used to call variables of parent function
#eg.
#x
#def a():
#   global x
#   c
#   def b():
#       global x
#       nonlocal c


#These are all the position lists storing positions, typed here for reference :
# playerPosition
# groundPositions
# walkPositions
# farmPositions
# plantPositions
# marketPositions


def generateLevel():
    #Canvas has by default a grayish width so highlightthickness is used
    canvas=tkinter.Canvas(gameFrame,bg=bgColor,height=640+2*64,width=640,highlightthickness=0)
    #height is big to accomodate market
    canvas.place(x=0,y=0)
    #focus on canvas to take input
    canvas.focus_set()

    uiCanvas=tkinter.Canvas(gameFrame,bg=uiColor,height=24,width=640,highlightthickness=0)
    uiCanvas.place(x=0,y=0)

    seed=0#in game item

    money=1#in game item

    plant=0#in game item

    uiSeed=uiCanvas.create_text(0,0,text="Seeds : "+str(seed),fill="white",anchor="nw",font=(fontName,12))#at position 0,0

    uiMoney=uiCanvas.create_text(200,0,text="Money : $"+str(money),fill="white",anchor="nw",font=(fontName,12))

    uiPlant=uiCanvas.create_text(400,0,text="Plant : "+str(plant),fill="white",anchor="nw",font=(fontName,12))


    marketFrame=tkinter.Canvas(gameFrame,bg=uiColor,height=320,width=320)
    marketFrame.place(x=1000,y=1000)#out of screen initially, this frame is used to buy seeds and sell plants

    #########################SAVING SYSTEM###############################

    highScore=0#score stored in a text file

    #NOTE : highScore.txt was manually created once at first time
    #This script merely updates that text file

    file1=open("highScore.txt","r")#read mode
    highScore=int(file1.read())
    file1.close()

    currentScore=0

    def addToScore(n):
    	nonlocal currentScore
    	nonlocal highScore

    	currentScore+=n

    	if currentScore>highScore:
    		highScore=currentScore

    		file1=open("highScore.txt","w")#write mode
    		file1.write(str(highScore))
    		file1.close()

    		#I could not think of a game INSIDE the game where I could show the score
    		#As a result, score is only shown in highscore.txt

    #######################################################################

    def showMarket():
        playSound(menuClickSound)
        marketFrame.place(x=160,y=160)#now visible
        #remove keyboard so player can not move when market is open
        marketFrame.focus_set()

    def closeMarket():
        playSound(menuClickSound)
        marketFrame.place(x=1000,y=1000)
        #take input again
        canvas.focus_set()

    def buySeed():

        nonlocal seed
        nonlocal money

        if money>=1:

            #Only play sound if pressing the button has any effect
            playSound(menuClickSound)

            seed+=1
            uiCanvas.itemconfig(uiSeed,text="Seeds : "+str(seed))

            money-=1
            uiCanvas.itemconfig(uiMoney,text="Money : $"+str(money))

    def sellPlant():

        nonlocal plant
        nonlocal money

        if plant>=1:

            playSound(menuClickSound)

            money+=2
            uiCanvas.itemconfig(uiMoney,text="Money : $"+str(money))

            plant-=1
            uiCanvas.itemconfig(uiPlant,text="Plant : "+str(plant))

            addToScore(1)


    def giveMoneyFromBank():

        nonlocal money

        money+=1

        uiCanvas.itemconfig(uiMoney,text="Money : $"+str(money))

        canvas.after(bankWaitTime,giveMoneyFromBank)

    #Banks are non-interactable buildings that generate $1 after every
    #5 seconds, per bank. Forager, the game on which this project is based 
    #have banks too.

    bankPositions=[]
    curBankPos=0#current index

    for x in range(2,10):
        for y in range(10,12):
            bankPositions.append([x,y])

    bankCost=10


    def getBank():

        nonlocal money
        nonlocal curBankPos
        nonlocal bankCost


        if money>=bankCost and curBankPos<len(bankPositions):
            playSound(menuClickSound) 

            money-=bankCost
            uiCanvas.itemconfig(uiMoney,text="Money : $"+str(money))

            addAtBankPos=bankPositions[curBankPos]

            placeImg(canvas,addAtBankPos[0],addAtBankPos[1],bankImage)

            #Exponential increase in next bank cost
            bankCost=int(bankCost*(math.pow(1.1,curBankPos*0.1+1)))
            bankButton.config(text="BUY BANK : PAY $"+str(bankCost))

            curBankPos+=1


            #After every per bank 5 seconds, call giveMoney function to add money
            #given by the banks
            canvas.after(bankWaitTime,giveMoneyFromBank)

            addToScore(2)

        elif curBankPos==len(bankPositions):
            bankButton.config(text="Max. Bank limit reached")


    seedButton=tkinter.Button(marketFrame,text="BUY 1 SEED : PAY $1",width=20,bg=uiColor,fg="white",command=buySeed,font=(fontName,12))
    seedButton.place(x=80,y=60)

    plantButton=tkinter.Button(marketFrame,text="SELL 1 PLANT : GET $2",width=20,bg=uiColor,fg="white",command=sellPlant,font=(fontName,12))
    plantButton.place(x=80,y=120)

    bankButton=tkinter.Button(marketFrame,text="BUY BANK : PAY $10",width=20,bg=uiColor,fg="white",command=getBank,font=(fontName,12))
    bankButton.place(x=80,y=180)

    #command function can not take any arguments
    marketExitButton=tkinter.Button(marketFrame,text="CLOSE",width=6,bg=uiColor,fg="white",command=closeMarket,font=(fontName,12))
    marketExitButton.place(x=260,y=0)

    groundPositions=[]#to check if farm can be placed

    farmPositions=[]#this is used below #to check if crop can be planted

    walkPositions=[]#to check if player can walk

    marketPositions=[]#to check if player clicked on market

    plantPositions=[]#to check if seed(grown to plant) can be removed to sell

    levelSizeMin=10


######################LEVEL GENERATION################################

    #The main and walkable land
    for x in range(levelSizeMin):
        for y in range(levelSizeMin):
            curGrass=placeImg(canvas,x,y,grassImage)

            #curGrass is an INDEX NUMBER, an id of a canvas object
            groundPositions.append([x,y])
            walkPositions.append([x,y])

    #not walkable land for market
    for x in range(0,2):
        for y in range(10,12):
            placeImg(canvas,x,y,roadImage)
            marketPositions.append([x,y])

    #land for banks
    for x in range(2,10):
        for y in range(10,12):
            placeImg(canvas,x,y,roadImage)

    placeImg(canvas,0,10,marketImage)#place the market image


#####################SOME FUNCTIONS##################################

    def incrementPlayerImage(index,anim):
        canvas.itemconfig(player,image=anim[index])

    def updatePlayerImage(curIndex,time=100):
        #time in miliseconds
        #changes to next image in given time
        nonlocal curPlayerState

        if curPlayerState=="Idle":
            end=len(playerIdleImage)-1
            if curIndex>=0 and curIndex<end:
                nextIndex=curIndex+1
            else:
                nextIndex=0

            incrementPlayerImage(nextIndex,playerIdleImage)
            curIndex=nextIndex
            
            #after(miliseconds, function callback,[argument of function separated by ,])
            canvas.after(time,updatePlayerImage,curIndex)

        elif curPlayerState=="Run":
            end=len(playerRunImage)-1
            nextIndex=0
            if curIndex>=0 and curIndex<end:
                nextIndex=curIndex+1
            else:
                curPlayerState="Idle"

            incrementPlayerImage(nextIndex,playerRunImage)
            curIndex=nextIndex
            
            #after(miliseconds, function callback,[argument of function separated by ,])
            canvas.after(time,updatePlayerImage,curIndex)


    #playerStates=["Idle","Run"]
    #These states determine which animation should be
    #played, whether the player's current position on canvas should be taken as
    #his current grid position etc.
    curPlayerState="Idle"

    startPosx=levelSizeMin//2
    startPosY=levelSizeMin//2

    player=placeImg(canvas,startPosx,startPosY,playerIdleImage[0])

    

    def movePlayerUp():
        canvas.tag_raise(player)
    #This moves the player on top of layer whenever called


    playerPosition=[startPosx,startPosY]
    
    #Call to above recursive function for animation
    updatePlayerImage(0)

    plantIds=[]

    def growPlant(plant,x,y):
        canvas.itemconfig(plant,image=plantGrownImage)
        playSound(plantGrownSound)
        plantPositions.append([x,y])
        plantIds.append(plant)

    def getPlant(x,y):

        nonlocal plant

        #I could not find any direct function to get object id from position
        #Hence I am cycling through an already created list of plant ids and
        # then deleting as necessary
        for i in plantIds:
            if canvas.coords(i)==[x*spriteSize,y*spriteSize]:
                canvas.delete(i)
                plant+=1
                uiCanvas.itemconfig(uiPlant,text="Plant :"+str(plant))

        plantPositions.remove([x,y])
        farmPositions.append([x,y])

    def plantSeeds(x,y):#function used in mouse click event
        nonlocal seed

        if seed>=1:
            seed-=1
            uiCanvas.itemconfig(uiSeed,text="Seeds : "+str(seed))
            curPlant=placeImg(canvas,x,y,plantImage)

            farmPositions.remove([x,y])#cant plant seed on already planted farmland
            #After 10 seconds, the plant grows, here curPlant,x,y are arguments
            #of functon growPlant

            playSound(plantPlaceSound)

            canvas.after(plantGrowTime,growPlant,curPlant,x,y)

        movePlayerUp()#raises player to top
        #player is raised because whenever a new object is created it is
        #by default on top-most layer and hence hides player

##################PLAYER MOVEMENT##############################

    canvasX=0
    canvasY=0

    #These are defined as nonlocal variables and not
    #local variables of motion(event) function
    #to fix the bug when mouseImage was not updating
    #when the player moves without changing the postion of
    #the mouse
    
    curMousePosX=0#Mouse Position x ON THE CANVAS
    curMousePosY=0#Mouse Position y ON THE CANVAS

    def placeMouseImage():
        pass

    def move(x,y):

        nonlocal canvasX
        nonlocal canvasY

        nonlocal curPlayerState

        nonlocal curMousePosX
        nonlocal curMousePosY

        curPlayerState="Run"

        #Move the canvas to keep player at center
        canvas.place(x=canvasX-x*spriteSize,y=canvasY-y*spriteSize)

        canvasX-=x*spriteSize
        canvasY-=y*spriteSize

        canvas.move(player,x*spriteSize,y*spriteSize)

        playerPosition[0]=playerPosition[0]+x
        playerPosition[1]=playerPosition[1]+y

        #Update mouseImage when player moves
        #because the mouse is not moved and
        #hence motion(event) function is not called to update mouseImage

        curMousePosX+=x
        curMousePosY+=y

        mouse=placeImg(canvas,curMousePosX,curMousePosY,mouseImage)
        mouses.append(mouse)

        #delete previous mouseImages
        if len(mouses)>1:
            for x in mouses:
                if not x==mouses[len(mouses)-1]:#if it is not last item of list
                    canvas.delete(x)
                    mouses.remove(x)


    def findInTwoDList(num,list2d,index):#index 0 or 1 of 2D list, i.e. , x or y value
        for i in range(len(list2d)):
            if num==list2d[i][index]:
                return True

    #In computer graphics, down is positive y and right is positive x
    def moveUp(event):
        cond=findInTwoDList(playerPosition[1]-1,walkPositions,1)
        if cond:  
            move(0,-1)

    def moveDown(event):
        cond=findInTwoDList(playerPosition[1]+1,walkPositions,1)
        if cond:
            move(0,1)

    def moveLeft(event):
        cond=findInTwoDList(playerPosition[0]-1,walkPositions,0)
        if cond:
            move(-1,0)

    def moveRight(event):
        cond=findInTwoDList(playerPosition[0]+1,walkPositions,0)
        if cond:
            move(1,0)

############################MOUSE#########################################

    
    def checkMouseDistFromPlayer(x,y):
        maxDist=2

        #fabs is the modulus function
        if math.fabs(playerPosition[0]-x)<maxDist:
            if math.fabs(playerPosition[1]-y)<maxDist:
                if not(playerPosition[0]==x and playerPosition[1]==y):
                    return True
    
    mouses=[]
    def motion(event):
        nonlocal curMousePosX
        nonlocal curMousePosY

        curMousePosX,curMousePosY=event.x,event.y#mouse x and y

        curMousePosX=curMousePosX//spriteSize
        curMousePosY=curMousePosY//spriteSize#x and y in world position

        if checkMouseDistFromPlayer(curMousePosX,curMousePosY):
            mouse=placeImg(canvas,curMousePosX,curMousePosY,mouseImage)
            mouses.append(mouse)

        #delete previous mouseImages
        if len(mouses)>1:
            for x in mouses:
                if not x==mouses[len(mouses)-1]:#if it is not last item of list
                    canvas.delete(x)
                    mouses.remove(x)

    def lclick(event):
        x,y=event.x,event.y
        x=x//spriteSize
        y=y//spriteSize
        if checkMouseDistFromPlayer(x,y):
            if [x,y] in groundPositions:
                farm=placeImg(canvas,x,y,farmImage)

                farmPositions.append([x,y])
                groundPositions.remove([x,y])#Note: not removing from walkPositions

                movePlayerUp()#raises player to top
                #player is raised because whenever a new object is created it is
                #by default on top-most layer and hence hides player

            elif [x,y] in farmPositions:
                plantSeeds(x,y)

            elif [x,y] in plantPositions:
                getPlant(x,y)

            elif [x,y] in marketPositions:
                showMarket()

    def toMenu(event):
        raiseFrame(menuFrame)


    #bind the canvas with keyboard keys to recieve input and call a function when input is given
    #It is required to place it at the end

   #tkinter does not allow arguments in binding functions

    canvas.bind("w",moveUp)
    canvas.bind("<Up>",moveUp)#arrow key

    canvas.bind("a",moveLeft)
    canvas.bind("<Left>",moveLeft)

    canvas.bind("s",moveDown)
    canvas.bind("<Down>",moveDown)

    canvas.bind("d",moveRight)
    canvas.bind("<Right>",moveRight)

    canvas.bind("<Motion>",motion)#mouse moved
    canvas.bind("<Button-1>",lclick)#left mouse click

    canvas.bind("<Escape>", toMenu)#Go to Main menu


#######################MAIN MENU#################################################


#random quotes, inspired from Minecraft's title screen
#80 character limit
#Duplicate lines so they show more often
wordsOfWisdom=[
"This isn't even my final form.",
"All we have to do was to follow the train, CJ",
"Any computer is a laptop if you are brave enough!",
"Semicolons? We don't do that here.",
"State of the art visuals.",
"It's the endgame.",
"Gamers don't die. They respawn.",
"12345 is a bad password.",
"90% bug free!",
"Any computer is a laptop if you are brave enough!",
"Where there is a code, there is a bug.",
"pyRogue!",
"Have you played Undertale?",
"Play Deltarune. It's free!",
"It's a game.",
"Any computer is a laptop if you are brave enough!",
"Made in India",
"sqrt(-1) like you!",
"Don't kill people.",
"School project.",
"Kendriya Vidyalaya, Shalimar Bagh"]

wordsOfWisdomIndex=random.randint(0,len(wordsOfWisdom)-1)

#All the functions and objects below are written so they do not raise
#any error related to references and hence they should not be moved to any
#other line


menuFrame=tkinter.Frame(root,width=640,height=640,bg=bgColor)
menuFrame.place(x=0,y=0)

def raiseFrame(frame):
    frame.tkraise()
    #change wordsOfWisdom text
    if frame==menuFrame:
        global wordsOfWisdomIndex
        wordsOfWisdomIndex=random.randint(0,len(wordsOfWisdom)-1)
        wordsOfWisdomText.config(text=wordsOfWisdom[wordsOfWisdomIndex])

gameFrame=tkinter.Frame(root,width=640,height=640)
gameFrame.place(x=0,y=0)
raiseFrame(gameFrame)

bgGameCanvas=tkinter.Canvas(gameFrame,bg=bgColor,height=1200,width=1200,highlightthickness=0)

bgGameCanvas.place(x=-400,y=-400)

def creditToMain():
    playSound(menuClickSound)
    raiseFrame(menuFrame)

creditFrame=tkinter.Frame(root,width=640,height=640,bg=bgColor)
creditFrame.place(x=0,y=0)

creditText="    MADE BY \n  NIKHIL KADIYAN \n PROGRAMMING, ART*, TESTING\n\n\n\n\n\n\n\n *Only the character is downloaded\
\nLink in source code"

creditTextLabel=tkinter.Label(creditFrame,text=creditText,bg=bgColor,fg="white",font=(fontName,20))
creditTextLabel.place(x=140,y=100)

creditToMainButton=tkinter.Button(creditFrame,text="MENU",width=10,bg=bgColor,fg="white",command=creditToMain,font=(fontName,12))
creditToMainButton.place(x=300,y=600)

#call the above function, that initiates the game

generateLevel()

def startGame():
    playSound(startGameSound)
    raiseFrame(gameFrame)
    #Change text
    startButton.config(text="RESUME")

def credit():
    playSound(menuClickSound)
    raiseFrame(creditFrame)

#the commands of these buttons do not take any arguments, it is a tkinter limitation

titleText=tkinter.Label(menuFrame,text="pyRager",bg=bgColor,fg="white",font=(fontName,70))
titleText.place(x=200,y=120)

startButton=tkinter.Button(menuFrame,text="START",width=10,bg=bgColor,fg="white",command=startGame,font=(fontName,12))
startButton.place(x=300,y=320)

creditButton=tkinter.Button(menuFrame,text="CREDITS",width=10,bg=bgColor,fg="white",command=credit,font=(fontName,12))
creditButton.place(x=300,y=360)

quitButton=tkinter.Button(menuFrame,text="QUIT",width=10,bg=bgColor,fg="white",font=(fontName,12),command=root.destroy)
quitButton.place(x=300,y=400)

wordsOfWisdomText=tkinter.Label(menuFrame,text=wordsOfWisdom[wordsOfWisdomIndex],bg=bgColor,fg="white",font=(fontName,20))
wordsOfWisdomText.place(x=0,y=600)

#Make sure that menu is the first thing the user sees when
#opening the game
raiseFrame(menuFrame)

#an infinite loop that is called till
#the game window is closed
root.mainloop()

