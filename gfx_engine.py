import sys
import tetris
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

        self.tickno = 0
        self.frame_time = 20
        self.speed = 2

        self.screen = pygame.display.set_mode((self.cell_width*self.board.width,
                                               self.cell_width*(self.board.height-self.board.hidden_top)))

    def run(self):
        while True:
            t0 = pygame.time.get_ticks()

            self.draw()
            self.update()

            # wait for remaining time
            pygame.time.wait(self.frame_time-(pygame.time.get_ticks() - t0))
            self.tickno+=1

    def draw(self):
        # clear screen
        self.screen.fill(tetris.EMPTY)
        cur_row = 0
        for row in self.board.rboard()[self.board.hidden_top:]:
            cur_cell = 0
            for cell in row:

                rect=pygame.Rect(
                    cur_cell*self.cell_width,
                    cur_row*self.cell_width,
                    self.cell_width,
                    self.cell_width)

                pygame.draw.rect(self.screen,cell,rect)
                pygame.draw.rect(self.screen,tetris.EMPTY,rect,1)
                cur_cell+=1
            cur_row+=1

        pygame.display.flip()

    def update(self):

        # gameplay
        self.input_update()

        if self.tickno % (self.frame_time//self.speed) == 0:
            self.board.step()
            self.speed+=0.001 # increase speed as time goes on to incr difficult

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
                if event.key == pygame.K_DOWN:
                    self.board.drop()


if __name__ == '__main__':
    Engine().run()