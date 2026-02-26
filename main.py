from settings import *
from tetris import Tetris, Text
import sys
import pathlib


class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption('Tetromino-Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        icon = pg.image.load(resource_path('assets/logo.png')).convert_alpha()
        pg.display.set_icon(icon)
        self.clock = pg.time.Clock()
        pg.mixer.music.load(resource_path('assets/music/invention4-1loop.wav'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(loops=-1)
        self.sfx = {
            'move': pg.mixer.Sound(resource_path('assets/sfx/move.mp3')),
            'rotate': pg.mixer.Sound(resource_path('assets/sfx/rotate.mp3')),
            'break': pg.mixer.Sound(resource_path('assets/sfx/break.mp3')),
        }
        for s in self.sfx.values():
            s.set_volume(0.6)
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_images(self):
        files = [item for item in pathlib.Path(resource_path(SPRITE_DIR_PATH)).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    app = App()
    app.run()
