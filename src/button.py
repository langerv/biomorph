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

    def __init__(self, text, x, y, width, height, color, dir, data=None):
        super().__init__(x, y, width, height)
        self._text = text
        self._data = data
        angle = 0
        if dir == ArrowButton.direction.left:
            angle = 180
        x += width/2
        y += height/2
        self._shape = Arrow(x, y, angle, width, height, color)

    @property
    def Data(self):
        return self._data

    def draw(self):
        super().draw()
        arcade.draw_text(self._text, self._shape._x, self._shape._y, arcade.color.BLACK, 12, anchor_x='center', anchor_y='center')
