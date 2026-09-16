import tkinter as tk
from drone import Drone

def create_grid():
    # Create the main window
    root = tk.Tk()
    root.title("Grid")

    # Define grid size
    rows, cols = 10, 10
    cell_size = 30

    #space for axis labels
    left_margin = 40
    bottom_margin = 30
    canvas = tk.Canvas(root, width=cols * cell_size + left_margin, height=rows * cell_size + bottom_margin, bg="white")
    canvas.pack()

    # Draw the grid
    for row in range(rows):
        for col in range(cols):
            x1 = left_margin + col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white")
        
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

    # Create a Drone instance  
    drone_1 = Drone(9, 0, rows, cols)

    #calculate the drones position
    center_x = left_margin + drone_1.x * cell_size + cell_size / 2
    center_y = (rows - 1 - drone_1.y) * cell_size + cell_size / 2
    
    # draw the drone
    radius = 5
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, fill="blue")
    root.mainloop()


# Call the function to display the grid
create_grid()
