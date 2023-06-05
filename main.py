import arcade

# Set up constants for the window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Alien Invasion"

# Set up constants for the spaceship
SPACESHIP_SPEED = 5
SPACESHIP_IMAGE = "spaceship.png"

class Spaceship(arcade.Sprite):
    def __init__(self):
        super().__init__(SPACESHIP_IMAGE)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 50

    def update(self):
        # Update the spaceship's position based on user input or game logic
        self.center_x += self.change_x
        self.center_y += self.change_y

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.spaceship = None

    def setup(self):
        # Set up your game here, such as initializing variables and loading resources
        self.spaceship = Spaceship()

    def on_draw(self):
        # Render the screen here
        arcade.start_render()

        # Draw the spaceship
        self.spaceship.draw()

    def update(self, delta_time):
        # Update the game logic here
        self.spaceship.update()

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
