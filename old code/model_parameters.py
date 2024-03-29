import math
import numpy as np
import numpy.random as random
# Number of People
N = 90

# Walls list to check
room_height = 600 # height of the room
room_width = 600 # width of the room
room_left = 100 # left pixels coordinate
room_top = 100 # top pixels coordeinate

# Door 
door_ytop = 380
door_ybottom = 420
    
# Assigning Random Seed Value
random.seed(123)

def normalize(v):
    norm=np.linalg.norm(v)
    if norm != 0:
       return v/norm
    return v

def g(x):
    return np.max(x, 0)   

def wall_distance(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    r0 = point-p0
    proj = np.dot(d,r0)/np.dot(d,d)
    if proj <= 0.0:
        distance = np.sqrt(np.dot(r0,r0))
        proj_coordinate = p0 + proj*d
    elif proj >= 1.0:
        r1 = point-p1
        distance = np.sqrt(np.dot(r1,r1))
        proj_coordinate = p0 + proj*d
    else:
        proj_coordinate = p0 + proj*d
        distance = np.linalg.norm(proj_coordinate-point)
    direction = normalize(proj_coordinate-point)
    tangentWall = [-direction[1], direction[0]]
    return distance,direction,tangentWall

walls = [[room_left, room_top, room_left + room_width, room_top], 
[room_left, room_top+room_height, room_left, room_top], 
[room_left, room_top+room_height, room_left + room_width, room_top+ room_height],
[room_left + room_width, room_top, room_left + room_width, door_ytop],
[room_left+room_width, room_top + room_height, room_left + room_width, door_ybottom]]

# list to store all the locations
locations = []
persons_found = 0 
for i in range(0,N):   
    # We start by finding a random position in the room which satisfies our requirements
    found = False
    wall_collision = 0
    while found != True:
        wall_collision = 0 
        desiredSpeed =  20 # it is the desired velocity
        mass = 80
        shoulder_radius = 12/80 * mass # shoulder shoulder_radius
        x = np.random.uniform(100,700) # random x coordinate in room
        y = np.random.uniform(100,700) # random y coordinate in room
        for wall in walls:
            r_i = shoulder_radius
            d_iW,n_iW,t_iW = wall_distance(np.array([x, y]),wall)
            '''
            Here for each wall we are calculating the distance between the wall and
            the person if the distance between the wall and the person is less than the
            shoulder shoulder_radius of the person we increment our wall_collision (i.e. storing the
            number of times wall has been encountered)
            '''
            if d_iW < r_i:
                wall_collision += 1
        
        # if there are some positions initialized
        if len([locations[i] for i in range(0, persons_found)]) > 0:
            '''
                The count_persons variable will count how many persons found so far
                are valid i.e. for all other persons shoulders the sum of their shoulder
                shoulder_radius and that of our current person which we are looking for should be less
                than the distance between the 2 persons
            '''
            count_persons = 0 
            # loop over other people
            for position in [locations[i] for i in range(0, persons_found)]:
                # find out the distance between others and our current person
                distance = math.sqrt((position[0]-x)**2 + (position[1]-y)**2)
                '''
                    If valid (i.e. for all other persons shoulders the sum of their shoulder
                    shoulder_radius and that of our current person which we are looking for should be less
                    than the distance between the 2 persons) then increment person count
                '''
                
                if distance > position[2] + shoulder_radius: 
                    count_persons += 1
            # If the number of persons found so far which are valid is equal to the current size of the pool of people
            if count_persons == i and wall_collision == 0:
                found = True
                persons_found += 1 
            '''
                if none of the positions are initialized & the wall interaction = 0 then just 
                increment the number of persons found
            '''
        
        elif wall_collision == 0:
            found = True
            persons_found += 1 

    locations.append([x, y, shoulder_radius, mass, desiredSpeed])
