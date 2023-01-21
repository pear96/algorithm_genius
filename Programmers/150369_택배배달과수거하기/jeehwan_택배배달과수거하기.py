'''

그리디

한번에 가장 많이 실어서, 최대한 멀리 가서 한번에 해결...
마치 내가 일단 나가는 날, 한번에 다 처리 하려는 것 처럼

즉, 최소의 경로를 도달하기 위해서는 문제의 예시 처럼, 가장 먼 집의 경우 부터 해결해야 한다...


'''


def solution(cap, n, deliveries, pickups):
    answer = 0

    while True:

        while deliveries and deliveries[-1] == 0:
            deliveries.pop()

        while pickups and pickups[-1] == 0:
            pickups.pop()

        # print(deliveries, pickups)
        # break

        if not deliveries and not pickups:
            break

        answer += max(len(deliveries), len(pickups))

        # 뒷 쪽에서 부터 배달을 해줘야 함
        if deliveries:

            baedal = cap

            for i in reversed(range(len(deliveries))):
                # 배달최대치 보다, 배달해야할 것이 더 많다면
                if baedal < deliveries[i]:
                    deliveries[i] -= baedal
                    break
                else:
                    baedal -= deliveries[i]
                    deliveries[i] = 0

        if pickups:

            soogeo = cap

            for i in reversed(range(len(pickups))):
                # 배달최대치 보다, 배달해야할 것이 더 많다면
                if soogeo < pickups[i]:
                    pickups[i] -= soogeo
                    break

                # 그 집에 다 배달하고,
                else:
                    soogeo -= pickups[i]
                    pickups[i] = 0

    return answer * 2