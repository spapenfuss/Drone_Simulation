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

def spiral_path(rows, cols):
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