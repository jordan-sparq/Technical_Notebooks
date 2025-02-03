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

class SamplingUncertainty(Scene):

    def construct(self):
        # Construct axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.2],  # Adjusted range for normal distribution
            x_length=10,
            axis_config={"color": WHITE},
            tips=False,
        )

        labels = axes.get_axis_labels(
            x_label=Tex(r"Price"), y_label=Tex(r"Revenue")
        )
        labels[0].shift(DOWN * 0.8 + LEFT * 5.7)  # Adjust 0.3 based on your preference
        labels[1].shift(DOWN * 3 + LEFT * 1.6)
        labels[1].rotate(0.5*3.14)
        self.add(labels)

        # Define the Normal Distribution
        def normal_dist(x, mu=5, sigma=1.5):
            return np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi)) * 3

        # Define the confidence interval (e.g., ± 0.1 around the normal)
        def upper_bound(x):
            return min(1, normal_dist(x) + 0.1)  # Cap at 1

        def lower_bound(x):
            return max(0, normal_dist(x) - 0.1)  # Cap at 0

        # Generate x values for sampling
        x_vals = np.linspace(0, 10, 100)
        y_upper = [upper_bound(x) for x in x_vals]
        y_lower = [lower_bound(x) for x in x_vals]

        # Create the confidence band as a filled region
        confidence_region = VMobject()
        confidence_region.set_fill(GREY, opacity=0.3)
        confidence_region.set_stroke(width=0)

        # Function to update the confidence region shape
        def update_region(mob):
            points = [axes.c2p(x, y) for x, y in zip(x_vals, y_upper)]
            points += [axes.c2p(x, y) for x, y in zip(reversed(x_vals), reversed(y_lower))]
            mob.set_points_as_corners(points)

        confidence_region.add_updater(update_region)

        # Normal Distribution curve
        normal_curve = axes.plot(lambda x: normal_dist(x), color=BLUE)

        # Add elements
        self.add(axes)

        # Animate both the confidence interval and the curve
        self.add(confidence_region)
        self.play(Create(normal_curve), run_time=2)

        # self.wait()

        # Add a point
        action_1 = Dot(point=axes.c2p(5, normal_dist(5)), radius=0.2, color=RED)
        self.play(FadeIn(action_1), run_time=3)

        # # Remove the normal curve
        # self.play(FadeOut(normal_curve), run_time=3)

        l1= DashedLine(axes.c2p(5, 0), axes.c2p(5, normal_dist(5)))
        self.add(l1)

        self.wait()

        self.play(FadeOut(l1, action_1, normal_curve), run_time=3)

        self.wait()

        normal_curve = axes.plot(lambda x: normal_dist(x-0.3), color=BLUE)
        self.play(Create(normal_curve), run_time=2)
        action_2 = Dot(point=axes.c2p(5+0.3, normal_dist(5+0.3)), radius=0.2, color=RED)
        self.play(FadeIn(action_2), run_time=3)
        l2= DashedLine(axes.c2p(5+0.3, 0), axes.c2p(5+0.3, normal_dist(5+0.3)))
        self.add(l2)

        self.wait()

        self.play(FadeOut(l2, action_2, normal_curve), run_time=3)

        self.wait()

        normal_curve = axes.plot(lambda x: normal_dist(x+0.3), color=BLUE)
        self.play(Create(normal_curve), run_time=2)
        action_2 = Dot(point=axes.c2p(5-0.3, normal_dist(5-0.3)), radius=0.2, color=RED)
        self.play(FadeIn(action_2), run_time=3)
        l2= DashedLine(axes.c2p(5-0.3, 0), axes.c2p(5-0.3, normal_dist(5-0.3)))
        self.add(l2)

        self.wait()
