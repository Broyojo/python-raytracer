from ray.quat import *
from ray.scene import *

camera = Camera(
    position=Quat(0, 0, 0, 0),
    direction=euler(0, 0, 0),
    canvas_width=4000,
    canvas_height=4000,
    distance=1,
    fov=50
)

scene = Scene(
    camera=camera,
    objects=[
        Sphere(
            center=Quat(0, 0, -5001, 0),
            radius=5000,
            color=Quat(0, 255, 255, 0),
            specular=1000
        ),
        Sphere(
            center=Quat(0, 0, -1, 3), 
            radius=1, 
            color=Quat(0, 255, 0, 0), 
            specular= 500
        ),
        Sphere(
            center=Quat(0, 2, 0, 4), 
            radius=1, 
            color=Quat(0, 0, 0, 255),
            specular=1000
        ),
        Sphere(
            center=Quat(0, -2, 0, 4), 
            radius=1, 
            color=Quat(0, 0, 255, 0),
            specular=500
        )
    ],
    lights=[
      PointLight(intensity=0.9, position=Quat(0, 0, 0, 10)), 
      AmbientLight(intensity=0.1)
    ],
    background_color=Quat(0, 0, 0, 0),
    t_min=1,
    t_max=1e37,
    max_depth=1
)


def update():
    pass
    #scene.lights[0].position.z += 0.1



scene.render(update, file_name='images/balls.png', n_frames=1)
