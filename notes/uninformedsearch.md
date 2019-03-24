# [Search Stragtegy - Uninformed Search](https://mhesham.wordpress.com/tag/depth-first-search/)

## **Breadth-first search (BFS)**
* **Description**
  * A simple stragtegy in which the root is expanded first then all the root successors are expanded next, then their successors.
  * We visite the search tree level by level that all nodes are expanded at a given depth before any nodes at the next level are expanded
  * Order in which nodes are expanded
* **Performance Measure**
  * Completeness
    * It is easy to see that breadth-first search is complete that it visits all levels given that *d* factor is finite, so in some *d* it will find a solution.
  * Optimality
    * Breadth-first search is not optimal until all actions have the same cost.
  * Space complexity and Time complexity
    * Consider a state space where each node as a branching factor *b*, the root of the tree generates *b* nodes, each of which generates *b* nodes yielding *b^2* each of these generates *b^3* and so on.
    * In the worst case, suppose that our solution is at depth *d*, and we expand all nodes but the last node at level *d*, then the total number of generated nodes is: *b + b^2 + b^3 + b^4 + b^(d+1) - b = O(b^(d+1))*
    * As all the nodes must retain in memory while we expand our search, then the space complexity is like the time complexity plus the root node = *O(b(d+1))*
* **Conclusion**
  * We see that space complexity is the biggest problem for BFS than its exponential execution time
  * Time complexity is still a major problem

## **Uniform-cost search (UCS)**
* **Description**
  * Uniform-cost is guided by path cost rather than path length like in BFS, the algorithm starts by expanding the root, then expanding the node with the lowest cost from the root, the search continues in this manner for all nodes.
  * Hints about UCS implementation can be found [here](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Practical_optimizations_and_infinite_graphs)
  * You should not be surprised that [Dijkstra's Algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm), which is perhaps better-known, can be regarded as a variant of uniform-cost search, where there is no goal state and processing continues until the shortest path to all nodes has been determined.
* **Performance Measure**
  * Completeness
    * It is obvious that UCS is complete if the cost of each step exceeds some small positive integer, this is to prevent infinite loops.
  * Optimality
    * UCS is always optimal in the sense that the node that it always expands is the node with the least path cost.
  * Time Complexity
    * UCS is guided by path cost rather than path length so it is hard to determine its complexity in terms of *b* and *d*, so if we consider *C* to be the cost of the optimal solution, and every action costs at least *e*, then the algorithm worst case is *O(b^(C/e))*
  * Space Complexity
    * The space complexity is *O(b^(C/e))* as the time complexity of UCS
* **Conclusion**
  * UCS can be used instead of BFS in case that path cost is not equal and is guaranteed to be greater than a small positive value *e*.

## **Depth-first search (DFS)**
* **Description**
  * Order in which nodes are expanded.
* **Performance Measure**
  * Completeness
    * DFS is not complete, to convince yourself consider that our search start expanding the left sub tree of the root for so long path (may be infinite) when different choice near the root could lead to a solution, now suppose that the left sub tree of the root has no solutionm and it is unbounded, then the search will continue going deep infinitely, in this case we say that DFs is not complete
  * Optimality
    * Consider the scenario that there is more than one goal node, and our search decided to first expand the left sub tree of the root where there is a solution at a very deep level of this left sub tree, in the same time the right sub tree of the root has a solution near the root, here comes the non-optimality of DFS that it is not guaranteed that the first goal to find is the optimal one, so we conclude that DFS is not optimal
  * Time Complexity
    * Consider a state space that is identical to that of BFS, with branching factor *b*, and we start the search from the root
    * In the worst case that goal will be in the shallowest level in the search tree resulting in generating all tree nodes which are *O(b^m)*
  * Space Complexity
    * Unlike BFS, DFS has a very modest memory requirement, it needs to store only the path from the root to the leaf node, beside the siblings of each node on the path, remember that BFS needs to store all explored nodes in memory
    * DFS removes a node from memory once all of its descendants have been expanded
    * With branching factor *b* and maximum depth *m*, DFS requires storage of only *bm + 1* nodes which are *O(bm)* compared to the *O(b^(d+1))*
* **Conclusion**
  * DFS may suffer from non-termination when the length of a path in the search tree is infinite, so we perform DFS to a limited depth which is called Depth-limit search

## **Dpeth-limited search (DLS)**
* **Description**
  * The unbounded tree problem appeared in DFS can be fixed by imposing a limit on the depth that DFS can reach, this limit we will call depth limit *l*, this solves the infinite path problem.
* **Performance Measure**
  * Completeness
    * The limited path introduces another problem which is the case when we choose *l < d*, in which is our DLS will never reach a goal, in this case we can say DLS is not complete.
  * Optimality
    * One can view DFS as a special case of the depth DLS, that DFS is DLS with *l = infinity*
    * DLS is not optimal even if *l > d*
  * Time Complexity
    * *O(b^l)*
  * Space Complexity
    * *O(b^l)*
* **Conclusion**
  * DLS can be used when there is prior knowledge to the problem, which is always not the case. Typically, we will not know the depth of the shallowest goal of a problem unless we solved this problem before

## **Iterative deepening depth-first search (IDS)**
* **Description**
  * It is a search strategy resulting when you combine BFS and DFS, thus combining the advantages of each strategy, taking the completeness and optimality of BFS and the modest memory requirements of DFS
  * IDS works by looking for the best search depth *d*, thus starting with depth limit 0 and make a BFS and if the search failed it increase the depth limit by 1 and try a BFS again with depth 1 and so on - first *d = 0*, then 1 then 2 and so on - until a depth *d* is reached where a goal is found
* **Performance Measure**
  * Completeness
    * IDS is like BFS, is complete when the branching factor *b* is finite
  * Optimality
    * IDS is also like BFS optimal when the steps are of the same cost
  * Time Complexity
    * One may find that it is wasteful to generate nodes multiple times, but actually it is not that costly compared to BFS, that is because most of the generated nodes are always in the deepest level reached, consider that we are searching a binary tree and our depth limit reached 4, the nodes generated in last level - *2^4 = 16*, the nodes generated in all nodes before last level = *2^0 + 2^1 + 2^2 + 2^3 = 15*
    * Imagine this scenario, we are performing IDS and the depth limit reached depth *d*, now if your remember the way IDS expands nodes, you can see that nodes at depth *d* are generated once, nodes at depth *d-1* are generated 2 times, nodes at depth *d-2* are generated 3 times and so on, until you reach depth 1 which is generated *d* times, we can view the total number of generated nodes in the worst case as:
      * *N(IDS) = (b)d + (d – 1)b^2 + (d – 2)b^3 + …. + (2)b^(d-1) + (1)bd = O(b^(d+1))*
    * If we consider a realistic numbers, and use *b = 10* and *d = 5*, then number of generated nodes in BFS and IDS will be like
      * N(IDS) = 50 + 400 + 3000 + 20000 + 100000 = 123450 
      * N(BFS) = 10 + 100 + 1000 + 10000 + 100000 + 999990 = 1111100 
      * BFS generates like 9 time nodes to those generated with IDS.
  * Space Complexity
    * IDS is like DFS in its space complexity, taking *O(bd)* of memory
* **Conclusion**
  * We can conclude that IDS is a hybrid search strategy between BFS and DFS inheriting their advantages
  * IDS is faster than BFS and DFS
  * It is said that "IDS is the preferred uniformed search method when there is a large search space and the depth of the solution is not known"

## **Bidirectional search**
* **Description**
  * As the name suggests, bidirectional search suggests to run 2 simultaneous searches, one from the initial state and the other from the goal state, those 2 searches stop when they meet each other at some point in the middle of the graph.
* **Performance Measure**
  * Completeness
    * Bidirectional search is complete when we use BFS in both searches, the search that starts from the initial state and the other from the goal state
  * Optimality
    * Like the completeness, bidirectional search when BFS is used and paths are of a uniform cost - all steps of the same cost
    * Other search strategies can be used like DFS, but this will sacrifice the optimality and completeness, any other combination than BFS may lead to a sacrifice in optimality or completeness or may be both of them
  * Time and Space Complexity
    * May be the most attractive thing in bidirectional search is its performance, because both searches will run the same amount of time meeting in the middle of the graph, thus each search expands *O(b^(d/2))* node, in total both searches expand *O(b^(d/2) + b^(d/2))* node which is too far better than the *O(b^(d + 1))* of BFS
    * If a problem with *b = 10*, has a solution at depth *d = 6*, and each direction runs with BFS, then at the worst case they meet at depth *d = 3*, yielding 22200 nodes compared with 11111100 for a standard BFS
    * We can say that the time and space complexity of bidirectional search is *O(b^(d/2))*
* **Conclusion**
  * Bidirectional search seems attractive for its *O(b^(d/2))* preformance, but things are not that easy, especially the implementation part.
  * It is not that easy to formulate a problem such that each state can be reversed, that is going from the head to the tail is like going from the tail to the head
  * It should be efficient to compute the predecessor of any state so that we can run the search from the goal
