import numpy as np
from PIL import Image
from time import sleep
from ray.camera import *
from ray.geometry import *
from ray.quat import *
from math import inf
from random import random

class Scene():
    def __init__(self, camera, objects, lights, background_color):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.background_color = background_color
        self.image = np.zeros((self.camera.canvas_width, self.camera.canvas_height, 3), dtype=np.uint8)

    def ray_trace(self, ray, depth):
        closest_object, closest_t = self.calculate_intersection(ray)
        if closest_object != 0:
            intersect = ray.calculate_point(closest_t)
            normal = closest_object.get_normal(intersect)
            direction = ray.direction.conjugate()
            color = closest_object.material.color * self.shade(intersect, normal, direction)
            reflectivity = closest_object.material.reflectivity
            if depth > 0 and reflectivity > 0:
                reflection_direction = self.reflect(direction, normal)
                reflection_color = self.ray_trace(Ray(intersect, reflection_direction), depth-1)
                return color * (1 - reflectivity) + reflection_color * reflectivity
            else: return color 
        else: return self.background_color
    
    def calculate_intersection(self, ray):
        closest_t = self.camera.t_max + 1
        closest_object = 0
        for object in self.objects:
            t0, t1 = object.get_t(ray)
            if self.constrain(t0, closest_t): closest_t, closest_object = t0, object
            if self.constrain(t1, closest_t): closest_t, closest_object = t1, object
        return closest_object, closest_t
    
    def constrain(self, t, closest_t): return self.camera.t_min <= t <= self.camera.t_max and t < closest_t

    def shade(self, point, normal, vector):
        intensity = 0
        for light in self.lights:
            t = type(light)
            if t == AmbientLight: intensity += light.intensity
            else:
                if t == PointLight: direction = light.position - point
                else: direction = light.direction
                object, _ = self.calculate_intersection(Ray(point, direction))
                if object != 0: return intensity
                nd = normal.dot(direction)
                if nd > 0: intensity += light.intensity * nd / (abs(normal) * abs(direction))
        return intensity

    def reflect(self, direction, normal): return normal * 2 * normal.dot(direction) - direction

    def render(self, update, file_name, n_frames, depth):
        count = 0
        while count < n_frames:
            for x in range(self.camera.canvas_width):
                for y in range(self.camera.canvas_height):
                    origin = self.camera.direction * self.camera.translate_coords(x, y)
                    color = self.ray_trace(Ray(origin, (origin - self.camera.position).norm()), depth)
                    self.image[x, y] = [color.x, color.y, color.z]
            img = Image.fromarray(self.image, 'RGB')
            img = img.rotate(90)
            img.save(file_name + '-' + str(count) + '.png')
            update()
            count += 1
