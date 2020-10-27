import random
from shape import Rectangle
from npc import Npc
from aptitude import PhysicalAptitudes, PsychicalAptitudes


'''
Class Wanderer (NPC)
Behaviour: wander in the area and do nothing else (as preys)
'''

class Wanderer(Npc):

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)
       # design Wanderer aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.MOVE, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.CONS, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.INTL, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.CHAR, random.randrange(1,6))
        # compute Wanderer attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC, 60)
        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE, 1)
        self._size = self.size_rule(PhysicalAptitudes.CONS, 2)
        self._hue = random.random()
        self._color = self.color_rule(PsychicalAptitudes.INTL, PsychicalAptitudes.CHAR)
        # create shape
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)
 
    def update(self, neighbours, delta_time):
        Npc.update(self, delta_time)
        if self.Hit is True:
            return
        # wander
        if self._shape._x <= self._area[0] and self._dx < 0:
            self._dx *= -1
        elif self._shape._x >= self._area[2] and self._dx > 0:
            self._dx *= -1
        elif self._shape._y <= self._area[1] and self._dy < 0:
            self._dy *= -1
        elif self._shape._y >= self._area[3] and self._dy > 0:
            self._dy *= -1
        else:
            self.move(self._dx, self._dy)
