"""
Artwork from https://www.flaticon.com

"""

import arcade , random
from models import *

SCREEN_HEIGHT = 670
SCREEN_WIDTH = 900
METEORITE_COUNT = random.randint(3, 4)
STAR_COUNT = random.randint(3, 7)
SPEED_METEO = 6
SPEED_STAR = 4

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
        self.state = World.STATE_FROZEN

        self.world = World(width, height)
        self.ship_sprite = ModelSprite('img/ship.png', model=self.world.ship)


    def add_more_meteorite(self):
        for i in range(METEORITE_COUNT):
            meteo = Meteorite('img/meteorite.png')
            meteo.center_x = random.randrange(SCREEN_WIDTH)
            meteo.center_y = random.randrange(SCREEN_HEIGHT,
                                              SCREEN_HEIGHT + 300)

            self.meteo_sprite_list.append(meteo)

    def add_more_star(self):
        for i in range(STAR_COUNT):
            star = Star('img/star.png')

            star.center_x = random.randrange(SCREEN_WIDTH)
            star.center_y = random.randrange(SCREEN_HEIGHT,
                                             SCREEN_HEIGHT + 300)

            self.star_sprite_list.append(star)

    def check_hit_star(self):
        star_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.star_sprite_list)
        for s in star_hit_list:
            s.reset_pos_star()
            self.world.score += 1
            # change stage
            if self.world.score == 25:
                self.world.stage += 1

    def check_hit_meteo(self):
        meteo_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.meteo_sprite_list)
        for m in meteo_hit_list:
            if self.world.health > 0:
                m.reset_pos()
                self.world.health -= 10
                if self.world.health <= 0:
                    self.world.die()

    def set_up(self):
        self.background = arcade.load_texture("img/background.jpg")
        self.meteo_sprite_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()

        self.add_more_meteorite()
        self.add_more_star()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(f"| Score: {self.world.score}",
                         self.width - 120,
                         self.height - 40,
                         arcade.color.WHITE, 18)
        arcade.draw_text(f"Stage: {self.world.stage}",
                         self.width - 210,
                         self.height - 40,
                         arcade.color.WHITE, 18)
        self.ship_sprite.draw()
        self.meteo_sprite_list.draw()
        self.star_sprite_list.draw()

        self.healthbar_sprite = ModelSprite(f'healthbar/h{self.world.health}.png',
                                            model=self.world.healthbar_position)
        self.healthbar_sprite.draw()

        if self.world.state == 2:
            arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                         SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.RED_BROWN)
            arcade.draw_text(f'GAME OVER', 300 , SCREEN_HEIGHT // 2, arcade.color.WHITE, 40)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.meteo_sprite_list.update()
        self.star_sprite_list.update()
        self.check_hit_star()
        self.check_hit_meteo()


def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_up()
    arcade.run()

if __name__ == '__main__':
    main()

