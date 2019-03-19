class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y

class Ship:
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)

    def update(self, delta):
        pass


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ship = Ship(self, 100, 100)