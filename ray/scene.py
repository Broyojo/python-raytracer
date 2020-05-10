import numpy as np
from PIL import Image
from time import sleep
from ray.camera import *
from ray.geometry import *
from ray.quat import *


class Scene():
    def __init__(self, camera, objects, lights, background_color, t_min, t_max, max_depth):
        self.objects = objects
        self.lights = lights
        self.camera = camera
        self.background_color = background_color
        self.t_min = t_min
        self.t_max = t_max
        self.max_depth = max_depth
        self.image = np.zeros(  
            (self.camera.canvas_width, self.camera.canvas_height, 3), dtype=np.uint8)

    def ray_trace(self, ray):
        closest_t = self.t_max+1
        closest_object = 0
        for object in self.objects:
            if type(object) == Sphere:
                t0, t1 = object.get_t(ray)

                if self.t_min <= t0 <= self.t_max and closest_t > t0:
                    closest_t = t0
                    closest_object = object
                
                if self.t_min <= t1 <= self.t_max and closest_t > t1:
                    closest_t = t0
                    closest_object = object

            elif type(object) == Plane:
                t = object.get_t(ray)
                closest_t = t
                closest_object = object

        intersect = ray.calculate_point(closest_t)

        if closest_object != 0:
            return closest_object.color * self.shade(intersect, closest_object.get_normal(intersect), ray.direction * -1, closest_object.specular)
        else:
            return self.background_color
    
    def shade(self, point, normal, vector, specular):
        amount = 0
        distance = 0
        for light in self.lights:
            t = type(light)
            if t == AmbientLight:
                amount += light.intensity
            else:
                if t == PointLight:
                    distance = light.position - point     
                else:
                    distance = light.direction   
                nd = normal.dot(distance)
                if nd > 0:
                    amount += light.intensity * nd / (normal.magnitude() * distance.magnitude())
                if specular != -1:
                    reflection = normal * 2 * normal.dot(distance) - distance
                    rv = reflection.dot(vector)
                    if rv > 0:
                        amount += light.intensity*(rv / (reflection.magnitude() * vector.magnitude()))**specular

        return amount
    
    def to_color(self, q):
        return [q.x, q.y, q.z]

    
    def save_image(self, file_name):
        img = Image.fromarray(self.image, 'RGB')
        img = img.rotate(90)  # because PIL is weird, this is needed
        img.save(file_name)

    def render(self, update, file_name, n_frames):
        while n_frames > 0:
            n_frames -= 1
            for x in range(self.camera.canvas_width):
                for y in range(self.camera.canvas_height):
                    origin = self.camera.direction * self.camera.translate_coords(x, y)
                    direction = (origin - self.camera.position).norm()
                    color = self.ray_trace(Ray(origin, direction))
                    self.image[x, y] = self.to_color(color)
            self.save_image(file_name)
            update()
