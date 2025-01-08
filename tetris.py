from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        # Texto de título (TETRIS no centro superior)
        title_text = 'TETRIS'
        title_pos = (WIN_W // 2, WIN_H * 0.05)
        self.render_centered_text(title_text, title_pos, TILE_SIZE * 1.2, self.get_color())

        # Pontuação atual
        score_label = 'Score'
        score_label_pos = (WIN_W * 0.8, WIN_H * 0.05)
        self.render_centered_text(score_label, score_label_pos, TILE_SIZE * 0.6, 'orange')

        score_value = f'{self.app.tetris.score}'
        score_value_pos = (WIN_W * 0.8, WIN_H * 0.1)
        self.render_centered_text(score_value, score_value_pos, TILE_SIZE * 0.9, 'white')

        # Maior pontuação (High Score)
        high_score_label = 'High Score'
        high_score_label_pos = (WIN_W * 0.8, WIN_H * 0.15)
        self.render_centered_text(high_score_label, high_score_label_pos, TILE_SIZE * 0.6, 'orange')

        high_score_value = self.get_high_score()
        high_score_value_pos = (WIN_W * 0.8, WIN_H * 0.2)
        self.render_centered_text(high_score_value, high_score_value_pos, TILE_SIZE * 0.9, 'white')

        # Próximo Tetromino
        next_text = 'Next'
        next_pos = (WIN_W * 0.8, WIN_H * 0.3)
        self.render_centered_text(next_text, next_pos, TILE_SIZE * 0.7, 'orange')

    def get_high_score(self):
        rankings = self.app.ranking_manager.rankings
        if rankings:
            return str(rankings[0]['score'])  # Maior score do ranking
        return "0"

    def render_centered_text(self, text, position, size, color, bgcolor=None):
        text_surface, rect = self.font.render(text, fgcolor=color, size=size, bgcolor=bgcolor)
        rect.center = position
        self.app.screen.blit(text_surface, rect)


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.score = 0
        self.full_lines = 0
        self.lines_cleared = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.lines_cleared += self.full_lines
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, row)

            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0

                self.full_lines += 1

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            self.app.game_over = True
            return True
        return False

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                return
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if not self.app.game_over:
            if pressed_key == pg.K_LEFT:
                self.tetromino.move(direction='left')
            elif pressed_key == pg.K_RIGHT:
                self.tetromino.move(direction='right')
            elif pressed_key == pg.K_UP:
                self.tetromino.rotate()
            elif pressed_key == pg.K_DOWN:
                self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        if not self.app.game_over:
            trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
            if trigger:
                self.check_full_lines()
                self.tetromino.update()
                self.check_tetromino_landing()
                self.get_score()
            self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
        
