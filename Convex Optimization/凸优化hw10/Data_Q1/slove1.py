import numpy as np
import matplotlib.pyplot as plt
import mat4py
import math

class obj_func(object):
    def __init__(self,a):
        self.a=np.array(a)

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

    def call_direction(self,hessian,grad):
        zero1=np.zeros(self.a.shape[0])
        tmp1=np.concatenate((-grad,zero1))
        zero2 = np.zeros((self.a.shape[0], self.a.shape[0]))
        l=np.concatenate((hessian,self.a))
        r=np.concatenate((self.a.T,zero2))
        tmp2=np.concatenate((l,r),axis=1)
        return -np.matmul(np.linalg.inv(tmp2),tmp1)[:self.a.shape[1]]


class solve(object):
    def __init__(self, obj_func):
        self.obj_func = obj_func
        self.process = []
        self.stepsize = []
        self.current_x=[]

    def backtrack(self, x, direction, gradient, alpha=0.2, beta=0.8):
        t = 1.0
        while True:
            left = x - t * direction
            if self.obj_func.check(left):
                if self.obj_func.call_func(left) <= self.obj_func.call_func(x) - alpha * t * np.dot(gradient, direction):
                    break
            t *= beta
        print("backtrack finished")
        return t

    def search(self, initial):
        self.process = []
        if not self.obj_func.check(initial):
            raise ValueError("Initial point is not correct")
        else:
            ctr = 0
            current_x = initial
            self.current_x.append(current_x)
            eta = float('inf')
            while True:
                ctr += 1
                print("iteration {:d}".format(ctr))
                gradient = self.obj_func.call_grad(current_x)
                self.process.append(self.obj_func.call_func(current_x))
                if eta <= 1e-10:
                    break
                hessian = self.obj_func.call_hessian(current_x)
                direction = self.obj_func.call_direction(hessian, gradient)
                eta = np.matmul(np.matmul(direction, hessian), direction) / 2
                t = self.backtrack(current_x, direction, gradient)
                self.stepsize.append(t)
                current_x -= t * direction
                self.current_x.append(current_x)
                print("stepsize:", t)
                print("eta", eta)
        print("total number of iterations {:d}".format(ctr))
        print("optimum", self.process[-1])
        print("current_x", current_x)
        return current_x

    def plot(self, name):
        optimum = self.process[-1]
        y = [math.log(f - optimum) for f in self.process[:-1]]
        plt.figure(figsize=(10, 6))
        plt.plot(y, color="gray", linestyle='--', marker='+')
        plt.xlabel("number of iterations k")
        plt.ylabel("log(f-p*)")
        plt.title("log error v.s. number of iterations")
        plt.savefig(name+".png")

if __name__ == "__main__":
    A = mat4py.loadmat('./A.mat')['A']
    x_0 = mat4py.loadmat('./x_0.mat')['x_0']
    x_0 = np.array([x[0] for x in x_0])
    obj_func = obj_func(A)
    solver = solve(obj_func)
    solver.search(initial=x_0)
    solver.plot(name="p1")