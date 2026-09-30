import numpy as np

def create_grid_graph_and_heuristics(grid, target):
    rows, cols = grid.shape
    target_r, target_c = target
    
    graph = {}
    heuristics = {}

    def is_wall(r, c):
        # Treat out-of-bounds areas as walls
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return True
        return grid[r, c] == 99

    def get_node_cost(r, c):
        if grid[r, c] == 99:
            return 10000

        direct_neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        corner_neighbors = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]

        if any(is_wall(nr, nc) for nr, nc in direct_neighbors):
            return 4

        if any(is_wall(nr, nc) for nr, nc in corner_neighbors):
            return 3

        return 2

    # Movement directions (Up, Down, Left, Right)
    movement_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for r in range(rows):
        for c in range(cols):
            current_node = (r, c)
            graph[current_node] = []
            
            # 1. Calculate the heuristic (Manhattan distance to target)
            # We use absolute differences so the distance doesn't become negative
            heuristics[current_node] = abs(r - target_r) + abs(c - target_c)

            # 2. Build the graph edges
            for dr, dc in movement_directions:
                nr, nc = r + dr, c + dc
                
                if 0 <= nr < rows and 0 <= nc < cols:
                    target_cost = get_node_cost(nr, nc)
                    graph[current_node].append(((nr, nc), target_cost))

    return graph, heuristics

# =========================================
# Example Usage
# =========================================
if __name__ == "__main__":
    test_grid = np.zeros((35, 30), dtype=int)
    
    # Place a wall
    test_grid[1, 1] = 99
    
    # Set a target at the bottom right
    target_cell = (34, 29)
    
    # Generate both dictionaries
    graph, heuristics = create_grid_graph_and_heuristics(test_grid, target_cell)
    
    # Check the heuristic for the top-left cell (0, 0)
    # Expected: abs(0 - 34) + abs(0 - 29) = 34 + 29 = 63
    print("Heuristic for (0, 0):", heuristics[(0, 0)])
    
    # Check the heuristic for the target cell itself
    # Expected: 0
    print("Heuristic for (20, 27):", heuristics[(20, 27)])