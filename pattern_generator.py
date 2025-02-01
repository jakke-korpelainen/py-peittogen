__all__ = ['generate_pattern']

from typing import Tuple
from PIL import Image
import os
import uuid
import random
import numpy as np
from tiles import draw_tile_color, AlgorithmType, draw_tile_texture
from patterns.sine_wave import generate_sine_wave
from patterns.fibonacci_spiral import generate_fibonacci_spiral
from patterns.dragon_curve import generate_dragon_curve
from patterns.sierpinski import generate_sierpinski
from patterns.voronoi import generate_voronoi
from patterns.lsystem import generate_lsystem
from patterns.blanket import generate_blanket

BIRD_NAMES = [
    'sparrow', 'robin', 'cardinal', 'bluejay', 'finch', 
    'dove', 'crow', 'raven', 'woodpecker', 'owl',
    'hawk', 'eagle', 'hummingbird', 'warbler', 'chickadee'
]

def generate_filename() -> str:
    """Generate a filename"""
    bird = random.choice(BIRD_NAMES)
    return os.path.join('./output', f'{bird}_{uuid.uuid4().hex[:6]}.png')

def _apply_to_image(pattern: np.ndarray, width: int, height: int, tile_size: int, draw_func) -> Image.Image:
    """Apply pattern to image using draw function"""
    img = Image.new('RGB', (width, height))
    
    for y in range(len(pattern)):
        for x in range(len(pattern[0])):
            tile_type = pattern[y, x]
            if tile_type is None:
                continue
            
            # Create and paste tile
            tile = draw_func(tile_type, tile_size)
            paste_x = x * tile_size
            paste_y = y * tile_size
            
            # Only paste if within image bounds
            if paste_x + tile_size <= width and paste_y + tile_size <= height:
                img.paste(tile, (paste_x, paste_y))
    
    return img

def _apply_color_to_image(pattern: np.ndarray, width: int, height: int, tile_size: int) -> Image.Image:
    """Apply pattern to image using colors"""
    return _apply_to_image(pattern, width, height, tile_size, draw_tile_color)

def _apply_texture_to_image(pattern: np.ndarray, width: int, height: int, tile_size: int) -> Image.Image:
    """Apply pattern to image using textures"""
    return _apply_to_image(pattern, width, height, tile_size, draw_tile_texture)

def apply_algorithm(width: int, height: int, tile_size: int, algorithm_type: AlgorithmType, **kwargs) -> Image.Image:
    """Generate pattern based on algorithm"""
    
    if algorithm_type == AlgorithmType.SINEWAVE:
        return generate_sine_wave(width, height, tile_size)
    
    if algorithm_type == AlgorithmType.BLANKET:
        segments_x = kwargs.get('segments_x', 3)
        segments_y = kwargs.get('segments_y', 4)
        pattern = generate_blanket(segments_x, segments_y)
        
        # Calculate segment size based on image dimensions
        tile_size_x = width // segments_x
        tile_size_y = height // segments_y
        tile_size = min(tile_size_x, tile_size_y)
        
        return _apply_texture_to_image(pattern, width, height, tile_size)
        
    pattern_funcs = {
        AlgorithmType.FIBONACCI: generate_fibonacci_spiral,
        AlgorithmType.DRAGON: generate_dragon_curve,
        AlgorithmType.SIERPINSKI: generate_sierpinski,
        AlgorithmType.VORONOI: generate_voronoi,
        AlgorithmType.LSYSTEM: generate_lsystem,
    }
    
    if algorithm_type in pattern_funcs:
        pattern = pattern_funcs[algorithm_type](width, height)
        return _apply_color_to_image(pattern, width, height, tile_size)
    
    raise ValueError(f"Unknown algorithm type: {algorithm_type}")

def generate_pattern(width: int, height: int, algorithm_type: AlgorithmType, tile_size: int = 1, **kwargs) -> Tuple[Image.Image, str]:
    """Generate pattern"""
    os.makedirs('./output', exist_ok=True)
    
    img = apply_algorithm(width, height, tile_size, algorithm_type, **kwargs)
    filename = generate_filename()
    img.save(filename)
    
    return img, filename