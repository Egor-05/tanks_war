def finder(obj, width, height, tile_size, ind):
    for i in range(height // tile_size):
        for j in range(width // tile_size):
            if j * tile_size + ind <= obj.x < (j + 1) * tile_size + ind and \
                    i * tile_size <= obj.y < (i + 1) * tile_size:
                return (j, i)