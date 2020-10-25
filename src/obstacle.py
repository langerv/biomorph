import abc
import arcade
import random
from enum import Enum, auto
from shape import Rectangle, Ellipse
from aptitude import PsychicalAptitudes


class Obstacle(abc.ABC):

    class type(Enum):
        Wall = auto()
        LockedWall = auto()
        LaserBeam = auto()

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def X(self):
        return self._x

    @property
    def Y(self):
        return self._y

    @property
    def Width(self):
        return self._width

    @property
    def Height(self):
        return self._height

    def get_hint(self):
        return None

    def collide(self, x, y, object):
        half_size = object.Size/2
        return x >= self._x - half_size and x <= self._x + self._width + half_size and y >= self._y - half_size and y <= self._y + self._height + half_size

    @abc.abstractmethod
    def get_color(self):
        pass

    @abc.abstractmethod
    def update(self, delta_time):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
        
class Wall(Obstacle):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self._shape = Rectangle(
            x + width/2, 
            y + height/2,
            0,
            width, 
            height, 
            color)

    '''
    for testing vertical hints
    def get_hint(self):
        return "Wall"
    '''

    def get_color(self):
        return self._shape._color

    def update(self, delta_time):
        pass

    def draw(self):
        self._shape.draw()


class LockedWall(Wall):

    UNLOCK_INT_MIN = 4

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, arcade.color.GREEN_YELLOW)

    def get_hint(self):
        return f"INT > {LockedWall.UNLOCK_INT_MIN - 1}"

    def collide(self, x, y, object):
        if super().collide(x, y, object) is True:
            if object.get_aptitude(PsychicalAptitudes.INTL).Value < LockedWall.UNLOCK_INT_MIN:
                return True
        return False


class LaserBeam(Obstacle):

    HIT_POINTS_LASER = 200
    LASER_SPEED = 12
    LASER_COLOR = arcade.color.VIOLET_RED

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self._target = None
        self._y_beam = y
        self._dy = LaserBeam.LASER_SPEED
        self._shape = Rectangle(
            x + width/2, 
            y + height/2,
            0,
            width, 
            height, 
            color, 
            1)

    def get_color(self):
        return self._shape._color

    def get_hint(self):
        return "SPEED > 3"

    def collide(self, x, y, object):
        if super().collide(x, y, object) is True:
            self._target = object
        else:
            # to refactor if we can have other targets than the player, use a list instead to keep track
            # of the ones inside the LaserBeam area
            self._target = None
        return False

    def update(self, delta_time):
        if self._y_beam <= self._y + 10 and self._dy < 0:
            self._y_beam = self._y
            self._dy *= -1
        elif self._y_beam >= self._y + self._height - 10 and self._dy > 0:
            self._dy_beam = self._y + self._height 
            self._dy *= -1
        else:
            self._y_beam += self._dy

        if self._target is not None:
            half_size = self._target.Size/2
            if self._y_beam >= self._target.Y - half_size and self._y_beam <= self._target.Y + half_size:
                self._target.hurt(LaserBeam.HIT_POINTS_LASER)

    def draw(self):
        self._shape.draw()
        point_list = (
            # with width = 40
            (self._x, self._y_beam),
            (self._x + 5, self._y_beam  + 5*(0.5 - random.random()) ),
            (self._x + 10, self._y_beam + 10*(0.5 - random.random()) ),
            (self._x + 13, self._y_beam + 8*(0.5 - random.random()) ),
            (self._x + 20, self._y_beam + 10*(0.5 - random.random()) ),
            (self._x + 28, self._y_beam + 8*(0.5 - random.random()) ),
            (self._x + 32, self._y_beam + 6*(0.5 - random.random()) ),
            (self._x + 40, self._y_beam)
        )
        arcade.draw_line_strip(point_list, LaserBeam.LASER_COLOR, 2)
