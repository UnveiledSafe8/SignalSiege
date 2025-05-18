from typing import Literal, Dict

from backend.scripts_py import utils, player, node

turns = {"Black": 0, "White": 0, "Total": 0}

def take_turn(curr_player: player.Player) -> None:
    """
    Increments the turn count for the given player and the total turn count.

    Args:
        curr_player (Player): The player who just made a move.
    """

    turns[curr_player.color] += 1
    turns["Total"] += 1

def get_player_turn() -> Literal["White", "Black"]:
    """
    Returns the color of the player whose turn it is based on the turn count.

    Returns:
        Literal["White", "Black"]: The player color for the current turn.
    """
     
    return "Black" if turns["Total"] % 2 == 0 else "White"

def get_possible_moves(graph: Dict[str, node.Node], curr_player: player.Player) -> set[str]:
    """
    Computes the set of possible valid moves for the given player.

    Args:
        graph (dict[str, Node]): The game board graph.
        curr_player (Player): The player to evaluate moves for.

    Returns:
        set[str]: A set of node IDs representing valid move locations.
    """

    return {node_id for node_id in graph if utils.valid_placement(node_id, graph, curr_player)}

def place_router(graph: Dict[str, node.Node], curr_player: player.Player, node_id: str) -> bool:
    """
    Attempts to place a router on the specified node for the player.

    If the placement is valid:
        - Uncaptures the node if controlled.
        - Captures the node and places a router.
        - Updates control of neighboring nodes.
        - Advances the turn.

    Args:
        graph (dict[str, Node]): The game board graph.
        curr_player (Player): The player placing the router.
        node_id (str): The ID of the node to place the router on.

    Returns:
        bool: True if the router was successfully placed, False otherwise.
    """

    if node_id not in graph or not utils.valid_placement(node_id, graph, curr_player):
        return False

    target_node = graph[node_id]
    if target_node.controlled:
        target_node.uncapture()
    target_node.capture(curr_player, True)

    for nbr_id in target_node.nbrs:
        nbr = graph[nbr_id]
        if not nbr.router_owner and nbr.controlled != curr_player:
            utils.update_territory_control(graph, nbr)
        elif nbr.router_owner == curr_player.opponent and utils.is_group_capturable(graph, nbr, curr_player):
            utils.capture_territory(graph, nbr)

    take_turn(curr_player)
    return True