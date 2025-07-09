import UI.Display.display_algo as dp_algo
import UI.Display.display_costs as dp_cost
import UI.Display.display_level as dp_lv
import UI.Display.display_moves as dp_moves
import UI.Display.display_memory_peaked as dp_memory_peaked
import UI.Display.display_time_taken as dp_time_taken
import UI.Display.display_expanded_nodes as dp_expanded_nodes

class DisplayManager:
    def __init__(self, console):
        self.algo = dp_algo.DisplayAlgo(console)
        self.level = dp_lv.DisplayLevel(console)
        self.costs = dp_cost.DisplayCosts(console)
        self.moves = dp_moves.DisplayMoves(console)
        self.memory_peaked = dp_memory_peaked.DisplayMemoryPeaked(console)
        self.time_taken = dp_time_taken.DisplayTimeTaken(console)
        self.expanded_nodes = dp_expanded_nodes.DisplayExpandedNodes(console)

    def draw_all(self, screen):
        self.algo.draw(screen)
        self.level.draw(screen)
        self.costs.draw(screen)
        self.moves.draw(screen)
        self.memory_peaked.draw(screen)
        self.time_taken.draw(screen)    
        self.expanded_nodes.draw(screen)
