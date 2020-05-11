import numpy as np
from PIL import Image
from time import sleep
from ray.camera import *
from ray.geometry import *
from ray.quat import *
from math import inf
from random import random


class Scene():
    def __init__(self, camera, objects, lights, background_color, max_depth):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.background_color = background_color
        self.max_depth = max_depth
        self.image = np.zeros((self.camera.canvas_width, self.camera.canvas_height, 3), dtype=np.uint8)

    def ray_trace(self, ray):
        closest_object, closest_t = self.calculate_intersection(ray)
        if closest_object != 0:
            intersect = ray.calculate_point(closest_t)
            return closest_object.color * self.shade(intersect, closest_object.get_normal(intersect), ray.direction.conjugate(), closest_object.specular)
        else:
            return self.background_color
    
    def calculate_intersection(self, ray):
        closest_t = self.camera.t_max + 1
        closest_object = 0
        for object in self.objects:
            if type(object) == Sphere:
                t0, t1 = object.get_t(ray)

                if self.camera.t_min <= t0 <= self.camera.t_max and t0 < closest_t:
                    closest_t = t0
                    closest_object = object
                
                if self.camera.t_min <= t1 <= self.camera.t_max and t1 < closest_t:
                    closest_t = t1
                    closest_object = object

            elif type(object) == Plane:
                closest_t = object.get_t(ray)
                closest_object = object

        return closest_object, closest_t

    def shade(self, point, normal, vector, specular):
        intensity = 0
        for light in self.lights:
            t = type(light)
            if t == AmbientLight:
                intensity += light.intensity
            else:
                if t == PointLight:
                    direction = light.position - point
                    self.camera.t_max = 1
                else:
                    direction = light.direction
                    self.camera.t_max = inf
                
                object, _ = self.calculate_intersection(Ray(point, direction))
                if object != 0:
                    continue
                
                nd = normal.dot(direction)
                if nd > 0:
                    intensity += light.intensity * nd / (abs(normal) * abs(direction))

                '''
                if specular != -1:
                    r = normal * 2 * normal.dot(direction) - direction
                    rv = r.dot(vector)
                    if rv > 0:
                        intensity += light.intensity * (rv / (abs(r) * abs(vector)))**specular
                '''
                 
        return intensity
    
    def to_color(self, q): return [q.x, q.y, q.z]

    def reflect(self, vector, normal):
        return vector - 2 * vector.normal * normal

    def save_image(self, file_name):
        img = Image.fromarray(self.image, 'RGB')
        img = img.rotate(90)  # because PIL is weird, this is needed
        img.save(file_name)

    def render(self, update, file_name, n_frames, n_samples):
        while n_frames > 0:
            n_frames -= 1
            for x in range(self.camera.canvas_width):
                for y in range(self.camera.canvas_height):
                    origin = self.camera.direction * self.camera.translate_coords(x, y)
                    color = self.ray_trace(Ray(origin, (origin - self.camera.position).norm()))

                    self.image[x, y] = self.to_color(color)

            self.save_image(file_name)
            update()
