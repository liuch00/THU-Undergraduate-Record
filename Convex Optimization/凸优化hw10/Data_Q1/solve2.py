import numpy as np
import matplotlib.pyplot as plt
import mat4py
import math

class obj_func(object):
    def __init__(self,a,b):
        self.a=np.array(a)
        self.b=np.array(b)

    def check(self,x):
        if np.any(x<=0):
            return False
        else:
            return  True

    def call_func(self,x):
        return np.dot(x,np.log(x))

    def call_grad(self,x):
        return 1+np.log(x)

    def call_hessian(self,x):
        return np.diag(1/x)


    def call_direction(self,hessian,grad,x,v):
        zero = np.zeros((self.a.shape[0], self.a.shape[0]))
        l = np.concatenate((hessian,self.a))
        r = np.concatenate((self.a.T,zero))
        tmp = np.concatenate((l,r),axis=1)

        r_pri = np.matmul(self.a, x) - self.b
        rhs = - np.concatenate((grad, r_pri))
        tmp2 = np.matmul(np.linalg.inv(tmp), rhs)

        direction_x = - tmp2[: self.a.shape[1]]
        next_v = tmp2[self.a.shape[1]:]
        direction_v = v - next_v
        return direction_x, direction_v

    def residual_norm(self,x,v,grad):
        r_pri = np.matmul(self.a, x) - self.b
        r_dual = grad + np.matmul(self.a.T, v)
        r = np.concatenate((r_pri, r_dual))
        return np.linalg.norm(r_pri, 2), np.linalg.norm(r_dual, 2), np.linalg.norm(r, 2)




class solve(object):
    def __init__(self, obj_func):
        self.obj_func = obj_func
        self.process = []
        self.stepsize = []
        self.r_dual = []
        self.r_pri = []

    def backtrack(self, x, v, direction_x, direction_v, gradient, alpha=0.1, beta=0.5):
        t = 1.0
        while True:
            left_x = x - t * direction_x
            left_v = v - t*direction_v
            if self.obj_func.check(left_x):
                _,_,left = self.obj_func.residual_norm(left_x,left_v,gradient)
                _, _, right = self.obj_func.residual_norm(x, v, gradient)
                if left <= (1-alpha*t)*right:
                    break
            t *= beta
        print("backtrack finish")
        return t

    def search(self, initial,v):
        self.process = []
        self.stepsize = []
        self.r_dual = []
        self.r_pri = []
        if not self.obj_func.check(initial):
            raise ValueError("initial point is not correct")
        else:
            ctr = 0
            current_x = initial
            current_v = v
            eta = float('inf')
            while True:
                ctr += 1
                print("iteration {:d}".format(ctr))
                gradient = self.obj_func.call_grad(current_x)
                self.process.append(self.obj_func.call_func(current_x))
                if eta <= 1e-10:
                    break
                hessian = self.obj_func.call_hessian(current_x)
                direction_x,direction_v = self.obj_func.call_direction(hessian, gradient,current_x,current_v)
                eta_pri,eta_dual,eta = self.obj_func.residual_norm(current_x,current_v,gradient)
                self.r_dual.append(eta_dual)
                self.r_pri.append(eta_pri)
                t = self.backtrack(current_x, current_v, direction_x, direction_v, gradient)
                self.stepsize.append(t)
                current_x -= t * direction_x
                current_v -= t * direction_v
                print("stepsize:", t)

        print("total number of iterations {:d}".format(ctr))
        print("optimum", self.process[-1])
        print("current_x", current_x)
        print("current_v", current_v)
        return current_x

    def plot(self, name):
        optimum = self.process[-1]
        y = [(f - optimum) for f in self.process[:-1]]
        print('y ',y)
        plt.figure(figsize=(10, 6))
        plt.plot(y, color="gray", linestyle='--', marker='+')
        plt.xlabel("number of iterations k")
        plt.ylabel("log(f-p*)")
        plt.title("log error v.s. number of iterations")
        plt.savefig(name + "_1.png")

        plt.figure(figsize=(10, 6))
        plt.plot(self.r_pri, color="gray", linestyle='--', marker='+',label='primal residual')
        plt.plot(self.r_dual, color="blue", linestyle='--', marker='o', label='dual residual')
        plt.legend()
        plt.xlabel("number of iterations k")
        plt.ylabel("l_2 norm of primal and dual residuals")
        plt.title("l_2 norm of residuals v.s. number of iterations")
        plt.savefig(name+"_2.png")



if __name__ == "__main__":
    A = mat4py.loadmat('./A.mat')['A']
    b = mat4py.loadmat('./b.mat')['b']
    b = [temp[0] for temp in b]
    x_1 = mat4py.loadmat('./x_1.mat')['x_1']
    x_1 = np.array([x[0] for x in x_1])
    obj_func = obj_func(A, b)
    solver = solve(obj_func)
    zeros = np.zeros(len(A))
    solver.search(initial=x_1, v=zeros)
    solver.plot("p2")
