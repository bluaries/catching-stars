import arcade.key , random

DIR_STILL = 0
DIR_RIGHT = 1
DIR_LEFT = 2

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}

MOVEMENT_SPEED = 6

class Model:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y


class Ship(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)

        self.direction = DIR_RIGHT

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]

    def update(self, delta):
        self.move(self.direction)

        if self.x > self.world.width:
            self.x = self.world.width
        if self.x < 0:
            self.x = 0


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(self, 450, 130)
        self.score = 0
        self.stage = 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.direction = DIR_STILL
        if key == arcade.key.LEFT:
            self.ship.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.ship.direction = DIR_RIGHT

    def update(self, delta):
        self.ship.update(delta)
