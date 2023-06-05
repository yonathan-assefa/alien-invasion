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

# Set up constants for the bullets
BULLET_SPEED = 7
BULLET_IMAGE = "img/bullet.png"
BULLET_WIDTH = 16
BULLET_HEIGHT = 32

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

class Bullet(arcade.Sprite):
    def __init__(self, x, y, change_y):
        super().__init__(BULLET_IMAGE, scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_y = change_y

    def update(self):
        self.center_y += self.change_y

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.spaceship = None
        self.enemy_list = None
        self.bullet_list = None

    def setup(self):
        self.spaceship = Spaceship()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        for _ in range(5):
            enemy = Enemy(random.randint(64, SCREEN_WIDTH - 64),
                          random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.spaceship.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()
        self.bullet_list.update()

        # Check for collisions between bullets and enemies
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()

        # Check if there are no enemy ships left
        if len(self.enemy_list) == 0:
            self.spawn_enemy_ships()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.spaceship.change_x = -SPACESHIP_SPEED
        elif key == arcade.key.RIGHT:
            self.spaceship.change_x = SPACESHIP_SPEED
        elif key == arcade.key.UP:
            self.spaceship.change_y = SPACESHIP_SPEED
        elif key == arcade.key.DOWN:
            self.spaceship.change_y = -SPACESHIP_SPEED
        elif key == arcade.key.SPACE:
            bullet = Bullet(self.spaceship.center_x, self.spaceship.top, BULLET_SPEED)
            self.bullet_list.append(bullet)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.spaceship.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.spaceship.change_y = 0

    def spawn_enemy_ships(self):
        for _ in range(5):
            enemy = Enemy(random.randint(64, SCREEN_WIDTH - 64),
                          random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            self.enemy_list.append(enemy)

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
