import random
import copy
import math
from typing import Literal, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from backend.game_scripts import game_state

from backend.game_scripts import player, node

class AI(player.Player):
    """
    AI agent that selects and plays moves based on a specified difficulty level.

    Args:
        player (Player): The player object representing this AI's side.
        difficulty (Literal["easy", "medium", "hard", "very_hard", "insane"]): Difficulty level of the AI.

    Attributes:
        player (Player): The player instance the AI controls.
        color (str): The color of the AI player.
        difficulty (str): The difficulty level of this AI.

    Public Methods:
        AI_move(graph): Chooses and returns a move based on the current difficulty level.
    """

    def __init__(self, difficulty: Literal["easy", "medium", "hard", "very_hard", "insane"] = "easy", color: str = None, score: int = 0, opponent: str=None) -> None:
        """
        Initializes the AI player with a specific difficulty level.
        
        Args:
            player (Player): The player object this AI will control.
            difficulty (Literal["easy", "medium", "hard", "very_hard", "insane"]): The difficulty level of the AI.
        """

        self.color = color
        self.score = score
        self._opponent = opponent
        self.difficulty = difficulty

    def to_dict(self):
        return {"color": self.color, "score": self.score, "opponent": self._opponent, "difficulty": self.difficulty}
    
    def from_dict(self, dict_data):
        self.color = dict_data["color"]
        self.score = dict_data["score"]
        self._opponent = dict_data["opponent"]
        self.difficulty = dict_data["difficulty"]
        return self
    
    def AI_move(self, copied_game: "game_state.GameState") -> str:
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
        "very_hard": self._very_hard_move,
        "insane": self._insane_move
        }

        if self.difficulty not in bot_difficulty_moves:
            raise ValueError(f"Invalid AI difficulty level '{self.difficulty}'. Choose from: {', '.join(bot_difficulty_moves)}.")
        
        if (copied_game.players[self._opponent].score < self.score and copied_game.passes > 0):
            return "pass"
        
        return bot_difficulty_moves[self.difficulty](copied_game)  
    
    def _easy_move(self, copied_game: "game_state.GameState") -> str:
        """
        Selects a random valid move from the available ones (easy AI).
        
        Args:
            graph (dict): The game board graph.
        
        Returns:
            str: The ID of the randomly chosen node, or "pass".
        """

        WEIGHT_SCORE_DIFF = 5
        WEIGHT_NEIGHBOR_OWNED = 2
        WEIGHT_NEIGHBOR_ENEMY = -3
        WEIGHT_BORDER = -1

        moves = copied_game.get_possible_moves()
        ranked_moves = []
        for move in moves:
            curr_game = copy.deepcopy(copied_game)
            curr_game.place_router(move)

            player_self = curr_game.players[self.color]

            rank = 5 * (curr_game.height * curr_game.width)

            rank += WEIGHT_SCORE_DIFF * (player_self.score - curr_game.players[player_self.get_opponent()].score)

            y_str, x_str = move.split(".")

            if int(y_str) == curr_game.height - 1 or int(x_str) == curr_game.width - 1:
                rank += WEIGHT_BORDER

            for nbr in curr_game.graph[move].nbrs:
                if curr_game.graph[nbr].router_owner == player_self:
                    rank += WEIGHT_NEIGHBOR_OWNED
                elif curr_game.graph[nbr].router_owner == player_self.get_opponent():
                    rank += WEIGHT_NEIGHBOR_ENEMY

            ranked_moves.append((rank, move))

        if ranked_moves:
            max_rank = max(rank for rank, _ in ranked_moves)
            exp_ranks = [math.exp(rank - max_rank) for rank, _ in ranked_moves]
            total = sum(exp_ranks)

            moves = [move[1] for move in ranked_moves]
            weights = [e/total for e in exp_ranks]

        return random.choices(moves, weights, k=1)[0] if moves else "pass"

    def _medium_move(self, moves) -> str:
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