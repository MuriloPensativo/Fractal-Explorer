import pygame as pg
import numpy as np
from entities.settings import screen
import math
import numba

class Fractal:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((screen.width, screen.height, 3), [0,0,0], dtype=np.uint8)
        self.x_offset = 1
        self.y_offset = 1
        self.max_iter = 30
        self.zoom = 4 / 1000
        
    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render(screen_array, zoom, max_iter, delta_x, delta_y):
        for x in numba.prange(screen.width):
            for y in range(screen.height):
                c = (x - screen.offset[0] - delta_x) * zoom  + 1j * (y - screen.offset[1] - delta_y) * zoom
                z = 0
                num_iter = 0
                for i in range(max_iter):
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 > 4:
                        break
                    num_iter +=1
                col = int(screen.texture_size * num_iter / max_iter)
                screen_array[x, y] = screen.texture_array[col, col]
        return screen_array
    
    def controls(self):
        x, y = pg.mouse.get_rel()
        if pg.mouse.get_pressed()[0] == True:
            self.x_offset += x
            self.y_offset += y
        else:
            pg.mouse.get_rel()
        for event in pg.event.get():
            if event.type == pg.MOUSEWHEEL:
                self.zoom /= 1.1 ** event.y
                self.max_iter *= 1.03 ** event.y
                self.x_offset *= 1.1 ** event.y
                self.y_offset *= 1.1 ** event.y
                print(self.fractal.zoom, self.fractal.max_iter, event.y)
            if event.type == pg.QUIT:
                exit()

    def update(self):
        self.controls()
        self.screen_array = self.render(self.screen_array, self.zoom, self.max_iter, self.x_offset, self.y_offset)
    
    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()