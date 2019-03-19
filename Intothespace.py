import arcade

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='Into the space')
        arcade.set_background_color(arcade.color.WHEAT)

    def on_draw(self):
        arcade.start_render()

if __name__ == '__main__':
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()