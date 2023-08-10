from const import*
from square import Square
from piece import *
from move import Move
import copy
from sound import Sound
import os
class Board:
    #using the '_' signifies private functions only to be called by the board.
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self.last_move=None
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):
        for row in range(ROWS):
            for col in range (COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6,7) if color =='white' else (1, 0)
        #These are all for the pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other,1,Knight(color))
        self.squares[row_other][6] = Square(row_other,6, Knight(color))
        #TESTING PURPOSES ONLY: self.squares[4][4]= Square(4,4,Knight(color))

        #Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other,0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color) )
    def calc_move(self, piece, row, col, bool =True):
        '''
         Calculate all the possible valid moves of a specific piece on a specific position
        '''

        def pawn_moves():
            #steps for pawns
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir
            end = row+ (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        #create initial and final move
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # Create a new move
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)
                    #blocked and this means another piece is in front of our pawn
                    else: break
                    #not in range
                else: break

            #diagnal moves
            move_row = row + piece.dir
            move_col = [col-1,col+1]
            for move_col in move_col:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][move_col].piece
                        final = Square(move_row, move_col, final_piece)

                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                        else:
                            piece.add_moves(move)

            #en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color =='white' else 5
            #left en passant
            if Square.in_range(col-1) and row == r: # left en passant
                if self.squares[row][col-1].has_rival_piece(piece.color):
                    p = self.squares[row][col-1].piece

                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)

                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)

            if Square.in_range(col + 1) and row == r:  # left en passant
                if self.squares[row][col + 1].has_rival_piece(piece.color):
                    p = self.squares[row][col + 1].piece

                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)

                            move = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)





        def knight_moves():
            #8 possibles moves at most
            possible_moves = [
                (row -2, col+1),
                (row -1, col+2),
                (row +1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col -2),
                (row -1, col -2),
                (row -2, col-1),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        #create new squares
                        intial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)# send the piece later.
                        #create a new move
                        move = Move(intial, final)
                        #append final moves
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)
                            else: break
                        else:
                            piece.add_moves(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)
                        #empty space
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)

                            else:
                                piece.add_moves(move)
                        #enemy space


                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_moves(move)
                            else:
                                piece.add_moves(move)
                            break


                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else: break

                    #incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adj = [
                (row-1,col+ 0), #up
                (row+1, col +0),#down
                (row +0, col-1),#left
                (row +0, col+1), #right
                (row-1, col-1),#Up-left
                (row+1, col -1), #down-left
                (row -1, col +1), # Up-Right
                (row +1, col +1) #down-right
            ]
            # normal moves
            for possible_moves in adj:
                possible_move_row, possible_move_col = possible_moves

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial= Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_moves(move)

                            else:break
                        else:
                            piece.add_moves(move)
            #Queen Castling
            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c==3:
                                #adds left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial= Square(row, 0)
                                final = Square(row, 3)
                                moveL = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveL):
                                        left_rook.add_moves(moveL)
                                        piece.add_moves(moveK)

                                else:
                                    piece.add_moves(moveK)
                                    left_rook.add_moves(moveL)


            #King castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c==6:
                                #adds right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial= Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_moves(moveR)
                                        piece.add_moves(moveK)


                                else:
                                    piece.add_moves(moveK)
                                    right_rook.add_moves(moveR)

        if isinstance(piece, Pawn): pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1,1), #up-right
                (-1,-1),#up-left
                (1,1),#down-right
                (1,-1)# down - left
                ])
        elif isinstance(piece, Rook):
            straightline_moves([
                (-1,0),#up
                (0,1),#right
                (1,0),#down
                (0,-1)#left
                ])
        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down - left

                (-1, 0),  # up
                (0, 1),  # right
                (1, 0),  # down
                (0, -1)  # left

            ])
        elif isinstance(piece, King):king_moves()

    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final
        en_passant_empty = self.squares[final.row][final.col].isempty()
        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece =piece


        diff = final.col - initial.col
        if diff !=0 and en_passant_empty:
            self.squares[initial.row][initial.col+diff].piece = None
            self.squares[final.row][final.col].piece = piece
            if not testing:
                sound = Sound(os.path.join(f'Assets-Images-Sounds/sounds/capture.wav'))
                sound.play()


        #pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        piece.moved = True

        piece.clear_moves()
        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row== 0 or final.row ==7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_move(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True

        return False

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True


