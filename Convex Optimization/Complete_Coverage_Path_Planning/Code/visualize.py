from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import string
import copy
import utils

def Plot_Env(poly_list, point_list, start):
    """
    Polt the original environment with the given obstacles, rubbishes and starting point
    """
    temp_x = []
    temp_y = []

    plt.figure(figsize=(10, 10))
    for idx, (point_x, point_y) in enumerate(point_list):
        temp_x.append(point_x)
        temp_y.append(point_y)
        plt.text(point_x - 0.2, point_y - 0.2, '(Pt{}: {}, {})'.format(idx+1, point_x, point_y))
    plt.plot(temp_x, temp_y, 'ro')

    for i, poly in enumerate(poly_list):
        x = []
        y = []
        for j, (point_x, point_y) in enumerate(poly):
            x.append(point_x)
            y.append(point_y)
        if i > 0:
            name_x = np.mean(np.array(x))
            name_y = np.mean(np.array(y))
            plt.text(name_x, name_y, string.ascii_uppercase[i - 1])
        plt.plot(x, y, 'k-')

    plt.plot(start[0], start[1], 'b*')
    plt.axis('equal')

def Plot_Figure(x, y, title, fname, point, color = 'lightcoral', marker = 'o'):
    plt.figure(figsize=(10,10))
    plt.plot(x, y, color=color, linestyle='--', marker='o')
    plt.title(title)
    plt.xlabel("Distance from {} ".format(point))
    plt.ylabel("Objective function value")
    plt.savefig(fname + '.png')


def Plot_Coverage(fro, to, width, height):
    pts = utils.Cal_Extreme_Points(fro, to, width, height)
    x = []
    y = []
    for idx, (point_x, point_y) in enumerate(pts):
        x.append(point_x)
        y.append(point_y)
    plt.plot(x, y,linestyle = '-',color = 'cornflowerblue')

def Plot_Route(rubbish, start, sequence):
    """ 
    Plot the route when we use rubbish points as a proxy 
    for the center of cleaning vehicle
    """
    point_list = copy.deepcopy(rubbish)
    point_list.insert(0, start)
    x = []
    y = []
    for idx in sequence:
        x.append(point_list[idx][0])
        y.append(point_list[idx][1])
    plt.plot(x, y, linestyle='--', color='grey')

def Plot_Trail(x, y, width, height):
    for idx in range(len(x) - 1):
        fro = (x[idx], y[idx])
        to = (x[idx + 1], y[idx + 1])
        Plot_Coverage(fro, to, width, height)
    
    plt.plot(x, y, linestyle='--', color='grey')
    plt.plot(x, y, 'bo')

def Plot_Poly_Points(poly, points):
    plt.figure(figsize=(8, 8))
    x = []
    y = []
    for (point_x, point_y) in poly:
        x.append(point_x)
        y.append(point_y)
        plt.text(point_x, point_y, '({},{})'.format(point_x, point_y))
    plt.plot(x, y, 'k-')
    name_x = np.mean(np.array(x))
    name_y = np.mean(np.array(y))
    plt.text(name_x, name_y, 'A')
    
    fig = plt.gcf()
    ax = plt.gca()

    for i, point in enumerate(points):
        plt.plot(point[0], point[1], 'ro')
        plt.text(point[0] - 0.2, point[1] - 0.2, '(Pt{}: {}, {})'.format(i+1, point_x, point_y))
        circle = plt.Circle((point[0], point[1]), ((0.57 / 2) ** 2 + (0.7 / 2) ** 2) ** 0.5, color='orange', alpha=0.3)
        ax.add_artist(circle)

    # Add arrows
    r = 0.5 * (0.57 ** 2 + 0.7 ** 2) ** 0.5
    plt.arrow(poly[2][0],poly[2][1], 0, -r, head_width=0.05, fc='k')
    
    plt.axis('equal')
    plt.title('A Closer Look At Polygon A')
    plt.savefig('./plots/polya.png')




if __name__ == '__main__':
    width = 0.57
    height = 0.7
    # All the points are labeled counter-clockwise
    start = (0.57 / 2, 0.7 / 2)
    POLY_0 = [(0, 0), (0.57, 0), (0.57, 0.7), (0, 0.7), (0, 0)]
    POLY_A = [(1.23,3.47), (1.40,2.67), (1.58,2.30),(2.10,3.63), (1.75,4.00), (1.23,3.47)]
    POLY_B = [(4.00,6.48), (4.65,5.98), (5.90,6.95), (5.06,7.73), (4.52,7.68),(4.00,6.48)]
    POLY_C = [(6.78,3.40), (7.78,3.76), (7.78,5.10), (6.78,3.40)]
    POLY_D=[(4.00,3.00), (4.37,2.75), (4.80,3.45), (4.35,3.35), (4.00,3.00)]
    poly_list = [POLY_0, POLY_A, POLY_B, POLY_C, POLY_D]
    rubbish = [(0.40,3.00), (2.90,2.20), (1.10,6.50), (2.90,5.00), (3.00,8.30), (5.20,4.80), \
        (7.40,7.40), (5.30,1.20), (7.80,2.60), (6.00,6.00), (9.00,4.80), (5.00,8.50), (7.00,1.50), (2.50,7.50)]
    Plot_Env(poly_list, rubbish, start)
    plt.title("Problem Setting")
    plt.savefig("./plots/env.png")

    sequence = [0, 1, 2, 8, 13, 9, 11, 7, 10, 6, 4, 3, 14, 5, 12]
    Plot_Env(poly_list, rubbish, start)
    Plot_Route(rubbish, start, sequence)
    plt.title("Visting Order Determined By TSP")
    plt.savefig("./plots/route.png")

    Plot_Poly_Points(POLY_A, (rubbish[0], rubbish[1]))
    
