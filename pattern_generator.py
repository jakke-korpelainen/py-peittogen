__all__ = ['PatternGenerator']

import random
from PIL import Image
import os
import uuid
import numpy as np
from patterns.sine_wave import generate_sine_wave
from patterns.fibonacci_spiral import generate_fibonacci_spiral
from patterns.dragon_curve import generate_dragon_curve
from patterns.sierpinski import generate_sierpinski
from patterns.voronoi import generate_voronoi
from patterns.lsystem import generate_lsystem
from tiles import AlgorithmType, TileGenerator, TileType

class PatternGenerator:
    BIRD_NAMES = [
        'sparrow', 'robin', 'cardinal', 'bluejay', 'finch', 
        'dove', 'crow', 'raven', 'woodpecker', 'owl',
        'hawk', 'eagle', 'hummingbird', 'warbler', 'chickadee'
    ]

    def __init__(self, width, height, tile_size=1):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tile_generator = TileGenerator(tile_size)
        os.makedirs('./output', exist_ok=True)
    
    def _generate_filename(self) -> str:
        bird = random.choice(self.BIRD_NAMES)
        return os.path.join('./output', f'{bird}_{uuid.uuid4().hex[:6]}.png')
    
    # this function should produce an image of tiles where a same tile is allowed only diagonally as neighbour
    def random_pattern(self, img, tile_types):
        def get_tile_type_at(x, y):
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                return None
            # Get the pixel color at the center of the tile to determine its type
            center_x = x + self.tile_size // 2
            center_y = y + self.tile_size // 2
            return img.getpixel((center_x, center_y))

        def get_valid_tile_types(x, y):
            # Check horizontal and vertical neighbors
            left = get_tile_type_at(x - self.tile_size, y)
            right = get_tile_type_at(x + self.tile_size, y)
            top = get_tile_type_at(x, y - self.tile_size)
            bottom = get_tile_type_at(x, y + self.tile_size)
            
            # Create set of invalid colors (those present in neighbors)
            invalid_colors = set()
            for neighbor_color in [left, right, top, bottom]:
                if neighbor_color is not None:
                    invalid_colors.add(neighbor_color)
            
            # Return only tile types that aren't in invalid_colors
            valid_types = []
            for tile_type in tile_types:
                tile = self.tile_generator.create_tile(tile_type)
                center_color = tile.getpixel((self.tile_size // 2, self.tile_size // 2))
                if center_color not in invalid_colors:
                    valid_types.append(tile_type)
            return valid_types

        for y in range(0, self.height, self.tile_size):
            for x in range(0, self.width, self.tile_size):
                valid_types = get_valid_tile_types(x, y)
                if not valid_types:  # If no valid types, use any type
                    valid_types = tile_types
                tile_type = random.choice(valid_types)
                tile = self.tile_generator.create_tile(tile_type)
                img.paste(tile, (x, y))

    def generate_algorithmic_pattern(self, algorithm_type: AlgorithmType) -> Image.Image:
        # Create base image
        img = Image.new('RGB', (self.width, self.height))
        
        # Generate pattern based on algorithm
        if algorithm_type == AlgorithmType.SINEWAVE:
            generate_sine_wave(self, img, len(TileType))
        else:
            # Generate pattern based on algorithm
            pattern = None
            if algorithm_type == AlgorithmType.FIBONACCI:
                pattern = generate_fibonacci_spiral(self.width, self.height)
            elif algorithm_type == AlgorithmType.DRAGON:
                pattern = generate_dragon_curve(self.width, self.height)
            elif algorithm_type == AlgorithmType.SIERPINSKI:
                pattern = generate_sierpinski(self.width, self.height)
            elif algorithm_type == AlgorithmType.VORONOI:
                pattern = generate_voronoi(self.width, self.height)
            elif algorithm_type == AlgorithmType.LSYSTEM:
                pattern = generate_lsystem(self.width, self.height)
            
            if pattern is not None:
                # Scale the pattern to match tile size
                scaled_height = self.height // self.tile_size
                scaled_width = self.width // self.tile_size
                scaled_pattern = np.zeros((scaled_height, scaled_width))
                
                # Downsample the pattern to match tile grid
                for y in range(scaled_height):
                    for x in range(scaled_width):
                        y_start = y * self.tile_size
                        y_end = (y + 1) * self.tile_size
                        x_start = x * self.tile_size
                        x_end = (x + 1) * self.tile_size
                        # If any pixel in the tile area is 1, mark the tile
                        if np.any(pattern[y_start:y_end, x_start:x_end] > 0):
                            scaled_pattern[y, x] = 1

                # Use scaled pattern for tile placement
                tile_types = list(TileType)
                for y in range(scaled_height):
                    for x in range(scaled_width):
                        value = int(scaled_pattern[y, x])
                        tile_type = tile_types[value % len(tile_types)]
                        tile = self.tile_generator.create_tile(tile_type)
                        img.paste(tile, (x * self.tile_size, y * self.tile_size))
        
        filename = self._generate_filename()
        img.save(filename)
        return img, filename