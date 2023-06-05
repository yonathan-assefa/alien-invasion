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
ENEMY_IMAGE = "img/enemy1.png"
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64

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
        super().__init__(ENEMY_IMAGE, scale=0.15)
        self.center_x = x
        self.center_y = y
        self.change_x = 0
        self.change_y = -ENEMY_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.top < 0:
            self.center_x = random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH)
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

class EnemyBullet(arcade.Sprite):
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
        self.enemy_bullet_list = None

    def setup(self):
        self.spaceship = Spaceship()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        for _ in range(5):
            enemy = Enemy(random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH),
                          random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
            self.enemy_list.append(enemy)

    def on_draw(self):
        arcade.start_render()
        self.spaceship.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.enemy_bullet_list.draw()

    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()
        self.bullet_list.update()
        self.enemy_bullet_list.update()

        # Check for collisions between bullets and enemies
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()

        # Check for collisions between spaceship and enemies
        hit_list = arcade.check_for_collision_with_list(self.spaceship, self.enemy_list)
        if hit_list:
            self.spaceship.remove_from_sprite_lists()
            arcade.close_window()

        # Enemy bullet firing logic
        for enemy in self.enemy_list:
            if random.randint(1, 100) == 1:
                enemy_bullet = EnemyBullet(enemy.center_x, enemy.center_y, -BULLET_SPEED)
                self.enemy_bullet_list.append(enemy_bullet)

        # Check for collisions between enemy bullets and spaceship
        hit_list = arcade.check_for_collision_with_list(self.spaceship, self.enemy_bullet_list)
        if hit_list:
            self.spaceship.remove_from_sprite_lists()
            arcade.close_window()

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

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
