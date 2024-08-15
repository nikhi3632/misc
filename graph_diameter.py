'''
    The term "longest shortest path" refers to the diameter of a graph. 
    The diameter is the longest distance between any pair of nodes in the graph, 
    where distance is defined as the shortest path between the nodes.
    Shortest Path: The shortest path between two nodes is the path with the 
    minimum number of edges or the least total weight (in weighted graphs).
    Longest Shortest Path: Among all pairs of nodes, the longest of these shortest paths 
    is called the diameter of the graph.
'''

from collections import deque, defaultdict

def bfs(start_node, graph):
    """
    Perform BFS from start_node and return the farthest node and its distance from start_node.
    """
    distances = {node: -1 for node in graph}
    distances[start_node] = 0
    queue = deque([start_node])
    farthest_node = start_node
    max_distance = 0
    while queue:
        node = queue.popleft()
        current_distance = distances[node]
        for neighbor in graph[node]:
            if distances[neighbor] == -1:  # Unvisited
                distances[neighbor] = current_distance + 1
                queue.append(neighbor)
                if distances[neighbor] > max_distance:
                    max_distance = distances[neighbor]
                    farthest_node = neighbor
    return farthest_node, max_distance

def longest_shortest_path(edges):
    """
    Find the diameter of the graph defined by the edges.
    """
    # Build the graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    # arbitrary starting node (e.g., the first node in the graph)
    start_node = next(iter(graph))
    # Perform BFS from the start node to find the farthest node
    farthest_node, _ = bfs(start_node, graph)
    # Perform BFS from the farthest node found to determine the diameter
    _, diameter = bfs(farthest_node, graph)
    # two-pass BFS technique: Graphy theory insight, by performing BFS from an arbitrary node we identify a node that is farthest from the start, and this node is always one end of the longest shortest path.
    return diameter

edges = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6)]
print(f"The diameter of the graph is: {longest_shortest_path(edges)}")
