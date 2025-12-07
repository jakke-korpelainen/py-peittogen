import numpy as np

def generate_lsystem(width, height, iterations=5):
    """Generate a L-system pattern"""
    pattern = np.zeros((height, width))
    rules = {'F': 'F[+F]F[-F]F'}
    current = 'F'
    
    for _ in range(iterations):
        next_gen = ''.join(rules.get(c, c) for c in current)
        current = next_gen
    
    stack = []
    x, y = width/2, height-20
    angle = -90
    length = min(width, height) / (2 ** (iterations-1))  # Adaptive length
    
    for char in current:
        if char == 'F':
            new_x = x + length * np.cos(np.radians(angle))
            new_y = y + length * np.sin(np.radians(angle))
            if (0 <= x < width and 0 <= y < height and 
                0 <= new_x < width and 0 <= new_y < height):
                for t in np.linspace(0, 1, 10):
                    px = int(x * (1-t) + new_x * t)
                    py = int(y * (1-t) + new_y * t)
                    # Ensure indices are within bounds
                    if 0 <= px < width and 0 <= py < height:
                        pattern[int(py), int(px)] = 1
            x, y = new_x, new_y
        elif char == '+': angle += 25
        elif char == '-': angle -= 25
        elif char == '[': stack.append((x, y, angle))
        elif char == ']': 
            if stack:  # Check if stack is not empty
                x, y, angle = stack.pop()
    
    # Ensure output has integer indices for pattern generator
    return (pattern > 0).astype(int)