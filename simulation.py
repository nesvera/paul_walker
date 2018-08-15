import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pygame_util
import pymunk.util
from pymunk import Vec2d
from math import *
import random
from time import sleep
import copy

from walker import walker

class simulation():
    def __init__(self, scr_w = 800, scr_h = 600, \
                    angle=pi/10, gravity=200, \
                    show=True):
        # Window size
        self.scr_w = scr_w
        self.scr_h = scr_h
        # Graphics initialization (if show)
        self.show = show
        if self.show:
            pygame.init()
            self.screen = pygame.display.set_mode((self.scr_w, self.scr_h))
            self.clock = pygame.time.Clock()
        # Create the space
        self.space = pymunk.Space()
        self.space.gravity = (0, -gravity)
        # Create the floor 
        self._create_floor(angle)
    
    def _create_floor(self, angle):
        # Create the floor
        body = pymunk.Body()
        body.position = self.scr_w/2, self.scr_h/4
        v = [(-self.scr_w,-(self.scr_h/2)*sin(angle)), \
             (self.scr_w,(self.scr_h/2)*sin(angle)), \
             (self.scr_w, -self.scr_h/2), \
             (-self.scr_w, -self.scr_h/2)]
        floor = pymunk.Poly(body, v)
        floor.friction = 1.0
        floor.elasticity = 0.4
        self.space.add(floor)

    def _invy(self, pos):
        return pos[0], self.scr_h - pos[1]

    def step(self, delta, time, sim_time, generation, individuo):
        # Simulation step
        self.space.step(delta)
        # Draw stuff (if show)
        if self.show:
            self.screen.fill(THECOLORS['black'])
            pygame_util.draw_space(self.screen, self.space)
            pygame_util.text(self.screen, time, sim_time, generation, individuo)
            pygame.display.flip()
            self.clock.tick(1/delta)

    def interactive(self):
        # Interactive mode
        running = True
        robot = None
        while running:
            # Deal with clicks and other events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    robot = walker(self.space, self._invy((537,226)), 80, 60, 40, pi, pi/2, 0, 0)
        
            self.step(0.02, 0, 0, 0,0)

    def put_robot(self, robot):
        self.robot = robot

    def get_ke(self):
        # Calculates the kinect energy of the simulation
        k = 0.0
        for body in self.space.bodies:
            k += body.kinetic_energy
        return k

    # Simulation of an individual       
    def individual_sim(self, pos, ul, ll, w, lua, lla, rua, rla, generation, individuo):
        robot = walker(self.space, pos, ul, ll, w, lua, lla, rua, rla)
                
        sim_time = 2500                  # 300 ~= 6 segundos
        time = 0
        walk_time = 0

        last_x = [(0,0), (0,0), (0,0), (0,0)]

        while True: 
            self.step(0.02, time, sim_time, generation, individuo)
            time += 1

            # Get data from simulation
                # self.space.bodies[0].position = upper_leg_1
                # self.space.bodies[1].position = lower_leg_1
                # self.space.bodies[2].position = lower_leg_2
                # self.space.bodies[3].position = upper_leg_2
            
            ke = self.get_ke()
            cur_x = [(self.space.bodies[0].position.x, self.space.bodies[0].position.y),\
                     (self.space.bodies[1].position.x, self.space.bodies[1].position.y),\
                     (self.space.bodies[2].position.x, self.space.bodies[2].position.y),\
                     (self.space.bodies[3].position.x, self.space.bodies[3].position.y)]

            # Se o individuo estar se mexendo ou ainda tiver tempo ou se estiver dentro do cenario
            if time < sim_time and ke > 30000 and min(cur_x[:][0]) > 20:

                #Se a upper_leg estiver acima da lower_leg, em relacao ao eixo Y
                if (cur_x[0][1] - cur_x[1][1] > ll/2) and (cur_x[3][1] - cur_x[2][1] > ll/2):

                    #Se a posicao em x da lower_leg for diferente do passo anterior
                    if cur_x[1][0] < last_x[1][0] or cur_x[2][0] < last_x[2][0]:
                        walk_time += 1

            #Caso tempo acabe ou walker fique parado
            else:
                #retorna o tempo de caminhada e a o valor mais proximo da borda esquerda
                return walk_time, (800 - min(cur_x[1][0], cur_x[2][0]))
            
            last_x = copy.copy(cur_x)
            
# Uncomment this lines, change the values from the robot on line 73, run simulation.py, and use mouse click to create a robot
#s = simulation()
#s.interactive()

