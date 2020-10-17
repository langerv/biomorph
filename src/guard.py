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

        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE)
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

        # perception
        target = None
        target_dist = self._vision
        target_dx = target_dx = 0
        for neighbour in neighbours:
            target_dx = neighbour.X - self._shape._x
            target_dy = neighbour.Y - self._shape._y
            dist = math.sqrt(target_dx**2 + target_dy**2)
            if dist < target_dist:
                target = neighbour
                target_dist = dist

        # action: Guard FSM
        if self._state == Guard.state.idle:
            self._state = Guard.state.patrol

        elif self._state == Guard.state.patrol:
            if target_dist < self._vision:
                self._state = Guard.state.watch
            else:
                # patrol
                if self._shape._x < self._area[0] and self._patrol_dx < 0:
                    self._patrol_dx *= -1
                if self._shape._x > self._area[2] and self._patrol_dx > 0:
                    self._patrol_dx *= -1
                if self._shape._y < self._area[1] and self._patrol_dy < 0:
                    self._patrol_dy *= -1
                if self._shape._y > self._area[3] and self._patrol_dy > 0:
                    self._patrol_dy *= -1
                self.move(self._patrol_dx, self._patrol_dy)

        elif self._state == Guard.state.watch:
            # watch
            if target_dist >= self._vision:
                # TODO: if not inside area, go to center of the area first
                self._state = Guard.state.patrol
            elif target_dist < self._vision/2:
                self._state = Guard.state.attack
            else:
                # follow at distance TODO
                pass

        elif self._state == Guard.state.attack:
            # attack
            if target_dist >= self._vision/2:
                self._state = Guard.state.watch
            else:
                # move towards target
                if target_dist >= self.Delta_Speed:
                    self.move(self._dx * target_dx/target_dist, self._dy * target_dy/target_dist)
                else:
                    # hit target TODO
                    print(f"hit {target}")
