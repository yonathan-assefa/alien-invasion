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

class EnemyType1(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("img/enemy1.png", scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top < 0:
            self.center_x = random.randint(64, SCREEN_WIDTH - 64)
            self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)
            self.change_y = -ENEMY_SPEED

class EnemyType2(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("img/enemy2.png", scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top < 0:
            self.center_x = random.randint(64, SCREEN_WIDTH - 64)
            self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)
            self.change_y = -ENEMY_SPEED

class EnemyType3(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("img/enemy3.png", scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top < 0:
            self.center_x = random.randint(64, SCREEN_WIDTH - 64)
            self.center_y = random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)
            self.change_y = -ENEMY_SPEED

class EnemyType4(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("img/enemy4.png", scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top < 0:
            self.center_x = random.randint(64, SCREEN_WIDTH - 64)
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

        for _ in range(5):
            enemy1 = EnemyType1(random.randint(64, SCREEN_WIDTH - 64),
                                random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            enemy2 = EnemyType2(random.randint(64, SCREEN_WIDTH - 64),
                                random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            enemy3 = EnemyType3(random.randint(64, SCREEN_WIDTH - 64),
                                random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            enemy4 = EnemyType4(random.randint(64, SCREEN_WIDTH - 64),
                                random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            self.enemy_list.append(enemy1)
            self.enemy_list.append(enemy2)
            self.enemy_list.append(enemy3)
            self.enemy_list.append(enemy4)

    def on_draw(self):
        arcade.start_render()
        self.spaceship.draw()
        self.enemy_list.draw()

    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.spaceship.change_x = -SPACESHIP_SPEED
        elif key == arcade.key.RIGHT:
            self.spaceship.change_x = SPACESHIP_SPEED
        elif key == arcade.key.UP:
            self.spaceship.change_y = SPACESHIP_SPEED
        elif key == arcade.key.DOWN:
            self.spaceship.change_y = -SPACESHIP_SPEED

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
