import pygame
import console
import car
from board import *
from defs import *
from manage_car import *
from ui import *
from utils import GameUtils
from Algo import *

pygame.init()
console = console.Console()
console.convertMatrix()

screen = pygame.display.set_mode((console.screen_size, console.screen_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour') 
running = True  
board = Board(console.reSize_Image(MAP_PATH), SQUARE_SIZE_DEFAULT, 0, 0)

# Initialize game objects
main_car = car.MainCar(0, 2, console.reSize_Image(MAIN_CAR_PATH))
truck_0 = car.Car("truck_0", 4, 0, console.reSize_Image(CAR_PATH + "truck_0.png"), False, "down")
car_1 = car.Car("car_1", 4, 4, console.reSize_Image(CAR_PATH + "car_1.png"), True, "right")
car_2 = car.Car("car_2", 3, 3, console.reSize_Image(CAR_PATH + "car_2.png"), False, "down")

manage_car = ManageCar()   
manage_car.add_car(main_car)
manage_car.add_car(truck_0)
manage_car.add_car(car_1)
manage_car.add_car(car_2)

# Initialize UI and Utils
button_manager = ButtonManager(console)
display_manager = DisplayManager(console)
game_popup = GamePopup(console)
game_utils = GameUtils(console)

# Game objects dictionary for easy management
game_objects = {
    "manage_car": manage_car,
    "board": board
}

searched = False
path = []
current_step = 0
moves_count = 0
step_timer = 0
is_moving = False
waiting_for_next_step = False
algorithm_execution_completed = False

while running:  
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            exit()  
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
                        game_objects = game_utils.handle_algorithm_selection(clicked_popup_button, game_objects)
                        
                        # UPDATE DISPLAY SAU
                        algorithm_display_text = f"ALGORITHM :  {clicked_popup_button}"
                        display_manager.update_display_text("algorithm", algorithm_display_text)
                        
                        # ẨN POPUP
                        game_popup.hide()
                        
                        # Reset variables
                        searched = False
                        path = []
                        current_step = 0
                        step_timer = 0
                        is_moving = False
                        waiting_for_next_step = False
                        moves_count = 0
                        algorithm_execution_completed = False
                        
                        # Debug
                        print(f"Display text: {algorithm_display_text}")
                        print(f"Utils algorithm: {game_utils.get_selected_algorithm()}")
                        
                    elif game_popup.popup_type == "win":
                        # Xử lý win popup
                        game_objects = game_utils.handle_win_popup_action(clicked_popup_button, game_objects, game_popup)
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
                continue
            
            # Kiểm tra click vào main buttons
            clicked_button = game_utils.check_button_click(mouse_pos, button_manager)
            if clicked_button:
                if clicked_button == "exit":
                    running = False
                    game_utils.handle_button_action(clicked_button, game_objects)
                elif clicked_button == "reset":
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects)
                    # Reset algorithm variables
                    searched = False
                    path = []
                    current_step = 0
                    step_timer = 0
                    is_moving = False
                    waiting_for_next_step = False
                    moves_count = 0
                    algorithm_execution_completed = False
                    # Cập nhật display
                    display_manager.update_display_text("moves", "MOVES :  0")
                elif clicked_button == "play":
                    # Hiển thị popup algorithm selection
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects, game_popup)
                else:
                    game_objects = game_utils.handle_button_action(clicked_button, game_objects)

    # Run search - chỉ chạy khi không có popup hiển thị
    if not searched and not game_popup.visible and not algorithm_execution_completed:
        cars = []
        for car in game_objects["manage_car"].cars.values():
            cars.append(SimpleCar(car.name, car.length_grid, (car.y, car.x), not car.is_horizontal))
        start = State(cars)
        
        # Lấy algorithm được chọn
        selected_algo = game_utils.get_selected_algorithm()
        print(f"Running search with algorithm: {selected_algo}")
        
        # Chọn algorithm implementation
        if selected_algo == "BFS":
            path = ids(start)
        elif selected_algo == "IDS":
            path = ids(start)  # IDS implementation
        elif selected_algo == "A STAR":
            path = ids(start)
        elif selected_algo == "UCS":
            path = ids(start)
        else:
            path = ids(start)

        current_step = 0
        step_timer = current_time
        searched = True
        print(f"Found path with {len(path)} steps using {selected_algo}")

    # Draw game elements
    screen.blit(game_objects["board"].image, (game_objects["board"].offset_x, game_objects["board"].offset_y))
    
    # Algorithm execution with step timing - chỉ chạy khi không có popup
    if searched and path and not game_popup.visible and not algorithm_execution_completed:
        # Kiểm tra xem có xe nào đang di chuyển không
        cars_moving = game_objects["manage_car"].update_car()
        
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
                        if car.name in game_objects["manage_car"].cars:
                            game_objects["manage_car"].cars[car.name].y, game_objects["manage_car"].cars[car.name].x = car.coord
                    
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
                    algorithm_execution_completed = True
                    
                    # Kiểm tra win condition
                    if game_utils.check_win_condition(game_objects):
                        # Hiển thị win popup với algorithm được sử dụng
                        current_algorithm = game_utils.get_selected_algorithm()
                        game_popup.show_win_message(game_utils.get_current_level(), moves_count, current_algorithm)
                        game_utils.set_game_completed(True)
    else:
        # Update cars khi không có algorithm execution
        game_objects["manage_car"].update_car()

    game_objects["manage_car"].draw_all(screen)
    
    # Draw UI elements
    button_manager.draw_all_buttons(screen)
    display_manager.draw_all_displays(screen)
    create_3d_text(screen, "RUSH HOUR", 80, 180, console.screen_size - 96)
    
    # Draw popup (phải vẽ cuối cùng để hiển thị trên cùng)
    game_popup.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()