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

    def hover(self, x, y):
        pass

    def is_inside(self, x, y):
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
        self._color = color
        self._hover = False
        # compute the angle
        angle = 185 if direction == ArrowButton.direction.left else 5
        # recompute x,y at the center for the shape
        x += width/2 
        y += height/2
        self._shape = Arrow(x, y, angle, width, height, color)

    @property
    def Direction(self):
        return self._direction

    def hover(self, x, y):
        if self.is_inside(x, y):
            if self._hover is False:
                # is_inside() is True and _hover is False then change color
                self._shape = Arrow(self._shape._x, self._shape._y, self._shape._angle, self._shape._width, self._shape._height, arcade.color.RED_ORANGE)
                self._hover = True
        elif self._hover is True:
            # is_inside() is False and _hover is True then change color back to non hover
            self._shape = Arrow(self._shape._x, self._shape._y, self._shape._angle, self._shape._width, self._shape._height, self._color)
            self._hover = False

    def draw(self):
        super().draw()
        arcade.draw_text(self._text, self._shape._x, self._shape._y, arcade.color.BLACK, 12, anchor_x='center', anchor_y='center', rotation=5)
