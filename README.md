## What is the Travelling Salesmen Problem?

The Traveling Salesman Problem (TSP) is a classic optimization problem in which the goal is to find the shortest possible route that visits a set of given cities exactly once and returns to the origin city. 

It might seem simple, but its complexity grows exponentially with the number of cities, making it a quintessential problem in computer science and optimization theory.

Despite its seemingly straightforward nature, it is impractical to solve for larger instances using brute force or exhaustive search methods.

## What is ACO?

Ant Colony Optimization (ACO) is a metaheuristic algorithm inspired by the foraging behavior of ants seeking the shortest path between their colony and a food source. It's particularly useful for solving combinatorial optimization problems like the Traveling Salesman Problem (TSP).

Ants make decisions probabilistically, guided by a balance between the amount of pheromone on a path and the heuristic information (such as distance between cities). Over time, paths with better solutions receive more pheromone due to positive feedback, increasing the probability of other ants choosing these paths.

By combining exploration (to discover new paths) and exploitation (to exploit the best-known paths), ACO efficiently explores the solution space and converges towards an optimal or near-optimal solution for complex optimization problems.


### I. Implememtations
1. Implemented the **Travelling Sales Person** algorithm in python using two approaches : dynamic programming and nearest neighbour.
2. Implemented the **Ant Colony System** algorithm in python.
3. Implemented the dynamic search process and visualization of results for solving the Traveling Salesman Problem (TSP) using the **Ant Colony System** (ACS) algorithm.

### II Dataset
1. Oliver30: Comprising 30 cities, this dataset is a standard benchmark used to evaluate optimization algorithms for the Traveling Salesman Problem (TSP).
2. Eil51: With 51 cities, this dataset poses a moderate challenge for optimization algorithms due to increased complexity in finding the shortest path for the TSP.
3. Eil76: Featuring 76 cities, this dataset offers a more intricate challenge for optimization algorithms seeking optimal solutions in the Traveling Salesman Problem.
4. kroa100: A dataset encompassing 100 cities, providing a highly complex scenario for optimization algorithms, particularly in efficiently solving the Traveling Salesman Problem.

### III. After More Improvements, Applicable Scenarios
1. Traveling Salesman Problem (TSP)
2. Job-shop Scheduling Problem
3. Vehicle Routing Problem
4. Graph
5. Logistics - Routing and Delivery
