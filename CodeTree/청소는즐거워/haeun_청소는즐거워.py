"""
풀이 시간 : 1시간 15분
방향에 따라 비율 다르게 하는거 구현했는데
오히려 더 복잡하고 걍 쓸데 없다. 직접 손으로 쓰는게 낫다...(우울)
나선형은 이제 조금 외웠나 싶다.
"""

N = int(input())
dust = list(list(map(int, input().split())) for _ in range(N))

# 좌 하 우 상
dr = [0, 1, 0, -1]
dc = [-1, 0, 1, 0]

# 격자 밖의 먼지 양
answer = 0

# 빗자루
broom_row, broom_col = N // 2, N // 2
broom_dir, broom_dis = 0, 0


def print_dust():
    print("======== 먼지 상태 ===========")
    for line in dust:
        print(*line)
    print()
    print(f"==== 청소기 상태 : 위치 [{broom_row, broom_col}] & 방향 = {broom_dir}, 거리 = {broom_dis}")
    print()


def check(total, percentage, row, col):
    global answer
    d = int(total * (percentage / 100))
    if 0 <= row < N and 0 <= col < N:
        dust[row][col] += d
    else:
        answer += d
    return d

def swipe():
    global answer
    total = dust[broom_row][broom_col]
    moved = 0
    # 5%
    moved += check(total, 5, broom_row + dr[broom_dir] * 2, broom_col + dc[broom_dir] * 2)
    # 7%
    moved += check(total, 7, broom_row + dr[(broom_dir - 1) % 4], broom_col + dc[(broom_dir - 1) % 4])
    moved += check(total, 7, broom_row + dr[(broom_dir + 1) % 4], broom_col + dc[(broom_dir + 1) % 4])
    # 2%
    moved += check(total, 2, broom_row + dr[(broom_dir - 1) % 4] * 2, broom_col + dc[(broom_dir - 1) % 4] * 2)
    moved += check(total, 2, broom_row + dr[(broom_dir + 1) % 4] * 2, broom_col + dc[(broom_dir + 1) % 4] * 2)
    # 10%
    moved += check(total, 10, broom_row + dr[broom_dir] + dr[(broom_dir - 1) % 4],
                   broom_col + dc[broom_dir] + dc[(broom_dir - 1) % 4])
    moved += check(total, 10, broom_row + dr[broom_dir] + dr[(broom_dir + 1) % 4],
                   broom_col + dc[broom_dir] + dc[(broom_dir + 1) % 4])
    # 1%
    moved += check(total, 1, broom_row - dr[broom_dir] + dr[(broom_dir - 1) % 4],
                   broom_col - dc[broom_dir] + dc[(broom_dir - 1) % 4])
    moved += check(total, 1, broom_row - dr[broom_dir] + dr[(broom_dir + 1) % 4],
                   broom_col - dc[broom_dir] + dc[(broom_dir + 1) % 4])

    if total > moved:
        nr = broom_row + dr[broom_dir]
        nc = broom_col + dc[broom_dir]
        if 0 <= nr < N and 0 <= nc < N:
            dust[nr][nc] += total - moved
        else:
            answer += total - moved
    dust[broom_row][broom_col] = 0


def solution():
    global broom_row, broom_col, broom_dir, broom_dis
    while True:
        if broom_dir % 2 == 0:
            broom_dis += 1

        for _ in range(broom_dis):
            broom_row += dr[broom_dir]
            broom_col += dc[broom_dir]
            swipe()
            if broom_row == 0 and broom_col == 0:
                print(answer)
                return
            # print_dust()
        broom_dir = (broom_dir + 1) % 4
        # time.sleep(2)


solution()
