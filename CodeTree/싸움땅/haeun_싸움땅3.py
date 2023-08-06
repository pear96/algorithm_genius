"""
풀이시간] 59분 34초
- 방향 4번 업데이트 할 때 모듈러 연산 안해줘서  index 에러.. 미치겠다

"""
import sys


def input():
    return sys.stdin.readline().rstrip()


N, M, K = map(int, input().split())
# 플레이어 정보 (grid 때문에 1번부터 시작)
row = [0] * (M+1)  # 행
col = [0] * (M+1)  # 열
power = [0] * (M+1)  # 초기 능력치
weapon = [0] * (M+1)  # 획득 총
di = [0] * (M+1)  # 방향
point = [0] * (M+1) # 점수

# 2차원 배열 for 플레이어 위치
grid = [[0] * N for _ in range(N)]
# 3차원 배열 for 총 위치
gun = [[[] for _ in range(N)] for _ in range(N)]

# 델타 배열 (상 우 하 좌)
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]


def solution():
    init()
    for _ in range(K):
        for idx in range(1, M+1):
            opponent = move(idx)
            if opponent:
                # 상대방 번호가 0이 아니면 -> 싸움
                fight(idx, opponent)
            else:
                # 0이면 총이나 주움. 사람이 없었으면 해당 위치에 기록
                grid[row[idx]][col[idx]] = idx
                pick_gun(idx)

    print(*point[1:])


def init():
    # 총 넣기
    for r in range(N):
        line = list(map(int, input().split()))
        for c in range(N):
            if line[c]:
                gun[r][c].append(line[c])

    # 플레이어 저장
    for i in range(1, M + 1):
        row[i], col[i], di[i], power[i] = map(int, input().split())
        row[i] -= 1
        col[i] -= 1
        grid[row[i]][col[i]] = i


def in_range(r, c):
    return 0 <= r < N and 0 <= c < N


def move(idx):
    """
    이동을 해보고 해당 위치에 누가 있는지 반환함 (grid는 반영 X)
    :param idx: 이동할 사람 번호
    :return: grid[row[idx][col[idx]]
    """
    r, c, d = row[idx], col[idx], di[idx]
    grid[r][c] = 0 # 원래 위치에서는 지움

    if not in_range(r+dr[d], c+dc[d]):
        di[idx] = (d+2) % 4
        d = di[idx]

    row[idx] = r + dr[d]
    col[idx] = c + dc[d]

    return grid[row[idx]][col[idx]]


def fight(me, you):
    # me는 grid에 아직 위치 이동이 반영이 안된 상태
    # 대신 row, col은 me, you가 같음
    fight_row, fight_col = row[me], col[me]

    # 일단은 me가 이겼다고 저장해놓고
    winner, loser = me, you
    # me가 지면 you랑 바꿈
    if (power[me] + weapon[me], power[me]) < (power[you] + weapon[you], power[you]):
        winner, loser = you, me

    # 승자 포인트 적립
    point[winner] += power[winner] + weapon[winner] - (power[loser] + weapon[loser])

    # 진 사람
    loser_move(loser, fight_row, fight_col)

    # 이긴 사람
    winner_move(winner, fight_row, fight_col)


def pick_gun(idx):
    r, c = row[idx], col[idx]

    # 해당 위치에 총이 없으면, 바꿀 필요도 없음
    if gun[r][c]:
        if weapon[idx]:
            gun[r][c].append(weapon[idx])

        strongest = max(gun[r][c])
        weapon[idx] = strongest
        gun[r][c].remove(strongest)


def loser_move(loser, fight_row, fight_col):
    # 싸운 위치에 총 내려놓기
    if weapon[loser]:
        gun[fight_row][fight_col].append(weapon[loser])
        weapon[loser] = 0

    d = di[loser]
    # 4방향 보면서 빈칸 나올 때 까지 회전
    for i in range(4):
        nr = fight_row + dr[(d + i) % 4]
        nc = fight_col + dc[(d + i) % 4]
        if not in_range(nr, nc) or grid[nr][nc]:
            continue
        else:
            # 전에 이동해온 사람 위치를 grid에서 안빼서 틀렸던 것 같음
            row[loser], col[loser], di[loser] = nr, nc, (d + i) % 4
            grid[nr][nc] = loser
            break

    pick_gun(loser)


def winner_move(winner, fight_row, fight_col):
    # me, you중 누가 이겼는지 몰라서 일단 위치 업데이트
    row[winner], col[winner] = fight_row, fight_col
    grid[fight_row][fight_col] = winner
    # 이긴 사람 총 줍기
    pick_gun(winner)



solution()