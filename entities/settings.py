import pygame as pg
import numpy as np
import math
import numba

class screen:
    def __init__(self):
        #settings
        self.width = 960
        self.height = 540
        self.res = self.width, self.height
        self.offset = np.array([self.width, self.height]) // 2

        #texture
        self.texture = pg.image.load('images/texture.jpg')
        self.texture_size = min(self.texture.get_size()) - 1
        self.texture_array = pg.surfarray.array3d(self.texture)