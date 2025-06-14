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
        set_opponent(opponent): Assign an opponent to this player.
        get_opponent(): Retrieve the opponent of this player.
        increment_score(amount=1): Increase the player's score.
        decrement_score(amount=1): Decrease the player's score.
    """

    def __init__(self, color: str = None, score: int = 0, opponent: str = None):
        """
        Initializes a Player instance.

        Args:
            color (str): The color representing the player.
            score (int, optional): The initial score of the player. Defaults to 0.
        """
        
        self.color = color
        self.score = score
        self._opponent = opponent
    
    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the player.

        Returns:
            str: A detailed representation with color, score, and opponent info.
        """
         
        return f"Player(color={self.color!r}, score={self.score}, opponent={self._opponent if self._opponent else None!r})"
    
    def __str__(self) -> str:
        """
        Returns a readable string representation of the player.

        Returns:
            str: A simple description of the player and their score.
        """

        return f"Player({self.color}, Score: {self.score})"
    
    def to_dict(self):
        return {"color": self.color, "score": self.score, "opponent": self._opponent}
    
    def from_dict(self, dict_data):
        self.color = dict_data["color"]
        self.score = dict_data["score"]
        self._opponent = dict_data["opponent"]
        return self
    
    def set_opponent(self, opponent: str) -> None:
        """
        Assigns an opponent to this player.

        Args:
            opponent (Player): The opponent to assign.
        """

        self._opponent = opponent
    
    def get_opponent(self) -> str | None:
        """
        Retrieves the opponent of this player.

        Returns:
            Player | None: The assigned opponent, if any.
        """

        return self._opponent

    def increment_score(self, amount: int = 1) -> None:
        """
        Increments the player's score.

        Args:
            amount (int, optional): The amount to increment by. Defaults to 1.
        """
        if amount is None:
            amount = 0

        self.score += amount

    def decrement_score(self, amount: int = 1) -> None:
        """
        Decrements the player's score.

        Args:
            amount (int, optional): The amount to decrement by. Defaults to 1.
        """
        if amount is None:
            amount = 0

        if self.score - amount < 0:
            raise ValueError(f"Player {self.color} score underflow.")
        
        self.score -= amount