from config import *


# TODO list
# 1. make background (repeating images 'n shi')
# 2. make player and movement
# 3. make zombies
# 4. make zombies go to player and attack them (health for player)
# 5. make a gun that shoots bullets to kill zombies
# 6. enjoy


class ResourceLoader:
    def __init__(self):
        self.images = {}
        for file in os.listdir(RES_DIR):  # Getcwd means get current working directory
            if file.endswith('.png') or file.endswith('.gif'):
                # print(file.replace('.png', ''))   #OTHERS
                # print(file.split('.')[0])         #OTHERS
                file_path = os.path.join(RES_DIR, file)
                self.images[file[:-4]] = p.image.load(file_path).convert_alpha()

    def get_image(self, key):
        return self.images.get(key)


# This handles the game state
class State:
    def __init__(self):
        # State control
        self.prev_state = None
        self.current_state = None

    # Creates a new state
    def add(self, new):
        self.prev_state = self.current_state

        self.current_state = new

    # Updates the states
    def update(self, dt):
        self.current_state.update(dt)

    # Handles events
    def events(self):
        self.current_state.events()

    # Draws the screen
    def draw(self, screen):
        self.current_state.draw(screen)


class Manager:
    def __init__(self, game):
        # Set up displays
        self.screen = SCREEN
        self.loader = ResourceLoader()

        # Sprite groups
        self.all_sprites = p.sprite.Group()

        # Variables
        self.death = False
        self.game = game

    # This updates everything
    def update(self, dt):
        self.all_sprites.update(dt)

        if self.death:
            self.game.state.add(GameOver())

    # This draws the screen
    def draw(self, screen):
        self.all_sprites.draw(screen)

    # This updates and handles the events
    def events(self):
        pass


class Game:
    def __init__(self):

        # This creates the clock
        self.clock = p.time.Clock()

        # This is dt
        self.accumulator = 0.0
        self.time_step = 1 / TARGET_FPS

        self.state = State()
        self.state.add(Manager(self))

        self.timer = 0

    def run(self):
        # This makes the below continuously repeat until quit
        running = True
        while running:
            # This limits the computer's fps to 60
            dt = self.clock.tick() / 1000

            self.events()

            # This lets you close the screen when x is pressed
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                # This lets you close the screen when ESCAPE is pressed
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        running = False

            self.accumulator += dt
            while self.accumulator >= self.time_step:
                self.update(self.time_step)
                self.accumulator -= self.time_step

            self.draw(SCREEN, Manager)

    # This updates everything
    def update(self, dt):
        self.state.update(dt)

    # This updates and handles the events
    def events(self):
        self.state.events()

    # This draws the screen
    def draw(self, screen, manager):
        # bg = self.loader.get_image("Flowery_meadows")
        screen.fill((0, 0, 0))
        self.state.draw(screen)
        p.display.update()


class GameOver:
    @staticmethod
    def draw(screen):
        pass

    @staticmethod
    def events():
        if p.key.get_pressed()[p.K_q]:
            exit()

    def update(self, dt):
        pass


if __name__ == "__main__":
    g = Game()
    g.run()
