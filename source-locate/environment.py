import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


# template for 2D environment containing (width, height) and pollution data for each cell. As well as debugging render.
# Contains fnx set_pollution (allowing pollution level to be stored to a cell)
# Contains fnx get_pollution (allowing pollution level to be indexed by cell)
class Environment:
    # status
    CLEAN = 0
    # POLLUTED = between 0-1
    SOURCE = 1

    def __init__(self, width, height, depth, goal):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
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

    def set_do2(self, x, y, z, do2_level):
        self.dissolved_o2_data[x][y][z] = do2_level

    def get_pollution(self, x, y, z):
        # print(x, y, z)
        return self.pollution_data[x][y][z]

    def get_do2(self, x, y, z):
        return self.dissolved_o2_data[x][y][z]

    def render_pollution_grid(self):
        # ax is a global

        x = np.arange(0, self.width)
        y = np.arange(0, self.height)
        z = np.arange(0, self.depth)

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        self.fig.colorbar(cm.ScalarMappable(cmap=cm.viridis), ax=self.ax)

        min_pollution = self.pollution_data.min()
        max_pollution = self.pollution_data.max()

        normalize = cm.colors.Normalize(vmin=min_pollution, vmax=max_pollution)
        scalar_map = cm.ScalarMappable(norm=normalize, cmap=cm.viridis)

        for zpoint in z:
            for ypoint in y:
                for xpoint in x:
                    size = self.pollution_data[xpoint][ypoint][zpoint]  # s=size
                    pollution = self.pollution_data[xpoint, ypoint, zpoint]
                    self.ax.scatter3D(xpoint, ypoint, zpoint, s=size*20, color=scalar_map.to_rgba(pollution))  # c=self.pollution_data[xpoint,ypoint,zpoint], marker='*')
                    # fig.colorbar(scalarMap, ax=ax)
                    # todo:
                    # for an xyz color this point between [0 1] based on the normalzied self.pollution_data
        plt.pause(0.01)

    # visualizes agent in space in the Run window.
    def render_agent(self, agent, old=False, pause=0.5):
        size, color = (5, 'black') if old else (20, 'red')

        # self.ax.clear()
        self.ax.scatter3D(agent.x, agent.y, agent.z, s=size)
        if pause > 0:
            plt.pause(pause)

        # ax.cla()
        # color_map1 = plt.get_cmap('YlGnBu')
        # color_map2 = plt.get_cmap('RdBu')

        # x = np.arange(0, self.width)
        # # #x = x.flatten()
        # y = np.arange(0, self.height)
        # # #y = y.flatten()
        # z = np.arange(0, self.depth)
        # z = self.pollution_data[:, 2]
        # #z = z.flatten()
        # X, Y = np.meshgrid(x, y)
        # print(x)
        # print(y)
        # ax.plot_surface(X, Y, z, cmap=cm.viridis,
        #                    linewidth=0, antialiased=False)

        # ax.matshow(self.dissolved_o2_data, cmap=color_map2, alpha=0.0)
        # ax.set_box_aspect((agent.x), (agent.y), (agent.z))
