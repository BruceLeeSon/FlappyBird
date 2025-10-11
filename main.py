import arcade
from pyglet.event import EVENT_HANDLE_STATE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "FlappyBirdus"


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bird/bluebird-downflap.png", 1)

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        self.center_y += self.change_y
        self.change_y -= 0.2

class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("images/bg.png")
        self.fullscreen_rect = arcade.Rect(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT,
                                           SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.bird = Bird()

    def on_key_press(self, symbol: int, modifiers: int) -> EVENT_HANDLE_STATE:
        if symbol == arcade.key.SPACE:
            self.bird.change_y = 5

    def setup(self):
        self.bird.center_x = 50
        self.bird.center_y = SCREEN_HEIGHT / 2

    def on_draw(self) -> EVENT_HANDLE_STATE:
        self.clear((255, 255, 255))
        arcade.draw_texture_rect(self.bg, self.fullscreen_rect)
        arcade.draw_sprite(self.bird)

    def on_update(self, delta_time: float) -> bool | None:
        self.bird.update(delta_time)



window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()

arcade.run()
