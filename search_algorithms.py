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

