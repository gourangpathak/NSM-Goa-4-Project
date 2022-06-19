# Programming evacuation systems using Crowd Simulation
# Agent-Based Modelling
# Loading the pygame package
from turtle import screensize
import pygame
# Importing locals
from pygame.locals import *
# Other packages
import sys
import numpy as np
import numpy.random as random
import math
import time
import os
from model_parameters import positionmatrix,nr_agents,walls,distance_agent_to_wall,normalize,g

a = 1
while a <= nr_agents:
    path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\positions'
    file_name1 = "Person " + str(a) +".txt"
    file_name2 = "Person " + str(a) +".txt"
        
    with open(os.path.join(path, file_name1), 'w') as fp:
        fp.write("Person " + str(a) + "\n")
        fp.write("Starting Position = ")
    a += 1

b = 1
while b <= nr_agents:
    path = r'C:\\Users\\Gourang Pathak\\Desktop\\Gourang\\NSM-Goa-4-Project\\time'
    file_name1 = "Person " + str(b) +".txt"
    file_name2 = "Person " + str(b) +".txt"
        
    with open(os.path.join(path, file_name2), 'w') as fp:
        fp.write("")
    b += 1

data_folder1 = os.path.join(os.getcwd(), 'positions')
data_folder2 = os.path.join(os.getcwd(), 'time')

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

# Defining clock
clock = pygame.time.Clock()

# Creating evacuation object class
class Agent(object):
    def __init__(self):
        self.agentNumber = 0
        self.mass = 80 # random.uniform(40,90)
        self.radius = 20
        # random initialize a agent
        
        self.x = random.uniform(100 + self.radius, 600 - self.radius)
        self.y = random.uniform(100 + self.radius,700 - self.radius)
        self.pos = np.array([self.x, self.y])
        #self.pos = np.array([10.0, 10.0])
    
        self.aVelocityX = 0 #random.uniform(0,1.6)
        self.aVelocityY = 0 #random.uniform(0,1.6)
        self.aVelocity = np.array([self.aVelocityX, self.aVelocityY])
        #self.actualV = np.array([0.0, 0.0])
    
        # self.dest = np.array([random.uniform(100,700),random.uniform(100,700)])
        self.dest = np.array([700,400])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])
        
        self.dSpeed = 12
        self.dVelocity = self.dSpeed*self.direction
        
        self.acclTime = 0.25 #random.uniform(8,16) #10.0
        self.drivenAcc = (self.dVelocity - self.aVelocity)/self.acclTime
              
        
        self.bodyFactor = 120000
        self.F = 2000
        self.delta = 0.08*50  #random.uniform(0.8,1.6) #0.8 #0.08
        
        self.Goal = 0 # this represents if door is reached or not
        self.time = 0.0
        self.countcollision = 0
    	
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
        
    def velocity_force(self): # function to adapt velocity
        deltaV = self.dVelocity - self.aVelocity
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.acclTime
    
    
    def f_ij(self, other): # interaction with people
        r_ij = self.radius + other.radius
        d_ij = np.linalg.norm(self.pos - other.pos)
        e_ij = (self.pos - other.pos)/d_ij
        value = self.F*np.exp((r_ij-d_ij)/(self.delta))*e_ij
        + self.bodyFactor*g(r_ij-d_ij)*e_ij
        
        if d_ij <= r_ij:
            self.countcollision += 1
            
        return value
    
    def f_ik_wall(self, wall): # interaction with the wall in the room
        r_i = self.radius
        d_iw,e_iw = distance_agent_to_wall(self.pos,wall)
        value = -self.F*np.exp((r_i-d_iw)/self.delta)*e_iw # Assume wall and people give same force
        + self.bodyFactor*g(r_i-d_iw)*e_iw
        return value

def main():
    # Now to let multiple objects move to the door we define
    # nr_agents = nr_agents
    agent_color = RED
    line_color = WHITE
    
    
    """ 
    
    Now we need to create the doors through which objects will leave in case of evacuation
    This door's position can be determined using:
    
    """
    
    # initialize agents
    agents = []
    
    # initialize the persons and their positions
    def positions(agents):
        for i in range(nr_agents):
            agent = Agent()
            agent.agentNumber = i+1
            agent.walls = walls
            agent.x = positionmatrix[i][0]
            agent.y = positionmatrix[i][1]
            agent.pos = np.array([agent.x, agent.y])
            agent.radius = positionmatrix[i][2]
            agent.mass = positionmatrix[i][3]
            agent.dSpeed = positionmatrix[i][4]
            agents.append(agent)
        
    # call the positions method
    positions(agents)    
    
    # count to loop over our persons
    count = 0
    start_time = time.time()
    run = True
    

    while run:
        
        # Updating time
        if count < nr_agents - 2:
            current_time = time.time()
            elapsed_time = current_time - start_time
        else:
            for agent_i in agents:
                agents.remove(agent_i)
        
        # Finding delta t for this frame
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
            pygame.draw.line(roomscreen, line_color, start_posx, end_posx, 3)
        
        for agent_i in agents:
            agent_i.direction = normalize(agent_i.dest - agent_i.pos)
            agent_i.dVelocity = agent_i.dSpeed*agent_i.direction
            aVelocity_force = agent_i.velocity_force()
            people_interaction = 0.0
            wall_interaction = 0.0
        
            for agent_j in agents: 
                if agent_i == agent_j: continue
                people_interaction += agent_i.f_ij(agent_j)
        
            for wall in walls:
                wall_interaction += agent_i.f_ik_wall(wall)
            
            sumForce = aVelocity_force + people_interaction + wall_interaction
            dv_dt = sumForce/agent_i.mass
            agent_i.aVelocity = agent_i.aVelocity + dv_dt*dt 
            agent_i.pos = agent_i.pos + agent_i.aVelocity*dt

            path = str("positions/Person " + str(agent_i.agentNumber)+".txt")
            f = open(path, "a")
            f.write("("+str(agent_i.pos[0])+","+str(agent_i.pos[1])+ ")\n")
            f.close()

            # Avoiding disappearing agents   
            if agent_i.pos[0] > 750 or agent_i.pos[0] < 50 or agent_i.pos[1] > 750 or agent_i.pos[1] < 50:
                main()
                sys.exit()
            
            agent_i.time += clock.get_time()/1000 
        
            if int(agent_i.pos[0]) >= 699 and agent_i.Goal == 0:
                agent_i.Goal = 1
                path = str("time/Person " + str(agent_i.agentNumber)+".txt")
                f = open(path, "a")
                f.write('Time to Reach the Goal by person '+ str(agent_i.agentNumber) + " = " + str(agent_i.time) + " seconds\n")
                f.close()
            
            if int(agent_i.pos[0]) > 699 or int(agent_i.pos[0]) < 100:
                count += 1
                agents.remove(agent_i)
            
            pygame.draw.circle(roomscreen, agent_color, agent_i.pos, round(agent_i.radius), 3)
        
        # Present text on screen
        timestr = "Timer : " +  str(elapsed_time)
        timesurface = timefont.render(timestr, False, (255, 255, 255))
        roomscreen.blit(timesurface,(250,80))

        # Update the screen
        pygame.display.flip()
        
    pygame.quit()
main()

