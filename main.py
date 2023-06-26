import pygame as pg
import numpy as np
import numba

#settings
width = 960
height = 540
res = width, height
offset = np.array([width, height]) // 2

#texture
texture = pg.image.load('images/texture.jpg')
texture_size = min(texture.get_size()) - 1
texture_array = pg.surfarray.array3d(texture)

class Fractal:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0,0,0], dtype=np.uint8)
        self.x_offset = 1
        self.y_offset = 1
        self.max_iter = 30
        self.zoom = 4 / 1000
        
    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render(screen_array, zoom, max_iter, dx, dy):
        for x in numba.prange(width):
            for y in range(height):
                c = (x - offset[0] - dx) * zoom  + 1j * (y - offset[1] - dy) * zoom
                z = 0
                num_iter = 0
                for i in range(max_iter):
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 > 4:
                        break
                    num_iter +=1
                col = int(texture_size * num_iter / max_iter)
                screen_array[x, y] = texture_array[col, col]
        return screen_array

    def update(self):
        self.screen_array = self.render(self.screen_array, self.zoom, self.max_iter, self.x_offset, self.y_offset)
    
    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def run(self):
        self.update()
        self.draw()

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.fractal = Fractal(self)

    def run(self):

        while True:
            self.screen.fill('black')
            self.fractal.run()
            pg.display.flip()
            x, y = pg.mouse.get_rel()
            
            if pg.mouse.get_pressed()[0] == True:
                self.fractal.x_offset += x
                self.fractal.y_offset += y

            for event in pg.event.get():
                if event.type == pg.MOUSEWHEEL:
                    self.fractal.zoom /= 1.1 ** event.y
                    self.fractal.max_iter *= 1.03 ** event.y
                    self.fractal.x_offset *= 1.1 ** event.y
                    self.fractal.y_offset *= 1.1 ** event.y
                    print(self.fractal.zoom, self.fractal.max_iter, event.y)
                if event.type == pg.QUIT:
                    exit()
                    
            self.clock.tick()
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')

if __name__ == '__main__':
    app = App()
    app.run()