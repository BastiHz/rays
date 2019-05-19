"""Experiments with ray casting in Python and Pygame.


Copyright (C) 2019 Sebastian Henz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import sys
import math
import pygame as pg
from pprint import pprint

import ray
import wall


class App:
    def __init__(self):
        width = 800
        self.height = 400
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.main_surface = pg.display.set_mode((width, self.height))
        self.half_width = width // 2
        self.half_height = self.height // 2
        self.top_view = pg.Surface((self.half_width, self.height))
        self.front_view = pg.Surface((self.half_width, self.height))

        pg.mouse.set_visible(False)
        self.background_color = (20, 20, 20)

        self.raycaster = ray.RayCaster(self.half_width // 2, self.half_height, 0)
        self.raycaster.make_new_rays(math.pi/2, self.half_width)

        # -1 because otherwise w and h are off screen:
        w = self.half_width - 1
        h = self.height - 1
        self.walls = [
            wall.Wall(0, 0, w, 0),  # top
            wall.Wall(0, 0, 0, h),  # left
            wall.Wall(w, 0, w, h),  # right
            wall.Wall(0, h, w, h),  # bottom
            # cube:
            wall.Wall(100, 75, 100, 150, (0, 255, 255)),
            wall.Wall(100, 150, 175, 150, (0, 0, 255)),
            wall.Wall(175, 150, 175, 75, (255, 0, 255)),
            wall.Wall(175, 75, 100, 75, (255, 255, 0)),
            # triangle:
            wall.Wall(200, 250, 250, 350, (255, 128, 0)),
            wall.Wall(250, 350, 150, 350, (0, 255, 128)),
            wall.Wall(150, 350, 200, 250, (0, 128, 255)),
            # spiral:
            wall.Wall(300, 50, 375, 50, (128, 0, 128)),
            wall.Wall(375, 50, 375, 190, (255, 128, 255)),
            wall.Wall(300, 50, 300, 125, (128, 255, 255)),
            wall.Wall(300, 125, 340, 125, (128, 0, 255)),
            wall.Wall(340, 125, 340, 80, (0, 255, 128)),
            wall.Wall(375, 190, 300, 190, (128, 128, 255))
        ]

    def run(self):
        clock = pg.time.Clock()
        while True:
            dt = clock.tick(60) / 1000
            self.handle_input(dt)
            self.raycaster.update(dt, self.walls)
            self.top_view.fill(self.background_color)
            self.raycaster.draw_top_view(self.top_view)
            for w in self.walls:
                w.draw(self.top_view)
            self.main_surface.blit(self.top_view, (0, 0))
            self.front_view.fill(self.background_color)
            self.raycaster.draw_front_view(self.front_view, self.height, self.half_height)
            self.main_surface.blit(self.front_view, (self.half_width, 0))
            pg.display.update()

    def handle_input(self, dt):
        events = pg.event.get()
        pressed = pg.key.get_pressed()
        for event in events:
            if (event.type == pg.QUIT or
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Quit immediately without letting the current loop iteration
                # run to completion.
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                pprint(self.raycaster.hits)
        self.raycaster.handle_input(events, pressed, dt)


App().run()
