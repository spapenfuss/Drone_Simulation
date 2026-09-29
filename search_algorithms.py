def lawnmower_path(rows, cols):
    path = []
    for y in range(rows):
        if y % 2 == 0:
            # Move right
            for x in range(cols):
                path.append((x, y))
        else:
            # Move left
            for x in range(cols - 1, -1, -1):
                path.append((x, y))
    return path

def spiral_path_inwards(rows, cols):
    # Inward spiral around the grid
    path = []
    top = 0
    bottom = rows - 1
    left = 0
    right = cols - 1

    while top <= bottom and left <= right:
        for x in range(left, right + 1):
            path.append((x, top))
        top += 1

        for y in range(top, bottom + 1):
            path.append((right, y))
        right -= 1

        if top <= bottom:
            for x in range(right, left - 1, -1):
                path.append((x, bottom))
            bottom -= 1
        
        if left <= right:
            for y in range(bottom, top - 1, -1):
                path.append((left, y))
            left += 1

    return path

def spiral_path_from_point(rows, cols, start_x, start_y):
    # Outward spiral starting from a given point on grid
    path = []
    current_x = start_x
    current_y = start_y
    path.append((current_x, current_y))

    directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]  # right down left up
    direction_index = 0
    steps_to_move = 1

    while len(path) < rows * cols:
        for i in range(2):
            for j in range(steps_to_move):
                current_x += directions[direction_index][0]
                current_y += directions[direction_index][1]

                if 0 <= current_x < cols and 0 <= current_y < rows:
                    if (current_x, current_y) not in path:
                        path.append((current_x, current_y))

                if len(path) >= rows * cols:
                    return path

            direction_index = (direction_index + 1) % 4

        steps_to_move += 1

    return path
    
def shortest_path(start_x, start_y, goal_x, goal_y):
    # Simple straight-line pathfinding (not optimal for obstacles)
    path = []
    current_x = start_x
    current_y = start_y

    while current_x != goal_x or current_y != goal_y:
        if current_x < goal_x:
            current_x += 1
        elif current_x > goal_x:
            current_x -= 1

        if current_y < goal_y:
            current_y += 1
        elif current_y > goal_y:
            current_y -= 1

        path.append((current_x, current_y))

    return path
