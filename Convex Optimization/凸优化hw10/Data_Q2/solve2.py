import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import math
from scipy import linalg


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
def r(x, lamb, mu, t, A, b, P, q):
    m = x.shape[0]
    rdual = df(x, P, q) - lamb + A.T @ mu
    rcent = np.diag(lamb) @ x - np.ones(m) / t
    rpri = A @ x - b
    return np.r_[rdual, rcent, rpri]


def dual_search(x, lamb, mu, deltax, deltalambda, deltamu, t, r, A, b, alpha, beta):
    w = -lamb / deltalambda
    w[w < 0] = 1
    w = np.append(w, [1])
    s = 0.99 * np.min(w)
    while (x + s * deltax < 0).any() or linalg.norm(r(x + s * deltax,
                 lamb + s * deltalambda, mu + s * deltamu, t, A, b, P, q)) > \
                (1 - alpha * s) * linalg.norm(r(x, lamb, mu, t, A, b, P, q)):
        s = s * beta
    return s


def dual(f, df, H, x0, lambda0, mu0, P, q, A, b, u, alpha, beta,
         eps_pri=1e-10, eps_dual=1e-10, eps_eta=1e-10):
    x = x0.copy()
    lamb = lambda0.copy()
    mu = mu0.copy()
    m = x0.shape[0]
    eta = np.sum(x0 * lambda0)
    etatrack = [eta]
    t = u * m / eta
    rdual = df(x0, P, q) - lambda0 + A.T @ mu0
    rcent = np.diag(lambda0) @ x0 - np.ones(m) / t
    rpri = A @ x - b
    rtrack = [(linalg.norm(rpri)**2 + linalg.norm(rdual)**2)**0.5]
    indi = 0
    while linalg.norm(rdual) > eps_dual or linalg.norm(rpri) > eps_pri or eta > eps_eta:
        line1 = np.c_[H(x, P, q), -np.diag(np.ones(m)), A.T]
        line2 = np.c_[np.diag(lamb), np.diag(x), np.zeros((m, A.shape[0]))]
        line3 = np.c_[A, np.zeros((A.shape[0], (A.shape[0] + m)))]
        AAmat = np.r_[line1, line2, line3]
        bbmat = -np.r_[rdual, rcent, rpri]
        sol = linalg.solve(AAmat, bbmat)
        deltax = sol[:m]
        deltalambda = sol[m: 2 * m]
        deltamu = sol[2 * m:]
        s = dual_search(x, lamb, mu, deltax, deltalambda, deltamu, t, r, A, b, alpha, beta)
        x = x + s * deltax
        lamb = lamb + s * deltalambda
        mu = mu + s * deltamu
        eta = np.sum(x * lamb)
        etatrack.append(eta)
        t = u * m / eta
        rdual = df(x, P, q) - lamb + A.T @ mu
        rcent = np.diag(lamb) @ x - np.ones(m) / t
        rpri = A @ x - b
        rtrack.append((linalg.norm(rpri)**2 + linalg.norm(rdual)**2)**0.5)
        indi += 1
        print('\r' + 'iter: ' + str(indi) + ', rdual = ' + str(round(linalg.norm(rdual), 10)) +
              ', rpri = ' + str(round(linalg.norm(rpri), 10)) +
              ', eta = ' + str(eta), end='', flush=True)
    return x, lamb, mu, etatrack, rtrack



if __name__ == "__main__":
    P = loadmat('./P.mat')['P']  # shape = (200, 200)
    q = loadmat('./q.mat')['q'].reshape(-1)  # shape = (200,)
    A = loadmat('./A.mat')['A']  # shape = (100, 200)
    b = loadmat('./b.mat')['b'].reshape(-1)  # shape = (100,)
    x0 = loadmat('./x_0.mat')['x_0'].reshape(-1)  # shape = (200,)
    lambda0 = loadmat('./lambda.mat')['lambda'].reshape(-1)  # shape = (200,)
    mu0 = loadmat('./mu.mat')['mu'].reshape(-1)  # shape = (100,)
    xdual, lambdual, mudual, etatrack, rtrack = dual(f, df, H, x0, lambda0, mu0, P, q,A, b, u=10, alpha=0.01, beta=0.5)
    pdual = f(xdual, P, q)
    print(' p* = ' + str(round(pdual, 10)))
    print('x* = ')
    print(xdual)
    print('lambda* = ')
    print(lambdual)
    print('mu* = ')
    print(mudual)
    plt.figure(figsize=(10, 6))
    plt.plot(np.log(etatrack), color='skyblue')
    plt.xlabel('Newton iterations')
    plt.ylabel('$\log \hat{\eta}$')
    plt.grid(alpha=0.25)
    plt.title('Primal Dual Interior Point Method')
    plt.savefig('2.png', )

    plt.figure(figsize=(10, 6))
    plt.plot(np.log(rtrack), color='skyblue')
    plt.xlabel('Newton iterations')
    plt.ylabel('$\log\{(||r_{pri}||_{2}^{2} + ||r_{dual}||_{2}^{2})^{1/2}\}$')
    plt.grid(alpha=0.25)
    plt.title('Primal Dual Interior Point Method')
    plt.savefig('3.png')
