import random
import numpy as np
from typing import List
from tiles import TileType

class RowPattern:
    def __init__(self, tiles: List[TileType], repeat: bool = True, use_related: bool = False, rows: int = 1):
        self.tiles = tiles
        self.repeat = repeat
        self.use_related = use_related  # Whether to use related patterns for subsequent rows
        self.rows = rows  # How many rows this pattern group should span


# Pre-made blanket patterns for asthetically pleasing blankets
blanket_patterns = [
    # blanket example
    [
        RowPattern([TileType.A, TileType.B], use_related=True, rows=2),  # 2 rows of related diagonal patterns
        RowPattern([TileType.C, TileType.D, TileType.E], rows=1),  # 1 row of triple pattern
        RowPattern([TileType.E]), # 1 row of solid pattern
    ]
    # TODO: this is a stub, should add more blankets here
]

def get_related_pattern(prev_pattern: RowPattern) -> RowPattern:
    """Generate a related pattern based on the previous row"""
    # Simple relation: use complementary colors from available tiles
    all_tiles = list(TileType)
    unused_tiles = [t for t in all_tiles if t not in prev_pattern.tiles]
    return RowPattern(unused_tiles[:len(prev_pattern.tiles)], prev_pattern.repeat)

def generate_blanket(segments_x: int = 3, segments_y: int = 4) -> np.ndarray:
    """
    Generate a blanket pattern divided into segments
    
    Args:
        width: Total width in pixels (used only for array creation)
        height: Total height in pixels (used only for array creation)
        segments_x: Number of horizontal segments
        segments_y: Number of vertical segments
    
    Returns:
        numpy array representing the pattern with actual tile information
    """
    # Create pattern array with segment dimensions
    pattern = np.empty((segments_y, segments_x), dtype=object)
    
    # Define pattern sequence with different behaviors
    patterns = random.choice(blanket_patterns)
    
    current_pattern = patterns[0]
    pattern_index = 0
    rows_in_current = 0
    
    # Fill pattern array
    for sy in range(segments_y):
        for sx in range(segments_x):
            tile_type = current_pattern.tiles[sx % len(current_pattern.tiles)]
            pattern[sy, sx] = tile_type
        
        # Handle pattern transitions
        rows_in_current += 1
        if rows_in_current >= current_pattern.rows:
            rows_in_current = 0
            pattern_index = (pattern_index + 1) % len(patterns)
            current_pattern = patterns[pattern_index]
        elif current_pattern.use_related:
            current_pattern = get_related_pattern(current_pattern)
            current_pattern.use_related = True
            current_pattern.rows = patterns[pattern_index].rows - rows_in_current
    
    return pattern
