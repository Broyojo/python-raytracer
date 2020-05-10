from ray.quat import *
from ray.geometry import *
from math import tan, pi

class Camera():
    def __init__(self, position, direction, canvas_width, canvas_height, distance, fov, t_min, t_max):
        self.position = position
        self.direction = direction.norm()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.t_min = t_min
        self.t_max = t_max
        self.distance = distance
        self.aspect_ratio = canvas_width/canvas_height
        self.fov = fov
        self.viewport_width = tan(self.fov * pi / 180)
        self.viewport_height = self.viewport_width * self.aspect_ratio

    def rotate(self, q):
        self.direction *= q
        self.direction = self.direction.norm()

    def translate_coords(self, x, y):
        # normalize x and y to be negative and positive
        x -= self.canvas_width / 2
        y -= self.canvas_height / 2

        vx = x * (self.viewport_width / self.canvas_width)
        vy = y * (self.viewport_height / self.canvas_height)

        return Quat(0, vx, vy, self.distance)

