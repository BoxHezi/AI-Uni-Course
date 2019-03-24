# Tutorial Sheet 2

4. What are the dimesiona we judge the various search algorithms? Discuss each of them for each algorithm\
   * Completeness
     * Depth-first search: False
   * Optimality
     * Depth-first search: False
   * Time Complexity
   * Spcae Complexity
    > Complexity depends on *b*, the branching factor in the state spcae, and *d*, the depth of the shallowest solution

5. (RN) Which of the following are true and which are false? Explain your answers.
   * Depth-first search always expands at least as many nodes as A search with an admisible heuristic
     * False 
        > Depth-first search can be very lucky to get the optimal path at the fitst try
   * *h(n) = 0* is an admissible heuristic for the 8-puzzle
     * True
   * A* is of no use in robotics because percepts, states, and actions are continuous
     * False
   * Breadth-first search is complete even if zero step costs are allowed
     * False
        > Breadth-first search doesn't use cost
   * Assume that a rook can move on a chessboard any number of squares in a straight line, vertically or horizontally, but cannot jump over other pieces. Manhattan distance is an admissible heuristic for the problem of moving the rook from square A to square B in the smallest number of moves.
     * False