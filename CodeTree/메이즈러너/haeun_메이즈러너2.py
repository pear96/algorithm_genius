"""
풀이시간 : 1시간 43분
"""

N, M, K = map(int, input().split())
maze = list(list(map(int, input().split())) for _ in range(N))
runner = list([0, 0] for _ in range(M))
left = M

for i in range(M):
    r, c = map(int, input().split())
    runner[i] = [r - 1, c - 1]

exit_row, exit_col = map(int, input().split())
exit_row, exit_col = exit_row - 1, exit_col - 1

answer = 0

dr = [0, 0, 1, -1]
dc = [-1, 1, 0, 0]


def print_runner():
    print("--------- 참가자 출력 ----------")
    for i in range(M):
        print(f"{i}번 참가자 위치 : {runner[i]} vs 탈출구 : {exit_row, exit_col}")
    print()


def print_maze():
    print("--------- 미로 출력 ----------")
    for line in maze:
        print(*line)
    print()


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


# 참가자들 이동
def move_runners():
    global left, answer
    """
    1초마다 모든 참가자는 한 칸씩 움직입니다.
    한 칸에 2명 이상의 모험가가 있을 수 있습니다.
    -> (참가자를 2차원 맵에 직접 기록하지 않아 상관 없음)
    :return:
    """

    # 모든 참가자는 동시에 움직입니다.
    for i in range(M):
        row, col = runner[i]
        new_row, new_col = row, col
        # 두 위치 (x1,y1), (x2,y2)의 최단거리는 ∣x1−x2∣+∣y1−y2∣로 정의됩니다.
        distance = abs(row - exit_row) + abs(col - exit_col)

        for d in range(4):
            nr = row + dr[d]
            nc = col + dc[d]
            # 상하좌우로 움직일 수 있으며, 벽이 없는 곳으로 이동할 수 있습니다.
            # 움직인 칸은 현재 머물러 있던 칸보다 출구까지의 최단 거리가 가까워야 합니다.
            # 움직일 수 있는 칸이 2개 이상이라면, 상하로 움직이는 것을 우선시합니다.
            # -> 좌,우,하,상 순서로 움직여서 가능한 애들 중 상이 마지막이 되도록 함
            # 참가가가 움직일 수 없는 상황이라면, 움직이지 않습니다.
            if in_range(nr, nc):
                # 출구에 도달하면 즉시 탈출
                if nr == exit_row and nc == exit_col:
                    new_row, new_col = -1, -1
                    left -= 1
                    break
                if maze[nr][nc] == 0 and distance > (abs(nr - exit_row) + abs(nc - exit_col)):
                    # 조건에 맞지 않으면 원래 자리 그대로 머물도록
                    new_row, new_col = nr, nc

        if row != new_row or col != new_col:
            answer += 1
        runner[i] = [new_row, new_col]


# 참가자의 행 / 열과 탈출구의 행 / 열을 각각 비교해서 시작점을 찾아내 반환
def compare_pos(a, b, l):
    small = 0  # a, b 중에 더 작은 수
    gap = 0  # a, b 중 큰 수에서 l 뺀 값

    if a >= b:
        # a, b가 같거나 a가 큰 경우
        gap, small = a - l, b
    else:
        gap, small = b - l, a

    # gap이 0 이하이면 시작점을 0으로 하는게 낫다.
    if gap <= 0:
        return 0
    else:
        # 아니라면 더 위 or 왼쪽에 있는 점과 더 아래 or 오른쪽에 있는 점에서 변의 크기만큼 뺀 값 중 더 작은 것이 시작점
        return min(small, gap)


# 한 참가자의 위치 기준으로 시작점과 크기 반환
def get_rectangle(r, c):
    # 정사각형 크기
    size = max(abs(r - exit_row), abs(c - exit_col))
    # 시작점
    row = compare_pos(r, exit_row, size)
    col = compare_pos(c, exit_col, size)
    return row, col, size + 1


# 반환받은 정사각형 정보를 기준으로 회전 진행
# 미로 뿐만 아니라 출구, 참가자도 회전해야함
def rotate_maze():
    global exit_row, exit_col
    # 가장 작은 크기의 정사각형 정보
    rec_row, rec_col, rec_size = 10, 10, 10

    for i in range(M):
        if runner[i] != [-1, -1]:
            row, col, size = get_rectangle(*runner[i])
            if (rec_size, rec_row, rec_col) > (size, row, col):
                rec_row, rec_col, rec_size = row, col, size

    # 회전한 미로 저장
    moved = [[0] * rec_size for _ in range(rec_size)]

    # 90도 회전 + 내구도 1 감소
    for r in range(rec_size):
        for c in range(rec_size):
            moved[c][rec_size - r - 1] = maze[rec_row + r][rec_col + c]
            if moved[c][rec_size - r - 1]:
                moved[c][rec_size - r - 1] -= 1

    # 위의 작업한거 미로에 반영하기
    for r in range(rec_size):
        for c in range(rec_size):
            maze[rec_row + r][rec_col + c] = moved[r][c]

    # 탈출구도 회전
    exit_row -= rec_row
    exit_col -= rec_col
    exit_row, exit_col = exit_col, rec_size - exit_row - 1
    exit_row += rec_row
    exit_col += rec_col

    # 참가자도 회전
    for i in range(M):
        # 아직 탈출 안했고
        r, c = runner[i]
        if r != -1 and c != -1 \
                and rec_row <= r < rec_row + rec_size \
                and rec_col <= c < rec_col + rec_size:
            r -= rec_row
            c -= rec_col
            runner[i] = [c, rec_size - r - 1]
            runner[i][0] += rec_row
            runner[i][1] += rec_col


def solution():
    for _ in range(K):
        move_runners()
        if left == 0:
            break
        rotate_maze()

    print(answer)
    print(exit_row + 1, exit_col + 1)


solution()
