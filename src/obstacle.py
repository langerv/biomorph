import abc
import arcade
from enum import Enum, auto
from shape import Rectangle


class Obstacle(abc.ABC):

    class type(Enum):
        Wall = auto()
        LockedWall = auto()

    def __init__(self, x, y, width, height, color):
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

    def collide(self, x, y, half_size):
        return x > self._x - half_size and x < self._x + self._width + half_size and y > self._y - half_size and y < self._y + self._height + half_size

    @abc.abstractmethod
    def update(self, delta_time):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
        
class Wall(Obstacle):

    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
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
        color = arcade.color.RED_DEVIL
        super().__init__(x, y, width, height, color)

    def collide(self, x, y, half_size):
        return False