import sys

from tetris import Board, Piece
import pygame
from pygame.locals import *

class Engine:
    def __init__(self):
        self.board = Board()
        self.screen = pygame.display.set_mode((500,800))

        self.board.new_falling() # initial falling piece

        self.cell_width = 20
        self.offx = 0
        self.offy = 0

    def run(self):
        while True:
            t0 = pygame.time.get_ticks()

            self.draw()
            self.update()

            # wait for remaining time
            pygame.time.wait(40-(pygame.time.get_ticks() - t0))

    def draw(self):
        # clear screen
        self.screen.fill((0,0,0))
        cur_row = 0
        for row in self.board.rboard():
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
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        # gameplay
        self.input_update()
        self.board.step()

    def input_update(self, keys=None):
        if keys is None:
            keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            self.board.shift(-1)
        if keys[K_RIGHT]:
            self.board.shift(1)


if __name__ == '__main__':
    Engine().run()