import tkinter as tk
import random
import time
from grid import create_grid
from search_algorithms import lawnmower_path, spiral_path_inwards, spiral_path_from_point, shortest_path, region_search_path

# Default grid size
rows = 10
cols = 10
# Default speed (milliseconds between moves)
speed = 200 
# Drone starting point var
start_x = 0
start_y = 0
# Simulation data variables
grid_size = (rows, cols)
target = (0,0)
start_time = 0.0
end_time = 0.0
elapsed_time = 0.0
target_found = False
steps = 0
# Mutli-drone simulation data
drone_ids = []
drone_paths = []
drone_path_indices = []
drone_steps = []
drone_positions = []

def run_simulation():
    # Create the random goal point
    global goal_x, goal_y, after_id, canvas, drone_ids
    global target, grid_size, start_time, end_time
    global target_found, steps, elapsed_time
    global start_x, start_y, drone_paths
    global drone_path_indices, drone_steps, drone_positions

    try:
        start_x = int(start_x_var.get())
        start_y = int(start_y_var.get())
        drone_count = int(drone_count_var.get())
    except ValueError:
        status_label.config(text="Status: Invalid settings")
        return

    if not (0 <= start_x < cols and 0 <= start_y < rows):
        status_label.config(text="Status: Invalid starting point")
        return

    if drone_count > cols:
        status_label.config(text="Status: Need one column per drone")
        return

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    drone_positions, region_bounds = get_drone_positions(drone_count)

    goal_x = random.randint(0, cols - 1)
    goal_y = random.randint(0, rows - 1)
    target = (goal_x, goal_y)
    grid_size = (rows, cols)

    pattern = search_pattern_var.get()
    drone_paths = []

    for i, (start_col, end_col) in enumerate(region_bounds):
        drone_start_x, drone_start_y = drone_positions[i]

        search_path = region_search_path(pattern, rows, start_col, end_col, drone_start_x, drone_start_y)
        # Connect the starting point to the search path
        path = [drone_positions[i]]
        current_x, current_y = drone_positions[i]

        for point in search_path:
            next_x, next_y = point

            if (current_x, current_y) != (next_x, next_y):
                path.extend(
                    shortest_path(
                        current_x, current_y, next_x, next_y
                    )
                )

            current_x, current_y = next_x, next_y

        drone_paths.append(path)

    drone_path_indices = [0] * drone_count
    drone_steps = [0] * drone_count
    steps = 0

    if canvas is not None:
        canvas.destroy()

    canvas, drone_ids = create_grid(grid_frame, goal_x, goal_y, rows, cols, drone_positions=drone_positions)

    target_found = False
    end_time = 0.0
    elapsed_time = 0.0
    start_time = time.perf_counter()

    grid_size_label.config(text=f"Grid Size: {rows} x {cols}")
    target_label.config(text=f"Target: ({goal_x}, {goal_y})")
    steps_label.config(text="Steps: 0")
    time_label.config(text="Elapsed Time: 0.00 s")
    status_label.config(text=f"Status: Searching with {drone_count} drone(s)")

    move_drones()


def reset_simulation():
    global canvas, drone_ids, after_id
    global drone_paths, drone_path_indices, drone_steps, drone_positions
    global steps, target_found, elapsed_time, start_time, end_time

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    try:
        count = int(drone_count_var.get())
    except ValueError:
        count = 1

    count = max(1, min(count, cols))

    drone_positions, _ = get_drone_positions(count)

    if canvas is not None:
        canvas.destroy()

    canvas, drone_ids = create_grid(grid_frame, rows=rows, cols=cols, drone_positions=drone_positions)

    drone_paths = []
    drone_path_indices = [0] * count
    drone_steps = [0] * count
    steps = 0
    target_found = False
    elapsed_time = 0.0
    start_time = 0.0
    end_time = 0.0

    grid_size_label.config(text=f"Grid Size: {rows} x {cols}")
    target_label.config(text="Target: None")
    steps_label.config(text="Steps: 0")
    time_label.config(text="Elapsed Time: 0.00 s")
    status_label.config(text="Status: Ready")



def move_drones():
    global after_id, steps, target_found, end_time, elapsed_time

    if target_found:
        return

    active_drones = False

    for i, drone_path in enumerate(drone_paths):
        if drone_path_indices[i] >= len(drone_path):
            continue

        active_drones = True

        x, y = drone_path[drone_path_indices[i]]

        cell_size = 25
        left_margin = 40
        bottom_margin = 30
        center_x = left_margin + x * cell_size + cell_size / 2
        center_y = (rows - 1 - y) * cell_size + cell_size / 2
        radius = 6

        canvas.coords(drone_ids[i], center_x - radius, center_y - radius, center_x + radius, center_y + radius)

        drone_steps[i] += 1
        drone_path_indices[i] += 1

        # Check whether this drone has found the target
        if (x, y) == target:
            target_found = True
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            steps = sum(drone_steps)

            steps_label.config(text=f"Steps: {steps}")
            time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
            status_label.config(text=f"Status: Drone {i + 1} Found Target")
            after_id = None
            return

    steps = sum(drone_steps)
    elapsed_time = time.perf_counter() - start_time

    steps_label.config(text=f"Steps: {steps}")
    time_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")

    if any(drone_path_indices[i] < len(drone_paths[i]) for i in range(len(drone_paths))):
        after_id = root.after(speed, move_drones)
    else:
        after_id = None
        status_label.config(text="Status: Search Complete - Target Not Found")


def apply_grid_size():
    global rows, cols

    try:
        new_rows = int(rows_var.get())
        new_cols = int(cols_var.get())

        if new_rows > 0 and new_cols > 0:
            rows = new_rows
            cols = new_cols
            reset_simulation()

    except ValueError:
        pass

def apply_speed():
    global speed

    try:
        new_speed = int(speed_var.get())

        if new_speed > 0:
            speed = new_speed

    except ValueError:
        pass

def apply_starting_point():
    global start_x, start_y

    try:
        new_start_x = int(start_x_var.get())
        new_start_y = int(start_y_var.get())

        if 0 <= new_start_x < cols and 0 <= new_start_y < rows:
            start_x = new_start_x
            start_y = new_start_y
            reset_simulation()
    except ValueError:
        pass

def get_drone_positions(count):
    positions = []
    region_bounds = []

    for i in range(count):
        start_col = i * cols // count
        end_col = (i + 1) * cols // count - 1
        region_bounds.append((start_col, end_col))

        if i == 0:
            x = max(start_col, min(start_x, end_col))
            y = max(0, min(start_y, rows - 1))
        else:
            x = start_col
            y = 0
        
        positions.append((x, y))
    
    return positions, region_bounds
        

root = tk.Tk()
root.title("Drone Simulation")

title_label = tk.Label(root, text="Autonomous Drone Simulator", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Grid frame to hold the canvas
content_frame = tk.Frame(root)
content_frame.pack(pady=5)

grid_frame = tk.Frame(content_frame)
grid_frame.pack(side=tk.LEFT, padx=10, anchor='n')

goal_x = 0
goal_y = 0
canvas = None
drone = None
path = []
path_index = 0
after_id = None

# Data panel
data_frame = tk.LabelFrame(content_frame, text="Simulation Data", padx=10, pady=10)
data_frame.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
grid_size_label = tk.Label(data_frame, text="Grid Size: 10 x 10")
grid_size_label.pack(anchor="w", pady=2)

target_label = tk.Label(data_frame, text="Target: (0, 0)")
target_label.pack(anchor="w", pady=2)

steps_label = tk.Label(data_frame, text="Steps: 0")
steps_label.pack(anchor="w", pady=2)

time_label = tk.Label(data_frame, text="Elapsed Time: 0.00 s")
time_label.pack(anchor="w", pady=2)

status_label = tk.Label(data_frame, text="Status: Ready")
status_label.pack(anchor="w", pady=2)


# Settings
pattern_frame = tk.LabelFrame(root, text="Settings", padx=10, pady=10)
pattern_frame.pack(side=tk.BOTTOM, pady=10)

# Number of drones input
tk.Label(pattern_frame, text="Number of Drones:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
drone_count_var = tk.StringVar(value="1")
drone_count_menu = tk.OptionMenu(pattern_frame, drone_count_var, "1", "2", "3")
drone_count_menu.grid(row=0, column=1, padx=2, pady=2)

# Search pattern
tk.Label(pattern_frame, text="Search Pattern:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
search_pattern_var = tk.StringVar(value="Lawnmower")
pattern_menu = tk.OptionMenu(pattern_frame, search_pattern_var, "Lawnmower", "Spiral", "Spiral from Point")
pattern_menu.grid(row=1, column=1, padx=2, pady=2)

# Grid size input
tk.Label(pattern_frame, text="Grid Size:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
rows_var = tk.StringVar(value="10")
rows_entry = tk.Entry(pattern_frame, textvariable=rows_var, width=4)
rows_entry.grid(row=2, column=1, padx=(2,1), pady=5)

tk.Label(pattern_frame, text="x").grid(row=2, column=2, padx=1)

cols_var = tk.StringVar(value="10")
cols_entry = tk.Entry(pattern_frame, textvariable=cols_var, width=4)
cols_entry.grid(row=2, column=3, padx=(1,2), pady=5)

# Drone speed input
tk.Label(pattern_frame, text="Speed (ms):").grid(row=3, column=0, padx=2, pady=2, sticky="w")
speed_var = tk.StringVar(value="200")
speed_entry = tk.Entry(pattern_frame, textvariable=speed_var, width=4)
speed_entry.grid(row=3, column=1, padx=2, pady=2)

# Starting point input
tk.Label(pattern_frame, text="Starting Point (x,y):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
start_x_var = tk.StringVar(value="0")
start_x_entry = tk.Entry(pattern_frame, textvariable=start_x_var, width=4)
start_x_entry.grid(row=4, column=1, padx=(2,1), pady=5)
tk.Label(pattern_frame, text=",").grid(row=4, column=2, padx=1)

start_y_var = tk.StringVar(value="0")
start_y_entry = tk.Entry(pattern_frame, textvariable=start_y_var, width=4)
start_y_entry.grid(row=4, column=3, padx=(1,2), pady=5)

# Create legend to show which dot is drone, target, or obstacle
legend_frame = tk.Frame(root)
legend_frame.pack(side=tk.TOP, pady=10)

# Drone legend
drone_dot = tk.Canvas(legend_frame, width=15, height=15, bg="white")
drone_dot.create_oval(5, 5, 15, 15, fill="blue")
drone_dot.pack(side=tk.LEFT, padx=5)
tk.Label(legend_frame, text="Drone").pack(side=tk.LEFT, padx=(3, 15))

# Target legend
target_dot = tk.Canvas(legend_frame, width=15, height=15, bg="white")
target_dot.create_oval(5, 5, 15, 15, fill="red")
target_dot.pack(side=tk.LEFT)
tk.Label(legend_frame, text="Target").pack(side=tk.LEFT, padx=3)

# Create buttons to run/reset simulation
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=10)

run_button = tk.Button(button_frame, text="Run Simulation", command=run_simulation)
run_button.pack(side=tk.LEFT, padx=5)

reset_button = tk.Button(button_frame, text="Reset Simulation", command=reset_simulation)
reset_button.pack(side=tk.LEFT, padx=5)

# Create apply button for grid size, speed, starting point
apply_button = tk.Button(pattern_frame, text="Apply", command=lambda: [apply_grid_size(), apply_speed(), apply_starting_point()])
apply_button.grid(row=5, column=0, columnspan=4, pady=(10,4))

reset_simulation()
root.mainloop()
