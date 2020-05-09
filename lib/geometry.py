from quat import *
from camera import *

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

class Material():
    def __init__(self, emittance, reflectivity):
        self.emittance = emittance
        self.reflectivity = reflectivity