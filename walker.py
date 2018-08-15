#!/usr/bin/env python2.7

import pymunk
import pymunk.util
from pymunk import Vec2d
from math import pi

class walker():
    def __init__(self, space, pos, ul, ll, w, \
            lua, lla, rua, rla):
        '''Creates a passive dynamic walker. The parameters
        are as follow:
        space -- the pymunk space
        pos -- the initial position
        ul -- the length of the upper leg
        ll -- the length of the lower leg
        w -- the width of the robot
        lua -- the angle of the left hip
        lla -- the angle of the left ankle
        rua -- the angle of the right hip
        rla -- the angle of the right angle
        '''
        # Constructor method
        self.space = space
        self.density = 1.0
        self.friction = 1.0
        self.elasticity = 0.4
        self.group = 1
        # Create left leg
        self.lul = self._create_leg(pos, ul, w, lua)
        ll_pos = Vec2d(0, -ul).rotated(lua) + pos
        self.lll = self._create_leg(ll_pos, ll, w, lua+lla)
        self.l_knee = pymunk.PivotJoint(self.lul.body, \
                self.lll.body, ll_pos)
        # Create right leg
        self.rul = self._create_leg(pos, ul, w, rua)
        rl_pos = Vec2d(0, -ul).rotated(rua) + pos
        self.rll = self._create_leg(rl_pos, ll, w, rua+rla)
        self.r_knee = pymunk.PivotJoint(self.rul.body, \
                self.rll.body, rl_pos)
        # Hip
        self.hip = pymunk.PivotJoint(self.lul.body, self.rul.body, pos)
        # Limit rotation on the knees between zero and pi
        self.l_limit = pymunk.RotaryLimitJoint(self.lul.body, \
                self.lll.body, (-pi/360.0)-lla, pi-lla)
        self.r_limit = pymunk.RotaryLimitJoint(self.rul.body, \
                self.rll.body, (-pi/360.0)-rla, pi-rla)
        # add the constraints to the space
        self.space.add(self.l_knee, self.r_knee, self.hip, \
                self.l_limit, self.r_limit)
    def __del__(self):
        # Destructor
        # Remove the contraints
        for constraint in [self.l_knee, self.r_knee, self.hip, \
                self.l_limit, self.r_limit]:
            self.space.remove(constraint)
        # Remove the legs
        for leg in [self.lul, self.lll, self.rul, self.rll]:
            self._delete_leg(leg)
    def _delete_leg(self, leg):
        body = leg.body
        # Remove the shape
        self.space.remove(leg)
        # Remove the body
        self.space.remove(body)
    def _create_leg(self, pos, l=80.0, w=10.0, angle=0.0):
        # Calculate the position of the center of gravity
        cg = Vec2d(0, -l/2).rotated(angle) + pos
        # Find the vertices of the bounding box
        v1 = Vec2d(-w/2, l/2).rotated(angle)
        v2 = Vec2d(w/2, l/2).rotated(angle)
        v3 = Vec2d(w/2, -l/2).rotated(angle)
        v4 = Vec2d(-w/2, -l/2).rotated(angle)
        v = [v4,v3,v2,v1]
        # Calculate the properties of the polygon
        area = pymunk.util.calc_area(v)
        mass = area * self.density
        moment = pymunk.moment_for_poly(mass, v)
        # Create the body
        body = pymunk.Body(mass, moment)
        body.position = cg
        # Create the shape
        leg = pymunk.Poly(body, v)
        leg.friction = self.friction
        leg.elasticity = self.elasticity
        leg.group = self.group
        # Add the body and shape to the space
        self.space.add(leg, body)
        return leg

