import sys

from tetris import Board, Piece
import pygame
from pygame.locals import *

class Engine:
    def __init__(self):
        self.board = Board()

        self.board.new_falling() # initial falling piece

        self.cell_width = 20
        self.offx = 0
        self.offy = 0

        self.screen = pygame.display.set_mode((self.cell_width*self.board.width,
                                               self.cell_width*(self.board.height-self.board.hidden_top)))

    def run(self):
        while True:
            t0 = pygame.time.get_ticks()

            self.draw()
            self.update()

            # wait for remaining time
            pygame.time.wait(200-(pygame.time.get_ticks() - t0))

    def draw(self):
        # clear screen
        self.screen.fill((0,0,0))
        cur_row = 0
        for row in self.board.rboard()[self.board.hidden_top:]:
            cur_cell = 0
            for cell in row:
                pygame.draw.rect(self.screen,cell,pygame.Rect(
                    cur_cell*self.cell_width,
                    cur_row*self.cell_width,
                    self.cell_width,
                    self.cell_width))
                cur_cell+=1
            cur_row+=1

        pygame.display.flip()

    def update(self):

        # gameplay
        self.input_update()
        self.board.step()

    def input_update(self, events=None):
        if events is None:
            events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.board.shift(-1)
                if event.key == pygame.K_RIGHT:
                    self.board.shift(1)
                if event.key == pygame.K_SPACE:
                    self.board.rotate()


if __name__ == '__main__':
    Engine().run()