import math

from connectfour.agents.computer_player import RandomAgent


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5
        self.alpha = -math.inf
        self.beta = math.inf

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            # print(move)
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, self.alpha, self.beta, 1))

        print(str(self.id) + ": " + str(vals))
        bestMove = moves[vals.index(max(vals))]
        return bestMove

    def dfMiniMax(self, board, alpha, beta, depth):
        # Goal return column with maximized scores of all possible next states
        if depth == self.MaxDepth or self.is_terminal_node(board):  # reach to terminal node
            if self.is_terminal_node(board):
                opp_id = self.get_opp_id()
                if self.check_winning(board, self.id): # winning move
                    return math.inf
                elif self.check_winning(board, opp_id): # losing move
                    return -math.inf
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        if depth % 2 == 1:  # minimizing player
            best_value = math.inf
            for move in valid_moves:
                next_state = board.next_state(self.id % 2 + 1, move[1])
                new_value = self.dfMiniMax(next_state, alpha, beta, depth + 1)
                best_value = min(best_value, new_value)
                beta = min(beta, best_value)
                if alpha > beta:  # beta cut off
                    break
            return best_value

        else:  # maximizing player
            best_value = -math.inf
            for move in valid_moves:
                next_state = board.next_state(self.id, move[1])
                new_value = self.dfMiniMax(next_state, alpha, beta, depth + 1)
                best_value = max(best_value, new_value)
                alpha = max(alpha, best_value)
                if alpha > beta:  # alpha cut off
                    break
            return best_value

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        position_list = self.generate_position_list(board)
        final_score = self.score_position(board, position_list)
        return final_score

    def score_position(self, board, position_list):
        # check four direction to calculate score of each position move
        score = 0
        center_col_list = self.get_center_col(position_list)
        score += center_col_list.count(self.id) * 2
        score += self.eval_horiz(board, position_list)
        score += self.eval_vert(board, position_list)
        score += self.eval_positive_diag(board, position_list)
        score += self.eval_negative_diag(board, position_list)
        return score

    def get_center_col(self, position_list):
        # generate status of center column since center column weight more
        center_col_list = []
        for row in position_list:
            center_col_list.append(row[len(row) // 2])
        return center_col_list

    def eval_horiz(self, board, position_list):
        # evaluate each row
        score = 0
        for row in range(0, board.height):
            # status for each row
            row_array = position_list[row]
            for col in range(0, board.width - 3):
                # create a window which has length 4
                window = row_array[col:col + board.num_to_connect]
                score += self.eval_window(window)
        return score

    def eval_vert(self, board, position_list):
        # evaluate each column
        score = 0
        for col in range(0, board.width):
            col_array = self.generate_col_array(col, position_list)
            for row in range(0, board.height - 3):
                window = col_array[row:row + board.num_to_connect]
                score += self.eval_window(window)
        return score

    def generate_col_array(self, index, position_list):
        # generate each col's status using the position list
        col_array = []
        for row in position_list:
            col_array.append(row[index])
        return col_array

    def eval_positive_diag(self, board, position_list):
        # evaluate positive slope diagonal
        score = 0
        for row in range(3, board.height):
            for col in range(board.width - 3):
                window = [position_list[row - i][col + i] for i in range(board.num_to_connect)]
                score += self.eval_window(window)
        return score

    def eval_negative_diag(self, board, position_list):
        # evaluate negative slope diagonal
        score = 0
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                window = [position_list[row + i][col + i] for i in range(board.num_to_connect)]
                score += self.eval_window(window)
        return score

    def eval_window(self, window):
        """
        eval each window according to number of piece in each window
        """
        # set opponent id
        opp_id = self.get_opp_id()

        score = 0
        if window.count(self.id) == 4:
            score += 100
        elif window.count(self.id) == 3 and window.count(0) == 1:
            score += 50
        elif window.count(self.id) == 2 and window.count(0) == 2:
            score += 10

        if window.count(opp_id) == 3 and window.count(0) == 1:
            score -= 40

        return score

    def generate_position_list(self, board):
        position_list = list()
        for row in range(0, board.height):
            temp_list = list()
            for col in range(0, board.width):
                stone = board.get_cell_value(row, col)
                temp_list.append(stone)
            position_list.append(temp_list)

        return position_list

    def check_winning(self, board, token):
        # check horizontal winning state
        for row in range(board.height):
            for col in range(board.width - 3):
                if board.get_cell_value(row, col) == token \
                        and board.get_cell_value(row, col + 1) == token \
                        and board.get_cell_value(row, col + 2) == token \
                        and board.get_cell_value(row, col + 3) == token:
                    return True

        # check vertical winning state
        for col in range(board.width):
            for row in range(board.height - 3):
                if board.get_cell_value(row, col) == token \
                        and board.get_cell_value(row + 1, col) == token \
                        and board.get_cell_value(row + 2, col) == token \
                        and board.get_cell_value(row + 3, col) == token:
                    return True

        # check positive slope diagonals
        for row in range(3, board.height):
            for col in range(board.width - 3):
                if board.get_cell_value(row, col) == token \
                        and board.get_cell_value(row - 1, col + 1) == token \
                        and board.get_cell_value(row - 2, col + 2) == token \
                        and board.get_cell_value(row - 3, col + 3) == token:
                    return True

        # check negative slope diagonals
        for row in range(board.height - 3):
            for col in range(board.width - 3):
                if board.get_cell_value(row, col) == token \
                        and board.get_cell_value(row + 1, col + 1) == token \
                        and board.get_cell_value(row + 2, col + 2) == token \
                        and board.get_cell_value(row + 3, col + 3) == token:
                    return True

    def is_terminal_node(self, board):
        opp_id = self.get_opp_id()
        return self.check_winning(board, self.id) or self.check_winning(board, opp_id)

    def get_opp_id(self):
        opp_id = 0
        if self.id == 1:
            opp_id = 2
        elif self.id == 2:
            opp_id = 1
        return opp_id

    def add_weight(self, board, col):
        # make AI prefer center over edge
        center_col = board.width // 2
        value = center_col - col
        return abs(value)