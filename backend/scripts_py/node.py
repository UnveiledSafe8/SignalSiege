class Node:
    def __init__(self, node_id: str, router_owner = None):
        self.id = node_id
        self.nbrs = set()
        self.router_owner = router_owner
        self.controlled = router_owner

    def capture(self, player, router_bool: bool):
        if router_bool:
            self.router_owner = player
            self.controlled = player
        else:
            self.controlled = player
        player.score += 1

    def uncapture(self):
        controller = self.controlled
        controller.score -= 1
        self.controlled = None

    def destroyed(self, controller=None):
        self.router_owner = None
        self.controlled.score -= 1
        self.controlled = controller
        if controller:
            self.capture(controller, False)