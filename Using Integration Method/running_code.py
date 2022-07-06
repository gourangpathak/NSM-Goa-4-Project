from Simulation_class import Simulation

sim = Simulation(num_individuals=30, num_steps=1000, method="leap_frog", room_size=15, room="square")
sim.fill_room()                 # fills the spawn zone with random people
sim.run()                       # runs the simulation
sim.show(wait_time=50, sim_size=700)   # displays the solutions to the simulations in pygame with
