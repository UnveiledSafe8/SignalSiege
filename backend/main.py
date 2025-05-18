from backend.scripts_py import utils, game_state, node, player, AI
def main(height, width, full = True):
    colors = {"Black", "White"}
    colors = utils.randomize_color(colors)
    players = {colors[0]: player.Player(colors[0]), colors[1]: player.Player(colors[1])}
    ai_player = players[colors[1]]
    ai_controller = AI.AI(ai_player, "easy")
    human_player = players[colors[0]]
    human_player.opponent = ai_player
    ai_player.opponent = human_player
    graph = utils.generateMap(height, width, full)
    passes = 0
    komi = utils.compute_komi("easy", height, width)
    players["White"].score += komi
    while passes < 2:
        curr_player = players[game_state.get_player_turn()]
        valid_move_made = False
        while not valid_move_made:
            if curr_player == human_player:
                move = input(f"Move({human_player.color}): ")
                if move == "pass":
                    passes += 1
                    game_state.take_turn(human_player)
                    valid_move_made = True
                else:
                    passes = 0
                    valid_move_made = game_state.place_router(graph, curr_player, move)
            else:
                ai_move = ai_controller.AI_move(graph)
                if ai_move == "pass":
                    passes += 1
                    game_state.take_turn(ai_player)
                    valid_move_made = True
                else:
                    passes = 0
                    game_state.place_router(graph, curr_player, ai_move)
                    valid_move_made = True
        utils.print_board(graph)
        utils.print_score([human_player, ai_player])
main(5, 5, True)
print("GAME ENDED")