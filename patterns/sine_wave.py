import math
from PIL import Image
from tiles import TileType, create_tile

def generate_sine_wave(width, height, tile_size):
    img = Image.new('RGB', (width, height))
    tile_types = list(TileType)
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            # Create a pattern based on sine waves
            wave1 = math.sin(x / 50) * math.cos(y / 50)
            wave2 = math.sin((x + y) / 100)
            
            # Map the combined waves to a tile index
            combined = (wave1 + wave2 + 2) / 4  # Normalize to 0-1 range
            tile_index = int(combined * len(tile_types)) % len(tile_types)
            
            # Create and paste the tile
            tile = create_tile(tile_types[tile_index])
            img.paste(tile, (x, y))

    return img