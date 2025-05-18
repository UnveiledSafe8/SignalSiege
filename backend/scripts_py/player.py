class Player:
    """
    Represents a player in the game.

    Args:
        color (str): The color representing the player.
        score (int, optional): The initial score of the player. Defaults to 0.

    Attributes:
        color (str): The player's color.
        score (int): The player's current score.
        opponent (Player | None): The opposing player, if assigned.
    
    Public Methods:
        None
    """

    def __init__(self, color: str, score: int = 0):
        """
        Initializes a Player instance.

        Args:
            color (str): The color representing the player.
            score (int, optional): The initial score of the player. Defaults to 0.
        """
        
        self.color = color
        self.score = score
        self.opponent = None