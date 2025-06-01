from backend.scripts_py import main

game = main.create_game("1", "easy", 10, 10, True)
print(str(game))
while True:
    main.make_player_move(main.get_game("1"), input("Move: "))
    print(str(game))
    main.make_ai_move(game)
    print(str(game))
    if (main.is_game_over(game)):
        print("GAME OVER")
        break