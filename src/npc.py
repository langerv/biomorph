import math
import random
from shape import Rectangle
from game_object import GameObject
from character import Character
from aptitude import PhysicalAptitudes, PsychicalAptitudes

HIT_TIMER = 5 # number of seconds before a hit npc goes back to life
RAD2DEG = 180 / math.pi


'''
NPC class
'''

class Npc(Character, GameObject):

    def __init__(self, x, y, area):
        Character.__init__(self)
        GameObject.__init__(self, x, y)
        self._hit = False
        self._hit_time = 0
        self._area = area

    def __str__(self):
        return '    '.join([f"{key.name} = {ap.Value:0.1f}" for key, ap in self.Aptitudes.items()])

    @property
    def Area(self):
        return self._area

    @property
    def Hit(self):
        return self._hit

    @Hit.setter
    def Hit(self, value):
        self._hit = value


'''
Class Guard (NPC)
Behaviour: 
'''

class Guard(Npc):

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)

    def update(self, delta_time):
        pass

'''
Class Wanderer (NPC)
Behaviour: wander in the area and do nothing else (preys)
'''

class Wanderer(Npc):

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)

       # define aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.MOVE, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.CONS, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.INTL, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.CHAR, random.randrange(1,6))

        # define behaviour and shape
        self._dx = self._dy = self.get_aptitude(PhysicalAptitudes.MOVE).Value
        self._size = GameObject.MIN_SHAPE_SIZE + self.get_aptitude(PhysicalAptitudes.CONS).Value**2

        # compute color
        self._hue = random.random()
        self._color = self.HLS_to_Color(
            self._hue, # H
            self.get_aptitude(PsychicalAptitudes.INTL).Value / 5, # L
            self.get_aptitude(PsychicalAptitudes.CHAR).Value / 5) # S

        # create shape
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)
 
    def update(self, delta_time):
        if self._hit is True:
            # if a npc is hit, we compute time before to get it back to life
            self._hit_time += delta_time
            if int(self._hit_time) % 60 > HIT_TIMER:
                self._hit_time = 0
                self._hit = False
        else:
            # wander
            self._shape._x += self._dx
            self._shape._y += self._dy
            self._shape._angle = math.atan2(self._dy, self._dx) * RAD2DEG
            if self._shape._x < self._area[0] and self._dx < 0:
                self._dx *= -1
            if self._shape._x > self._area[2] and self._dx > 0:
                self._dx *= -1
            if self._shape._y < self._area[1] and self._dy < 0:
                self._dy *= -1
            if self._shape._y > self._area[3] and self._dy > 0:
                self._dy *= -1
