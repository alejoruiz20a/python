import arcade 
import random

# CONSTANTES 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Jump Game"

BACKGROUD_COLOR = arcade.color.BLACK
PLAYER_COLOR = arcade.color.BLUE
PLATFORM_COLOR = arcade.color.WHITE
SPIKE_COLOR = arcade.color.RED

GRAVITY = -1.2
JUMP_SPEED= 20
INITIAL_SPEED = 6
SPEED_UP_RATE = 0.005
GROUND_HEIGHT = 100

CUBE_SIZE = 40

class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.velocity_y = 0
        self.is_jumping = False
        self.is_alive = True

    def update(self):
        if not self.is_alive:
            return
        
        # Gravedad
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        # Verificar si está en el suelo
        if self.y <= GROUND_HEIGHT: # LUEGO VEMOS POR QUÉ ESTO SE DEBE MODIFICAR
            self.y = GROUND_HEIGHT
            self.velocity_y = 0
            self.is_jumping = False

    def jump(self):
        if not self.is_jumping and self.is_alive:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True

    def draw(self):
        if self.is_alive:
            half = self.size / 2

            points = [
                (self.x - half, self.y - half),
                (self.x + half, self.y - half),
                (self.x + half, self.y + half),
                (self.x - half, self.y + half)
            ]

            arcade.draw_polygon_filled(points, PLAYER_COLOR)
            arcade.draw_polygon_outline(points, arcade.color.WHITE, 2)
    
    def get_hitbox(self):
        half = self.size / 2
        return {
            'left': self.x - half,
            'right': self.x + half,
            'bottom': self.y - half,
            'top': self.y + half,
        }
    
class Spike():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed = INITIAL_SPEED

    def update(self, current_speed):
        self.x -= current_speed

    def is_off_screen(self):
        return self.x<-50
    
    def draw(self):
        half = self.size / 2
        points = [
            (self.x, self.y + self.size),
            (self.x - half, self.y),
            (self.x + half, self.y),
        ]

        arcade.draw_polygon_filled(points, SPIKE_COLOR)
        arcade.draw_polygon_outline(points, arcade.color.WHITE, 2)

    def check_collision(self, player):
        half = self.size / 2

        player_box = player.get_hitbox()

        spike_left = self.x - half
        spike_right = self.x + half
        spike_bottom = self.y
        spike_top = self.y + self.size

        return (player_box['right'] > spike_left and
                player_box['left'] < spike_right and
                player_box['bottom'] < spike_top and
                player_box['top'] > spike_bottom)

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUD_COLOR)

        self.player = None
        self.spikes = []
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        self.music = None
        self.current_speed = INITIAL_SPEED