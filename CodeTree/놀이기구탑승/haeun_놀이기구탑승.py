"""
풀이시간 : 1시간 13분
"""
from typing import List, Set


N: int = int(input())
cnt: int = N * N
order: List[int] = []
friends: List[Set[int]] = [set() for _ in range(cnt + 1)]
seat: List[List[int]] = [[0] * N for _ in range(N)]
score: List[int] = [0, 1, 10, 100, 1000]

dr: List[int] = [-1, 1, 0, 0]
dc: List[int] = [0, 0, -1, 1]


def in_range(r, c) -> bool:
    return 0 <= r < N and 0 <= c < N


def init() -> None:
    """
    입력 처리 함수.
    order에는 학생들의 순서를, friends에는 해당 idx의 학생이 좋아하는 친구들 4명 저장
    :return:
    """
    for _ in range(cnt):
        info: List[int] = list(map(int, input().split()))
        friends[info[0]] = set(info[1:])
        order.append(info[0])


def take_seat(idx: int) -> None:
    """
    order[idx] 학생의 자리를 찾아준다.
    :param idx: 학생의 번호 인덱스
    :return:
    """
    num: int = order[idx]
    # 비교를 위한 변수(가장 많은 친구, 가장 많은 빈칸)
    row, col = N+1, N+1
    max_empty, max_friend = 0, 0

    for r in range(N):
        for c in range(N):
            # 비어있다면
            if not seat[r][c]:
                friend, empty = 0, 0

                for d in range(4):
                    nr = r + dr[d]
                    nc = c + dc[d]
                    if not in_range(nr, nc): continue
                    if seat[nr][nc] == 0:
                        empty += 1
                    if seat[nr][nc] in friends[num]:
                        friend += 1
                # 1. 격자를 벗어나지 않는 4방향으로 인접한 칸 중 앉아있는 좋아하는 친구의 수가 가장 많은 위치로 갑니다.
                # 2. 만약 1번 조건을 만족하는 칸의 위치가 여러 곳이라면, 그 중 인접한 칸 중 비어있는 칸의 수가 가장 많은 위치로 갑니다.
                #    단 이때 격자를 벗어나는 칸은 비어있는 칸으로 간주하지 않습니다.
                # 3. 만약 2번 조건까지 동일한 위치가 여러 곳이라면, 그 중 행 번호가 가장 작은 위치로 갑니다.
                # 4. 만약 3번 조건까지 동일한 위치가 여러 곳이라면, 그 중 열 번호가 가장 작은 위치로 갑니다.

                if (max_friend, max_empty, -row, -col) < (friend, empty, -r, -c):
                    max_friend, max_empty, row, col = friend, empty, r, c

    seat[row][col] = num


def get_score() -> int:
    answer = 0
    for r in range(N):
        for c in range(N):
            me = seat[r][c]
            friend = 0

            for d in range(4):
                nr = r + dr[d]
                nc = c + dc[d]
                if in_range(nr, nc) and seat[nr][nc] in friends[me]:
                    friend += 1
            answer += score[friend]

    return answer


def solution() -> None:
    init()
    for idx in range(cnt):
        take_seat(idx)
    print(get_score())


solution()
