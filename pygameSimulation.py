import pygame
import numpy as np
import matplotlib.pyplot as plt

movement_data = np.random.randint(20, 700, (2, 5, 5))
objects_pos = np.random.randint(100, 700, (2, 10))


def simulate(movement_data, room, wait_time, radii, sim_size, agents_escaped):
    background_color =(43, 44, 41)       
    people_color = (250, 0, 0)                    
    destination_color = (20, 56, 36)               
    object_color = (0, 0, 0)                      

    # variable for initializing pygame simulation
    normalizer = int(sim_size/room.get_room_size()) # the ratio (size of image) / (size of actual room) 
    map_size = (room.get_room_size()*normalizer + 100,  #size of the map
                room.get_room_size()*normalizer + 100)  #plus a little free space
    wait_time = wait_time                              #time that the simultation waits between each timestep
    wait_time_after_sim = 3000                        #waittime after simulation
    movement_data_dim = movement_data.shape         
    num_persons = movement_data_dim[1]          #number of indiciduals in the simulation
    num_time_iterations = movement_data_dim[2]  #number of timesteps
    num_walls = room.get_num_walls()          #number of walls

    pygame.init()                                 #initialize the intanz
    simulate=False                                  #variable to indicate if the simulation is running
    font = pygame.font.Font(None, 32)             #create a new object of type Font(filename, size)
    worldmap = pygame.display.set_mode(map_size)
    
    while True:
        # start simulation if any key is pressed and quits pygame if told so
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                simulate=True
            elif event.type == pygame.QUIT:
                pygame.quit()
        worldmap.fill(0)
        #This creates a new surface with text already drawn onto it
        text = font.render('Start Simulating', True, (255, 255, 255))
        #printing the text starting with a 'distance' of (100,100) from top left
        worldmap.blit(text, (200, 200))
        pygame.display.update()
        
        if simulate == True:
            # print the map for each timestep
            for t in range(num_time_iterations):
                # quit the simulation if told so
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                #initialize the map with background color
                worldmap.fill(background_color)
        
                #draw each peron for timestep t
                for person in range(num_persons):
                    pygame.draw.circle(worldmap, people_color, 
                                    ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                    (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                    int(normalizer * radii[person]), 0)
        
                #draw each object for timestep t
                for wall in range(num_walls):
                    pygame.draw.lines(worldmap, object_color, True, 
                                    normalizer*room.get_wall(wall) + 50, 2)
                # draw the destination of the agents in green
                for des in room.get_destination():
                    pygame.draw.circle(worldmap, destination_color,
                        ((normalizer * des[0] + 50).astype(int),
                        (normalizer * des[1] + 50).astype(int)),
                        7, 0)

                #update the map
                pygame.display.update()
                #wait for a while before drawing new positions
                pygame.time.wait(wait_time)
            simulate=False
            text = font.render('SIMULATION FINISHED', True, (255, 255, 255))
            worldmap.blit(text, (100, 100))
            pygame.display.update()
            pygame.time.wait(wait_time_after_sim)
            

