# Oppgave a - Øving 3 Kongitive Arkitekturer
# 
# Ved Distance = 3.7 og Delta = 1.2 begår roboten følgene Mandami Resonering:
# 
# #1 Fuzzification:
# Distance = 3.7 gir Distance_Small = 0.6 og Distance_Perfect = 0.1.  
# Delta = 1.2 gir Delta_Stable = 0.3 og Delta_Growing = 0.4. 
# 
# #2 Rule Evaluation: 
# Since Distance_Small = 0.6 AND Delta_Growing = 0.4 then Action_None = 0.5
# Since Distance_Small = 0.6 AND Delta_Stable = 0.3 then  Action_SlowDown = 0.45
# Since Distance_Perfect = 0.1 AND Delta_Growing = 0.4 then Action_SpeedUp = 0.25
#
# #3 Aggregation of the rule outputs: 
# Action: Action_BrakeHard = 0.0, Action_SlowDown = 0.45, Action_None = 0.5, Action_SpeedUp = 0.25, Action_FloorIt = 0.0
# 
# #4 Defuzzification:
# Action_COG = (((-4)*0.45 + (0)*0.5 + (4)*0.25)/ 1.20) = -0.93
# Action_COG gives action as None.
#

# Oppgave 2

# Global distance and delta
distance = 0 
delta = 0

# Global const fuzzy categories
# Note: The graphs are a little vague on the precise boundaries of the different definitions, therefore I will do a reasonable approximation. 
# FOF 
distanceBoundaries = [(1, 2.5),(1.5, 4.5),(3.5, 6.5),(5.5, 8.5),(7.50, 9)]
deltaBoundaries = [(-5, -2.5),(-3.5, -0.5),(-1.5, 1.5),(0.5, 3.5),(2.5, 4)]
actionBoundaries = [(-8, -5),(-7, -1),(-3, 3),(1, 7),(5, 8)]

# fuzzysets

def triangle(position, x0, x1, x2, clip):
    print("triangle", position, x0, x1, x2, clip)
    value = 0
    if(position >= x0 and position <= x1):
         value = (position - x0)/(x1-x0)
    elif(position >= x1 and position <= x2):
        value = (x2 - position) / (x1 - x0)
    if(value > clip):
        value = clip
    return value

def grade(position, x0, x1, clip):
    print("grade", position, x0, x1, clip)
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
    print("reverse_grade", position, x0, x1, clip)
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
    print(boundaries, index, indexLength)
    if(index == indexLength-1):
        return grade(calcValue, boundaries[0], boundaries[1], 1)
    elif(index == 0):
        return reverse_grade(calcValue, boundaries[0], boundaries[1], 1)
    else:
        return triangle(calcValue, boundaries[0], ((boundaries[0] + boundaries[1])/2), boundaries[1], 1)
    
# cog calculation

def cog_calc():
    print("Yet to implement")

# rule sets

#TODO

# main

def main():
    global distance, delta
    try:
        distance = float(input("Please input a number for distance")) 
        delta = float(input("Please input a number for delta")) 
    except ValueError:
        print("Invalid input, please re-enter!")
    
    fuzzyDistances = []
    fuzzyDeltas = []

    for i in range(0, len(distanceBoundaries)):
        fuzzyDistances.append(fuzzification(distanceBoundaries[i], i, len(distanceBoundaries), distance)) 
    
    for i in range(0, len(deltaBoundaries)):
        fuzzyDeltas.append(fuzzification(deltaBoundaries[i], i, len(deltaBoundaries), delta)) 

    print(fuzzyDistances)
    print(fuzzyDeltas)


main()
