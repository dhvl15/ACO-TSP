from City import City
import numpy as np

# nearest neighbour algorithm

def tsp_nearest_neighbor(city_file_name):
    city = City(city_file_name)
    city.city_import()

    num_cities = city.num_city
    dist_matrix = city.get_dis_matrix()
    x_list, y_list = city.x_list, city.y_list

    # Initialize variables
    visited = [0] * num_cities  # Keep track of visited cities
    path = [0]  # Starting with the first city
    x_coords = [x_list[0]]  # X coordinates of the path
    y_coords = [y_list[0]]  # Y coordinates of the path
    current_city = 0  # Start from the first city

    for _ in range(num_cities - 1):
        visited[current_city] = 1
        min_dist = float('inf')
        nearest_city = -1

        # Find the nearest unvisited city
        for city_index in range(num_cities):
            if not visited[city_index] and dist_matrix[current_city][city_index] < min_dist:
                min_dist = dist_matrix[current_city][city_index]
                nearest_city = city_index

        path.append(nearest_city)
        x_coords.append(x_list[nearest_city])
        y_coords.append(y_list[nearest_city])
        current_city = nearest_city

    # Add the starting city to complete the cycle
    path.append(0)
    x_coords.append(x_list[0])
    y_coords.append(y_list[0])

    total_distance = sum(dist_matrix[path[i]][path[i + 1]] for i in range(num_cities))

    return total_distance, path, x_coords, y_coords

# Example usage:
# distance, path, x_coords, y_coords = tsp_nearest_neighbor("Oliver30.txt")
# print("Optimal Distance using Nearest Neighbor:", distance)
# print("Optimal Path using Nearest Neighbor:", path)
# print("X Coordinates of Optimal Path:", x_coords)
# print("Y Coordinates of Optimal Path:", y_coords)

# dynamic programming approach with memoization

# def tsp_dynamic_programming(city_file_name):
#     city = City(city_file_name)
#     city.city_import()

#     num_cities = city.num_city
#     all_points_set = set(range(num_cities))
#     dist_matrix = city.get_dis_matrix()
#     x_list, y_list = city.x_list, city.y_list

#     # memoization table to store subproblem solutions
#     memo = {}

#     def tsp_dp_helper(mask, current_point):
#         # base case: all cities visited
#         if mask == all_points_set:
#             return dist_matrix[current_point][0], [0], [x_list[current_point]], [y_list[current_point]]

#         # check if subproblem solution already computed
#         memo_key = (tuple(mask), current_point)
#         if memo_key in memo:
#             return memo[memo_key]

#         # compute the minimum distance and path for the current subproblem
#         min_distance = float('inf')
#         min_path = None
#         min_x_list = None
#         min_y_list = None

#         for next_point in range(num_cities):
#             if next_point != current_point and next_point not in mask:
#                 new_mask = mask | {next_point}
#                 distance, path, x_path, y_path = tsp_dp_helper(new_mask, next_point)
#                 total_distance = dist_matrix[current_point][next_point] + distance

#                 if total_distance < min_distance:
#                     min_distance = total_distance
#                     min_path = [current_point] + path
#                     min_x_list = [x_list[current_point]] + x_path
#                     min_y_list = [y_list[current_point]] + y_path

#         # memoize the solution and return
#         memo[memo_key] = min_distance, min_path, min_x_list, min_y_list
#         return min_distance, min_path, min_x_list, min_y_list

#     # start the dynamic programming recursion
#     optimal_distance, optimal_path, x_coords, y_coords = tsp_dp_helper({0}, 0)

#     return optimal_distance, optimal_path, x_coords, y_coords

# # Example usage:
# distance, path, x_coords, y_coords = tsp_dynamic_programming("myTest.txt")
# print("Optimal Distance:", distance)
# #print("Optimal Path:", path)
# #print("X Coordinates of Optimal Path:", x_coords)
# #print("Y Coordinates of Optimal Path:", y_coords)