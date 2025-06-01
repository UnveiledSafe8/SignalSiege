from typing import Literal, Optional
from collections import defaultdict, deque
import copy

from backend.scripts_py import utils, player, node, constants, AI

class GameState:
    """
    Manages the complete game state, including players, AI behavior, board setup,
    and the logic for placing routers, capturing territory, and determining valid moves.

    Args:
        difficulty (str): AI difficulty level. Can be "easy", "medium", "hard", "very hard", "insane", or "self".
        height (int): Height of the game board (number of rows).
        width (int): Width of the game board (number of columns).
        full (bool, optional): Whether to generate a fully connected board graph. Defaults to True.

    Attributes:
        players (dict[str, Player]): Dictionary of players by color.
        ai_player (Optional[Player]): The AI player, if any.
        ai_controller (Optional[AI]): The AI controller logic instance, if any.
        komi (float): Komi score bonus given to the second player to balance advantage.
        graph (dict[str, Node]): The game board represented as a graph of nodes.
        _turns (dict[str, int]): Internal turn counters.

    Public Methods:
        - get_player_turn() -> Player: Returns the current player whose turn it is.
        - is_Ai_turn() -> bool: Checks whether it's currently the AI's turn.
        - ai_move() -> Optional[str]: Executes an AI move and returns the chosen node ID.
        - place_router(node_id: str) -> bool: Attempts to place a router at the given node.
        - get_possible_moves() -> set[str]: Returns the set of valid node IDs for placement.
        - valid_placement(node_id: str) -> bool: Determines if a router can be placed at the node.
    """

    def __init__(self, difficulty: Literal["easy", "medium", "hard", "very hard", "insane", "self"], height: int = 5, width: int = 5, full: bool = True):
        """
        Initializes the game state with players, AI, board graph, and komi scoring.

        Args:
            difficulty (str): Game difficulty (e.g., "easy", "medium", "hard", "very hard", "self").
            height (int): Height of the board.
            width (int): Width of the board.
            full (bool, optional): Whether to generate a fully connected board. Defaults to True.
        """

        self._turns = {"Total": 0}
        for color in constants.colors:
            self._turns[color] = 0

        colors = utils.randomize_color(constants.colors)
        self.players = {colors[0]: player.Player(colors[0]), colors[1]: player.Player(colors[1])}
        self.ai_players = []
        self.ai_controllers = []

        self.players[colors[0]].set_opponent(self.players[colors[1]])
        self.players[colors[1]].set_opponent(self.players[colors[0]])

        if difficulty in ["easy", "medium", "hard", "very hard", "insane"]:
            self.ai_controllers.append(AI.AI(self.players[colors[1]], difficulty))
            self.ai_players.append(self.players[colors[1]])
        elif difficulty == "self":
            pass
        else:
            raise ValueError(f"Invalid difficulty inputted")
        
        self.difficulty = difficulty

        self.komi = utils.compute_komi(difficulty, height, width)
        self.players[constants.colors[1]].increment_score(self.komi)

        self.graph = utils.generate_map(height, width, full)
        self.height = height
        self.width = width

        self.passes = 0
    
    def __str__(self):
        """
        Returns a string representation of the board and current scores.

        Returns:
            str: Formatted board and score state.
        """

        game_board = []

        for node_id in self.graph:
            y, x = map(int, node_id.split("."))
            while y >= len(game_board):
                game_board.append([])
            nde = self.graph[node_id]
            if nde.router_owner:
                char = nde.router_owner.color[0].upper()
            elif nde.controlled:
                char = nde.controlled.color[0].lower()
            else:
                char = "."
            game_board[y].append(char)
        col_labels = "   " + " ".join(str(i) for i in range(len(game_board[0])))
        board_rows = []
        for row_idx, row in enumerate(game_board):
            board_rows.append(f"{row_idx:<2} " + " ".join(row))
        score_line = " | ".join(f"{p.color}: {p.score}" for p in self.players.values())
        return "\n".join([col_labels, *board_rows, "", score_line])
    
    def __deepcopy__(self, memo):
        copied_game = GameState(self.difficulty)
        copied_game.graph = copy.deepcopy(self.graph, memo)
        copied_game._turns = copy.deepcopy(self._turns, memo)
        copied_game.passes = self.passes
        copied_game.komi = self.komi
        copied_game.height = self.height
        copied_game.width = self.width
        copied_game.players = {color: copy.deepcopy(plyer, memo) for color, plyer in self.players.items()}
        copied_game.ai_players = [copied_game.players[ai.color] for ai in self.ai_players]
        copied_game.ai_controllers = [AI.AI(copied_game.players[controller.color], controller.difficulty) for controller in self.ai_controllers]

        return copied_game
    
    
    def get_player_turn(self) -> player.Player:
        """
        Returns the current player based on the turn count.

        Returns:
            player.Player: The player whose turn it is.
        """
     
        return self.players[constants.colors[0]] if self._turns["Total"] % 2 == 0 else self.players[constants.colors[1]]
    
    def is_Ai_turn(self) -> bool:
        """
        Checks if it's currently the AI's turn.

        Returns:
            bool: True if it's the AI's turn, False otherwise.
        """
         
        return self.get_player_turn() in self.ai_players
    
    def ai_move(self) -> Optional[str]:
        """
        Executes and returns the AI's move.

        Returns:
            Optional[str]: The node ID where the AI decides to place, or None.
        """
        if not self.is_Ai_turn():
            raise ValueError(f"Can not resolve the AI's move since it is not the AI's turn")
        
        curr_ai = self.get_player_turn()
        controller = self.ai_controllers[self.ai_players.index(curr_ai)]
        return controller.AI_move(copy.deepcopy(self))
    
    def take_turn(self) -> None:
        """
        Advances the game turn counter for both the current player and total turns.
        """

        self._turns[self.get_player_turn().color] += 1
        self._turns["Total"] += 1
    
    def group_has_liberties(self, start_node: node.Node, controller: player.Player) -> bool:
        """
        Checks if a group of routers controlled by the player has any adjacent empty nodes.

        Args:
            start_node (node.Node): Starting node of the group.
            controller (player.Player): Owner of the group.

        Returns:
            bool: True if the group has at least one liberty, False if fully surrounded.
        """

        visited = {start_node.id}
        queue = deque([start_node])
        while queue:
            curr = queue.popleft()
            for nbr_id in curr.nbrs:
                nbr = self.graph[nbr_id]
                if nbr_id not in visited and nbr.router_owner == controller:
                    queue.append(nbr)
                    visited.add(nbr_id)
                elif not nbr.router_owner and nbr_id not in visited:
                    return True
        return False

    def is_group_capturable(self, start_node: node.Node, attacker: player.Player) -> bool:
        """
        Determines if an opponent group is capturable from the given node.

        Args:
            start_node (node.Node): A node in the opponent's group.
            attacker (player.Player): Player attempting the capture.

        Returns:
            bool: True if the group can be captured, False otherwise.
        """

        return not self.group_has_liberties(start_node, attacker.get_opponent())

    def destroy_territory_routers(self, start_node: node.Node) -> None:
        """
        Destroys all routers in the connected group starting from the given node.

        Args:
            start_node (node.Node): Node to start the destruction from.
        """

        opponent = start_node.router_owner
        queue = deque([start_node])
        start_node.destroy()
        while queue:
            curr_node = queue.popleft()
            for nbr_id in curr_node.nbrs:
                nbr_node = self.graph[nbr_id]
                if nbr_node.router_owner == opponent:
                    queue.append(nbr_node)
                    nbr_node.destroy()

    def update_territory_control(self, start_node: node.Node) -> None:
        """
        Updates the control status of a territory region starting from a node.

        Args:
            start_node (node.Node): Node to evaluate the territory from.
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
                    nbr_node = self.graph[nbr_id]
                    if nbr_node.router_owner:
                        routers_owners_found.add(nbr_node.router_owner)
                        potential_border[nbr_node] += 1
                    else:
                        visited.add(nbr_id)
                        queue.append(nbr_node)
        if controlled and len(routers_owners_found) > 1:
            for node_id in visited:
                self.graph[node_id].uncapture()
        elif not controlled and len(routers_owners_found) == 1 and len(visited) < len(self.graph) - 3:
            for node_id in visited:
                self.graph[node_id].capture(next(iter(routers_owners_found)), False)

    def capture_territory(self, start_node: node.Node) -> None:
        """
        Captures a territory by destroying enemy routers and updating control.

        Args:
            start_node (node.Node): A node in the opponent's group to be captured.
        """

        self.destroy_territory_routers(start_node)
        self.update_territory_control(start_node)
    
    def get_possible_moves(self) -> set[str]:
        """
        Computes all currently valid node placements for the current player.

        Returns:
            Set[str]: Set of node IDs that are valid placements.
        """

        return {node_id for node_id in self.graph if self.valid_placement(node_id)}
    
    def valid_placement(self, node_id: str) -> bool:
        """
        Checks if the current player can legally place a router at the given node.

        Args:
            node_id (str): The node ID to test.

        Returns:
            bool: True if the move is valid, False otherwise.
        """

        nde = self.graph[node_id]
        curr_player = self.get_player_turn()
        return not nde.has_router() and (self.group_has_liberties(nde, curr_player) or self.is_group_capturable(nde, curr_player))
    
    def place_router(self, node_id: str) -> bool:
        """
        Places a router for the current player if the move is valid.

        Args:
            node_id (str): The node ID to place a router on.

        Returns:
            bool: True if placement was successful, False otherwise.
        """

        curr_player = self.get_player_turn()

        if node_id not in self.graph or not self.valid_placement(node_id):
            return False

        target_node = self.graph[node_id]
        if target_node.controlled:
            target_node.uncapture()
        target_node.capture(curr_player, True)

        for nbr_id in target_node.nbrs:
            nbr = self.graph[nbr_id]
            if not nbr.router_owner and nbr.controlled != curr_player:
                self.update_territory_control(nbr)
            elif nbr.router_owner == curr_player.get_opponent() and self.is_group_capturable(nbr, curr_player):
                self.capture_territory(nbr)

        self.take_turn()
        return True
    
    def game_summary(self):
        game_board = []

        for node_id in self.graph:
            y, x = map(int, node_id.split("."))
            while y >= len(game_board):
                game_board.append([])
            nde = self.graph[node_id]
            if nde.router_owner:
                char = nde.router_owner.color[0].upper()
            elif nde.controlled:
                char = nde.controlled.color[0].lower()
            else:
                char = "."
            game_board[y].append(char)
        scores = {p.color: p.score for p in self.players.values()}
        human_players_colors = []
        ai_players_colors = []
        for player in self.players.keys():
            if player not in [ai.color for ai in self.ai_players]:
                human_players_colors.append(player)
            else:
                ai_players_colors.append(player)
        return game_board, scores, self.difficulty, human_players_colors, ai_players_colors