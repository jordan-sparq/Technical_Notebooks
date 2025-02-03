from manim import *
import numpy as np
import random

config.pixel_height = 1080  # Full HD height
config.pixel_width = 1920  # Full HD width
config.frame_height = 8.0
config.frame_width = 14.0
np.random.seed(42)
random.seed(42)
config.background_color = "#121D3D"

class AirlineSeatingCustom(Scene):

    def construct(self):
    
        # Seating layout definition
        seating_layout = np.array([
            ["1A", "1B", "1C", "", "1D", "1E", "1F"],  # Row 1
            ["2A", "2B", "2C", "", "2D", "2E", "2F"],  # Row 2
            ["3A", "3B", "3C", "", "3D", "3E", "3F"],  # Row 3
            ["4A", "4B", "4C", "", "4D", "4E", "4F"],  # Row 4
            ["5A", "5B", "5C", "", "5D", "5E", "5F"],  # Row 5
            ["", "", "", "", "", "", ""],  # Aisle (empty space)
            ["6A", "6B", "6C", "", "6D", "6E", "6F"],  # Row 6
            ["7A", "7B", "7C", "", "7D", "7E", "7F"],  # Row 7
            ["8A", "8B", "8C", "", "8D", "8E", "8F"],  # Row 8
        ])
        seating_layout_ = np.array([
            ["1A", "1B", "1C", "1D", "1E", "1F"],  # Row 1
            ["2A", "2B", "2C", "2D", "2E", "2F"],  # Row 2
            ["3A", "3B", "3C",  "3D", "3E", "3F"],  # Row 3
            ["4A", "4B", "4C",  "4D", "4E", "4F"],  # Row 4
            ["5A", "5B", "5C", "5D", "5E", "5F"],  # Row 5
            ["6A", "6B", "6C",  "6D", "6E", "6F"],  # Row 6[
            ["7A", "7B", "7C", "7D", "7E", "7F"],  # Row 7
            ["8A", "8B", "8C","8D", "8E", "8F"],  # Row 8
        ])
        # Pricing scheme with front 4 rows being more expensive, and row 1 being the highest
        seat_prices = {
            "1A": 300, "1B": 300, "1C": 300, "1D": 300, "1E": 300, "1F": 300,  # Front row
            "2A": 250, "2B": 250, "2C": 250, "2D": 250, "2E": 250, "2F": 250,  # Row 2
            "3A": 220, "3B": 220, "3C": 220, "3D": 220, "3E": 220, "3F": 220,  # Row 3
            "4A": 200, "4B": 200, "4C": 200, "4D": 200, "4E": 200, "4F": 200,  # Row 4
            "5A": 150, "5B": 150, "5C": 150, "5D": 150, "5E": 150, "5F": 150,  # Row 5
            "6A": 130, "6B": 130, "6C": 130, "6D": 130, "6E": 130, "6F": 130,  # Row 6
            "7A": 120, "7B": 120, "7C": 120, "7D": 120, "7E": 120, "7F": 120,  # Row 7
            "8A": 100, "8B": 100, "8C": 100, "8D": 100, "8E": 100, "8F": 100   # Row 8
        }

        seat_size = 0.5  # Size of each seat square
        spacing = 0.6  # Spacing between seats
        seats = VGroup()  # Create a group to hold all seats and labels
        seat_squares = []  # List to store references to the seat squares

        # Function to determine color based on price
        def get_seat_color(price):
            min_price = 0
            max_price =300
            # Normalize the price to a color gradient (blue for low, red for high)
            color_value = interpolate_color(BLUE, RED, (price - min_price) / (max_price - min_price))
            return color_value

        # Generate seating grid
        for i, row in enumerate(seating_layout):
            for j, seat in enumerate(row):
                if seat:  # Only add seats, ignore empty spaces (aisles)
                    # Get the price for the current seat
                    price = seat_prices.get(seat, 150)  # Default to a middle-range price if not specified
                    
                    # Create a seat square with color based on price
                    seat_color = get_seat_color(price)
                    seat_square = Square(
                        seat_size, 
                        color=seat_color, 
                        fill_opacity=1, 
                        # stroke_color=WHITE,  # Edge color
                        # stroke_width=4        # Edge thickness
                    )
                    seat_square.move_to(
                        np.array([(j - len(row) / 2) * spacing, (-i) * spacing, 0])
                    )
                    seats.add(seat_square)  # Add seat square to the group
                    seat_squares.append(seat_square)  # Keep track of the seat square

                    # Add seat label
                    label = Text(seat, font_size=14).move_to(seat_square.get_center())
                    seats.add(label)  # Add label to the group

        # Move the entire grid up
        seats.shift(UP * 2.5)  # Adjust the value to move the grid higher or lower
        self.add(seats)  # Add the group to the scene

        # Add the legend
        def create_upward_arrow():
            arrow = Arrow(start=DOWN*2, end=UP, color=RED, stroke_width=4, tip_length=0.2)

            # Apply a vertical gradient fill (red at the bottom, blue at the top)
            arrow.set_fill(RED, opacity=0.6)

            # Position the arrow at the side of the seating grid
            arrow.move_to(RIGHT * 3 + UP)
            self.add(arrow)
            line = Line(start=DOWN, end=UP*0.5, color=BLUE, stroke_width=4)
            line.move_to(RIGHT * 3)
            line.set_fill(BLUE, opacity=0.6)
            text = Text("Price", font_size=30, color=WHITE)
            text.move_to(RIGHT*3.3 + UP*0.8)
            text.rotate(1.5*3.14)
            self.add(line)
            self.add(text)
        create_upward_arrow()

        # Select seat to sell
        def weighted_random_selection(grid_layout, already_sold):
            sold = False
            while not sold:
                n = len(grid_layout)  # Number of rows
                m = len(grid_layout[0]) if n > 0 else 0  # Number of columns

                weights = np.arange(1, n + 1)  # Higher weights for lower-index rows
                weights = weights / weights.sum()  # Normalize the weights

                row = np.random.choice(n, p=weights)  # Row index selection based on the weights
                column = random.randint(0, m - 1)  # Randomly select a column

                # Check if the seat is available (not sold and not an empty space)
                if ((row, column) not in already_sold) and (grid_layout[row][column] != ""):
                    sold = True

            return row, column

        # Sell seat and update row prices and seat colors
        def sell_seat(row, col, wait_time):
            seat_label = seating_layout_[row][col]
            print(f"Selling {seat_label}")
            seat_square = seat_squares[row * len(seating_layout_[0]) + col]
            
            # Change stroke color to red when sold
            self.play(seat_square.animate.set_stroke(color=WHITE), run_time=0.5)
            self.wait(wait_time)

                        # Update prices for all seats in the row and update colors
            for col_idx in range(len(seating_layout_[0])):
                seat_in_row = seating_layout_[row][col_idx]
                if seat_in_row:  # Only update if the seat exists
                    # Increase price by £10
                    seat_prices[seat_in_row] -= 50
                    # Update the color based on the new price
                    new_color = get_seat_color(seat_prices[seat_in_row])
                    seat_square = seat_squares[row * len(seating_layout_[0]) + col_idx]
                    seat_square.set_fill(new_color)

        already_sold = []
        for i in range(20):
            row, col = weighted_random_selection(seating_layout_, already_sold)
            sell_seat(row, col, wait_time=0.5)
            already_sold.append((row, col))
