import numpy as np

def generate_dragon_curve(width, height, iterations=12):
    """Generate a dragon curve pattern"""
    pattern = np.zeros((height, width))
    
    def dragon_points(n):
        turns = [1]
        for i in range(n):
            turns = turns + [1] + [-x for x in turns][::-1]
        return turns

    step_size = min(width, height) / (2 ** (iterations/2))
    x, y = width//3, height//2
    dx, dy = step_size, 0
    points = [(x, y)]
    
    for turn in dragon_points(iterations):
        if turn == 1:
            dx, dy = -dy, dx
        else:
            dx, dy = dy, -dx
        x, y = x + dx, y + dy
        if 0 <= x < width and 0 <= y < height:
            pattern[int(y), int(x)] = 1
            
    return pattern