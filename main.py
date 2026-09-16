import tkinter as tk
import random
from grid import create_grid

rows = 20
cols = 20

def run_simulation():
    # Create the random goal point
    global goal_x, goal_y
    goal_x = random.randint(0, cols - 1)
    goal_y = random.randint(0, rows - 1)
    reset_simulation()

def reset_simulation():
    global canvas
    if canvas is not None:
        canvas.destroy()

    canvas = create_grid(root, goal_x, goal_y)

root = tk.Tk()
root.title("Drone Simulation")
goal_x = 0
goal_y = 0
canvas = None

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
