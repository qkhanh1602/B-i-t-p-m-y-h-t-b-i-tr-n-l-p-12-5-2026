
start_state = [
    [1, 2, 3],
    [4, 0, 6],
    [7, 5, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

model = []


def print_puzzle(state):
    for row in state:
        print(row)


def is_goal(state):
    return state == goal_state


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def get_actions(x, y):
    actions = []

    if x > 0:
        actions.append("UP")

    if x < 2:
        actions.append("DOWN")

    if y > 0:
        actions.append("LEFT")

    if y < 2:
        actions.append("RIGHT")

    return actions


def move(state, action):
    x, y = find_blank(state)

    new_state = [row[:] for row in state]

    if action == "UP":
        new_x, new_y = x - 1, y

    elif action == "DOWN":
        new_x, new_y = x + 1, y

    elif action == "LEFT":
        new_x, new_y = x, y - 1

    elif action == "RIGHT":
        new_x, new_y = x, y + 1

    new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]

    return new_state


def puzzle_agent(state):
    global model

    step = 1

    while True:
        print(f"\nBước {step}")
        print("Trạng thái hiện tại:")
        print_puzzle(state)

        model = [row[:] for row in state]

        if is_goal(model):
            print("\nĐã đạt trạng thái đích!")
            break

        x, y = find_blank(model)
        actions = get_actions(x, y)

        print("Vị trí ô trống:", (x, y))
        print("Các hành động có thể đi:", actions)


        if "DOWN" in actions:
            action = "DOWN"
        elif "RIGHT" in actions:
            action = "RIGHT"
        elif "UP" in actions:
            action = "UP"
        else:
            action = "LEFT"

        print("Hành động chọn:", action)

        state = move(state, action)

        step += 1

        if step > 10:
            print("\nDừng sau 10 bước để tránh lặp vô hạn.")
            break


puzzle_agent(start_state)