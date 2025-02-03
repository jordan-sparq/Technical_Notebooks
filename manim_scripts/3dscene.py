from manim import *
import numpy as np
import random
### how to run
# manim -pql filename.py ClassName
### config values changed like this
config.pixel_height = 2160  # Full HD height
config.pixel_width = 3840   # Full HD width
config.frame_height = 8.0
config.frame_width = 14.0
config.background_color = "#121D3D"

class ThreeDeeScene(ThreeDScene):
    def construct(self):

        surface = Surface(
            lambda u, v: np.array([
                u, 
                v, 
                np.sin(u) * np.cos(v)
            ]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(15, 15),
            fill_color=BLUE
        )

        # Add the surface to the scene
        self.add(surface)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        self.add(ThreeDAxes())
        self.wait()
        self.play(phi.animate.set_value(50*DEGREES), run_time=3)
        self.play(theta.animate.set_value(50*DEGREES), run_time=3)
        self.play(theta.animate.set_value(-1*50*DEGREES), run_time=3)
        self.wait()