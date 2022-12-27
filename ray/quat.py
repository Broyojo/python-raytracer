from math import cos, sin


class Quat:
    def __init__(self, w, x, y, z):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, q):
        return Quat(self.w + q.w, self.x + q.x, self.y + q.y, self.z + q.z)

    def __sub__(self, q):
        return Quat(self.w - q.w, self.x - q.x, self.y - q.y, self.z - q.z)

    def __mul__(self, q):
        if type(q) == Quat:
            return Quat(
                -self.x * q.x - self.y * q.y - self.z * q.z + self.w * q.w,
                self.x * q.w + self.y * q.z - self.z * q.y + self.w * q.x,
                -self.x * q.z + self.y * q.w + self.z * q.x + self.w * q.y,
                self.x * q.y - self.y * q.x + self.z * q.w + self.w * q.z,
            )
        else:
            return Quat(self.w * q, self.x * q, self.y * q, self.z * q)

    def __str__(self):
        i_sign = " + " if self.x >= 0 else " "
        j_sign = " + " if self.y >= 0 else " "
        k_sign = " + " if self.z >= 0 else " "
        return f"{self.w}{i_sign}{self.x}i{j_sign}{self.y}j{k_sign}{self.z}k"

    def __getitem__(self, key):
        list = [self.w, self.x, self.y, self.z]
        return list[key]

    def conjugate(self):
        return Quat(self.w, -self.x, -self.y, -self.z)

    def dot(self, q):
        return self.w * q.w + self.x * q.x + self.y * q.y + self.z * q.z

    def __abs__(self):
        return (self.w**2 + self.x**2 + self.y**2 + self.z**2) ** 0.5

    def norm(self):
        m = self.__abs__()
        return Quat(self.w / m, self.x / m, self.y / m, self.z / m)


def euler(pitch, roll, yaw):
    w = cos(roll / 2) * cos(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)
    x = sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) - cos(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)
    y = cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * cos(
        pitch / 2
    ) * sin(yaw / 2)
    z = cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) - sin(roll / 2) * sin(
        pitch / 2
    ) * cos(yaw / 2)
    return Quat(w, x, y, z)
