import numpy as np

def exp_euler(y0, v0, f, N_steps, dt, room):
    tmp = 0
    agents_escaped = np.zeros(N_steps)

    y = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    v = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    a = np.zeros((y0.shape[0], y0.shape[1], N_steps))

    y[:,:,0] = y0

    for k in range(N_steps-1):
        a[:,:,k] = f(y[:,:,k], v[:,:,k])
        v[:,:,k+1] = v[:,:,k] + dt*a[:,:,k]
        y[:,:,k+1] = y[:,:,k] + dt*v[:,:,k+1]

        for i in range(y.shape[1]):
            # checks if there are two destination and calculates the distance to the closest destination
            destination = np.zeros(len(room.get_destination()))
            for count, des in enumerate(room.get_destination()):
                destination[count] = np.linalg.norm(y[:, i, k + 1] - des)
            distance = np.amin(destination)

            if distance < 0.1:
                y[:,i,k+1] = 10**6 * np.random.rand(2)       
                # y[:,i,k+1] = y[:,i,k]       
                tmp += 1             
            
        agents_escaped[k+1] = tmp

    return y, agents_escaped, a

def leap_frog(y0, v0, f, N_steps, dt, room):

    tmp = 0
    agents_escaped = np.zeros(N_steps)

    y = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    v = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    a = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    
    y[:,:,0] = y0
    v[:,:,0] += 0.5*dt*f(y[:,:,0], v[:,:,0])
    
    for k in range(N_steps-1):
        y[:,:,k+1] = y[:,:,k] + dt*v[:,:,k]
        a[:,:,k] = f(y[:,:,k], v[:,:,k])
        v[:,:,k+1] = v[:,:,k] + dt*f(y[:,:,k+1], v[:,:,k] + dt*a[:,:,k])

        for i in range(y.shape[1]):
            destination = np.zeros(len(room.get_destination()))
            for count, des in enumerate(room.get_destination()):
                destination[count] = np.linalg.norm(y[:, i, k + 1] - des)
            distance = np.amin(destination)

            if distance < 0.1:
                y[:,i,k+1] = 10**6 * np.random.rand(2)          
                tmp += 1             

        agents_escaped[k+1] = tmp

    return y, agents_escaped, a
    

def odestep(y0, v0, f, t, dt, room, dtmin = 0.0001, tol = 0.00001, maxiter = 100000):
    ytemp = y0
    vtemp = v0
    it = 0
    step = t
    dx = 0.1*dt

    a21 = (1.0/5.0)
    a31 = (3.0/40.0)
    a32 = (9.0/40.0)
    a41 = (44.0/45.0)
    a42 = (-56.0/15.0)
    a43 = (32.0/9.0)
    a51 = (19372.0/6561.0)
    a52 = (-25360.0/2187.0)
    a53 = (64448.0/6561.0)
    a54 = (-212.0/729.0)
    a61 = (9017.0/3168.0)
    a62 = (-355.0/33.0)
    a63 = (46732.0/5247.0)
    a64 = (49.0/176.0)
    a65 = (-5103.0/18656.0)
    a71 = (35.0/384.0)
    a73 = (500.0/1113.0)
    a74 = (125.0/192.0)
    a75 = (-2187.0/6784.0)
    a76 = (11.0/84.0)
    a81 = (5179.0/57600.0)
    a83 = (7571.0/16695.0)
    a84 = (393.0/640.0)
    a85 = (-92097.0/339200.0)
    a86 = (187.0/2100.0)
    a87 = (1.0/40.0)

    for i in range(maxiter):
        v1 = vtemp
        k1 = f(ytemp, vtemp)
        
        v2 = a21*v1
        k2 = f(ytemp + dx*v2, vtemp + dx*a21*k1)
        
        v3 = a31*v1 + a32*v2
        k3 = f(ytemp + dx*v3, vtemp + dx*(a31*k1 + a32*k2))
        
        v4 = a41*v1 + a42*v2 + a43*v3
        k4 = f(ytemp + dx*v4, vtemp + dx*(a41*k1 + a42*k2 + a43*k3))
        
        v5 = a51*v1 + a52*v2 + a53*v3 + a54*v4
        k5 = f(ytemp + dx*v5, vtemp + dx*(a51*k1 + a52*k2 + a53*k3 + a54*k4))
        
        v6 = a61*v1 + a62*v2 + a63*v3 + a64*v4 + a65*v5
        k6 = f(ytemp + dx*v6, vtemp + dx*(a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5))
        
        v7 = a71*v1 + a73*v3 + a74*v4 + a75*v5 + a76*v6
        k7 = f(ytemp + dx*v7, vtemp + dx*(a71*k1 + a73*k3 + a74*k4 + a75*k5 + a76*k6)) 
        
        #Error Control
        error = np.linalg.norm((a71-a81)*k1 + (a73-a83)*k3 + (a74-a84)*k4 + (a75-a85)*k5 + (a76-a86)*k6 - a87*k7)
        delta = 0.84*((tol/error)**0.2)
        
        
        if (error < tol or dx <= dtmin):
            step += dx
            vtemp += dx*(a81*k1 + a83*k3 + a84*k4 + a85*k5 + a86*k6 + a87*k7)
            ytemp += dx*(a81*v1 + a83*v3 + a84*v4 + a85*v5 + a86*v6 + a87*v7)

        if (delta <= 0.1):
            dx *= 0.1
        elif (delta >= 4.0):
            dx *= 2.0
        else:
            dx *= delta

        if (dx >= 0.5*dt):
            dx = 0.5*dt

        if (step >= t + dt):
            break
        elif (step + dx > t + dt):
            dx = t + dt - step
            continue
        elif (dx < dtmin):
            dx = dtmin
            continue    
        
    return ytemp, vtemp

def ode45(y0, v0, f, N_steps, dt, room):
    tmp = int(0)
    agents_escaped = np.zeros(N_steps)
    y = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    v = np.zeros((y0.shape[0], y0.shape[1], N_steps))
    a = np.zeros((y0.shape[0], y0.shape[1], N_steps))

    y[:,:,0] = y0
    v[:,:,0] = v0
    a[:,:,0] = f(y0, v0)

    for k in range(N_steps-1):
        y[:,:,k+1], v[:,:,k+1] = odestep(y[:,:,k], v[:,:,k], f, 0.0, 0.5, room)
        a[:,:,k+1] = f(y[:,:,k+1], v[:,:,k+1])

        for i in range(y.shape[1]):
            # checks if there are two destination and calculates the distance to the closets destination
            destination = np.zeros(len(room.get_destination()))
            for count, des in enumerate(room.get_destination()):
                destination[count] = np.linalg.norm(y[:, i, k + 1] - des)
            distance = np.amin(destination)

            if distance < 0.1:
                y[:,i,k+1] = 10**6 * np.random.rand(2)          
                tmp += 1             
                  
        agents_escaped[k+1] = tmp
    
    return y, agents_escaped, a