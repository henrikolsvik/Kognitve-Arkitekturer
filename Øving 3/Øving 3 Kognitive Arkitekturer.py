# Oppgave a - Øving 3 Kongitive Arkitekturer
# 
# Ved Distance = 3.7 og Delta = 1.2 begår roboten følgene Mandami Resonering:
# 
# #1 Fuzzification:
# Distance = 3.7 gir Distance_Small = 0.6 og Distance_Perfect = 0.1.  
# Delta = 1.2 gir Delta_Stable = 0.3 og Delta_Growing = 0.4. 
# 
# #2 Rule Evaluation: 
# Since Distance_Small = 0.6 AND Delta_Growing = 0.4 then Action_None = 0.4
# Since Distance_Small = 0.6 AND Delta_Stable = 0.3 then  Action_SlowDown = 0.3
# Since Distance_Perfect = 0.1 AND Delta_Growing = 0.4 then Action_SpeedUp = 0.1
#
# #3 Aggregation of the rule outputs: 
# Action: Action_BrakeHard = 0.0, Action_SlowDown = 0.3, Action_None = 0.4, Action_SpeedUp = 0.1, Action_FloorIt = 0.0
# 
# #4 Defuzzification:
# Action_COG = (((-4)*0.3 + (0)*0.4 + (4)*0.1)/ 0.8) = -1
# Action_COG gives action as None.
#

# Oppgave b

# Global distance and delta
distance = 0 
delta = 0

# Global const fuzzy categories
# Note: The graphs are a little vague on the precise boundaries of the different definitions, therefore I will do a reasonable approximation. 
# FOF 
distanceBoundaries = [(1, 2.5),(1.5, 4.5),(3.5, 6.5),(5.5, 8.5),(7.50, 9)]
deltaBoundaries = [(-5, -2.5),(-3.5, -0.5),(-1.5, 1.5),(0.5, 3.5),(2.5, 4)]
actionBoundaries = [(-8, -5, "ＡＣＴＩＯＮ:　「ＢＲＡＫＥ　ＨＡＲＤ」"),(-7, -1, "ＡＣＴＩＯＮ:　「ＳＬＯＷ　ＤＯＷＮ」"),(-3, 3, "ＡＣＴＩＯＮ:　「ＮＯＮＥ」"),(1, 7, "ＡＣＴＩＯＮ:　「ＳＰＥＥＤ　ＵＰ」"),(5, 8, "ＡＣＴＩＯＮ:　「ＦＬＯＯＲ　ＩＴ」")]
aWP = [-8.25, -4, 0, 4, 8.25]

# fuzzysets

import time

def triangle(position, x0, x1, x2, clip):
    value = 0
    if(position >= x0 and position <= x1):
         value = (position - x0)/(x1-x0)
    elif(position >= x1 and position <= x2):
        value = (x2 - position) / (x1 - x0)
    if(value > clip):
        value = clip
    return value

def grade(position, x0, x1, clip):
    value = 0
    if(position >= x1):
        value = 1
    elif(position <= x0):
        value = 0
    else:
        value = (position - x0)/(x1 - x0)
    if(value > clip):
        value = clip
    return value

def reverse_grade(position, x0, x1, clip):
    value = 0
    if(position <= x0):
        value = 1
    elif(position >= x1):
        value = 0
    else:
        value = (x1- position)/(x1 - x0)
    if(value > clip):
        value = clip
    return value

def fuzzification(boundaries, index, indexLength, calcValue):
    if(index == indexLength-1):
        return grade(calcValue, boundaries[0], boundaries[1], 1)
    elif(index == 0):
        return reverse_grade(calcValue, boundaries[0], boundaries[1], 1)
    else:
        return triangle(calcValue, boundaries[0], ((boundaries[0] + boundaries[1])/2), boundaries[1], 1)
    
def defuzzification(cog, set):
    defuzzifiedValues = []
    for i in range(0, len(set)):
        defuzzifiedValues.append(fuzzification(set[i], i, len(set), cog))
    return set[defuzzifiedValues.index(max(defuzzifiedValues))][2]



# cog calculation

def cog_calc_action(fuzzySet):
    #tilnermet integrasjon
    weight = 0
    for x in range(0, len(aWP)):
        weight += fuzzySet[x]*aWP[x]
    try:    
        return ( weight / sum(fuzzySet))
    except ZeroDivisionError: 
        return 0

# rule sets

#TODO

def rule_evaluation(fuzzyDistances, fuzzyDeltas):
    fuzzyActions = []
    print("「Ｅｖａｌｕａｔｉｎｇ　Ｒｕｌｅｓ！」")
    fuzzyActions.append(fuzzyDistances[0]) #IF	distance	is	VerySmall	THEN	action	is	BrakeHard
    fuzzyActions.append(min(fuzzyDistances[1], fuzzyDeltas[2])) #IF	distance	is	Small	AND	delta	is	Stable	THEN	action	is	SlowDown
    fuzzyActions.append(min(fuzzyDistances[1], fuzzyDeltas[3])) #IF	distance	is	Small	AND	delta	is	Growing	THEN	action	is	None
    fuzzyActions.append(min(fuzzyDistances[2], fuzzyDeltas[3])) #IF	distance	is	Perfect	AND	delta	is	Growing	THEN	action	is	SpeedUp
    fuzzyActions.append(min(fuzzyDistances[4], 1 - (max((fuzzyDeltas[3]), (fuzzyDeltas[4]))))) #IF	distance	is	VeryBig	AND	(delta	is	NOT	Growing	OR	delta	is	NOT	GrowingFast) THEN	action	is	 FloorIt
    return fuzzyActions

def main():
    global distance, delta
    try:
        distance = float(input("Please input a number for 「distance」 ")) 
        delta = float(input("Please input a number for 「delta」 ")) 
    except ValueError:
        print("Invalid input, please re-enter!")
        main()
    
    fuzzyDistances = []
    fuzzyDeltas = []

    for i in range(0, len(distanceBoundaries)):
        fuzzyDistances.append(fuzzification(distanceBoundaries[i], i, len(distanceBoundaries), distance)) 
    
    for i in range(0, len(deltaBoundaries)):
        fuzzyDeltas.append(fuzzification(deltaBoundaries[i], i, len(deltaBoundaries), delta)) 

    print(defuzzification(cog_calc_action(rule_evaluation(fuzzyDistances, fuzzyDeltas)), actionBoundaries))
    print("\n")
    main()

main()