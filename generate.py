import json

import sys
from random import random, randint, choice

#with open('types.json') as f:
#  Library = json.load(f)

Library = {
  'Initial': {
    'width': 20,
    'length': 10,
    'body':{}
    },
  'Types': ["a", "b", "c", "d","f","g","h","i","j","k","l"],
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

monsterLength = 20
monsterShape = []
current = []
monsterShape.insert(-1,[Library['Initial']['width']/2, Library['Initial']['length']/2])
next = []
x = 0
for x in range(0, monsterLength):
  i = 0
  for i in range(0, len(monsterShape)):
    if[monsterShape[i][0] - 0, monsterShape[i][1] + 1] not in monsterShape:
      next.insert(-1,[monsterShape[i][0] - 0, monsterShape[i][1] + 1])
    if[monsterShape[i][0] - 1, monsterShape[i][1] - 0] not in monsterShape:
      next.insert(-1,[monsterShape[i][0] - 1, monsterShape[i][1] - 0])
    if[monsterShape[i][0] - 0, monsterShape[i][1] - 1] not in monsterShape:
      next.insert(-1,[monsterShape[i][0] - 0, monsterShape[i][1] - 1])
    if[monsterShape[i][0] + 1, monsterShape[i][1] - 0] not in monsterShape:
      next.insert(-1,[monsterShape[i][0] + 1, monsterShape[i][1] - 0])
  monsterShape.insert(-1, next.pop(randint(0, len(next) - 1)))
  del next[:]

#print monsterShape

state = Library['Initial']
for j in range(0, len(monsterShape)):
  assign(state, monsterShape[j][0], monsterShape[j][1])
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
