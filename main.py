from settings import *
from tetris import Tetris, Text
from ranking_manager import RankingManager
import sys
import pathlib


class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.game_over = False
        self.ranking_manager = RankingManager()

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
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

    def display_game_over(self):
        self.screen.fill(BG_COLOR)
        font = pg.font.Font(FONT_PATH, 40)
        text_surface = font.render("GAME OVER", True, "white")
        text_rect = text_surface.get_rect(center=(WIN_W // 2, WIN_H // 2))
        self.screen.blit(text_surface, text_rect)
        pg.display.flip()
        pg.time.wait(3000)

        player_name = input("Digite seu nome para o ranking: ").strip()
        self.ranking_manager.add_score(player_name, self.tetris.score)
        self.ranking_manager.display_rankings()

        self.restart_game()

    def restart_game(self):
        self.__init__()

    def update(self):
        if not self.game_over:
            self.tetris.update()
            self.clock.tick(FPS)

    def draw(self):
        if self.game_over:
            self.display_game_over()
        else:
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
    App().run()
