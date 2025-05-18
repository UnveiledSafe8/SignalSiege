import random
from typing import Literal, Dict

from backend.scripts_py import game_state, player, node

class AI:
    """
    AI agent that selects and plays moves based on a specified difficulty level.

    Args:
        player (Player): The player object representing this AI's side.
        difficulty (Literal["easy", "medium", "hard", "very hard", "insane"]): Difficulty level of the AI.

    Attributes:
        player (Player): The player instance the AI controls.
        color (str): The color of the AI player.
        difficulty (str): The difficulty level of this AI.

    Public Methods:
        AI_move(graph): Chooses and returns a move based on the current difficulty level.
    """

    def __init__(self, player: player.Player, difficulty: Literal["easy", "medium", "hard", "very hard", "insane"]) -> None:
        """
        Initializes the AI player with a specific difficulty level.
        
        Args:
            player (Player): The player object this AI will control.
            difficulty (Literal["easy", "medium", "hard", "very hard", "insane"]): The difficulty level of the AI.
        """

        self.player = player
        self.color = player.color
        self.difficulty = difficulty
    
    def AI_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Chooses a move based on the AI difficulty level.
        
        Args:
            graph (dict): The game board represented as a node graph.
        
        Returns:
            str: The ID of the selected node, or "pass".
        """

        bot_difficulty_moves = {
        "easy": self._easy_move,
        "medium": self._medium_move,
        "hard": self._hard_move,
        "very hard": self._very_hard_move,
        "insane": self._insane_move
        }

        if self.difficulty not in bot_difficulty_moves:
            raise ValueError(f"Invalid AI difficulty level '{self.difficulty}'. Choose from: {', '.join(bot_difficulty_moves)}.")
        
        return bot_difficulty_moves[self.difficulty](graph)
        
    
    def _easy_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Selects a random valid move from the available ones (easy AI).
        
        Args:
            graph (dict): The game board graph.
        
        Returns:
            str: The ID of the randomly chosen node, or "pass".
        """

        moves = game_state.get_possible_moves(graph, self.player)
        return random.choice(list(moves)) if moves else "pass"

    def _medium_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Medium difficulty move logic placeholder.

        Currently, this method always returns "pass". Intended to implement
        a basic heuristic strategy for the medium difficulty level.

        Args:
            graph (dict): The game board graph.

        Returns:
            str: The move chosen by the medium difficulty AI.
        """
        
        return "pass"
    
    def _hard_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Hard difficulty move logic placeholder.

        Currently, this method always returns "pass". Intended to implement
        a more advanced strategy involving deeper analysis of the game state.

        Args:
            graph (dict): The game board graph.

        Returns:
            str: The move chosen by the hard difficulty AI.
        """
        
        return "pass"
    
    def _very_hard_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Very hard difficulty move logic placeholder.

        Currently, this method always returns "pass". Intended to implement
        complex strategic decision-making to challenge advanced players.

        Args:
            graph (dict): The game board graph.

        Returns:
            str: The move chosen by the very hard difficulty AI.
        """
         
        return "pass"
    
    def _insane_move(self, graph: Dict[str, node.Node]) -> str:
        """
        Insane difficulty move logic placeholder.

        Currently, this method always returns "pass". Intended to implement
        the most challenging AI behavior, possibly using machine learning or
        exhaustive search algorithms.

        Args:
            graph (dict): The game board graph.

        Returns:
            str: The move chosen by the insane difficulty AI.
        """

        return "pass"