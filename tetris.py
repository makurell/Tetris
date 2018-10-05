from typing import *

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
        ]*4
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
    #endregion

    @property
    def shape(self):
        return self.shapes[self.rot]

    @property
    def lspace(self):
        """
        gets the amount of empty left columns
        :return:
        """
        ret=1000
        for row in self.shape:
            pre=0
            for b in row:
                if b:
                    break
                else:
                    pre+=1
            if pre<ret:
                ret=pre
        return ret

    @property
    def rspace(self):
        """
        gets the amount of empty right columns
        :return:
        """
        ret=1000
        for row in self.shape:
            pre=0
            for b in reversed(row):
                if b:
                    break
                else:
                    pre+=1
            if pre<ret:
                ret=pre
        return ret

    @property
    def tspace(self):
        i=0
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

    def __init__(self, x, y, rot, colour: Tuple[int,int,int], shapes: List[List[List[int]]]):
        """
        :param colour: r,g,b tuple
        :param shapes: array of 16bit binary numbers (4x4 matricies) defining orientations
        """
        self.shapes = shapes
        self.colour = colour
        self.x = x
        self.y = y
        self.rot = rot

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
    def __init__(self):
        # standard Tetris board guidelines:
        self.width = 10
        self.height = 22
        self.hidden_top = 2

        self.pieces:List[Piece]=[]

    @property
    def grid(self):
        """
        return a 2d array of (r,g,b) values representing the state of the board: [x][y]
        :return: List[List[Tuple[int,int,int]]]
        """
        # board init
        ret:List[List[Tuple[int,int,int]]]=[]
        for i in range(self.height):
            buf=[]
            for j in range(self.width):
                buf.append((0,0,0))
            ret.append(buf)

        # pieces
        for piece in self.pieces:
            cur_row = 0
            for row in piece.shape:
                cur_b = 0
                for b in row:
                    if b:
                        ret[piece.y+cur_row][piece.x+cur_b] = piece.colour
                    cur_b+=1
                cur_row+=1
        return ret

    def __str__(self):
        """
        get string representation of board state
        """
        ret=""
        for row in self.grid:
            for pixel in row:
                if pixel != (0,0,0):
                    ret+='#'
                else:
                    ret+='.'
            ret+="\n"
        return ret