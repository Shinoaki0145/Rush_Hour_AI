import pygame
import console
from Cars import *
from board import *
from defs import *
from UI.Display.display_manage import DisplayManager
from UI.Display.display_menu import DisplayMenu
from UI.Button.button_manage import ButtonManager
from UI.Button.button_menu import ButtonMenu
# from UI.Popup.popup_manage import GamePopup
from ui import GamePopup
from UI import create_3d_text
from Utils import *
from Algo import *
from random import choice
from time import time
import tracemalloc, gc
import threading

def init_common_game_var():
    return (False, [], 1, 0, 0, 0, False, False, False, False)

def load_map(console, map_name):
    clear_valid_matrix()
    new_car_manager = ManageCar()
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

class Game():
    def __init__(self):
        pygame.init()
        self.console = console.Console()
        self.console.convertMatrix()

        self.screen = pygame.display.set_mode((self.console.screen_size, self.console.screen_size))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Rush Hour') 
        self.board = Board(self.console.reSize_Image(BACKGROUND_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

        # Initialize UI and Utils
        self.button_manager = ButtonManager(self.console)
        self.display_manager = DisplayManager(self.console)
        self.game_popup = GamePopup(self.console)
        self.game_utils = GameUtils(self.console)

        self.flag_menu = True
        self.button_menu = ButtonMenu(self.console)
        self.display_menu = DisplayMenu(self.console, self.button_menu, self.board.image, self.flag_menu)

        # THAY ĐỔI: Khởi tạo với level 1 nhưng sẽ được thay đổi khi người chơi chọn
        self.map_name = "map1"  # Default map
        self.car_manager = load_map(self.console, self.map_name)

        # THAY ĐỔI: Không cập nhật level display ngay lập tức vì người chơi chưa chọn
        # display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")

        # Initialize game logic
        (self.searched,
        self.path,
        self.current_step,
        self.moves_count,
        self.cost,
        self.step_timer,
        self.is_moving,
        self.waiting_for_next_step,
        self.algorithm_running,
        self.algorithm_completed) = init_common_game_var()
    
    def on_algorithm_complete(self, result_path, algorithm_name):
        """Callback khi thuật toán hoàn thành"""
        self.algorithm_running = False
        self.algorithm_completed = True
        
        if result_path is None or len(result_path) == 0:
            print(f"No solution found with {algorithm_name}")
            current_algorithm = self.game_utils.get_selected_algorithm()
            self.game_utils.play_fail_music()
            # self.game_popup.lose.show(self.game_utils.get_current_level(), current_algorithm)
            # self.game_popup.update(True, "lose")
            self.game_popup.show_lose_message(self.game_utils.get_current_level(), current_algorithm)
        else:
            print(f"Found path with {len(result_path)} states using {algorithm_name}")
            self.path = result_path
            self.searched = True
            self.current_step = 1
            # QUAN TRỌNG: Reset step_timer khi bắt đầu execution
            self.step_timer = 0
    
    def run_algorithm_search(self, cars, selected_algo, callback):
        """Chạy thuật toán trong thread riêng"""
        def search_thread():
            try:
                print(f"Starting search with algorithm: {selected_algo}")
                
                # Setup search
                simple_cars = []
                for car in cars:
                    simple_cars.append(SimpleCar(car.name, car.length_grid, (car.y, car.x), not car.is_horizontal))
                start = State(simple_cars)

                # Measure performance
                gc.collect()
                tracemalloc.start()
                begin = time()
                
                # Run algorithm
                if selected_algo == "BFS":
                    self.path = bfs(start)
                elif selected_algo == "DFS":
                    self.path = dfs(start)
                elif selected_algo == "A STAR":
                    self.path = a_star(start)
                elif selected_algo == "UCS":
                    self.path = ucs(start)
                else:
                    self.path = a_star(start)
                
                time_taken = round(time() - begin, 4)
                memory_used = round(tracemalloc.get_traced_memory()[1] / (1024 ** 2), 2)
                tracemalloc.stop()
                
                print(f"Time taken: {time_taken} seconds.")
                print(f"Memory peaked: {memory_used} MB.")
                
                # Callback với kết quả
                callback(self.path, selected_algo)
                
            except Exception as e:
                print(f"Error in algorithm search: {e}")
                callback(None, selected_algo)
        
        # Chạy trong thread riêng
        search_thread = threading.Thread(target=search_thread, daemon=True)
        search_thread.start()
    
    def game_start(self):
        lv_started = False
        resetting = False
        reset_timer = 0
        game_initialized = False  # THÊM: Flag để theo dõi xem game đã được khởi tạo chưa
        
        running = True  
        while running:  
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Kiểm tra click vào popup trước
                    if not self.flag_menu:
                        if self.game_popup.visible:
                            clicked_popup_button = self.game_popup.check_button_click(mouse_pos)
                            if clicked_popup_button:
                                if self.game_popup.popup_type == "algorithm":
                                    # Xử lý algorithm selection
                                    print(f"Algorithm selected: {clicked_popup_button}")
                                    
                                    # SET ALGORITHM TRƯỚC
                                    self.game_utils.handle_algorithm_selection(clicked_popup_button)
                                    
                                    # UPDATE DISPLAY SAU
                                    algorithm_display_text = f"ALGORITHM :  {clicked_popup_button}"
                                    self.display_manager.algo.update_text(algorithm_display_text)
                                    
                                    # ẨN POPUP
                                    self.game_popup.hide()
                                    
                                    # Reset variables
                                    (self.searched,
                                    self.path,
                                    self.current_step,
                                    self.moves_count,
                                    self.cost,
                                    self.step_timer,
                                    self.is_moving,
                                    self.waiting_for_next_step,
                                    self.algorithm_running,
                                    self.algorithm_completed) = init_common_game_var()
                                    
                                    # Debug
                                    print(f"Display text: {algorithm_display_text}")
                                    print(f"Utils algorithm: {self.game_utils.get_selected_algorithm()}")
                                    
                                elif self.game_popup.popup_type == "win":
                                    # Xử lý win popup
                                    next_lv = self.game_utils.handle_win_popup_action(clicked_popup_button, self.game_popup)
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    # Reset variables
                                    if next_lv:
                                        self.map_name = "map" + str(self.game_utils.get_current_level())
                                    self.car_manager = load_map(self.console, self.map_name)
                                    lv_started = False
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    (self.searched,
                                    self.path,
                                    self.current_step,
                                    self.moves_count,
                                    self.cost,
                                    self.step_timer,
                                    self.is_moving,
                                    self.waiting_for_next_step,
                                    self.algorithm_running,
                                    self.algorithm_completed) = init_common_game_var()

                                elif self.game_popup.popup_type == "lose":    
                                    # Xử lý lose popup
                                    reset_level = self.game_utils.handle_lose_popup_action(clicked_popup_button, self.game_popup)
                                    self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    self.display_manager.algo.update_text("ALGORITHM :  ")
                                    
                                    # Reset variables
                                    if reset_level:  # Nếu cần reset level
                                        self.car_manager = load_map(self.console, self.map_name)
                                    lv_started = False

                                    (self.searched,
                                    self.path,
                                    self.current_step,
                                    self.moves_count,
                                    self.cost,
                                    self.step_timer,
                                    self.is_moving,
                                    self.waiting_for_next_step,
                                    self.algorithm_running,
                                    self.algorithm_completed) = init_common_game_var()
                                    
                                elif self.game_popup.popup_type == "final_win_1":
                                    # Xử lý final win 1 popup
                                    self.car_manager = self.game_utils.handle_final_win_1_popup_action(
                                        clicked_popup_button, 
                                        self.car_manager, 
                                        self.game_popup
                                    )

                                elif self.game_popup.popup_type == "final_win_2":
                                    # THAY ĐỔI: Xử lý final win 2 popup (level selection)
                                    if clicked_popup_button != "exit":
                                        # Người chơi đã chọn level
                                        self.car_manager = self.game_utils.handle_final_win_2_popup_action(
                                            clicked_popup_button, 
                                            self.car_manager, 
                                            self.game_popup,
                                            self.console, 
                                            load_map
                                        )

                                        # Cập nhật tất cả displays sau khi chọn level
                                        self.map_name = "map" + str(self.game_utils.get_current_level())
                                        self.display_manager.level.update_text(f"LEVEL :  {self.game_utils.get_current_level()}")
                                        self.display_manager.moves.update_text("MOVES :  0")
                                        self.display_manager.costs.update_text("COSTS :  0")
                                        self.display_manager.algo.update_text("ALGORITHM :  ")
                                        
                                        # Reset algorithm variables
                                        (self.searched,
                                        self.path,
                                        self.current_step,
                                        self.moves_count,
                                        self.cost,
                                        self.step_timer,
                                        self.is_moving,
                                        self.waiting_for_next_step,
                                        self.algorithm_running,
                                        self.algorithm_completed) = init_common_game_var()
                                        
                                        lv_started = False
                                        game_initialized = True  # THÊM: Đánh dấu game đã được khởi tạo
                                        
                                        print(f"Game initialized with level: {self.game_utils.get_current_level()}")
                                    else:
                                        # Người chơi chọn exit
                                        running = False
                                elif self.game_popup.popup_type == "info_buttons":
                                    self.game_utils.handle_info_in_game_popup_action(clicked_popup_button, self.game_popup)
                                        
                            continue
                    else:
                        clicked_popup_button = self.game_popup.check_button_click(mouse_pos)
                        if (self.game_popup.visible and clicked_button and 
                            self.game_popup.popup_type == "info_menu"):
                            self.game_utils.handle_info_in_game_popup_action(clicked_popup_button, self.game_popup)

                    if not self.flag_menu:    
                        # THAY ĐỔI: Chỉ xử lý click button khi game đã được khởi tạo
                        if game_initialized:
                            # Kiểm tra click vào main buttons
                            clicked_button = self.game_utils.check_button_click(mouse_pos, self.button_manager)
                            if clicked_button:
                                if clicked_button == "exit":
                                    running = False
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager)
                                elif clicked_button == "reset":
                                    # Lấy level hiện tại và tạo map_name tương ứng
                                    current_map_name = "map" + str(self.game_utils.get_current_level())
                                    self.car_manager = self.game_utils.handle_button_action(clicked_button, load_map(self.console, current_map_name))
                                    # Reset algorithm variables
                                    (self.searched,
                                    self.path,
                                    self.current_step,
                                    self.moves_count,
                                    self.cost,
                                    self.step_timer,
                                    self.is_moving,
                                    self.waiting_for_next_step,
                                    self.algorithm_running,
                                    self.algorithm_completed) = init_common_game_var()
                                    # Cập nhật display
                                    self.display_manager.moves.update_text("MOVES :  0")
                                    self.display_manager.costs.update_text("COSTS :  0")
                                    # Start reset timer
                                    resetting = True
                                    reset_timer = current_time
                                elif clicked_button == "play":
                                    # Hiển thị popup algorithm selection
                                    if not lv_started:
                                        self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                        lv_started = True
                                elif clicked_button == "mute":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager)
                                    if self.game_utils.audio_muted:
                                        self.button_manager.mute.update_icon(BUTTON_PATH + "but_no_audio.png")
                                    else:
                                        self.button_manager.mute.update_icon(BUTTON_PATH + "but_audio.png")
                                elif clicked_button == "info":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                elif clicked_button == "pause":
                                    self.game_utils.handle_button_action(clicked_button, self.car_manager, self.game_popup)
                                    if self.game_utils.game_pause:
                                        self.button_manager.pause.update_icon(BUTTON_PATH + "but_next.png")
                                    else:
                                        self.button_manager.pause.update_icon(BUTTON_PATH + "but_pause.png")
                                else:
                                    self.car_manager = self.game_utils.handle_button_action(clicked_button, self.car_manager)
                    
                    else:
                        clicked_button = self.game_utils.check_button_click(mouse_pos, self.button_menu)
                        if clicked_button:
                            if clicked_button == "play":
                                # game_utils.handle_button_action_menu(clicked_button, game_popup)
                                self.game_popup.show_final_win_2_message()  # Hiển thị popup chọn level
                                self.flag_menu = False
                            elif clicked_button == "info":
                                self.game_utils.handle_button_action_menu(clicked_button, self.game_popup)
                            elif clicked_button == "mute":
                                self.game_utils.handle_button_action_menu(clicked_button, self.car_manager)
                                if self.game_utils.audio_muted:
                                    self.button_menu.update_mute_icon(BUTTON_PATH + "but_no_audio.png")
                                else:
                                    self.button_menu.update_mute_icon(BUTTON_PATH + "but_audio.png")   
                            elif clicked_button == "exit":
                                running = False
            
            if not self.flag_menu:
                if resetting and current_time - reset_timer >= RESET_DELAY:
                    resetting = False
                
                # THAY ĐỔI: Chỉ chạy algorithm khi game đã được khởi tạoself.
                if (game_initialized and lv_started and not self.searched and 
                    not self.algorithm_running and not self.algorithm_completed and 
                    self.game_utils.has_selected_algorithm() and not self.game_popup.visible):
                    
                    print("Starting algorithm search in background thread...")
                    self.algorithm_running = True
                    cars = list(self.car_manager.cars.values())
                    selected_algo = self.game_utils.get_selected_algorithm()
                    
                    # Chạy thuật toán trong thread riêng
                    self.run_algorithm_search(cars, selected_algo, self.on_algorithm_complete)

                # Draw game elements
                self.screen.blit(self.board.image, (self.board.offset_x, self.board.offset_y))
                
                # THAY ĐỔI: Chỉ thực hiện algorithm execution khi game đã được khởi tạo
                if (game_initialized and not resetting 
                    and self.searched and self.path 
                    and not self.game_popup.visible and self.algorithm_completed
                    and not self.game_utils.game_pause):
                    # Kiểm tra xem có xe nào đang di chuyển không
                    cars_moving = self.car_manager.update_car()
                    if not cars_moving:  # Không có xe nào đang di chuyển
                        if self.waiting_for_next_step:
                            # Đang chờ để thực hiện step tiếp theo
                            if current_time - self.step_timer >= STEP_DELAY:
                                self.waiting_for_next_step = False
                                self.current_step += 1
                        else:
                            # Thực hiện step tiếp theo nếu còn
                            if self.current_step < len(self.path):
                                # QUAN TRỌNG: Chỉ set step_timer khi bắt đầu step mới
                                if self.step_timer == 0:  # Lần đầu tiên hoặc sau khi reset
                                    self.step_timer = current_time
                                
                                # Cập nhật vị trí xe theo step hiện tại
                                for car in self.path[self.current_step].cars:
                                    if car.name in self.car_manager.cars:
                                        self.car_manager.cars[car.name].y, self.car_manager.cars[car.name].x = car.coord
                                
                                self.moves_count += 1  # Tăng số bước di chuyển
                                # Cập nhật hiển thị số bước di chuyển
                                self.display_manager.moves.update_text(f"MOVES :  {self.moves_count}")
                                if(self.game_utils.get_selected_algorithm() in ["A STAR", "UCS"]):
                                    self.display_manager.costs.update_text(f"COSTS :  {self.path[self.current_step].cost}")
                                    self.cost = self.path[self.current_step].cost
                                else:
                                    self.display_manager.costs.update_text(f"COSTS :  {self.moves_count}")
                                    self.cost = self.moves_count

                                print(f"Executing state {self.current_step}/{len(self.path) - 1}")
                                
                                # Bắt đầu đếm thời gian chờ cho step tiếp theo
                                self.step_timer = current_time
                                self.waiting_for_next_step = True
                            else:
                                # Algorithm execution completed
                                print(f"Algorithm execution completed! Total moves: {self.moves_count}")

                                if self.game_utils.check_win_condition(self.car_manager):
                                    current_algorithm = self.game_utils.get_selected_algorithm()
                                    self.game_utils.play_win_music()
                                    
                                    # Kiểm tra final win condition (level 12)
                                    if self.game_utils.check_final_win_condition(self.car_manager):
                                        # self.game_popup.finalwin1.show(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)
                                        # self.game_popup.update(True, "final_win_1")
                                        self.game_popup.show_final_win_1_message(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)
                                    else:
                                        # self.game_popup.win.show(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)
                                        # self.game_popup.update(True, "win")
                                        self.game_popup.show_win_message(self.game_utils.get_current_level(), self.moves_count, self.cost, current_algorithm)


                                    self.game_utils.set_game_completed(True)
                else:
                    # Update cars khi không có algorithm execution
                    self.car_manager.update_car()

                self.car_manager.draw_all(self.screen)
                
                # THAY ĐỔI: Chỉ hiển thị highlight khi game đã được khởi tạo và chưa bắt đầu level
                if game_initialized and not lv_started:
                    target_car = self.car_manager.cars["target_car"]
                    self.screen.blit(self.console.reSize_Image(HIGHLIGHT_PATH), (target_car.offset_x, target_car.offset_y))
                
                # Hiển thị loading indicator khi algorithm đang chạy
                if self.algorithm_running:
                    loading_text = "COMPUTING SOLUTION..."
                    text_x = self.console.screen_size // 2 - len(loading_text) * 8 + 20
                    text_y = self.console.screen_size // 2 
                    create_3d_text(self.screen, loading_text, 24, text_x, text_y)
                    
                # Draw UI elements
                self.button_manager.draw_all(self.screen)
                self.display_manager.draw_all(self.screen)
                create_3d_text(self.screen, "RUSH HOUR", 80, 180, self.console.screen_size - 96)
            else:
                self.display_menu.draw_menu(self.screen)
                create_3d_text(self.screen, "RUSH HOUR", 100, 125, self.console.screen_size // 3 - 120)
           
            # Draw popup (phải vẽ cuối cùng để hiển thị trên cùng)
            self.game_popup.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
    