from scipy.optimize import minimize
import numpy as np
import cvxpy as cp

def Turn_To_Matrix(poly):
    """
    Turn a polygeon into linear inequalities
    """
    nrow = len(poly) - 1
    ncol = 2
    b = np.zeros(nrow)
    A = np.zeros((nrow, ncol))
    for idx in range(len(poly) - 1):
        pt1 = poly[idx]
        pt2 = poly[idx + 1]
        A[idx, 0] = pt2[1] - pt1[1] # y2-y1
        A[idx, 1] = pt1[0] - pt2[0] # x1-x2
        b[idx] = pt1[0] * (pt2[1] - pt1[1]) - pt1[1] * (pt2[0] - pt1[0])
    return (A, b)

def Check_Intersect_Poly(poly1, poly2):
    """
    @poly1, poly2: tuples with coordinates of vertex
    """
    A1, b1 = Turn_To_Matrix(poly1)
    A2, b2 = Turn_To_Matrix(poly2)
    x = cp.Variable(A1.shape[1])
    prob = cp.Problem(cp.Minimize(1), [A1 @ x <= b1, A2 @ x <= b2])
    prob.solve()
    if prob.status == "optimal":
        return True
    else:
        return False


def Cal_Extreme_Points(fro, to, width, height):
    """
    Given the center of two positions, calculate the vertex of the rectangle
    """
    x1 = fro[0]
    y1 = fro[1]
    x2 = to[0]
    y2 = to[1]
    cos = (x2 - x1) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    sin = (y2 - y1) / ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    mid1_x = x1 - cos * 0.5 * height
    mid1_y = y1 - sin * 0.5 * height
    point1_x = mid1_x - sin * 0.5 * width
    point1_y = mid1_y + cos * 0.5 * width
    point2_x = mid1_x + sin * 0.5 * width
    point2_y = mid1_y - cos * 0.5 * width

    mid2_x = x2 + cos * 0.5 * height
    mid2_y = y2 + sin * 0.5 * height
    point3_x = mid2_x + sin * 0.5 * width
    point3_y = mid2_y - cos * 0.5 * width
    point4_x = mid2_x - sin * 0.5 * width
    point4_y = mid2_y + cos * 0.5 * width

    ret = ((point1_x, point1_y), (point2_x, point2_y), (point3_x, point3_y), (point4_x, point4_y), (point1_x, point1_y))
    return ret
