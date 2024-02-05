"""
Artwork from https://www.flaticon.com
    https://www.cognigen-cellular.com
    https://www.freepik.com
    https://dribbble.com
music : EDGE Soundtrack - Kakkoi

"""

import arcade
import random
from models import World

SCREEN_HEIGHT = 700
SCREEN_WIDTH = 570
INSTRUCTIONS_0 = 0
INSTRUCTIONS_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3

METEORITE_COUNT = random.randint(3, 4)
STAR_COUNT = random.randint(4, 5)
SPEED_METEO = 7.5
SPEED_STAR = 5.5
SPEED_BG_STAR = 2

WHITE_COLOR = (224, 224, 224)

music = arcade.load_sound('sound/game_music.wav')
arcade.play_sound(music)

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
        self.center_y = random.randrange(SCREEN_HEIGHT, SCREEN_HEIGHT + 300)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        self.angle += self.change_angle

        if self.top < 0:
            self.reset_pos()

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, title='catching stars!')

        self.background = None
        self.gameover = None
        self.instructions = []
        self.current_state = INSTRUCTIONS_0

        self.world = World(width, height)
        self.ship_sprite = ModelSprite('img/ship2.0.png', model=self.world.ship, scale=0.47)
        self.instructions.append(arcade.load_texture('img/menu.jpg'))
        self.instructions.append(arcade.load_texture('img/howtoplay.jpg'))

        self.press_mouse = arcade.sound.load_sound('sound/button.wav')
        self.start_sound = arcade.sound.load_sound('sound/start.wav')
        self.hit_sound = arcade.load_sound('sound/hit.wav')
        self.collect_sound = arcade.load_sound('sound/collect.wav')

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
            star =  ItemSprite('img/star.png', scale=0.9)
            bg_star =  ItemSprite('bg/bg_star.png')

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
        heart.center_y = random.randrange(SCREEN_HEIGHT+30,
                                          SCREEN_HEIGHT + 300)

        self.heart_sprite_list.append(heart)

    def set_moving(self,lst1, x1, y1, lst2, x2, y2):
        lst1.move(x1, y1), lst2.move(x2, y2)

    def check_hit(self):
        star_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.star_sprite_list)
        for s in star_hit_list:
            arcade.play_sound(self.collect_sound)
            s.reset_pos()
            self.world.score += 1
            # change stage
            if self.world.score == 25:
                self.world.stage += 1
            elif self .world.score == 40:
                self.world.stage += 1
            elif self .world.score == 80:
                self.world.stage += 1
            elif self .world.score == 120:
                self.world.stage += 1

        meteo_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.meteo_sprite_list)
        for m in meteo_hit_list:
            arcade.play_sound(self.hit_sound)
            m.reset_pos()
            if self.world.health > 0:
                self.world.health -= 10

        heart_hit_list = arcade.check_for_collision_with_list(self.ship_sprite, self.heart_sprite_list)
        for h in heart_hit_list:
            arcade.play_sound(self.collect_sound)
            h.reset_pos()
            if self.world.health < 110:
                self.world.health += 10

    def run_level(self):
        if self.current_state == INSTRUCTIONS_0 or self.current_state == INSTRUCTIONS_1:
            self.set_moving(self.meteo_sprite_list, 0, 0,
                            self.star_sprite_list, 0, 0)
        elif self.world.health == 0:
            self.set_moving(self.meteo_sprite_list, 0, 0,
                            self.star_sprite_list, 0, 0)
            self.heart_sprite_list.move(0, 0)
            self.world.die()
            self.current_state = GAME_OVER
        else:
            if self.world.stage == 1 :
                self.set_moving(self.meteo_sprite_list, 0, -SPEED_METEO,
                                self.star_sprite_list, 0, -SPEED_STAR)
            elif self.world.stage == 2 :
                self.set_moving(self.meteo_sprite_list, 0, -(SPEED_METEO+2),
                                self.star_sprite_list, 0, -(SPEED_STAR+2))
            elif self.world.stage == 3:
                self.set_moving(self.meteo_sprite_list, 0, -(SPEED_METEO+4),
                                self.star_sprite_list, 0, -(SPEED_STAR+4))
            elif self.world.stage == 4:
                self.set_moving(self.meteo_sprite_list, 0, -(SPEED_METEO+8),
                                self.star_sprite_list, 0, -(SPEED_STAR+8))
            elif self.world.stage == 5:
                self.set_moving(self.meteo_sprite_list, 0, -(SPEED_METEO+12),
                                self.star_sprite_list, 0, -(SPEED_STAR+12))
            self.bg_star_list.move(0, -SPEED_BG_STAR)

    def menu_button(self):
        duration_button = 600
        # button animation
        button = arcade.AnimatedTimeBasedSprite('img/start_button1.png')
        button.center_x = SCREEN_WIDTH // 2
        button.center_y = SCREEN_HEIGHT // 2

        # loading the frames individually
        # frame 1
        texture = arcade.load_texture('img/start_button1.png')
        button.frames.append(arcade.AnimationKeyframe(tile_id=0, duration=duration_button, texture= arcade.load_texture('img/start_button1.png')))
        # frame 2
        button.frames.append(arcade.AnimationKeyframe(tile_id=1, duration=duration_button, texture= arcade.load_texture('img/start_button2.png')))

        self.menu_button_list.append(button)

        how_to_play = arcade.Sprite('img/howtoplay_button.png')
        how_to_play.center_x = 48
        how_to_play.center_y = 43
    
        self.menu_button_list.append(how_to_play)

        version = arcade.create_text_sprite(text='v2.0', start_x=80, start_y=26, color=WHITE_COLOR, font_size=12, bold=True)

        self.menu_button_list.append(version)

    def moving_bg(self):
        duration_bg = 2400
        bg_state = arcade.AnimatedTimeBasedSprite('bg/bg0.jpg')
        bg_state.center_x = SCREEN_WIDTH // 2
        bg_state.center_y = SCREEN_HEIGHT // 2

        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=0, duration=duration_bg, texture= arcade.load_texture('bg/bg0.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=1, duration=duration_bg, texture= arcade.load_texture('bg/bg1.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=2, duration=duration_bg, texture= arcade.load_texture('bg/bg2.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=3, duration=duration_bg, texture= arcade.load_texture('bg/bg3.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=4, duration=duration_bg, texture= arcade.load_texture('bg/bg4.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=5, duration=duration_bg, texture= arcade.load_texture('bg/bg5.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=6, duration=duration_bg, texture= arcade.load_texture('bg/bg6.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=7, duration=duration_bg, texture= arcade.load_texture('bg/bg7.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=8, duration=duration_bg, texture= arcade.load_texture('bg/bg8.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=9, duration=duration_bg, texture= arcade.load_texture('bg/bg9.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=10, duration=duration_bg, texture= arcade.load_texture('bg/bg10.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=11, duration=duration_bg, texture= arcade.load_texture('bg/bg11.jpg')))
        bg_state.frames.append(arcade.AnimationKeyframe(tile_id=12, duration=duration_bg, texture= arcade.load_texture('bg/bg12.jpg')))

        self.bg_list.append(bg_state)
    
    def run_bg_msc(self, delta):
        self.bg_music_time += delta
        if self.bg_music_time > 90:
            arcade.sound.play_sound(arcade.sound.load_sound('sound/game_music.wav'))
            self.bg_music_time = 0

    def set_restart(self):
        self.world.health = 150
        self.world.score = 0
        self.world.stage = 1

    def set_up(self):
        self.gameover = arcade.load_texture('bg/gameover.png')

        self.meteo_sprite_list = arcade.SpriteList()
        self.star_sprite_list = arcade.SpriteList()
        self.bg_star_list = arcade.SpriteList()
        self.heart_sprite_list = arcade.SpriteList()
        self.menu_button_list = arcade.SpriteList()
        self.bg_list = arcade.SpriteList()

        self.add_more_meteo_star()
        self.add_item()
        self.menu_button()
        self.moving_bg()

    def draw_bg(self):
        self.bg_list.draw()
        self.bg_star_list.draw()

    def draw_game(self):
        self.ship_sprite.draw()
        self.meteo_sprite_list.draw()
        self.star_sprite_list.draw()
        if self.world.stage == 2 and self.world.health < 100 and self.world.health != 0:
            self.heart_sprite_list.draw()
            self.heart_sprite_list.move(0, -(SPEED_STAR+2))
        elif self.world.stage == 3 and self.world.health < 70 and self.world.health != 0:
            self.heart_sprite_list.draw()
            self.heart_sprite_list.move(0, -(SPEED_STAR+4))
        elif self.world.stage == 4 and self.world.health < 30 and self.world.health != 0:
            self.heart_sprite_list.draw()
            self.heart_sprite_list.move(0, -(SPEED_STAR+8))

        level_score_bar = arcade.Sprite('img/bar.png')
        level_score_bar.center_x = 450
        level_score_bar.center_y = 655

        arcade.draw_text(f'{self.world.stage}',
                         418, 647.2, arcade.color.WHITE, 18)
        arcade.draw_text(f'{self.world.score}',
                         517, 647, arcade.color.WHITE, 18)
        self.healthbar_sprite = ModelSprite(f'healthbar/h{self.world.health}.png',
                                            model=self.world.healthbar_position, scale=0.8)
        self.healthbar_sprite.draw()
        level_score_bar.draw()

    def draw_instructions(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
        
    def draw_gameover(self):
        self.draw_bg()
        self.draw_game()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT, self.gameover)

        arcade.draw_text(f'{self.world.stage}',
                            275, 380, arcade.color.BLACK, 30)
        arcade.draw_text(f'{self.world.score}',
                            263, 245, arcade.color.BLACK, 30)

    def on_draw(self):
        arcade.start_render()
        if self.current_state == INSTRUCTIONS_0:
            self.draw_instructions(0)
            self.menu_button_list.draw()
        elif self.current_state == INSTRUCTIONS_1:
            self.draw_instructions(1)
        elif self.current_state == GAME_RUNNING:
            self.draw_bg()
            self.draw_game()
        elif self.current_state == GAME_OVER:
            self.draw_gameover()

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if key == arcade.key.SPACE and self.current_state == INSTRUCTIONS_0:
            arcade.play_sound(self.start_sound)
            self.current_state = GAME_RUNNING
            self.world.state = World.STATE_STARTED

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == INSTRUCTIONS_0:
            arcade.play_sound(self.press_mouse)
            self.current_state = INSTRUCTIONS_1
        elif self.current_state == INSTRUCTIONS_1:
            arcade.play_sound(self.press_mouse)
            self.current_state = INSTRUCTIONS_0
        elif self.current_state == GAME_OVER:
            arcade.play_sound(self.press_mouse)
            self.current_state = INSTRUCTIONS_0
            self.set_restart()

    def update(self, delta):
        self.world.update(delta)

        self.meteo_sprite_list.update()
        self.star_sprite_list.update()
        self.bg_star_list.update()
        self.heart_sprite_list.update()

        self.menu_button_list.update_animation()
        self.bg_list.update_animation()

        self.check_hit()
        self.run_level()

def main():
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.set_up()
    arcade.run()

if __name__ == '__main__':
    main()
