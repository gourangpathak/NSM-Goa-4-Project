# Importing packages
# from additional_functions import *
import numpy as np
import math
import numpy.random as random
# Setting seed
random.seed(123)
# Creating a dataset
nr_agents = 90

# Walls list to check
room_height = 600 # height of the room
room_width = 600 # width of the room
room_left = 100 # left pixels coordinate
room_top = 100 # top pixels coordeinate

# Door 
door_ytop = 382
door_ybottom = 418
    
def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):
    return np.max(x, 0)   

def distance_agent_to_wall(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    ymp0 = point-p0
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        cross = p0 + t*d
    elif t >= 1.0:
        ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        cross = p0 + t*d
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    return dist,npw

walls = [[room_left, room_top, room_left + room_width, room_top], 
[room_left, room_top+room_height, room_left, room_top], 
[room_left, room_top+room_height, room_left + room_width, room_top+ room_height],
[room_left + room_width, room_top, room_left + room_width, door_ytop],
[room_left+room_width, room_top + room_height, room_left + room_width, door_ybottom]]

# List to save positions
positionmatrix = []
# For all experiments
# for j in range(0,nr_experiments):
# nr_experiment = j + 1
agents_found = 0 
for i in range(0,nr_agents): # For all objects   
    # We start by finding a random position in the room which satisfies our requirements
    found = False
    countwall = 0
    while found == False:
        countwall = 0 
        desiredS =  20 # it is the desired velocity
        mass = 80 #np.random.uniform(60,100) 
        radius = 12/80 * mass # shoulder radius
        object_x = np.random.uniform(100,700) # random x coordinate in room
        object_y = np.random.uniform(100,700) # random y coordinate in room
        for wall in walls:
            r_i = radius
            d_iw,e_iw = distance_agent_to_wall(np.array([object_x, object_y]),wall)
            '''
            here for each wall we are calculating the distance between the wall and
            the person if the distance between the wall and the person is less than the
            shoulder radius of the person we increment our countwall (i.e. storing the
            number of times wall has been encountered)
            '''
            if d_iw < r_i:
                countwall += 1
        
        # if there are some positions initialized
        if len([positionmatrix[i] for i in range(0, agents_found)]) > 0:
            '''
            The countagents variable will count how many persons found so far
            are valid i.e. for all other persons shoulders the sum of their shoulder
            radius and that of our current person which we are looking for should be less
            than the distance between the 2 persons
            '''
            countagents = 0 
            # loop over other people
            for position in [positionmatrix[i] for i in range(0, agents_found)]:
                # find out the distance between others and our current person
                dist = math.sqrt((position[0]-object_x)**2 + (position[1]-object_y)**2)
                # if valid (i.e. for all other persons shoulders the sum of their shoulder
                # radius and that of our current person which we are looking for should be less
                # than the distance between the 2 persons) then increment person count
                if dist > position[2] + radius: 
                    countagents += 1
            # If the number of persons found so far which are valid is equal to the 
            if countagents == i and countwall == 0:
                found = True
                agents_found += 1 
        # if none of the positions are initialized & the wall interaction = 0 then just 
        # increment the number of persons found
        elif countwall == 0:
            found = True
            agents_found += 1 

    positionmatrix.append([object_x, object_y, radius, mass, desiredS])
