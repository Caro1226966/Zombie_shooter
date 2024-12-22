from config import *


class Zombie(p.sprite.Sprite):
    def __init__(self, x, y, game):
        super(Zombie, self).__init__()

        # Zombie image
        self.image = p.Surface((SCREEN_WIDTH / 80, SCREEN_HEIGHT / 75))
        self.image.fill((0, 100, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.game = game

        self.speed = 1.5

        self.attack_ready = True
        self.attack_time = 0

    def update(self, dt):
        # Call required functions
        self.collisions(dt)
        self.handle_flags(dt)

        # Find direction vector (dx, dy) between enemy and player.
        dirvect = p.math.Vector2(self.game.player.rect.x - self.rect.x,
                                 self.game.player.rect.y - self.rect.y)
        try:
            dirvect.normalize()
            # Move along this normalized vector towards the player at current speed.
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)

        except:
            pass

    def collisions(self, dt):
        collided_bullets = p.sprite.spritecollide(self, self.game.all_bullets, True)

        for bullet in collided_bullets:
            self.game.all_sprites.remove(self)
            self.game.all_zombies.remove(self)
            self.game.player.score += 1

        collided_players = p.sprite.spritecollide(self, self.game.all_players, False)

        for player in collided_players:
            if self.attack_ready:
                self.attack_ready = False
                self.game.player.health -= 1

    # Handles flags
    def handle_flags(self, dt):
        if not self.attack_ready:
            self.attack_time += dt
        if self.attack_time >= ZOMBIE_ATTACK_COOLDOWN:
            self.attack_ready = True
            self.attack_time = 0


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

        self.screen = SCREEN

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

        # Zombie spawning
        self.zombie_spawntime = 0
        self.can_spawn_zombies = True
        self.zombie_cooldown = 2

        self.score = 0

        # self.image = game.loader.get_image("purple_player")

    def update(self, dt):
        # Calls the needed functions
        self.inputs(dt)
        self.clipping(dt)
        self.handle_flags(dt)

        # Zombie spawning
        if self.can_spawn_zombies:
            self.can_spawn_zombies = False

            for i in range(random.randint(0, 5)):
                zombie = Zombie(random.randint(0, SCREEN_WIDTH),
                                random.randint(0, SCREEN_HEIGHT), self.game)

                self.game.all_sprites.add(zombie)
                self.game.all_zombies.add(zombie)

            if not self.zombie_spawntime <= 0.5:
                self.zombie_spawntime -= 0.5

        if self.health <= 0:
            print('You Died!!!')
            print('You scored', self.score)
            exit()

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

        # Zombie spawning
        if not self.can_spawn_zombies:
            self.zombie_spawntime += dt
        if self.zombie_spawntime >= self.zombie_cooldown:
            self.can_spawn_zombies = True
            self.zombie_spawntime = 0

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

