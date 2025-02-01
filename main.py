from typing import Optional, Tuple, Callable
from algorithms import AlgorithmType
from pattern_generator import generate_pattern
import sys
import time
import itertools
import threading
import os

def _create_spinner(start_time) -> Tuple[Callable, Callable]:
    """Create a spinner to show progress in terminal"""
    state = {'running': False, 'start_time': start_time}
    spinner = itertools.cycle(['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'])
    
    def spin():
        while state['running']:
            elapsed = time.time() - state['start_time']
            sys.stdout.write(f'Generating ({elapsed:.1f}s) ')
            sys.stdout.write(next(spinner))
            sys.stdout.write('\b' * 20)
            sys.stdout.flush()
            time.sleep(0.1)
    
    def start_spinner():
        state['running'] = True
        state['start_time'] = time.time()
        threading.Thread(target=spin).start()
        
    def stop_spinner():
        state['running'] = False
        
    return start_spinner, stop_spinner

def _parse_arguments(args: list) -> Optional[Tuple[int, int, AlgorithmType, dict]]:
    """Pure function to parse command line arguments"""
    if len(args) < 3:
        return None
        
    try:
        width = int(args[1])
        height = int(args[2])
        pattern_type = AlgorithmType(args[3]) if len(args) > 3 else AlgorithmType.SINEWAVE
        
        kwargs = {}
        if pattern_type == AlgorithmType.BLANKET:
            kwargs['segments_x'] = int(args[4])
            kwargs['segments_y'] = int(args[5])
        
        return width, height, pattern_type, kwargs
    except ValueError:
        return None

def main() -> None:
    result = _parse_arguments(sys.argv)
            
    print(f"Arguments: {result}")
    
    if result is None:
        print("Usage: python main.py <width> <height> [pattern_type]")
        print("For blanket pattern: python main.py <width> <height> blanket <segments_x> <segments_y>")
        print("Available patterns:", [t.value for t in AlgorithmType])
        return
        
    width, height, pattern_type, kwargs = result
    
    try:
        start_time = time.time()
        start_spinner, stop_spinner = _create_spinner(start_time)
        start_spinner()
        _, filename = generate_pattern(width, height, pattern_type, **kwargs)
        
        stop_spinner()
        elapsed_time = time.time() - start_time
        print(f"\rImage generated: {filename} (took {elapsed_time:.2f} seconds)")

        os.startfile(filename)
    except Exception as e:
        stop_spinner()
        print(f"\rError generating patterns: {str(e)}")

if __name__ == "__main__":
    main()