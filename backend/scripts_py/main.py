from typing import Literal, Optional

from backend.scripts_py import game_state

games = {}

def create_game(game_id: str, difficulty: Literal["easy", "medium", "hard", "very hard", "insane", "self"], height: int, width: int, full: bool = True) -> game_state.GameState:
    """
    Initializes and stores a new GameState instance.

    Args:
        game_id (str): Unique identifier for the game.
        difficulty Literal["easy", "medium", "hard", "very hard", "insane", "self"]: AI difficulty level.
        height (int): Board height (rows).
        width (int): Board width (columns).
        full (bool): Whether to use a fully connected board.

    Returns:
        GameState: The initialized game instance.
    """

    game = game_state.GameState(difficulty, height, width, full)
    games[game_id] = game
    return game

def get_game(game_id: str) -> Optional[game_state.GameState]:
    """
    Retrieves a game instance by its ID.

    Args:
        game_id (str): The game identifier.

    Returns:
        GameState or None: The game object or None if not found.
    """

    return games.get(game_id)

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