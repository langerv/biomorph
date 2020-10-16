import arcade
import timeit
import math
import random
from shape import Rectangle, Ellipse
from game_object import GameObject
from player import Player
from npc import Npc, Wanderer, Guard
from button import ArrowButton

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


# --- Game levels ---

LEVEL_1 = {
    'name': 'level 1',
    'map': {
        'color1':(5,10,5), 
        'color2':(10,20,10)
        },
    'player': {
        'pos':(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        },
    'npc' : [
        {
            'class': Npc.type.Wanderer,
            'quantity':30, 
            'area':(WORLD_XMIN, WORLD_YMIN, WORLD_XMAX, WORLD_YMAX)}
    ]
}

LEVEL_2 = {
    'name': 'level 2',
    'map' : {
        'color1':(10,5,5), 
        'color2':(20,10,10),
        'obstacles' : [
            {
                'color':arcade.color.BLUE_GREEN,
                'rectangle':(0,450,300,50) # (x, y, width, height)
            },
            {
                'color':arcade.color.BLUE_GREEN,
                'rectangle':(500,450,300,50)
            }
        ]
    },
    'player': {
        'pos':(SCREEN_WIDTH/2, 100)
        },
    'npc' : [
        {
            'class': Npc.type.Wanderer,
            'quantity':30, 
            'area':(WORLD_XMIN, WORLD_YMIN, WORLD_XMAX, 400)},
        {
            'class': Npc.type.Guard,
            'quantity':1,
            'area':(330,470,470,520)}
    ]
}


'''
GameView: gameplay screen
'''

class GameView(arcade.View):

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
        self._player_neighbours = []
        self._buttons = []

    def setup(self, level):
        self._level_name = level['name'] if 'name' in level else ""
        self._background_shape = arcade.ShapeElementList()
        self._map = arcade.ShapeElementList()
        self._obstacles = []
        if 'map' in level:
            map_dict = level['map']
            if 'color1' in map_dict:
                color1 = map_dict['color1']
                if 'color2' in map_dict:
                    color2 = map_dict['color2']
                    points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
                    colors = (color1, color1, color2, color2)
                    rect = arcade.create_rectangle_filled_with_colors(points, colors)
                    self._background_shape.append(rect)

            if 'obstacles' in map_dict:
                for obstacle in map_dict['obstacles']:
                    if 'color' in obstacle:
                        point_list = None
                        if 'rectangle' in obstacle:
                            (x, y, width, height) = obstacle['rectangle']
                            point_list = [
                                (x, y), # xmin, ymin
                                (x+width, y), #xmax, ymin
                                (x+width, y+height), #xmax, ymax
                                (x, y+height)] #xmin, ymax

                        if point_list is not None:
                            self._obstacles.append((x, y, width, height))
                            self._map.append(arcade.create_polygon(
                                    point_list,
                                    obstacle['color']))

        if 'player' in level:
            player_dict = level['player']
            if 'pos' in player_dict:
                pos = player_dict['pos']
                self._player = Player(pos[0], pos[1], SCREEN_WIDTH, SCREEN_HEIGHT, self._obstacles)
            else:
                # we need a player so by default position is the center of the screen
                self._player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self._obstacles)
        
        self._npcs = []
        if 'npc' in level:
            for npc_dict in level['npc']:
                if 'class' in npc_dict:
                    npc_class = npc_dict['class']
                    if 'quantity' in npc_dict:
                        num = npc_dict['quantity']
                        if 'area' in npc_dict:
                            area = npc_dict['area']
                            for _ in range(num):
                                x = random.randrange(area[0], area[2])
                                y = random.randrange(area[1], area[3])
                                if npc_class == Npc.type.Wanderer:
                                    self._npcs.append(Wanderer(x, y, area))
                                elif npc_class == Npc.type.Guard:
                                    self._npcs.append(Guard(x, y, area))

        # buttons
        self._buttons.append(
            ArrowButton("Next", 730, 570, 60, 100, arcade.color.ORANGE_PEEL, ArrowButton.direction.right)
        )
        self._buttons.append(
            ArrowButton("Previous", 0, 570, 60, 100, arcade.color.ORANGE_PEEL, ArrowButton.direction.left)
        )

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
        self._background_shape.draw()
        self._map.draw()
        
        # draw perception lines between player and perceived shapes
        line_list = arcade.ShapeElementList()
        for (npc, squared_dist) in self._player_neighbours:
            if squared_dist > 0:
                line_list.append(arcade.create_line(
                    self._player.X, 
                    self._player.Y,
                    npc.X, 
                    npc.Y,
                    npc.Color,
                    2))
        else:
            line_list.draw()

        # render NPCs
        text_y = 16
        for npc in self._npcs:
            npc.draw()
            if npc.Hit is True:
                text_y += 16
                arcade.draw_text(str(npc), SCREEN_WIDTH/2, text_y, npc.Color, 14, anchor_x='center')

        # render player
        self._player.draw()

        # render buttons
        for button in self._buttons:
            button.draw()

        # display game infos
        minutes = int(self._total_time) // 60
        seconds = int(self._total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(output, SCREEN_WIDTH/2, SCREEN_HEIGHT - 35, arcade.color.WHITE, 25, anchor_x='center')
        arcade.draw_text(str(self._player), SCREEN_WIDTH/2, 16, arcade.color.WHITE, 14, anchor_x='center')

        # display performance
        if self._perf:
            # Display timings
            output = f"Processing time: {self._processing_time:.3f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 15, arcade.color.GREEN, 12)
            output = f"Drawing time: {self._draw_time:.3f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 30, arcade.color.GREEN, 12)
            if self._fps is not None:
                output = f"FPS: {self._fps:.0f}"
                arcade.draw_text(output, 20, SCREEN_HEIGHT - 45, arcade.color.RED, 12)

        self._draw_time = timeit.default_timer() - draw_start_time

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.F1:
            self._perf = not self._perf
        #elif key == arcade.key.SPACE:
        #    self.window.set_fullscreen(not self.window.fullscreen)
        #    self.window.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # test buttons
            for button in self._buttons:
                if button.is_clicked(x, y) is True:
                    start_view = GameView()
                    start_view.setup(LEVEL_2)
                    self.window.show_view(start_view)

            # test if we've hit a npc
            for (npc, _) in self._player_neighbours:
                 if npc.is_inside(x, y):
                    if npc.Hit is False:
                        npc.Hit = True
                        return
                    else:
                        self._player.Target = npc
            # move player
            self._player.Goal = (x, y)

    def on_update(self, delta_time):
        start_time = timeit.default_timer()
        self._player.update(delta_time)
        self._player_neighbours = []
        squared_vision = self._player.Vision**2
        for npc in self._npcs:
            npc.update(delta_time)
            if npc.X > 0 and npc.Y < SCREEN_WIDTH and npc.Y > 0 and npc.Y < SCREEN_HEIGHT: # cannot be perceived outside of screen  boundaries
                dx = npc.X - self._player.X
                dy = npc.Y - self._player.Y
                squared_dist = dx**2+dy**2
                if squared_dist < squared_vision: # and only if in range of player's perception
                    self._player_neighbours.append((npc, squared_dist))

        self._total_time += delta_time
        self._processing_time = timeit.default_timer() - start_time


'''
MenuView screen
'''

class MenuView(arcade.View):

    def on_show(self):
        self._background_shape = arcade.ShapeElementList()
        color1 = (5,10,5)
        color2 = (10,20,10)
        points = (0, 0), (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT)
        colors = (color1, color1, color2, color2)
        rect = arcade.create_rectangle_filled_with_colors(points, colors)
        self._background_shape.append(rect)
        self._alpha_delta = 2
        self._title_color = [180, 230, 180, 0] 
        self._count_frame = 0
        self._blink = False
    
    def on_update(self, delta_time):
        self._count_frame += 1
        self._title_color[3] = 255 if self._title_color[3] >= 255 else self._title_color[3] + self._alpha_delta
        if self._title_color[3] > 200 and self._count_frame % 20 == 0:
            self._blink = not self._blink

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_draw(self):
        arcade.start_render()
        self._background_shape.draw()

        arcade.draw_text(
            "A Biomorph little game :-)\n", 
            SCREEN_WIDTH/2, 
            SCREEN_HEIGHT/2 + 75, 
            self._title_color, 
            font_size=40,
            anchor_x="center",
            anchor_y="center")

        if self._blink is True:
            arcade.draw_text(
                "Click to PLAY!", 
                SCREEN_WIDTH/2, 
                SCREEN_HEIGHT/2-75, 
                arcade.color.GREEN_YELLOW, 
                font_size=20, 
                anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        start_view = GameView()
        start_view.setup(LEVEL_1)
        self.window.show_view(start_view)

'''
main function: initialize and start the game screens
'''
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    window.set_update_rate(1/40)
    arcade.run()
 

if __name__ == "__main__":
    main()