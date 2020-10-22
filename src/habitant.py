import random
from shape import Rectangle
from npc import Npc
from aptitude import PhysicalAptitudes, PsychicalAptitudes


'''
Class Habitant (NPC)
Bahviour: NPCs that are allowed to pass the guard, just go in/out of the protected area
'''

class Habitant(Npc):

    def __init__(self, x, y, area):
        Npc.__init__(self, x, y, area)
       # design Wanderer aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, random.randrange(1,3))
        self.set_aptitude(PhysicalAptitudes.MOVE, random.randrange(4,6))
        self.set_aptitude(PhysicalAptitudes.CONS, random.randrange(1,3))
        self.set_aptitude(PsychicalAptitudes.INTL, 4)
        self.set_aptitude(PsychicalAptitudes.CHAR, 4)
        # compute Wanderer attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC, 60)

        self._speed = self.speed_rule(PhysicalAptitudes.MOVE, 1)
        self._dx = self._dy = self._speed
        self._dir_x = self._dir_y = 0
        self._dir_x = self._dx if random.random() <= 0.5 else -self._dx

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
            elif self._shape._x > self._area[2] and self._dir_x > 0:
                self._dir_x = 0
                self._dir_y = self._dy
            elif self._shape._y < self._area[1] and self._dir_y < 0:
                self._dir_x = self._dx
                self._dir_y = 0
            elif self._shape._y > self._area[3] and self._dir_y > 0:
                self._dir_x = -self._dx
                self._dir_y = 0
            else:
                self.move(self._dir_x, self._dir_y)
                # here we perturbate speed to make it a bit more challenging and fun
                if random.randint(0, 100) == 0:
                    newspeed = random.random() * self._speed
                    self._dir_x = newspeed if self._dir_x != 0 else 0
                    self._dir_y = newspeed if self._dir_y != 0 else 0
