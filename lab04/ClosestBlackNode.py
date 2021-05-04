def load_graph():
    # Load number of nodes and edges
    n, e = input().split()
    n, e = int(n), int(e)

    # Load colors
    # index of colors list are index of nodes -> useful
    colors = []
    for i in range(n):
        colors.append(int(input()))

    # Load edges
    edges = []
    for i in range(e):
        node1, node2 = input().split()
        edges.append((int(node1), int(node2)))

    return n, e, colors, edges


def bfs_search_for_black_node(start_node, colors, neighbors):
    depth = 0
    front = [(start_node, depth)]
    discovered = [start_node]
    visited = []
    while True:

        # If front is empty and black node wasn't found return
        if len(front) == 0:
            return -1, -1

        # Pick closest with lowest index
        candidates = []
        current_node, current_depth = front.pop(0)
        if colors[current_node] == 1:
            candidates.append(current_node)
        for node, depth in front:
            if colors[node] == 1 and depth == current_depth:
                candidates.append(node)
        if len(candidates) != 0:
            return min(candidates), current_depth

        # Get neighbors of current node
        for neighbor in neighbors[current_node]:
            if neighbor not in discovered:
                discovered.append(neighbor)
                front.append((neighbor, current_depth + 1))


if __name__ == "__main__":
    # Load graph data
    n, e, colors, edges = load_graph()

    # Build neighbor dictionary
    neighbors = {}
    for i in range(n):
        neighbors[i] = []
    for edge in edges:
        neighbors[edge[0]].append(edge[1])
        neighbors[edge[1]].append(edge[0])
    for node in neighbors:
        neighbors[node].sort()

    # Iterate through all nodes
    for node in range(n):
        index_of_closest, distance = bfs_search_for_black_node(
            node, colors, neighbors)
        print("{} {}".format(index_of_closest, distance))
