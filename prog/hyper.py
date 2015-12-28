import numpy as np
import matplotlib.pyplot as plt


class PoincareDisk:

    def __init__(self):
        fig, ax = plt.subplots(1)
        ax.set_aspect(1)
        self.axis = ax
        self.figure = fig

    def plot(self, shape):
        shape.plot(self)
        plt.show()

    def mkBoundary(self):
        return Boundary()

    def mkPoint(self, x, y):
        pass

    def mkLine(self, x1, y1, x2, y2):
        pass

    def distanceBetween(self, x1, y1, x2, y2):
        pass

class Boundary:

    def __init__(self):
        self.t = np.linspace(0, 2 * np.pi, 1000)
        self.x = np.cos(self.t)
        self.y = np.sin(self.t)

    def plot(self, pd):
        pd.axis.plot(self.x, self.y)


class Point:

    def __init__(self):
        pass


class Line:

    def __init__(self):
        pass