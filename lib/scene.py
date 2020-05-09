import numpy as np
from PIL import Image
from time import sleep
from quat import *
from camera import *
from geometry import *
from 



class Scene():
    def __init__(self, camera, objects, background_color, t_min, t_max, max_depth):
        self.objects = objects
        self.camera = camera
        self.background_color = background_color
        self.t_min = t_min
        self.t_max = t_max
        self.max_depth = max_depth
        self.image = np.zeros(
            (self.camera.canvas_height, self.camera.canvas_width, 3), dtype=np.uint8)


    def ray_trace(self, ray):
        closest_t = self.t_max+1
        closest_object = 0
        for object in self.objects:
            t0, t1 = object.get_t(ray)

            if self.t_min <= t0 <= self.t_max and closest_t > t0:
                closest_t = t0
                closest_object = object
            
            if self.t_min <= t1 <= self.t_max and closest_t > t1:
                closest_t = t0
                closest_object = object
        return closest_object.color if closest_object != 0 else self.background_color

    def render(self, update, n_samples, file_name):
        for x in range(self.camera.canvas_width):
            for y in range(self.camera.canvas_height):
                for i in range(n_samples):
                    origin = self.camera.direction * self.camera.translate_coords(x, y)
                    direction = (origin - self.camera.position).norm()
                    color = self.ray_trace(Ray(origin, direction))
                    self.image[x, y] = color
        img = Image.fromarray(self.image, 'RGB')
        img = img.rotate(90)  # because PIL is weird, this is needed
        img.save(file_name)
        update()
        sleep(0.01)
