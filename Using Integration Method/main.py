from simulationClass import Simulation

sim = Simulation(num_individuals=50, num_steps=1000, method="ode45", room_size=10, room="square")
sim.fill_area()                 
sim.run()                      
sim.show(wait_time=200, sim_size=800)   
