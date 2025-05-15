import node
import random
def generateMap(height: int, width: int, full: bool = False):
    graph = {}
    directions = ((1,0), (-1,0), (0,1), (0,-1))
    for row in range(height):
        for col in range(width):
            new_node = node.Node(f"{row}.{col}")
            graph[new_node.id] = new_node
            for d_row, d_col in directions:
                nbr_row, nbr_col = d_row + row, d_col + col
                if 0 <= nbr_row < height and 0 <= nbr_col < width:
                    nbr_node_id = f"{nbr_row}.{nbr_col}"
                    new_node.nbrs.add(nbr_node_id)
    return graph
graph = generateMap(2, 3)
for nde in graph:
    print(str(nde) + ":" + str(graph[nde].nbrs))