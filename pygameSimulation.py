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
    normalizer = int(sim_size/room.get_room_size()) 
    map_size = (room.get_room_size()*normalizer + 100,  
                room.get_room_size()*normalizer + 100)  
    wait_time = wait_time                              
    wait_time_after_sim = 3000                        
    movement_data_dim = movement_data.shape         
    num_persons = movement_data_dim[1]          
    num_time_iterations = movement_data_dim[2]  
    num_walls = room.get_num_walls()          
    pygame.init()                                 
    simulate=False                                  
    font = pygame.font.Font(None, 32)             
    worldmap = pygame.display.set_mode(map_size)
    
    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                simulate=True
            elif event.type == pygame.QUIT:
                pygame.quit()
        worldmap.fill(0)
        text = font.render('Start Simulating', True, (255, 255, 255))
        worldmap.blit(text, (200, 200))
        pygame.display.update()
        
        if simulate == True:
            for t in range(num_time_iterations):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                
                worldmap.fill(background_color)
        
                for person in range(num_persons):
                    pygame.draw.circle(worldmap, people_color, 
                                    ((normalizer*movement_data[0, person, t] + 50).astype(int),
                                    (normalizer*movement_data[1, person, t] + 50).astype(int)),
                                    int(normalizer * radii[person]), 0)
        
                for wall in range(num_walls):
                    pygame.draw.lines(worldmap, object_color, True, 
                                    normalizer*room.get_wall(wall) + 50, 2)
                for des in room.get_destination():
                    pygame.draw.circle(worldmap, destination_color,
                        ((normalizer * des[0] + 50).astype(int),
                        (normalizer * des[1] + 50).astype(int)),
                        7, 0)

                pygame.display.update()
                pygame.time.wait(wait_time)
            simulate=False
            text = font.render('SIMULATION FINISHED', True, (255, 255, 255))
            worldmap.blit(text, (100, 100))
            pygame.display.update()
            pygame.time.wait(wait_time_after_sim)
            

