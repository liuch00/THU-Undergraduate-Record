import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import math
from scipy import linalg
from sklearn.linear_model import LinearRegression

def f(x, P, q):
    return (0.5 * (x.reshape(-1, 1)).T @ P @ x.reshape(-1, 1) + np.sum(q * x))[0][0]


def df(x, P, q):
    return P @ x + q


def H(x, P, q):
    return P


def F(x, P, q, t):
    return (t * (0.5 * (x.reshape(-1, 1)).T @ P @ x.reshape(-1, 1) +
                 np.sum(q * x)) - np.sum(np.log(x)))[0][0]


def dF(x, P, q, t):
    return t * (P @ x + q) - 1 / x


def HF(x, P, q, t):
    return t * P + np.diag(1 / x**2)

def back_search(func, df, x, d, alpha, beta, P, q, t):
    ans = 1
    fx = func(x, P, q, t)
    dfx = df(x, P, q, t)
    while func(x + ans * d, P, q, t) > fx + alpha * ans * np.sum(dfx * d) or \
            np.isnan(func(x + ans * d, P, q, t)):
        ans = beta * ans
    return ans

def feasible_newton(f, df, H, x0, A, b, P, q, t, alpha, beta, ttrack, eta=1e-10):
    m = A.shape[0]
    n = A.shape[1]
    dfx0 = df(x0, P, q, t)
    Hx0 = H(x0, P, q, t)
    x = x0.copy()
    Alarge = np.r_[np.c_[Hx0, A.T], np.c_[A, np.zeros((m, m))]]
    blarge = np.r_[-dfx0, np.zeros(m)]
    deltax = linalg.solve(Alarge, blarge)[:n]
    lambdax = (deltax.reshape(-1, 1).T @ Hx0 @ deltax.reshape(-1, 1))**0.5
    ttrack.append(t)
    indi = 0
    while lambdax**2 / 2 > eta and indi < 50:
        indi += 1
        tt = back_search(f, df, x, deltax, alpha, beta, P, q, t)
        x += tt * deltax
        dfx = df(x, P, q, t)
        Hx = H(x, P, q, t)
        Alarge = np.r_[np.c_[Hx, A.T], np.c_[A, np.zeros((m, m))]]
        blarge = np.r_[-dfx, np.zeros(m)]
        deltax = linalg.solve(Alarge, blarge)[:n]
        lambdax = ((deltax.reshape(-1, 1).T @ Hx @ deltax.reshape(-1, 1))**0.5)[0][0]
        ttrack.append(t)
        print('\r' + 'iter: ' + str(indi) + ', error = ' + str(round(lambdax**2 / 2, 10)) +
              ', t = ' + str(t), end='', flush=True)
    return x, ttrack


def barrier(f, df, H, x0, A, b, P, q, alpha, beta, t, mu=10, epsilon=1e-10):
    m = x0.shape[0]
    x = x0.copy()
    ttrack = []
    i = 0
    while m / t >= epsilon and i < 15:
        i += 1
        xnew, ttrack = feasible_newton(f, df, H, x, A, b, P, q, t, alpha, beta, ttrack)
        x = xnew
        t = mu * t
    return x, ttrack


if __name__ == "__main__":
    P = loadmat('./P.mat')['P']  # shape = (200, 200)
    q = loadmat('./q.mat')['q'].reshape(-1)  # shape = (200,)
    A = loadmat('./A.mat')['A']  # shape = (100, 200)
    b = loadmat('./b.mat')['b'].reshape(-1)  # shape = (100,)
    x0 = loadmat('./x_0.mat')['x_0'].reshape(-1)  # shape = (200,)
    lambda0 = loadmat('./lambda.mat')['lambda'].reshape(-1)  # shape = (200,)
    mu0 = loadmat('./mu.mat')['mu'].reshape(-1)  # shape = (100,)

    x_star, ttrack = barrier(F, dF, HF, x0, A, b, P, q, alpha=0.01, beta=0.5, t=1)
    p_star = f(x_star, P, q)
    lambda_star = 1 / ttrack[-1] / x_star
    model = LinearRegression()
    model.fit(A.T, -df(x_star, P, q) + lambda_star)
    mu_star = model.coef_
    print(' p* = ' + str(round(p_star, 10)))
    print('x* = ')
    print(x_star)
    print('lambda* = ')
    print(lambda_star)
    print('mu* = ')
    print(mu_star)
    plt.figure(figsize=(10, 6))
    plt.plot(np.log(x0.shape[0] / np.array(ttrack)), color='skyblue')
    plt.xlabel('Newton iterations')
    plt.ylabel('Duality Gap ($\log(n/t)$)')
    plt.grid(alpha=0.25)
    plt.title('Barrier Method')
    plt.savefig('1.png')