import tkinter as tk
from drone import Drone


def create_grid(root, goal_x = None, goal_y = None, rows = 10, cols = 10, drone_positions=None):
    cell_size = 25  # size of each cell in pixels

    # space for axis labels
    left_margin = 40
    bottom_margin = 30

    canvas = tk.Canvas(
        root,
        width= cols * cell_size + left_margin,
        height= rows * cell_size + bottom_margin,
        bg= "white"
    )
    canvas.pack()

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x1 = left_margin + col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size

            canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="black",
                fill="white"
            )

    # label the x-axis
    for x in range(cols):
        center_x = left_margin + x * cell_size + cell_size / 2
        center_y = rows * cell_size + 15
        canvas.create_text(center_x, center_y, text=str(x), font=("Arial", 10), fill="black")

    # Label the y-axis
    for y in range(rows):
        center_x = left_margin / 2
        center_y = (rows - 1 - y) * cell_size + cell_size / 2

        canvas.create_text(center_x, center_y, text=str(y), font=("Arial", 10), fill="black")

    # Default to one drone at (0, 0)
    if drone_positions is None:
        drone_positions = [(0, 0)]
    
    drone_ids = []
    drone_colors = ["blue", "purple", "orange", "green"]  # Different colors for different drones

    # Draw each drone
    for i, (start_x, start_y) in enumerate(drone_positions):
        drone_object = Drone(start_x, start_y, rows, cols)
        center_x = left_margin + drone_object.x * cell_size + cell_size / 2
        center_y = (rows - 1 - drone_object.y) * cell_size + cell_size / 2
        radius = 6

        color = drone_colors[i % len(drone_colors)]
        drone_id = canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=color
        )
        drone_ids.append(drone_id)
    
    # Draw the goal if provided
    if goal_x is not None and goal_y is not None:
        goal_center_x = left_margin + goal_x * cell_size + cell_size / 2
        goal_center_y = (rows - 1 - goal_y) * cell_size + cell_size / 2
        goal_radius = 7

        canvas.create_oval(
            goal_center_x - goal_radius, goal_center_y - goal_radius,
            goal_center_x + goal_radius, goal_center_y + goal_radius,
            fill="red"
        )
    
    return canvas, drone_ids