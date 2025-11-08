import arcade

SCREEN_WIDTH = 800 * 3 + 210
SCREEN_HEIGHT = 600
SCREEN_TITLE = "FlappyBirdus"

BIRD_SPEED = 5
LIMIT_ANGLE = 45

GRAVITATION = 0.2
GRAVITATION_ANGLE = 0.4

DISTANCE = 150
PIPE_SPEED = 4

ENDGAME_SIZE = 2


class Pipe(arcade.Sprite):
    def __init__(self, is_up):
        super().__init__("images/pipe.png", 0.2, flipped_vertically=is_up)

    def update(self):
        self.center_x -= self.change_x
        if self.right < 0:
            self.left = SCREEN_WIDTH


class Bird(arcade.Sprite):
    def __init__(self):
        super().__init__("images/bird/bluebird-downflap.png", 1)
        self.angle = 0
        self.change_angle = 0
        self.hit_sound = arcade.load_sound("audio/hit.wav")
        self.wing_sound = arcade.load_sound("audio/wing.wav")

    def update(self):
        self.angle -= self.change_angle
        self.center_y += self.change_y

        self.change_y -= GRAVITATION
        self.change_angle += GRAVITATION_ANGLE

        if self.angle > LIMIT_ANGLE:
            self.angle = LIMIT_ANGLE

        if self.angle < -LIMIT_ANGLE:
            self.angle = -LIMIT_ANGLE

        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
            self.change_y = 0
        if self.bottom < 0:
            self.bottom = 0
            self.change_y = 0


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("images/bg.png")
        self.bird = Bird()
        self.pipe_list = arcade.SpriteList()
        self.grass = arcade.load_texture("images/grass.png")

        self.game = True
        self.game_end = arcade.load_texture("images/gameover.png")

    def on_key_press(self, symbol, modifiers):
        if self.game == True:
            if symbol == arcade.key.SPACE:
                self.bird.wing_sound.play(volume=0.20)
                self.bird.change_y = BIRD_SPEED
                self.bird.change_angle = -7

    def setup(self):
        self.bird.center_x = 50
        self.bird.center_y = SCREEN_HEIGHT / 2

        for i in range(6 * 3):
            pipe_bottom = Pipe(is_up=False)
            pipe_bottom.center_y = 45
            pipe_bottom.center_x = DISTANCE * i + SCREEN_WIDTH
            pipe_bottom.change_x = PIPE_SPEED
            self.pipe_list.append(pipe_bottom)

            pipe_top = Pipe(is_up=True)
            pipe_top.center_y = SCREEN_HEIGHT
            pipe_top.center_x = pipe_bottom.center_x
            pipe_top.change_x = PIPE_SPEED
            self.pipe_list.append(pipe_top)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)

        self.pipe_list.draw()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.grass)
        self.bird.draw()
        if self.game == False:
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.game_end.width * ENDGAME_SIZE, self.game_end.height * ENDGAME_SIZE, self.game_end)

    def update(self, delta_time):
        if self.game == True:
            self.bird.update()
            self.pipe_list.update()
            hit_list = arcade.check_for_collision_with_list(self.bird, self.pipe_list)
            if len(hit_list) > 0:
                self.bird.hit_sound.play(volume=0.20)
                self.bird.stop()
                self.game = False
                for pipe in self.pipe_list:
                    pipe.stop()


def main():
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
