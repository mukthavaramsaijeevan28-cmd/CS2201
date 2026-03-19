import heapq
import csv
def dijkstra(graph, start, goal):
    # Priority queue: (distance, current_node, path)
    pq = [(0, start, [start])]
    visited = set()

    while pq:
        (cost, node, path) = heapq.heappop(pq)
        
        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return cost, path

        for neighbor, weight in graph.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return float("inf"), []

def load_graph_from_csv(path):
    graph = {}
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Expected columns: source|Origin, destination|Destination, distance|Distance
        for row in reader:
            u = row.get('source') or row.get('Source') or row.get('Origin') or row.get('origin')
            v = row.get('destination') or row.get('Destination') or row.get('Destination') or row.get('destination')
            d = row.get('distance') or row.get('Distance')
            if not u or not v or not d:
                continue
            try:
                w = float(d)
            except ValueError:
                continue
            u = u.strip(); v = v.strip()
            graph.setdefault(u, {})[v] = w
    return graph

# Ensure graph is undirected: if u->v exists with weight w, also make v->u = w

def make_undirected(graph):
    undirected = {}
    for u, neighbors in graph.items():
        undirected.setdefault(u, {})
        for v, w in neighbors.items():
            if v not in undirected:
                undirected[v] = {}
            if undirected[u].get(v, float('inf')) > w:
                undirected[u][v] = w
            if undirected[v].get(u, float('inf')) > w:
                undirected[v][u] = w
    return undirected

csv_path = 'roads.csv'  # change this to your CSV path if needed
india_roads = make_undirected(load_graph_from_csv(csv_path))

print("Available cities:", ", ".join(sorted(india_roads.keys())))

source = input("Enter source city: ").strip()
destination = input("Enter destination city: ").strip()

if source not in india_roads or destination not in india_roads:
    print("Error: source and destination must be in the listed cities.")
else:
    dist, route = dijkstra(india_roads, source, destination)
    if dist == float('inf'):
        print(f"No path found between {source} and {destination}.")
    else:
        print(f"Shortest Distance: {dist} km\nRoute: {' -> '.join(route)}")
    