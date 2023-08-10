import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from piece import Piece

from config import Config
class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.piece = Piece('a','black', 1)

    def mainloop(self):
        game =self.game
        board = self.game.board
        screen = self.screen
        dragger = self.game.dragger
        p = self.piece



        while True:
            #show methods
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                #click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY //SQSIZE
                    clicked_col = dragger.mouseX //SQSIZE

                    #if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece= board.squares[clicked_row][clicked_col].piece
                        if piece.color ==game.next_player:

                            board.calc_move(piece, clicked_row, clicked_col, bool = True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            #show methods
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)


                #click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY //SQSIZE
                        released_col = dragger.mouseX //SQSIZE

                        #create a possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            game.play_sound(captured)
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            #use your show methods
                            game.show_bg(screen)
                            game.show_pieces(screen)
                            game.next_turn()


                    dragger.undrag_piece(event.pos)
                #key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key==pygame.K_p:
                        print('something')
                        game.show_pieces(screen)
                        p.change_texture()




                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger




                #Quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
main = Main()
main.mainloop()