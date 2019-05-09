import arcade.key

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
MOVEMENT_SPEED = 8

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2
DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}

class Model:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Ship(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)

        self.direction = DIR_STILL

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]

    def update(self, delta):
        self.move(self.direction)

        if self.x > self.world.width:
            self.x = self.world.width
        if self.x < 0:
            self.x = 0


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(self, 275, 125)
        self.healthbar_position = Model(self, 110, 655)

        self.score = 0
        self.stage = 1
        self.health = 150
        self.bg_state = 1

        self.state = World.STATE_FROZEN


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.ship.direction = DIR_LEFT
        elif key == arcade.key.RIGHT:
            self.ship.direction = DIR_RIGHT

    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_started(self):
        return self.state == World.STATE_STARTED

    def die(self):
        self.state = World.STATE_DEAD

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.ship.update(delta)
