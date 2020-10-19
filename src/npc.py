import math
from enum import Enum, auto
from game_object import GameObject
from character import Character

'''
NPC class
'''

class Npc(Character, GameObject):

    HIT_TIMER = 5 # number of seconds before a hit npc goes back to life

    class type(Enum):
        Wanderer = auto()
        Guard = auto()

    def __init__(self, x, y, area):
        Character.__init__(self)
        GameObject.__init__(self, x, y)
        self._width = area[2] - area[0]
        self._height = area[3] - area[1]
        self._center_x = (area[0] + area[2])/2
        self._center_y = (area[1] + area[3])/2
        self._hit = False
        self._hit_time = 0
        self._area = area
        self._hue = 0
        # create rules to transform aptitudes to NPC behaviours
        self.vision_rule = lambda a, b : self.get_aptitude(a).Value * math.sqrt(self._width**2 + self._height**2)/b
        self.speed_rule = lambda a : self.get_aptitude(a).Value
        self.size_rule = lambda a : GameObject.MIN_SHAPE_SIZE + self.get_aptitude(a).Value**2 
        self.color_rule = lambda a, b :  self.HLS_to_Color(
            self._hue, # H
            self.get_aptitude(a).Value / 10, # L max is 0.5
            self.get_aptitude(b).Value / 5) # S max is 1.0

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

    def in_area(self, x, y):
        return x >= self._area[0] and x <= self._area[2] and y >= self._area[1] and y <= self._area[3]

    def look_at(self, x, y):
        dx = x - self._shape._x
        dy = y - self._shape._y
        self._shape._angle = math.atan2(dy, dx) * GameObject.RAD2DEG
        return True

    def move_to(self, x, y):
        dx = x - self._shape._x
        dy = y - self._shape._y
        dist = math.sqrt(dx**2+dy**2)
        if dist > 0:
            return self.move(self._dx * dx/dist, self._dy * dy/dist)
        return True

    def move(self, dx, dy):
        self._shape._x += dx
        self._shape._y += dy
        self._shape._angle = math.atan2(dy, dx) * GameObject.RAD2DEG
        return True
    