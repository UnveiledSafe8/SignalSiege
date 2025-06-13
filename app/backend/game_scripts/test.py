from backend.game_scripts import main

game = main.create_game("easy", 10, 10, True)
print(str(game))
if game.is_Ai_turn():
    main.make_ai_move(game)
    print(str(game))
while True:
    main.make_player_move(game, input("Move: "))
    print(str(game))
    print(game.to_dict())
    main.make_ai_move(game)
    print(str(game))
    print(game.to_dict())
    if (main.is_game_over(game)):
        print("GAME OVER")
        break