import arcade , random
from models import World, Ship

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
METEORITE_COUNT = random.randint(3, 4)
STAR_COUNT = random.randint(3, 7)
SPEED_METEO = 9
SPEED_STAR = 4

class Meteorite(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT,
                                         SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.center_y -= SPEED_METEO

        if self.top < 0:
            self.reset_pos()


class Star(arcade.Sprite):
    def reset_pos_star(self):
        self.center_y = random.randrange(SCREEN_HEIGHT,
                                         SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.center_y -= SPEED_STAR

        if self.top < 0:
            self.reset_pos_star()


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='Into the space')

        self.background = None
        self.meteo_sprite_list = None
        self.star_sprite_list = None

        self.world = World(width, height)
        self.ship_sprite = ModelSprite('img/ship.png', model=self.world.ship)

    def add_more_meteotire(self):
        for i in range(METEORITE_COUNT):
            meteo = Meteorite('img/meteorite.png')

            meteo.center_x = random.randrange(SCREEN_WIDTH)
            meteo.center_y = random.randrange(SCREEN_HEIGHT,
                                              SCREEN_HEIGHT + 300)

            self.meteo_sprite_list.append(meteo)

    def add_more_star(self):
        for i in range(STAR_COUNT):
            star = Star('img/star.png')

            self.center_y = random.randrange(SCREEN_HEIGHT,
                                             SCREEN_HEIGHT + 300)
            self.center_x = random.randrange(SCREEN_WIDTH)

            self.star_sprite_list.append(star)

    def set_up(self):
        self.background = arcade.load_texture("img/background.jpg")
        self.meteo_sprite_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()

        self.add_more_meteotire()
        self.add_more_star()

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(f"Score: {self.world.score}",
                         self.width - 120,
                         self.height - 40,
                         arcade.color.WHITE, 18)
        self.ship_sprite.draw()
        self.meteo_sprite_list.draw()
        self.star_sprite_list.draw()


    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.meteo_sprite_list.update()
        self.star_sprite_list.update()

        self.check_hit()

    def check_hit(self, ):
        star_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.star_sprite_list)

        for star in star_hit_list:
            star.reset_pos_star()

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