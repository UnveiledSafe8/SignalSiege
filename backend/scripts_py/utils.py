from backend.scripts_py import node
from collections import deque
import random
def generateMap(height: int, width: int, full: bool = True):
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

def randomize_color(colors):
    chosen = []
    for _ in range(len(colors)):
        choice = random.choice([color for color in colors if color not in chosen])
        chosen.append(choice)
    return chosen

def compute_komi(bot_difficulty, height, width):
    bot_difficulty_scale = {
        "easy": 0.7,
        "medium": 1.0,
        "hard": 1.2,
        "very hard": 1.4,
        "insane": 1.8
    }

    if bot_difficulty not in bot_difficulty_scale:
        return None
    
    komi = 6.5 * bot_difficulty_scale[bot_difficulty] * (height*width / 361)
    return round(komi * 2) / 2

def group_has_liberties(graph, start_node, player):
    visited = {start_node.id}
    queue = deque([start_node])
    while queue:
        curr = queue.popleft()
        for nbr_ID in curr.nbrs:
            nbr = graph[nbr_ID]
            if nbr_ID not in visited and nbr.router_owner == player:
                queue.append(nbr)
                visited.add(nbr_ID)
            elif not nbr.router_owner and nbr_ID not in visited:
                return True
    return False

def is_group_capturable(graph, start_node, player):
    return not group_has_liberties(graph, start_node, player.opponent)

def destroy_territory_routers(graph, start_node):
    opponent = start_node.router_owner
    queue = deque([start_node])
    start_node.destroyed()
    while queue:
        curr_node = queue.popleft()
        for nbr_ID in curr_node.nbrs:
            nbr_node = graph[nbr_ID]
            if nbr_node.router_owner == opponent:
                queue.append(nbr_node)
                nbr_node.destroyed()

def update_territory_control(graph, start_node):
    queue = deque([start_node])
    visited = {start_node.id}
    controlled = True if start_node.controlled else False
    routers_owners_found = set()

    while queue:
        curr_node = queue.popleft()
        for nbr_ID in curr_node.nbrs:
            if nbr_ID not in visited:
                nbr_node = graph[nbr_ID]
                if nbr_node.router_owner:
                    routers_owners_found.add(nbr_node.router_owner)
                else:
                    visited.add(nbr_ID)
                    queue.append(nbr_node)
    if controlled and len(routers_owners_found) > 1:
        for node_ID in visited:
            graph[node_ID].uncapture()
    elif not controlled and len(routers_owners_found) == 1:
        for node_ID in visited:
            graph[node_ID].capture(next(iter(routers_owners_found)), False)

def capture_territory(graph, start_node):
    destroy_territory_routers(graph, start_node)
    update_territory_control(graph, start_node)

def valid_placement(node_ID, graph, player):
    nde = graph[node_ID]
    return not nde.router_owner and (group_has_liberties(graph, nde, player) or is_group_capturable(graph, nde, player))

def print_board(graph):
    game_board = []
    for nde_ID in graph:
        nde = graph[nde_ID]
        y,x = nde_ID.split(".")
        if int(y) >= len(game_board):
            game_board.append(list())
        if nde.router_owner:
            char = nde.router_owner.color[0:1]
        elif nde.controlled:
            char = "+"
        else:
            char = "."
        game_board[int(y)].append(char)
    col_label = " "
    for col_index in range(len(game_board[0])):
        col_label += " " + str(col_index)
    print(col_label)
    row_index = 0
    for row in game_board:
        print(str(row_index) + " " + " ".join(row))
        row_index += 1

def print_score(players):
    string = ""
    for player in players:
        string += f"{player.color}: {player.score} | "
    print(string[:-3])