from config import *


# This is the player
class Player(p.sprite.Sprite):
    def __init__(self, x, y, game, health=20):
        super(Player, self).__init__()

        # Player variables
        self.game = game
        self.health = health

        # Player dimensions
        self.image = p.Surface((SCREEN_WIDTH / 30, SCREEN_HEIGHT / 25))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # self.image = game.loader.get_image("purple_player")

    def update(self, dt):
        # Calls the needed functions
        self.inputs(dt)
        self.movement(dt)
        self.clipping(dt)
        self.handle_flags(dt)

    def clipping(self, dt):
        # Handles wrapping around screen
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

    def handle_flags(self, dt):
        pass

    def inputs(self, dt):
        # Player Controls
        keys = p.key.get_pressed()
        mouse = p.mouse.get_pressed()

        # Player key presses
        if keys[p.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[p.K_w]:
            self.rect.y -= PLAYER_SPEED
        if keys[p.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[p.K_s]:
            self.rect.y += PLAYER_SPEED

    def movement(self, dt):
        pass

    def collisions(self, dt):
        pass
