class Node:
    def __init__(self, node_id: str):
        self.id = node_id
        self.nbrs = set()