from tetris import Piece, Board
from pprint import pprint

b = Board()
p = Piece(0,0,0,(255,255,255),Piece.SHAPE_J)

print(p)
print(p.lspace)
print(p.rspace)
print(p.tspace)
print(p.bspace)


b.pieces.append(p)
# print(b)