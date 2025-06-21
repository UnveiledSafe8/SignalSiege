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

    def __init__(self, node_id: str = "0.0", router_owner: str = None, nbrs: set[str] = None):
        """
        Initializes a Node instance.

        Args:
            node_id (str): Unique identifier for the node.
            router_owner (Player, optional): Player who owns the router at this node, if any. Defaults to None.
        """
        
        self.id = node_id
        self.nbrs = nbrs if nbrs else set()
        self.router_owner = router_owner
        self.controlled = router_owner
    
    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the node for debugging.

        Returns:
            str: String summarizing the node's ID, controller, and router owner.
        """
        return f"<Node {self.id} | Controlled: {self.controlled} | Router: {self.router_owner}>"
    
    def to_dict(self):
        return {"node_id": self.id, "nbr_ids": list(self.nbrs), "router_owner": self.router_owner, "controlled": self.controlled}
    
    def from_dict(self, dict_data):
        self.id = dict_data["node_id"]
        self.nbrs = set(dict_data["nbr_ids"])
        self.router_owner = dict_data["router_owner"]
        self.controlled = dict_data["controlled"]
        return self
    
    def has_router(self) -> bool:
        """
        Checks whether the node currently has a router installed.

        Returns:
            bool: True if a router is present (i.e., router_owner is not None), False otherwise.
        """
        
        return self.router_owner is not None

    def capture(self, player: str, router_bool: bool = False) -> None:
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

    def uncapture(self) -> None:
        """
        Removes control of the node from its current controlling player.

        Side Effects:
            Decrements the current controller's score by 1.
            Sets controlled to None.
        """

        if self.controlled is None:
            raise ValueError(f"Cannot uncapture node '{self.id}' because it is not controlled.")

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

        self.controlled = None
        self.router_owner = None