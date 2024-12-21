from config import *


class Bullet(p.sprite.Sprite):
    def __init__(self, start_x, start_y, dest_x, dest_y, game):
        super(Bullet, self).__init__()

        # Bullet image
        self.image = p.Surface((SCREEN_WIDTH / 100, SCREEN_HEIGHT / 80))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 5
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity

        self.bullet_life = 0

        self.game = game

    def update(self, dt):
        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x

        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        self.bullet_life += dt
        if self.bullet_life >= BULLET_LIFESPAN:
            # This removes the bullet from all sprites and stops updating
            self.game.all_sprites.remove(self)


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

        # Shooting
        self.can_shoot = True
        self.shoot_time = 0

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
        # Shoot cooldown
        if not self.can_shoot:
            self.shoot_time += dt
        if self.shoot_time >= SHOOT_COOLDOWN:
            self.can_shoot = True
            self.shoot_time = 0

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

        # Shooting
        if mouse[0] and self.can_shoot:
            self.can_shoot = False

            destination_x, destination_y = p.mouse.get_pos()
            bullet = Bullet(self.rect.x, self.rect.y, destination_x, destination_y, game=self.game)
            self.game.all_sprites.add(bullet)
            self.game.all_bullets.add(bullet)

    def movement(self, dt):
        pass

    def collisions(self, dt):
        pass
