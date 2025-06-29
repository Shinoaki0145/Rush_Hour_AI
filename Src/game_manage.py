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
    return (False, [], 1, 0, 0, False, False)


pygame.init()
console = console.Console()
console.convertMatrix()

screen = pygame.display.set_mode((console.screen_size, console.screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour') 
running = True  
board = Board(console.reSize_Image(BACKGROUND_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

# Initialize UI and Utils
button_manager = ButtonManager(console)
display_manager = DisplayManager(console)
game_popup = GamePopup(console)
game_utils = GameUtils(console)

# Initialize cars
map_name = "map" + str(game_utils.get_current_level())
manage_car = load_map(map_name)

# Initialize game logic
(searched,
path,
current_step,
moves_count,
step_timer,
is_moving,
waiting_for_next_step) = init_common_game_var()
lv_started = False
resetting = False
reset_timer = 0

while running:  
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Kiểm tra click vào popup trước
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
                        step_timer,
                        is_moving,
                        waiting_for_next_step) = init_common_game_var()
                        
                        # Debug
                        print(f"Display text: {algorithm_display_text}")
                        print(f"Utils algorithm: {game_utils.get_selected_algorithm()}")
                        
                    elif game_popup.popup_type == "win":
                        # Xử lý win popup
                        next_lv = game_utils.handle_win_popup_action(clicked_popup_button, game_popup)
                        display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                        display_manager.update_display_text("moves", "MOVES :  0")
                        
                        # Reset variables
                        if next_lv:
                            map_name = "map" + str(game_utils.get_current_level())
                        manage_car = load_map(map_name)
                        lv_started = False
                        (searched,
                        path,
                        current_step,
                        moves_count,
                        step_timer,
                        is_moving,
                        waiting_for_next_step) = init_common_game_var()

                    elif game_popup.popup_type == "lose":
                        # Xử lý lose popup
                        mange_car = game_utils.handle_lose_popup_action(clicked_popup_button, load_map(map_name), game_popup)
                        display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                        display_manager.update_display_text("moves", "MOVES :  0")
                        
                        # Reset variables
                        searched = False
                        path = []
                        current_step = 0
                        step_timer = 0
                        is_moving = False
                        waiting_for_next_step = False
                        moves_count = 0
                        algorithm_execution_completed = False
                        
                    elif game_popup.popup_type == "final_win_1":
                        # Xử lý final win 1 popup
                        manage_car = game_utils.handle_final_win_1_popup_action(
                            clicked_popup_button, 
                            manage_car, 
                            game_popup
                        )

                    elif game_popup.popup_type == "final_win_2":
                        # Xử lý final win 2 popup
                        manage_car = game_utils.handle_final_win_2_popup_action(
                            clicked_popup_button, 
                            manage_car, 
                            game_popup, 
                            load_map
                        )
                        
                        # Cập nhật display và reset variables chỉ khi không exit
                        if clicked_popup_button != "exit":
                            display_manager.update_display_text("level", f"LEVEL :  {game_utils.get_current_level()}")
                            display_manager.update_display_text("moves", "MOVES :  0")
                            
                            # Reset algorithm variables
                            searched = False
                            path = []
                            current_step = 0
                            step_timer = 0
                            is_moving = False
                            waiting_for_next_step = False
                            moves_count = 0
                            algorithm_execution_completed = False
                continue
            
            # Kiểm tra click vào main buttons
            clicked_button = game_utils.check_button_click(mouse_pos, button_manager)
            if clicked_button:
                if clicked_button == "exit":
                    running = False
                    game_utils.handle_button_action(clicked_button, manage_car)
                elif clicked_button == "reset":
                    manage_car = game_utils.handle_button_action(clicked_button, load_map(map_name))
                    # Reset algorithm variables
                    (searched,
                    path,
                    current_step,
                    moves_count,
                    step_timer,
                    is_moving,
                    waiting_for_next_step) = init_common_game_var()
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
                else:
                    manage_car = game_utils.handle_button_action(clicked_button, manage_car)
    if resetting and current_time - reset_timer >= RESET_DELAY:
        resetting = False
    # Run search - chỉ chạy khi không có popup hiển thị
    if lv_started and not searched:
        cars = []
        for car in manage_car.cars.values():
            cars.append(SimpleCar(car.name, car.length_grid, (car.y, car.x), not car.is_horizontal))
        start = State(cars)

        # Lấy algorithm được chọn
        selected_algo = game_utils.get_selected_algorithm()
        print(f"Running search with algorithm: {selected_algo}")
        
        # Chọn algorithm implementation
        if selected_algo == "BFS":
            path = bfs(start)
        elif selected_algo == "IDS":
            path = ids(start)
        elif selected_algo == "A STAR":
            path = a_star(start)
        elif selected_algo == "UCS":
            path = ucs(start)
        else:
            path = a_star(start)
            
        current_step = 1
        step_timer = current_time
        searched = True

        if game_utils.check_lose_condition(path, True):
            print(f"No solution found with {selected_algo}")
            current_algorithm = game_utils.get_selected_algorithm()
            game_popup.show_lose_message(game_utils.get_current_level(), current_algorithm)
            algorithm_execution_completed = True
        else:
            print(f"Found path with {len(path)} steps using {selected_algo}")

    # Draw game elements
    screen.blit(board.image, (board.offset_x, board.offset_y))
    
    # Algorithm execution with step timing - chỉ chạy khi không có popup
    if not resetting and searched and path and not game_popup.visible:
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
                    # Cập nhật vị trí xe theo step hiện tại
                    for car in path[current_step].cars:
                        if car.name in manage_car.cars:
                            manage_car.cars[car.name].y, manage_car.cars[car.name].x = car.coord
                    
                    moves_count += 1  # Tăng số bước di chuyển
                    # Cập nhật hiển thị số bước di chuyển
                    display_manager.update_display_text("moves", f"MOVES :  {moves_count}")
                    
                    print(f"Executing step {current_step + 1}/{len(path)}")
                    
                    # Bắt đầu đếm thời gian chờ cho step tiếp theo
                    step_timer = current_time
                    waiting_for_next_step = True
                else:
                    # Algorithm execution completed
                    print(f"Algorithm execution completed! Total moves: {moves_count}")

                    if game_utils.check_win_condition(manage_car):
                        current_algorithm = game_utils.get_selected_algorithm()
                        
                        # Kiểm tra final win condition (level 12)
                        if game_utils.check_final_win_condition(manage_car):
                            game_popup.show_final_win_1_message(game_utils.get_current_level(), moves_count, current_algorithm)
                        else:
                            game_popup.show_win_message(game_utils.get_current_level(), moves_count, current_algorithm)
                        
                        game_utils.set_game_completed(True)
                    # Kiểm tra lose condition
                    elif game_utils.check_lose_condition(path, True):
                        current_algorithm = game_utils.get_selected_algorithm()
                        game_popup.show_lose_message(game_utils.get_current_level(), current_algorithm)
    else:
        # Update cars khi không có algorithm execution
        manage_car.update_car()

    manage_car.draw_all(screen)
    if not lv_started:
        target_car = manage_car.cars["target_car"]
        screen.blit(console.reSize_Image(HIGHLIGHT_PATH), (target_car.offset_x, target_car.offset_y))
        
    # Draw UI elements
    button_manager.draw_all_buttons(screen)
    display_manager.draw_all_displays(screen)
    create_3d_text(screen, "RUSH HOUR", 80, 180, console.screen_size - 96)
    
    # Draw popup (phải vẽ cuối cùng để hiển thị trên cùng)
    game_popup.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()