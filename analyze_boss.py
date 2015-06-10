import generate

# Gives the total number of tiles used
# Also represents the AREA
def numTiles(monster):
    dict = {}
    #print len(monster['body']), 'is the total amount of boss tiles'
    dict['value'] = len(monster['body'])
    dict['string'] = len(monster['body']), 'is the total amount of boss tiles'
    return dict
        
# Gives the coordinate position for each tile
def posTiles(monster):
    for key in monster['body']:
        print key, 'corresponds to', monster['body'][key]
        
# Tells the amount of each tile there is on the boss
def numSpecTiles(monster):
    num_type = {}
    for type in generate.Library['Types']:
        num_type[type] = 0
    for key in monster['body']:
        num_type[monster['body'][key]] += 1
    for type in num_type:
        print 'There are', num_type[type] , 'amounts of' , type
    return num_type
 
# Prints the level of difficulty of the generated boss
# The lower score the weapon has on a tile, the less effective it is
# Therefore, the lower the score of the boss, the more difficult the boss is
# Max sword points: 100
# Max fire points: 150
# Max arrow points: 200
def difficulty(monster):    
    dict = {}
    #Difficulty for just sword
    sword_points = solve_points(monster,'sword')
    sword_total = generate.sumProp(monster, 'sword')
    sword_perc = diff_checker(sword_points, sword_total, 'sword')
    dict['sword_points'] = sword_points
    dict['sword_total'] = sword_total
    dict['sword_perc'] = sword_perc
 
    #Difficulty for just fire
    fire_points = solve_points(monster, 'fire')
    fire_total = generate.sumProp(monster, 'fire')
    fire_perc = diff_checker(fire_points, fire_total, 'fire')
    dict['fire_points'] = fire_points
    dict['fire_total'] = fire_total
    dict['fire_perc'] = fire_perc
    
    #Difficulty for just arrow
    arrow_points = solve_points(monster, 'arrow')
    arrow_total = generate.sumProp(monster, 'arrow')
    arrow_perc = diff_checker(arrow_points, arrow_total, 'arrow')
    dict['arrow_points'] = arrow_points
    dict['arrow_total'] = arrow_total
    dict['arrow_perc'] = arrow_perc
    
    return dict
    
    
def solve_points(monster, tool):
    max_point = 0
    for tile in generate.Library['Props']:
        if tool in generate.Library['Props'][tile] and generate.Library['Props'][tile][tool] > max_point:
            max_point = generate.Library['Props'][tile][tool]
    max_point *= len(monster['body'])
    # Now split the value into 3 values - Easy/Intermediate/Difficult
    d = max_point/3
    i = max_point * 2/3
    points = {}
    points['easy'] = max_point
    points['inter'] = i
    points['diff'] = d
    return points
    
def diff_checker(tool_points, tool_total, tool):
    dict = {}
    #print '0% - 33% Beatable: Difficult, 34%-66% Beatable: Intermediate, 67% - 100% Beatable: Easy'
    percent = (1.0 * tool_total)/tool_points['easy']
    percent *= 100
    dict['value'] = percent
    if(tool_total <= tool_points['diff']):
        #print 'If your only tool is a', tool,': Difficult'
        dict['string'] = 'If your only tool is a', tool,': Difficult'
    elif(tool_total > tool_points['diff'] and tool_total <= tool_points['inter']):
        #print 'If your only tool is a', tool,': Intermediate'
        dict['string'] = 'If your only tool is a', tool,': Intermediate'
    elif(tool_total > tool_points['inter'] and tool_total <= tool_points['easy']):
        #print 'If your only tool is a', tool,': Easy'
        dict['string'] = 'If your only tool is a', tool,': Easy'
    dict['string2'] = tool,' score', tool_total, 'out of', tool_points['easy'], ':', percent,'%'
    return dict
    
