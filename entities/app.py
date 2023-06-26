from entities.fractals import Fractal
from entities.settings import screen
import pygame as pg
import numpy as np
import math
import numba

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(screen.res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.fractal = Fractal(self)

    def run(self):

        while True:
            self.screen.fill('black')
            self.fractal.run()
            pg.display.flip()
                    
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')