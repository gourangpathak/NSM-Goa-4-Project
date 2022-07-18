import numpy as np

class Differential_Equation:
    def __init__(self, num_individuals, L, tau, room, radii, weights):
        # Initial conditions
        self.room = room                            #import class room as room
        self.N = num_individuals                    # quantity of agents
        self.m = weights                            # mass of agents (kg)
        self.v_0 = 1.5 * np.ones(self.N)            # desired velocity (m/s)
        self.radii = radii                          # radii of agents (m)
        self.A = 2*10**3                            # constant (N)
        self.B = 0.08                               # constant (m)
        self.tau = tau                              # time-step (s)
        self.k = 1.2*10**5                          # parameter (kg/s^2)
        self.kap = 2.4*10**5                        # parameter (kg/(m*s^2))
        self.L = L                                  # size of square room (m)
        self.r_D = room.get_destination()           # position of door (m,m)
        self.numwalls = self.room.get_num_walls()   # number of walls 
        self.walls = self.room.walls                # position of corner points of the walls
        self.wallshere = self.room.wallshere        # True if there are walls in the middle of the room

    #Checks if an agent touches anotherone or a wall  
    def g(self, x):    
        if x < 0:
            return 0
        else:
            return x      
        
    #Adds the radii of agents i and j
    def rad(self, i, j):  
        return self.radii[i] + self.radii[j]

    #Distance between agent i at positon r and wall j
    def wall_distance(self, i, j, r):
        temp_wall      = self.walls[j,:,:]
        line_vec       = temp_wall[1,:]-temp_wall[0,:]
        pnt_vec        = r[:,i]-temp_wall[0,:]
        line_len       = np.linalg.norm(line_vec)
        line_unitvec   = line_vec/line_len
        pnt_vec_scaled = pnt_vec/line_len
        temp           = line_unitvec.dot(pnt_vec_scaled)    
        if temp < 0.0:
            temp = 0.0
        elif temp > 1.0:
            temp = 1.0
        nearest       = line_vec*temp
        dist          = pnt_vec-nearest
        nearest       = nearest + temp_wall[0,:]
        distance      = np.linalg.norm(dist)
        n             = dist/distance
        t             = np.array([-n[1], n[0]])
        return distance, n, t, nearest   
    
    #Distance between agent i and agent j
    def agent(self, i, j, r,v):
        d    = np.linalg.norm(r[:, i] - r[:, j])
        n    = (r[:, i] - r[:, j])/d
        t    = np.array([-n[1],n[0]])
        temp = v[:, j] - v[:, i]
        dv_t = temp.dot(t)
        return d, n, t, dv_t
    
    #Force between agent i and j
    def f_ij(self, i, j, r, v):  
        d, n, t, dv_t = self.agent(i, j, r,v)
        rad_ij = self.rad(i,j)
        a = self.A * np.exp((rad_ij - d) / self.B) + self.k * self.g(rad_ij - d)
        b = self.kap * self.g(rad_ij - d) * dv_t
        return a * n + b * t
    
    #Force between agent i and wall j
    def f_iW(self, i, j, r, v):  
        d,n,t = self.wall_distance(i, j, r)[:-1]
        a = self.A * np.exp((self.radii[i] - d) / self.B) + self.k * self.g(self.radii[i] - d)
        b = self.kap * self.g(self.radii[i] - d) * v[:, i].dot(t)
        return a * n - b * t

    #point of intersection of two lines formed by the points (a1,a2), respectively (b1,b2)
    def seg_intersect(self, a1,a2,b1,b2):
        da = a2-a1
        db = b2-b1
        dp = a1-b1
        dap = np.array([-da[0][1],da[0][0]])
        denom = np.dot(dap, db)
        num = np.dot(dap, dp)
        return (num / denom.astype(float))*db + b1

    #return true if the point c is between the two points a and b
    def is_between(self,a,b,c):
        return np.linalg.norm(a-c) + np.linalg.norm(c-b) == np.linalg.norm(a-b) 
    
    #taking the right agent vector direction
    def direction(self,i,j,r):
        wall = self.walls[j,:,:]
        wall_norm = (wall[0,:]-wall[1,:])/np.linalg.norm(wall[0,:]-wall[1,:])
        point = self.seg_intersect(r[:,i],self.r_D,wall[0,:],wall[1,:])
        t_or_f = self.is_between(wall[0,:],wall[1,:],point)
        
        if (t_or_f == 1 and np.linalg.norm(-r[:,i]+self.r_D)+self.radii[i] > np.linalg.norm(-point+self.r_D)) or (np.min([np.linalg.norm(r[:,i]-wall[0,:]),np.linalg.norm(r[:,i]-wall[1,:])]) < np.linalg.norm(2*self.radii[i]) and np.linalg.norm(-r[:,i]+self.r_D) > np.linalg.norm(-point+self.r_D)):
            e = self.nearest_path(wall,t_or_f,point,wall_norm,r[:,i],i)
        else:
            e = self.e_0(r[:,i],i)
        return e 

    #take the right direction in case of wall corner points
    def e_1(self,r_i,temp_wall,i,j):
        all_walls = self.walls[:,:,:]
        wall_norm = (temp_wall[0,:]-temp_wall[1,:])/np.linalg.norm(temp_wall[0,:]-temp_wall[1,:])
        check_close_corner = np.zeros((all_walls.shape[0],2))
        point = self.seg_intersect(r_i,self.r_D,temp_wall[0,:],temp_wall[1,:])
        t_or_f = self.is_between(temp_wall[0,:],temp_wall[1,:],point)
        
        for k in range(all_walls.shape[0]):
            if k == j:
                continue
            check_close_corner[k,0] = self.is_between(all_walls[k,0,:],all_walls[k,1,:],temp_wall[0,:])
            check_close_corner[k,1] = self.is_between(all_walls[k,0,:],all_walls[k,1,:],temp_wall[1,:])
        
        if np.sum(check_close_corner) == 1:
            for k in range(all_walls.shape[0]):
                if (check_close_corner[k,0] == 1 and check_close_corner[k,1] == 0) and self.is_between(all_walls[k,0,:],all_walls[k,1,:],self.seg_intersect(r_i,self.r_D,all_walls[k,0,:],all_walls[k,1,:])) == 1:
                    e = self.nearest_path(temp_wall,t_or_f,point,wall_norm,r_i,i)
                    break
                elif (check_close_corner[k,0] == 1 and check_close_corner[k,1] == 0) and self.is_between(all_walls[k,0,:],all_walls[k,1,:],self.seg_intersect(r_i,self.r_D,all_walls[k,0,:],all_walls[k,1,:])) == 0:
                    if np.linalg.norm(r_i-point)<self.radii[i]:
                        e = self.nearest_path(temp_wall,t_or_f,point,wall_norm,r_i,i)
                    elif (t_or_f == 1 and np.linalg.norm(point-r_i)<2*self.radii[i]):
                        e =  - wall_norm 
                        break
                    else:
                        p = temp_wall[1,:] - wall_norm*2*self.radii[i]
                        e = (-r_i+p)/np.linalg.norm(-r_i+p)
                        break
                elif check_close_corner[k,0] == 0 and check_close_corner[k,1] == 1 and self.is_between(all_walls[k,0,:],all_walls[k,1,:],self.seg_intersect(r_i,self.r_D,all_walls[k,0,:],all_walls[k,1,:])) == 1:
                    e = self.nearest_path(temp_wall,t_or_f,point,wall_norm,r_i,i)
                    break
                    
                elif check_close_corner[k,0] == 0 and check_close_corner[k,1] == 1 and self.is_between(all_walls[k,0,:],all_walls[k,1,:],self.seg_intersect(r_i,self.r_D,all_walls[k,0,:],all_walls[k,1,:])) == 0:    
                    if np.linalg.norm(r_i-point)<self.radii[i]:
                        e = self.nearest_path(temp_wall,t_or_f,point,wall_norm,r_i,i)
                    elif (t_or_f == 1 and np.linalg.norm(point-r_i)<2*self.radii[i]):
                        e =  wall_norm 
                        break
                    else: 
                        p = temp_wall[0,:] + wall_norm*2*self.radii[i]
                        e = (-r_i+p)/np.linalg.norm(-r_i+p)
                        break
        else:
            e = self.nearest_path(temp_wall,t_or_f,point,wall_norm,r_i,i)
        return e
    
    
    #take the nearest path if one agents has to overtake a wall
    def nearest_path(self,temp_wall,t_or_f,point,wall_norm,r_i,i):
        if (np.linalg.norm(self.r_D-temp_wall[0,:]) + np.linalg.norm(r_i-temp_wall[0,:])) <= (np.linalg.norm(self.r_D-temp_wall[1,:]) + np.linalg.norm(r_i-temp_wall[1,:])):
            #if (t_or_f == 1 and np.linalg.norm(point-r_i)<2*self.radii[i]):
            #    e =  wall_norm 
            #else: 
            p = temp_wall[0,:] + wall_norm*2*self.radii[i]
            e = (-r_i+p)/np.linalg.norm(-r_i+p)
        else:
            #if (t_or_f == 1 and np.linalg.norm(point-r_i)<2*self.radii[i]):
            #    e =  - wall_norm 
            #else:
            p = temp_wall[1,:] - wall_norm*2*self.radii[i]
            e = (-r_i+p)/np.linalg.norm(-r_i+p)
        return e
    

    #Desired direction normalized for one agent
    def e_0(self, r, i):  
        #If there are two destinations, then half of the people go to each destination
        if len(self.r_D) == 2:
            if i < self.N/2:
                return (-r + self.r_D[0]) / np.linalg.norm(-r + self.r_D[0])
            else:
                return (-r + self.r_D[1]) / np.linalg.norm(-r + self.r_D[1])

        return (-r + self.r_D) / np.linalg.norm(-r + self.r_D)

    #Finding the nearest wall that ubstruct one person
    def nearest_wall(self,r_i):
        all_walls = self.walls[5:,:,:]
        distance = np.zeros((all_walls.shape[0]))
        for i in range(all_walls.shape[0]):
            temp_wall = all_walls[i,:,:]
            point = self.seg_intersect(r_i,self.r_D,temp_wall[0,:],temp_wall[1,:])
            distance[i] = np.linalg.norm(point-r_i)
        return 5+np.argmin(distance)
  

    #Desired direction normalized for all agents
    def e_t(self, r):
        e_temp = np.zeros((2, self.N))
        #If there are additional walls the desired direction doesn't have to...
        #...be the direction of a door.
        if self.wallshere == False: 
            for i in range(self.N):
                e_temp[:, i] = self.e_0(r[:,i], i)
        else:
            for i in range(self.N):
                j = self.nearest_wall(r[:,i])
                e_temp[:, i] = self.direction(i,j,r)
        return e_temp


    #The interacting force of the agents to each other  
    def f_ag(self, r, v):

        f_agent = np.zeros((2, self.N))
        fij     = np.zeros(((2, self.N, self.N)))
        for i in range(self.N-1):
            for j in range(self.N-1-i):
                    fij[:,i,j+i+1] = self.f_ij(i,j+i+1,r,v)
                    fij[:,j+i+1,i] = -fij[:,i,j+i+1]
        f_agent = np.sum(fij, 2)
        return f_agent

    #The force of each wall acting on each agents
    def f_wa(self, r, v):
        f_wall = np.zeros((2, self.N))
        for i in range(self.N):
            for j in range(self.numwalls):
                f_wall[:, i] += self.f_iW(i, j, r, v)
        return f_wall
    
    #The diff_equation of our problem
    #Calculates the accelaration of each agent
    def f(self, r, v):
        e_temp = self.e_t(r)
        acc = (self.v_0 * e_temp - v) / self.tau + self.f_ag(r, v) / self.m + self.f_wa(r, v) / self.m
        return acc

