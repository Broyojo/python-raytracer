from ray.quat import *
from ray.scene import *
from random import uniform, randint

camera = Camera(
    position=Quat(0, 0, 0, 0),
    direction=euler(0, 0, 0),
    canvas_width=500,
    canvas_height=500,
    t_min=0.001,
    t_max=1e37,
    distance=1,
    fov=60
)

scene = Scene(
    camera=camera,
    objects=[
        Sphere(
            center=Quat(0, 0, -5001, 0),
            radius=5000,
            color=Quat(0, 255, 255, 0),
            specular=100
        ),
        Sphere(
            center=Quat(0, 0, -1, 3), 
            radius=1, 
            color=Quat(0, 255, 0, 0), 
            specular=500
        ),
        Sphere(
            center=Quat(0, 2, 0, 4), 
            radius=1, 
            color=Quat(0, 0, 0, 255),
            specular=100
        ),
        Sphere(
            center=Quat(0, -2, 0, 4), 
            radius=1, 
            color=Quat(0, 0, 255, 0),
            specular=10
        )
    ],
    lights=[
        AmbientLight(intensity=0.2),
        PointLight(intensity=0.6, position=Quat(0, 2, 1, 0)),
        DirectionalLight(intensity=0.2,  direction=Quat(0, 1, 4, 4))
    ],
    background_color=Quat(0, 135, 206, 235),
    max_depth=1
)

def update():
    pass
    #scene.objects[1].center.z += 0.1
    #scene.objects[1].center.y += 0.1

    
scene.render(update, file_name='images/balls.png', n_frames=1000)
