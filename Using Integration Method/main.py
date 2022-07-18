from modelClass import Model
ins = Model(N=5, steps=1000, method="intg", room_size=30, desired_v = 1.5, room="square")
ins.populate()                 
ins.set()                      
ins.run(100, 700)   
