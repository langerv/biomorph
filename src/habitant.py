import random
from shape import Rectangle
from npc import Npc
from aptitude import PhysicalAptitudes, PsychicalAptitudes


'''
Class Local (NPC)
'''

class Habitant(Npc):

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)
       # design Wanderer aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, random.randrange(1,3))
        self.set_aptitude(PhysicalAptitudes.MOVE, random.randrange(4,6))
        self.set_aptitude(PhysicalAptitudes.CONS, random.randrange(1,3))
        self.set_aptitude(PsychicalAptitudes.INTL, 5)
        self.set_aptitude(PsychicalAptitudes.CHAR, 5)
        # compute Wanderer attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC, 60)
        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE, 1)
        self._dir_x = self._dx
        self._dir_y = 0
        self._size = self.size_rule(PhysicalAptitudes.CONS, 2)
        self._hue = 0.85
        self._color = self.color_rule(PsychicalAptitudes.INTL, PsychicalAptitudes.CHAR)
        # create shape
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)
 
    def update(self, neighbours, delta_time):
        if self._hit is True:
            # if a npc is hit, we compute time before to get it back to life
            self._hit_time += delta_time
            if int(self._hit_time) % 60 > Npc.HIT_TIMER:
                self._hit_time = 0
                self._hit = False
        else:
            if self._shape._x < self._area[0] and self._dir_x < 0:
                self._dir_x = 0
                self._dir_y = -self._dy

            if self._shape._x > self._area[2] and self._dir_x > 0:
                self._dir_x = 0
                self._dir_y = self._dy

            if self._shape._y < self._area[1] and self._dir_y < 0:
                self._dir_x = self._dx
                self._dir_y = 0

            if self._shape._y > self._area[3] and self._dir_y > 0:
                self._dir_x = -self._dx
                self._dir_y = 0

            if random.randint(0, 1000) == 0:
                self._dir_x, self._dir_y = self._dir_y, self._dir_x

            self.move(self._dir_x, self._dir_y)
