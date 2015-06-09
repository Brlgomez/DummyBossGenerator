from generate import *

# Gives the total number of tiles used
# Also represents the AREA
def numTiles():
    print len(monster['body']), 'is the total amount of boss tiles'
        
# Gives the coordinate position for each tile
def posTiles():
    for key in monster['body']:
        print key, 'corresponds to', monster['body'][key]
        
# Tells the amount of each tile there is on the boss
def numSpecTiles():
    num_type = {}
    for type in Library['Types']:
        num_type[type] = 0
    for key in monster['body']:
        num_type[monster['body'][key]] += 1
    for type in num_type:
        print 'There are', num_type[type] , 'amounts of' , type
 
# Prints the level of difficulty of the generated boss
# The lower score the weapon has on a tile, the less effective it is
# Therefore, the lower the score of the boss, the more difficult the boss is
# Max sword points: 100
# Max fire points: 150
# Max arrow points: 200
def difficulty():    
    #Difficulty for just sword
    # If we have several tools, I will make another generic tool function
    # To calculate this
    sword_points = solve_points('sword')
    sword_total = sumProp(monster, 'sword')
    if(sword_total <= sword_points['diff']):
        print 'If your only tool is a sword: Difficult'
    elif(sword_total > sword_points['diff'] and sword_total <= sword_points['inter']):
        print 'If your only tool is a sword: Intermediate'
    elif(sword_total > sword_points['inter'] and sword_total <= sword_points['easy']):
        print 'If your only tool is a sword: Easy'
    print 'Sword score', sword_total
 
    #Difficulty for just fire
    fire_points = solve_points('fire')
    fire_total = sumProp(monster, 'fire')
    if(fire_total <= fire_points['diff']):
        print 'If your only tool is a fire: Difficult'
    elif(fire_total > fire_points['diff'] and fire_total <= fire_points['inter']):
        print 'If your only tool is a fire: Intermediate'
    elif(fire_total > fire_points['inter'] and fire_total <= fire_points['easy']):
        print 'If your only tool is a fire: Easy'
    print 'fire score', fire_total

    #Difficulty for just arrow
    arrow_points = solve_points('arrow')
    arrow_total = sumProp(monster, 'arrow')
    if(arrow_total <= arrow_points['diff']):
        print 'If your only tool is a arrow: Difficult'
    elif(arrow_total > arrow_points['diff'] and arrow_total <= arrow_points['inter']):
        print 'If your only tool is a arrow: Intermediate'
    elif(arrow_total > arrow_points['inter'] and arrow_total <= arrow_points['easy']):
        print 'If your only tool is a arrow: Easy'
    print 'arrow score', arrow_total    
    
    
def solve_points(tool):
    max_point = 0
    for tile in Library['Props']:
        if tool in Library['Props'][tile] and Library['Props'][tile][tool] > max_point:
            max_point = Library['Props'][tile][tool]
    max_point *= len(monster['body'])
    # Now split the value into 3 values - Easy/Intermediate/Difficult
    d = max_point/3
    i = max_point * 2/3
    points = {}
    points['easy'] = max_point
    points['inter'] = i
    points['diff'] = d
    return points
    
difficulty()

#numTiles()
#posTiles()
#numSpecTiles()
