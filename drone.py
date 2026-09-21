class Drone:
    def __init__(self, x, y, rows, cols):
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
    
    def move_up(self):
        if self.col < self.rows - 1:
            self.col += 1
    
    def move_down(self):
        if self.col > 0:
            self.col -= 1
    
    def move_left(self):
        if self.row > 0:
            self.row -= 1
    
    def move_right(self):
        if self.row < self.cols - 1:
            self.row += 1
    
    def move_to(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            self.x = x
            self.y = y