"""
풀이 시간 : 1시간 41분
- 2차원 배열이 전역변수인데도 global을 붙여야 하는 이유??
=> 전역 변수인 배열을 함수 안에서 global 없이 수정이 가능하다.
=> 하지만 함수 안에서 global 없이 새로 '할당'할 경우, 이는 함수 안의 새로운 지역 변수가 된다.
"""

from collections import deque

# import sys
# sys.stdin = open('input.txt', 'r')

N, M, K = map(int, input().split())
# 공격력 2차원 배열
power = list(list(map(int, input().split())) for _ in range(N))
# 공격 시점 2차원 배열
history = [[0] * M for _ in range(N)]
# 공격과 관련되었는지 기록 2차원 배열
fight = [[False] * M for _ in range(N)]

# 공격을 위한 델타 배열 (8 방향)
dr = [0, 1, 1, 1, 0, -1, -1, -1]
dc = [1, 1, 0, -1, -1, -1, 0, 1]


def solution():
    global fight
    for turn in range(1, K+1):
        # 1. 포탑이 1개만 남으면 중지
        if not check():
            break
        # 턴마다 초기화가 필요함
        fight = [[False] * M for _ in range(N)]
        # 2. 공격자 선정 -> 공격자 위치 [r, c] 반환
        ar, ac = pick_attacker(turn)
        # 3. 공격 대상 선정
        vr, vc = pick_victim()
        # 4. 공격 (레이저 or 포탄)
        attack(ar, ac, vr, vc)
        # 5. 포탑 부서짐
        destroy()
        # 6. 포탑 정비
        fix()

    get_answer()


def check():
    alive = 0
    for r in range(N):
        for c in range(M):
            if power[r][c]:
                alive += 1

    return True if alive > 1 else False


def fix():
    for r in range(N):
        for c in range(M):
            if not fight[r][c] and power[r][c] > 0:
                power[r][c] += 1


def destroy():
    for r in range(N):
        for c in range(M):
            if power[r][c] < 0:
                power[r][c] = 0


def pick_attacker(turn):
    row, col, ability, last = -1, -1, 5001, -1

    for r in range(N):
        for c in range(M):
            a, l = power[r][c], history[r][c]
            if power[r][c] == 0:
                continue
            if (ability, -last, -(row+col), -col) > (a, -l, -(r+c), -c):
                # r, c에 있는 포탑이 공격력이 더 낮을 때
                # 공격력은 같은데 마지막 공격 시간이 더 클 때 (- 붙임)
                # 공격 시간도 같은데 행,열의 합이 더 클 때 (-붙임)
                # 이마저도 같다면 열 값이 더 클 때 (-붙임)
                ability, last, row, col = a, l, r, c

    # print(f"[공격자 선정]    우리중 최약체!! 힘 =  {ability}, 기록 = {last}, 위치 = {row, col}")
    history[row][col] = turn

    return row, col


def pick_victim():
    row, col, ability, last = 11, 11, -1, K+1

    for r in range(N):
        for c in range(M):
            a, l = power[r][c], history[r][c]
            if power[r][c] == 0:
                continue
            if (ability, -last, -(row + col), -col) < (a, -l, -(r + c), -c):
                # r, c에 있는 포탑이 공격력이 더 클 때
                # 공격력은 같은데 마지막 공격 시간이 더 작을 때 (- 붙임)
                # 공격 시간도 같은데 행,열의 합이 더 작을 때 (-붙임)
                # 이마저도 같다면 열 값이 더 작을 때 (-붙임)
                ability, last, row, col = a, l, r, c

    # print(f"[대상자 선정]    우리중 최강체!! 힘 =  {ability}, 기록 = {last}, 위치 = {row, col}")

    return row, col


def attack(ar, ac, vr, vc):
    # 공격자의 공격력을 대상자 선정 전에 올려서 오류남
    power[ar][ac] += N+M
    # 일단 공격자 대상자는 공격에 휘말림
    fight[ar][ac] = True
    fight[vr][vc] = True

    if not lazer(ar, ac, vr, vc):
        bomb(ar, ac, vr, vc)


def lazer(ar, ac, vr, vc):
    # 레이저 공격 시도
    route = [[False] * M for _ in range(N)]
    route[ar][ac] = [ar, ac]
    q = deque([[ar, ac]])

    while q:
        r, c = q.popleft()

        for d in range(4):
            nr = (r + dr[d*2]) % N
            nc = (c + dc[d*2]) % M
            if not power[nr][nc]:
                continue
            if not route[nr][nc]:
                route[nr][nc] = [r, c]
                q.append([nr, nc])

    # 레이저 공격이 된다!
    if route[vr][vc]:
        # 공격 대상자는 쓴 맛을 본다.
        power[vr][vc] -= power[ar][ac]

        # 경로에 있던 애들도 피해를 본다.
        pr, pc = route[vr][vc]
        while pr != ar or pc != ac:
            power[pr][pc] -= power[ar][ac] // 2
            fight[pr][pc] = True
            pr, pc = route[pr][pc]
        return True
    else:
        return False


def bomb(ar, ac, vr, vc):
    # 레이저 공격 실패해서 폭탄 떨구러 옴
    power[vr][vc] -= power[ar][ac]

    for d in range(8):
        nr = (vr + dr[d]) % N
        nc = (vc + dc[d]) % M
        if nr == ar and nc == ac:
            continue
        power[nr][nc] -= power[ar][ac] // 2
        fight[nr][nc] = True


def get_answer():
    vr, vc = pick_victim()
    print(power[vr][vc])


solution()