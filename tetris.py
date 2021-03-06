import copy
import random
from typing import *

EMPTY = (40,44,52)

class Piece:
    #region shapes
    SHAPE_I = [
        [
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
            [0,0,0,0],
        ],
        [
            [0,0,1,0],
            [0,0,1,0],
            [0,0,1,0],
            [0,0,1,0],
        ],
        [
            [0,0,0,0],
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
        ],
        [
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0],
            [0,1,0,0],
        ]
    ]
    SHAPE_J = [
        [
            [1,0,0],
            [1,1,1],
            [0,0,0],
        ],
        [
            [0,1,1],
            [0,1,0],
            [0,1,0],
        ],
        [
            [0,0,0],
            [1,1,1],
            [0,0,1],
        ],
        [
            [0,1,0],
            [0,1,0],
            [1,1,0],

        ]
    ]
    SHAPE_L=[
        [
            [0,0,1],
            [1,1,1],
            [0,0,0],
        ],
        [
            [0,1,0],
            [0,1,0],
            [0,1,1],
        ],
        [
            [0,0,0],
            [1,1,1],
            [1,0,0],
        ],
        [
            [1,1,0],
            [0,1,0],
            [0,1,0],
        ]
    ]
    SHAPE_O=[
        [
            [1,1],
            [1,1],
        ],
        [
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [1, 1],
        ],
        [
            [1, 1],
            [1, 1],
        ],
    ]
    SHAPE_Z=[
        [
            [0,1,1],
            [1,1,0],
            [0,0,0],
        ],
        [
            [0,1,0],
            [0,1,1],
            [0,0,1],
        ],
        [
            [0,0,0],
            [0,1,1],
            [1,1,0],
        ],
        [
            [1,0,0],
            [1,1,0],
            [0,1,0],
        ]
    ]
    SHAPE_T=[
        [
            [0,1,0],
            [1,1,1],
            [0,0,0],
        ],
        [
            [0,1,0],
            [0,1,1],
            [0,1,0],
        ],
        [
            [0,0,0],
            [1,1,1],
            [0,1,0],
        ],
        [
            [0,1,0],
            [1,1,0],
            [0,1,0],
        ]
    ]
    SHAPE_S=[
        [
            [1,1,0],
            [0,1,1],
            [0,0,0],
        ],
        [
            [0,0,1],
            [0,1,1],
            [0,1,0]
        ],
        [
            [0,0,0],
            [1,1,0],
            [0,1,1],
        ],
        [
            [0,1,0],
            [1,1,0],
            [1,0,0],
        ]
    ]
    SHAPES=[SHAPE_I,SHAPE_J,SHAPE_L,SHAPE_O,SHAPE_S,SHAPE_T,SHAPE_Z]
    #endregion

    def __init__(self, x, y, rot, colour: Tuple[int,int,int], shapes: List[List[List[int]]]):
        """
        :param colour: r,g,b tuple
        :param shapes: 2d arrays (matricies) of 1s and 0s, defining rotation positions
        """
        self.shapes = shapes
        self.colour = colour
        self.x = x
        self.y = y
        self.rot = rot

    @property
    def shape(self):
        return self.shapes[self.rot]

    @property
    def lspace(self):
        """
        gets the amount of empty left columns
        :return:
        """
        ret = 1000
        for row in self.shape:
            pre = 0
            for b in row:
                if b:
                    break
                else:
                    pre += 1
            if pre < ret:
                ret = pre
        return ret

    @property
    def rspace(self):
        """
        gets the amount of empty right columns
        :return:
        """
        ret = 1000
        for row in self.shape:
            pre = 0
            for b in reversed(row):
                if b:
                    break
                else:
                    pre += 1
            if pre < ret:
                ret = pre
        return ret

    @property
    def tspace(self):
        i = 0
        for row in self.shape:
            if all([b == 0 for b in row]):
                i += 1
            else:
                return i

    @property
    def bspace(self):
        i = 0
        for row in reversed(self.shape):
            if all([b == 0 for b in row]):
                i += 1
            else:
                return i

    @property
    def width(self):
        return len(self.shape[0]) - self.lspace - self.rspace

    def __str__(self):
        """
        get an ASCII art string representation of the current shape - for debugging
        """
        ret=""
        i=0
        for row in self.shape:
            for b in row:
                if b:
                    ret+="#"
                else:
                    ret+="."
            ret+="\n"
            i+=1
        return ret.strip()

class Board:
    PALETTE = [(224,108,117),
               (152,195,121),
               (209,154,102),
               (97,174,238),
               (198,120,221),
               (86,182,194),
               (171,178,191)]

    def __init__(self):
        # standard Tetris board guidelines:
        self.width = 10
        self.height = 22
        self.hidden_top = 2

        self.board:List[List[Tuple[int,int,int]]]=[]

        self.falling = None
        self.at_rest = False

        self.game_over = False

        # board init
        for i in range(self.height):
            buf = []
            for j in range(self.width):
                buf.append(EMPTY)
            self.board.append(buf)

    def rboard(self):
        """
        rendered board: includes the falling piece as part of the board
        """
        return self.commit_falling(copy.deepcopy(self.board))

    def commit_falling(self, board):
        """
        commits the falling piece into the board
        :return:
        """
        cur_row = 0
        for row in self.falling.shape:
            cur_b = 0
            for b in row:
                if b:
                    board[self.falling.y + cur_row][self.falling.x + cur_b] = self.falling.colour
                cur_b += 1
            cur_row += 1
        return board

    def __str__(self):
        """
        get string representation of board state
        """
        ret=""
        for row in self.rboard():
            for pixel in row:
                if pixel != EMPTY:
                    ret+='#'
                else:
                    ret+='.'
            ret+="\n"
        return ret

    def new_falling(self):
        """
        spawn a random new piece to be falling
        :return:
        """
        self.at_rest = False

        p = Piece(0,0,random.randint(0,3),random.choice(self.PALETTE),random.choice(Piece.SHAPES))
        x = random.randint(0-p.lspace,self.width-p.width-p.lspace)
        p.x=x
        p.y=0-p.tspace

        if not self.check_overlap(p.shape,p.x,p.y):
            self.falling = p
        else:
            # game over
            self.game_over = True

    def check_overlap(self, shape, x, y):
        """
        check if the shape will overlap with anything if committed to the board at the coordinates
        """
        cur_row = 0
        for row in shape:
            cur_b = 0
            for b in row:
                if b:
                    try:
                        if y+cur_row < 0 or x+cur_b<0: return True
                        if self.board[y + cur_row][x+ cur_b] != EMPTY:
                            return True
                    except IndexError:
                        return True
                cur_b += 1
            cur_row += 1
        return False

    def rotate(self,right=True):
        """
        rotate the currently falling piece
        :param right: the direction to loop through the possible rotations
        """
        nr = (self.falling.rot+(1 if right else -1)) % len(self.falling.shapes)
        if not self.check_overlap(self.falling.shapes[nr],self.falling.x,self.falling.y):
            # commit rotation
            self.falling.rot = nr
            self.at_rest = False

    def shift(self, dx):
        """
        shift the currently falling piece
        :return:
        """
        nx = self.falling.x+dx
        if not self.check_overlap(self.falling.shape,nx,self.falling.y):
            # commit shifting
            self.falling.x=nx
            self.at_rest=False

    def drop(self):
        """
        drop the currently falling piece
        """
        while not self.at_rest:
            self.step()

    def step(self):
        if self.game_over:
            print("game over")
            return

        if self.at_rest:
            # commit piece
            self.board = self.commit_falling(self.board)
            self.clear_lines()

            self.new_falling()
        else:
            self.gravity()

    def clear_lines(self):
        cleared=[]
        i=0
        for row in self.board:
            if all([x != EMPTY for x in row]):
                cleared.append(i)
            i+=1

        for i in cleared:
            self.board.pop(i)
            buf = []
            for j in range(self.width):
                buf.append(EMPTY)
            self.board.insert(0,buf)

    def gravity(self):
        nx,ny = (self.falling.x,self.falling.y+1)
        if not self.check_overlap(self.falling.shape,nx,ny):
            self.falling.x=nx
            self.falling.y=ny
        else:
            self.at_rest = True
