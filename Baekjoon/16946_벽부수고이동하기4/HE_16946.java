/* 풀이시간 : 50분
 * 일반 BFS는 시간 초과 N*M*(N*M) -> 너무 무시했다.ㅎ 하기사 번호가 4가 붙어있어서 쎄했음...
 * 오히려 0을 기준으로 얼마나 갈 수 있는지 세어놓고, 벽의 상/하/좌/우 에서 0일 때 얼마나 사용했는지 체크?
 * -> 근데 이러면 4방향 중 이어진 데가 있을 수 있음. 중복 계산.. 을 피하려면 그룹을 체크해야됨
 * 좌표에는 그룹 번호를, 그리고 HashMap에는 해당 그룹 번호의 연결된 개수를 저장하고..
 * 벽을 볼 때, 해당 그룹을 이미 봤는지 체크하는 법은.. 배열에 체크..는 의미가 없어서, 결국 Set 초기화.
 * */

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.HashSet;

public class HE_16946 {	
	static int[] dr = {-1, 1, 0, 0};
	static int[] dc = {0, 0, -1, 1};
	
	static int N, M;
	static int[][] answer; // 벽에서 갈 수 있는 칸의 수 저장
	static boolean[][] map; // 벽 = true, 빈칸 = false
	
	static int[][] group; // 해당 빈칸이 속한 그룹의 번호 -> visited를 사용할까 고민했지만, 그룹 번호 지정은 필수이므로 합침.
	static int groupCnt = 0; // 그룹의 갯수
	static HashMap<Integer, Integer> groupInfo = new HashMap<Integer, Integer>(); // 그룹 번호별 연결된 칸의 갯수
	
	// (x, y)
	static class Pos {
		int r;
		int c;
		
		public Pos(int r, int c) {
			this.r = r;
			this.c = c;
		}
	}
	
	// 격자 내 판단
	static boolean inRange(int r, int c) {
		return 0 <= r && r < N && 0 <= c && c <M;
	}
	
	// 빈칸에서 BFS 실행
	static void bfs(int row, int col) {
		ArrayDeque<Pos> deque = new ArrayDeque<>();
		
		deque.add(new Pos(row, col));
		group[row][col] = groupCnt;
		
		// 지금 이 빈칸과 연결된 칸이 몇개인가? 본인 포함
		int cnt = 1;
		
		while(!deque.isEmpty()) {
			Pos now = deque.poll();
			
			for(int d = 0; d < 4; d++) {
				int nr = now.r + dr[d], nc = now.c + dc[d];
				if(!inRange(nr, nc)) continue; // 범위 밖
				if(group[nr][nc] > 0) continue; // 이미 체크됨
				if(map[nr][nc]) continue; // 벽임
				
				deque.add(new Pos(nr, nc));
				group[nr][nc] = groupCnt; // 어디 그룹인지 지정
				cnt++; // 연결된 칸의 수 증가
			}
		}
		
		// groupCnt번째 그룹에는 cnt 개의 빈칸들이 연결되어있다.
		groupInfo.put(groupCnt, cnt);
	}
	
	public static void main(String[] args) throws IOException {
		StringBuilder sb = new StringBuilder();
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String[] input = br.readLine().split(" ");
		N = Integer.parseInt(input[0]);
		M = Integer.parseInt(input[1]);
		map = new boolean[N][M]; // 벽, 빈칸 구분
		answer = new int[N][M]; // 벽에서 갈 수 있는 칸의 수
		group = new int[N][M]; // 빈칸이 속한 그룹의 번호
		
		for(int r = 0; r < N; r++) {
			char[] line = br.readLine().toCharArray();
			for(int c = 0; c < M; c++) {
				// 벽이면 true, 빈칸이면 false
				map[r][c] = (line[c] == '1') ? true : false;
			}
		}
		
		// 빈 칸의 그룹을 계산하러 간다. group이 0번이면 아직 그룹이 정해지지 않은 = 방문하지 않은 것이다.
		for(int r = 0; r < N; r++) {
			for(int c = 0; c < M; c++) {
				if(map[r][c] == false && group[r][c] == 0) {
					groupCnt++;
					bfs(r, c);
				}
			}
		}
		
		// 벽에서 몇 칸을 갈 수 있는지 상/하/좌/우만 확인한다.
		// 이때 그룹 중복 체크를 배열로 하려고 했는데, 그러면 결국 어느 그룹을 갔는지 따로 저장해놓고 나중에 false로 풀어야해서
		// 비록 HashSet을 매번 초기화 해줘야 하지만 어쩔 수 없이 이렇게 했다.
		for(int r = 0; r < N; r++) {
			for(int c = 0; c < M; c++) {
				if (map[r][c]) {
					// 일단 본인 포함
					int cnt = 1;
					// 해당 그룹을 확인 했는지 체크
					HashSet<Integer> used = new HashSet<>();
					// 상하좌우 연결된 곳 확인
					for(int d = 0; d < 4; d++) {
						int nr = r + dr[d], nc = c + dc[d];
						if(!inRange(nr, nc)) continue; // 범위 밖
						if(map[nr][nc]) continue; // 벽임

						// 연결된 빈칸이 속한 그룹의 번호
						int groupNumber = group[nr][nc];
						// 이미 연결된 곳을 방문 했다면, 중복 계산을 방지해야한다.
						if(used.contains(groupNumber)) continue;
						
						// 방문 처리 및 계산
						used.add(groupNumber);
						cnt += groupInfo.get(groupNumber);
					}
					// 문제 조건에서 10으로 나눈 수를 출력하라고 했다.
					answer[r][c] = cnt % 10;
				}
			}
		}
		
		// 1000 * 1000 이니깐 StringBuilder를 사용했다.
		for(int r = 0; r < N; r++) {
			for(int c = 0; c < M; c++) {
				sb.append(answer[r][c]);
			}
			sb.append("\n");
		}
		
		sb.deleteCharAt(sb.length()-1);
		System.out.println(sb.toString());
	}

}
