#과제 해결 방법
#1. 현재 상황 (global_sep)을 보고 누구 공격차례인지 판단.
#2. 모든 경우의 수를 생각 (백트래킹)
#3. res값이 업데이트 되지 않으면 승부가 나지 않은 것
#4. 백트래킹 매 턴마다 게임이 끝나는지 확인하고 게임이 끝나는 상황이면 -1을 반환하고 종료
#5. 내 턴이 아닌 곳에서 종료되면 상대방이 이기는 것으로, 상대 턴에서 종료되면 내가 이기는 것으로 하기 위해서
# return값에 -를 붙여서 1은 -1으로 -1은 1로 반환되도록한다.

#아무도 두지 않은 경우(게임 시작 직후)에는 판단이 무의미 하므로 판단하는 함수 호출을
#숫자 입력 이후로 두었습니다.


class TicTacToe:
    def __init__(self):
        self.N = 3
        #3X3 맵 생성
        self.map = [['E' for _ in range(self.N)] for _ in range(self.N)]    # E: 빈 공간(Empty)
        
        #맵 인덱스
        self.map_index_description = [h*self.N + w for h in range(self.N) for w in range(self.N)]
        
        self.player_types = ('X', 'O')  # 선공: X, 후공: O
        self.global_step = 0

        #승,무,패 판단
        self.win_reward = 1.0
        self.defeat_reward = -1.0
        self.draw_reward = 0.0

        #기본으로 'draw' 값 설정
        self.player_result = {'X': self.draw_reward, 'O': self.draw_reward}

        #게임이 끝났는지 판단
        self.done = False

    #3X3 맵 재설정
    def reset(self):
        self.map = [['E' for _ in range(self.N)] for _ in range(self.N)]
        self.global_step = 0
        self.player_result = {'X': self.draw_reward, 'O': self.draw_reward}
        self.done = False

        return self.map

    #게임 진행 (action 을 인수로 받음)
    def step(self, action):
        #반환 받은 튜플값 = 보드의 세로와 가로
        action_coord_h, action_coord_w = self.transform_action(action)

        #Turn을 2로 나누었을 때? 나누어 떨어지면 (짝수 턴)
        if self.global_step % 2 == 0:
            current_player_idx = 0
            other_player_idx = 1

        #(홀수 턴)
        else:
            current_player_idx = 1
            other_player_idx = 0
        
        #player_type은 'X', 'O'
        current_player_type = self.player_types[current_player_idx]
        other_player_type = self.player_types[other_player_idx]

        #입력받은 숫자칸이 E라면
        if self.map[action_coord_h][action_coord_w] == 'E':
            #X or O 플레이어 타입으로 변경
            self.map[action_coord_h][action_coord_w] = current_player_type

            #승리 판단
            if self.is_win(current_player_type):    # 현재 플레이어 승리 (True가 반환될 경우)
                self.player_result[current_player_type] = self.win_reward
                self.player_result[other_player_type] = self.defeat_reward
                self.done = True

            #보드가 꽉 찼는지 판단    
            elif self.is_full():    # 무승부
                self.done = True
            else:
                pass

        #이미 점령한 칸을 또 선택했다면?
        else:   # 현재 플레이어 패배
            self.player_result[current_player_type] = self.defeat_reward
            self.player_result[other_player_type] = self.win_reward
            self.done = True

        #Turn++
        self.global_step += 1

        return self.map, self.player_result, self.done

    #숫자를 받아서 3(self.N)으로 나눈 후 몫과 나머지를 튜플 형식으로 반환
    def transform_action(self, action):
        return divmod(action, self.N)

    #이겼는지 판단 (플레이어가 이겼다면 True 반환)
    def is_win(self, current_player_type):
        vertical_win = [True for _ in range(self.N)]
        horizontal_win = [True for _ in range(self.N)]
        diagonal_win = [True for _ in range(2)]
        for h in range(self.N):
            for w in range(self.N):
                # 가로, 세로
                if self.map[h][w] != current_player_type:
                    vertical_win[h] = False
                    horizontal_win[w] = False
                else:
                    pass
                # 왼 대각
                if h == w and self.map[h][w] != current_player_type:
                    diagonal_win[0] = False
                # 오른 대각
                rotated_w = abs(w - (self.N - 1))
                if h == rotated_w and self.map[h][w] != current_player_type:
                    diagonal_win[1] = False
        if any(vertical_win) or any(horizontal_win) or any(diagonal_win):
            return True
        else:
            return False

    #보드(맵)가 꽉 찼는지 학인
    def is_full(self):
        for h in range(self.N):
            for w in range(self.N):
                if self.map[h][w] == 'E':
                    return False
                else:
                    pass
        return True
    
    
    def print_description(self):
        print("** Initial NxN Tic-tac-toe Map **")

        #맵 출력
        self.print_current_map()

        print("** Action Indexes **")
        for idx, des in enumerate(self.map_index_description):
            print(des, end=' ')
            if (idx + 1) % self.N == 0:
                print('\n', end='')

    def print_current_map(self):
        for h in range(self.N):
            for w in range(self.N):
                print(self.map[h][w], end=' ')
            print('\n', end='')
        print()

    # Fill this function
    def match_prediction(self):
        res = 0

        #현재 플레이어 확인
        if self.global_step % 2 == 0:
            res = self.think('X')
        else:
            res = self.think('O')

        #res는 -1, 0, 1 중 하나임
        if(res==0):
            print("비깁니다")
        elif(res==1):
            print("이깁니다")
        else:
            print("집니다")

    #현재 플레이어를 입력으로 받음
    def think(self, turn):
        #현재 플레이어에 따른 other플레이어를 other에 저장
        other = ' '
        if (turn=='O'):
            other='X'
        elif(turn=='X'):
            other='O'
        else:
            return False
        
        #상대방이 이긴경우라면 종료 (-1 반환)
        if(self.is_win(other)):
            return -1

        #minimum은 2로 초기화 (-1, 0, 1중 하나가 들어올 것이기 때문에 2 이상으로 해두면 무관)
        minimum = 2

        #아직 두지 않은 곳에 둬보면서 모든 경우의 수 고려
        #백트래킹 -> 모든 곳에 번갈아 가면서 놓아봄
        for y in range (0,3):
            for x in range(0,3):
                if(self.map[y][x]=='E'):
                    self.map[y][x]=turn
                    #ohter에게 턴을 넘기기
                    buff = self.think(other)
                    #리스트에 minimum과 buff를 넣고 min함수를 사용하여 최솟값 저장
                    l = [minimum, buff]
                    minimum = min(l)

                    #다시 되돌려 놓기
                    self.map[y][x]='E'
        
        #값이 변화가 없거나 0이면 0(무승부)반환
        if(minimum==2 or minimum==0):
            return 0
        
        #내가 이기면 1을 출력하기 위해서 -를 붙여서 반환
        return -minimum
        
if __name__ == '__main__':
    game = TicTacToe()
    game.print_description()

    game.reset()
    done = False
    while not done:
        print()

        action = int(input('Select action please: '))
        if not(game.map_index_description[0] <= action <= game.map_index_description[-1]):
            done = True
            print("Error: You entered the wrong number.")
            continue
        _, player_result, done = game.step(action)
        game.print_current_map()
        if done:
            for player, result in player_result.items():
                if result == game.win_reward:
                    player_result[player] = 'win'
                elif result == game.defeat_reward:
                    player_result[player] = 'defeat'
                else:
                    player_result[player] = 'draw'
            print(player_result)
        game.match_prediction()