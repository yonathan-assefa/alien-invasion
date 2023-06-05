import arcade
import random

# Set up constants for the window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Alien Invasion"

# Set up constants for the spaceship
SPACESHIP_SPEED = 5
SPACESHIP_IMAGE = "img/spaceship.png"
SPACESHIP_WIDTH = 64
SPACESHIP_HEIGHT = 64
SPACESHIP_BOUNDARY = 20

# Set up constants for the enemies
ENEMY_SPEED = 2
ENEMY_IMAGE = "img/enemy.png"
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64

class Spaceship(arcade.Sprite):
    def __init__(self):
        super().__init__(SPACESHIP_IMAGE, scale=0.15)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 50
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < SPACESHIP_BOUNDARY:
            self.left = SPACESHIP_BOUNDARY
        elif self.right > SCREEN_WIDTH - SPACESHIP_BOUNDARY:
            self.right = SCREEN_WIDTH - SPACESHIP_BOUNDARY
        if self.bottom < SPACESHIP_BOUNDARY:
            self.bottom = SPACESHIP_BOUNDARY
        elif self.top > SCREEN_HEIGHT - SPACESHIP_BOUNDARY:
            self.top = SCREEN_HEIGHT - SPACESHIP_BOUNDARY

class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(ENEMY_IMAGE, scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If the enemy reaches the bottom of the screen, reset its position
        if self.top < 0:
            self.center_x = random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH)
            self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)
            self.change_y = -ENEMY_SPEED

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.spaceship = None
        self.enemy_list = None

    def setup(self):
        self.spaceship = Spaceship()
        self.enemy_list = arcade.SpriteList()

        for _ in range(5):  # Adjust the number of enemies as desired
            enemy = Enemy(random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH),
                          random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.spaceship.draw()
        self.enemy_list.draw()

    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
