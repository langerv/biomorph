import abc
import arcade
from enum import Enum, auto
from shape import Rectangle


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

    def collide(self, x, y, object):
        half_size = object.Size/2
        return x >= self._x - half_size and x <= self._x + self._width + half_size and y >= self._y - half_size and y <= self._y + self._height + half_size

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

    def update(self, delta_time):
        pass

    def draw(self):
        self._shape.draw()

class LockedWall(Wall):
    def __init__(self, x, y, width, height):
        color = arcade.color.GREEN_YELLOW
        super().__init__(x, y, width, height, color)

    def collide(self, x, y, object):
        return super().collide(x, y, object)

class LaserBeam(Obstacle):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self._target = None
        self._shape = Rectangle(
            x + width/2, 
            y + height/2,
            0,
            width, 
            height, 
            color, 
            1)

    def collide(self, x, y, object):
        if super().collide(x, y, object) is True:
            self._target = object
        else:
            self._target = None
        return False

    def update(self, delta_time):
        if self._target is not None:
            self._target.hit(30)

    def draw(self):
        self._shape.draw()
