from random import random

import numpy as np

from ray.camera import *
from ray.geometry import *
from ray.quat import *


class Scene:
    def __init__(self, camera, objects, lights, background_color, max_depth):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.background_color = background_color
        self.max_depth = max_depth
        self.image = np.zeros(
            (self.camera.canvas_width, self.camera.canvas_height, 3), dtype=np.uint8
        )

    def ray_trace(self, ray):
        pass

    def get_intersection(self, ray):
        closest_t = self.camera.t_max + 1
        closest_object = 0
        for object in self.objects:
            t0, t1 = object.get_t(ray)

            if self.check_restrictions(t0, closest_t):
                closest_t = t0
                closest_object = object

            if self.check_restrictions(t1, closest_t):
                closest_t = t1
                closest_object = object

    def check_restrictions(self, t, closest_t):
        return self.camera.t_min <= t <= self.camera.t_max and t < closest_t

    def shade(self, ray):
        pass

    def random_vec(self):
        vector = Quat(0, 0, 0, 0)
        while len(vector) >= 1:
            vector = 2 * Quat(0, random(), random(), random()) - Quat(0, 1, 1, 1)
        return vector

    def render(self, update, file_name, n_frames):
        while n_frames > 0:
            n_frames -= 1
            for x in range(self.camera.canvas_width):
                for y in range(self.camera.canvas_height):
                    origin = self.camera.direction * self.camera.translate_coords(x, y)
                    color = self.ray_trace(
                        Ray(origin, (origin - self.camera.position).norm())
                    )

                    self.image[x, y] = [color.x, color.y, color.z]

            self.save_image(file_name)
            update()
