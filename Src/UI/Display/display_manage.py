import UI.Display.display_algo as dp_algo
import UI.Display.display_cost as dp_cost
import UI.Display.display_level as dp_lv
import UI.Display.display_moves as dp_moves

class DisplayManager:
    def __init__(self, console):
        self.algo = dp_algo.DisplayAlgo(console)
        self.level = dp_lv.DisplayLevel(console)
        self.costs = dp_cost.DisplayCost(console)
        self.moves = dp_moves.DisplayMoves(console)

    def draw_all(self, screen):
        self.algo.draw(screen)
        self.level.draw(screen)
        self.costs.draw(screen)
        self.moves.draw(screen)
