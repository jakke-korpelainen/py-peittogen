import numpy as np
from scipy.spatial import Voronoi

def generate_voronoi(width, height, points_count=None):
    """Generate a Voronoi pattern"""
    if points_count is None:
        points_count = int((width * height) ** 0.5 / 10)  # Adaptive point count
    
    pattern = np.zeros((height, width))
    
    # Add border points to ensure coverage
    border_points = np.array([
        [0, 0], [width/2, 0], [width, 0],
        [0, height/2], [width, height/2],
        [0, height], [width/2, height], [width, height]
    ])
    
    # Generate random points
    inner_points = np.random.rand(points_count, 2)
    inner_points[:,0] *= width * 0.8  # Slight inset from borders
    inner_points[:,1] *= height * 0.8
    inner_points += np.array([width*0.1, height*0.1])  # Center the pattern
    
    # Combine border and inner points
    points = np.vstack([border_points, inner_points])
    
    vor = Voronoi(points)
    
    for simplex in vor.ridge_vertices:
        if -1 not in simplex:
            x1, y1 = vor.vertices[simplex[0]]
            x2, y2 = vor.vertices[simplex[1]]
            
            for t in np.linspace(0, 1, 100):
                x = int(x1 * (1-t) + x2 * t)
                y = int(y1 * (1-t) + y2 * t)
                if 0 <= x < width and 0 <= y < height:
                    pattern[y, x] = 1
    
    return pattern