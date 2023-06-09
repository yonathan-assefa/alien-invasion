import arcade
import random
import time
from database import DatabaseHandler

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

# Set up constants for the power-up types
POWERUP_TYPE_EXTRA_BULLETS = 1
POWERUP_TYPE_PENETRATING_BULLETS = 2
POWERUP_TYPE_LIFE = 3  # Unique value for the life power-up

# Set up constants for the life power-up and remaining life image
LIFE_POWERUP_IMAGE = "img/life.png"
REMAINING_LIFE_IMAGE = "img/remaining.png"
MAX_LIFE = 5


# Set up constants for the explosion
EXPLOSION_IMAGE = "img/explosion.png"
EXPLOSION_COLUMNS = 16
EXPLOSION_ROWS = 16


class Explosion(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(EXPLOSION_IMAGE, scale=0.5)
        self.center_x = x
        self.center_y = y
        self.cur_texture = 0
        self.textures = []

        # Load explosion textures
        for row in range(EXPLOSION_ROWS):
            for column in range(EXPLOSION_COLUMNS):
                texture = arcade.load_texture(EXPLOSION_IMAGE,
                                              x=column * 32, y=row * 32,
                                              width=32, height=32)
                self.textures.append(texture)

    def update(self):
        self.cur_texture += 1
        if self.cur_texture < len(self.textures):
            self.texture = self.textures[self.cur_texture]
        else:
            self.remove_from_sprite_lists()

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

    def check_collision(self, sprite_list):
        hit_list = arcade.check_for_collision_with_list(self, sprite_list)
        if hit_list:
            for sprite in hit_list:
                sprite.remove_from_sprite_lists()
            self.remove_from_sprite_lists()

        if self.top < 0 or self.bottom > SCREEN_HEIGHT or self.right < 0 or self.left > SCREEN_WIDTH:
            self.remove_from_sprite_lists()


class PowerUp(arcade.Sprite):
    def __init__(self, x, y, powerup_type):
        if powerup_type == POWERUP_TYPE_EXTRA_BULLETS:
            super().__init__(POWERUP_IMAGE_1, scale=0.15)
        elif powerup_type == POWERUP_TYPE_PENETRATING_BULLETS:
            super().__init__(POWERUP_IMAGE_2, scale=0.15)
        elif powerup_type == POWERUP_TYPE_LIFE:
            super().__init__(LIFE_POWERUP_IMAGE, scale=0.15)  # Use the life power-up image

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

        # Database
        self.db_handler = DatabaseHandler('scores.db')

        self.background_texture = arcade.load_texture("img/bg/star.png")
        self.spaceship = None
        self.enemy_list = None
        self.bullet_list = None
        self.enemy_bullet_list = None
        self.powerup_list = None
        self.explosion_list = None
        self.extra_bullets_powerup = False
        self.penetrating_bullets_powerup = False
        
        
        self.bullet_limit = 6
        
        self.life = 3  # Number of lives for the spaceship
        self.game_over = False  # Flag to track game over state
        self.is_firing = False  # Flag to track if the spaceship is firing
        self.last_bullet_shot_time = 0  # Track the time when the last bullet was shot

        self.current_score = 0  # Initialize current_score to 0

        self.remaining_life_sprite = arcade.Sprite(REMAINING_LIFE_IMAGE, scale=0.05)  # Create the remaining life sprite
        self.remaining_life_sprite.position = 20, SCREEN_HEIGHT - 20  # Set the position of the remaining life sprite
        self.remaining_life_sprite_list = arcade.SpriteList()  # Create a sprite list to hold the remaining life sprite
        self.remaining_life = 3  # Set the initial remaining life

        self.remaining_life_sprites = []  # List to hold the remaining life sprites

        self.game_started = False
        self.top_score = self.db_handler.get_top_scores()[0][0]
        self.opening_sound = arcade.load_sound("sound/hell.ogg")
        self.playing_sound = arcade.play_sound(self.opening_sound, looping=True)

        # Bullet firing difference
        self.bullet_firing_difference = 0.25

    def setup(self):
        self.spaceship = Spaceship()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.powerup_list = arcade.SpriteList()
        self.explosion_list = arcade.SpriteList()
        self.create_remaining_life_sprites()  # Create the initial remaining life sprites
        self.current_score = 0
        self.remaining_life = 3
        self.create_remaining_life_sprites()
        
        self.top_score = self.db_handler.get_top_scores()[0][0]

        

   
        if self.game_started:
            arcade.stop_sound(self.playing_sound)

    def create_remaining_life_sprites(self):
        # Clear the previous remaining life sprites
        self.remaining_life_sprites = []
        # Create the remaining life sprites based on the remaining_life count
        for _ in range(self.remaining_life):
            life_sprite = arcade.Sprite("img/remaining.png", scale=0.05)
            self.remaining_life_sprites.append(life_sprite)

    # Database
    def on_close(self):
        self.db_handler.close()
    def store_score(self):
        self.db_handler.insert_score(self.current_score)

    def display_top_scores(self):
        top_scores = self.db_handler.get_top_scores()

        if top_scores:
            print("Top Scores:")
            for score in top_scores:
                print(score[0])  # Assuming the score is stored as the first element in the tuple
        else:
            print("No top scores available")
    
    # Game starter
    def start_game(self):
        self.game_started = True
        self.setup()  # Reset the game state

    # Top score
    def view_top_scores(self):
        top_scores = self.db_handler.get_top_scores()

        if top_scores:
            print("Top Scores:")
            for score in top_scores:
                print(score[0])  # Assuming the score is stored as the first element in the tuple
        else:
            print("No top scores available")

    def on_draw(self):
        if not self.game_started:
            self.draw_home_page()
        else:
            arcade.start_render()
            # Draw the background image
            arcade.draw_texture_rectangle(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
            SCREEN_WIDTH, SCREEN_HEIGHT,
            self.background_texture, 0
            )
            if not self.game_over:
                # Draw the remaining life sprites
                for i, life_sprite in enumerate(self.remaining_life_sprites):
                    life_sprite.center_x = i * (POWERUP_WIDTH + 10) + POWERUP_WIDTH / 2 + 10
                    life_sprite.center_y = SCREEN_HEIGHT - POWERUP_HEIGHT / 2 - 10
                    life_sprite.draw()
                self.spaceship.draw()
                self.enemy_list.draw()
                self.bullet_list.draw()
                self.enemy_bullet_list.draw()
                self.powerup_list.draw()
                self.explosion_list.draw()
                self.remaining_life_sprite_list.draw()  # Draw the remaining life sprite


                # Display the current score
                score_text = f"{self.current_score}"
                arcade.draw_text(
                    score_text,
                    SCREEN_WIDTH - 10,
                    SCREEN_HEIGHT - 20,
                    arcade.color.WHITE,
                    font_size=16,
                    font_name='Kenney Rocket',
                    anchor_x="right",
                    anchor_y="top",
                )
            else:
                # Game over screen
                game_over_image = arcade.load_texture("img/game_over.png")
                arcade.draw_texture_rectangle(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                    game_over_image.width, game_over_image.height,
                    game_over_image, 0
                )
                message = f"Socre: {self.current_score}\nPress 'R' to restart"
                arcade.draw_text(
                    message,
                    SCREEN_WIDTH // 2,
                    30,
                    arcade.color.YELLOW,
                    font_size=15,
                    font_name='Kenney Blocks',
                    anchor_x="center",
                    anchor_y="center",
                    align='center',
                    width=800,
                )
             
    
    def draw_home_page(self):
        # Clear the screen
        arcade.start_render()

        # Draw the game logo
        logo_image = arcade.load_texture("img/logo.png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, logo_image.width, logo_image.height, logo_image)

        # Draw the start button
        arcade.draw_text(
            "Start Game",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
            arcade.color.WHITE,
            font_size=30,
            font_name='Kenney Blocks',
            anchor_x="center"
        )

        # Draw the view top scores button
        arcade.draw_text(
            f"High Score: {self.top_score}",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150,
            arcade.color.WHITE,
            font_size=25,
            font_name='Kenney Blocks',
            anchor_x="center",
        )

    def restart_game(self):
        # Reset the game state
        self.setup()
        self.game_over = False


    def on_mouse_press(self, x, y, button, modifiers):
        # if not self.game_started or self.game_over:
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100:
            if SCREEN_HEIGHT // 2 - 120 <= y <= SCREEN_HEIGHT // 2 - 80:
                click_sound = arcade.load_sound("sound/click.mp3")
                arcade.play_sound(click_sound)
                self.start_game()
            elif SCREEN_HEIGHT // 2 - 170 <= y <= SCREEN_HEIGHT // 2 - 130:
                click_sound = arcade.load_sound("sound/click.mp3")
                arcade.play_sound(click_sound)
                self.view_top_scores()

    # Key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.extra_bullets_powerup:
                self.bullet_limit = 6  # Increase bullet limit to 6

        if key == arcade.key.LEFT:
            self.spaceship.change_x = -SPACESHIP_SPEED
        elif key == arcade.key.RIGHT:
            self.spaceship.change_x = SPACESHIP_SPEED
        elif key == arcade.key.UP:
            self.spaceship.change_y = SPACESHIP_SPEED
        elif key == arcade.key.DOWN:
            self.spaceship.change_y = -SPACESHIP_SPEED
        elif key == arcade.key.SPACE:
            self.is_firing = True
        elif key == arcade.key.R and self.game_over:
            # Restart the game when 'R' key is pressed
            self.restart_game()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.spaceship.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.spaceship.change_y = 0
        elif key == arcade.key.SPACE:
            self.is_firing = False
    
        if self.game_over:
            self.store_score()  # Store the score in the database
            if key == arcade.key.ENTER:
                self.restart_game()  # Restart the game


    
    def add_score(self, score):
        self.db_handler.add_score(score)

    
    def update(self, delta_time):
        self.spaceship.update()
        self.enemy_list.update()
        self.bullet_list.update()  # Remove enemy_list as an argument
        self.enemy_bullet_list.update()
        self.powerup_list.update()
        self.explosion_list.update()

        self.remaining_life_sprite_list.update()  # Update the remaining life sprite position

        for enemy in self.enemy_list:
            if random.randint(1, 100) == 1:
                enemy_bullet = Bullet(
                    enemy.center_x, enemy.center_y, -ENEMY_BULLET_SPEED,
                    ENEMY_BULLET_IMAGE, 0.15, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT
                )
                self.enemy_bullet_list.append(enemy_bullet)
                if self.game_started and not self.game_over:
                    laser_sound = arcade.load_sound("sound/enemy-fire.wav")
                    arcade.play_sound(laser_sound)

        for enemy_bullet in self.enemy_bullet_list:
            enemy_bullet.update()
            if enemy_bullet.top < 0:
                enemy_bullet.remove_from_sprite_lists()

        # Bullet firing logic
        if self.is_firing and len(self.bullet_list) < self.bullet_limit:
            current_time = time.time()
            time_difference = current_time - self.last_bullet_shot_time

            # Fire a bullet if enough time has passed since the last bullet was shot
            if time_difference >= self.bullet_firing_difference:  # Adjust the time interval as desired
                self.last_bullet_shot_time = current_time

                if self.extra_bullets_powerup:
                    bullet1 = Bullet(
                        self.spaceship.center_x - PLAYER_BULLET_WIDTH // 2,
                        self.spaceship.top,
                        PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE,
                        0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                    )
                    bullet2 = Bullet(
                        self.spaceship.center_x + PLAYER_BULLET_WIDTH // 2,
                        self.spaceship.top,
                        PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE,
                        0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                    )
                    self.bullet_list.extend([bullet1, bullet2])
                elif self.penetrating_bullets_powerup:
                    bullet = Bullet(
                        self.spaceship.center_x, self.spaceship.top,
                        PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE,
                        0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                    )
                    self.bullet_list.append(bullet)
                else:
                    bullet = Bullet(
                        self.spaceship.center_x, self.spaceship.top,
                        PLAYER_BULLET_SPEED, PLAYER_BULLET_IMAGE,
                        0.15, PLAYER_BULLET_WIDTH, PLAYER_BULLET_HEIGHT
                    )
                    self.bullet_list.append(bullet)
                if self.game_started and not self.game_over:
                    laser_sound = arcade.load_sound("sound/fire.mp3")
                    arcade.play_sound(laser_sound)

        if not self.game_over:        
            # Check for collisions between bullets and enemies
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for enemy in hit_list:
                        enemy.remove_from_sprite_lists()
                        self.current_score += 10  # Increment current_score by 10 for each enemy hit
                        explosion = Explosion(enemy.center_x, enemy.center_y)
                        self.explosion_list.append(explosion)
                    if self.game_started and not self.game_over:
                        laser_sound = arcade.load_sound("sound/enemy-died.wav")
                        arcade.play_sound(laser_sound)
            for bullet in self.bullet_list:
                bullet.check_collision(self.enemy_list)
          
            # Check for collisions between spaceship and enemy bullets
            hit_list = arcade.check_for_collision_with_list(self.spaceship, self.enemy_bullet_list)
            if hit_list:
                if self.game_started and not self.game_over:
                    laser_sound = arcade.load_sound("sound/sp exploded.wav")
                    arcade.play_sound(laser_sound)
                self.remaining_life -= 1
                self.update_remaining_life_sprite(1)  # Update the remaining life sprite
                for bullet in hit_list:
                    bullet.remove_from_sprite_lists()  # Remove the bullet from enemy_bullet_list
                if self.remaining_life <= 0:
                    self.game_over = True
                    self.spaceship.remove_from_sprite_lists()

            # Check for collisions between spaceship and enemies
            hit_list = arcade.check_for_collision_with_list(self.spaceship, self.enemy_list)
            if hit_list:
                self.remaining_life -= 1
                self.update_remaining_life_sprite(1)  # Update the remaining life sprite
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()
                    if self.current_score > 0:
                        self.current_score -= 5
                    explosion = Explosion(enemy.center_x, enemy.center_y)
                    self.explosion_list.append(explosion)
                    if self.remaining_life <= 0:
                        self.game_over = True
                        self.spaceship.remove_from_sprite_lists()
                if self.game_started and not self.game_over:
                    laser_sound = arcade.load_sound("sound/hit.mp3")
                    arcade.play_sound(laser_sound)

            # Check for collisions between bullets and power-ups
            for bullet in self.bullet_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.powerup_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for powerup in hit_list:
                        if powerup.powerup_type == POWERUP_TYPE_EXTRA_BULLETS:
                            self.bullet_limit = 6  # Increase bullet limit to 6
                            if self.bullet_firing_difference > 0.15:
                                self.bullet_firing_difference -= 0.05
                        elif powerup.powerup_type == POWERUP_TYPE_PENETRATING_BULLETS:
                            self.penetrating_bullets_powerup = True
                            if self.bullet_firing_difference > 0.15:
                                self.bullet_firing_difference -= 0.05
                        powerup.remove_from_sprite_lists()


            # Check for collisions between spaceship and life power-ups
            hit_list = arcade.check_for_collision_with_list(self.spaceship, self.powerup_list)
            if hit_list:
                for powerup in hit_list:
                    if powerup.powerup_type == POWERUP_TYPE_LIFE:
                        self.remaining_life = min(MAX_LIFE, self.remaining_life + 1)  # Increase remaining life (up to maximum)
                        life_sprite = arcade.Sprite("img/remaining.png", scale=0.05)
                        self.remaining_life_sprite_list.append(life_sprite)
                        self.update_remaining_life_sprite(0)  # Update the remaining life sprite

                    powerup.remove_from_sprite_lists()

            # Remove excess bullets if bullet_list exceeds bullet_limit
            while len(self.bullet_list) > self.bullet_limit:
                self.bullet_list[0].remove_from_sprite_lists()

            # Spawn new enemy ships if there are fewer than a certain number
            if len(self.enemy_list) < 5:
                for _ in range(5 - len(self.enemy_list)):
                    enemy = Enemy(
                        random.randint(ENEMY_WIDTH, SCREEN_WIDTH - ENEMY_WIDTH),
                        random.randint(SCREEN_HEIGHT, SCREEN_HEIGHT + 200)
                    )
                    self.enemy_list.append(enemy)

            # Spawn power-ups randomly
            if random.randint(1, 500) == 1:
                powerup_type = random.choice([POWERUP_TYPE_EXTRA_BULLETS, POWERUP_TYPE_PENETRATING_BULLETS, POWERUP_TYPE_LIFE])
                powerup = PowerUp(
                    random.randint(POWERUP_WIDTH, SCREEN_WIDTH - POWERUP_WIDTH),
                    SCREEN_HEIGHT + POWERUP_HEIGHT,
                    powerup_type
                )
                self.powerup_list.append(powerup)
    
    def update_remaining_life_sprite(self, state):
        if state:
            if self.remaining_life_sprites: 
                self.remaining_life_sprites.pop()  # Clear the remaining life sprite list
        else:
            if len(self.remaining_life_sprites) < 5:
                life_sprite = arcade.Sprite("img/remaining.png", scale=0.05)
                self.remaining_life_sprites.append(life_sprite)


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
