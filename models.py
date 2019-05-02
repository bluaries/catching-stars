import arcade.key

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 900
MOVEMENT_SPEED = 6

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


class Healthbar(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)


class World:
    STATE_FROZEN = 1
    STATE_DEAD = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(self, 450, 125)

        self.healthbar_position = Healthbar(self, 130, 620)
        self.score = 0
        self.stage = 1
        self.health = 100

        self.state = World.STATE_FROZEN


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            self.ship.direction = DIR_STILL
        if key == arcade.key.LEFT:
            self.ship.direction = DIR_LEFT
        if key == arcade.key.RIGHT:
            self.ship.direction = DIR_RIGHT

    def freeze(self):
        self.state = World.STATE_FROZEN

    def die(self):
        self.state = World.STATE_DEAD

    def update(self, delta):
        self.ship.update(delta)

