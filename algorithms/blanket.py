import random
import numpy as np
from typing import List
from tiles import TileType

tile_base = [TileType.A, TileType.B]
tile_flowers = [TileType.C, TileType.D, TileType.E, TileType.F]
tile_flowers_counter = {tile: 0 for tile in tile_flowers}

def _get_least_used_flowers() -> List[TileType]:
    """Get flower tiles that have been used the least"""
    min_usage = min(tile_flowers_counter.values())
    return [tile for tile, count in tile_flowers_counter.items() if count == min_usage]

def _choose_flower() -> TileType:
    """Choose a flower tile with preference for less used ones"""
    candidates = _get_least_used_flowers()
    chosen = random.choice(candidates)
    tile_flowers_counter[chosen] += 1
    return chosen

class QuiltRow:
    def __init__(self, tiles: List[TileType], repeat: bool = True, rows: int = 1):
        self.tiles = tiles
        self.repeat = repeat
        self.rows = rows

quilt_template = [
    QuiltRow([TileType.A, _choose_flower], rows=1),
    QuiltRow([_choose_flower, TileType.B], rows=1),
]

def _resolve_tile(tile) -> TileType:
    """Resolve tile value from callable or direct TileType"""
    return tile() if callable(tile) else tile

def _generate_quilt_row(pattern: QuiltRow, segments_x: int) -> List[TileType]:
    """Generate a single row of the blanket quilt"""
    return [_resolve_tile(pattern.tiles[x % len(pattern.tiles)]) for x in range(segments_x)]

def _get_next_pattern_state(
    current_pattern: QuiltRow,
    patterns: List[QuiltRow],
    pattern_index: int,
    rows_in_current: int
) -> tuple[QuiltRow, int, int]:
    """Determine the next pattern state"""
    new_rows_in_current = rows_in_current + 1
    new_pattern_index = pattern_index
    next_pattern = current_pattern

    if new_rows_in_current >= current_pattern.rows:
        new_rows_in_current = 0
        new_pattern_index = (pattern_index + 1) % len(patterns)
        next_pattern = patterns[new_pattern_index]

    return next_pattern, new_pattern_index, new_rows_in_current

def generate_blanket(segments_x: int = 3, segments_y: int = 4) -> np.ndarray:
    """
    Generate a blanket pattern divided into segments
    """
    
    pattern = np.empty((segments_y, segments_x), dtype=object)
    
    def _generate_all_rows(
        current_pattern: QuiltRow,
        pattern_index: int,
        rows_in_current: int,
        row: int
    ):
        if row >= segments_y:
            return
            
        pattern[row] = _generate_quilt_row(current_pattern, segments_x)
        
        next_pattern, next_index, next_rows = _get_next_pattern_state(
            current_pattern, quilt_template, pattern_index, rows_in_current
        )
        
        _generate_all_rows(next_pattern, next_index, next_rows, row + 1)
    
    _generate_all_rows(quilt_template[0], 0, 0, 0)

    return pattern
