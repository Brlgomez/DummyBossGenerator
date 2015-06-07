from generate import *

# Gives the total number of tiles used
# Also represents the AREA
def numTiles():
    total_tiles = 0
    for key in state['body']:
        total_tiles += 1
    print total_tiles, 'is the total amount of boss tiles'
        
# Gives the coordinate position for each tile
def posTiles():
    for key in state['body']:
        print key, 'corresponds to', state['body'][key]
        
numTiles()
