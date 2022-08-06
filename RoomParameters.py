import numpy as np
class Room:
    def __init__(self, room, room_size):
        self.room_size = room_size
        if room == "square":
            self.wallshere = False
            self.door_size = room_size/15                    
            self.destination = np.array([[-0.5, room_size/2]])  
            self.num_walls = 5
            self.walls = np.array([[[0, 0], [0, room_size/2-self.door_size/2]],
                          [[0, room_size/2+self.door_size/2], [0, room_size]], 
                          [[0, room_size], [room_size, room_size]],             
                          [[room_size, room_size], [room_size, 0]],          
                          [[room_size, 0], [0, 0]]])                         
            self.spawn_zone = np.array([[room_size/2, room_size-1], [1, room_size-1]])

    def get_wall(self, n):             
        return self.walls[n,:,:]

    def get_num_walls(self):         
        return self.num_walls

    def get_spawn_zone(self):          
        return self.spawn_zone

    def get_room_size(self):            
        return self.room_size

    def get_destination(self):         
        return self.destination
