import os
import pygame

class Font:
    def __init__(self, dim, latex_font=False) -> None:
        
        self.original = int(dim)

        self.latex_font = latex_font

        self.dim_font = self.original 

        if self.latex_font:        
            path_r = os.path.join('TEXTURES', 'century_r.TTF')
            path_b = os.path.join('TEXTURES', 'century_b.TTF')
            path_i = os.path.join('TEXTURES', 'century_i.TTF')
        else:
            path_r = os.path.join('TEXTURES', 'font_r.ttf')
            path_b = os.path.join('TEXTURES', 'font_b.ttf')
            path_i = os.path.join('TEXTURES', 'font_i.ttf')
        
        self.font_pyg_r = pygame.font.Font(path_r, self.dim_font)
        self.font_pyg_i = pygame.font.Font(path_i, self.dim_font)
        self.font_pyg_b = pygame.font.Font(path_b, self.dim_font)

        self.font_pixel_dim = self.font_pyg_r.size("a")


    def scala_font(self, moltiplicatore):

        if moltiplicatore == -1:
            if self.dim_font != self.original:
                self.dim_font = self.original
        else:
            self.dim_font *= moltiplicatore 
    
        if self.latex_font:    
            path_r = os.path.join('TEXTURES', 'century_r.TTF')
            path_b = os.path.join('TEXTURES', 'century_b.TTF')
            path_i = os.path.join('TEXTURES', 'century_i.TTF')
        else:
            path_r = os.path.join('TEXTURES', 'font_r.ttf')
            path_b = os.path.join('TEXTURES', 'font_b.ttf')
            path_i = os.path.join('TEXTURES', 'font_i.ttf')
        
        self.font_pyg_r = pygame.font.Font(path_r, round(self.dim_font))
        self.font_pyg_i = pygame.font.Font(path_i, round(self.dim_font))
        self.font_pyg_b = pygame.font.Font(path_b, round(self.dim_font))

        self.font_pixel_dim = self.font_pyg_r.size("a")