import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class HE_2467 {
	static int N;
	static int[] answer = new int[2];
	static int[] liquid;
	
	static void binary () {
		int leastGap = Integer.MAX_VALUE;
		//  [-99, -2, -1, 4, 98]
		// liquid 하나씩 보면서, 짝지를 찾아준다.
        for(int l = 0; l < N-1; l++) {
            int now = liquid[l];
            // 내 다음부터 끝까지 보고
            int low = l+1, high = N - 1;
            int mid;

            while(low <= high) {
                mid = (low + high) / 2;
                
                // 갭이 더 작으면 업데이트
                if (leastGap > Math.abs(now + liquid[mid])) {
                    leastGap = Math.abs(now + liquid[mid]);
                    answer[0] = now;
                    answer[1] = liquid[mid];
                }
                
                // 합이 - 면 더 큰 용액이랑 섞엇을 때 0에 가까워질 수 있으니깐
                // 용액이 정렬되어있으므로, low값 올려보는 시도 함.
                if (now + liquid[mid] <= 0) {
                    low = mid + 1;
                } else {
                	// 합이 + 면 더 작은 용액이랑 섞었을 때 0에 가까워질 수 있으니깐 high값 내려봄.
                    high = mid - 1;
                }
            }
        }
	}
	
	static void twoPointer() {
		int left = 0;
		int right = N-1;
		int sum = Integer.MAX_VALUE;
		
		while (left < right) {
			// 값 갱신
			if (Math.abs(sum) > Math.abs(liquid[left] + liquid[right])) {
				sum = liquid[left] + liquid[right];
				answer[0] = liquid[left];
				answer[1] = liquid[right];
			}
			
			// 갱신은 했고, 더 있나 탐색해보기
			// 합이 0보다 크면 right가 양수에 클 가능성이 높은 값이니 얘를 줄여보고
			// 0보다 작다면 left가 음수에 작을 가능성이 높은 값이니 얘를 키워본다.
			if (liquid[left] + liquid[right] > 0) {
				right--;
			} else left++;
		}
	}
	
	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		N = Integer.parseInt(br.readLine());
		// 이미 정렬된 값이 저장됨
		liquid = new int[N];
		
		StringTokenizer st = new StringTokenizer(br.readLine());
		for(int i = 0; i < N; i++) {
			liquid[i] = Integer.parseInt(st.nextToken());
		}
		Arrays.sort(liquid);
		
//		twoPointer();
		binary();
		
		System.out.println(answer[0] + " " + answer[1]);
		
	}

}
