# Máy Hút Bụi - Model-Based Reflex Agent

## Giới thiệu

Dự án này mô phỏng một **máy hút bụi thông minh** hoạt động theo mô hình **Model-Based Reflex Agent** trong môn Trí tuệ nhân tạo.

Agent di chuyển trong một căn phòng dạng ma trận `4x4`. Mỗi ô trong ma trận biểu diễn trạng thái của một vị trí trong phòng.

Quy ước:

```text
1 = Dơ
0 = Sạch
None = Chưa biết
False = Chưa đi qua
True = Đã đi qua
```

Agent bắt đầu tại vị trí `(0, 0)` và di chuyển trong ma trận. Khi gặp ô dơ, agent sẽ hút bụi. Khi gặp ô sạch, agent sẽ chọn một hướng đi hợp lệ, ưu tiên đi đến ô chưa từng thăm.

---

## Mục tiêu của chương trình

Chương trình mô phỏng quá trình hoạt động của một agent máy hút bụi:

1. Quan sát trạng thái ô hiện tại.
2. Lưu trạng thái ô hiện tại vào `model`.
3. Đánh dấu ô hiện tại là đã đi qua trong `visited`.
4. Nếu ô hiện tại dơ thì hút bụi.
5. Nếu ô hiện tại sạch thì chọn hướng di chuyển.
6. Ưu tiên di chuyển đến ô chưa từng đi qua.
7. Lặp lại cho đến khi phòng sạch hoặc vượt quá số bước giới hạn.

---

## Môi trường ban đầu

Môi trường được lưu trong biến `room`:

```python
room = [
    [1, 0, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 0, 1, 1]
]
```

Trong đó:

```text
1 = Ô dơ
0 = Ô sạch
```

Các ô dơ ban đầu là:

```text
(0,0), (0,2), (0,3), (1,0),
(2,0), (3,0), (3,2), (3,3)
```

---

## Model của Agent

Trong chương trình, `model` là bộ nhớ của agent.

Ban đầu agent chưa biết trạng thái của các ô trong phòng, nên `model` được khởi tạo như sau:

```python
model = [
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
    [None, None, None, None],
]
```

Ý nghĩa:

```text
None = Agent chưa biết trạng thái của ô đó
1    = Agent biết ô đó dơ
0    = Agent biết ô đó sạch
```

Khi agent đi tới một ô, nó quan sát trạng thái ô đó và lưu vào `model`:

```python
state = room[x][y]
model[x][y] = state
```

Nếu ô đó dơ và agent hút bụi xong, chương trình cập nhật lại:

```python
room[x][y] = 0
model[x][y] = 0
```

Nghĩa là ô đó trong phòng đã sạch, đồng thời agent cũng ghi nhớ ô đó đã sạch.

---

## Bộ nhớ visited

Ngoài `model`, chương trình còn có `visited`.

`visited` dùng để lưu những ô agent đã từng đi qua.

Ban đầu:

```python
visited = [
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
]
```

Ý nghĩa:

```text
False = Ô chưa từng đi qua
True  = Ô đã từng đi qua
```

Khi agent đứng tại ô nào, ô đó được đánh dấu là đã đi qua:

```python
visited[x][y] = True
```

Nhờ có `visited`, agent có thể ưu tiên chọn hướng đi đến những ô chưa thăm.

---

## Vì sao đây là Model-Based Reflex Agent?

Đây là **Model-Based Reflex Agent** vì agent không chỉ phản ứng với trạng thái hiện tại, mà còn có bộ nhớ bên trong để lưu thông tin môi trường.

Trong chương trình này:

```python
model[x][y] = state
visited[x][y] = True
```

Agent lưu:

- Trạng thái ô hiện tại vào `model`
- Ô đã đi qua vào `visited`

Sau đó agent dùng thông tin này để chọn hành động:

```python
if model[x][y] == 1:
    action = "SUCK"
else:
    action = choose_action_by_model(x, y, actions, visited)
```

So sánh đơn giản:

```text
Simple Reflex Agent:
Chỉ nhìn trạng thái hiện tại rồi hành động.

Model-Based Reflex Agent:
Quan sát trạng thái hiện tại, cập nhật model, ghi nhớ ô đã đi qua, rồi mới quyết định hành động.
```

---

## Tập luật của Agent

Agent hoạt động dựa trên tập luật dạng:

```text
IF điều kiện THEN hành động
```

---

### Luật 1: Nếu ô hiện tại dơ thì hút bụi

```python
if model[x][y] == 1:
    action = "SUCK"
    room[x][y] = 0
    model[x][y] = 0
```

Ý nghĩa:

```text
IF ô hiện tại dơ
    THEN hút bụi
    cập nhật room[x][y] = 0
    cập nhật model[x][y] = 0
```

Sau khi hút bụi, ô hiện tại được chuyển thành sạch.

---

### Luật 2: Nếu ô hiện tại sạch thì di chuyển

```python
else:
    actions = get_action(x, y)
    action = choose_action_by_model(x, y, actions, visited)
```

Ý nghĩa:

```text
IF ô hiện tại sạch
    THEN lấy danh sách các hướng có thể đi
    THEN chọn hướng đi dựa trên model/visited
```

---

### Luật 3: Ưu tiên đi đến ô chưa thăm

```python
if visited[new_x][new_y] == False:
    chua_tham.append(action)
```

Nếu có hướng dẫn đến ô chưa thăm:

```python
if len(chua_tham) > 0:
    return random.choice(chua_tham)
```

Ý nghĩa:

```text
IF có ô lân cận chưa đi qua
    THEN chọn ngẫu nhiên một hướng đến ô chưa đi qua
```

Nếu tất cả ô lân cận đều đã đi qua:

```python
return random.choice(actions)
```

Ý nghĩa:

```text
ELSE chọn ngẫu nhiên một hướng hợp lệ bất kỳ
```

---

## Tập luật tổng quát

Có thể viết tập luật tổng quát như sau:

```text
IF ô hiện tại dơ
    THEN hút bụi
    cập nhật ô đó trong room thành sạch
    cập nhật ô đó trong model thành sạch

ELSE IF ô hiện tại sạch
    THEN lấy danh sách hướng có thể di chuyển

IF có hướng đi đến ô chưa thăm
    THEN chọn ngẫu nhiên một hướng trong các hướng chưa thăm

ELSE
    THEN chọn ngẫu nhiên một hướng hợp lệ bất kỳ
```

---

## Các hành động của Agent

Agent có thể thực hiện các hành động sau:

| Hành động | Ý nghĩa |
|---|---|
| `SUCK` | Hút bụi |
| `UP` | Đi lên |
| `DOWN` | Đi xuống |
| `LEFT` | Đi sang trái |
| `RIGHT` | Đi sang phải |

---

## Giải thích các hàm trong chương trình

### 1. Hàm `get_action(x, y)`

```python
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
```

Hàm này trả về danh sách các hướng mà agent có thể đi tại vị trí hiện tại.

Ví dụ:

Nếu agent đang ở góc trên bên trái `(0,0)`:

```text
Không thể đi UP
Không thể đi LEFT
Có thể đi DOWN
Có thể đi RIGHT
```

Kết quả:

```python
["DOWN", "RIGHT"]
```

Nếu agent đang ở giữa ma trận, ví dụ `(1,1)`, thì có thể đi đủ bốn hướng:

```python
["UP", "DOWN", "LEFT", "RIGHT"]
```

---

### 2. Hàm `is_clean(room)`

```python
def is_clean(room):
    for row in room:
        if 1 in row:
            return False
    return True
```

Hàm này kiểm tra xem phòng đã sạch hoàn toàn chưa.

Nếu trong phòng còn số `1`, nghĩa là vẫn còn ô dơ:

```python
return False
```

Nếu không còn số `1`, nghĩa là phòng đã sạch:

```python
return True
```

---

### 3. Hàm `print_room(room)`

```python
def print_room(room):
    for row in room:
        print(row)
```

Hàm này dùng để in ma trận ra màn hình.

Nó được dùng để hiển thị:

- Ma trận phòng hiện tại
- Model của agent

---

### 4. Hàm `move(x, y, action)`

```python
def move(x, y, action):
    if action == "UP":
        x -= 1

    elif action == "DOWN":
        x += 1

    elif action == "LEFT":
        y -= 1

    elif action == "RIGHT":
        y += 1

    return x, y
```

Hàm này cập nhật vị trí mới của agent dựa trên hành động di chuyển.

Quy tắc:

```text
UP    → x giảm 1
DOWN  → x tăng 1
LEFT  → y giảm 1
RIGHT → y tăng 1
```

Ví dụ:

Nếu agent đang ở `(1,1)` và hành động là `RIGHT`, vị trí mới sẽ là:

```text
(1,2)
```

---

### 5. Hàm `choose_action_by_model(x, y, actions, visited)`

```python
def choose_action_by_model(x, y, actions, visited):
```

Hàm này chọn hành động di chuyển dựa trên `visited`.

Nó kiểm tra từng hướng có thể đi. Nếu hướng đó dẫn đến ô chưa thăm thì đưa vào danh sách `chua_tham`.

```python
chua_tham = []
```

Nếu có ô chưa thăm:

```python
return random.choice(chua_tham)
```

Agent sẽ chọn ngẫu nhiên một hướng trong danh sách ô chưa thăm.

Nếu không còn ô chưa thăm xung quanh:

```python
return random.choice(actions)
```

Agent sẽ chọn ngẫu nhiên một hướng hợp lệ bất kỳ.

---

### 6. Hàm `vacuum_cleaner_model_based(room)`

```python
def vacuum_cleaner_model_based(room):
```

Đây là hàm chính điều khiển toàn bộ hoạt động của agent.

Hàm này thực hiện các bước:

1. Đặt vị trí bắt đầu của agent là `(0,0)`.
2. Khởi tạo `model`.
3. Khởi tạo `visited`.
4. In ma trận ban đầu.
5. Agent quan sát trạng thái ô hiện tại.
6. Cập nhật `model`.
7. Cập nhật `visited`.
8. Nếu phòng sạch thì dừng.
9. Nếu ô hiện tại dơ thì hút bụi.
10. Nếu ô hiện tại sạch thì chọn hướng di chuyển.
11. In ma trận phòng hiện tại và model.
12. Lặp lại quá trình cho đến khi phòng sạch hoặc quá 50 bước.

---

## Code chính

```python
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


def move(x, y, action):
    if action == "UP":
        x -= 1

    elif action == "DOWN":
        x += 1

    elif action == "LEFT":
        y -= 1

    elif action == "RIGHT":
        y += 1

    return x, y


def choose_action_by_model(x, y, actions, visited):

    chua_tham = []

    for action in actions:
        new_x, new_y = move(x, y, action)

        if visited[new_x][new_y] == False:
            chua_tham.append(action)

    if len(chua_tham) > 0:
        return random.choice(chua_tham)

    return random.choice(actions)


def vacuum_cleaner_model_based(room):
    x, y = 0, 0
    step = 1

    model = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    visited = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
    ]

    print("Ma trận ban đầu:")
    print_room(room)
    print("=" * 40)

    while True:
        state = room[x][y]

        model[x][y] = state
        visited[x][y] = True

        print(f"\nBước {step}")
        print(f"Vị trí hiện tại: ({x}, {y})")
        print(f"Trạng thái ô: {'Dơ' if state == 1 else 'Sạch'}")

        if is_clean(room):
            print("\nPhòng đã sạch")
            break

        if model[x][y] == 1:
            action = "SUCK"
            room[x][y] = 0
            model[x][y] = 0

            print("Hành động: Hút bụi")

        else:
            actions = get_action(x, y)

            action = choose_action_by_model(x, y, actions, visited)

            print("Các hướng có thể đi:", actions)
            print("Hành động được chọn:", action)

            x, y = move(x, y, action)

        print("Ma trận phòng hiện tại:")
        print_room(room)

        print("Model của agent:")
        print_room(model)

        step += 1

        if step > 50:
            print("\nDừng vì quá số bước giới hạn")
            break


if __name__ == "__main__":
    room = [[1, 0, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 1, 1]]

    vacuum_cleaner_model_based(room)
```

---

## Cách chạy chương trình

### Bước 1: Tạo file Python

Tạo file tên:

```text
24110251_mayhutbuitrenlop.py
```

Sau đó dán code vào file.

---

### Bước 2: Chạy chương trình

Mở terminal hoặc command prompt trong thư mục chứa file và chạy:

```bash
python 24110251_mayhutbuitrenlop.py
```

Hoặc nếu dùng Python 3:

```bash
python3 24110251_mayhutbuitrenlop.py
```

---

## Ví dụ kết quả chạy

Khi chạy chương trình, màn hình sẽ hiển thị ma trận ban đầu:

```text
Ma trận ban đầu:
[1, 0, 1, 1]
[1, 0, 0, 0]
[1, 0, 0, 0]
[1, 0, 1, 1]
========================================
```

Sau đó agent hoạt động từng bước:

```text
Bước 1
Vị trí hiện tại: (0, 0)
Trạng thái ô: Dơ
Hành động: Hút bụi
Ma trận phòng hiện tại:
[0, 0, 1, 1]
[1, 0, 0, 0]
[1, 0, 0, 0]
[1, 0, 1, 1]
Model của agent:
[0, None, None, None]
[None, None, None, None]
[None, None, None, None]
[None, None, None, None]
```

Nếu ô hiện tại sạch, chương trình sẽ hiển thị các hướng có thể đi:

```text
Các hướng có thể đi: ['DOWN', 'RIGHT']
Hành động được chọn: RIGHT
```

---

## Kết quả mong đợi

Khi phòng đã sạch, chương trình sẽ in:

```text
Phòng đã sạch
```

Nếu agent chạy quá lâu, chương trình sẽ dừng ở bước giới hạn:

```text
Dừng vì quá số bước giới hạn
```

Giới hạn này được đặt bằng đoạn code:

```python
if step > 50:
    print("\nDừng vì quá số bước giới hạn")
    break
```

Mục đích là tránh trường hợp agent di chuyển ngẫu nhiên quá lâu.

---

## Số trạng thái được lưu

Ma trận có kích thước `4x4`, nên có:

```text
4 x 4 = 16 ô
```

Vì vậy:

- `model` có thể lưu tối đa 16 trạng thái ô.
- `visited` có thể lưu tối đa 16 trạng thái đã đi qua.

Các giá trị trong `model`:

```text
None = Chưa biết
1    = Dơ
0    = Sạch
```

Các giá trị trong `visited`:

```text
False = Chưa đi qua
True  = Đã đi qua
```

---

## Kiến thức AI được minh họa

### Agent

Agent là đối tượng có khả năng quan sát môi trường và thực hiện hành động.

Trong chương trình này, agent là máy hút bụi.

---

### Environment

Environment là môi trường mà agent hoạt động.

Trong chương trình này, environment là căn phòng dạng ma trận `4x4`.

---

### Percept

Percept là thông tin agent nhận được từ môi trường.

Trong chương trình này, percept là trạng thái ô hiện tại:

```python
state = room[x][y]
```

Nếu `state == 1`, agent biết ô hiện tại dơ.  
Nếu `state == 0`, agent biết ô hiện tại sạch.

---

### Action

Action là hành động mà agent thực hiện.

Trong chương trình này, action có thể là:

```text
SUCK
UP
DOWN
LEFT
RIGHT
```

---

### Model

Model là bộ nhớ bên trong của agent dùng để lưu trạng thái môi trường mà agent đã quan sát.

Trong chương trình này, `model` là ma trận `4x4` ban đầu chứa `None`.

---

### Visited

`visited` là bộ nhớ dùng để lưu các ô agent đã từng đi qua.

Nó giúp agent ưu tiên chọn hướng đến ô chưa thăm.

---

### Model-Based Reflex Agent

Model-Based Reflex Agent là agent sử dụng trạng thái hiện tại kết hợp với model bên trong để quyết định hành động.

Trong chương trình này:

```text
Agent quan sát ô hiện tại
Agent cập nhật model
Agent cập nhật visited
Nếu ô dơ thì hút
Nếu ô sạch thì chọn hướng đi dựa trên visited
```

---

## Ưu điểm

- Code đơn giản, dễ hiểu.
- Minh họa rõ mô hình Model-Based Reflex Agent.
- Có `model` để lưu trạng thái các ô đã quan sát.
- Có `visited` để lưu các ô đã đi qua.
- Agent ưu tiên đi đến ô chưa thăm.
- Không cần cài đặt thư viện ngoài, chỉ dùng thư viện `random` có sẵn trong Python.

---

## Hạn chế

- Agent vẫn chọn hướng đi ngẫu nhiên nên chưa tối ưu hoàn toàn.
- Có thể đi lòng vòng nếu các ô xung quanh đều đã thăm.
- Chương trình chỉ thiết kế cho ma trận `4x4`.
- Nếu muốn dùng ma trận kích thước khác, cần sửa điều kiện trong `get_action(x, y)`.
- Chương trình phải đặt giới hạn `50` bước để tránh lặp quá lâu.

---

## Hướng phát triển

Có thể mở rộng chương trình theo các hướng sau:

1. Cho phép nhập kích thước ma trận bất kỳ.
2. Thay `random.choice()` bằng thuật toán tìm đường thông minh hơn.
3. Lưu lịch sử percept của agent.
4. Lưu lịch sử các hành động đã thực hiện.
5. Thêm giao diện hiển thị trực quan.
6. Áp dụng BFS hoặc DFS để agent tìm đường đến ô dơ gần nhất.
7. Tối ưu đường đi để giảm số bước dọn phòng.

---

## Kết luận

Chương trình mô phỏng máy hút bụi hoạt động theo mô hình **Model-Based Reflex Agent**.

Agent có khả năng:

```text
Quan sát trạng thái ô hiện tại
Lưu trạng thái vào model
Ghi nhớ ô đã đi qua bằng visited
Hút bụi nếu ô hiện tại dơ
Di chuyển nếu ô hiện tại sạch
Ưu tiên đi đến ô chưa thăm
```

