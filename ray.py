import math

import pygame as pg


class RayCaster:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading
        self.move_speed = 50  # px/s
        self.turn_speed = math.pi / 2  # rad/s
        self.rays = []
        self.hits = []  # stores the distances to the walls or None if a ray didn't hit a wall
        self.max_view_distance = 500
        self.color = (255, 196, 0)

    def make_new_rays(self, fov, n):
        self.hits = [None]*n
        self.rays = [None]*n
        # I want rays that when emitted onto an orthogonal wall make
        # intersection points that are equally spaced along that wall. For
        # this I need tan() to compute the angles. This reduces distortion.
        tan_max = math.tan(fov / 2)
        a = -tan_max
        b = tan_max
        step = (b - a) / (n - 1)
        for i in range(n):
            self.rays[i] = Ray(
                self.x, 
                self.y, 
                self.heading, 
                math.atan(a + step * i)
            )

    def handle_input(self, events, pressed, dt):
        if pressed[pg.K_w]:
            self.move(dt, 1, self.heading)
        if pressed[pg.K_s]:
            self.move(dt, -1, self.heading)
        if pressed[pg.K_e]:
            self.turn(dt, 1)
        if pressed[pg.K_q]:
            self.turn(dt, -1)
        if pressed[pg.K_a]:
            self.strafe(dt, -1)
        if pressed[pg.K_d]:
            self.strafe(dt, 1)

    def move(self, dt, sign, angle):
        # positive sign means forward, negative backward
        dx = math.cos(angle) * self.move_speed * dt * sign
        dy = math.sin(angle) * self.move_speed * dt * sign
        for r in self.rays:
            r.move(dx, dy)
        self.x += dx
        self.y += dy

    def turn(self, dt, sign):
        # positive sign means right, negative means left
        self.heading += self.turn_speed * dt * sign
        for r in self.rays:
            r.rotate(self.heading)

    def strafe(self, dt, sign):
        # move sideways in relation to the view
        # positive sign means right, negative means left
        angle = self.heading + (math.pi / 2 * sign)
        self.move(dt, 1, angle)

    def update(self, dt, walls):
        for i, r in enumerate(self.rays):
            self.hits[i] = r.cast(walls)

    def draw_top_view(self, target_surface):
        pg.draw.circle(target_surface, self.color, (int(self.x), int(self.y)), 3)
        for r in self.rays:
            r.draw(target_surface)

    def draw_front_view(self, target_surface, surface_height, surface_half_height):
        # TODO: Make the wall darker the farther away it is. There must be an
        #  easy way to manipulate the brightness in pygame apart from changing
        #  the rgb values. Maybe use pygame.Color.hsva
        # FIXME: Understand how to fix the distortion properly. Maybe look at
        #  the repo of thecodingtrain and see how the fans fixed it.
        #  The distances are still wrong.
        for i, hit in enumerate(self.hits):
            if hit is not None and hit[0] <= self.max_view_distance:
                dist, color = hit
                h = surface_height / dist * 30  # that right number maybe is the wall height?
                pg.draw.line(
                    target_surface,
                    color,
                    (i, surface_half_height - h / 2),
                    (i, surface_half_height + h / 2)
                )


class Ray:
    def __init__(self, x, y, heading, relative_angle):
        self.x1 = x
        self.y1 = y
        # relative_angle is the angle relative to the raycasters heading
        self.relative_angle = relative_angle
        angle = relative_angle + heading
        self.x2 = self.x1 + math.cos(angle)
        self.y2 = self.y1 + math.sin(angle)
        self.color = (255, 196, 0)
        self.wall_intersect = []

    def move(self, dist_x, dist_y):
        self.x1 += dist_x
        self.y1 += dist_y
        self.x2 += dist_x
        self.y2 += dist_y
        
    def rotate(self, new_heading):
        angle = new_heading + self.relative_angle
        self.x2 = self.x1 + math.cos(angle)
        self.y2 = self.y1 + math.sin(angle)

    def draw(self, target_surf):
        if self.wall_intersect:
            pg.draw.line(
                target_surf,
                self.color,
                (self.x1, self.y1),
                self.wall_intersect
            )

    def cast(self, walls):
        # Algorithm taken from https://www.youtube.com/watch?v=-6iIc6-Y-kk
        # which references https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        # I check t with 0 <= t <= 1 like it says in wikipedia,
        # however thecodingtrain only uses '<' in the video.
        # I don't believe it matters much.
        #
        # As far as I understand 'u' is the distance to the intersect in units
        # of ray length. So if the ray is 1 pixel long then a 'u' of 123 means
        # a distance of 123 pixels to the wall.
        self.wall_intersect = ()
        min_distance = math.inf
        nearest_wall_color = None
        for w in walls:
            denominator = ((w.x1 - w.x2) * (self.y1 - self.y2)
                           - (w.y1 - w.y2) * (self.x1 - self.x2))
            if denominator == 0:
                continue
            t = (((w.x1 - self.x1) * (self.y1 - self.y2)
                  - (w.y1 - self.y1) * (self.x1 - self.x2)) / denominator)
            u = -((w.x1 - w.x2) * (w.y1 - self.y1)
                  - (w.y1 - w.y2) * (w.x1 - self.x1)) / denominator
            if 0 <= t <= 1 and u > 0:
                # FIXME: Put the calculation of intersect inside the if block
                # because it is unnecessary if u >= min_distance.
                intersect_x = w.x1 + t * (w.x2 - w.x1)
                intersect_y = w.y1 + t * (w.y2 - w.y1)
                if u < min_distance:
                    min_distance = u
                    nearest_wall_color = w.color
                    self.wall_intersect = (intersect_x, intersect_y)
        if self.wall_intersect:
            dist = min_distance * math.cos(self.relative_angle)
            return dist, nearest_wall_color
