import arcade
import math
from enum import Enum, auto
import random
from shape import Rectangle
from npc import Npc
from aptitude import PhysicalAptitudes, PsychicalAptitudes


'''
Class Guard (NPC)
Behaviour: 
'''

class Guard(Npc):

    class state(Enum):
        idle = auto()
        patrol = auto()
        watch = auto()
        attack = auto()

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)
        self._state = Guard.state.idle

        # design Guard aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, 3)
        self.set_aptitude(PhysicalAptitudes.MOVE, 3)
        self.set_aptitude(PhysicalAptitudes.CONS, 5)
        self.set_aptitude(PsychicalAptitudes.INTL, 2)
        self.set_aptitude(PsychicalAptitudes.CHAR, 2)

        # compute Guard attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC)
        self._vision_limit_attack = self._vision * 0.7

        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE)
        self._delta = self.Delta_Speed
        self._patrol_dx = self._patrol_dy = 0
        if self._width >= self._height:
            self._patrol_dx = self._dx
        else:
            self._patrol_dy = self._dy

        self._size = self.size_rule(PhysicalAptitudes.CONS)
        self._hue = 0
        self._color = arcade.color.RED
        # create shape
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)

    def update(self, neighbours, delta_time):

        # perception: find closest neighbour
        target = None
        target_dist = self._vision
        for neighbour in neighbours:
            dx = neighbour.X - self._shape._x
            dy = neighbour.Y - self._shape._y
            dist = math.sqrt(dx**2 + dy**2)
            if dist < target_dist:
                target = neighbour
                target_dist = dist

        ''' guard FSM '''
        if self._state == Guard.state.idle:
            self._state = Guard.state.patrol
    
        # patrol behaviour
        elif self._state == Guard.state.patrol:
            if target_dist < self._vision:
                self._state = Guard.state.watch
            else:
                # patrol move
                if self._shape._x < self._area[0] and self._patrol_dx < 0:
                    self._patrol_dx *= -1
                if self._shape._x > self._area[2] and self._patrol_dx > 0:
                    self._patrol_dx *= -1
                if self._shape._y < self._area[1] and self._patrol_dy < 0:
                    self._patrol_dy *= -1
                if self._shape._y > self._area[3] and self._patrol_dy > 0:
                    self._patrol_dy *= -1
                self.move(self._patrol_dx, self._patrol_dy)

        # watch behaviour
        elif self._state == Guard.state.watch:
            if target_dist >= self._vision:
                # target too far, get back to patrol behaviour
                if self.in_area(self._shape._x, self._shape._y) is True:
                    # guard in area, patrol again
                    self._state = Guard.state.patrol
                else:
                    # guard not in area, go to center of the area first
                    self.move_to(self._center_x, self._center_y)

            elif target_dist < self._vision_limit_attack: 
                # target too close, attack!
                self._state = Guard.state.attack

            else:
                # follow at distance
                self.look_at(target.X, target.Y)

        # attack behaviour
        elif self._state == Guard.state.attack:
            if target_dist >= self._vision_limit_attack:
                self._state = Guard.state.watch
            else:
                # move towards target
                if target_dist >= self._delta:
                    self.move_to(target.X, target.Y)
                else:
                    # hit target: hit points depend on difference of Constitution with minimum of 0.1
                    hit_points = max(self.get_aptitude(PhysicalAptitudes.CONS).Value - target.get_aptitude(PhysicalAptitudes.CONS).Value, 0.1)
                    target.hit(hit_points)
