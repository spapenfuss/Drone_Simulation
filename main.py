import tkinter as tk
import random
from grid import create_grid
from search_algorithms import lawnmower_path, spiral_path

# Default grid size
rows = 10
cols = 10
#default speed (milliseconds between moves)
speed = 200 

def run_simulation():
    # Create the random goal point
    global goal_x, goal_y, path, path_index, after_id, canvas, drone

    goal_x = random.randint(0, cols - 1)
    goal_y = random.randint(0, rows - 1)

    # Determine the search pattern based on user selection
    if search_pattern_var.get() == "Lawnmower":
        path = lawnmower_path(rows, cols)
    elif search_pattern_var.get() == "Spiral":
        path = spiral_path(rows, cols)

    path_index = 0
    after_id = None

    if canvas is not None:
        canvas.destroy()

    canvas, drone = create_grid(root, goal_x, goal_y, rows, cols)

    move_drone()


def reset_simulation():
    global canvas, drone, after_id, path_index

    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None

    path_index = 0

    if canvas is not None:
        canvas.destroy()

    canvas, drone = create_grid(root, rows=rows, cols=cols)


def move_drone():
    global path_index, after_id

    if path_index >= len(path):
        return
    
    x, y = path[path_index]

    # Check if drone has reached the goal
    if x == goal_x and y == goal_y:
        print("Drone has reached the goal!")
        return

    cell_size = 25
    left_margin = 40

    center_x = left_margin + x * cell_size + cell_size / 2
    center_y = (rows - 1 - y) * cell_size + cell_size / 2

    radius = 6

    canvas.coords(drone, center_x - radius, center_y - radius, center_x + radius, center_y + radius)

    path_index += 1

    after_id = root.after(speed, move_drone)


root = tk.Tk()
root.title("Drone Simulation")

goal_x = 0
goal_y = 0
canvas = None
drone = None
path = []
path_index = 0
after_id = None

# Search pattern menu bar
pattern_frame = tk.Frame(root)
pattern_frame.pack(side=tk.BOTTOM, pady=10)

tk.Label(pattern_frame, text="Select Search Pattern:").pack(side=tk.LEFT, padx=5)

search_pattern_var = tk.StringVar(value="Lawnmower")

pattern_menu = tk.OptionMenu(pattern_frame, search_pattern_var, "Lawnmower", "Spiral")

pattern_menu.pack(side=tk.LEFT, padx=5)

# Grid size input
grid_frame = tk.Frame(root)
grid_frame.pack(side=tk.BOTTOM, pady=5)

tk.Label(grid_frame, text="Rows:").pack(side=tk.LEFT, padx=5)

rows_var = tk.StringVar(value="10")
rows_entry = tk.Entry(grid_frame, textvariable=rows_var, width=5)
rows_entry.pack(side=tk.LEFT, padx=5)

tk.Label(grid_frame, text="Columns:").pack(side=tk.LEFT, padx=5)

cols_var = tk.StringVar(value="10")
cols_entry = tk.Entry(grid_frame, textvariable=cols_var, width=5)
cols_entry.pack(side=tk.LEFT, padx=5)


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

# Drone speed input
speed_frame = tk.Frame(root)
speed_frame.pack(side=tk.BOTTOM, pady=5)
tk.Label(speed_frame, text="Speed (ms):").pack(side=tk.LEFT, padx=5)
speed_var = tk.StringVar(value="200")
speed_entry = tk.Entry(speed_frame, textvariable=speed_var, width=5)
speed_entry.pack(side=tk.LEFT, padx=5)

def apply_speed():
    global speed

    try:
        new_speed = int(speed_var.get())

        if new_speed > 0:
            speed = new_speed

    except ValueError:
        pass

speed_button = tk.Button(
    speed_frame,
    text="Apply",
    command=apply_speed
)
speed_button.pack(side=tk.LEFT, padx=5)

grid_size_button = tk.Button(grid_frame, text="Apply", command=apply_grid_size)
grid_size_button.pack(side=tk.LEFT, padx=5)

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

reset_simulation()

root.mainloop()