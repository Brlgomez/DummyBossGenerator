from Tkinter import *
from tkMessageBox import *
from random import randint
import generate
import analyze_boss
import game


TILE_SIZE = 32
COLOR = {
    'a': 'white',
    'b': 'red',
    'c': 'green',
    'd': 'blue',
    'e': 'yellow',
    'f': 'orange',
    'g': 'purple',
    'h': 'gray',
    'i': 'brown',
    'wall': 'black',
    'player': 'green',
    'swordQEntity': 'gray',
    'arrowEntity': 'white',
    'fireBallEntity': 'red',
    'floor':"white"
}
boss = {"width":0,"length":0}
player = None
level = game.buildSmall()

stats = "" 

def hello():
  showinfo("Hello","hello")
  
def genLevel(canvas,x,y,width,start):
  def draw():
    global level
    state = game.buildSmall()
    print game.stateToString(state)
    drawLevel(canvas,state,x,y,cell = width,anchor =start)
    level = state
  return draw

def gen(canvas,x,y,width,start):  
  def draw():
    global boss
    #state = generate.initialize(20,20)
    state = generate.createMonster(randint(25,75),10,10)
    #while (len(state['body'])<200):
    #    generate.randomAssign(state);
    print generate.draw(state)[0]
    boss = state
    #pos = analyze_boss.posTiles(state)
    #othermaster.destroy()
    canvas.delete(ALL)
    drawBoss(canvas,boss,x,y,cell = width,anchor =start )
  return draw
def eval():
    global boss
    state = boss
    value = analyze_boss.numTiles(state)
    num = analyze_boss.numSpecTiles(state)
    stat2 = analyze_boss.difficulty(state)
    #print 'fire', generate.sumProp(state,'fire')
    #print 'sword',generate.sumProp(state,'sword')
    #print 'arrow',generate.sumProp(state,'arrow')
    stats = value
    othermaster = Tk()
    othermaster.title("Analysis")
    text = Text(othermaster, width = 100)
    text.insert(INSERT, "0% - 33% Beatable: Difficult, 34%-66% Beatable: Intermediate, 67% - 100% Beatable: Easy ")
    text.insert(INSERT, "\n")
    text.insert(INSERT, stat2['sword_perc']['string2'])
    text.insert(INSERT, "\n")
    text.insert(INSERT, stat2['fire_perc']['string2'])
    text.insert(INSERT, "\n")
    text.insert(INSERT, stat2['arrow_perc']['string2'])
    text.insert(END, "")
    text.pack()
    othermaster.bind('<Escape>', lambda event: othermaster.destroy())  
def drawCell(canvas, x, y, width, type):
    coord = (x,y,x+width,y+width)
    color = COLOR[type]
    rect = canvas.create_rectangle(coord, fill=color)
    #, tags=('boss',), outline=''
def drawRect(canvas, x, y, w,l, type):
    coord = (x,y,x+w,y+l)
    color = COLOR[type]
    rect = canvas.create_rectangle(coord, fill=color)
    #, tags=('boss',), outline=''

def getInitialCoord(x,y,width,length,anchor):
    startX, startY = 0, 0
    if anchor is 'CENTER':
        startX, startY = x-width/2, y-length/2
    elif anchor is 'NW':
        startX, startY = x, y
    elif anchor is 'N':
        startX, startY = x-width/2, y
    elif anchor is 'NE':
        startX, startY = x-width, y
    elif anchor is 'W':
        startX, startY = x, y-length/2
    elif anchor is 'E':
        startX, startY = x-width, y-length/2
    elif anchor is 'SE':
        startX, startY = x, y-length
    elif anchor is 'N':
        startX, startY = x-width/2, y-length
    elif anchor is 'N':
        startX, startY = x-width, y-length
    return startX,startY
    
def drawBoss(canvas,state,x,y,cell = 4,anchor = 'CENTER'):
    width = state['width']*cell
    length = state['length']*cell
    startX, startY = getInitialCoord(x,y,width,length,anchor)
    currX, currY = startX, startY
    for l in range(state['length']):
        currX = startX
        for w in range(state['width']):
            #print (w,l)
            if (w,l) in state['body']:
                drawCell(canvas,currX,currY,cell,state['body'][(w,l)])
            currX+=cell
        currY+=cell
    
def drawLevel(canvas,state,x,y,cell = 4,anchor = 'CENTER'):
    canvas.delete(ALL)
    width = state['width']*cell
    length = state['length']*cell
    startX, startY = getInitialCoord(x,y,width,length,anchor)
    currX, currY = startX, startY
    for l in range(state['length']):
        currX = startX
        for w in range(state['width']):
            #print (w,l)
            if (w,l) in state['objects']:
                wid = state['objects'][(w,l)]["width"]*cell
                len = state['objects'][(w,l)]["length"]*cell
                drawRect(canvas,currX-wid/2,currY-len/2,wid,len,state['objects'][(w,l)]["name"])
            currX+=cell
        currY+=cell
    for item in state['entities']:
        loc, entity = item
        x,y = entity["physLoc"]
        wid = entity["width"]*cell
        len = entity["length"]*cell
        if entity["name"] is "boss":
            drawBoss(canvas,entity["data"],startX+x*cell,startY+y*cell,cell,'CENTER')
        else:
          drawRect(canvas,startX+x*cell-wid/2,startY+y*cell-len/2,wid,len,entity["name"])
    x,y = state['player']
    #drawCell(canvas,startX+x*cell,startY+y*cell,cell,"player")
    drawRect(canvas,startX+x*cell-cell/2,startY+y*cell-cell/2,cell,cell,"player")
def addBoss(canvas,x,y,width,start):
    def add():
        global boss
        global level
        game.placeBoss(level,level["width"]/2,level["width"]/2,boss)
        drawLevel(canvas,level,x,y,cell = width,anchor =start)
    return add
def button():
    global boss
    boss = gen()
def main(argv):
    prog = argv
    #design = load_design(filename)

    master = Tk()
    master.title("Boss Maker")
    w,h = TILE_SIZE * 10, TILE_SIZE * 10
    bossCanvas = Canvas(master, bg="navy", width=w, height=h)
    canvas = Canvas(master, bg="navy", width=w, height=h)
    coord = 10, 10, 240, 240
    #filename = PhotoImage(file = "sunshine.gif")
    #image = canvas.create_image(300, 300, anchor=CENTER, image=filename)
    global level 
    drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
    funct = genLevel(canvas,w/2,h/2,10,start = 'CENTER')
    B = Button(master, text ="Clear", command = funct)
    add = addBoss(canvas,w/2,h/2,10,start = 'CENTER')
    A = Button(master, text ="Import",command = add)
    gener = gen(bossCanvas,w/2,h/2,10,start = 'CENTER')
    C = Button(master, text ="Generate", command = gener)
    D = Button(master, text ="Evaluate", command = eval)
    
    canvas.pack()
    canvas.grid(row=0, column = 0, columnspan = 2)
    bossCanvas.pack()
    bossCanvas.grid(row=0, column = 2, columnspan = 2)
    B.pack()
    B.grid(row=1, column = 0)
    A.pack()
    A.grid(row=1, column = 1)
    C.pack()
    C.grid(row=1, column = 2)
    D.pack()
    D.grid(row=1, column = 3)
    
    def tick():
       game.tick(level)
       drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
       master.after(10, tick)
    def move(direction):
       game.moveOrTurn(level,direction,0.5)
       drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
    def fire():
       game.shootFire(level)
       drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
    def sword():
       game.swingSword(level)
       drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
    def arrow():
       game.shootArrow(level)
       drawLevel(canvas,level,w/2,h/2,10,anchor = 'CENTER')
    master.bind('<Escape>', lambda event: master.quit())
    master.bind('<Right>', lambda event:move("E"))
    master.bind('<Left>', lambda event: move("W"))
    master.bind('<Up>', lambda event: move("N"))
    master.bind('<Down>', lambda event: move("S"))
    master.bind('<space>', lambda event: sword())
    master.bind('a', lambda event: fire())
    master.bind('s', lambda event: arrow())
    master.after(1000, tick)
    master.mainloop()
if __name__ == '__main__':
    import sys

    main(sys.argv)
