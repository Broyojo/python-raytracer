import numpy as np
from PIL import Image
from time import sleep
from math import tan, pi, cos, sin
from quat import Quat, euler
from random import random

# camera class


class Camera():
    def __init__(self, position, direction, canvas_width, canvas_height, distance, fov):
        self.position = position
        self.direction = direction.norm()
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
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

# ray class


class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def calculate_point(self, t):
        return self.origin + t * self.direction

# sphere class


class Sphere():
    def __init__(self, center, radius, color, material):
        self.center = center
        self.radius = radius
        self.color = color
        self.material = material

    def get_t(self, ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius**2
        if (b**2) - (4 * a * c) > 0:
            t0 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
            t1 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
            return t0, t1
        else:
            return -1, -1

    def get_normal(self, pos):
        return (pos - self.center).norm()

# material class


class Material():
    def __init__(self, emittance, reflectivity):
        self.emittance = emittance
        self.reflectivity = reflectivity

# Main Scene class


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

    '''

    def ray_trace(self, ray, depth):
        if depth < self.max_depth: return self.background_color
        did_hit, closest_distance, ray, object = self.check_intersect(ray)
        if did_hit == False: return self.background_color
        closest_point = ray.calculate_point(closest_distance)
        material = object.material
        emittance = material.emittance
        point_normal = object.get_normal(closest_point)
        new_ray_direction = self.random_hemisphere_uv(point_normal)
        new_ray = Ray(closest_point, new_ray_direction)
        probability = 1 / (2 * pi)
        cos_theta = new_ray.direction.dot(point_normal)
        BRDF = material.reflectivity / pi
        reflected = self.ray_trace(new_ray, depth + 1)
        return emittance + (BRDF * reflected * cos_theta / probability)

    # this function is super complex and difficult to understand.

    def random_hemisphere_uv(self, n):
        if n.x > n.y:
            nt = Quat(0, n.z, 0 - n.x) / (n.x**2 + n.z**2)**0.5
        else:
            nt = Quat(0, 0, -n.z, n.y) / (n.y**2 + n.z**2)**0.5
        nb = n * nt

        r0, r1 = random(), random()
        sin_theta = (1-r0**2)
        phi = 2 * pi * r1
        x = sin_theta * cos(phi)
        z = sin_theta * sin(phi)
        sample = Quat(0, x, 0, z)

        tranform = Quat(
            0,
            nt.x, nt.y, nt.z,
            n.x, n.y, n.x,
            nb.x, nb.y, nb.z
        )

        return sample * tranform
    '''
    def check_intersect(self, ray):
        closest_t = self.t_max+1
        closest_object = 0
        for object in self.objects:
            t0, t1 = object.get_t(ray)

            

            closest_t, closest_object = self.check_restraints(t0, closest_t, closest_object)

            closest_t, closest_object = self.check_restraints(t1, closest_t, closest_object)


        return closest_object.color if closest_object != 0 else self.background_color
        '''
        if closest_object != 0:
            return True, closest_t, ray, closest_object
            print('yes')
        else:
            return False, False, False, False, False
        '''

    def check_restraints(self, t, closest_t, closest_object):
        return t, closest_object if self.t_min <= t <= self.t_max and closest_t > t else 
            return 

    def render(self, update, n_samples, file_name):
        for x in range(self.camera.canvas_width):
            for y in range(self.camera.canvas_height):
                for i in range(n_samples):
                    point = self.camera.direction * self.camera.translate_coords(x, y)
                    direction = (point - self.camera.position).norm()
                    color = self.check_intersect(Ray(point, direction))
                    #color = self.ray_trace(Ray(self.camera.position, direction), depth=0)
                    self.image[x, y] = color
        img = Image.fromarray(self.image, 'RGB')
        img = img.rotate(90)  # because PIL is weird, this is needed
        img.save(file_name)
        update()
