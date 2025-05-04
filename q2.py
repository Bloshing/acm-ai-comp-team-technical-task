import numpy as np
from pathlib import Path

EXPECTED_FILE_NAMES = ['walls', 'terrain']
CSV_SUFFIX = '.csv'
CSV_DIR = 'csvs'

EMPTY, DRYWALL, WOOD, STONE = [0, 1, 2, 3]
MUD, DIRT, STONE, BEDROCK = [0, 1, 2, 3]

LEAK_ORIGIN = (6, 5)

def unstable_walls(walls: np.ndarray, terrain: np.ndarray, threshold: int = MUD) -> int:
    if not isinstance(walls, np.ndarray) or not isinstance(terrain, np.ndarray):
        raise TypeError("Inputs must be numpy arrays")
    if walls.shape != terrain.shape:
        raise ValueError("Walls and terrain arrays must have the same shape")
    if len(walls.shape) != 2:
        raise ValueError("Arrays must be 2-dimensional")
    
    wall_mask = (walls > 0)
    unstable_terrain_mask = (terrain <= threshold)
    return np.sum(wall_mask & unstable_terrain_mask)

def leak_territory(walls: np.ndarray, leak_origin: tuple[int] = LEAK_ORIGIN) -> int:
    if not isinstance(walls, np.ndarray):
        raise TypeError("Input must be a numpy array")
    if len(walls.shape) != 2:
        raise ValueError("Array must be 2-dimensional")
    
    if not isinstance(leak_origin, tuple) or len(leak_origin) != 2:
        raise TypeError("Leak origin must be a tuple of two integers")
    if not all(isinstance(x, int) for x in leak_origin):
        raise TypeError("Leak origin coordinates must be integers")
    
    rows, cols = walls.shape
    if not (0 <= leak_origin[0] < rows and 0 <= leak_origin[1] < cols):
        raise ValueError("Leak origin coordinates must be within array bounds")
    
    visited = np.zeros_like(walls, dtype=bool)
    queue = [leak_origin]
    visited[leak_origin] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    
    while queue:
        current_row, current_col = queue.pop(0)
        count += 1
        
        for row_change, col_change in directions:
            new_row = current_row + row_change
            new_col = current_col + col_change
            
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if walls[new_row, new_col] == EMPTY and not visited[new_row, new_col]:
                    visited[new_row, new_col] = True
                    queue.append((new_row, new_col))
    
    return count

def validate_env(csv_dir: Path):
    
    if (not csv_dir.exists()):
        raise('csv dir does not exist')
    for expected_file in EXPECTED_FILE_NAMES:
        expected_file_path = csv_dir / (expected_file + CSV_SUFFIX)
        if (not expected_file_path.exists()):
            raise(f'{expected_file_path} does not exist')

def main():

    parent_dir = Path(__file__).parent.resolve()
    csv_dir = parent_dir / CSV_DIR
    validate_env(csv_dir)

    WALLS = np.loadtxt(CSV_DIR / Path('walls.csv'), delimiter=',').astype(np.int8)
    TERRAIN = np.loadtxt(CSV_DIR / Path('terrain.csv'), delimiter=',').astype(np.int8)

    # Q2a result printed here
    print('unstable_walls:', unstable_walls(np.copy(WALLS), np.copy(TERRAIN), threshold=DIRT))

    # Q2b result printed here
    print('leak_territory:', leak_territory(np.copy(WALLS), leak_origin=LEAK_ORIGIN))

if __name__ == '__main__':
    main()
