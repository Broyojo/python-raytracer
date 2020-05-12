from ray.quat import *
from ray.scene import *

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def calculate_point(self, t): return self.origin + self.direction * t

class AmbientLight():
    def __init__(self, intensity):
        self.intensity = intensity

class PointLight():
    def __init__(self, intensity, position):
        self.intensity = intensity
        self.position = position

class DirectionalLight():
    def __init__(self, intensity, direction):
        self.intensity = intensity
        self.direction = direction

class Material():
    def __init__(self, color, reflectivity):
        self.color = color
        self.reflectivity = reflectivity

class Sphere():
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
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
        else: return -1, -1

    def get_normal(self, pos): return (pos - self.center).norm()