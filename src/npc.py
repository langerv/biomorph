import math
import random
import arcade
from enum import Enum, auto
from shape import Rectangle, Ellipse
from game_object import GameObject
from character import Character
from aptitude import PhysicalAptitudes, PsychicalAptitudes

RAD2DEG = 180 / math.pi


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
        self._hit = False
        self._hit_time = 0
        self._area = area
        self._hue = 0
        # create rules to transform aptitudes to NPC behaviours
        self.vision_rule = lambda a : self.get_aptitude(a).Value * max(self._width, self._height)/2
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

    def move(self, dx, dy):
        self._shape._x += dx
        self._shape._y += dy
        self._shape._angle = math.atan2(dy, dx) * RAD2DEG
        return True


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
        self._closest_target = None
        # design Guard aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, 3)
        self.set_aptitude(PhysicalAptitudes.MOVE, 3)
        self.set_aptitude(PhysicalAptitudes.CONS, 5)
        self.set_aptitude(PsychicalAptitudes.INTL, 2)
        self.set_aptitude(PsychicalAptitudes.CHAR, 2)
        # compute Guard attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC)
        speed = self.speed_rule(PhysicalAptitudes.MOVE)
        if self._width >= self._height:
            self._dx = speed
        else:
            self._dy = speed
        self._size = self.size_rule(PhysicalAptitudes.CONS)
        self._hue = 0
#        self._color = self.color_rule(PsychicalAptitudes.INTL, PsychicalAptitudes.CHAR)
        self._color = arcade.color.RED
        # create shape
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)

    def update(self, neighbours, delta_time):

        # perception
        closest = self._vision
        for neighbour in neighbours:
            dx = neighbour.X - self._shape._x
            dy = neighbour.Y - self._shape._y
            dist = math.sqrt(dx**2 + dy**2)
            if dist < closest:
                self._closest_target = neighbour
                closest = dist

        # action: Guard FSM
        if self._state == Guard.state.idle:
            self._state = Guard.state.patrol

        elif self._state == Guard.state.patrol:
            if closest < self._vision:
                self._state = Guard.state.watch
            else:
                # patrol
                if self._shape._x < self._area[0] and self._dx < 0:
                    self._dx *= -1
                if self._shape._x > self._area[2] and self._dx > 0:
                    self._dx *= -1
                if self._shape._y < self._area[1] and self._dy < 0:
                    self._dy *= -1
                if self._shape._y > self._area[3] and self._dy > 0:
                    self._dy *= -1
                self.move(self._dx, self._dy)

        elif self._state == Guard.state.watch:
            # watch
            print(f"{self._state}")
            if closest >= self._vision:
                self._state = Guard.state.patrol
            elif closest < self._vision/2:
                self._state = Guard.state.attack

        elif self._state == Guard.state.attack:
            # attack
            print(f"{self._state}")
            if closest >= self._vision/2:
                self._state = Guard.state.watch


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
        self._vision = self.vision_rule(PhysicalAptitudes.PERC)
        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE)
        self._size = self.size_rule(PhysicalAptitudes.CONS)
        self._hue = random.random()
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
            # wander
            if self._shape._x < self._area[0] and self._dx < 0:
                self._dx *= -1
            if self._shape._x > self._area[2] and self._dx > 0:
                self._dx *= -1
            if self._shape._y < self._area[1] and self._dy < 0:
                self._dy *= -1
            if self._shape._y > self._area[3] and self._dy > 0:
                self._dy *= -1
            self.move(self._dx, self._dy)
