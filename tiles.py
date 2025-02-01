__all__ = ['draw_tile_color', 'TileType', 'AlgorithmType']

from enum import Enum
import sys
from PIL import Image
from typing import Tuple

class TileType(Enum):
    A = "tile_a"
    B = "tile_b"
    C = "tile_c"
    D = "tile_d"
    E = "tile_e"

class AlgorithmType(Enum):
    FIBONACCI = "fibonacci"
    DRAGON = "dragon"
    SIERPINSKI = "sierpinski"
    VORONOI = "voronoi"
    LSYSTEM = "lsystem"
    SINEWAVE = "sinewave"
    BLANKET = "blanket"

DEFAULT_TILE_SIZE = 32

# Move tile colors to module level constant
TILE_COLORS: dict[TileType, Tuple[int, int, int]] = {
    TileType.A: (0, 0, 0),       # Black
    TileType.B: (255, 255, 255), # White
    TileType.C: (0, 0, 255),     # Blue
    TileType.D: (255, 255, 0),   # Yellow
    TileType.E: (255, 0, 255),   # Magenta
}

def _get_tile_texture_path(tile_type: TileType) -> str:
    """Get path to texture for tile type"""
    return f"tiles/{tile_type.value}.png"

def draw_tile_color(tile_type: TileType, tile_size: int = DEFAULT_TILE_SIZE) -> Image.Image:
    """Create a tile image based on type and size"""
    if tile_size <= 0:
        raise ValueError("Tile size must be positive")
    return Image.new('RGB', (tile_size, tile_size), TILE_COLORS[tile_type])

def draw_tile_texture(tile_type: TileType, tile_size: int = DEFAULT_TILE_SIZE) -> Image.Image:
    """Create a tile image based on type and size using texture"""
    if tile_size <= 0:
        raise ValueError("Tile size must be positive")

    # Load texture image
    texture = Image.open(_get_tile_texture_path(tile_type))
    texture = texture.resize((tile_size, tile_size))
    return texture