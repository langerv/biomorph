import arcade 

class Shape():
    def __init__(self, x, y, angle, width, height, color):
        self._x = x
        self._y = y
        self._angle = angle
        self._width = width
        self._height = height
        self._color = color
        self._shape_list = None

    def draw(self):
        self._shape_list.center_x = self._x
        self._shape_list.center_y = self._y
        self._shape_list.angle = self._angle
        self._shape_list.draw()


class Arrow(Shape):
    def __init__(self, x, y, angle, width, height, color):
        super().__init__(x, y, angle, width, height, color)
        point_list = (
            (0, 0.1*height),
            (0.7*width, 0.1*height),
            (0.7*width, 0.2*height),
            (width, 0),
            (0.7*width, -0.2*height),
            (0.7*width, -0.1*height),
            (0, -0.1*height)
        )
        self._shape_list = arcade.ShapeElementList()
        self._shape_list.append(arcade.create_polygon(
            point_list, 
            color)
        )



class Rectangle(Shape):
    def __init__(self, x, y, angle, width, height, color):
        super().__init__(x, y, angle, width, height, color)
        self._shape_list = arcade.ShapeElementList()
        self._shape_list.append(arcade.create_rectangle_filled(
            0, 0, 
            self._width, 
            self._height, 
            self._color, 
            self._angle)
        )


class Ellipse(Shape):
    def __init__(self, x, y, angle, width, height, color, outline_color=None):
        super().__init__(x, y, angle, width, height, color)
        self._shape_list = arcade.ShapeElementList()
        self._shape_list.append(arcade.create_ellipse_filled(
            0, 0, 
            self._width, 
            self._height, 
            self._color, 
            self._angle)
        )
        if outline_color is not None:
            self._shape_list.append(arcade.create_ellipse_outline(
                0, 0, 
                self._width, 
                self._height,
                outline_color)
            )


