import os
import sys
import math
import time
import pygame
import numpy as np
import numpy.random as random
from pygame.locals import *
from turtle import screensize
from model_parameters import locations, N, walls, wall_distance, normalize, g

# a = 1 
# while a <= N:
#     path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\positions'
#     file_name = "Person " + str(a) +".txt"
        
#     with open(os.path.join(path, file_name), 'w') as fp:
#         fp.write("Person " + str(a) + "\n")
#         fp.write("Starting Position = ")
#     a += 1

# b = 1
# while b <= N:
#     path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\time'
#     file_name = "Person " + str(b) +".txt"
        
#     with open(os.path.join(path, file_name), 'w') as fp:
#         fp.write("")
#     b += 1

# c = 1
# while c <= N:
#     path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\velocity'
#     file_name = "Person " + str(c) +".txt"
        
#     with open(os.path.join(path, file_name), 'w') as fp:
#         fp.write("Person " + str(a) + "\n")
#         fp.write("Starting Actual Velocity = ")
#     c += 1

pygame.init()
pygame.font.init() 
timefont = pygame.font.SysFont('Arial', 30)

""" 
Creating a screen with a room that is smaller than then screen 
"""

# Size of the screen
screenwidth = 800
screenheight = 800  
size = screenwidth, screenheight

# Creating screen
roomscreen = pygame.display.set_mode(size)

# Making background white and creating colors
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
background_color = BLACK
roomscreen.fill(background_color)
pygame.display.update()

# Defining clock
clock = pygame.time.Clock()

# Making a Person Class
class Person(object):
    def __init__(self):
        self.personNumber = 0
        self.mass = 80 
        self.shoulder_radius = 20
        
        self.x = random.uniform(100 + self.shoulder_radius, 600 - self.shoulder_radius)
        self.y = random.uniform(100 + self.shoulder_radius,700 - self.shoulder_radius)
        self.pos = np.array([self.x, self.y])
    
        self.actual_X = 0 
        self.actual_Y = 0 
        self.actual_V = np.array([self.actual_X, self.actual_Y])
    
        self.door_center = np.array([700,400])
        self.dir = normalize(self.door_center - self.pos)
        
        self.desiredSpeed = 12
        self.desired_V = self.desiredSpeed*self.dir
        
        self.tau = 0.25
        self.acclrn = (self.desired_V - self.actual_V)/self.tau
              
        
        self.K = 120000
        self.A_i = 2000
        self.B_i = 0.08*50

        # this represents if door is reached or not
        self.door_reached = 0 
        self.time = 0.0
        self.collisions = 0

    # to calculate the 1st term	
    def acceleration_term(self):
        dV = self.desired_V - self.actual_V
        if np.allclose(dV, np.zeros(2)):
            dV = np.zeros(2)
        return dV*self.mass/self.tau
    
    # interaction with people
    def f_ij(self, other): 
        d_ij = np.linalg.norm(self.pos - other.pos)
        r_ij = self.shoulder_radius + other.shoulder_radius
        n_ij = (self.pos - other.pos)/d_ij
        total = self.A_i*np.exp((r_ij-d_ij)/(self.B_i))*n_ij
        + self.K*g(r_ij-d_ij)*n_ij
        
        if d_ij <= r_ij:
            self.collisions += 1
            
        return total
    
    def f_iW(self, wall): # interaction with the wall in the room
        d_iW,n_iW = wall_distance(self.pos,wall)
        r_i = self.shoulder_radius
        total = -self.A_i*np.exp((r_i-d_iW)/self.B_i)*n_iW 
        + self.K*g(r_i-d_iW)*n_iW
        return total

def main():
    person_color = RED
    wall_color = WHITE
    
    # initialize persons
    persons = []
    
    # initialize the persons and their positions
    def positions(persons):
        for i in range(N):
            person = Person()
            person.personNumber = i+1
            person.walls = walls
            person.x = locations[i][0]
            person.y = locations[i][1]
            person.pos = np.array([person.x, person.y])
            person.shoulder_radius = locations[i][2]
            person.mass = locations[i][3]
            person.desiredSpeed = locations[i][4]
            persons.append(person)
        
    # call the positions method
    positions(persons)    
    
    # count to loop over our persons
    count = 0
    start_time = time.time()
    run = True
    

    while run:
        
        # Updating time
        if count < N - 2:
            current_time = time.time()
            time_taken = current_time - start_time
        else:
            for P_i in persons:
                persons.remove(P_i)

        dt = clock.tick(70)/1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                print(x, y)
        
        roomscreen.fill(background_color)
        
        # draw walls
        for wall in walls:
            start_posw = np.array([wall[0],wall[1]])
            end_posw = np.array([wall[2],wall[3]])
            start_posx = start_posw 
            end_posx = end_posw
            pygame.draw.line(roomscreen, wall_color, start_posx, end_posx, 3)
        
        for P_i in persons:
            P_i.dir = normalize(P_i.door_center - P_i.pos)
            P_i.desired_V = P_i.desiredSpeed*P_i.dir
            term_1 = P_i.acceleration_term()
            people_Force = 0.0
            wall_Force = 0.0
        
            for P_j in persons: 
                if P_i == P_j: continue
                people_Force += P_i.f_ij(P_j)
        
            for wall in walls:
             wall_Force += P_i.f_iW(wall)
            
            total_Force = term_1 + people_Force + wall_Force
            acc = total_Force/P_i.mass
            P_i.actual_V = P_i.actual_V + acc*dt 
            P_i.pos = P_i.pos + P_i.actual_V*dt

            # path = str("positions/Person " + str(P_i.personNumber)+".txt")
            # f = open(path, "a")
            # f.write("("+str(P_i.pos[0])+","+str(P_i.pos[1])+ ")\n")
            # f.close()

            # path = str("velocity/Person " + str(P_i.personNumber)+".txt")
            # f = open(path, "a")
            # f.write(str(P_i.actual_V)+"\n")
            # f.close()

            # Avoiding disappearing persons   
            if P_i.pos[0] > 750 or P_i.pos[0] < 50 or P_i.pos[1] > 750 or P_i.pos[1] < 50:
                main()
                sys.exit()
            
            P_i.time += clock.get_time()/1000 
        
            if int(P_i.pos[0]) >= 699 and P_i.door_reached == 0:
                P_i.door_reached = 1
                # path = str("time/Person " + str(P_i.personNumber)+".txt")
                # f = open(path, "a")
                # f.write('Time to Reach the door_reached by person '+ str(P_i.personNumber) + " = " + str(P_i.time) + " seconds\n")
                # f.close()
            
            if int(P_i.pos[0]) > 699 or int(P_i.pos[0]) < 100:
                count += 1
                persons.remove(P_i)
            
            pygame.draw.circle(roomscreen, person_color, P_i.pos, round(P_i.shoulder_radius), 3)
        
        # Present text on screen
        timestr = "Timer : " +  str(time_taken)
        timesurface = timefont.render(timestr, False, (255, 255, 255))
        roomscreen.blit(timesurface,(250,50))

        # Update the screen
        pygame.display.flip()
        
    pygame.quit()
main()

