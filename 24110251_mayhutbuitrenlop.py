import random


def get_action(x, y):
    actions = []

    if x > 0:
        actions.append("UP")

    if x < 3:
        actions.append("DOWN")

    if y > 0:
        actions.append("LEFT")

    if y < 3:
        actions.append("RIGHT")

    return actions


def is_clean(room):
    for row in room:
        if 1 in row:
            return False
    return True


def print_room(room):
    for row in room:
        print(row)


def vacuum_cleaner(room):
    x, y = 0, 0
    step = 1

    print("Ma trận ban đầu")
    print_room(room)
    print("=" * 40)

    while True:
        state = room[x][y]

        print(f"\nBước {step}")
        print(f"Vị trí hiện tại: ({x}, {y})")
        print(f"Trạng thái ô: {'Dơ' if state == 1 else 'Sạch'}")

        if is_clean(room):
            print("\nPhòng đã sạch")
            break

        if state == 1:
            action = "SUCK"
            room[x][y] = 0
            print("Hành động: Hút bụi")

        else:
            actions = get_action(x, y)
            action = random.choice(actions)

            print("Các hướng có thể đi:", actions)
            print("Hành động được chọn:", action)

            if action == "UP":
                x -= 1

            elif action == "DOWN":
                x += 1

            elif action == "LEFT":
                y -= 1

            elif action == "RIGHT":
                y += 1

        print("Sau khi hút :")
        print_room(room)

        step += 1


if __name__ == "__main__":
    room = [[1, 0, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 1, 1]]

    vacuum_cleaner(room)
