"""
풀이시간 : 27분
두뇌 재활하려고 품 ㅠㅠ
"""


N, M = map(int, input().split())

tree = list(list(map(int, input().split())) for _ in range(N))
nutri = [[0] * N for _ in range(N)]

dr = [0, 0, -1, -1, -1, 0, 1, 1, 1]
dc = [0, 1, 1, 0, -1, -1, -1, 0, 1]


def print_tree():
    print("========= 나무 출력 ==========")
    for line in tree:
        print(*line)
    print()


def print_nutri():
    print("========= 영양제 출력 ==========")
    for line in nutri:
        print(*line)
    print()


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def move_nutrition(d, p):
    """
    특수 영양제를 이동 규칙에 따라 이동시킵니다.
    특수 영양제를 이동 시킨 후 해당 땅에 특수 영양제를 투입합니다.

    :param d: 방향
    :param p: 거리
    :return:
    """
    moved = [[0] * N for _ in range(N)]

    # 이동
    for r in range(N):
        for c in range(N):
            if nutri[r][c]:
                nr = (r + dr[d] * p) % N
                nc = (c + dc[d] * p) % N
                moved[nr][nc] = 1  # 영양제 이동하고
                tree[nr][nc] += 1  # 영양제 있는 나무 높이 성장

    # 반영(투입)
    for r in range(N):
        nutri[r] = moved[r][:]


def grow():
    """
    특수 영양제를 투입한 리브로수의 대각선으로 인접한 방향에 높이가 1 이상인 리브로수가 있는 만큼 높이가 더 성장합니다.
    대각선으로 인접한 방향이 격자를 벗어나는 경우에는 세지 않습니다.(2,4,6,8번 방향)
    :return:
    """
    for r in range(N):
        for c in range(N):
            if nutri[r][c]:
                cnt = 0
                for d in range(1, 5):
                    nr = r + dr[d*2]
                    nc = c + dc[d*2]

                    if in_range(nr, nc) and tree[nr][nc]:
                        cnt += 1
                tree[r][c] += cnt


def buy_nutri():
    for r in range(N):
        for c in range(N):
            if nutri[r][c]:
                # 이미 영양제를 맞았던 곳
                nutri[r][c] = 0
            elif tree[r][c] >= 2:
                # 영양제를 맞지 않았는데 높이가 2 이상이라 영양제 구매
                tree[r][c] -= 2
                nutri[r][c] = 1


def get_answer():
    answer = 0
    for r in range(N):
        for c in range(N):
            if tree[r][c]:
                answer += tree[r][c]

    print(answer)




def solution():
    # 좌하단 4칸에 특수 영양제
    for r in range(2):
        for c in range(2):
            nutri[N-r-1][c] = 1

    for _ in range(M):
        d, p = map(int, input().split())
        move_nutrition(d, p)
        grow()
        buy_nutri()
    get_answer()




solution()