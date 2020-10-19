import arcade 
from enum import Enum, auto
from shape import Arrow


class ButtonType(Enum):
    button = auto()
    arrow_left = auto()
    arrow_right = auto()


class Button():

    def __init__(self, x, y, width, height, type, color, color_hover):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._type = type
        self._color = color
        self._color_hover = color_hover
        self._hover = False
        self._shape = None

    @property
    def Type(self):
        return self._type

    ''' Hover logic '''
    def is_hover(self, x, y):
        if x >= self._x and x <= self._x + self._width and y >= self._y and y <= self._y + self._height:
            if self._hover is False:
                self._shape = Arrow(self._shape._x, self._shape._y, self._shape._angle, self._shape._width, self._shape._height, self._color_hover)
                self._hover = True
            return True
        elif self._hover is True:
            self._shape = Arrow(self._shape._x, self._shape._y, self._shape._angle, self._shape._width, self._shape._height, self._color)
            self._hover = False
        return False

    def draw(self):
        self._shape.draw()
 
class ArrowButton(Button):

    def __init__(self, text, x, y, width, height, type, color, color_hover, color_text=arcade.color.BLACK):
        super().__init__(x, y, width, height, type, color, color_hover)
        self._text = text
        self._color_text = color_text
        # compute angle and x,y at the center of the shape
        angle = 185 if type == ButtonType.arrow_left else 5
        self._shape = Arrow(x + width/2, y + height/2, angle, width, height, color)

    def draw(self):
        super().draw()
        arcade.draw_text(
            self._text, 
            self._shape._x, 
            self._shape._y,
            self._color_text, 
            12, 
            anchor_x='center', 
            anchor_y='center', 
            rotation=5)
