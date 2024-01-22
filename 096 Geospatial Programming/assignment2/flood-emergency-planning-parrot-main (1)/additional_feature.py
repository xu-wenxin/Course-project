import Task2 as tk2
import Task3 as tk3
import Task4 as tk4
import Task5 as tk5

import matplotlib.pyplot as plt
from shapely.geometry import Point
import numpy as np
import rasterio


def add_elevation(ax, ele_plot, sz_file, max_ele):
    # Get the suitable elevation (above and below 20m of the highest point)
    ele_plot[ele_plot < max_ele-20] = np.nan
    m = np.ma.masked_where(np.isnan(ele_plot), ele_plot)

    # extent_ele
    ele_f = rasterio.open(sz_file, "r")
    bound_ele = ele_f.bounds
    extent_ele = [bound_ele.left, bound_ele.right,
                  bound_ele.bottom, bound_ele.top]

    # plot elevation
    plt.imshow(m, interpolation='nearest',
               extent=extent_ele, cmap='Reds')
    plt.title('Click any area that shows an elevation(place with color)',
              fontsize=7, fontweight='bold')

    # Add a color bar for elevation
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=6)

    # ticks show
    plt.xticks(fontsize=4)
    plt.yticks(fontsize=4)

    print('plot elevation')


def main():
    wd = ".\\Material\\Material"
    background_file = wd+"\\Material\\background\\raster-50k_2724246.tif"
    itn_file = wd+"\\Material\\itn\\solent_itn.json"
    elevation_file = wd+"\\Material\\elevation\\SZ.asc"
    isle_file = wd+"\\Material\\shape\\isle_of_wight.shp"
    plot = tk5.Plotter()

    # 1.1 Click to retrieve the coordinate (x,y)
    fig, ax = plot.add_background(background_file)
    user = plt.ginput(1)[0]
    plt.close('all')
    print('get user point: ', user)
    # 1.2 Convert coordinates to Point(x,y)
    x = user[0]
    y = user[1]
    user_point = Point(x, y)

    # 2. Get the destination point
    # 2.1 Get the highest point
    ele_boundary = tk2.ele_boundary()
    ele_read = tk2.elevation()
    buffer = ele_boundary.buffer_clip(user_point, isle_file)
    ele_clip = ele_read.read_elevation(buffer, elevation_file)

    print("highest point returned")

    # 2.2 Click to get the destination point from the suitable elevation range
    max_ele = np.amax(ele_clip)
    fig, ax = plot.add_background(background_file)
    add_elevation(ax, ele_clip, elevation_file, max_ele)
    plot.add_point(x, y)
    plt.xlim(left=x-5000, right=x+5000)
    plt.ylim(bottom=y-5000, top=y+5000)
    pt_ele = plt.ginput(1)[0]
    plt.close('all')
    print('choose point: ', pt_ele)

    # 3. returns the nearest node to the user and the highest point: (x, y)
    nearest_user, nearest_hp, if_samepoint, user_nearest_list, hp_nearest_list = tk3.itn(
        user, pt_ele, itn_file)
    print("nearest node(s) returned")

    # 4. returns the shortest path between the nearest node to the user and the the highest point
    try:
        sp = tk4.shortest_path(itn_file, elevation_file,
                               buffer, nearest_user, nearest_hp, ele_clip)
        print("4. shortest path returned: ", sp)

    except:
        print("No path connecting the user position and the highest point")
        size = float(input("Please enter a new buffer size (>5km): "))
        new_buffer = user_point.buffer(size)
        new_ele = tk2.elevation()
        new_ele_clip = new_ele.read_elevation(new_buffer, elevation_file)
        print("4.1 elevation for new buffer")

        # 4.2 returns the shortest path between the nearest node to the user and the the highest point
        sp = tk4.shortest_path(itn_file, elevation_file,
                               new_buffer, nearest_user, nearest_hp, new_ele_clip)
        print("4.2 new shortest path returned: ", sp)

    # 5.plotting
    # add background
    fig, ax = plot.add_background(background_file)
    # add elevation
    plot.add_elevation(ele_clip, elevation_file)
    # add buffer
    plot.add_buffer(user_point)
    # add the shortest path
    xs = list(map(lambda x: x[0], sp))
    ys = list(map(lambda x: x[1], sp))
    plot.add_line(xs, ys)
    print("shortest path has been added")
    # add user position, highest point, and their nearest nodes
    plot.add_point(x, y)
    plot.add_user_node(nearest_user[0], nearest_user[1])
    plot.add_distance_point(pt_ele[0], pt_ele[1])
    plot.add_distance_node(nearest_hp[0], nearest_hp[1])
    plot.show(ax, x, y)


if __name__ == '__main__':
    main()
