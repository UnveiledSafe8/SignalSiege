from collections import deque
from backend.scripts_py import utils
turns = {"Black": 0, "White": 0, "Total": 0}

def take_turn(player):
    turns[player.color] += 1
    turns["Total"] += 1

def get_player_turn():
    return "Black" if turns["Total"] % 2 == 0 else "White"

def get_possible_moves(graph: dict, player):
    moves = set()
    directions = ((1,0), (-1,0), (0,1), (0,-1))
    for cell in graph.values():
        no_router = not cell.router_owner
        not_suicidal = False
        for dx, dy in directions:
            y_str, x_str = cell.id.split(".")
            fx, fy = int(x_str) + dx, int(y_str) + dy
            nbr_ID = f"{fy}.{fx}"
            if nbr_ID in graph and ((not graph[nbr_ID].router_owner) or graph[nbr_ID].router_owner == player):
                not_suicidal = True
                break
        if no_router and not_suicidal:
            moves.add(cell.id)
    return moves

def place_router(graph: dict, player, node_ID) -> bool:
    if node_ID not in graph or not utils.valid_placement(node_ID, graph, player):
        return False

    placed_node = graph[node_ID]
    if placed_node.controlled:
        placed_node.uncapture()
    placed_node.capture(player, True)

    for nbr_ID in placed_node.nbrs:
        nbr = graph[nbr_ID]
        if not nbr.router_owner and nbr.controlled != player:
            utils.update_territory_control(graph, nbr)
        elif nbr.router_owner == player.opponent and utils.is_group_capturable(graph, nbr, player):
            utils.capture_territory(graph, nbr)

    take_turn(player)
    return True