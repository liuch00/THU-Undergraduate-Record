from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import visualize

def obj(x):
    """
    Objective Function
    """
    start = np.array((0.57 / 2, 0.7 / 2))
    dims = int(len(x) / 2)
    x_new = x[: dims]
    y_new = x[dims: ]
    ret = ((x_new[0] - start[0]) ** 2 + (y_new[0] - start[1]) ** 2) ** 0.5
    for idx in range(dims - 1):
        next_idx = idx + 1
        tmp1 = (x_new[idx] - x_new[next_idx]) ** 2 
        tmp2 = (y_new[idx] - y_new[next_idx]) ** 2
        tmp = (tmp1 + tmp2) ** 0.5
        ret += tmp
    return ret


def cons(x):
    """
    Constraints: each center shoulde fall within a circle with rubbish as its center
    """
    rubbish = [(0.40,3.00), (2.90,2.20), (1.10,6.50), (2.90,5.00), (3.00,8.30), (5.20,4.80), \
        (7.40,7.40), (5.30,1.20), (7.80,2.60), (6.00,6.00), (9.00,4.80), (5.00,8.50), (7.00,1.50), (2.50,7.50)]
    sequence = [1, 2, 8, 13, 9, 11, 7, 10, 6, 4, 3, 14, 5, 12]
    centers_x = []
    centers_y = []
    for i in sequence:
        centers_x.append(rubbish[i - 1][0])
        centers_y.append(rubbish[i - 1][1])

    centers_x = np.array(centers_x)
    centers_y = np.array(centers_y)


    dims = int(len(x) / 2)

    x_new = x[: dims]
    y_new = x[dims: ]

    ret = - (x_new - centers_x) ** 2 - (y_new - centers_y) ** 2 + 0.57 ** 2 / 4 + 0.7 ** 2 / 4
    return ret

def Solve_Cvx(rubbish):
    """
    The process of solving the convex programming
    """
    sequence = [1, 2, 8, 13, 9, 11, 7, 10, 6, 4, 3, 14, 5, 12]
    centers_x = []
    centers_y = []
    for i in sequence:
        centers_x.append(rubbish[i - 1][0])
        centers_y.append(rubbish[i - 1][1])

    centers_x.extend(centers_y)
    x0 = np.array(centers_x)
    constraints = [dict(type='ineq', fun=cons)]
    x_cons_opt = minimize(obj, x0,method='SLSQP',constraints=constraints)
    return x_cons_opt.x, x_cons_opt.fun

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
    x, fun = Solve_Cvx(rubbish)
    print("optimal value {}".format(fun))

    # Do some visualization
    visualize.Plot_Env(poly_list, rubbish, start)
    dims = int(len(x) / 2)

    x_new = x[: dims]
    y_new = x[dims: ]

    x_new = np.hstack((np.array(start[0]), x_new))
    y_new = np.hstack((np.array(start[0]), y_new))

    visualize.Plot_Trail(x_new, y_new, width, height)

    plt.title("Optimal Route Without Collision Avoidance")
    plt.savefig('./plots/cvx_programming.png')

    