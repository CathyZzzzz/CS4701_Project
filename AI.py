#from AI_helper import AI_helper
from Board import Board
import numpy as np

class AI_helper(object):

    def __init__(self, size = 15):
        self.size = size
        # initialize the scores according to their position
        # zeros around and the higher score in the center (size//2)
        self.size = size
        self.score = []
        for i in range(size):
            row_score = []
            for j in range(size):
                k = size // 2
                curr_score = k - max(abs(k-i), abs(k-j))
                row_score.append(curr_score)
            self.score.append(row_score)

        # assign the score to different situation
        # referred from Chinese tranditional Gomoku strategies
        self.strat_lst = ['unvisited', 'two', 'three', 'four', 'two_both', 'three_both', 'four_both', 'five', 'visited']

        self.current = [self.size for i in range(self.size * 2)]
        self.result = [0 for i in range(self.size * 2)]
        
        self.record = [ [] for i in range(size)]
        for i in range(size):
            for j in range(size):
                self.record[i].append([None,None,None,None])
        self.count = []
        for i in range(3):
            self.count.append([0 for i in range(10)])
        self.init_score()
    
    def init_score(self):
        """
        reset the record and count
        """
        for i in range(self.size):
            for j in range(self.size):
                for k in range(4):
                    self.record[i][j][k] = None
        for i in range(3):
            for j in range(10):
                self.count[i][j] = 0
        return 0
    

    def calculate_score(self, board, player):
        # for every movement, reset the record and the count
        self.init_score()
        # assign the score to each situation
        two = 1
        three = 2
        four = 3
        two_both = 4
        three_both = 5
        four_both = 6
        five = 7

        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != 0:
                    for k in range(4):
                        if not self.record[i][j][k]:
                            self.cal(board, i, j, k)
                curr_player = board[i][j]
                if curr_player != 0:
                    for k in range(4):
                        if self.record[i][j][k] in [1,2,3,4,5,6,7]:
                            self.count[curr_player][self.record[i][j][k]] += 1
        # black = 1
        # white = 2

        score_me = 0
        score_oppo = 0

        if player == 1:
            me = 1
            oppo = 2
        else:
            me = 2
            oppo = 1
        for i in range(1,3):
            if self.count[i][four] >= 2:
                self.count[i][four_both] += 1
			
        if self.count[me][five]:
            return 9999
        if self.count[oppo][five]:
            return -9999
        if self.count[me][four_both] > 0:
            return 9990
        if self.count[me][four] > 0:
            return 9980
        if self.count[oppo][four_both] > 0:
            return -9990
        if self.count[oppo][four] and self.count[oppo][three_both]:
            return -9960
        if self.count[me][three_both] and self.count[oppo][four] == 0:
            return -9950
        if self.count[oppo][three_both] > 1 and self.count[me][four] == 0 and self.count[me][three_both] == 0 and self.count[me][three] == 0:
            return -9940
        if self.count[me][three_both] and self.count[oppo][three_both] == 0:
            return 9930

        if self.count[me][three_both] > 1:
            score_me += 2000
        elif self.count[me][three_both]:
            score_me += 200
        if self.count[oppo][three_both] > 1:
            score_oppo += 2000
        elif self.count[oppo][three_both]:
            score_oppo += 200
        
        if self.count[me][three]:
            score_me += self.count[me][three] * 10
        if self.count[oppo][three]:
            score_oppo += self.count[oppo][three] * 10
        if self.count[me][two_both]:
            score_me += self.count[me][two_both] * 3
        if self.count[oppo][two_both]:
            score_oppo += self.count[oppo][two_both] * 3
        if self.count[me][two]:
            score_me += self.count[me][two]
        if self.count[oppo][two]:
            score_oppo += self.count[oppo][two]

        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == player:
                    score_me += self.score[i][j]
                elif board[i][j] != 0:
                    score_oppo += self.score[i][j]
        
        final_score = score_me - score_oppo
        if final_score < -9000:
            for i in range(10):
                if self.count[oppo][i] > 0:
                    final_score -= i
        elif final_score > 9000:
            for i in range(10):
                if self.count[me][i] > 0:
                    final_score += i
        return final_score

    def cal(self, board, i, j, k):
        """
        calculate the score for each situation
        k = 0 horizontal
        k = 1 vertical
        k = 2 left diagonal
        k = 3 right diagonal
        """
        if k == 0:
            for row in range(self.size):
                self.current[row] = board[i][row]
            self.cal_helper(self.size, j)
            for row in range(self.size):
                if self.result[row] != 0:
                    self.record[i][row][0] = self.result[row]
            return self.record[i][j][0]
        elif k == 1:
            for row in range(self.size):
                self.current[row] = board[row][j]
            self.cal_helper(self.size, i)
            for row in range(self.size):
                if self.result[row] != 0:
                    self.record[row][j][1] = self.result[row]
            return self.record[i][j][1]
        elif k == 2:
            if i < j:
                x, y = j - i, 0
            else:
                x, y = 0, i - j
            a = 0
            while a < self.size:
                if x + a > self.size - 1 or y + a > self.size - 1:
                    break
                self.current[a] = board[y+a][x+a]
                a += 1
            self.cal_helper(a, j-x)
            for row in range(a):
                if self.result[row] != 0:
                    self.record[y + row][x + row][2] = self.result[row]
            return self.record[i][j][2]
        elif k == 3:
            if self.size - 1 - i < j:
                x, y= j-(self.size-1)+i, self.size-1
            else:
                x, y = 0, i+j
            a = 0
            while a < self.size:
                if x + a > self.size - 1 or y + a < 0:
                    break
                self.current[a] = board[y-a][x+a]
                a += 1
            self.cal_helper(a, j-x)
            for row in range(a):
                if self.result[row] != 0:
                    self.record[y - row][x + row][3] = self.result[row]
            return self.record[i][j][3]
        return None

    def cal_helper(self, num, inx):
        for i in range(num, self.size * 2):
            self.current[i] = self.size
        for i in range(num):
            self.result[i] = 0
        x = self.current[inx]
        oppo = [0, 2, 1][x]
        num -= 1
        left = inx
        right = inx

        while left > 0:
            if self.current[left - 1] != x:
                break
            left -= 1
        while right < num:
            if self.current[right + 1] != x:
                break
            right += 1

		# left and right range for consecutive pieces for current player
        left_range = left
        right_range = right
        while right_range < num:
            if self.current[right_range + 1] == oppo:
                break
            right_range += 1
        while left_range > 0:
            if self.current[left_range - 1] == oppo:
                break
            left_range -= 1
        srange = right - left + 1
        
        # set as visited
        for k in range(left, right + 1):
            self.result[k] = 8
        
        # Five
        if srange >= 5:	
            self.result[inx] = 7
            return self.result[inx]
        
        # Four & Four_both
        elif srange == 4:	
            left_ind = False
            right_ind = False
            if left > 0 and self.current[left-1] == 0:
                left_ind = True
            if right < num and self.current[right+1] == 0:
                right_ind = True
            if left_ind and right_ind:
                self.result[inx] = 6
            elif (left_ind and not right_ind) or (not left_ind and right_ind):
                self.result[inx] = 3
            return self.result[inx]
        
        # Three & Three_both
        elif srange == 3:
            left_ind = False
            right_ind = False
            if left > 0:
                if right == num or self.current[right+1] != 0:
                    return 0
                if self.current[left - 1] == 0:
                    if left == 1 or self.current[left - 2] != x:
                        left_ind = True
                    else:
                        self.result[left] = 3
                        self.result[left - 2] = 8
            if (self.current[left - 1] == 0 or right > num) and self.result[left] == 3:
                return self.result[left]
            if right < num:
                if self.current[right + 1] == 0:
                    right_ind = True
                    if right < num - 1 and self.current[right + 2] == x:
                        left_ind = False
                        self.result[right] = 3
                        self.result[right + 2] = 8
            if left_ind and right_ind:
                self.result[right] = 5
            elif not left_ind and right_ind:
                self.result[right] = 2
            return self.result[x]
        
        # Two & Two_both
        elif srange == 2:
            left_ind = False
            left_ind2 = False
            if left > 2:
                if self.current[left - 1] == 0:
                    if self.current[left-2] != x:
                        left_ind = True
                    else:
                        if self.current[left - 3] == x:
                            self.result[left - 3], self.result[left - 2] = 8, 8
                            self.result[left] = 3
                        elif self.current[left - 3] == 0:
                            self.result[left - 2] = 8
                            self.result[left] = 2
            if right < num:
                if self.current[right + 1] == 0:
                    if right < num - 2 and self.current[right + 2] == x:
                        if self.current[right + 3] == x:
                            self.result[right + 3], self.result[right + 2]  = 8, 8
                            self.result[right] = 3
                        elif self.current[right + 3] == 0:
                            self.result[right + 2] = 8
                            self.result[right] = left_ind and 2 or 5
                    else:
                        if self.result[left] == 2:
                                self.result[left] = 5
                                return self.result[left]
                        if self.result[left] == 3:
                            return self.result[left]
                        if left_ind:
                            self.result[inx] = 4
                        else:
                            self.result[inx] = 1
                else:
                    if self.result[left] == 3:
                        return self.result[left]
                    if left_ind:
                        self.result[inx] = 1
            return self.result[inx]
        return 0


class AI(object):
	def __init__ (self, size = 15):
		self.size = size
		self.board = Board(size)
		self.AI_helper = AI_helper(size)
		self.overvalue = 0
		# set to 3 or taking too long
		self.max_depth = 3
		self.best_strat = None


	def legal(self):
		legal_moves = []
		for i in range(self.size):
			for j in range(self.size):
				if self.board[i][j] == 0:
					legal_moves.append((self.AI_helper.score[i][j], i, j))
	
		legal_moves.sort(reverse=True)
		return legal_moves
	

	def minimax_helper(self, player, depth, upper = np.inf, lower = -np.inf):
		#upper = np.inf
		#lower = -np.inf
		score = self.AI_helper.calculate_score(self.board, player)
		if depth <= 0:
			return score
		# Five is achieved
		# there is a winner so do not need further calculation
		if abs(score) >= 9999 and depth < self.max_depth: 
			return score

		legal_moves = self.legal()
		best_strat = None
		for score, row, col in legal_moves:
			if player == 1:
				next_turn = 2
			elif player == 2:
				next_turn = 1
			# mark the board for the current player
			self.board[row][col] = player
			# update the score for next_turn
			score = - self.minimax_helper(next_turn, depth - 1, -lower, -upper)
			# mark the board for empty again
			self.board[row][col] = 0
			if score > lower:
				lower = score
				best_strat = (row, col)
				if lower >= upper:
					break
		# reach the max_depth
		if depth == self.max_depth and best_strat != None:
			self.best_strat = best_strat

		# return the score
		return lower

	def minimax(self, player, depth=3):
		self.max_depth = depth
		self.best_strat = None
		score = self.minimax_helper(player, depth)
		if abs(score) > 8000:
			self.max_depth = depth
		best_row, best_col = self.best_strat
		return best_row, best_col