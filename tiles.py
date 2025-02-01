__all__ = ['create_tile', 'TileType', 'AlgorithmType']

from enum import Enum
from PIL import Image
from typing import Tuple

class TileType(Enum):
    A = "tile_a"
    B = "tile_b"
    C = "tile_c"
    D = "tile_d"
    E = "tile_e"
    F = "tile_f"

class AlgorithmType(Enum):
    FIBONACCI = "fibonacci"
    DRAGON = "dragon"
    SIERPINSKI = "sierpinski"
    VORONOI = "voronoi"
    LSYSTEM = "lsystem"
    SINEWAVE = "sinewave"

DEFAULT_TILE_SIZE = 32

# Move tile colors to module level constant
TILE_COLORS: dict[TileType, Tuple[int, int, int]] = {
    TileType.A: (0, 0, 0),       # Black
    TileType.B: (255, 255, 255), # White
    TileType.C: (0, 0, 255),     # Blue
    TileType.D: (255, 255, 0),   # Yellow
    TileType.E: (255, 0, 255),   # Magenta
    TileType.F: (0, 255, 255),   # Cyan
}

def create_tile(tile_type: TileType, tile_size: int = DEFAULT_TILE_SIZE) -> Image.Image:
    """Pure function to create a tile"""
    if tile_size <= 0:
        raise ValueError("Tile size must be positive")
    return Image.new('RGB', (tile_size, tile_size), TILE_COLORS[tile_type])