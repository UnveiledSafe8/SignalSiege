from backend.game_scripts import main

game = main.create_game("easy", 5, 5, True)
data = None
print(str(game))
if game.is_Ai_turn():
    main.make_ai_move(game)
    print(str(game))
while True:
    if data:
        game = main.restore_game_from_data(data)
    main.make_player_move(game, input("Move: "))
    print(str(game))
    main.make_ai_move(game)
    print(str(game))
    if (main.is_game_over(game)):
        print("GAME OVER")
        break
    data = main.get_game_data(game)
    print(data)