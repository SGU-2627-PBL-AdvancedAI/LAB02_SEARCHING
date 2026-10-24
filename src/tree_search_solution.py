import sys
import heapq
import numpy as np
import random

# --- CẤU HÌNH THỨ TỰ TÌM KIẾM ---
_search_order = "NESW"
_random_order = False

def set_order(order="NESW", random=False, **kwargs):
    global _search_order, _random_order
    _search_order = order
    _random_order = random

def min_index(lst):
    return lst.index(min(lst))

def show_path(maze, result):
    if result is None or 'path' not in result or result['path'] is None:
        print("No solution found!")
        return
    print(f"Path length: {len(result['path'])-1}")
    print(f"Nodes expanded: {result.get('nodes_expanded', 0)}")
    print(f"Max depth: {result.get('max_depth', 0)}")
    print(f"Max frontier: {result.get('max_frontier', 0)}")

# --- LỚP NODE CƠ BẢN ---
class Node:
    def __init__(self, pos, parent, action, cost):
        self.pos = tuple(pos)
        self.parent = parent
        self.action = action
        self.cost = cost

    def __str__(self):
        return f"Node - pos = {self.pos}; action = {self.action}; cost = {self.cost}"
    
    def get_path_from_root(self):
        node = self
        path = [node]
        while not node.parent is None:
            node = node.parent
            path.append(node)
        path.reverse()
        return path

# --- HÀM HỖ TRỢ XỬ LÝ MA TRẬN MÊ CUNG ---
def find_pos(maze, char):
    pos = np.where(maze == char)
    if len(pos[0]) > 0:
        return (int(pos[0][0]), int(pos[1][0]))
    return None

def maze_successors(maze, pos):
    row, col = pos
    successors = []
    directions = [('N', (-1, 0)), ('E', (0, 1)), ('S', (1, 0)), ('W', (0, -1))]
    
    global _random_order
    if _random_order:
        random.shuffle(directions)
        
    for action, (dr, dc) in directions:
        r, c = row + dr, col + dc
        if 0 <= r < maze.shape[0] and 0 <= c < maze.shape[1]:
            if maze[r, c] != 'X':
                successors.append((action, (r, c)))
    return successors

# --- HEURISTIC ĐỘNG ---
def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def euclidean(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

heuristic = manhattan # Gán mặc định

# --- 1. THUẬT TOÁN DFS & DEPTH-LIMITED SEARCH (DLS) ---
def DFS(maze, limit=float('inf'), max_tries=100000, check_cycle=True, frontier_option=1, **kwargs):
    start_pos = find_pos(maze, 'S')
    goal_pos = find_pos(maze, 'G')
    
    start_node = Node(pos=start_pos, parent=None, action=None, cost=0)
    frontier = [start_node] 
    reached = {start_node.pos: start_node} 
    
    nodes_expanded = 0
    max_frontier = 1
    max_depth = 0
    
    while frontier and nodes_expanded < max_tries:
        current_node = frontier.pop()
        
        if current_node.cost > max_depth:
            max_depth = current_node.cost
            
        if current_node.pos == goal_pos:
            path_nodes = current_node.get_path_from_root()
            return {
                'path': path_nodes,
                'actions': [n.action for n in path_nodes if n.action is not None],
                'nodes_expanded': nodes_expanded,
                'max_depth': max_depth,
                'max_frontier': max_frontier,
                'reached': reached # Hỗ trợ vẽ ảnh động
            }
        
        nodes_expanded += 1
        
        if current_node.cost < limit:
            for action, next_pos in maze_successors(maze, current_node.pos):
                child_cost = current_node.cost + 1
                
                if not check_cycle or next_pos not in reached or child_cost < reached[next_pos].cost:
                    child_node = Node(pos=next_pos, parent=current_node, action=action, cost=child_cost)
                    frontier.append(child_node)
                    reached[next_pos] = child_node
                    
            if len(frontier) > max_frontier:
                max_frontier = len(frontier)

    return {'path': None, 'actions': [], 'nodes_expanded': nodes_expanded, 'max_depth': max_depth, 'max_frontier': max_frontier, 'reached': reached}

# --- 2. THUẬT TOÁN ITERATIVE DEEPENING SEARCH (IDS) ---
def IDS(maze, max_tries=100000, frontier_option=2, **kwargs):
    total_nodes_expanded = 0
    max_frontier_all = 0
    
    for depth_limit in range(sys.maxsize):
        result = DFS(maze, limit=depth_limit, max_tries=max_tries, check_cycle=True, frontier_option=frontier_option, **kwargs)
        total_nodes_expanded += result['nodes_expanded']
        max_frontier_all = max(max_frontier_all, result['max_frontier'])
        
        if result['path'] is not None or result['nodes_expanded'] >= max_tries:
            result['nodes_expanded'] = total_nodes_expanded
            result['max_frontier'] = max_frontier_all
            return result
            
    return {'path': None, 'actions': [], 'reached': {}}

# --- 3. BEST-FIRST SEARCH (GBFS, A*, Weighted A*) ---
def best_first_search(maze, strategy="A*", W=1.0, max_tries=100000, **kwargs):
    start_pos = find_pos(maze, 'S')
    goal_pos = find_pos(maze, 'G')
    
    start_node = Node(pos=start_pos, parent=None, action=None, cost=0)
    
    frontier = []
    counter = 0
    heapq.heappush(frontier, (0, counter, start_node))
    reached = {start_node.pos: start_node}
    
    nodes_expanded = 0
    max_frontier = 1
    max_depth = 0
    
    global heuristic 
    
    while frontier and nodes_expanded < max_tries:
        _, _, current_node = heapq.heappop(frontier)
        
        if current_node.cost > max_depth:
            max_depth = current_node.cost
            
        if current_node.pos == goal_pos:
            path_nodes = current_node.get_path_from_root()
            return {
                'path': path_nodes,
                'actions': [n.action for n in path_nodes if n.action is not None],
                'nodes_expanded': nodes_expanded,
                'max_depth': max_depth,
                'max_frontier': max_frontier,
                'reached': reached # Hỗ trợ vẽ ảnh động
            }
            
        nodes_expanded += 1
        
        for action, next_pos in maze_successors(maze, current_node.pos):
            child_cost = current_node.cost + 1
            
            if next_pos not in reached or child_cost < reached[next_pos].cost:
                child_node = Node(pos=next_pos, parent=current_node, action=action, cost=child_cost)
                reached[next_pos] = child_node
                
                h_n = heuristic(next_pos, goal_pos) 
                
                if strategy == "BFS":
                    f_n = child_cost 
                elif strategy == "GBFS":
                    f_n = h_n
                elif strategy == "A*":
                    f_n = child_cost + W * h_n 
                else:
                    f_n = child_cost
                
                counter += 1
                heapq.heappush(frontier, (f_n, counter, child_node))
                
        if len(frontier) > max_frontier:
            max_frontier = len(frontier)

    return {'path': None, 'actions': [], 'nodes_expanded': nodes_expanded, 'max_depth': max_depth, 'max_frontier': max_frontier, 'reached': reached}

# --- 4. HÀM GỌI NHANH BFS ---
def BFS(maze, **kwargs):
    return best_first_search(maze, strategy="BFS", **kwargs)
