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

import top_view_scene
import front_view_scene
import ray


class App:
    def __init__(self):
        width = 800
        height = 400
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        self.main_surface = pg.display.set_mode((width, height))
        pg.mouse.set_visible(False)
        self.running = True
        scene_width = width // 2
        self.raycaster = ray.RayCaster(scene_width // 2, height // 2, 0)
        self.raycaster.make_new_rays(math.pi/2, scene_width)
        self.scenes = [
            top_view_scene.TopView(0, 0, scene_width, height, self.raycaster),
            front_view_scene.FrontView(scene_width, 0, scene_width, height, self.raycaster)
        ]

    def run(self):
        clock = pg.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000
            events, pressed = self.handle_input()
            self.raycaster.handle_input(events, pressed, dt)
            for scene in self.scenes:
                scene.handle_input(events, pressed, dt)
                scene.update(dt)
                scene.draw(self.main_surface)
            pg.display.update()

    def handle_input(self):
        events = pg.event.get()
        pressed = pg.key.get_pressed()
        for event in events:
            if (event.type == pg.QUIT or
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Quit immediately without letting the current loop iteration
                # run to completion.
                sys.exit()
        return events, pressed


App().run()