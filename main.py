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
PLAYER_BULLET_SPEED = 10
PLAYER_BULLET_IMAGE = "img/player_bullet.png"
PLAYER_BULLET_WIDTH = 32
PLAYER_BULLET_HEIGHT = 32

ENEMY_BULLET_SPEED = 2
ENEMY_BULLET_IMAGE = "img/enemy_bullet.png"
ENEMY_BULLET_WIDTH = 16
ENEMY_BULLET_HEIGHT = 16

# Set up constants for the power-ups
POWERUP_SPEED = 1
POWERUP_IMAGE_1 = "img/powerup_1.png"
POWERUP_IMAGE_2 = "img/powerup_2.png"
POWERUP_WIDTH = 32
POWERUP_HEIGHT = 32

# Power-up types
POWERUP_TYPE_EXTRA_BULLETS = 1
POWERUP_TYPE_PENETRATING_BULLETS = 2


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
    def __init__(self, x, y, change_y, image_path, scale, width, height):
        super().__init__(image_path, scale)
        self.center_x = x
        self.center_y = y
        self.change_y = change_y
        self.width = width
        self.height = height

    def update(self):
        self.center_y += self.change_y

class PowerUp(arcade.Sprite):
    def __init__(self, x, y, powerup_type):
        if powerup_type == POWERUP_TYPE_EXTRA_BULLETS:
            super().__init__(POWERUP_IMAGE_1, scale=0.15)
        elif powerup_type == POWERUP_TYPE_PENETRATING_BULLETS:
            super().__init__(POWERUP_IMAGE_2, scale=0.15)
        else:
            raise ValueError("Invalid power-up type")

        self.center_x = x
        self.center_y = y
        self.change_y = -POWERUP_SPEED
        self.powerup_type = powerup_type

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
        self.powerup_list = None
        self.explosion_list = None
        self.extra_bullets_powerup = False
        self.penetrating_bullets_powerup = False

    def setup(self):
        self.spaceship = Spaceship()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
      

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
        self.powerup_list.draw()
    


    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.powerup_list.update()
 


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

        # Check for collisions between bullets and power-ups
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.powerup_list)
            if hit_list:
                bullet.remove_from_sprite_lists()
                for powerup in hit_list:
                    if powerup.powerup_type == POWERUP_TYPE_EXTRA_BULLETS:
                        self.extra_bullets_powerup = True
                    elif powerup.powerup_type == POWERUP_TYPE_PENETRATING_BULLETS:
                        self.penetrating_bullets_powerup = True
                    powerup.remove_from_sprite_lists()

        # Enemy bullet firing logic
        for enemy in self.enemy_list:
            if random.randint(1, 100) == 1:
                enemy_bullet = Bullet(enemy.center_x, enemy.center_y, -ENEMY_BULLET_SPEED,
                                      ENEMY_BULLET_IMAGE, 0.15, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT)
                self.enemy_bullet_list.append(enemy_bullet)

        # Check for collisions between enemy bullets and spaceship
        hit_list = arcade.check_for_collision_with_list(self.spaceship, self.enemy_bullet_list)
        if hit_list:
            self.spaceship.remove_from_sprite_lists()
            arcade.close_window()

        # Update enemy bullet positions
        for enemy_bullet in self.enemy_bullet_list:
            enemy_bullet.update()
            # Remove enemy bullets when they go off-screen
            if enemy_bullet.top < 0:
                enemy_bullet.remove_from_sprite_lists()
        
        # Spawn new enemy ships if there are fewer than a certain number
        if len(self.enemy_list) < 5:
            for _ in range(5 - len(self.enemy_list)):
                enemy = Enemy(random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH),
                              random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200))
                self.enemy_list.append(enemy)
        
        # Spawn power-ups randomly
        if random.randint(1, 500) == 1:
            powerup_type = random.choice([POWERUP_TYPE_EXTRA_BULLETS, POWERUP_TYPE_PENETRATING_BULLETS])
            powerup = PowerUp(random.randint(POWERUP_WIDTH, SCREEN_WIDTH - POWERUP_WIDTH),
                              SCREEN_HEIGHT + POWERUP_HEIGHT, powerup_type)
            self.powerup_list.append(powerup)

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
            if self.extra_bullets_powerup:
                bullet1 = Bullet(self.spaceship.center_x - PLAYER_BULLET_WIDTH // 2, self.spaceship.top,
                                 PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE, 0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                bullet2 = Bullet(self.spaceship.center_x + PLAYER_BULLET_WIDTH // 2, self.spaceship.top,
                                 PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE, 0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.bullet_list.extend([bullet1, bullet2])
            elif self.penetrating_bullets_powerup:
                bullet = Bullet(self.spaceship.center_x, self.spaceship.top,
                                PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE, 0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
                self.bullet_list.append(bullet)
            else:
                bullet = Bullet(self.spaceship.center_x, self.spaceship.top,
                                PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE, 0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT)
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
