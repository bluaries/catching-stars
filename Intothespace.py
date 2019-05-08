"""
Artwork from https://www.flaticon.com
    https://www.cognigen-cellular.com
"""

import arcade
import random
from models import *

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 570

METEORITE_COUNT = random.randint(3, 4)
STAR_COUNT = random.randint(4, 5)
SPEED_METEO = 7
SPEED_STAR = 5
SPEED_BG_STAR = 2

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

class ItemSprite(arcade.Sprite):
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT,
                                         SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.angle += self.change_angle

        if self.top < 0:
            self.reset_pos()

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='Into the space')

        self.background = None
        self.gameover = None

        self.world = World(width, height)
        self.ship_sprite = ModelSprite('img/ship.png', model=self.world.ship, scale=0.9)

    def add_more_meteo_star(self):
        for i in range(METEORITE_COUNT):
            meteo =  ItemSprite('img/meteorite1.png')
            meteo.center_x = random.randrange(SCREEN_WIDTH)
            meteo.center_y = random.randrange(SCREEN_HEIGHT,
                                        SCREEN_HEIGHT + 300)

            meteo.angle = random.randrange(3, 360)
            meteo.scale = random.uniform(0.7, 1.7)
            self.meteo_sprite_list.append(meteo)

        for i in range(STAR_COUNT):
            star =  ItemSprite('img/star.png')
            bg_star =  ItemSprite('img/bg_star.png')

            star.center_x = random.randrange(SCREEN_WIDTH)
            star.center_y = random.randrange(SCREEN_HEIGHT,
                                        SCREEN_HEIGHT + 300)
            star.angle = random.randrange(3, 360)
            star.change_angle = random.randrange(-5, 6)

            bg_star.center_x = random.randrange(SCREEN_WIDTH)
            bg_star.center_y = random.randrange(0, SCREEN_HEIGHT)

            self.bg_star_list.append(bg_star)
            self.star_sprite_list.append(star)

    def add_item(self):
        heart = ItemSprite('img/heart.png')
        heart.center_x = random.randrange(SCREEN_WIDTH)
        heart.center_y = random.randrange(SCREEN_HEIGHT,
                                          SCREEN_HEIGHT + 300)

        self.heart_sprite_list.append(heart)

    def check_hit(self):
        star_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.star_sprite_list)
        for s in star_hit_list:
            s.reset_pos()
            self.world.score += 1
            # change stage
            if self.world.score % 3 == 0:
                self.world.bg_state += 1
            elif self.world.score == 83 or self.world.score == 167:
                self.world.bg_state = 0
            if self.world.score == 25:
                self.world.stage += 1
            elif self .world.score == 40:
                self.world.stage += 1

        meteo_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.meteo_sprite_list)
        for m in meteo_hit_list:
            m.reset_pos()
            if self.world.health > 0:
                self.world.health -= 10

        heart_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.heart_sprite_list)
        for h in heart_hit_list:
            h.reset_pos()
            if self.world.health < 110:
                self.world.health += 10

    def run_level(self):
        if self.world.health == 0:
            self.meteo_sprite_list.move(0, 0)
            self.star_sprite_list.move(0, 0)
            self.bg_star_list.move(0, 0)
            self.world.die()
        else:
            if self.world.stage == 1 :
                self.meteo_sprite_list.move(0, -SPEED_METEO)
                self.star_sprite_list.move(0, -SPEED_STAR)
            elif self.world.stage == 2 :
                self.meteo_sprite_list.move(0, -(SPEED_METEO+2))
                self.star_sprite_list.move(0, -(SPEED_STAR+2))
                if self.world.health < 70 and self.world.health > 30:
                    self.heart_sprite_list.move(0, -(SPEED_STAR+2))
            elif self.world.stage == 3:
                self.meteo_sprite_list.move(0, -(SPEED_METEO+4))
                self.star_sprite_list.move(0, -(SPEED_STAR+4))
                if self.world.health < 70 and self.world.health > 30:
                    self.heart_sprite_list.move(0, -(SPEED_STAR+4))
            self.bg_star_list.move(0, -SPEED_BG_STAR)
    def set_up(self):
        self.background = arcade.load_texture(f'bg/bg{self.world.bg_state}.jpg')
        self.gameover = arcade.load_texture('bg/gameover.png')
        self.meteo_sprite_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.bg_star_list = arcade.SpriteList()
        self.heart_sprite_list = arcade.SpriteList()

        self.add_more_meteo_star()
        self.add_item()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,SCREEN_WIDTH ,
                    SCREEN_HEIGHT, arcade.load_texture(f'bg/bg{self.world.bg_state}.jpg'))
        self.bg_star_list.draw()

        self.ship_sprite.draw()
        self.meteo_sprite_list.draw()
        self.star_sprite_list.draw()
        self.heart_sprite_list.draw()

        arcade.draw_text(f"| Score: {self.world.score}",
                         self.width - 120,
                         self.height - 45,
                         arcade.color.WHITE, 18)
        arcade.draw_text(f"Stage: {self.world.stage}",
                         self.width - 198,
                         self.height - 45,
                         arcade.color.WHITE, 18)
        self.healthbar_sprite = ModelSprite(f'healthbar/h{self.world.health}.png',
                                            model=self.world.healthbar_position, scale=0.8)
        self.healthbar_sprite.draw()

        if self.world.state == 3:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                          SCREEN_WIDTH, SCREEN_HEIGHT, self.gameover)
            arcade.draw_text(f'GAME OVER', 170, SCREEN_HEIGHT // 2, arcade.color.WHITE, 30)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.meteo_sprite_list.update()
        self.star_sprite_list.update()
        self.bg_star_list.update()
        self.heart_sprite_list.update()

        self.check_hit()

        self.run_level()

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_up()
    arcade.run()

if __name__ == '__main__':
    main()