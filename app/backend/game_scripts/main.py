from typing import Literal
import random

from backend.game_scripts import game_state

def create_game(difficulty: Literal["easy", "medium", "hard", "very hard", "insane", "self", "random"], height: int, width: int, full: bool = True) -> game_state.GameState:
    """
    Initializes and stores a new GameState instance.

    Args:
        difficulty Literal["easy", "medium", "hard", "very hard", "insane", "self"]: AI difficulty level.
        height (int): Board height (rows).
        width (int): Board width (columns).
        full (bool): Whether to use a fully connected board.

    Returns:
        GameState: The initialized game instance.
    """
    if difficulty == "random":
        difficulty = random.choice(["easy", "medium", "hard", "very hard", "insane"])

    game = game_state.GameState(difficulty, height, width, full)

    return game

def make_player_move(game: game_state.GameState, move: str) -> bool:
    """
    Handles a player's move.

    Args:
        game (GameState): The current game object.
        move (str): The move string (e.g., "3.4" or "pass").

    Returns:
        bool: True if the move was successfully made, else False.
    """

    if move == "pass":
        game.take_turn()
        game.passes += 1
        return True
    else:
        val = game.place_router(move)
        if val:
            game.passes = 0
        return val
    
def make_ai_move(game: game_state.GameState) -> bool:
    """
    Processes the AI move if it's the AI's turn.

    Args:
        game (GameState): The game object.

    Returns:
        bool: True if the AI made a move, else False.
    """

    if game.is_Ai_turn():
        ai_move = game.ai_move()
        if ai_move == "pass":
            game.take_turn()
            game.passes += 1
            return True
        else:
            val = game.place_router(ai_move)
            if val:
                game.passes = 0
            return val

def is_game_over(game: game_state.GameState) -> bool:
    """
    Determines if the game should end (e.g., 2 passes in a row).

    Args:
        game (GameState): The game instance.

    Returns:
        bool: True if the game is over, else False.
    """

    return game.passes >= 2

def get_game_data(game):
    return game.to_dict()

def restore_game_from_data(dict_data):
    return game_state.GameState().from_dict(dict_data)