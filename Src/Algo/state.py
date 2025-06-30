from car import SimpleCar

FORWARD = 1
BACKWARD = -1
GOAL_X = 4

class State:
    def __init__(self, cars, parent=None, cost=0):
        self.cars = cars  # Danh sách các xe
        self.parent = parent  # Lưu cha để truy vết lời giải
        self.cost = cost

    # Dựng lại bản đồ 6x6 từ danh sách xe
    def generate_map(self):
        m = [[0] * 6 for _ in range(6)]
        for car in self.cars:
            y, x = car.coord
            for i in range(car.length):
                if car.vertical:
                    m[y + i][x] = 1
                else:
                    m[y][x + i] = 1
        return m

    # Biểu diễn trạng thái thành tuple để lưu vào explored
    def to_tuple(self):
        return tuple((car.length, car.coord, car.vertical) for car in self.cars)

    # Sinh tất cả các trạng thái con hợp lệ
    def next_states(self):
        states = []
        m = self.generate_map()
        for i, car in enumerate(self.cars):
            for dir in [FORWARD, BACKWARD]:
                if (dir == FORWARD and front_empty(m, car)) or (dir == BACKWARD and back_empty(m, car)):
                    new_cars = self.cars.copy()
                    old_car = self.cars[i]
                    new_cars[i] = SimpleCar(old_car.name, old_car.length, old_car.coord, old_car.vertical)
                    y, x = new_cars[i].coord
                    if dir == FORWARD:
                        if new_cars[i].vertical:
                            y += 1
                        else:
                            x += 1
                    else:
                        if new_cars[i].vertical:
                            y -= 1
                        else:
                            x -= 1
                    new_cars[i].coord = (y, x)
                    states.append(State(new_cars, parent=self, cost=self.cost + car.length))
        return states
    

def front_empty(map, car):
    if car.coord[car.axis] + car.length == 6:
        return False
     
    if car.vertical:
        return map[car.coord[0] + car.length][car.coord[1]] == 0
    return map[car.coord[0]][car.coord[1] + car.length] == 0

def back_empty(map, car):
    if car.coord[car.axis] == 0:
        return False
    
    if car.vertical:
        return map[car.coord[0] - 1][car.coord[1]] == 0
    return map[car.coord[0]][car.coord[1] - 1] == 0