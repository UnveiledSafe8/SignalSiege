from collections import deque, defaultdict
from typing import Dict, Literal
import random

from backend.scripts_py import node, player

def generate_map(height: int, width: int, full: bool = True) -> Dict[str, node.Node]:
    """
    Generate a rectangular grid graph where each node is connected to its adjacent nodes.

    Args:
        height (int): Number of rows.
        width (int): Number of columns.
        full (bool): Placeholder parameter for future use.

    Returns:
        Dict[str, node.Node]: A dictionary of nodes indexed by their ID.
    """

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

def randomize_color(colors: set) -> list:
    """
    Return a randomized list of unique colors.

    Args:
        colors (set[str]): Set of unique color strings.

    Returns:
        list[str]: List of shuffled colors.
    """

    return random.sample(colors, len(colors))

def compute_komi(bot_difficulty: Literal["easy", "medium", "hard", "very hard", "insane"], height: int, width: int) -> float | None:
    """
    Compute the komi (compensation points) based on board size and bot difficulty.

    Args:
        bot_difficulty (Literal): Difficulty level of the bot.
        height (int): Board height.
        width (int): Board width.

    Returns:
        float | None: Komi value, or None if difficulty is invalid.
    """

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

def group_has_liberties(graph: Dict[str, node.Node], start_node: node.Node, controller: player.Player) -> bool:
    """
    Determine whether a group of connected routers has any adjacent empty spaces.

    Args:
        graph (Dict[str, node.Node]): Game board graph.
        start_node (node.Node): Starting node of the group.
        controller (player.Player): Controller of the group.

    Returns:
        bool: True if the group has at least one liberty.
    """

    visited = {start_node.id}
    queue = deque([start_node])
    while queue:
        curr = queue.popleft()
        for nbr_id in curr.nbrs:
            nbr = graph[nbr_id]
            if nbr_id not in visited and nbr.router_owner == controller:
                queue.append(nbr)
                visited.add(nbr_id)
            elif not nbr.router_owner and nbr_id not in visited:
                return True
    return False

def is_group_capturable(graph: Dict[str, node.Node], start_node: node.Node, attacker: player.Player) -> bool:
    """
    Check if the opponent's group starting from a node can be captured.

    Args:
        graph (Dict[str, node.Node]): Game board graph.
        start (node.Node): Starting node of opponent's group.
        attacker (player.Player): Attacking player.

    Returns:
        bool: True if the group can be captured.
    """

    return not group_has_liberties(graph, start_node, attacker.opponent)

def destroy_territory_routers(graph: Dict[str, node.Node], start_node: node.Node) -> None:
    """
    Recursively destroy all routers in a connected group starting from the given node.

    Args:
        graph (Dict[str, node.Node]): Game board graph.
        start (node.Node): Starting node of the territory.
    """

    opponent = start_node.router_owner
    queue = deque([start_node])
    start_node.destroy()
    while queue:
        curr_node = queue.popleft()
        for nbr_id in curr_node.nbrs:
            nbr_node = graph[nbr_id]
            if nbr_node.router_owner == opponent:
                queue.append(nbr_node)
                nbr_node.destroy()

def update_territory_control(graph: Dict[str, node.Node], start_node: node.Node) -> None: #known bug where placing in a corner results in the whole board being conquered
    """
    Reevaluate and assign control over a territory area.

    Args:
        graph (Dict[str, node.Node]): Game board graph.
        start (node.Node): Starting node of the region to evaluate.
    """

    queue = deque([start_node])
    visited = {start_node.id}
    controlled = True if start_node.controlled else False
    routers_owners_found = set()
    potential_border = defaultdict(int)

    while queue:
        curr_node = queue.popleft()
        for nbr_id in curr_node.nbrs:
            if nbr_id not in visited:
                nbr_node = graph[nbr_id]
                if nbr_node.router_owner:
                    routers_owners_found.add(nbr_node.router_owner)
                    potential_border[nbr_node] += 1
                else:
                    visited.add(nbr_id)
                    queue.append(nbr_node)
    if controlled and len(routers_owners_found) > 1:
        for node_id in visited:
            graph[node_id].uncapture()
    elif not controlled and len(routers_owners_found) == 1 and max(potential_border.values()) < 3:
        for node_id in visited:
            graph[node_id].capture(next(iter(routers_owners_found)), False)

def capture_territory(graph: Dict[str, node.Node], start_node: node.Node) -> None:
    """
    Capture a territory by destroying opponent routers and updating control.

    Args:
        graph (Dict[str, node.Node]): Game board graph.
        start (node.Node): Starting node of the capture.
    """

    destroy_territory_routers(graph, start_node)
    update_territory_control(graph, start_node)

def valid_placement(node_id: str, graph: Dict[str, node.Node], curr_player: player.Player) -> bool:
    """
    Check if placing a router at a node is a legal move.

    Args:
        node_id (str): Node ID.
        graph (Dict[str, node.Node]): Game board graph.
        curr_player (player.Player): Player making the move.

    Returns:
        bool: True if the placement is valid.
    """

    nde = graph[node_id]
    return not nde.router_owner and (group_has_liberties(graph, nde, curr_player) or is_group_capturable(graph, nde, curr_player))

def print_board(graph: Dict[str, node.Node]) -> None:
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

def print_score(players) -> None:
    string = ""
    for player in players:
        string += f"{player.color}: {player.score} | "
    print(string[:-3])