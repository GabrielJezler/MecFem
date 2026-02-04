import numpy as np

class Solution():
    def __init__(self, X, t, C, E, Fi, Fb, Qm):
        self.xNodes = X[:, 0]
        self.yNodes = X[:, 1]
        self.zNodes = X[:, 2]
        self.t = t
        self.C = C
        self.E = E
        self.Fi = Fi
        self.Fb = Fb
        self.Qm = Qm

    def getX(self):
        return np.hstack((self.xNodes[:, np.newaxis], self.yNodes[:, np.newaxis], self.zNodes[:, np.newaxis]))
