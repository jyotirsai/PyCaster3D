from collections import deque

class PathFinder:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.graph = {}
        self.build_graph()
    
    def get_path(self, start, goal):
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]
    
    def bfs(self, start, goal, graph):
        q = deque([start])
        visited = {start: None}

        while q:
            node = q.popleft()
            if node == goal:
                break
            next_nodes = graph[node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.enemy_pos:
                    q.append(next_node)
                    visited[next_node] = node
        
        return visited
    
    def get_next_nodes(self, x, y):
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        return [(x+dx, y+dy) for dx,dy in directions if (x+dx, y+dy) not in self.game.map.walls]
    
    def build_graph(self):
        for y in range(self.game.map.rows):
            for x in range(self.game.map.cols):
                if self.game.map.mini_map[y][x] == 0:
                    self.graph[(x,y)] = self.graph.get((x,y), []) + self.get_next_nodes(x,y)

