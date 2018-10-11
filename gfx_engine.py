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
        self.frame_time = 20 # amount of ms each frame is to be shown
        self.speed = 2
        self.hold_time = 200 # amount of ms for a button to be held
        self.hold_speed = 30 # amount of ms between updates when holding

        # setup
        self.screen = pygame.display.set_mode((self.cell_width*self.board.width,
                                               self.cell_width*(self.board.height-self.board.hidden_top)))
        pygame.display.set_caption('Makurell Tetris')

        pygame.font.init()
        self.font1 = pygame.font.SysFont('Arial',20)
        self.font2 = pygame.font.SysFont('Arial',15)

        self.down_keys = {}

    def run(self):
        last_game_running = 0
        while True:
            t0 = pygame.time.get_ticks()

            if not self.board.game_over:
                self.draw()
                self.update()
                last_game_running = self.tickno
            else:
                # game over screen
                if self.tickno*self.frame_time % (self.hold_speed*1) == 0 and (self.tickno-last_game_running)<10:
                    # fade background
                    self.draw_transp()
                    pygame.display.flip()
                else:
                    # text
                    self.draw_text(self.font1,'Game Over',0.5,0.5)

            # wait for remaining time
            pygame.time.wait(self.frame_time-(pygame.time.get_ticks() - t0))
            self.tickno+=1

    def draw_text(self, font, text:str, x:float, y:float, center=True, colour=(255,255,255)):
        """
        Draw given text at the specified position. Coords to be given as fractions of total width/height.
        """
        if not center:
            # top-left
            rx, ry = self.screen.get_width()*x, self.screen.get_height()*y
        else:
            w, h = font.size(text)
            rx, ry = self.screen.get_width()*x-(w/2.0), self.screen.get_height()*y-(h/2.0)

        self.screen.blit(font.render(text,False,colour),(rx,ry))

    def draw_transp(self,alpha=100):
        """
        draw a semi-transparent overlay on top of the screen
        """
        transp = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
        transp.set_alpha(alpha)
        transp.fill(tetris.EMPTY)
        self.screen.blit(transp,(0,0))

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

    def should_register(self, key):
        return key in self.down_keys \
               and (self.down_keys[key] == self.tickno
                    or (self.tickno - self.down_keys[key])*self.frame_time>self.hold_time
                    and self.tickno*self.frame_time % self.hold_speed == 0)

    def input_update(self, events=None):
        if events is None:
            events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self.down_keys[event.key] = self.tickno

            if event.type == pygame.KEYUP:
                try:
                    del self.down_keys[event.key]
                except KeyError:
                    # x not in dict = ignore
                    pass

        if self.should_register(pygame.K_LEFT):
                self.board.shift(-1)
        if self.should_register(pygame.K_RIGHT):
            self.board.shift(1)
        if self.should_register(pygame.K_SPACE) or self.should_register(pygame.K_UP):
            self.board.rotate()
        if self.should_register(pygame.K_DOWN):
            self.board.drop()


if __name__ == '__main__':
    Engine().run()