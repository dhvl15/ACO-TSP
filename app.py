from flask import Flask, render_template, request, jsonify
from TSP import *
import matplotlib.pyplot as plt, matplotlib
from PIL import Image, ImageTk
matplotlib.use('Agg')
from TSP_DP import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_acs', methods=['POST'])
def run_acs():
    data = request.get_json()
    problem = data['problem']+".txt"
    max_gen = int(data['max_gen'])
    test_times = int(data['test_times'])

    avg_list = []

    for i in range(test_times):
        my_acs = ACS(city_name=problem)
        my_acs.init()
        best_distances = []  # Store the best distances for each run

        # Run the ACS algorithm for 'max_gen' generations
        for j in range(max_gen):
            my_acs.path_construct()
            my_acs.pheromone_update()
            best_distances.append(my_acs.best.dis)
            if(i==0) :
                x_seq = []
                y_seq = []
                for i in range(my_acs.num_city):
                    x_seq.append(my_acs.city.x_list[my_acs.best.path[i]])
                    y_seq.append(my_acs.city.y_list[my_acs.best.path[i]])
                x_seq.append(my_acs.city.x_list[my_acs.best.path[0]])
                y_seq.append(my_acs.city.y_list[my_acs.best.path[0]])
                plt.figure(figsize=(8, 6))
                plt.plot(x_seq, y_seq, color='green', linewidth=2, marker='x', markersize=8, label='Initail Optimal Path')
                plt.scatter(x_seq, y_seq, color='red', marker='o', s=50, label='Visited Cities')
                plt.title('Ant Colony Optimization (ACS)')
                for a, b in zip(x_seq, y_seq):
                    plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)
                plt.legend()
                plt.savefig("static/images/init_path.png")
            

        avg_list.append(best_distances)

        x_seq = []
        y_seq = []
        for i in range(my_acs.num_city):
            x_seq.append(my_acs.city.x_list[my_acs.best.path[i]])
            y_seq.append(my_acs.city.y_list[my_acs.best.path[i]])
        x_seq.append(my_acs.city.x_list[my_acs.best.path[0]])
        y_seq.append(my_acs.city.y_list[my_acs.best.path[0]])

        
        # Update Path Plot
        plt.figure(figsize=(8, 6))
        plt.plot(x_seq, y_seq, color='green', linewidth=2, marker='x', markersize=8, label='Optimal Path')
        plt.scatter(x_seq, y_seq, color='red', marker='o', s=50, label='Visited Cities')
        plt.title('Ant Colony Optimization (ACS)')
        for a, b in zip(x_seq, y_seq):
            plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)
        plt.legend()
        plt.savefig("static/images/update_path.png")

        # Result Curve Plot
        x = list(range(1, 51))
        plt.figure(figsize=(8, 6))
        plt.plot(x, best_distances, color='blue', linewidth=2, label='Best Distances')
        plt.title('Evolution of Best Distances')
        plt.xlabel('Generation')
        plt.ylabel('Distance')
        plt.legend()
        plt.grid(True)
        plt.savefig("static/images/result_curve.png")

        plt.close("all")



    # Calculate the average distances and standard deviation
    avg_data = {
        'average_distances': [sum(distances) / len(distances) for distances in zip(*avg_list)],
        'std_deviation': sum([best_dis for best_dis in best_distances]) / len(best_distances),
        'optimal_path': 'static/images/update_path.png',
        'curve_path' : "static/images/result_curve.png",
        'init_path' : "static/images/init_path.png"
    }

    return jsonify(avg_data)

@app.route('/run_tsp', methods=['POST'])
def run_tsp():
    data = request.get_json()
    problem = data['problem']+".txt"

    distance, path, x_coords, y_coords = tsp_nearest_neighbor(problem)

    plt.figure(figsize=(8, 6))
    plt.plot(x_coords, y_coords, color='green', linewidth=2, marker='x', markersize=8, label='Optimal Path')
    plt.scatter(x_coords, y_coords, color='red', marker='o', s=50, label='Visited Cities')
    plt.title('Nearest Neighbour (TSP)')
    for a, b in zip(x_coords, y_coords):
        plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)
    plt.legend()
    plt.savefig("static/images/update_path2.png")

    # Calculate the average distances and standard deviation
    avg_data = {
        'average_distances': distance,
        'optimal_path': 'static/images/update_path2.png',
    }

    return jsonify(avg_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
