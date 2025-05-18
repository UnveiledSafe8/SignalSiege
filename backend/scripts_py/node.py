from backend.scripts_py import player

class Node:
    """
    Represents a node in the game graph.

    Args:
        node_id (str): Unique identifier for the node.
        router_owner (Player, optional): Player who owns the router at this node. Defaults to None.

    Attributes:
        id (str): Unique identifier for the node.
        nbrs (set[str]): Set of neighboring node ids.
        router_owner (Player | None): Player who owns the router at this node, if any.
        controlled (Player | None): Player who currently controls this node, if any.

    Public Methods:
        capture(player, router_bool=False): Control the node for a player, optionally also placing a router.
        uncapture(): Remove control of the node from its current controlling player.
        destroy(): Destroy the node, removing control and router ownership.
    """

    def __init__(self, node_id: str, router_owner: player.Player = None):
        """
        Initializes a Node instance.

        Args:
            node_id (str): Unique identifier for the node.
            router_owner (Player, optional): Player who owns the router at this node, if any. Defaults to None.
        """
        
        self.id = node_id
        self.nbrs = set()
        self.router_owner = router_owner
        self.controlled = router_owner

    def capture(self, player: player.Player, router_bool: bool = False) -> None:
        """
        Captures the node for a given player.

        Args:
            player (Player): The player capturing the node.
            router_bool (bool, optional): Whether the capture includes placing a router. Defaults to False.

        Side Effects:
            Updates router_owner and controlled attributes accordingly.
            Increments the player's score by 1.
        """

        if self.controlled is not None:
            raise ValueError(f"Cannot capture node '{self.id}' because it is already controlled by {self.controlled}.")
         
        if router_bool:
            self.router_owner = player
        self.controlled = player
        player.score += 1

    def uncapture(self) -> None:
        """
        Removes control of the node from its current controlling player.

        Side Effects:
            Decrements the current controller's score by 1.
            Sets controlled to None.
        """

        if self.controlled is None:
            raise ValueError(f"Cannot uncapture node '{self.id}' because it is not controlled.")

        controller = self.controlled
        controller.score -= 1
        self.controlled = None

    def destroy(self) -> None:
        """
        Destroys the node, removing any control and router ownership.

        Side Effects:
            Decrements the current controller's score by 1.
            Sets controlled and router_owner to None.
        """

        if self.controlled is None:
            raise ValueError(f"Cannot destroy node '{self.id}' because it is not controlled.")

        self.controlled.score -= 1
        self.controlled = None
        self.router_owner = None