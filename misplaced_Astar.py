import heapq

# -----------------------------
# 1. HEURISTIC: Misplaced Tiles
# -----------------------------
def misplaced_tiles(state, goal):
    """Count of tiles not in their goal position"""
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

# -----------------------------
# 2. PRINT FUNCTION
# -----------------------------
def print_state(state):
    for row in state:
        print(" ".join(str(num) if num != 0 else " " for num in row))
    print()

# -----------------------------
# 3. A* ALGORITHM using Misplaced Tiles heuristic
# -----------------------------
def a_star(start, goal):
    pq = []  # priority queue (min-heap)
    heapq.heappush(pq, (0, start, []))  # (f(n), current_state, path_so_far)
    visited = set()

    while pq:
        f, state, path = heapq.heappop(pq)

        if state == goal:
            return path

        visited.add(tuple(map(tuple, state)))

        # Find blank (0) position
        i, j = [(row_i, col_i)
                for row_i in range(3)
                for col_i in range(3) if state[row_i][col_i] == 0][0]

        # Possible blank moves
        moves = [(-1, 0, "Up"), (1, 0, "Down"), (0, -1, "Left"), (0, 1, "Right")]

        for dx, dy, action in moves:
            x, y = i + dx, j + dy
            if 0 <= x < 3 and 0 <= y < 3:
                new_state = [row[:] for row in state]
                # Swap blank with neighbor
                new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]

                if tuple(map(tuple, new_state)) not in visited:
                    h = misplaced_tiles(new_state, goal)
                    g = len(path) + 1  # cost so far
                    f_new = g + h
                    heapq.heappush(pq, (f_new, new_state, path + [action]))

    return None  # if no solution

# -----------------------------
# 4. RUN
# -----------------------------
print("Enter the puzzle state as 9 numbers (0 for blank):")
nums = list(map(int, input().split()))
start_state = [nums[i:i+3] for i in range(0, 9, 3)]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

solution = a_star(start_state, goal_state)

if not solution:
    print("No solution found")
else:
    print("Initial State:")
    print_state(start_state)
    current_state = start_state

    for step in solution:
        print(f"Move: {step}")
        # Find blank
        i, j = [(row_i, col_i)
                for row_i in range(3)
                for col_i in range(3) if current_state[row_i][col_i] == 0][0]

        if step == "Up":
            x, y = i - 1, j
        elif step == "Down":
            x, y = i + 1, j
        elif step == "Left":
            x, y = i, j - 1
        elif step == "Right":
            x, y = i, j + 1

        # Create new state after move
        new_state = [row[:] for row in current_state]
        new_state[i][j], new_state[x][y] = new_state[x][y], new_state[i][j]
        current_state = new_state

        print_state(current_state)
