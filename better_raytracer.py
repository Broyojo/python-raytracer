from renderer import Scene, Camera, Sphere, Ray, Material
from quat import Quat, euler

camera = Camera(
    position=Quat(0, 0, 0, 0),
    direction=euler(0, 0, 0),
    canvas_width=100,
    canvas_height=100,
    distance=1,
    fov=60
)

scene = Scene(
    camera=camera,
    objects=[
        Sphere(
            center=Quat(0, 0, 0, 3), radius=1, color=[255, 0, 0], material=Material(reflectivity=1, emittance=1)
        )
    ],
    background_color=[0, 0, 0],
    t_min=1,
    t_max=1e37,
    max_depth=1
)


def update():
    pass
    #camera.rotate(euler(-0.01, 0, 0))


scene.render(update, n_samples=10, file_name='balls.png')
