from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import visualize
import calculate_angles
import utils
def obj(x):
    """
    Objective function
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

def cons1(x):
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
    x_new = np.hstack((np.array(x[0]), x[2: 6], x[7: dims]))
    y_new = np.hstack((np.array(x[dims]), x[dims + 2: dims + 6], x[dims + 7 :]))


    ret = - (x_new - centers_x) ** 2 - (y_new - centers_y) ** 2 + 0.57 ** 2 / 4 + 0.7 ** 2 / 4
    return ret

def cons2(x, dist1, dist2):
    """
    Linear inequality constraint
    """
    dims = int(len(x) / 2)
    y1 = x[dims + 1]
    y2 = x[dims + 6]
    y = np.array([y1, y2])
    ret = np.array([2.3, 3.76]) - np.array([dist1, dist2]) - (0.57 ** 2 / 4 + 0.7 ** 2 / 4) ** 0.5 - y
    return ret

def cons3(x):
    """
    Equality constraint
    """
    x1 = x[1]
    x2 = x[6]
    x = np.array([x1, x2])
    ret = x - np.array([1.58, 7.78])

    return ret



def Solve_Cvx(dist1, dist2):
    sequence = [1, 2, 8, 13, 9, 11, 7, 10, 6, 4, 3, 14, 5, 12]
    centers_x = []
    centers_y = []
    for i in sequence:
        centers_x.append(rubbish[i - 1][0])
        centers_y.append(rubbish[i - 1][1])

    centers_x.insert(1, 1.58)
    centers_x.insert(6, 7.78)

    centers_y.insert(1, 2.3 - 2 * (0.57 ** 2 / 4 + .7 ** 2 / 4) ** 0.5)
    centers_y.insert(6, 3.76 - 2 * (0.57 ** 2 / 4 + .7 ** 2 / 4) ** 0.5)

    centers_x.extend(centers_y)
    x0 = np.array(centers_x)
    constraints = [dict(type='ineq', fun=cons1), dict(type='ineq', fun=cons2, args=[dist1, dist2]), dict(type='eq', fun=cons3)]
    x_cons_opt = minimize(obj, x0,method='SLSQP',constraints=constraints)
    return x_cons_opt.x, x_cons_opt.fun

def Adjust_PolyA_PolyC(stepsize, width, height):
    """
    Use grid search to relax or tighten the constraints
    """
    dist1 = 0
    dist2 = 0
    fun1_track = []
    dist1_track = []
    while True:
        sol, fun = Solve_Cvx(dist1, dist2)
        fun1_track.append(fun)
        dist1_track.append((width ** 2 / 4 + height ** 2 / 4) ** 0.5 + dist1)
        dims = int(len(sol) / 2)
        x = sol[: dims]
        y = sol[dims: ]
        fro = (x[0], y[0])
        to = (x[1], y[1])
        poly1 = utils.Cal_Extreme_Points(fro, to, width, height)
        if utils.Check_Intersect_Poly(poly1, POLY_A):
            break
        dist1 -= stepsize
    
    dist1_track = dist1_track[: -1]
    fun1_track = fun1_track[: -1]
    dist1 += stepsize

    fun2_track = []
    dist2_track = []

    while True:
        sol, fun = Solve_Cvx(dist1, dist2)
        dims = int(len(sol) / 2)
        x = sol[: dims]
        y = sol[dims: ]
        fro = (x[6], y[6])
        to = (x[7], y[7])
        poly2 = utils.Cal_Extreme_Points(fro, to, width, height)

        dist2_track.append((width ** 2 / 4 + height ** 2 / 4) ** 0.5 + dist2)
        fun2_track.append(fun)

        fro = (x[0], y[0])
        to = (x[1], y[1])
        poly1 = utils.Cal_Extreme_Points(fro, to, width, height)
        print("Check intersect", utils.Check_Intersect_Poly(poly1, POLY_A))

        if not utils.Check_Intersect_Poly(poly2, POLY_C):
            break
        dist2 += stepsize
    print("Optimal Value {}".format(fun))
    print("dist1 {}, dist2 {}".format(dist1, dist2))
    return (x, y, dist1, dist2, fun, dist1_track, fun1_track, dist2_track, fun2_track)


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
    sequence = [1, 2, 8, 13, 9, 11, 7, 10, 6, 4, 3, 14, 5, 12]
    x, fun = Solve_Cvx(dist1=0, dist2=0)
    print("Optimal value {}".format(fun))
    
    # Do some visualization
    visualize.Plot_Env(poly_list, rubbish, start)
    dims = int(len(x) / 2)

    x_new = x[: dims]
    y_new = x[dims: ]

    x_new = np.hstack((np.array(start[0]), x_new))
    y_new = np.hstack((np.array(start[0]), y_new))

    visualize.Plot_Trail(x_new, y_new, width, height)

    fig = plt.gcf()
    ax = plt.gca()

    circle1 = plt.Circle((7.78, 3.67), ((0.57 / 2) ** 2 + (0.7 / 2) ** 2) ** 0.5, color='purple', fill=False)
    circle2 = plt.Circle((1.58, 2.3), ((0.57 / 2) ** 2 + (0.7 / 2) ** 2) ** 0.5, color='purple', fill=False)
    ax.add_artist(circle1)
    ax.add_artist(circle2)

    r = 0.5 * (0.57 ** 2 + 0.7 ** 2) ** 0.5
    plt.arrow(2.1 ,2.3 - r, 0, r, head_width=0.05, fc='purple', ec='purple')
    plt.arrow(8 ,3.5, 0, r, head_width=0.05, fc='purple', ec='purple')

    plt.title("Optimal Route After Adding Linear Constraints")
    plt.savefig('./plots/add_constraint.png')


    x, y, _, _, _, _, _, _, _,= Adjust_PolyA_PolyC(0.01, width, height)

    visualize.Plot_Env(poly_list, rubbish, start)
    visualize.Plot_Trail(x, y, width, height)
    plt.title("Optimal Route After Grid Search")
    plt.savefig('./plots/gridsearch.png')

    calculate_angles.run(rubbish, sequence, x, y)

    visualize.Plot_Env(poly_list, rubbish, start)
    visualize.Plot_Trail(x, y, width, height)
    plt.title("Optimal Route After Grid Search")
    plt.savefig('./plots/gridsearch.png')

    for i in range(len(x)):
        print("No.{}, ({},{})".format(i, x[i], y[i]))

