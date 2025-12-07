import numpy as np

def generate_fibonacci_spiral(width, height, scale=None):
    """Generate a Fibonacci spiral pattern"""
    pattern = np.zeros((height, width))
    phi = (1 + np.sqrt(5)) / 2
    
    # Calculate scale based on image dimensions
    if scale is None:
        scale = min(width, height) / 20
    
    def plot_point(x, y):
        if 0 <= x < width and 0 <= y < height:
            pattern[int(y), int(x)] = 1

    max_t = 4 * np.pi  # Two full rotations
    for t in np.arange(0, max_t, 0.1):
        r = scale * phi ** (t/2)
        x = width/2 + r * np.cos(t)
        y = height/2 + r * np.sin(t)
        plot_point(x, y)
    
    return pattern