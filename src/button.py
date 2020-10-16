import arcade 
from enum import Enum, auto
from shape import Arrow

class Button():

    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._shape = None

    def is_clicked(self, x, y):
        return x >= self._x and x <= self._x + self._width and y >= self._y and y <= self._y + self._height

    def draw(self):
        self._shape.draw()
 
class ArrowButton(Button):

    class direction(Enum):
        left = auto()
        right = auto()

    def __init__(self, text, x, y, width, height, color, direction):
        super().__init__(x, y, width, height)
        self._text = text
        self._direction = direction
        # compute the angle
        angle = 180 if direction == ArrowButton.direction.left else 0
        # recompute x,y at the center for the shape
        x += width/2 
        y += height/2
        self._shape = Arrow(x, y, angle, width, height, color)

    @property
    def Direction(self):
        return self._direction

    def draw(self):
        super().draw()
        arcade.draw_text(self._text, self._shape._x, self._shape._y, arcade.color.BLACK, 12, anchor_x='center', anchor_y='center')
