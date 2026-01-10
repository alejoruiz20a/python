import arcade 
import random
import math

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
        self.rotation = 0

    def update(self):
        if not self.is_alive:
            return
        
        # Gravedad
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.is_jumping:
            self.rotation -= 5

        # Verificar si está en el suelo
        if self.y <= GROUND_HEIGHT + CUBE_SIZE/2: # LUEGO VEMOS POR QUÉ ESTO SE DEBE MODIFICAR
            self.y = GROUND_HEIGHT + CUBE_SIZE/2
            self.velocity_y = 0
            self.is_jumping = False
            self.rotation = 0

    def jump(self):
        if not self.is_jumping and self.is_alive:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True

    def draw(self):
        if self.is_alive:
            half = self.size / 2

            points = [
                (-half, -half),
                (half, -half),
                (half, half),
                (-half, half)
            ]

            angle_rad = math.radians(self.rotation)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            rotated_points = []
            for px, py in points:
                new_x = px * cos_a - py*sin_a + self.x
                new_y = px * sin_a + py*cos_a + self.y
                rotated_points.append((new_x, new_y))

            arcade.draw_polygon_filled(rotated_points, PLAYER_COLOR)
            arcade.draw_polygon_outline(rotated_points, arcade.color.WHITE, 2)
    
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
        self.music_player = None
        self.current_speed = INITIAL_SPEED

    def setup(self): 
        self.player = Player(150, GROUND_HEIGHT, CUBE_SIZE)
        self.spikes = []
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False
        self.current_speed = INITIAL_SPEED

        if self.music_player:
            self.music_player.pause()

        try:
            self.music = arcade.load_sound("background_music.mp3")
            self.music_player = arcade.play_sound(self.music, loop=True)
        except:
            print("No se pudo cargar la musica de fondo")

    def on_draw(self):
        self.clear()

        platform_points = [
            (0,0),
            (SCREEN_WIDTH,0),
            (SCREEN_WIDTH, GROUND_HEIGHT),
            (0, GROUND_HEIGHT)
        ]
        arcade.draw_polygon_filled(platform_points, PLATFORM_COLOR)

        self.player.draw()

        for spike in self.spikes:
            spike.draw()

        arcade.draw_text(f"Puntuación: {self.score}",10, SCREEN_HEIGHT-30,arcade.color.WHITE, 20)
        arcade.draw_text(f"Velocidad: {self.current_speed}",10, SCREEN_HEIGHT-60,arcade.color.WHITE, 20)

        if self.game_over:
            self.music_player.pause()
            box_points = [
                (SCREEN_WIDTH/2-200,SCREEN_HEIGHT/2-100),
                (SCREEN_WIDTH/2+200,SCREEN_HEIGHT/2-100),
                (SCREEN_WIDTH/2+200,SCREEN_HEIGHT/2+100),
                (SCREEN_WIDTH/2-200,SCREEN_HEIGHT/2+100)
            ]
            arcade.draw_polygon_filled(box_points, arcade.color.BLACK)
            arcade.draw_polygon_outline(box_points, arcade.color.RED, 3)

            arcade.draw_text("FIN DEL JUEGO", SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2+30, arcade.color.RED, 40)
            arcade.draw_text(f"Puntuación Final: {self.score}", SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2-20, arcade.color.WHITE, 20)
            arcade.draw_text("Presiona R para reiniciar", SCREEN_WIDTH/2-120, SCREEN_HEIGHT/2-60, arcade.color.WHITE, 16)

    def on_update(self, delta_time):
        if self.game_over:
            return
        
        self.current_speed += SPEED_UP_RATE

        self.player.update()

        for spike in self.spikes:
            spike.update(self.current_speed)

            if spike.check_collision(self.player):
                self.player.is_alive = False
                self.game_over = True

        self.spikes = [spike for spike in self.spikes if not spike.is_off_screen()]

        self.spawn_timer += delta_time
        spawn_interval = max(0.8, 1.5 - (self.current_speed - INITIAL_SPEED) * 0.1)

        if self.spawn_timer > spawn_interval:
            self.spawn_spike()
            self.spawn_timer = 0

        if self.player.is_alive:
            self.score += 1

    def spawn_spike(self):
        x = SCREEN_WIDTH + 50

        spike_type = random.choice(['ground', 'ground', 'ground_double', 'elevated'])

        if spike_type == 'ground':
            self.spikes.append(Spike(x, GROUND_HEIGHT, CUBE_SIZE))
        elif spike_type == 'ground_double':
            self.spikes.append(Spike(x, GROUND_HEIGHT, CUBE_SIZE))
            self.spikes.append(Spike(x + CUBE_SIZE, GROUND_HEIGHT, CUBE_SIZE))
        elif spike_type == 'elevated':
            spike = Spike(x, GROUND_HEIGHT+150, CUBE_SIZE)
            self.spikes.append(spike)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R and self.game_over:
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        self.player.jump()

game = Game()
game.setup()
arcade.run()