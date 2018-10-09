from tetris import Board, Piece
import pygame

class Engine:
    def __init__(self):
        self.board = Board

    def run(self):
        t0 = pygame.time.get_ticks()

        self.draw()
        self.update()

        # wait for remaining time
        pygame.time.wait(40-(pygame.time.get_ticks() - t0))

    def draw(self):
        pass

    def update(self):
        pass