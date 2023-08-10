import pygame
import os
from sound import Sound
from theme import Theme

class Config:

    def __init__(self):
        self.idx =1 #1. Green/White, 2. Brown, 3. Blue/White, 4. Dark Gray

        self.themes = []
        self._add_theme()
        self.theme = self.themes[self.idx]
        #font
        self.font = pygame.font.SysFont('monospace', 18, bold = True)
        self.move_sound = Sound(
            os.path.join('Assets-Images-Sounds/sounds/move.wav'))
        self.capture_sound = Sound(
            os.path.join('Assets-Images-Sounds/sounds/capture.wav'))

    def change_theme(self):
        self.idx +=1
        self.idx %= len(self.themes) # [T1, T2, T3, T4]
        self.theme = self.themes[self.idx]



    def _add_theme(self):
        #               light_bg,        dark_bg,       light_trace,    dark_trace,     light_moves,    dark_moves
        #green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C846446')
        brown = Theme((235, 209, 166), (165, 117, 80), (245,234,100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229,228,200), (60,95, 135), (123,187,227), (43,119,191), '#C86464', '#C84646')
        gray = Theme((120,119,118), (86,85,84), (99,126,143), (82, 102, 128), '#C86464', '#C84646')


        self.themes = [brown, blue, gray]