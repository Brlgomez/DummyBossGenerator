from Tkinter import *
from tkMessageBox import *
from random import randint
import generate
import analyze_boss


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
}
boss = {"width":0,"length":0}
stats = "" 

def hello():
  showinfo("Hello","hello")

def gen(canvas,x,y,width,start):
  C = canvas
  W = width
  def draw():
    global boss
    #state = generate.initialize(20,20)
    state = generate.createMonster(randint(25,75),10,10)
    #while (len(state['body'])<200):
    #    generate.randomAssign(state);
    print generate.draw(state)[0]
    value = analyze_boss.numTiles(state)
    #pos = analyze_boss.posTiles(state)
    num = analyze_boss.numSpecTiles(state)
    analyze_boss.difficulty(state)
    #print 'fire', generate.sumProp(state,'fire')
    #print 'sword',generate.sumProp(state,'sword')
    #print 'arrow',generate.sumProp(state,'arrow')
    boss = state
    stats = value
    drawBoss(C,boss,x,y,cell = width,anchor =start )
  return draw
def drawCell(canvas, x, y, width, type):
    coord = (x,y,x+width,y+width)
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
    canvas.delete(ALL)
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
    

def button():
    global boss
    boss = gen()
def main(argv):
    prog = argv
    #design = load_design(filename)

    master = Tk()
    master.title("Boss Maker")
    w,h = TILE_SIZE * 10, TILE_SIZE * 10
    #w, h = TILE_SIZE * design['width'], TILE_SIZE * design['height']
    canvas = Canvas(master, bg="navy", width=w, height=h)
    coord = 10, 10, 240, 240
    #filename = PhotoImage(file = "sunshine.gif")
    #image = canvas.create_image(300, 300, anchor=CENTER, image=filename)
    #arc = canvas.create_arc(coord, start=0, extent=200, fill="red")
    #arc = canvas.create_arc(coord, start=200, extent=100, fill="green")
    #drawState(canvas,boss,100,100)
    funct = gen(canvas,w/2,h/2,15,start = 'CENTER')
    B = Button(master, text ="Generate", command = funct)
    canvas.pack(side = TOP)
    B.pack(side = BOTTOM)
    
    
    text = Text(master)
    text.insert(INSERT, "0% - 33% Beatable: Difficult, 34%-66% Beatable: Intermediate, 67% - 100% Beatable: Easy ")
    text.insert(INSERT, stats)
    text.insert(END, " Insert stuff")
    text.pack()

    #display_design_on_canvas(canvas, design)

    master.bind('<Escape>', lambda event: master.quit())
    master.mainloop()


if __name__ == '__main__':
    import sys

    main(sys.argv)
