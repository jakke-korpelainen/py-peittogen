__all__ = ['TileGenerator', 'TileType']

from enum import Enum
from PIL import Image, ImageDraw

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

class TileGenerator:
    DEFAULT_TILE_SIZE = 32
    
    # Predefined colors for each tile type
    TILE_COLORS = {
        TileType.A: (0, 0, 0),          # Black
        TileType.B: (255, 255, 255),    # White
        TileType.C: (0, 0, 255),        # Blue
        TileType.D: (255, 255, 0),      # Yellow
        TileType.E: (255, 0, 255),      # Magenta
        TileType.F: (0, 255, 255),      # Cyan
    }

    def __init__(self, tile_size: int = DEFAULT_TILE_SIZE):
        self._tile_size = tile_size
    
    @property
    def tile_size(self) -> int:
        return self._tile_size
    
    @tile_size.setter
    def tile_size(self, value: int):
        if value <= 0:
            raise ValueError("Tile size must be positive")
        self._tile_size = value
    
    def create_tile(self, tile_type: TileType) -> Image.Image:
        # Override color2 with predefined color for the tile type
        tile_color = self.TILE_COLORS[tile_type]
        return Image.new('RGB', (self.tile_size, self.tile_size), tile_color)