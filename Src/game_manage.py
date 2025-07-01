import pygame
import console
from car import *
from board import *
from defs import *
from manage_car import *
from ui import *
from utils import *
from Algo import *
from random import choice
from time import time
import tracemalloc, gc
import threading

def load_map(map_name):
    clear_valid_matrix()
    new_manage_car = ManageCar()
    map_path = ASSET_PATH + "Map/" + map_name + ".txt"
    with open(map_path) as f:
        target_car_x, target_car_y = list(map(int, f.readline().strip().split(',')))
        target_car = MainCar(target_car_x, target_car_y, console.reSize_Image(TARGET_CAR_PATH))
        new_manage_car.add_car(target_car)

        car_count = 0
        for line in f.readlines():
            type, x, y, horizontal, direction = line.strip().split(',')
            if type == 'car':
                car_id = str(choice(range(0, 5)))
            else:
                car_id = str(choice(range(0, 3)))
            new_manage_car.add_car(Car(
                type + str(car_count),
                int(x),
                int(y),
                console.reSize_Image(CAR_PATH + type + "_" + car_id + ".png"),
                int(horizontal),
                direction
            ))
            car_count += 1
    return new_manage_car

def init_common_game_var():
    return (False, [], 1, 0, 0, 0, False, False, False, False)

def run_algorithm_search(cars, selected_algo, callback):
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
                path = bfs(start)
            elif selected_algo == "DFS":
                path = dfs(start)
            elif selected_algo == "A STAR":
                path = a_star(start)
            elif selected_algo == "UCS":
                path = ucs(start)
            else:
                path = a_star(start)
            
            time_taken = round(time() - begin, 4)
            memory_used = round(tracemalloc.get_traced_memory()[1] / (1024 ** 2), 2)
            tracemalloc.stop()
            
            print(f"Time taken: {time_taken} seconds.")
            print(f"Memory peaked: {memory_used} MB.")
            
            # Callback với kết quả
            callback(path, selected_algo)
            
        except Exception as e:
            print(f"Error in algorithm search: {e}")
            callback(None, selected_algo)
    
    # Chạy trong thread riêng
    search_thread = threading.Thread(target=search_thread, daemon=True)
    search_thread.start()

pygame.init()
console = console.Console()
console.convertMatrix()

screen = pygame.display.set_mode((console.screen_size, console.screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour') 
running = True  
board = Board(console.reSize_Image(BACKGROUND_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

flag_menu = True
# flag_menu = False

# Initialize UI and Utils
button_manager = ButtonManager(console)
display_manager = DisplayManager(console)
game_popup = GamePopup(console)
game_utils = GameUtils(console)
button_menu = ButtonMenu(console)
display_menu = DisplayMenu(console, button_menu, board.image, flag_menu)

# THAY ĐỔI: Hiển thị popup chọn level ngay khi khởi động
# game_popup.show_final_win_2_message()  # Hiển thị popup chọn level

# THAY ĐỔI: Khởi tạo với level 1 nhưng sẽ được thay đổi khi người chơi chọn
map_name = "map1"  # Default map
manage_car = load_map(map_name)

# THAY ĐỔI: Không cập nhật level display ngay lập tức vì người chơi chưa chọn
# display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")

# Initialize game logic
(searched,
path,
current_step,
moves_count,
cost,
step_timer,
is_moving,
waiting_for_next_step,
algorithm_running,
algorithm_completed) = init_common_game_var()

lv_started = False
resetting = False
reset_timer = 0
game_initialized = False  # THÊM: Flag để theo dõi xem game đã được khởi tạo chưa

def on_algorithm_complete(result_path, algorithm_name):
    """Callback khi thuật toán hoàn thành"""
    global path, searched, algorithm_running, algorithm_completed, current_step, step_timer
    
    algorithm_running = False
    algorithm_completed = True
    
    if result_path is None or len(result_path) == 0:
        print(f"No solution found with {algorithm_name}")
        current_algorithm = game_utils.get_selected_algorithm()
        game_popup.show_lose_message(game_utils.get_current_level(), current_algorithm)
    else:
        print(f"Found path with {len(result_path)} states using {algorithm_name}")
        path = result_path
        searched = True
        current_step = 1
        # QUAN TRỌNG: Reset step_timer khi bắt đầu execution
        step_timer = 0

while running:  
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Kiểm tra click vào popup trước
            if not flag_menu:
                if game_popup.visible:
                    clicked_popup_button = game_popup.check_button_click(mouse_pos)
                    if clicked_popup_button:
                        if game_popup.popup_type == "algorithm":
                            # Xử lý algorithm selection
                            print(f"Algorithm selected: {clicked_popup_button}")
                            
                            # SET ALGORITHM TRƯỚC
                            game_utils.handle_algorithm_selection(clicked_popup_button)
                            
                            # UPDATE DISPLAY SAU
                            algorithm_display_text = f"ALGORITHM :  {clicked_popup_button}"
                            display_manager.update_display_text("algorithm", algorithm_display_text)
                            
                            # ẨN POPUP
                            game_popup.hide()
                            
                            # Reset variables
                            (searched,
                            path,
                            current_step,
                            moves_count,
                            cost,
                            step_timer,
                            is_moving,
                            waiting_for_next_step,
                            algorithm_running,
                            algorithm_completed) = init_common_game_var()
                            
                            # Debug
                            print(f"Display text: {algorithm_display_text}")
                            print(f"Utils algorithm: {game_utils.get_selected_algorithm()}")
                            
                        elif game_popup.popup_type == "win":
                            # Xử lý win popup
                            next_lv = game_utils.handle_win_popup_action(clicked_popup_button, game_popup)
                            display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                            display_manager.update_display_text("moves", "MOVES :  0")
                            display_manager.update_display_text("costs", "COSTS :  0")
                            display_manager.update_display_text("algorithm", "ALGORITHM :  ")
                            # Reset variables
                            if next_lv:
                                map_name = "map" + str(game_utils.get_current_level())
                            manage_car = load_map(map_name)
                            lv_started = False
                            display_manager.update_display_text("algorithm", "ALGORITHM :  ")
                            (searched,
                            path,
                            current_step,
                            moves_count,
                            cost,
                            step_timer,
                            is_moving,
                            waiting_for_next_step,
                            algorithm_running,
                            algorithm_completed) = init_common_game_var()

                        elif game_popup.popup_type == "lose":    
                            # Xử lý lose popup
                            reset_level = game_utils.handle_lose_popup_action(clicked_popup_button, game_popup)
                            display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                            display_manager.update_display_text("moves", "MOVES :  0")
                            display_manager.update_display_text("costs", "COSTS :  0")
                            display_manager.update_display_text("algorithm", "ALGORITHM :  ")
                            
                            # Reset variables
                            if reset_level:  # Nếu cần reset level
                                manage_car = load_map(map_name)
                            lv_started = False

                            (searched,
                            path,
                            current_step,
                            moves_count,
                            cost,
                            step_timer,
                            is_moving,
                            waiting_for_next_step,
                            algorithm_running,
                            algorithm_completed) = init_common_game_var()
                            
                        elif game_popup.popup_type == "final_win_1":
                            # Xử lý final win 1 popup
                            manage_car = game_utils.handle_final_win_1_popup_action(
                                clicked_popup_button, 
                                manage_car, 
                                game_popup
                            )

                        elif game_popup.popup_type == "final_win_2":
                            # THAY ĐỔI: Xử lý final win 2 popup (level selection)
                            if clicked_popup_button != "exit":
                                # Người chơi đã chọn level
                                manage_car = game_utils.handle_final_win_2_popup_action(
                                    clicked_popup_button, 
                                    manage_car, 
                                    game_popup, 
                                    load_map
                                )
                                
                                # Cập nhật tất cả displays sau khi chọn level
                                map_name = "map" + str(game_utils.get_current_level())
                                display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                                display_manager.update_display_text("moves", "MOVES :  0")
                                display_manager.update_display_text("costs", "COSTS :  0")
                                display_manager.update_display_text("algorithm", "ALGORITHM :  ")
                                
                                # Reset algorithm variables
                                (searched,
                                path,
                                current_step,
                                moves_count,
                                cost,
                                step_timer,
                                is_moving,
                                waiting_for_next_step,
                                algorithm_running,
                                algorithm_completed) = init_common_game_var()
                                
                                lv_started = False
                                game_initialized = True  # THÊM: Đánh dấu game đã được khởi tạo
                                
                                print(f"Game initialized with level: {game_utils.get_current_level()}")
                            else:
                                # Người chơi chọn exit
                                running = False
                        elif game_popup.popup_type == "info_buttons":
                            game_utils.handle_info_in_game_popup_action(clicked_popup_button, game_popup)
                                
                    continue
            else:
                clicked_popup_button = game_popup.check_button_click(mouse_pos)
                if game_popup.visible:
                    if clicked_popup_button:
                        if game_popup.popup_type == "info_menu": 
                            game_utils.handle_info_in_game_popup_action(clicked_popup_button, game_popup)
            if not flag_menu:
                # THAY ĐỔI: Chỉ xử lý click button khi game đã được khởi tạo
                if game_initialized:
                    # Kiểm tra click vào main buttons
                    clicked_button = game_utils.check_button_click(mouse_pos, button_manager)
                    if clicked_button:
                        if clicked_button == "exit":
                            running = False
                            game_utils.handle_button_action(clicked_button, manage_car)
                        elif clicked_button == "reset":
                            # Lấy level hiện tại và tạo map_name tương ứng
                            current_map_name = "map" + str(game_utils.get_current_level())
                            manage_car = game_utils.handle_button_action(clicked_button, load_map(current_map_name))
                            # Reset algorithm variables
                            (searched,
                            path,
                            current_step,
                            moves_count,
                            cost,
                            step_timer,
                            is_moving,
                            waiting_for_next_step,
                            algorithm_running,
                            algorithm_completed) = init_common_game_var()
                            # Cập nhật display
                            display_manager.update_display_text("moves", "MOVES :  0")
                            # Start reset timer
                            resetting = True
                            reset_timer = current_time
                        elif clicked_button == "play":
                            # Hiển thị popup algorithm selection
                            if not lv_started:
                                game_utils.handle_button_action(clicked_button, manage_car, game_popup)
                                lv_started = True
                        elif clicked_button == "mute":
                            game_utils.handle_button_action(clicked_button, manage_car)
                            if game_utils.audio_muted:
                                button_manager.update_button_icon("mute", BUTTON_PATH + "but_no_audio.png")
                            else:
                                button_manager.update_button_icon("mute", BUTTON_PATH + "but_audio.png")
                        elif clicked_button == "info":
                            game_utils.handle_button_action(clicked_button, manage_car, game_popup)
                        else:
                            manage_car = game_utils.handle_button_action(clicked_button, manage_car)
            else:
                clicked_button = game_utils.check_button_click(mouse_pos, button_menu)
                if clicked_button:
                    if clicked_button == "play":
                        # game_utils.handle_button_action_menu(clicked_button, game_popup)
                        game_popup.show_final_win_2_message()  # Hiển thị popup chọn level
                        flag_menu = False
                    if clicked_button == "info":
                        game_utils.handle_button_action_menu(clicked_button, game_popup)
                    elif clicked_button == "exit":
                        running = False
    
    if(not flag_menu):
        if resetting and current_time - reset_timer >= RESET_DELAY:
            resetting = False
        
        # THAY ĐỔI: Chỉ chạy algorithm khi game đã được khởi tạo
        if (game_initialized and lv_started and not searched and not algorithm_running and not algorithm_completed 
            and game_utils.has_selected_algorithm() and not game_popup.visible):
            
            print("Starting algorithm search in background thread...")
            algorithm_running = True
            cars = list(manage_car.cars.values())
            selected_algo = game_utils.get_selected_algorithm()
            
            # Chạy thuật toán trong thread riêng
            run_algorithm_search(cars, selected_algo, on_algorithm_complete)

        # Draw game elements
        screen.blit(board.image, (board.offset_x, board.offset_y))
        
        # THAY ĐỔI: Chỉ thực hiện algorithm execution khi game đã được khởi tạo
        if (game_initialized and not resetting and searched and path and not game_popup.visible and algorithm_completed):
            # Kiểm tra xem có xe nào đang di chuyển không
            cars_moving = manage_car.update_car()
            if not cars_moving:  # Không có xe nào đang di chuyển
                if waiting_for_next_step:
                    # Đang chờ để thực hiện step tiếp theo
                    if current_time - step_timer >= STEP_DELAY:
                        waiting_for_next_step = False
                        current_step += 1
                else:
                    # Thực hiện step tiếp theo nếu còn
                    if current_step < len(path):
                        # QUAN TRỌNG: Chỉ set step_timer khi bắt đầu step mới
                        if step_timer == 0:  # Lần đầu tiên hoặc sau khi reset
                            step_timer = current_time
                        
                        # Cập nhật vị trí xe theo step hiện tại
                        for car in path[current_step].cars:
                            if car.name in manage_car.cars:
                                manage_car.cars[car.name].y, manage_car.cars[car.name].x = car.coord
                        
                        moves_count += 1  # Tăng số bước di chuyển
                        # Cập nhật hiển thị số bước di chuyển
                        display_manager.update_display_text("moves", f"MOVES :  {moves_count}")
                        if(game_utils.get_selected_algorithm() in ["A STAR", "UCS"]):
                            display_manager.update_display_text("costs", f"COSTS :  {path[current_step].cost}")
                            cost = path[current_step].cost
                        else:
                            display_manager.update_display_text("costs", f"COSTS :  {moves_count}")
                            cost = moves_count

                        print(f"Executing state {current_step}/{len(path) - 1}")
                        
                        # Bắt đầu đếm thời gian chờ cho step tiếp theo
                        step_timer = current_time
                        waiting_for_next_step = True
                    else:
                        # Algorithm execution completed
                        print(f"Algorithm execution completed! Total moves: {moves_count}")

                        if game_utils.check_win_condition(manage_car):
                            current_algorithm = game_utils.get_selected_algorithm()
                            game_utils.play_win_music()
                            
                            # Kiểm tra final win condition (level 12)
                            if game_utils.check_final_win_condition(manage_car):
                                game_popup.show_final_win_1_message(game_utils.get_current_level(), moves_count, cost, current_algorithm)
                            else:
                                game_popup.show_win_message(game_utils.get_current_level(), moves_count, cost, current_algorithm)


                            game_utils.set_game_completed(True)
        else:
            # Update cars khi không có algorithm execution
            manage_car.update_car()

        manage_car.draw_all(screen)
        
        # THAY ĐỔI: Chỉ hiển thị highlight khi game đã được khởi tạo và chưa bắt đầu level
        if game_initialized and not lv_started:
            target_car = manage_car.cars["target_car"]
            screen.blit(console.reSize_Image(HIGHLIGHT_PATH), (target_car.offset_x, target_car.offset_y))
        
        # Hiển thị loading indicator khi algorithm đang chạy
        if algorithm_running:
            loading_text = "COMPUTING SOLUTION..."
            text_x = console.screen_size // 2 - len(loading_text) * 8 + 20
            text_y = console.screen_size // 2 
            create_3d_text(screen, loading_text, 24, text_x, text_y)
            
        # Draw UI elements
        button_manager.draw_all_buttons(screen)
        display_manager.draw_all_displays(screen)
        create_3d_text(screen, "RUSH HOUR", 80, 180, console.screen_size - 96)

    else:
        display_menu.draw_menu(screen)
        create_3d_text(screen, "RUSH HOUR", 100, 125, console.screen_size // 3 - 120)
    
    # Draw popup (phải vẽ cuối cùng để hiển thị trên cùng)
    game_popup.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()