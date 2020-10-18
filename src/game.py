import arcade
import timeit
import math
import random
from shape import Rectangle, Ellipse
from game_object import GameObject
from player import Player
from npc import Npc
from wanderer import Wanderer
from guard import Guard
from button import ArrowButton, ButtonType

# --- Constants ---
SCREEN_WIDTH =  800
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Biomorph game"
WORLD_WIDTH =  2 * SCREEN_WIDTH
WORLD_HEIGHT = 2 * SCREEN_HEIGHT
WORLD_XMIN =  SCREEN_WIDTH/2 - WORLD_WIDTH/2
WORLD_XMAX =  SCREEN_WIDTH/2 + WORLD_WIDTH/2
WORLD_YMIN =  SCREEN_HEIGHT/2 - WORLD_HEIGHT/2
WORLD_YMAX =  SCREEN_HEIGHT/2 + WORLD_HEIGHT/2
PLAYER_INIT_LIFE = 1000

# --- Game levels ---

LEVEL_1 = {
    'name': 'Level 1',
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
    'name': 'Level 2',
    'map' : {
        'color1':(10,5,5), 
        'color2':(20,10,10),
        'obstacles' : [
            {
                'color':arcade.color.BLUE_GREEN,
                'rectangle':(0, SCREEN_HEIGHT - 190, 300, 40) # rectangle is (x, y, width, height)
            },
            {
                'color':arcade.color.BLUE_GREEN,
                'rectangle':(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 190, 300, 40)
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
            'area':(330, SCREEN_HEIGHT - 145, 470, SCREEN_HEIGHT - 105)}
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
        #  game over variable and effect
        self._game_over = False
        self._blink = False
        self._font_size = 20
        self._font_size_delta = 2
        self._font_angle = 0
        self._font_angle_delta = 10

    def setup(self, level, next_level=None, prev_level=None):
        # level
        self._level_name = level['name'] if 'name' in level else ""
        self._background_shape = arcade.ShapeElementList()
        self._level = level

        # load map
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

        # load player
        if 'player' in level:
            player_dict = level['player']
            if 'pos' in player_dict:
                pos = player_dict['pos']
                self._player = Player(
                    pos[0], 
                    pos[1], 
                    SCREEN_WIDTH, 
                    SCREEN_HEIGHT, 
                    PLAYER_INIT_LIFE, 
                    self._obstacles)
            else:
                # we need a player so by default position is the center of the screen
                self._player = Player(
                    SCREEN_WIDTH/2, 
                    SCREEN_HEIGHT/2, 
                    SCREEN_WIDTH, 
                    SCREEN_HEIGHT, 
                    PLAYER_INIT_LIFE, 
                    self._obstacles)

        # load npcs        
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
                                    self._npcs.append(Wanderer(
                                        x, 
                                        y, 
                                        area))
                                elif npc_class == Npc.type.Guard:
                                    self._npcs.append(Guard(
                                        x, 
                                        y, 
                                        area))

        # add buttons and flow
        self._buttons = []
        self._button_hover = None
        if next_level is not None:
            self._buttons.append(
                ArrowButton(
                    "Next", 
                    SCREEN_WIDTH - 50, 
                    SCREEN_HEIGHT - 40, 
                    30, 
                    35, 
                    ButtonType.arrow_right, 
                    arcade.color.ORANGE_PEEL, 
                    arcade.color.RED_ORANGE,
                    arcade.color.BLACK_BEAN)
            )

        if prev_level is not None:
            self._buttons.append(
                ArrowButton(
                    "Back", 
                    20, 
                    SCREEN_HEIGHT - 40, 
                    30, 
                    35, 
                    ButtonType.arrow_left, 
                    arcade.color.ORANGE_PEEL,
                    arcade.color.RED_ORANGE,
                    arcade.color.BLACK_BEAN)
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
        text_y = 14
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

        # game over screen
        if self._game_over is True:
            
            self._font_size += self._font_size_delta
            if self._font_size > 60 or self._font_size < 20:
                self._font_size_delta *= -1

            self._font_angle += self._font_angle_delta 
            if self._font_angle >= 363:
                self._font_angle = 3
                self._font_angle_delta = 0

            if self._frame_count % 20 == 0:
                self._blink = not self._blink

            arcade.draw_text(
                "GAME OVER!\n", 
                SCREEN_WIDTH/2, 
                SCREEN_HEIGHT/2, 
                arcade.color.WHITE, 
                font_size=self._font_size, #40,
                anchor_x="center",
                anchor_y="center",
                rotation=self._font_angle)

            if self._blink is True:
                arcade.draw_text(
                    "Click to REPLAY!", 
                    SCREEN_WIDTH/2, 
                    SCREEN_HEIGHT/2-70,
                    arcade.color.GREEN_YELLOW, 
                    font_size=20, 
                    anchor_x="center",
                    rotation=-3)

        # display game infos
        arcade.draw_text(
            str(self._level_name), 
            SCREEN_WIDTH/2, 
            SCREEN_HEIGHT - 25, 
            arcade.color.WHITE, 20, 
            anchor_x='center')

        # time info
        minutes = int(self._total_time) // 60
        seconds = int(self._total_time) % 60
        output = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(
            output, 
            SCREEN_WIDTH/2, 
            SCREEN_HEIGHT - 55, 
            arcade.color.WHITE, 
            25, 
            anchor_x='center')

        # player info
        arcade.draw_text(
            f"Life: {self._player.Life:.0f}", 
            SCREEN_WIDTH/2, 
            text_y + 20, 
            arcade.color.RED if self._player.Life < 200 else arcade.color.WHITE, 
            20, 
            anchor_x='center')

        arcade.draw_text(
            str(self._player), 
            SCREEN_WIDTH/2, 
            14,
            arcade.color.WHITE, 
            14, 
            anchor_x='center')

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
        for button in self._buttons:
            if button.is_hover(x, y):
                self._button_hover = button
                break
        else:
            self._button_hover = None

    '''
    Game flow to refactor
    '''
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # check is buttons have been clicked
            if self._button_hover is not None:
                if self._button_hover.Type == ButtonType.arrow_right:
                    if self._level == LEVEL_1:
                        start_view = GameView()
                        start_view.setup(LEVEL_2, None, LEVEL_1)
                        self.window.show_view(start_view)
                elif self._button_hover.Type == ButtonType.arrow_left:
                    if self._level == LEVEL_2:
                        start_view = GameView()
                        start_view.setup(LEVEL_1, LEVEL_2, None)
                        self.window.show_view(start_view)

        # in a game over state, just relaunch the same scene
        if self._game_over is True:
            start_view = GameView()
            start_view.setup(LEVEL_2, None, LEVEL_1)
            self.window.show_view(start_view)

        # test if we've hit a npc
        for (npc, _) in self._player_neighbours:
            if npc.is_inside(x, y):
                if npc.Hit is False:
                    npc.Hit = True
                    return
                else:
                    self._player.Target = npc

        # set playe goal
        self._player.Goal = (x, y)

    def on_update(self, delta_time):
        # end game condition
        if self._game_over is True:
            return
        elif self._player.Life == 0:
            self._game_over = True
            return

        start_time = timeit.default_timer()

        # update player
        self._player.update(delta_time)

        # update NPCs and compute player's neigbourhood
        self._player_neighbours = []
        squared_vision = self._player.Vision**2
        for npc in self._npcs:
            npc.update([self._player], delta_time)
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
        if self._title_color[3] > 100 and self._count_frame % 20 == 0:
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
            anchor_y="center",
            rotation=3)

        if self._blink is True:
            arcade.draw_text(
                "Click to PLAY!", 
                SCREEN_WIDTH/2, 
                SCREEN_HEIGHT/2-75, 
                arcade.color.GREEN_YELLOW, 
                font_size=20, 
                anchor_x="center",
                rotation=-3)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        start_view = GameView()
        start_view.setup(LEVEL_1, LEVEL_2)
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