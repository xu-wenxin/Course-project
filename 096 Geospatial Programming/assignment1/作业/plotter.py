from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt

# if plotting does not work comment the following line
matplotlib.use('TkAgg')


class Plotter:

    def __init__(self):
        plt.figure()

    def add_polygon(self, xs, ys):
        plt.fill(xs, ys, 'lightgray', label='Polygon')

    def add_point(self, x, y, kind=None, name=None):
        plt.text(x, y+0.1, name)
        if kind == 'outside':
            plt.plot(x, y, 'ro', label='Outside')
        elif kind == 'boundary':
            plt.plot(x, y, 'bo', label='Boundary')
        elif kind == 'inside':
            plt.plot(x, y, 'go', label='Inside')
        else:
            plt.plot(x, y, 'ko', label='Unclassified')

    def add_ray(self, x, y, x_max, kind=None):
        try:
            if kind == 'outside':
                plt.plot([x, x_max+0.5], [y, y], 'r')
                plt.quiver(x_max+0.5, y, 1, 0, color='r')
            elif kind == 'inside':
                plt.plot([x, x_max+0.5], [y, y], 'g')
                plt.quiver(x_max+0.5, y, 1, 0, color='g')
        except:
            pass


    def show(self):
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()
