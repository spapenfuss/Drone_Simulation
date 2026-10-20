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


def spiral_path_outwards(rows, cols):
    start_x = (cols - 1) // 2
    start_y = (rows - 1) // 2
    path = [(start_x, start_y)]
    visited = {(start_x, start_y)}

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    x, y = start_x, start_y
    steps_to_move = 1
    direction_index = 0

    while len(path) < rows * cols:
        for i in range(2):
            dx, dy = directions[direction_index]

            for j in range(steps_to_move):
                x += dx
                y += dy

                if 0 <= x < cols and 0 <= y < rows and (x, y) not in visited:
                    path.append((x, y))
                    visited.add((x, y))

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

def region_search_path(pattern, rows, start_col, end_col, start_x=None, start_y=0):
    region_cols = end_col - start_col + 1

    if pattern == "Lawnmower":
        path = lawnmower_path(rows, region_cols)
    elif pattern == "Spiral inwards":
        path = spiral_path_inwards(rows, region_cols)
    elif pattern == "Spiral outwards":
        local_start_x = start_x - start_col
        local_start_x = max(0, min(local_start_x, region_cols - 1))
        local_start_y = max(0, min(start_y, rows - 1))

        path = spiral_path_outwards(rows, region_cols)
    else:
        raise ValueError(f"Unknown search pattern: {pattern}")
    return [(x + start_col, y) for x, y in path]