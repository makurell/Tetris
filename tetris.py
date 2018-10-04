from typing import *

class Pos:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Piece:

    def __init__(self, pos, rot, colour: Tuple[int,int,int], shapes: List[List[int]]):
        """
        :param colour: r,g,b tuple
        :param shapes: array of 16bit binary numbers (4x4 matricies) defining orientations
        """
        self.shapes = shapes
        self.colour = colour
        self.pos = pos
        self.rot = rot

    def __str__(self):
        """
        get an ASCII art string representation of the current shape - for debugging
        """
        ret=""
        shape = self.shapes[self.rot]
        i=0
        for b in shape:
            if i%4==0:
                ret+="\n"
            if b:
                ret+="#"
            else:
                ret+="."
            i+=1
        return ret.strip()
