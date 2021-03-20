import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')


# template for 2D environment containing (width, height) and pollution data for each cell. As well as debugging render.
# Contains fnx set_pollution (allowing pollution level to be stored to a cell)
# Contains fnx get_pollution (allowing pollution level to be indexed by cell)
class Environment:
    # status
    CLEAN = 0
    # POLLUTED = between 0-1
    SOURCE = 1

    def __init__(self, width, height, depth, goal):
        self.width = width
        self.height = height
        self.depth = depth
        self.goal = goal
        self.pollution_data = np.zeros((width, height, depth))
        self.dissolved_o2_data = np.zeros((width, height, depth))
        # print(self.pollution_data)
        # print(len(self.pollution_data[0]))
        # print(len(self.pollution_data[0][0]))

    def is_goal(self, x, y, z):
        return x == self.goal[0] and y == self.goal[1] and z == self.goal[2]

    def set_pollution(self, x, y, z, pollution_level):
        self.pollution_data[x][y][z] = pollution_level
        # print(self.pollution_data)
        # print(len(self.pollution_data[0]))
        # print(len(self.pollution_data[0][0]))

    def set_do2(self, x, y, z,  do2_level):
        self.dissolved_o2_data[x][y][z] = do2_level

    def get_pollution(self, x, y, z):
        print(x, y, z)
        return self.pollution_data[x][y][z]

    def get_do2(self, x, y, z):
        return self.dissolved_o2_data[x][y][z]

    def render_console(self, agent, symbolic=True):
        for y in range(self.height):
            print()
            for x in range(self.width):
                if agent.is_at(x, y, z):
                    if symbolic:
                        print('@', end='')
                    else:
                        print('   @   ', end='')
                    continue

                pollution = self.get_pollution(x, y, z)
                print(pollution)

                if symbolic:
                    if pollution == 0:
                        print('.', end='')
                    elif pollution < 0.25:
                        print('-', end='')
                    elif pollution < 0.5:
                        print('~', end='')
                    elif pollution < 0.75:
                        print('*', end='')
                    elif pollution < 1:
                        print('s', end='')
                    else:
                        print('0', end='')
                else:
                    print('%.4f ' % pollution, end='')

        print("")
        time.sleep(0.001)

    # visualizes agent in space in the Run window.
    def render_plt(self, agent):
        ax.cla()
        color_map1 = plt.get_cmap('YlGnBu')
        color_map2 = plt.get_cmap('RdBu')
        '''
        x = self.pollution_data[:,,]
        y = self.pollution_data[,:,]
        z = self.pollution_data[,,:]
        X, Y, Z = np.meshgrid(x, y, z, indexing = 'ij')
        ax.plot_surface(X, Y, Z, cmap=cm.viridis,
                           linewidth=0, antialiased=False)
        '''
        #ax.matshow(self.dissolved_o2_data, cmap=color_map2, alpha=0.0)
        #ax.set_box_aspect((agent.x), (agent.y), (agent.z))
        ax.scatter3D(agent.x, agent.y, agent.z)
        plt.pause(0.00001)
