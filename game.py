import math

DAMAGETYPES = ("slash","pierce","fire")
ATTACKTYPES = ("swing","straight","throw")
DIRECTIONS = ("N","E","W","S")
TOOLS = {
  "sword": {
    "damage":1,
    "attackType":"swing",
    "range":1,
    "damageType":"slash",
  },
  "arrow": {
    "damage":1,
    "attackType":"straight",
    "range":10,
    "damageType":"pierce",
  },
  "fireRod": {
    "damage":1,
    "attackType":"straight",
    "range":5,
    "damageType":"fire",
  }
}
NOTHING_HAPPENED = 0
DEAD = 1
MOVED = 2
# ###############################################
# FUNCTIONS CALLED DURING TICKS AND COLLISIONS
#
# These functions make up a list of functions 
# that can be called by an object or entity's
# collision with another object, or every second
# ###############################################
# ties a function to a list of targets, used for collision tests
def contactWith(targets,do):
    def function(state,this,that):
        if that["name"] in targets:
          return do(state,this,that)
    return function
# when counter reaches goal, do function
# goal should be a lambda function, like 
# (lambda x: x>2)
def countDown(goal,do,increment = 1,restart = True):
    def function(state,this,that = None):
        #print this["counter"]
        if goal(this["counter"]):
            if restart: this["counter"] = 0
            return do(state,this,that)
        else:
            this["counter"] += increment
    return function
#deletes it's own index
def killSelf(state,this,that = None):
    dict, i = this["dataLoc"]
    del this
    return DEAD
#move in object's direction
def moveForward(state,this, that = None):
    loc = {"N":(0,-1),"E":(1,0),"W":(-1,0),"S":(0,1)}
    #print this["name"]
    dx,dy = loc[this["direction"]]
    x,y = this["physLoc"]
    nX, nY = x+dx*this["movementSpeed"],y+dy*this["movementSpeed"]
    #print x,y
    #print dx,dy
    #print nX,nY
    if (nX<0 or nX>=state["width"] or nY<0 or nY>=state["length"]):
        return
    this["physLoc"] = (nX,nY)
    return MOVED
#objects stay in grid locations, one per location
OBJECTS = {
  "wall":{
    "name":"wall",
    "length":1.0,
    "width":1.0,
    "dataLoc": ("objects",0),
    "physLoc": (0.0,0.0),
    "isSolid":True,
    "movementSpeed":0.0,
    "movementDirection":"N",
    "damageEnemy":False,
    "damageHero":False,
    "damageType":"",
    "counter": 0,
    "onCollision": [],
    "onTick": [],
    "asChar":'W'
  }
}
#entities can have float locations, and can have multiple at any given spot
ENTITIES = {
  "swordQEntity":{
    "name":"swordQEntity",
    "length":2.0,
    "width":2.0,
    "dataLoc": ("entities",0),
    "physLoc": (0.0,0.0),
    "isSolid":False,
    "movementSpeed":0.0,
    "movementDirection":"N",
    "damageEnemy":True,
    "damageHero":False,
    "damageType":"slash",
    "counter": 0,
    "onCollision": [],
    "onTick": [countDown(lambda x: x>0,killSelf)],
    "asChar": '/'
  },
  "arrowEntity":{
    "name":"arrowEntity",
    "length":1.0,
    "width":1.0,
    "dataLoc": ("entities",0),
    "physLoc": (0.0,0.0),
    "isSolid":False,
    "movementSpeed":1.0,
    "movementDirection":"N",
    "damageEnemy":True,
    "damageHero":False,
    "damageType":"pierce",
    "counter": 0,
    "onCollision": [contactWith(("wall","boss"),killSelf)],
    "onTick": [moveForward],
    "asChar": '|'
  },
  "fireBallEntity":{
    "name":"fireBallEntity",
    "length":0.8,
    "width":0.8,
    "dataLoc": ("entities",0),
    "physLoc": (0,0),
    "isSolid":False,
    "movementSpeed":1,
    "movementDirection":"N",
    "damageEnemy":True,
    "damageHero":False,
    "damageType":"fire",
    "counter": 0,
    "onCollision": [contactWith(("wall","boss"),killSelf)],
    "onTick": [moveForward],
    "asChar":'*'
  }
}
#turn float coordinates into grid coordinates
def getGridNum(floatPair):
    return (math.floor(floatPair[0]),math.floor(floatPair[1]))
def initialize(width,length):
  assert width>0 and length>0
  return {
    "width":width,
    "length":length,
    "player":(width/2.0,length/2.0),
    "playerDirection":"N",
    "playerInventory":(),
    "currentItem":None,
    #(arrow,sword,boomerang)
    "objects":{},
    #(x,y): objectName
    "entities":[]
    #[((x,y),entityName),]
  }
# places object at x,y of a given state,
# x,y are int
def placeObject(state,x,y,name):
  assert name in OBJECTS.keys()
  assert x >= 0 and x <state["width"]
  assert y >= 0 and x <state["length"]
  object = dict(OBJECTS[name])
  object["dataLoc"] = ("object",(x,y))
  object["physLoc"] = (x,y)
  state["objects"][(x,y)] = object
  return object
# places entity at x,y of a given state,
# x,y are float
def placeEntity(state,x,y,name):
  assert name in ENTITIES.keys()
  assert x >= 0 and x <state["width"] and y >= 0 and y <state["length"]
  entity = dict(ENTITIES[name])
  entity["physLoc"] = (x,y)    
  thisItem = 0
  colliding = checkCollision(state,entity)
  for colFunction in entity["onCollision"]:
    for that in colliding:
      thisItem = colFunction(state,entity,that)
  if thisItem is DEAD:
    return {}
  entity["dataLoc"] = ("entities",len(state["entities"]))
  state["entities"].append(((x,y),entity))
  return entity
def importBoss(boss,x,y):  
  bossEntity = {
    "name":"boss",
    "length":boss["length"],
    "width":boss["width"],
    "dataLoc": ("entities",0),
    "physLoc": (x,y),
    "isSolid":False,
    "movementSpeed":1,
    "movementDirection":"S",
    "damageEnemy":False,
    "damageHero":True,
    "damageType":"",
    "counter": 0,
    "onCollision": [],
    "onTick": [],
    "asChar":'B',
    "data" : boss
  }
  return bossEntity
def placeBoss(state,x,y,boss):
  #assert x >= 0 and x <state["width"] and y >= 0 and y <state["length"]
  if(x < 0 or x>=state["width"] or y<0 or y>=state["length"]):
    print "ERROR: invalid location"
    return
  enemy = importBoss(boss,x,y)
  w,l = enemy["width"],enemy["length"]
  if(x - w/2< 0 or x+w/2>=state["width"] or y-l/2<0 or y+l/2>=state["length"]):
    print "ERROR: Boss too big"
    return     
  enemy["dataLoc"] = ("entities",len(state["entities"]))
  state["entities"].append(((x,y),enemy))
  return enemy
def buildSmall():
    w, l = 20,20
    state = initialize(w,l)
    for i in range(w):
      placeObject(state,i,0,"wall")
      placeObject(state,i,l-1,"wall")
    for i in range(1,l-1):
      placeObject(state,0,i,"wall")
      placeObject(state,w-1,i,"wall")
    state["player"] = (w/2,l-3)
    return state
def intersect(minX1,maxX1,minY1,maxY1,minX2,maxX2,minY2,maxY2):
    insideX = (minX1<=minX2 and minX2<=maxX1) or (minX2<=minX1 and minX1<=maxX2)
    insideY = (minY1<=minY2 and minY2<=maxY1) or (minY2<=minY1 and minY1<=maxY2)
    return insideX and insideY
def intersectBoss(minX,maxX,minY,maxY,boss):
    w,l = boss["width"]/2.0,boss["length"]/2.0
    x,y = boss["physLoc"]
    #trivial check
    if not intersect(minX,maxX,minY,maxY,x-w,x+w,y-l,y+l):
        return False
    for loc,type in boss["data"]["body"].items():
        width = 1.0
        x1,y1 = loc
        x2 = x-w +x1*boss["width"]/boss["data"]["width"]
        y2 = y-l +y1*boss["length"]/boss["data"]["length"]
        #may end up changing intersect so it returns some information
        i = intersect(minX,maxX,minY,maxY,x2,x2+width,y2,y2+width)
        if i:
            del boss["data"]["body"][(x1,y1)]
            return i
    return False
def intersectThat(minX,maxX,minY,maxY,that):
    if that["name"] == "boss": 
        return intersectBoss(minX,maxX,minY,maxY,that)
    w,l = that["width"]/2.0,that["length"]/2.0
    x,y = that["physLoc"]
    eMinX, eMinY = x-w,y-l
    eMaxX,eMaxY = x+w,y+l
    return intersect(minX,maxX,minY,maxY,eMinX,eMaxX,eMinY,eMaxY)
def intersectThisThat(this, that):
    w,l = this["width"]/2.0,this["length"]/2.0
    x,y = this["physLoc"]
    minX,minY = x-w,y-l 
    maxX,maxY = x+w,y+l
    if that["name"] == "boss": 
        return intersectThat(minX,maxX,minY,maxY,that)
    if this["name"] == "boss": 
        return intersectThat(that,this)
    w,l = that["width"]/2,that["length"]/2
    x,y = that["physLoc"]
    eMinX, eMinY = x-w,y-l
    eMaxX,eMaxY = x+w,y+l
    #print minX,maxX,minY,maxY,eMinX,eMaxX,eMinY,eMaxY
    return intersect(minX,maxX,minY,maxY,eMinX,eMaxX,eMinY,eMaxY)
def entitiesToGrid(entities):
    entityDict = {}
    for loc,entity in entities:
        rLoc = getGridNum(loc)
        if rLoc not in entityDict:
            entityDict[loc] = []
        entityDict[loc].append(entity)
    return entityDict
def stateToString(state):
    str = ''
    playerChar = {"N":'^',"E":'>',"W":'<',"S":'v'}
    entities = entitiesToGrid(state["entities"])
    for y in range(state["length"]):
        for x in range(state["width"]):
            ch = '-'
            #elif (x,y) in state["entities"]:
            if (x,y) == getGridNum(state["player"]):
              ch = playerChar[state["playerDirection"]]
            elif (x,y) in entities:
              ch = entities[(x,y)][0]["asChar"]
            elif (x,y) in state["objects"]:
              obj = state["objects"][(x,y)]
              ch = obj["asChar"]
            str+=ch
        str+='\n'
    return str
def viableLoc(state,x,y,w=0,l=0):
    if (x-w/2<0 or x+w/2>=state["width"] or y-l/2<0 or y+l/2>=state["length"]):
        return False
    for object in state['objects'].values():
        if object["isSolid"] and intersectThat(x-w/2,x+w/2,y-l/2,y+l/2,object):
            return False
    for loc,entity in state['entities']:
        if entity["isSolid"] and intersectThat(x-w,x+w,y-l,y+l,entity):
            return False
    return True
def checkCollision(state,this):
    touching = []
    for that in state["objects"].values():
        if (this is not that) and (intersectThisThat(this,that)):
          touching.append(that)
    for loc,that in state["entities"]:
        if (this is not that) and (intersectThisThat(this,that)):
          touching.append(that)
    return touching
def tick(state):
    for loc,object in state["objects"].items():
        for function in object["onTick"]:
            function(state,object)
    #for i in range(len(state["entities"])):
    i = 0
    while (i<len(state["entities"])):
        entity = state["entities"][i][1]
        isDead = False
        for tickFunction in entity["onTick"]:
            if isDead: break
            #returns true if collision should be checked
            this = tickFunction(state,entity)
            if this is MOVED:
                state["entities"][i] = (entity["physLoc"],entity)
                colliding = checkCollision(state,entity)
                for colFunction in entity["onCollision"]:
                    for that in colliding:
                        thisItem = colFunction(state,entity,that)
                        if thisItem is DEAD:
                            del state['entities'][i]
                            isDead = True
                            i -=1
                            break
                    if isDead: break
            elif this is DEAD:
                del state['entities'][i]
                i -= 1
        i+=1
def playerTurn(state,direction):
    state["playerDirection"] = direction
def playerForward(state,distance):
    loc = {"N":(0,-1),"E":(1,0),"W":(-1,0),"S":(0,1)}
    dx,dy = loc[state["playerDirection"]]
    x,y = state["player"]
    nX, nY = x+dx*distance,y+dy*distance
    if(viableLoc(state,nX,nY,1,1)):
        state["player"] = (nX,nY)
def moveOrTurn(state,direction,distance = 1):
    if state["playerDirection"] != direction:
        playerTurn(state,direction)
    else:
        playerForward(state,distance)
    #print state["player"]
    return state["player"]
def shootArrow(state):
    loc = {"N":(0,-1),"E":(1,0),"W":(-1,0),"S":(0,1)}
    shape = {"N":(0.2,1.0),"E":(1.0,0.2),"W":(1.0,0.2),"S":(0.2,1.0)}
    dx,dy = loc[state["playerDirection"]]
    x,y = state["player"]
    nX, nY = x+dx,y+dy
    arrow = placeEntity(state,nX,nY,"arrowEntity")
    arrow["direction"] = state["playerDirection"]
    arrow["width"],arrow["length"] = shape[arrow["direction"]]
def shootFire(state):
    loc = {"N":(0,-1),"E":(1,0),"W":(-1,0),"S":(0,1)}
    dx,dy = loc[state["playerDirection"]]
    x,y = state["player"]
    nX, nY = x+dx,y+dy
    fire = placeEntity(state,nX,nY,"fireBallEntity")
    fire["direction"] = state["playerDirection"]
def swingSword(state):
    loc = {"N":(0,-1),"E":(1,0),"W":(-1,0),"S":(0,1)}
    dx,dy = loc[state["playerDirection"]]
    x,y = state["player"]
    nX, nY = x+dx,y+dy
    placeEntity(state,nX,nY,"swordQEntity")


#def useCurrentItem(state):
state = buildSmall()
tick(state)
print stateToString(state)
shootArrow(state)
playerTurn(state,"W")
shootArrow(state)
playerTurn(state,"S")
shootFire(state)
for i in range(3):
  #playerForward(state,1)
  tick(state)    
swingSword(state)
tick(state)
print stateToString(state)
tick(state)
print stateToString(state)
