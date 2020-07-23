from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pylab as plt

fig3d = plt.figure(figsize=(10, 10), constrained_layout=True)
ax3d = fig3d.add_subplot(111, projection='3d')

x = np.arange(10)
y = np.arange(10)
z = np.arange(10)


alphas = np.linspace(0.1, 1, 10)
rgba_colors = np.zeros((10,4))
# for red the first column needs to be one
rgba_colors[:,0] = 1.0
# the fourth column needs to be your alphas
rgba_colors[:, 3] = alphas

print(rgba_colors.shape)

ax3d.scatter(x, y, z, color=rgba_colors)
plt.show()
