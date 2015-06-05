import json

import sys
from random import random, randint, choice

#with open('types.json') as f:
#  Library = json.load(f)

Library = {
  'Initial': {
    'width': 30,
    'length': 20,
    'body':{}
    },
  'Types': ["a", "b", "c", "d","f","g","h"],
  'Props': {
    "a" : {
      'sword': 2,
      'arrow': 1,
      'fire': 0
      },
    "b" : {
      'sword': 0,
      'arrow': 0,
      'fire': 3
      },
    "c" : {
      'sword': 1,
      'arrow': 1,
      'fire': 1
      },
    "d" : {
      'sword': 1,
      'arrow': 4,
      'fire': 1
      },
    "e" : {
      'sword': 2,
      'arrow': 1,
      'fire': 0
      },
    "f" : {
      'sword': 0,
      'arrow': 0,
      'fire': 3
      },
    "g" : {
      'sword': 1,
      'arrow': 1,
      'fire': 1
      },
    "h" : {
      'sword': 1,
      'arrow': 4,
      'fire': 1
      }
   }
}
def assignTile(state,loc,tile):
  state['body'][loc] = tile
  return state

def randomAssign(state):
  w = randint(0,state['width']-1)
  l = randint(0,state['length']-1)
  assignTile(state,(w,l),choice(Library['Types']))

def assign(state, w, l):
  assignTile(state,(w,l),choice(Library['Types']))

def draw(state):
  for l in range(0,state['length']):
    line = ''
    for w in range(0,state['width']):
	  if (w,l) in state['body']:
	    line+=state['body'][(w,l)]
	  else:
	    line+=' '
    print line
def sumProp(state,prop):
  sum = 0
  for tile in state['body'].values():
    if tile in Library['Props']:
	  if prop in Library['Props'][tile]:
  	    sum += Library['Props'][tile][prop]
  return sum

def createMonster(parts):
  monsterLength = parts
  monsterShape = []
  current = []
  width = Library['Initial']['width']
  length = Library['Initial']['length']
  monsterShape.insert(-1, [width/2, length/2])
  next = []
  j = 0
  for j in range(0, monsterLength - 1):
    i = 0
    for i in range(0, len(monsterShape)):
      x = monsterShape[i][0]
      y = monsterShape[i][1]
      if[x - 0, y + 1] not in monsterShape and [x - 0, y + 1] not in next: 
        if x-0 >= 0 and x-0 <= width and y+1 >= 0 and y+1 <= length:
          next.insert(-1,[x - 0, y + 1])
      if[x - 1, y - 0] not in monsterShape and [x - 1, y - 0] not in next:
        if x-1 >= 0 and x-1 <= width and y+0 >= 0 and y+0 <= length:
          next.insert(-1,[x - 1, y - 0])
      if[x - 0, y - 1] not in monsterShape and [x - 0, y - 1] not in next:
        if x-0 >= 0 and x-0 <= width and y-1 >= 0 and y-1 <= length:
          next.insert(-1,[x - 0, y - 1])
      if[x + 1, y - 0] not in monsterShape and [x + 1, y - 0] not in next:
        if x+1 >= 0 and x+1 <= width and y-0 >= 0 and y-0 <= length:
          next.insert(-1,[x + 1, y - 0])
    monsterShape.insert(-1, next.pop(randint(0, len(next) - 1)))
    del next[:]
  return monsterShape

monster = []
monster = createMonster(50)

state = Library['Initial']
for j in range(0, len(monster)):
  assign(state, monster[j][0], monster[j][1])
draw(state)

#state = Library['Initial']
#while (len(state['body'])<20):
#  randomAssign(state);
#draw(state)

#state = Library['Initial']
#for i in range(0,1000):
#  randomAssign(state);
#draw(state)
print 'sword',sumProp(state,'sword')

#state = Library['Initial']
#while (sumProp(state,'fire') < 60):
#  randomAssign(state);
#draw(state)
print 'fire',sumProp(state,'fire')
