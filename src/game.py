import abc
import arcade
import timeit
import random
import math
from shape import Rectangle, Ellipse
from biomorph import Biomorph
from character import Character
from aptitude import PhysicalAptitudes, PsychicalAptitudes

# --- Constants ---
SCREEN_WIDTH =  800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Biomorph game"
WORLD_WIDTH =  2 * SCREEN_WIDTH
WORLD_HEIGHT = 2 * SCREEN_HEIGHT
WORLD_XMIN =  SCREEN_WIDTH/2 - WORLD_WIDTH/2
WORLD_XMAX =  SCREEN_WIDTH/2 + WORLD_WIDTH/2
WORLD_YMIN =  SCREEN_HEIGHT/2 - WORLD_HEIGHT/2
WORLD_YMAX =  SCREEN_HEIGHT/2 + WORLD_HEIGHT/2
NUM_NPC = 30
HIT_TIMER = 5 # number of seconds before a hit npc goes back to life
MIN_SHAPE_SIZE = 20
RAD2DEG = 180 / math.pi

'''
GameObject class
'''
class GameObject(abc.ABC):

    def __init__(self, x, y):
        self._angle = 0
        self._dx = 0
        self._dy = 0
        self._size = MIN_SHAPE_SIZE
        self._color = (0,0,0,0)
        self._shape = None

    @property
    def X(self):
        return self._shape._x

    @property
    def Y(self):
        return self._shape._y

    @property
    def Size(self):
        return self._size

    @property
    def Color(self):
        return self._color

    def is_inside(self, x, y):
        half_size = self._size/2
        return x >= (self._shape._x - half_size) and x <= (self._shape._x + half_size) and y >= (self._shape._y - half_size) and y <= (self._shape._y + half_size)

    @abc.abstractmethod
    def update(self, delta_time):
        pass

    def draw(self):
        self._shape.draw()


'''
Player class
'''
class Player(Biomorph, GameObject):

    def __init__(self, x, y):
        Biomorph.__init__(self)
        GameObject.__init__(self, x, y)
        self._goal = None
        self._morph_target = None
        # define aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, 1)
        self.set_aptitude(PhysicalAptitudes.MOVE, 1)
        self.set_aptitude(PhysicalAptitudes.CONS, 1)
        self.set_aptitude(PsychicalAptitudes.INTL, 1)
        self.set_aptitude(PsychicalAptitudes.CHAR, 1)
        self.set_aptitude(PsychicalAptitudes.ETHQ, 1)
        # define behaviour and shape
        self._vision = self.get_aptitude(PhysicalAptitudes.PERC).Value * max(SCREEN_WIDTH, SCREEN_HEIGHT)/10
        self._dx = self._dy = self.get_aptitude(PhysicalAptitudes.MOVE).Value*2 # gives a slight move advantage to the player
        self._mindist = math.sqrt(self._dx*self._dx+self._dy*self._dy)
        self._size +=  self.get_aptitude(PhysicalAptitudes.CONS).Value**2
        self._color = (
            int(self.get_aptitude(PsychicalAptitudes.INTL).Value * 255/5), # r
            int(self.get_aptitude(PsychicalAptitudes.CHAR).Value * 255/5), # g
            int(self.get_aptitude(PsychicalAptitudes.ETHQ).Value * 255/5)) # b
        self._shape = Ellipse(x, y, 0, self._size, self._size, self._color)

    def __str__(self):
        return '    '.join([f"{key.name} = {ap.Value}" for key, ap in self.Aptitudes.items()])

    @property
    def Vision(self):
        return self._vision

    @property
    def Goal(self):
        return self._goal

    @Goal.setter
    def Goal(self, goal):
        self._goal = goal

    @property
    def Target(self):
        return self._morph_target

    @Target.setter
    def Target(self, target):
        self._morph_target = target

    def update(self, delta_time):
        if self._goal is not None:
            (x, y) = self._goal
            dx = x - self._shape._x
            dy = y - self._shape._y
            dist = math.sqrt(dx*dx+dy*dy)
            if dist >= self._mindist:
                # move
                self._shape._x += self._dx * dx/dist
                self._shape._y += self._dy * dy/dist
            else:
                # we arrived
                self._shape._x = x
                self._shape._y = y
                self._goal = None

        # morph
        if self._morph_target is not None:
            if self._morph_target.Hit is True and self._morph_target.is_inside(self._shape._x, self._shape._y):
                print(f"morphing with {self._morph_target}")
            else:
                self._morph_target = None


'''
NPC class

Shape creation
shape TODO
vision (_vision) depends on PERC aptitude => how to visualize?
speed (_dx, _dy) depends on MOVE aptitude
size (_size) depends on CONST aptitude
color (r,g,b) depends on psychical aptitudes (INTL, CHAR, ETHQ)
'''
class NPC(Character, GameObject):

    def __init__(self, x, y):
        Character.__init__(self)
        GameObject.__init__(self, x, y)
        self._hit = False
        self._hit_time = 0
        # define aptitudes
        self.set_aptitude(PhysicalAptitudes.PERC, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.MOVE, random.randrange(1,6))
        self.set_aptitude(PhysicalAptitudes.CONS, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.INTL, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.CHAR, random.randrange(1,6))
        self.set_aptitude(PsychicalAptitudes.ETHQ, random.randrange(1,6))
        # define behaviour and shape
        self._dx = self._dy = self.get_aptitude(PhysicalAptitudes.MOVE).Value
        self._size += self.get_aptitude(PhysicalAptitudes.CONS).Value**2
        self._color = (
            int(self.get_aptitude(PsychicalAptitudes.INTL).Value * 255/5), # r
            int(self.get_aptitude(PsychicalAptitudes.CHAR).Value * 255/5), # g
            int(self.get_aptitude(PsychicalAptitudes.ETHQ).Value * 255/5)) # b
        self._shape = Rectangle(x, y, 0, self._size, self._size, self._color)

    def __str__(self):
        return '    '.join([f"{key.name} = {ap.Value}" for key, ap in self.Aptitudes.items()])

    @property
    def Hit(self):
        return self._hit

    @Hit.setter
    def Hit(self, value):
        self._hit = value

    def update(self, delta_time):
        if self._hit is True:
            # if a npc is hit, we compute time before to get it back to life
            self._hit_time += delta_time
            if int(self._hit_time) % 60 > HIT_TIMER:
                self._hit_time = 0
                self._hit = False
        else:
            # move
            self._shape._x += self._dx
            self._shape._y += self._dy
            self._shape._angle = math.atan2(self._dy, self._dx) * RAD2DEG
            if self._shape._x < WORLD_XMIN and self._dx < 0:
                self._dx *= -1
            if self._shape._x > WORLD_XMAX and self._dx > 0:
                self._dx *= -1
            if self._shape._y < WORLD_YMIN and self._dy < 0:
                self._dy *= -1
            if self._shape._y > WORLD_YMAX and self._dy > 0:
                self._dy *= -1


'''
GameView class: main gameplay screen
'''
class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        super().__init__()
        self._perf = False
        self._processing_time = 0
        self._draw_time = 0
        self._frame_count = 0
        self._fps_start_timer = None
        self._fps = None
        self._total_time = 0.0        
        self._npcs = None
        self._neighbours = []

    def setup(self):
        x = SCREEN_WIDTH/2 #random.randrange(50, SCREEN_WIDTH-50)
        y = SCREEN_HEIGHT/2 #random.randrange(50, SCREEN_HEIGHT-50)
        self._player = Player(x, y)
        self._npcs = []
        for _ in range(NUM_NPC):
            x = random.randrange(WORLD_XMIN, WORLD_XMAX)
            y = random.randrange(WORLD_YMIN, WORLD_YMAX)
            self._npcs.append(NPC(x, y))

    def on_draw(self):
        # Start timing how long this takes and count frames
        draw_start_time = timeit.default_timer()
        if self._frame_count % 60 == 0:
            if self._fps_start_timer is not None:
                total_time = timeit.default_timer() - self._fps_start_timer
                self._fps = 60 / total_time
            self._fps_start_timer = timeit.default_timer()
        self._frame_count += 1

        # render game stuffs
        arcade.start_render()

        # draw perception lines between player and perceived shapes
        line_list = arcade.ShapeElementList()
        for npc in self._neighbours:
            line_list.append(arcade.create_line(
                self._player.X, 
                self._player.Y,
                npc.X, 
                npc.Y,
                npc.Color, 
                2))
        line_list.draw()

        # render NPCs and Player
        for npc in self._npcs:
            npc.draw()
        self._player.draw()

        # display game infos
        minutes = int(self._total_time) // 60
        seconds = int(self._total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT - 35, arcade.color.WHITE, 25)
        arcade.draw_text(str(self._player), 150, 16, arcade.color.WHITE, 14)

        # display performance
        if self._perf:
            # Display timings
            output = f"Processing time: {self._processing_time:.3f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 15, arcade.color.WHITE, 12)
            output = f"Drawing time: {self._draw_time:.3f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 30, arcade.color.WHITE, 12)
            if self._fps is not None:
                output = f"FPS: {self._fps:.0f}"
                arcade.draw_text(output, 20, SCREEN_HEIGHT - 45, arcade.color.WHITE, 12)

        self._draw_time = timeit.default_timer() - draw_start_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.F1:
            self._perf = not self._perf
        
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # test if we've hit a npc
            for npc in self._neighbours:
                 if npc.is_inside(x, y):
                    if npc.Hit is False:
                        npc.Hit = True
                    else:
                        self._player.Target = npc
            # move player
            self._player.Goal = (x, y)

    def on_update(self, delta_time):
        start_time = timeit.default_timer()
        self._player.update(delta_time)
        self._neighbours = []
        squared_vision = self._player.Vision**2
        for npc in self._npcs:
            npc.update(delta_time)
            dx = npc.X - self._player.X
            dy = npc.Y - self._player.Y
            if (dx*dx+dy*dy) < squared_vision:
                self._neighbours.append(npc)

        self._total_time += delta_time
        self._processing_time = timeit.default_timer() - start_time

'''
main function: initialize and start the game screens
'''
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    start_view.setup()
    window.set_update_rate(1/40)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()