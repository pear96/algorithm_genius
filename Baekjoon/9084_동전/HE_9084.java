
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class HE_9084 {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		StringBuilder sb = new StringBuilder();
		int T = Integer.parseInt(br.readLine());
		// 테스트케이스
		for(int tc = 0; tc < T; tc++) {
			int N = Integer.parseInt(br.readLine());
			// 동전 저장
			int[] coins = new int[N];
			StringTokenizer st = new StringTokenizer(br.readLine());
			for(int i = 0; i < N; i++) {
				coins[i] = Integer.parseInt(st.nextToken());
			}
			// 목표 금액
			int goal = Integer.parseInt(br.readLine());
			// 해당 금액을 만드는 경우의 수
			int[] dp = new int[10001];
			
			// !! 주의!! 바깥 반복문이 '동전'이어야 하는 이유
			// 처음엔 바깥이나 내부나 동전과 금액이 상관 없을거라고 생각했음.
			// 근데 자꾸 틀려서 보니 중복을 처리하지 못함
			// 3번째 테스트 케이스에서 17의 경우의 수가 1이 아니라 2가 나옴.
			// 왜냐면 dp[12] + 5랑, dp[10] + 7 가 같은 경우인데 다르게 계산했기 때문이다.
			// 바깥 반복문이 동전이라면, 동전을 무한정 사용할 수 있다고 가정하고, 각 동전을 기준으로 금액을 만들어나간다.
			// -> 동전을 독립적으로 취급하여 그 동전을 사용해서 만들 수 있는 금액에 초점
			// 바깥 반복문이 금액이라면, 모든 동전을 통틀어 해당 금액을 만드는 걸 보는데, 중복이 발생할 수 있다.
			// -> 위의 예시 처럼 같은 경우인데 다르게 처리함.

			// 1원 동전 보는 중 : dp[3] += dp[2] => [1+1] ,[2] => [1+1+1] , [2+1]
			// 2원 동전 보는 중 : dp[3] += dp[1] => [1+2]
			
			for(int coin: coins) {
				for(int money = 0; money <= goal; money++) {
					if (coin == money) {
						dp[coin]++;
					}
					else if (money - coin > 0){
						dp[money] += dp[money - coin];
					}
				}
			}
			sb.append(dp[goal]+"\n");
			
//			for(int i = 0; i <= goal; i++) {
//				System.out.println("금액 : " + i + "의 경우의 수 " + dp[i]);
//			}
			
		}
		sb.deleteCharAt(sb.length()-1);
		System.out.println(sb.toString());
	}
}
