import arcade , random
from models import World, Ship

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
METEORITE_COUNT = random.randint(2, 4)
STAR_COUNT = random.randint(1, 7)
SPEED = 7

class Meteorite(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT,
                                         SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)


    def update(self):
        self.center_y -= SPEED

        if self.top < 0:
            self.reset_pos()

class Star(arcade.Sprite):
    def reset_pos_star(self):
        self.center_y = random.randrange(SCREEN_HEIGHT,
                                         SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)


    def update(self):
        self.center_y -= 4

        if self.top < 0:
            self.reset_pos_star()


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='Into the space')

        self.background = None
        self.meteo_sprite_list = None
        self.star_speite_list = None

        self.world = World(width, height)
        self.ship_sprite = ModelSprite('img/ship.png', model=self.world.ship)

    def set_up(self):
        self.background = arcade.load_texture("img/background.jpg")
        self.meteo_sprite_list = arcade.SpriteList()
        self.star_speite_list = arcade.SpriteList()

        for i in range(METEORITE_COUNT):
            meteo = Meteorite('img/meteorite.png')

            meteo.center_x = random.randrange(SCREEN_WIDTH)
            meteo.center_y = random.randrange(SCREEN_HEIGHT,
                                              SCREEN_HEIGHT + 300)

            self.meteo_sprite_list.append(meteo)

        for i in range(STAR_COUNT):
            star = Star('img/star.png')

            star.center_x = random.randrange(SCREEN_WIDTH)
            star.center_y = random.randrange(SCREEN_HEIGHT,
                                              SCREEN_HEIGHT + 300)

            self.meteo_sprite_list.append(star)



    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.ship_sprite.draw()
        self.meteo_sprite_list.draw()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.meteo_sprite_list.update()

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

if __name__ == '__main__':
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_up()
    arcade.run()