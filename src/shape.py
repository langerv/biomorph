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
            (-0.5*width, 0.3*height),
            (0.5*width, 0.25*height),
            (0.5*width,  0.5*height),
            (1.0*width, 0),
            (0.5*width, -0.5*height),
            (0.5*width, -0.25*height),
            (-0.5*width, -0.3*height)
        )
        self._shape_list = arcade.ShapeElementList()
        self._shape_list.append(arcade.create_polygon(
            point_list, 
            color)
        )


class Rectangle(Shape):
    def __init__(self, x, y, angle, width, height, color, outline=0):
        super().__init__(x, y, angle, width, height, color)
        self._shape_list = arcade.ShapeElementList()
        if outline == 0:
            self._shape_list.append(arcade.create_rectangle_filled(
                0, 0, 
                self._width, 
                self._height, 
                self._color, 
                self._angle)
            )
        else:
            self._shape_list.append(arcade.create_rectangle_outline(
                0, 0, 
                self._width, 
                self._height, 
                self._color, 
                outline,
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


