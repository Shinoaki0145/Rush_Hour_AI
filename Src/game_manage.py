import pygame
import console
from Cars import *
from board import *
from defs import *
from UI.Display.display_manage import DisplayManager
from UI.Display.display_menu import DisplayMenu
from UI.Button.button_manage import ButtonManager
from UI.Button.button_menu import ButtonMenu
from UI.Popup.popup_manage import GamePopup
from UI import create_3d_text
from utils import *
from Algo import *
from random import choice
from time import time
import tracemalloc, gc
import threading

def load_map(console, map_name):
    clear_valid_matrix()
    new_car_manager = CarManager()
    map_path = ASSET_PATH + "Map/" + map_name + ".txt"
    with open(map_path) as f:
        target_car_x, target_car_y = list(map(int, f.readline().strip().split(',')))
        target_car = MainCar(target_car_x, target_car_y, console.reSize_Image(TARGET_CAR_PATH))
        new_car_manager.add_car(target_car)

        car_count = 0
        for line in f.readlines():
            type, x, y, horizontal, direction = line.strip().split(',')
            if type == 'car':
                car_id = str(choice(range(0, 5)))
            else:
                car_id = str(choice(range(0, 3)))
            new_car_manager.add_car(Car(
                type + str(car_count),
                int(x),
                int(y),
                console.reSize_Image(CAR_PATH + type + "_" + car_id + ".png"),
                int(horizontal),
                direction
            ))
            car_count += 1
    return new_car_manager

class Game:
    def __init__(self):
        pygame.init()
        self.console = console.Console()
        self.console.convertMatrix()

        self.screen = pygame.display.set_mode((self.console.screen_size, self.console.screen_size))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Rush Hour AI Game') 
        self.board = Board(self.console.reSize_Image(BACKGROUND_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

        self.button_manager = ButtonManager(self.console)
        self.display_manager = DisplayManager(self.console)
        self.game_popup = GamePopup(self.console)
        self.game_utils = GameUtils(self.console)

        self.flag_menu = True
        self.button_menu = ButtonMenu(self.console)
        self.display_menu = DisplayMenu(self.console, self.button_menu, self.board.image, self.flag_menu)

        self.map_name = "map1"  # Default map
        self.car_manager = load_map(self.console, self.map_name)

        # Initialize game logic
        self.init_common_game_var()
    
    def init_common_game_var(self):
        self.searched = False
        self.path = []
        self.current_step = 1
        self.moves_count = 0
        self.cost = 0
        self.step_timer = 0
        self.is_moving = False
        self.waiting_for_next_step = False
        self.algorithm_running = False
        self.algorithm_completed = False

    def on_algorithm_complete(self, result_path, algorithm_name):
        """Callback khi thuật toán hoàn thành"""
        self.algorithm_running = False
        self.algorithm_completed = True
        
        if result_path is None or len(result_path) == 0:
            print(f"No solution found with {algorithm_name}")
            current_algorithm = self.game_utils.get_selected_algorithm()
            current_level = self.game_utils.get_current_level()
            fail_count = self.game_utils.check_final_lose_condition(current_algorithm, current_level)

            if fail_count == 4:
                self.game_utils.play_win_music()
                self.game_popup.final_lose.show(current_level)
                self.game_popup.update_type("final_lose")
            else:
                self.game_utils.play_fail_music()
                self.game_popup.lose.show(current_level, current_algorithm)
                self.game_popup.update_type("lose")
        else:
            print(f"Found path with {len(result_path)} states using {algorithm_name}")
            self.path = result_path
            self.searched = True
            self.current_step = 1
            self.step_timer = 0
    
    def run_algorithm_search(self, cars, selected_algo, callback):
        """Chạy thuật toán trong thread riêng"""
        def search_thread():
            try:
                print(f"Starting search with algorithm: {selected_algo}")
                
                simple_cars = []
                for car in cars:
                    simple_cars.append(SimpleCar(car.name, car.length_grid, (car.y, car.x), not car.is_horizontal))
                start = State(simple_cars)

                gc.collect()
                tracemalloc.start()
                begin = time()
                
                if selected_algo == "BFS":
                    self.path, expanded_nodes = bfs(start)
                elif selected_algo == "DFS":
                    self.path, expanded_nodes = dfs(start)
                elif selected_algo == "A STAR":
                    self.path, expanded_nodes = a_star(start)
                elif selected_algo == "UCS":
                    self.path, expanded_nodes = ucs(start)
                else:
                    self.path, expanded_nodes = a_star(start)

                time_taken = round(time() - begin, 4)
                memory_used = round(tracemalloc.get_traced_memory()[1] / (1024 ** 2), 2)
                tracemalloc.stop()

                print(f"Expanded nodes: {expanded_nodes}")
                self.display_manager.expanded_nodes.update_text(f"EXPANDED NODES : {expanded_nodes}")
                print(f"Time taken: {time_taken} seconds.")
                self.display_manager.time_taken.update_text(f"TIME TAKEN : {time_taken} s")
                print(f"Memory peaked: {memory_used} MB.")
                self.display_manager.memory_peaked.update_text(f"MEMORY PEAKED : {memory_used} MB")
                
                callback(self.path, selected_algo)
                
            except Exception as e:
                print(f"Error in algorithm search: {e}")
                callback(None, selected_algo)
        
        search_thread = threading.Thread(target=search_thread, daemon=True)
        search_thread.start()
    
    def game_start(self):
        lv_started = False
        resetting = False
        reset_timer = 0
        game_initialized = False
        
        running = True  
        while running:  
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.game_popup.visible:
                        clicked_popup_button = self.game_popup.check_button_click(mouse_pos)
                        if clicked_popup_button:
                            if not self.flag_menu:
                                if self.game_popup.popup_type == "algorithm":
                                    self.game_utils.handle_algorithm_selection(clicked_popup_button)
                                    
                                    algorithm_display_text = f"ALGORITHM :  {clicked_popup_button}"
                                    self.display_manager.algo.update_text(algorithm_display_text)
                                    
                                    self.game_popup.hide()
                                    
                                    self.init_common_game_var()
                                    
                                elif self.game_popup.popup_type == "win":
                                    next_lv = self.game_utils.handle_win_popup_action(clicked_popup_button, self.game_popup)
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                    self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                    self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")
                                   
                                    if next_lv:
                                        self.map_name = "map" + str(self.game_utils.get_current_level())
                                    self.car_manager = load_map(self.console, self.map_name)
                                    lv_started = False
                                    self.init_common_game_var()

                                elif self.game_popup.popup_type == "lose":    
                                    reset_level = self.game_utils.handle_lose_popup_action(clicked_popup_button, self.game_popup)
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                    self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                    self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")
                                    
                                    if reset_level:
                                        self.car_manager = load_map(self.console, self.map_name)
                                    lv_started = False
                                    self.init_common_game_var()
                                    
                                elif self.game_popup.popup_type == "final_lose":
                                    next_lv = self.game_utils.handle_final_lose_popup_action(clicked_popup_button, self.game_popup)
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                    self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                    self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")
                                   
                                    if next_lv:
                                        self.map_name = "map" + str(self.game_utils.get_current_level())
                                    self.car_manager = load_map(self.console, self.map_name)
                                    lv_started = False
                                    self.init_common_game_var()
                                    
                                elif self.game_popup.popup_type == "final_win":
                                    result = self.game_utils.handle_final_win_popup_action(
                                        clicked_popup_button, 
                                        self.car_manager, 
                                        self.game_popup
                                    )
                                    
                                    if result == "return_to_menu":
                                        self.flag_menu = True
                                        game_initialized = False
                                        
                                        self.init_common_game_var()
                                        
                                        lv_started = False
                                        resetting = False
                                        
                                        self.display_manager.level.update_text("LEVEL :  ")
                                        self.display_manager.moves.update_text("MOVES :  0")
                                        self.display_manager.costs.update_text("COSTS :  0")
                                        self.display_manager.algo.update_text("ALGORITHM :  ")
                                        self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                        self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                        self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")
                                    else:
                                        self.car_manager = result

                                elif self.game_popup.popup_type == "choose_level":
                                    self.car_manager = self.game_utils.handle_choose_level_popup_action(
                                        clicked_popup_button, 
                                        self.car_manager, 
                                        self.game_popup,
                                        self.console, 
                                        load_map
                                    )
                                    
                                    self.map_name = "map" + str(self.game_utils.get_current_level())
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                    self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                    self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")
                                    
                                    self.init_common_game_var()
                                    
                                    lv_started = False
                                    game_initialized = True
                                    
                                elif self.game_popup.popup_type == "info_buttons":
                                    self.game_utils.handle_info_in_game_popup_action(clicked_popup_button, self.game_popup)
                            else:
                                if self.game_popup.popup_type == "info_menu":
                                    self.game_utils.handle_info_in_game_popup_action(clicked_popup_button, self.game_popup)
                        continue      

                    if not self.flag_menu:    
                        if game_initialized:
                            clicked_button = self.game_utils.check_button_click(mouse_pos, self.button_manager)
                            if clicked_button:
                                if clicked_button == "exit":
                                    running = False
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager)

                                elif clicked_button == "reset":
                                    current_map_name = "map" + str(self.game_utils.get_current_level())
                                    self.car_manager = self.game_utils.handle_button_action(clicked_button, load_map(self.console, current_map_name))
                                    
                                    self.init_common_game_var()
                                    
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.time_taken.update_text("TIME TAKEN : 0 s")
                                    self.display_manager.memory_peaked.update_text("MEMORY PEAKED : 0 MB")
                                    self.display_manager.expanded_nodes.update_text("EXPANDED NODES : 0")

                                    resetting = True
                                    reset_timer = current_time
                                    
                                elif clicked_button == "play":
                                    if not lv_started:
                                        self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                        lv_started = True

                                elif clicked_button == "mute":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager)
                                    self.button_manager.is_muted = not self.button_manager.is_muted

                                elif clicked_button == "info":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                
                                elif clicked_button == "pause":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                    self.button_manager.is_paused = not self.button_manager.is_paused

                                else:
                                    self.car_manager = self.game_utils.handle_button_action(clicked_button, self.car_manager)
                    
                    else:
                        clicked_button = self.game_utils.check_button_click(mouse_pos, self.button_menu)
                        if clicked_button:
                            if clicked_button == "play":
                                self.game_popup.choose_lv.show()
                                self.game_popup.update_type("choose_level")
                                self.flag_menu = False

                            elif clicked_button == "info":
                                self.game_utils.handle_button_action_menu(clicked_button, self.game_popup)

                            elif clicked_button == "mute":
                                self.game_utils.handle_button_action_menu(clicked_button)
                                self.button_menu.is_muted = not self.button_menu.is_muted
                                self.button_manager.is_muted = not self.button_manager.is_muted

                            elif clicked_button == "exit":
                                running = False
            
            if not self.flag_menu:
                if resetting and current_time - reset_timer >= RESET_DELAY:
                    resetting = False
                
                if (game_initialized and lv_started and not self.searched and 
                    not self.algorithm_running and not self.algorithm_completed and 
                    self.game_utils.has_selected_algorithm() and not self.game_popup.visible):
                    
                    self.algorithm_running = True
                    cars = list(self.car_manager.cars.values())
                    selected_algo = self.game_utils.get_selected_algorithm()
                    
                    self.run_algorithm_search(cars, selected_algo, self.on_algorithm_complete)

                self.screen.blit(self.board.image, (self.board.offset_x, self.board.offset_y))
                
                if (game_initialized and not resetting 
                    and self.searched and self.path 
                    and not self.game_popup.visible and self.algorithm_completed
                    and not self.game_utils.game_pause):
                    
                    cars_moving = self.car_manager.update_car()
                    if not cars_moving:  
                        if self.waiting_for_next_step:
                            
                            if current_time - self.step_timer >= STEP_DELAY:
                                self.waiting_for_next_step = False
                                self.current_step += 1
                        else:
                            if self.current_step < len(self.path):
                                if self.step_timer == 0:
                                    self.step_timer = current_time
                                
                                for car in self.path[self.current_step].cars:
                                    if car.name in self.car_manager.cars:
                                        self.car_manager.cars[car.name].y, self.car_manager.cars[car.name].x = car.coord
                                
                                self.moves_count += 1
                                self.display_manager.moves.update_text(f"MOVES :  {self.moves_count}")
                                
                                if(self.game_utils.get_selected_algorithm() in ["A STAR", "UCS"]):
                                    self.display_manager.costs.update_text(f"COSTS :  {self.path[self.current_step].cost}")
                                    self.cost = self.path[self.current_step].cost
                                else:
                                    self.display_manager.costs.update_text(f"COSTS :  {self.moves_count}")
                                    self.cost = self.moves_count

                                print(f"Executing state {self.current_step}/{len(self.path) - 1}")
                                
                                self.step_timer = current_time
                                self.waiting_for_next_step = True
                            else:
                                print(f"Algorithm execution completed! Total moves: {self.moves_count}")

                                if self.game_utils.check_win_condition(self.car_manager):
                                    current_algorithm = self.game_utils.get_selected_algorithm()
                                    self.game_utils.play_win_music()
                                    
                                    if self.game_utils.check_final_win_condition(self.car_manager):
                                        self.game_popup.final_win.show(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)
                                        self.game_popup.update_type("final_win")
                                    else:
                                        self.game_popup.win.show(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)
                                        self.game_popup.update_type("win")

                                    self.game_utils.set_game_completed(True)
                else:
                    self.car_manager.update_car()

                self.car_manager.draw_all(self.screen)
                
                if game_initialized and not lv_started:
                    target_car = self.car_manager.cars["target_car"]
                    self.screen.blit(self.console.reSize_Image(HIGHLIGHT_PATH), (target_car.offset_x, target_car.offset_y))
                
                if self.algorithm_running:
                    loading_text = "COMPUTING SOLUTION..."
                    text_x = self.console.screen_size // 2 - self.console.convertCoordinate(227, 0)[0]
                    text_y = self.console.screen_size // 2 
                    create_3d_text(self.screen, loading_text, 50, text_x, text_y, self.console)
                    
                self.button_manager.draw_all(self.screen)
                self.display_manager.draw_all(self.screen)
                x, y = self.console.convertCoordinate(284, 150)
                create_3d_text(self.screen, "RUSH HOUR", 140, self.console.screen_size // 2 - x, self.console.screen_size // 3 * 2 + y, self.console)
            else:
                self.display_menu.draw_menu(self.screen)
                x, y = self.console.convertCoordinate(284, 140)
                create_3d_text(self.screen, "RUSH HOUR", 140, self.console.screen_size // 2 - x, self.console.screen_size // 3 - y, self.console)

            self.game_popup.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
    