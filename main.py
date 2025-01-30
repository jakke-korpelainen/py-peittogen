from pattern_generator import PatternGenerator
from tiles import AlgorithmType, TileType
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <width> <height> [pattern_type]")
        print("Available patterns:", [t.value for t in TileType])
        return

    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
        pattern_type = AlgorithmType(sys.argv[3]) if len(sys.argv) > 3 else None
    except ValueError:
        print("Width and height must be integers")
        return
    except ValueError:
        print(f"Invalid pattern type. Available patterns: {[t.value for t in AlgorithmType]}")
        return

    generator = PatternGenerator(width, height)

    try:
        _, filename = generator.generate_algorithmic_pattern(pattern_type)
        print("Image generated:", filename)
    except Exception as e:
        print(f"Error generating patterns: {str(e)}")
        return

if __name__ == "__main__":
    main()