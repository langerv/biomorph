import abc
import math
import colorsys

'''
Base class for game objects
properties
- position
- angle 
- speed
- shape to draw
- size 
- color
'''

class GameObject(abc.ABC):

    RAD2DEG = 180 / math.pi
    MIN_SHAPE_SIZE = 20

    def __init__(self, x, y):
        self._angle = 0
        self._dx = 0
        self._dy = 0
        self._size = 0
        self._shape = None

    @property
    def X(self):
        return self._shape._x

    @property
    def Y(self):
        return self._shape._y

    @property
    def Speed(self):
        return math.sqrt(self._dx**2 + self._dy**2)

    @property
    def Size(self):
        return self._size

    @property
    def Color(self):
        return self._shape._color

    def HLS_to_Color(self, h, l,s):
        (r, g, b) = colorsys.hls_to_rgb(h, l, s)
        return (round(r*255), round(g*255), round(b*255))

    def is_inside(self, x, y):
        half_size = self._size/2
        return x >= (self._shape._x - half_size) and x <= (self._shape._x + half_size) and y >= (self._shape._y - half_size) and y <= (self._shape._y + half_size)

    def draw(self):
        self._shape.draw()

    @abc.abstractmethod
    def update(self, delta_time):
        pass
