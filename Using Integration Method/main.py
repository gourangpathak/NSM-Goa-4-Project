from modelClass import Model
ins = Model(N=50, steps=1000, method="ode45", room_size=25, desired_v = 1.5, room="square")
ins.populate()                 
ins.set()                      
ins.run(100, 700)   
