import numpy as np

def generate_sierpinski(width, height, depth=8):
    """Generate a Sierpinski triangle pattern"""
    pattern = np.zeros((height, width))
    
    def draw_triangle(x1, y1, x2, y2, x3, y3, depth):
        """Draw a triangle with given vertices"""
        if depth == 0:
            for x, y in [(x1,y1), (x2,y2), (x3,y3)]:
                if 0 <= x < width and 0 <= y < height:
                    pattern[int(y), int(x)] = 1
            return
        
        mx1, my1 = (x1 + x2) / 2, (y1 + y2) / 2
        mx2, my2 = (x2 + x3) / 2, (y2 + y3) / 2
        mx3, my3 = (x3 + x1) / 2, (y3 + y1) / 2
        
        draw_triangle(x1, y1, mx1, my1, mx3, my3, depth-1)
        draw_triangle(mx1, my1, x2, y2, mx2, my2, depth-1)
        draw_triangle(mx3, my3, mx2, my2, x3, y3, depth-1)
    
    y_top = height * 0.1  # Leave some margin at top
    y_bottom = height * 0.9  # Leave some margin at bottom
    draw_triangle(width/2, y_top,  # top vertex
                 width * 0.1, y_bottom,  # bottom left
                 width * 0.9, y_bottom,  # bottom right
                 depth)
    return pattern