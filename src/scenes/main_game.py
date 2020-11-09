import pygame

from src.constants import *
from src.resources import controls, worlds
from src.scenes.scene import Scene, DevOverlay
from src import raycaster


class MainGame(Scene):
    def __init__(self, scene_manager, world_name):
        self.world = worlds[world_name]
        self.world_name = world_name
        self.raycaster = raycaster.RayCaster(self.world)
        super().__init__(scene_manager, MainGameDevOverlay)
        self.line_tops = []
        self.line_bottoms = []
        self.line_colors = []
        self.move_straight_sign = 0  # 1 is forward, -1 is backward
        self.rotate_sign = 0  # 1 is right, -1 is left
        self.move_sideways_sign = 0  #
        self.mouse_motion_x = 0  # positive sign is right, negative is left
        self.is_paused = False

    def start(self):
        super().start()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
            elif event.key == controls[MOVE_FORWARD]:
                self.move_straight_sign = 1
            elif event.key == controls[MOVE_BACKWARD]:
                self.move_straight_sign = -1
            elif event.key == controls[MOVE_LEFT]:
                self.move_sideways_sign = -1
            elif event.key == controls[MOVE_RIGHT]:
                self.move_sideways_sign = 1
            elif event.key == controls[ROTATE_LEFT]:
                self.rotate_sign = -1
            elif event.key == controls[ROTATE_RIGHT]:
                self.rotate_sign = 1
            elif event.key == controls[PAUSE]:
                self.is_paused = not self.is_paused
                pygame.mouse.set_visible(self.is_paused)
                pygame.event.set_grab(not self.is_paused)
        elif event.type == pygame.KEYUP:
            if event.key in (controls[MOVE_FORWARD], controls[MOVE_BACKWARD]):
                self.move_straight_sign = 0
            elif event.key in (controls[ROTATE_LEFT], controls[ROTATE_RIGHT]):
                self.rotate_sign = 0
            elif event.key in (controls[MOVE_LEFT], controls[MOVE_RIGHT]):
                self.move_sideways_sign = 0
        elif event.type == pygame.MOUSEMOTION:
            # This needs to be "+=" because more than one mousemotion event
            # per frame can happen. That was a nasty bug to track down because
            # the rotation rate was almost exactly half of what it is supposed
            # to be. This was caused by there being 2 mousemotion events
            # on average per frame.
            self.mouse_motion_x += event.rel[0]
        elif (event.type == pygame.ACTIVEEVENT
              and event.gain == 0 and event.state == 1):
            # The window loses focus.
            self.is_paused = True
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)

    def update(self, dt):
        if self.is_paused:
            self.mouse_motion_x = 0
            return
        if self.move_straight_sign != 0:
            self.raycaster.move_straight(self.move_straight_sign, dt)
        if self.move_sideways_sign != 0:
            self.raycaster.move_sideways(self.move_sideways_sign, dt)
        if self.rotate_sign != 0:
            self.raycaster.rotate_keyboard(self.rotate_sign, dt)
        if self.mouse_motion_x != 0:
            self.raycaster.rotate_mouse(self.mouse_motion_x)
            self.mouse_motion_x = 0
        self.line_tops, self.line_bottoms, self.line_colors = self.raycaster.cast()

    def draw(self):
        self.target_surface.fill(BACKGROUND_COLOR)
        for x in range(SMALL_DISPLAY_WIDTH):
            pygame.draw.line(
                self.target_surface,
                self.line_colors[x],
                (x, self.line_tops[x]),
                (x, self.line_bottoms[x])
            )


class MainGameDevOverlay(DevOverlay):
    def __init__(self, scene):
        super().__init__(scene)

        self.world_name_surf, self.world_name_rect = self.font.render(
            f"world name: {self.scene.world_name}"
        )
        self.world_name_rect.topleft = self.fps_rect.bottomleft

        self.pos_text = self.get_pos_text()
        self.pos_surf, self.pos_rect = self.font.render(self.pos_text)
        self.pos_rect.topleft = self.world_name_rect.bottomleft

        self.view_dir_text = self.get_view_dir_text()
        self.view_dir_surf, self.view_dir_rect = self.font.render(self.view_dir_text)
        self.view_dir_rect.topleft = self.pos_rect.bottomleft

    def update(self):
        super().update()
        new_pos_text = self.get_pos_text()
        if new_pos_text != self.pos_text:
            self.pos_text = new_pos_text
            self.pos_surf, self.pos_rect = self.font.render(self.pos_text)
            self.pos_rect.topleft = self.world_name_rect.bottomleft
        new_view_dir_text = self.get_view_dir_text()
        if new_view_dir_text != self.view_dir_text:
            self.view_dir_text = new_view_dir_text
            self.view_dir_surf, self.view_dir_rect = self.font.render(self.view_dir_text)
            self.view_dir_rect.topleft = self.pos_rect.bottomleft

    def draw(self):
        super().draw()
        self.target_surface.blit(self.world_name_surf, self.world_name_rect)
        self.target_surface.blit(self.pos_surf, self.pos_rect)
        self.target_surface.blit(self.view_dir_surf, self.view_dir_rect)

    def get_pos_text(self):
        return (
            f"position: "
            f"{self.scene.raycaster.position.x:.2f}, "
            f"{self.scene.raycaster.position.y:.2f}"
        )

    def get_view_dir_text(self):
        return (
            f"view direction: "
            f"{self.scene.raycaster.view_direction.x:.2f}, "
            f"{self.scene.raycaster.view_direction.y:.2f}"
        )
