from ray.quat import *
from ray.scene import *
from random import uniform, randint
import time

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
            center=Quat(0, 0, -1, 3), 
            radius=1, 
            material=Material(color=Quat(0, 255, 0, 0), reflectivity=0.3)
        ),
        Sphere(
            center=Quat(0, 2, 0, 4), 
            radius=1, 
            material=Material(color=Quat(0, 0, 0, 255), reflectivity=0.4)
        ),
        Sphere(
            center=Quat(0, -2, 0, 4), 
            radius=1, 
            material=Material(color=Quat(0, 0, 255, 0), reflectivity=0.2)
        ),
        Sphere(
            center=Quat(0, 0, -5001, 0),
            radius=5000,
            material=Material(color=Quat(0, 255, 255, 0), reflectivity=0.5)
        )
    ],
    lights=[
        AmbientLight(intensity=0.2),
        PointLight(intensity=0.6, position=Quat(0, 2, 1, 0)),
        DirectionalLight(intensity=0.2,  direction=Quat(0, 1, 4, 4))
    ],
    background_color=Quat(0, 0, 0, 0),
)



def update():
    scene.objects[1].center.z += 0.01
    print('done rendering frame')

t = time.time()  
scene.render(update, file_name='images/video1/balls', n_frames=1, depth=10)
print(time.time() - t, "seconds")