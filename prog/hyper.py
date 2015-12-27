import numpy as np
import matplotlib.pyplot as plt

# theta goes from 0 to 2pi
theta = np.linspace(0, 2*np.pi, 1000)

# the radius of the circle
r = 1

# compute x1 and x2
x1 = r*np.cos(theta)
x2 = r*np.sin(theta)

# create the figure
fig, ax = plt.subplots(1)
ax.plot(x1, x2)
ax.set_aspect(1)
plt.show()