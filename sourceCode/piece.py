import os
class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect= None):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False
        self.piece_style = 0
        self.num_of_styles = 3
        value_sign = 1 if color =='white' else -1
        self.value = value *value_sign
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, num=2):
        if num is not range(0,3):
            num = 0

        textures = [f'Assets-Images-Sounds/white_vs_blue/{self.color}_{self.name}.png',
                    f'Assets-Images-Sounds/gold_vs_black/{self.color}_{self.name}.png',
                    f'Assets-Images-Sounds/white_vs_black/{self.color}_{self.name}.png',
                    f'Assets-Images-Sounds/gold_vs_blue/{self.color}_{self.name}.png']

        self.texture = os.path.join(textures[num])

    def change_texture(self):
        print('else')
        self.piece_style= self.piece_style+1
        if self.piece_style>3:
            self.piece_style = 0
        num = self.piece_style
        self.set_texture(num)

    def add_moves(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []
class Pawn(Piece):
    def __init__(self, color):
        self.dir =-1 if color =='white' else 1
        self.en_passant = False
        super().__init__('pawn', color, 1.0,)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.0001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)
class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000000.0)
