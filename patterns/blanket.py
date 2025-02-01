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

def _get_related_pattern(prev_pattern: RowPattern) -> RowPattern:
    """Generate a related pattern based on the previous row"""
    # Simple relation: use complementary colors from available tiles
    all_tiles = list(TileType)
    unused_tiles = [t for t in all_tiles if t not in prev_pattern.tiles]
    return RowPattern(unused_tiles[:len(prev_pattern.tiles)], prev_pattern.repeat)

def _generate_row(pattern: RowPattern, segments_x: int) -> List[TileType]:
    """Generate a single row of the blanket pattern"""
    return [pattern.tiles[x % len(pattern.tiles)] for x in range(segments_x)]

def _get_next_pattern_state(
    current_pattern: RowPattern,
    patterns: List[RowPattern],
    pattern_index: int,
    rows_in_current: int
) -> tuple[RowPattern, int, int]:
    """Determine the next pattern state"""
    new_rows_in_current = rows_in_current + 1
    new_pattern_index = pattern_index
    next_pattern = current_pattern

    if new_rows_in_current >= current_pattern.rows:
        new_rows_in_current = 0
        new_pattern_index = (pattern_index + 1) % len(patterns)
        next_pattern = patterns[new_pattern_index]
    elif current_pattern.use_related:
        next_pattern = _get_related_pattern(current_pattern)
        next_pattern.use_related = True
        next_pattern.rows = patterns[pattern_index].rows - new_rows_in_current

    return next_pattern, new_pattern_index, new_rows_in_current

def generate_blanket(segments_x: int = 3, segments_y: int = 4) -> np.ndarray:
    """
    Generate a blanket pattern divided into segments
    """
    patterns = random.choice(blanket_patterns)
    pattern = np.empty((segments_y, segments_x), dtype=object)
    
    def _generate_all_rows(
        current_pattern: RowPattern,
        pattern_index: int,
        rows_in_current: int,
        row: int
    ):
        if row >= segments_y:
            return
            
        pattern[row] = _generate_row(current_pattern, segments_x)
        
        next_pattern, next_index, next_rows = _get_next_pattern_state(
            current_pattern, patterns, pattern_index, rows_in_current
        )
        
        _generate_all_rows(next_pattern, next_index, next_rows, row + 1)
    
    _generate_all_rows(patterns[0], 0, 0, 0)
    return pattern
