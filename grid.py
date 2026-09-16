import tkinter as tk
from drone import Drone

def create_grid():
    # Create the main window
    root = tk.Tk()
    root.title("10x10 Grid")

    canvas = tk.Canvas(root, width=500, height=500, bg="white")
    canvas.pack()

    # Define grid size
    rows, cols = 10, 10
    cell_width = 50
    cell_height = 50

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
        
    # Create a Drone instance at a specific position (e.g., row 2, col 3)
    drone_1 = Drone(9,0)

    #calculate the drones position
    x1 = drone_1.col * cell_width
    y1 = drone_1.row * cell_height
    x2 = x1 + cell_width
    y2 = y1 + cell_height

    # find center of drones cell
    center_x = drone_1.col * cell_width + cell_width / 2
    center_y = (rows - 1 - drone_1.row) * cell_height + cell_height / 2
    
    # draw the drone
    radius = 10
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="blue")
    root.mainloop()


# Call the function to display the grid
create_grid()
