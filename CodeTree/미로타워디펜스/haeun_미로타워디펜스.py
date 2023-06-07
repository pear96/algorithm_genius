"""
풀이시간 : 2시간 이상
"""

answer = 0
N, M = map(int, input().split())
grid = list(list(map(int, input().split())) for _ in range(N))

# 델타 우 하 좌 상
dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]

HALF = N // 2


def print_grid(turn):
    print(f" >>>>>>>>>> {turn} <<<<<<<<<< ")
    for line in grid:
        print(*line)
    print()


# 입력받은 1차원 배열을 그리드에 채운다.
# 4개 이상의 몬스터가 연속으로 있는지도 확인한다.
def fill_grid(monsters):
    new_grid = [[0] * N for _ in range(N)]
    row, col = HALF, HALF
    dct, length = 2, 1

    m_idx = 0
    m_cnt = len(monsters)
    more_than_four = False

    if m_cnt > 0:
        # 4마리 이상 인 몬스터가 있는지 확인
        prv_num, prv_cnt = monsters[0], 1
        for i in range(1, m_cnt):
            if monsters[i] == prv_num:
                prv_cnt += 1
                if prv_cnt > 3:
                    more_than_four = True
                    break
            else:
                prv_cnt = 1
                prv_num = monsters[i]

        # 달팽이
        while row or col:
            for _ in range(length):
                row += dr[dct]
                col += dc[dct]

                if not row and not col:
                    break

                new_grid[row][col] = monsters[m_idx]
                m_idx += 1
                if m_idx == m_cnt:
                    row, col = 0, 0
                    break
            dct = (dct - 1) % 4
            if dct == 0 or dct == 2:
                length += 1

    # 복사 붙여넣기
    for r in range(N):
        grid[r] = new_grid[r][:]

    # 4마리 이상 있었는지 반환
    return more_than_four


# 플레이어 공격
def attack(dct, power):
    global answer
    row, col = HALF, HALF

    for _ in range(power):
        row += dr[dct]
        col += dc[dct]
        answer += grid[row][col]
        grid[row][col] = 0


# 한칸씩 돌면서 몬스터 리스트에 담아 빈칸 없애기
def line_monster():
    monsters = []
    row, col = HALF, HALF
    dct, length = 2, 1  # 우/하/좌/상 이라 좌 부터 시작!

    while row or col:
        for _ in range(length):
            row += dr[dct]
            col += dc[dct]

            if not row and not col:
                break

            if grid[row][col]:
                monsters.append(grid[row][col])
        dct = (dct - 1) % 4
        if dct == 0 or dct == 2:
            length += 1

    return monsters


# 달팽이 + 몬스터 수 세면서 삭제
def kill_more_than_four():
    global answer
    # 몬스터 죽인거 빼고 반환하는 1차원 배열 [1, 2, 3 ... ]
    monsters = []
    row, col = HALF, HALF
    dct, length = 2, 1

    prv_num, prv_cnt = grid[row][col-1], 0

    # 플레이어 왼쪽에 몬스터가 있으면
    if prv_num:
        # 달팽이로 돌면서
        while row or col:
            for _ in range(length):
                row += dr[dct]
                col += dc[dct]

                if not row and not col:
                    break
                # 끝까지 안갔는데 더 이상 몬스터가 없음
                if prv_num == 0 and grid[row][col] == 0:
                    row, col = 0, 0
                    break

                # 이전 숫자와 같으면 개수 추가
                if grid[row][col] == prv_num:
                    prv_cnt += 1
                else:
                    # 4개 이상이면 삭제라 점수 추가
                    if prv_cnt > 3:
                        answer += (prv_num * prv_cnt)
                    # 3개 이하면 monsters에 추가
                    else:
                        # monsters += [1, 1, 1]
                        monsters += [prv_num] * prv_cnt
                    # 바뀐 숫자므로 어쨌든 1로 초기화
                    prv_cnt = 1
                    prv_num = grid[row][col]
            # 달팽이 때문에 방향 전환
            dct = (dct - 1) % 4

            if dct == 0 or dct == 2:
                length += 1

    # 4마리 이상인 애들은 빠진 1차원 몬스터 배열
    return monsters


def pair_monster():
    result = []

    row, col = HALF, HALF
    dct, length = 2, 1

    prv_num, prv_cnt = grid[row][col - 1], 0

    # 플레이어 왼쪽에 숫자가 있는 경우
    if prv_num:
        # 달팽이로 돌면서
        while row or col:
            for _ in range(length):
                row += dr[dct]
                col += dc[dct]

                if not row and not col:
                    break

                if prv_num == 0 and grid[row][col] == 0:
                    return result
                # 이전 숫자와 같으면 개수 추가
                if grid[row][col] == prv_num:
                    prv_cnt += 1
                else:
                    result += [prv_cnt, prv_num]
                    prv_cnt = 1
                    prv_num = grid[row][col]
            dct = (dct - 1) % 4
            # 좌, 우 움직임에서 거리가 증가해야함
            if dct == 0 or dct == 2:
                length += 1

    return result


def solution():
    for _ in range(M):
        d, p = map(int, input().split())
        # 플레이어는 상하좌우 방향 중 주어진 공격 칸 수만큼 몬스터를 공격하여 없앨 수 있습니다.
        attack(d, p)

        # 비어있는 공간만큼 몬스터는 앞으로 이동하여 빈 공간을 채웁니다.
        # [1, 2, 3, 2 ....]
        monsters = line_monster()

        # 이때 몬스터의 종류가 4번 이상 반복하여 나오면
        while fill_grid(monsters):
            # 해당 몬스터 또한 삭제됩니다. 해당 몬스터들은 동시에 사라집니다.
            monsters = kill_more_than_four()
            # 삭제된 이후에는 몬스터들을 앞으로 당겨주고, 4번 이상 나오는 몬스터가 있을 경우 또 삭제를 해줍니다.
        # 4번 이상 나오는 몬스터가 없을 때까지 반복해줍니다.
        # 삭제가 끝난 다음에는 몬스터를 차례대로 나열했을 때 같은 숫자끼리 짝을 지어줍니다.
        # 이후 각각의 짝을 (총 개수, 숫자의 크기)로 바꾸어서 다시 미로 속에 집어넣습니다.
        monsters = pair_monster()
        fill_grid(monsters)

    print(answer)

solution()