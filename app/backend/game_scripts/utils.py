from typing import Dict, Literal
import random

from backend.game_scripts import node, constants

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
        "insane": 1.8,
        "self": 1
    }

    if bot_difficulty not in bot_difficulty_scale:
        return None
    
    komi = constants.base_komi * bot_difficulty_scale[bot_difficulty] * (height*width / 361)
    return round(komi * 2) / 2