import time

from tetris import Piece, Board
from pprint import pprint

b = Board()
p = Piece(0,0,0,(255,255,255),Piece.SHAPE_L)
#
# print(p)
# print(p.lspace)
# print(p.rspace)
# print(p.tspace)
# print(p.bspace)


# b.pieces.append(p)
b.new_falling()
print(b)
while True:
    b.step()
    print(b)
    time.sleep(.2)