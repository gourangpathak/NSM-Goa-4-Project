# Author : Gourang Pathak
# BTech CSE 24' @IIT Goa 
# contact : gourangp29@gmail.com
# NSM Goa 4 Project

import os
import sys
import math
import time
import numpy as np
import numpy.random as random
import pygame
from pygame.locals import *
from turtle import screensize
from model_parameters import positionmatrix, nr_persons,walls,distance_Person_to_wall,normalize,g

# a = 1
# while a <= nr_persons:
#     path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\positions'
#     file_name1 = "Person " + str(a) +".txt"
#     file_name2 = "Person " + str(a) +".txt"
        
#     with open(os.path.join(path, file_name1), 'w') as fp:
#         fp.write("Person " + str(a) + "\n")
#         fp.write("Starting Position = ")
#     a += 1

# b = 1
# while b <= nr_persons:
#     path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\time'
#     file_name1 = "Person " + str(b) +".txt"
#     file_name2 = "Person " + str(b) +".txt"
        
#     with open(os.path.join(path, file_name2), 'w') as fp:
#         fp.write("")
#     b += 1

# data_folder1 = os.path.join(os.getcwd(), 'positions')
# data_folder2 = os.path.join(os.getcwd(), 'time')

pygame.init()
pygame.font.init() 
timefont = pygame.font.SysFont('John Hubbard', 30)

""" 
Creating a screen with a room that is smaller than then screen 
"""

# Size of the screen
width = 800
height = 800  
size = width, height # Do not adjust this

# Creating screen
roomscreen = pygame.display.set_mode(size)

# Making background white and creating colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
background_color = BLACK
roomscreen.fill(background_color)
pygame.display.update()

clock = pygame.time.Clock()

class Person(object):
    def __init__(self):
        # Some general characteristics of a person
        self.PersonNumber = 0
        self.mass = 80 
        self.shoulder_radius = 20
        self.x_pos = random.uniform(100 + self.shoulder_radius, 600 - self.shoulder_radius)
        self.y_pos = random.uniform(100 + self.shoulder_radius,700 - self.shoulder_radius)
        self.pos = np.array([self.x_pos, self.y_pos])

        # Actual Velocities & directions 
        self.Vi_x = random.uniform(0,1.6)
        self.Vi_y = random.uniform(0,1.6)
        self.Vi = np.array([self.Vi_x, self.Vi_y])
        self.doorcenter = np.array([700,400])
        self.dir = normalize(self.doorcenter - self.pos)
        
        # Desired Velocity
        self.Si_0 = 12
        self.Vi_0 = self.Si_0*self.dir
        self.tau = 0.25 
        self.acceleration = (self.Vi_0 - self.Vi)/self.tau
        self.k = 120000
        self.A_i = 2000
        self.B_i = 0.08*50  
        # reached_door property of Person class represents if door is reached or not
        self.reached_door = 0 
        self.time = 0.0
        self.collisions = 0
    
    def acceleration_term(self): 
        dV = self.Vi_0 - self.Vi
        # if dV ~ 0 then I set dV = 0
        return dV*self.mass/self.tau
    
    
    def f_ij(self, otherperson): 
        r_ij = self.shoulder_radius + otherperson.shoulder_radius
        d_ij = np.linalg.norm(self.pos - otherperson.pos)
        n_ij = (self.pos - otherperson.pos)/d_ij
        total = self.A_i*np.exp((r_ij-d_ij)/(self.B_i))*n_ij + self.k*g(r_ij-d_ij)*n_ij
        
        if d_ij <= r_ij:
            self.collisions += 1
            
        return total
    
    def f_iW(self, wall): 
        r_i = self.shoulder_radius
        d_iW,n_iW = distance_Person_to_wall(self.pos,wall)
        total = -self.A_i*np.exp((r_i-d_iW)/self.B_i)*n_iW + self.k*g(r_i-d_iW)*n_iW
        return total

def main():
    # Now to let multiple objects move to the door we define
    # nr_Persons = nr_Persons
    Person_color = RED
    wall_color = WHITE
    
    
    """ 
    
    Now we need to create the doors through which objects will leave in case of evacuation
    This door's position can be determined using:
    
    """
    
    # initialize Persons
    Persons = []
    
    # initialize the persons and their positions
    def positions(Persons):
        for i in range(nr_persons):
            person = Person()
            person.PersonNumber = i+1
            person.walls = walls
            person.x_pos = positionmatrix[i][0]
            person.y_pos = positionmatrix[i][1]
            person.pos = np.array([person.x_pos, person.y_pos])
            person.shoulder_radius = positionmatrix[i][2]
            person.mass = positionmatrix[i][3]
            person.Si_0 = positionmatrix[i][4]
            Persons.append(person)
        
    # call the positions method to initialize the people
    positions(Persons)    
    
    # count to loop over our persons
    count = 0
    start_time = time.time()
    run = True
    

    while run:
        
        # Updating time
        if count < nr_persons - 2:
            current_time = time.time()
            elapsed_time = current_time - start_time
        else:
            for P_i in Persons:
                Persons.remove(P_i)
        
        # Finding B_i t for this frame
        dt = clock.tick(70)/1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (x_pos, y_pos) = pygame.mouse.get_pos()
                print(x_pos, y_pos)
        
        roomscreen.fill(background_color)
        
        # draw walls
        for wall in walls:
            start_posw = np.array([wall[0],wall[1]])
            end_posw = np.array([wall[2],wall[3]])
            start_posx = start_posw 
            end_posx = end_posw
            pygame.draw.line(roomscreen, wall_color, start_posx, end_posx, 3)
        
        for P_i in Persons:
            P_i.dir = normalize(P_i.doorcenter - P_i.pos)
            P_i.Vi_0 = P_i.Si_0*P_i.dir
            aVelocity_force = P_i.acceleration_term()
            people_interaction = 0.0
            wall_interaction = 0.0
        
            for P_j in Persons: 
                if P_i == P_j: continue
                people_interaction += P_i.f_ij(P_j)
        
            for wall in walls:
                wall_interaction += P_i.f_iW(wall)
            
            sumForce = aVelocity_force + people_interaction + wall_interaction
            dv_dt = sumForce/P_i.mass
            P_i.Vi = P_i.Vi + dv_dt*dt 
            P_i.pos = P_i.pos + P_i.Vi*dt

            # path = str("positions/Person " + str(P_i.PersonNumber)+".txt")
            # f = open(path, "a")
            # f.write("("+str(P_i.pos[0])+","+str(P_i.pos[1])+ ")\n")
            # f.close();

            # Avoiding disappearing Persons   
            if P_i.pos[0] > 750 or P_i.pos[0] < 50 or P_i.pos[1] > 750 or P_i.pos[1] < 50:
                main()
                sys.exit()
            
            P_i.time += clock.get_time()/1000 
        
            if int(P_i.pos[0]) >= 699 and P_i.reached_door == 0:
                P_i.reached_door = 1
                # path = str("time/Person " + str(P_i.PersonNumber)+".txt")
                # f = open(path, "a")
                # f.write('Time to Reach the reached_door by person '+ str(P_i.PersonNumber) + " = " + str(P_i.time) + " seconds\n")
                # f.close()
            
            if int(P_i.pos[0]) > 699 or int(P_i.pos[0]) < 100:
                count += 1
                Persons.remove(P_i)
            
            pygame.draw.circle(roomscreen, Person_color, P_i.pos, round(P_i.shoulder_radius), 3)
        
        # Present text on screen
        timestr = "Timer : " +  str(elapsed_time)
        timesurface = timefont.render(timestr, False, (255, 255, 255))
        roomscreen.blit(timesurface,(250,80))

        # Update the screen
        pygame.display.flip()
        
    pygame.quit()
main()

