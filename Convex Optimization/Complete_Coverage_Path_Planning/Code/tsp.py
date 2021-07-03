"""Simple travelling salesman problem between cities."""
import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

rubbish = [(0.57 / 2, 0.7 / 2), (0.40,3.00), (2.90,2.20), (1.10,6.50), (2.90,5.00), (3.00,8.30), (5.20,4.80), \
        (7.40,7.40), (5.30,1.20), (7.80,2.60), (6.00,6.00), (9.00,4.80), (5.00,8.50), (7.00,1.50), (2.50,7.50)]


num_nodes = len(rubbish) + 1
DIST = np.zeros((num_nodes, num_nodes))
for i in range(num_nodes - 1):
    for j in range(num_nodes - 1):
        x1, y1 = rubbish[i]
        x2, y2 = rubbish[j]
        # The API only allows integer distances, so we rescale it to reduce the rounding error.
        DIST[i, j] = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 * 100000


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = DIST
    data['num_vehicles'] = 1
    data['starts'] = [0]
    data['ends'] = [15]
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        idx1 = manager.IndexToNode(index)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        temp = routing.GetArcCostForVehicle(previous_index, index, 0)
        route_distance += temp
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    print(plan_output)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['starts'],
                                           data['ends'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == '__main__':
    main()