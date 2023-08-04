"""
풀이 시간] 13:44 ~ 15:21 (1시간 37분)
상 좌 우 하 로 우선순위가 정해져있는데, BFS의 출발, 도착지를 서로 바꿀 경우
이 우선순위에 영향이 있나? 했는데 없었음.
이유 from GPT]

상하좌우 방향에 우선순위를 부여하는 것은 방향성을 추가하는 것과 같습니다.
그럼에도 불구하고 출발지와 도착지를 바꿔도 최단 경로가 변하지 않는 이유는
BFS가 모든 가능한 경로를 동시에 탐색하기 때문입니다.
BFS는 시작점에서 멀어진 순서대로 노드를 방문하며,
이 과정에서 방향 우선순위가 최종 결과에 큰 영향을 미치지 않습니다.

왜냐하면, BFS는 시작점에서 모든 방향으로 동시에 확장되기 때문에,
"상"을 먼저 방문하더라도 그 이후에 "하" "좌" "우" 방향으로도 계속해서 확장됩니다.
이 과정에서 모든 방향으로부터 도달 가능한 최단 거리를 기록하게 되므로,
출발점이나 도착점에서 시작하든, 경로의 우선순위를 상관없이 BFS는 최단 경로를 찾게 됩니다.
"""

from collections import deque

import sys
sys.stdin = open('input.txt', 'r')


def input():
    return sys.stdin.readline().rstrip()


N, M = map(int, input().split())
basecamp = list(list(map(int, input().split())) for _ in range(N))
# 해당 위치가 막혔는지, 아닌지
block = [[False] * N for _ in range(N)]
# 사람들 위치
pos = [[-1, -1] for _ in range(M)]
# 사람들 도착 여부
arrived = [False for _ in range(M)]
# 사람들 목표 편의점 위치
goal = []

# 목표 편의점 위치 저장
for _ in range(M):
    r, c = map(int, input().split())
    goal.append([r-1, c-1])

# 현재 시간
now = 0

# 델타 배열 ↑, ←, →, ↓
dr = [-1, 0, 0, 1]
dc = [0, -1, 1, 0]


def solution():
    global now
    # 베이스 캠프 찾기
    while True:
        if False in arrived:
            move()
            update()
            if now < M:
                on_basecamp(now)
            now += 1
        else:
            print(now)
            break


def move():
    for i in range(M):
        if not arrived[i] and pos[i] != [-1, -1]:
            row, col = pos[i]
            dist = bfs_from_cvs(*goal[i])

            to_row, to_col, to_dist = N, N, N*N

            # BFS로 받아온 결과에서 가장 가고싶은 곳
            for d in range(4):
                nr, nc = row + dr[d], col + dc[d]
                # 범위 내에, 갈수 있으며(블락은 이미 BFS에서 처리했고, 거리가 0이상이어야함), 우선순위
                if in_range(nr, nc) and dist[nr][nc] and (to_dist, to_row, to_col) > (dist[nr][nc], nr, nc):
                    to_row, to_col, to_dist = nr, nc, dist[nr][nc]

            pos[i] = [to_row, to_col]


def update():
    for i in range(M):
        if not arrived[i] and pos[i] == goal[i]:
            arrived[i] = True
            block[pos[i][0]][pos[i][1]] = True


def on_basecamp(num):
    dist = bfs_from_cvs(*goal[num])
    # 베이스 캠프 중 가장 가까운 곳을 찾을 거임
    row, col, length = N, N, N*N

    for r in range(N):
        for c in range(N):
            # 베이스 캠프 + 갈 수 있음(블락은 BFS에서 처리함, 그래서 0이 아닌 곳 = BFS로 닿은 곳)
            # 여기서 dist[r][c] 검사 안해서 이상한 베이스캠프로 가버렸고, 거기서 무한 루프에 걸려버림
            if basecamp[r][c] and dist[r][c]:
                if (length, row, col) > (dist[r][c], r, c):
                    length, row, col = dist[r][c], r, c

    pos[num] = [row, col]
    block[row][col] = True


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def bfs_from_cvs(c_row, c_col):
    dist = [[0] * N for _ in range(N)]
    q = deque([(c_row, c_col)])
    dist[c_row][c_col] = 1

    while q:
        r, c = q.popleft()

        for d in range(4):
            # 편의점에서 가는거라 반대 방향으로 가봄
            nr, nc = r + dr[3-d], c + dc[3-d]
            # 범위 내에, 블락이 아니고, 방문하지 않은 곳
            if in_range(nr, nc) and not block[nr][nc] and not dist[nr][nc]:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    return dist


solution()