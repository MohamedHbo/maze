import pygame
import heapq
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)

# (up, down, left, right)
neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")

# Define cell and grid sizes
CELL_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# icons
ICON_SIZE = (CELL_SIZE, CELL_SIZE)


icon_img = pygame.image.load('bus.png')
icon_img = pygame.transform.scale(icon_img, ICON_SIZE)


start_img = pygame.image.load('start.jpeg')
end_img = pygame.image.load('end.jpeg')

start_img = pygame.transform.scale(start_img, ICON_SIZE)
end_img = pygame.transform.scale(end_img, ICON_SIZE)

# sound 
pygame.mixer.music.load('hbos.mpga')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


# Maze representation (0 for open, 1 for walls)
maze = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Define start and end points
start = (0, 0)
end = (GRID_HEIGHT -1 , GRID_WIDTH-1 )

# Generate walls randomly
for _ in range(WIDTH*HEIGHT):
    row = pygame.time.get_ticks() % GRID_HEIGHT
    col = pygame.time.get_ticks() % GRID_WIDTH
    if row % 2==0 and (row,col)!=(0,0)and(row ,col)!=(GRID_HEIGHT -1 , GRID_WIDTH-1 ):
      maze[row][col] = 1

def dfs(maze, start, end):
    stack = [(start, [start])]
    visited = []
    count=1
    while stack:
        current_pos, path = stack.pop(-1)

        if current_pos == end:
            return path,count

        if current_pos in visited:
            continue

        visited.append(current_pos)
        count=count+1
        for direction in neighbors:
            new_row, new_col = current_pos[0] + direction[0], current_pos[1] + direction[1]

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                stack.append(((new_row, new_col), path + [(new_row, new_col)]))

    return []

def bfs(maze, start, end):
    queue = [(start, [start])]
    visited = set()
    count=1
    while queue:
        current, path = queue.pop(0)

        if current == end:
            return path,count

        if current in visited:
            continue

        visited.add(current)
        count=count+1
        for direction in neighbors:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                queue.append(((new_row, new_col), path + [(new_row, new_col)]))

    return []
#Define node class for A* and UCS
class Node:
    def __init__(self, position, cost=0, path=None, heuristic=0):
        self.position = position
        self.cost = cost
        self.path = path or [position]
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
    
def heuristic_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def greedy_best_first(maze, start, end):
    heap = [Node(start, 0, [start], heuristic_distance(start, end))]
    visited = set()
    count=1
    while heap:
        current_node = heapq.heappop(heap)
        current, path = current_node.position, current_node.path

        if current == end:
            return path,count

        if current in visited:
            continue

        visited.add(current)
        count=count+1
        for direction in neighbors:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                new_pos=(new_row,new_col)
                new_path = path + [(new_pos)]
                heapq.heappush(heap, Node((new_pos), 0, new_path, heuristic_distance((new_pos), end)))

    return []

def ucs(maze, start, end):
    heap = [Node(start, 0)]
    visited = set()
    count=1
    while heap:
        current_node = heapq.heappop(heap)
        current, cost ,path= current_node.position, current_node.cost,current_node.path

        if current == end:
            return current_node.path,count

        if current in visited:
            continue

        visited.add(current)
        count=count+1
        for direction in neighbors:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                new_pos=(new_row,new_col)
                new_cost = cost + 1 
                new_path=path+[(new_pos)] 
                heapq.heappush(heap, Node((new_pos), new_cost, new_path, 0))  # Add the new node to the heap


    return []  

def astar(maze, start, end):
    heap = [Node(start, 0, [start], heuristic_distance(start, end))]
    visited = set()
    count=1
    while heap:
        current_node = heapq.heappop(heap)
        current, cost, path = current_node.position, current_node.cost, current_node.path

        if current == end:
            return current_node.path,count

        if current in visited:
            continue

        visited.add(current)
        count=count+1
        for direction in neighbors:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]

            if 0 <= new_row < GRID_HEIGHT and 0 <= new_col < GRID_WIDTH and maze[new_row][new_col] == 0:
                new_pos=(new_row,new_col)
                new_path = path + [new_pos]
                new_cost=cost+1
                heapq.heappush(heap, Node((new_pos), new_cost, new_path,
                                          heuristic_distance((new_pos), end)))

    return []

def draw_maze():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if maze[row][col] == 1:
                pygame.draw.rect(screen, GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    screen.blit(start_img, (start[1] * CELL_SIZE, start[0] * CELL_SIZE))
    screen.blit(end_img, (end[1] * CELL_SIZE, end[0] * CELL_SIZE))

def draw_path(path,number_of_cells):
    for row, col in path:
        screen.blit(icon_img, (col * CELL_SIZE, row * CELL_SIZE))
        pygame.display.set_caption(f"Maze Solver - Algorithm: {algorithm_name}, Total Cost: {len(path)}, Cell-Visited: {number_of_cells}")
        pygame.display.flip()
        pygame.time.delay(80)

running = True
algorithm = None
path = [] 
algorithm_name = ""
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                algorithm = bfs
                algorithm_name = "BFS"
            elif event.key == pygame.K_d:
                algorithm = dfs
                algorithm_name = "DFS"
            elif event.key == pygame.K_a:
                algorithm = astar
                algorithm_name = "A*"
            elif event.key == pygame.K_u:
                algorithm = ucs
                algorithm_name = "UCS"
            elif event.key == pygame.K_g:
                algorithm = greedy_best_first
                algorithm_name = "Greedy-best-first"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // CELL_SIZE
            col = mouse_pos[0] // CELL_SIZE
            if event.button == 1:  # Left mouse button
                start = (row, col)
                if maze[row][col]==1:
                    pygame.display.set_caption("start cell in wrong position")
                    start=(0,0)
                else :
                    pygame.display.set_caption("maze solver")
                
            elif event.button == 3:  # Right mouse button
                end = (row, col)
                if maze[row][col]==1:
                    pygame.display.set_caption("end cell in wrong position")
                    end = (GRID_HEIGHT -1 , GRID_WIDTH-1 )
                else :
                    pygame.display.set_caption("maze solver")
            

    draw_maze()
    
    if start and end and algorithm:
        path,cell_visited = algorithm(maze, start, end)
        draw_path(path,cell_visited)
        algorithm = None
        pygame.display.set_caption("maze solver")
    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
