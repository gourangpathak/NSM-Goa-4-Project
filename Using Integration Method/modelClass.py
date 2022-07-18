import sys
import pygame
import numpy as np
import pandas as pd
import Integrator
from Integrator import intg
from RoomParameters import Room
from differentialEquation import Differential_Equation
from pygameSimulation import simulate

class Model:
    def __init__(self, N, steps, method="intg", tau=0.1, desired_v=1.5, room="square",
                 room_size=25):
        std_deviation = 0.07                    
        variation = np.random.normal(loc=1, scale=std_deviation, size=(1, N)) # is late used to make the agents differ in weight and size

        # Parameters
        self.L = room_size  # size of square room (m)
        self.N = N  # quantity of pedestrians
        self.tau = tau  # time-step (s)
        self.steps = steps  # number of steps for integration
        self.radii = 0.4 * (np.ones(self.N)*variation).squeeze()  # radii of pedestrians (m)
        self.desired_v = desired_v * np.ones(self.N)  # desired velocity (m/s)
        self.m = 80 * (np.ones(self.N)*variation).squeeze()  # mass of pedestrians (kg)
        self.forces = None              # forces on the agents
        self.agents_escaped = None    #number of agents escaped by timesteps
        self.v = np.zeros((2, self.N, self.steps))  # Three dimensional array of velocity
        self.y = np.zeros(
            (2, self.N, self.steps))  # Three dimensional array of place: x = coordinates, y = Agent, z=Time
        self.room = Room(room, room_size)  # kind of room the simulation runs in
        self.method = getattr(Integrator, method)  # method used for integration
        self.diff_equ = Differential_Equation(self.N, self.L, self.tau, self.room, self.radii, self.m)  # initialize Differential equation

    # yields true if 2 person touch
    def touch(self, i, x): 
        for j in range(i - 1):
            if np.linalg.norm(x - self.y[:, j, 0]) < 3 * self.radii[i]:
                return True
        return False

    # fills the room with agents with random positions
    def populate(self):
        spawn = self.room.get_spawn_zone()
        len_right = spawn[0, 1] - spawn[0, 0]
        len_left = spawn[1, 1] - spawn[1, 0]
        max_len = max(len_left, len_right)

        # checks if the area is too small for the agents to fit in
        area_people = 0
        for i in range(self.N):
            area_people += 4 * self.radii[i] ** 2
        if area_people >= 0.7 * max_len ** 2:
            sys.exit('Too much people! Please change the size of the room/spawn-zone or the amount of people.')
        # checks if the agent touches another agent/wall and if so gives it a new random position in the spawn-zone 
        for i in range(self.N):
            # The pedestrians don't touch the wall
            x = len_right*np.random.rand() + spawn[0, 0]
            y = len_left * np.random.rand() + spawn[1, 0]
            pos = [x, y]

            # The pedestrians don't touch each other
            while self.touch(i, x):
                x = len_right * np.random.rand() + spawn[0, 0]
                y = len_left * np.random.rand() + spawn[1, 0]
                pos = [x, y]
            self.y[:, i, 0] = pos

        self.v[:, :, 0] = self.desired_v * self.diff_equ.e_t(self.y[:, :, 0])

    # calls the method of integration with the starting positions, diffequatial equation, number of steps, and delta t = tau
    def set(self):
        self.y, self.agents_escaped, self.forces = self.method(self.y[:, :, 0], self.v[:, :, 0], self.diff_equ.f, self.steps, self.tau, self.room)

    # Displayes the simulation in pygame
    def run(self, time, size):
        # self.y.tofile('sample.csv',sep='\n')
        simulate(self.y, self.room, time, self.radii, size, self.agents_escaped)
