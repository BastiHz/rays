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
import pygame as pg

import top_view_scene


class App:
    def __init__(self):
        width = 800
        height = 600
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.main_surface = pg.display.set_mode((width, height))
        pg.mouse.set_visible(False)
        self.running = True
        self.scene = top_view_scene.TopView(self)

    def run(self):
        clock = pg.time.Clock()
        while self.running:
            clock.tick(60)
            self.handle_input()
            self.scene.update()
            self.scene.draw(self.main_surface)
            pg.display.update()

    def handle_input(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT or
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Quit immediately without letting the current loop iteration
                # run to completion.
                sys.exit()
            else:
                self.scene.handle_input(event)


App().run()