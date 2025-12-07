__all__ = ['generate_pattern']

from typing import Tuple, List, Optional
from PIL import Image
import os
import uuid
import random
import numpy as np
from tiles import create_tile, TileType, AlgorithmType
from patterns.sine_wave import generate_sine_wave
from patterns.fibonacci_spiral import generate_fibonacci_spiral
from patterns.dragon_curve import generate_dragon_curve
from patterns.sierpinski import generate_sierpinski
from patterns.voronoi import generate_voronoi
from patterns.lsystem import generate_lsystem

BIRD_NAMES = [
    'sparrow', 'robin', 'cardinal', 'bluejay', 'finch', 
    'dove', 'crow', 'raven', 'woodpecker', 'owl',
    'hawk', 'eagle', 'hummingbird', 'warbler', 'chickadee'
]

def generate_filename() -> str:
    """Generate a filename"""
    bird = random.choice(BIRD_NAMES)
    return os.path.join('./output', f'{bird}_{uuid.uuid4().hex[:6]}.png')

def get_valid_tile_types(img: Image.Image, x: int, y: int, tile_size: int, tile_types: List[TileType]) -> List[TileType]:
    """Get valid tile types for a position"""
    def get_tile_type_at(px: int, py: int) -> Optional[Tuple[int, int, int]]:
        if px < 0 or py < 0 or px >= img.width or py >= img.height:
            return None
        return img.getpixel((px + tile_size // 2, py + tile_size // 2))

    neighbors = [
        get_tile_type_at(x - tile_size, y),
        get_tile_type_at(x + tile_size, y),
        get_tile_type_at(x, y - tile_size),
        get_tile_type_at(x, y + tile_size)
    ]
    
    invalid_colors = {color for color in neighbors if color is not None}
    return [
        t_type for t_type in tile_types 
        if create_tile(t_type, tile_size).getpixel((tile_size // 2, tile_size // 2)) not in invalid_colors
    ]

def apply_pattern_to_image(pattern: np.ndarray, width: int, height: int, tile_size: int) -> Image.Image:
    """Apply pattern to image"""
    img = Image.new('RGB', (width, height))
    scaled_height = height // tile_size
    scaled_width = width // tile_size
    
    for y in range(scaled_height):
        for x in range(scaled_width):
            value = int(pattern[y * tile_size:(y + 1) * tile_size, 
                              x * tile_size:(x + 1) * tile_size].any())
            tile_type = list(TileType)[value % len(TileType)]
            tile = create_tile(tile_type, tile_size)
            img.paste(tile, (x * tile_size, y * tile_size))
    
    return img

def apply_algorithm(width: int, height: int, tile_size: int, algorithm_type: AlgorithmType) -> Image.Image:
    """Generate pattern based on algorithm"""
    
    if algorithm_type == AlgorithmType.SINEWAVE:
        return generate_sine_wave(width, height, tile_size)
        
    pattern_funcs = {
        AlgorithmType.FIBONACCI: generate_fibonacci_spiral,
        AlgorithmType.DRAGON: generate_dragon_curve,
        AlgorithmType.SIERPINSKI: generate_sierpinski,
        AlgorithmType.VORONOI: generate_voronoi,
        AlgorithmType.LSYSTEM: generate_lsystem
    }
    
    if algorithm_type in pattern_funcs:
        pattern = pattern_funcs[algorithm_type](width, height)
        return apply_pattern_to_image(pattern, width, height, tile_size)
    
    raise ValueError(f"Unknown algorithm type: {algorithm_type}")

def generate_pattern(width: int, height: int, algorithm_type: AlgorithmType, tile_size: int = 1) -> Tuple[Image.Image, str]:
    """Generate pattern"""
    os.makedirs('./output', exist_ok=True)
    
    img = apply_algorithm(width, height, tile_size, algorithm_type)
    filename = generate_filename()
    img.save(filename)
    
    return img, filename