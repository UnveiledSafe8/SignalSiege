import random
from backend.scripts_py import game_state
class AI:
    def __init__(self, player):
        self.player = player
        self.color = player.color
    
    def AI_move(self, graph):
        moves = game_state.get_possible_moves(graph, self.color)
        move = "pass"
        if moves:
            move = random.choice(list(moves))
        return move
