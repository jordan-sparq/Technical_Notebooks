from manim import *
import numpy as np
import random

# Set configurations
config.pixel_height = 2160  # Full HD height
config.pixel_width = 3840   # Full HD width
config.frame_height = 8.0
config.frame_width = 14.0
np.random.seed(42)
random.seed(42)
config.background_color = "#121D3D"

class CabinBag(Scene):

    def construct(self):

        ###### BAG 1
        hollow_circle = Circle(stroke_width=5, color="#26afe9", radius=0.2)  # Adjust thickness with stroke_width
        
        # Create a square around the circle
        rectangle = Rectangle(height=0.6,width=1.2, color="#26afe9")
        rectangle.set_fill("#26afe9",opacity=1)

        # Position the shapes on the screen
        hollow_circle.move_to(ORIGIN + UP*0.3 + RIGHT)
        rectangle.move_to(ORIGIN + RIGHT)

        # Add both the square and hollow circle to the scene
        bag1 = VGroup(rectangle, hollow_circle) 
        bag1.shift(UP*2 + LEFT * 4)

        self.add(bag1)

        target1 = 1*LEFT
        target2 = 1*RIGHT

        ### bag 2
        hollow_circle2 = Circle(stroke_width=5, color="#92d449", radius=0.2)  # Adjust thickness with stroke_width
        
        # Create a square around the circle
        rectangle2 = Rectangle(height=0.8,width=1.6, color="#92d449")
        rectangle2.set_fill("#92d449",opacity=1)

        # Position the shapes on the screen
        hollow_circle2.move_to(ORIGIN + UP*0.3 + RIGHT)
        rectangle2.move_to(ORIGIN + RIGHT)

        # Add both the square and hollow circle to the scene
        bag2 = VGroup(rectangle2, hollow_circle2) 
        bag2.shift(UP*0.7 + LEFT * 4)

        self.add(bag2)
        target3 = 1*LEFT
        target4 = 1*RIGHT

        ## bag 3
        hollow_circle3 = Circle(stroke_width=5, color="#cf3e4c", radius=0.2)  # Adjust thickness with stroke_width
        
        # Create a square around the circle
        rectangle3 = Rectangle(height=1.2,width=2.4, color="#cf3e4c")
        rectangle3.set_fill("#cf3e4c",opacity=1)

        # Position the shapes on the screen
        hollow_circle3.move_to(ORIGIN + UP*0.5 + RIGHT)
        rectangle3.move_to(ORIGIN + RIGHT)

        # Add both the square and hollow circle to the scene
        bag3 = VGroup(rectangle3, hollow_circle3) 
        bag3.shift(DOWN*1 + LEFT * 4)

        self.add(bag3)
        target5 = 1.*LEFT
        target6 = 1.*RIGHT

        ## Graphing
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.2],  # Adjusted range for normal distribution
            x_length=4,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False,
        )

        labels = axes.get_axis_labels(
            x_label=Tex(r"Price Difference"), y_label=Tex(r"Revenue")
        )
        labels[0].shift(DOWN*0.2 +LEFT*1.8)  # Adjust 0.3 based on your preference
        labels[1].shift(DOWN * 1.7 + RIGHT * 0.5)
        labels[1].rotate(0.5*3.14)
        axes.shift(RIGHT*2 + UP*0.5)

        self.add(axes)
        self.add(labels)

        ### Plot normal distribution
        def normal_dist(x, mu=2.5, sigma=1.5):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi)) * 3
        normal_curve = axes.plot(lambda x: normal_dist(x), color=BLUE, x_range=[0,2.5])
        normal_curve2 = axes.plot(lambda x: normal_dist(x), color=BLUE, x_range=[2.5,5])

        #### ANIMATE
        self.play(
            bag1.animate.shift(target1),
            bag3.animate.shift(target6),
            Create(normal_curve),
            run_time=5
        )

        # Second play: Move bag1 and bag3 simultaneously to new positions for 5 seconds
        self.play(
            bag1.animate.shift(target2),
            bag3.animate.shift(target5),
            Create(normal_curve2),
            run_time=5
        )

        self.wait()