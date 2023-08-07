"""
풀이시간] 1시간 46분
아ㅠㅠㅠㅠㅠㅠㅠㅠ 왤케 오래걸리는데 ㅠㅠㅠㅠㅠㅠㅠㅠ

"""

from collections import deque
import sys


def input():
    return sys.stdin.readline().rstrip()


# 격자 크기, 팀의 개수, 라운드 수
N, M, K = map(int, input().split())

# 팀 별 위치 저장
# 0번 = 머리 / 1 ~ 팀원수-2 = 몸통 / 팀원수 -1 = 꼬리
members = [deque() for _ in range(M)]
# 팀 별 경로 저장
routes = [deque() for _ in range(M)]

# 팀별 인원수 저장
teams = [0] * M

# 델타 배열 (우, 상, 좌, 하)
dr = [0, -1, 0, 1]
dc = [1, 0, -1, 0]

# 점수 총 합
answer = 0


def solution():
    init()
    for rnd in range(K):
        move()
        team_num = throw(rnd)
        if team_num >= 0:
            reverse_team(team_num)
    print(answer)


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def get_team_info(r, c, idx, info, visited):
    cnt = 1
    member = deque([(r, c)])
    route = deque()

    q = deque([(r, c)])
    visited[r][c] = True

    while q:
        row, col = q.popleft()
        goal = []
        num = info[row][col]

        if num == 1:
            goal = [2]
        elif num == 2:
            goal = [2, 3]
        elif num == 3 or num == 4:
            goal = [4]

        for d in range(4):
            nr = row + dr[d]
            nc = col + dc[d]
            if in_range(nr, nc) and not visited[nr][nc] and info[nr][nc] in goal:
                visited[nr][nc] = True
                q.append((nr, nc))
                if info[nr][nc] == 2 or info[nr][nc] == 3:
                    cnt += 1
                    member.append((nr, nc))
                else:
                    route.append((nr, nc))

    members[idx] = member
    routes[idx] = route
    teams[idx] = cnt


def init():
    info = list(list(map(int, input().split())) for _ in range(N))
    visited = [[False] * N for _ in range(N)]
    team_idx = 0

    for r in range(N):
        for c in range(N):
            if info[r][c] == 1 and not visited[r][c]:
                get_team_info(r, c, team_idx, info, visited)
                team_idx += 1


def move():
    for idx in range(M):
        # 꼬리는 경로의 0번째가 된다.
        routes[idx].appendleft(members[idx].pop())
        # 경로의 끝은 머리가 된다.
        members[idx].appendleft(routes[idx].pop())


def set_info(grid, team):
    for team_idx in range(M):
        # 팀 별 멤버 수
        for idx in range(teams[team_idx]):
            # 멤버의 위치
            row, col = members[team_idx][idx]
            grid[row][col] = idx + 1
            team[row][col] = team_idx


def throw(rnd):
    global answer
    direction = (rnd // N) % 4
    position = rnd % N

    # 각 팀의 멤버를 2차원 배열에 기록
    grid = [[0] * N for _ in range(N)]
    team = [[-1] * N for _ in range(N)]
    set_info(grid, team)
    team_num = -1

    if direction == 0:
        for col in range(N):
            if grid[position][col]:
                answer += (grid[position][col]) ** 2
                team_num = team[position][col]
                break
    elif direction == 1:
        for row in range(N - 1, -1, -1):
            if grid[row][position]:
                answer += (grid[row][position]) ** 2
                team_num = team[row][position]
                break
    elif direction == 2:
        for col in range(N - 1, -1, -1):
            if grid[N - 1 - position][col]:
                answer += (grid[N - 1 - position][col]) ** 2
                team_num = team[N - 1 - position][col]
                break
    else:
        for row in range(N):
            if grid[row][N - 1 - position]:
                answer += (grid[row][N - 1 - position]) ** 2
                team_num = team[row][N - 1 - position]
                break

    return team_num


def reverse_team(idx):
    members[idx].reverse()
    routes[idx].reverse()


solution()