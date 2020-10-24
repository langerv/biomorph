import math
import arcade
from shape import Ellipse
from obstacle import Obstacle
from game_object import GameObject
from biomorph import Biomorph
from aptitude import PhysicalAptitudes, PsychicalAptitudes

'''
Player class
Shape creation:
    Colors (_color) use an HLS system:
    - Intelligence defines COLOR INTENSITY (hLs)
    - Charisma defines COLOR SATURATION (hlS)
    - COLOR HUE is random
    Behaviour 
    - Perception defines the vision RADIUS (_vision)
    - Movement defines the SPEED (_dx, _dy)
    - Constitution defines the SIZE (_size)
    Shape is random between SQUARE, ELLIPSE, ...
'''

class Player(Biomorph, GameObject):

    def __init__(self, x, y, width, height, life, obstacles):
        Biomorph.__init__(self)
        GameObject.__init__(self, x, y)
        self._width = width
        self._height = height
        self._obstacles = obstacles
        self._goal = None
        self._morph_target = None
        self._hue = 0
        self._life = life

        # define aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, 1)
        self.set_aptitude(PhysicalAptitudes.MOVE, 1)
        self.set_aptitude(PhysicalAptitudes.CONS, 1)
        self.set_aptitude(PsychicalAptitudes.INTL, 1)
        self.set_aptitude(PsychicalAptitudes.CHAR, 1)

        # define behaviour and shape
        # create rules to transform aptitudes to behaviours
        self.vision_rule = lambda a, b : self.get_aptitude(a).Value * b
        self.speed_rule = lambda a, b : self.get_aptitude(a).Value # slight advantage for the player here
        self.size_rule = lambda a, b : GameObject.MIN_SHAPE_SIZE + self.get_aptitude(a).Value**b
        self.color_rule = lambda a, b :  self.HLS_to_Color(
            self._hue, # H
            self.get_aptitude(a).Value / 10, # L max is 0.5
            self.get_aptitude(b).Value / 5) # S max is 1.0

        # compute Player attributes
        self._vision = self.vision_rule(PhysicalAptitudes.PERC, 60)
        self._dx = self._dy = self.speed_rule(PhysicalAptitudes.MOVE, 2)
        self._delta = self.Delta_Speed
        self._size = self.size_rule(PhysicalAptitudes.CONS, 2)
        self._color = self.color_rule(PsychicalAptitudes.INTL, PsychicalAptitudes.CHAR)
        self._outline_color =arcade.color.BRANDEIS_BLUE

        # create shape
        self._shape = Ellipse(x, y, 0, self._size/2, self._size/2, self._color, self._outline_color)

    def __str__(self):
        return '    '.join([f"{key.name} = {ap.Value:0.1f}" for key, ap in self.Aptitudes.items()])

    @property
    def Hue(self):
        return self._hue

    @property
    def Life(self):
        return self._life

    @property
    def Vision(self):
        return self._vision

    @property
    def Goal(self):
        return self._goal

    @Goal.setter
    def Goal(self, goal):
        self._goal = goal

    @property
    def Target(self):
        return self._morph_target

    @Target.setter
    def Target(self, target):
        self._morph_target = target

    def hit(self, hit_points):
        self._life = max(self._life - hit_points, 0)

    def move_to(self, goal):
        (x, y) = goal
        dx = x - self._shape._x
        dy = y - self._shape._y
        dist = math.sqrt(dx**2+dy**2)
        if dist >= self._delta:
            if self.move(self._dx * dx/dist, self._dy * dy/dist) is False:
                # we collided then stop
                return True
        else:
            # we arrived
            self._shape._x = x
            self._shape._y = y
            return True
        return False

    def move(self, dx, dy):
        new_x = self._shape._x + dx
        new_y = self._shape._y + dy
        offset = self._size/2
        for obs in self._obstacles:
            if obs.collide(new_x, new_y, offset) is True:
                return False
        self._shape._x = new_x
        self._shape._y = new_y
        return True

    def update(self, delta_time):
        Biomorph.update(self)

        # update behaviours from morphing
        self._vision = self.vision_rule(PhysicalAptitudes.PERC, 60)
        speed = self.speed_rule(PhysicalAptitudes.MOVE, 2)
        if speed != self._dx or speed != self._dy:
            self._dx = self._dy = speed
            self._delta = self.Delta_Speed
        self._size = self.size_rule(PhysicalAptitudes.CONS, 2)
        self._color = self.color_rule(PsychicalAptitudes.INTL, PsychicalAptitudes.CHAR)
        self._shape = Ellipse(self._shape._x, self._shape._y, 0, self._size/2, self._size/2, self._color, self._outline_color)

        # move to Goal if exists
        if self._goal is not None:
            if self.move_to(self._goal) is True:
                self._goal = None

        # morph
        if self._morph_target is not None:
            if self._morph_target.Hit is True:
                if self._morph_target.is_inside(self._shape._x, self._shape._y):
                    # start morphs only when we're above the target
                    print(f"morphing to {self._morph_target}")
                    self.morph(self._morph_target)
                    self._hue = self._morph_target._hue
                    self._morph_target = None
            else:
                self._morph_target = None
