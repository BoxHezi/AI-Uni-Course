from connectfour.agents.computer_player import RandomAgent
import random
import math
import re
from progress.bar import FillingSquaresBar as Bar
#from progress.bar import Bar as Bar
import time
import threading
import multiprocessing
import sys


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 5
        self.built = False
        self.debug = False


    def buildDiag(self, board):
        good_pos = []

        # Eval from top left to bottom right
        # e.g. from 0,0 to board.width, board.height
        # Done in two sections

        pos = []
        # diagonals for row minus and col plus
        row = 3
        col = 0
        while True:
            temp_row = row
            temp_col = col
            while True:
                if temp_row < 0:
                    break
                if temp_col > board.width:
                    break
                pos.append([temp_row, temp_col])

                temp_col += 1
                temp_row -= 1

            good_pos.append(pos)
            pos = []
            row += 1
            if row >= board.height:
                break

        # diagonals for row minus and col plus from bottom of the board moving to right
        row = 5
        col = 1
        while True:
            temp_row = row
            temp_col = col
            while True:
                if temp_row < 0:
                    break
                if temp_col >= board.width:
                    break
                pos.append([temp_row, temp_col])

                temp_col += 1
                temp_row -= 1

            if len(pos) < board.num_to_connect:
                break
            good_pos.append(pos)
            pos = []
            col += 1
            if col >= board.width:
                break

        pos = []
        # diagonals for row minus and col plus
        row = 0
        col = 0
        while True:
            temp_row = row
            temp_col = col
            while True:
                if temp_row >= board.height:
                    break
                if temp_col >= board.width:
                    break
                pos.append([temp_row, temp_col])

                temp_col += 1
                temp_row += 1

            if len(pos) < board.num_to_connect:
                break
            good_pos.append(pos)
            pos = []
            row += 1
            if row >= board.height:
                break

        pos = []
        # diagonals for row minus and col plus
        row = 0
        col = 1
        while True:
            temp_row = row
            temp_col = col
            while True:
                if temp_row >= board.height:
                    break
                if temp_col >= board.width:
                    break
                pos.append([temp_row, temp_col])

                temp_col += 1
                temp_row += 1

            if len(pos) < board.num_to_connect:
                break
            good_pos.append(pos)
            pos = []
            col += 1
            if col >= board.width:
                break


        self.diag_pos = good_pos
        self.built = True



        #for sett in self.diag_pos:
            #print(sett)



    def get_move(self, board):
        self.print_board(board)
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """
        valid_moves = board.valid_moves()
        moves = []


        start = time.time()

        pos = 0
        threads = []
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        vals = [0] * board.width
        bar = Bar('Calculating Next Move', max=board.width+2)
        bar.next()
        for move in valid_moves:
            pos += 1
            if self.debug:
                print("=" * 32 + "Get MOVE" + "=" * 32)
                print(move)

            next_state = board.next_state(self.id, move[1])
            moves.append(move)

            thread = multiprocessing.Process(target=self.threadMiniMax, args=(next_state, 1, return_dict, pos-1))
            
            threads.append(thread)

            threads[pos-1].start()
            #value = self.dfMiniMax(next_state, 1)

        for thread in threads:
            thread.join()
            bar.next()



        for i in range(0, board.width):   
            vals[i] = return_dict[i]

       
        bar.next()
        bar.finish()
 
        end = time.time()
        #print("Time taken: "+str(math.trunc(end-start)))
        print("Time taken: "+str(end-start))


        print(vals)
        bestMove = moves[vals.index(max(vals))]
        self.print_board(board.next_state(self.id, bestMove[1]))
        return bestMove

    def threadMiniMax(self, board, depth, results, index):
        out = self.dfMiniMax(board, depth)
        results[index] = out

    def dfMiniMax(self, board, depth):
        if self.debug:
            print("MINI MAX ", end="")
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            if self.debug:
                print("depth: " + str(depth))
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if self.debug:
                print("next state:" + str(move) + " depth: " + str(depth))
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)
       
        return bestVal


    def slidingWindow(self, board, positions):

        our_score = self.slidingWindowInternal(board, positions, self.id)
        #print("Our Score: "+str(our_score))

        if self.id is 1:
            enemy_id = 2
        else:
            enemy_id = 1

        their_score = self.slidingWindowInternal(board, positions, enemy_id)
        #print("Their Score: "+str(their_score))


        return [our_score, their_score]



    # POSITIONS: an array of positions for evaluation
    def slidingWindowInternal(self, board, positions, playerID):
        #print(positions)

        value = 0
        blank_weight = 0.0
        self_weight = 10 # >= 2
        runningTotal = 0
        selfInWindow = 0
        pos = 0
        #print("Starting row")
        for posi in positions:

            row = posi[0]
            col = posi[1]
            #print("Checking: row:"+str(row)+" col:"+str(col))

            # TODO: NOT NEED THIS
            if row >= board.height or col >= board.width:
                continue

            stone = board.get_cell_value(row, col)

            if stone == playerID:
                selfInWindow += 1
                #runningTotal += self_weight*selfInWindow
                runningTotal += pow(self_weight, selfInWindow*selfInWindow)
                #runningTotal += pow(self_weight, selfInWindow*1)
            elif stone == 0:
                runningTotal += blank_weight
            elif stone != playerID and stone != 0:
                if pos >= board.num_to_connect:
                    # We have a good run, add to running total
                    value += runningTotal
                # reset running total to 0 since the run is bad
                runningTotal = 0
                selfInWindow = 0
                pos = 0
                continue

            pos += 1

        if pos >= board.num_to_connect:
            value += runningTotal

        return value


    def evalHoriz(self, board):
        our_value = 0
        their_value = 0
        for row in range(0, board.height):
            isEmpty = True # TODO: Optimize
            for col in range(0, board.width):
                if board.get_cell_value(row, col) is not 0:
                    isEmpty = False
                    break
            if isEmpty: # Skip empty row
                #continue
                pass


            poss = []
            for col in range(0, board.width):
                poss.append([row, col])

            out = self.slidingWindow(board, poss)
            our_value += out[0]
            their_value += out[1]


        return [our_value, their_value]

    def evalVert(self, board):
        our_value = 0
        their_value = 0
        for col in range(0, board.width):
            # TODO: skip empty
            poss = []
            for row in range(0, board.height):
                poss.append([row, col])

            out = self.slidingWindow(board, poss)
            our_value += out[0]
            their_value += out[1]


        return [our_value, their_value]


    def evalDiag(self, board):
        # Build the positions array if not yet done
        if self.built is not True:
            self.buildDiag(board)

        our_value = 0
        their_value = 0
        # Evaluate diagonals
        for pos_set in self.diag_pos:
            out = self.slidingWindow(board, pos_set)
            our_value += out[0]
            their_value += out[1]


        return [our_value, their_value]




    def evaluateBoardState(self, board):
        if self.debug:
            self.print_board(board)


        our_value = 0
        their_value = 0
        outh = self.evalHoriz(board)

        outv = self.evalVert(board)
        
        outd = self.evalDiag(board)

        value = []
        value.append(outh[0] + outv[0] + outd[0])
        value.append(outh[1] + outv[1] + outd[1])

        if self.debug:
            print("Value: " + str(value))


        return value[0]-(value[1]*0.999)

    def handleScores(self, out):
        our_score = out[0]



    def print_board(self, board):
        #print("-" * 20 + "evaluating" + "-" * 20)
        height = board.height
        width = board.width

        print("_"*(board.width*2+1))
        for row in range(height):
            for col in range(width):
                piece = board.get_cell_value(row, col)
                if piece == 1:
                    print("|1", end="")
                elif piece == 2:
                    print("|2", end="")
                else:
                    print("| ", end="")
            print("|")
        print("¯"*(board.width*2+1))
