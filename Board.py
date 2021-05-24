class Board(object):
    def __init__(self, size = 15):
        """
        set the board with [size]
        """
        self.size = size
        self.__board = [[0 for i in range(size)] for j in range(size)]


    def get_board(self):
        return self.__board


    def check_winner(self):
        """
        Check for winner 
        Return [black] if the black wins, [white] if the white wins, and else [None]
        """
        for i in range(self.size):
            for j in range(self.size):
                if self.__board[i][j] == 0:
                    continue
                curr_value = self.__board[i][j]
                # check for each direction
                for direction in ((1, 1), (1, -1), (1, 0), (0, 1)):
                    curr_i = i 
                    curr_j = j
                    count = 0
                    for k in range(5):
                        if self.__board[curr_i][curr_j] != curr_value:
                            break
                        curr_i += direction[0]
                        curr_j += direction[1]
                        count += 1
                    if count == 5:
                        if curr_value == 1:
                            return 'Black'
                        else:
                            return 'White'
        return None


