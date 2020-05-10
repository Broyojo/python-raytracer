from ray.quat import *

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def calculate_point(self, t):
        return self.origin + self.direction * t

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

class Sphere():
    def __init__(self, center, radius, color, specular):
        self.center = center
        self.radius = radius
        self.color = color
        self.specular = specular

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

class Plane():
    def __init__(self, point, normal, color):
        self.point = point
        self.normal = normal
        self.color = color
    
    def get_t(self, ray):
        denom = self.normal.dot(self.point)
        if denom > 1e-6:
            po = self.point - ray.origin
            t = po.dot(self.normal) / denom
            return t >= 0