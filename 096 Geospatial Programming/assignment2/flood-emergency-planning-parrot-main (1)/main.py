import Task1 as tk1
import Task2 as tk2
import Task3 as tk3
import Task4 as tk4
import Task5 as tk5


def main():
    # 0. defines files
    print('Make sure the Material folder is in the same folder as the program, enter any character to run')
    input()

    wd = ".\\Material\\Material"
    itn_file = wd + "\\itn\\solent_itn.json"
    elevation_file = wd + "\\elevation\\SZ.asc"
    isle_file = wd+"\\shape\\isle_of_wight.shp"
    background_file = wd+"\\background\\raster-50k_2724246.tif"

    # 1. requests a user location input, and returns a user point: [x,y], Point(x,y)
    pib_result, user, user_point = tk1.input_point()
    print('1. user point entered')

    # 2.1 returns a buffer polygon within 5km of the user location
    ele_boundary = tk2.ele_boundary()
    buffer = ele_boundary.buffer_clip(user_point, isle_file)
    print('2.1 elevation buffer created')

    # 2.2 returns a list of highest point within the buffer: [[x, y],...] and return a array of clipped elevation
    highest_point_list, ele_clip = tk2.get_highest_point(
        buffer, elevation_file)
    highest_point = highest_point_list[0]
    print("2.2 highest point returned")

    # 3. returns the nearest node to the user and the highest point: (x, y)
    nearest_user, nearest_hp, if_samepoint, user_nearest_list, hp_nearest_list = tk3.itn(
        user, highest_point, itn_file)
    print("3. nearest node(s) returned")

    print("These are the nearest road nodes to the user position: ", user_nearest_list)
    print("These are the nearest road nodes to the highest point: ", hp_nearest_list)
    if len(user_nearest_list) > 1:
        try:
            user_index = int(
                input("Please enter the list index of the nearest user node: "))
            nearest_user = user_nearest_list[user_index-1]
        except:
            user_index = int(
                input("Please enter the 'list index' of the nearest user node: "))
            nearest_user = user_nearest_list[user_index-1]

    if len(hp_nearest_list) > 1:
        try:
            hp_index = int(
                input("Please enter the list index of the nearest highest node: "))
            nearest_hp = hp_nearest_list[hp_index-1]
        except:
            hp_index = int(
                input("Please enter the 'list index' of the nearest highest node: "))
            nearest_hp = hp_nearest_list[hp_index-1]

    # 4. returns the shortest path between the nearest node to the user and the the highest point
    try:
        sp = tk4.shortest_path(itn_file, elevation_file,
                               buffer, nearest_user, nearest_hp, ele_clip)
        print("4. shortest path returned: ", sp)

    except:
        print("No path connecting the user position and the highest point")
        size = float(input("Please enter a new buffer size (>5000): "))
        new_buffer = user_point.buffer(size)
        new_ele = tk2.elevation()
        new_ele_clip = new_ele.read_elevation(new_buffer, elevation_file)
        print("4.1 elevation for new buffer")

        # 4.2 returns the shortest path between the nearest node to the user and the the highest point
        sp = tk4.shortest_path(itn_file, elevation_file,
                               new_buffer, nearest_user, nearest_hp, new_ele_clip)
        print("4.2 new shortest path returned: ", sp)

    # 5. plotting
    tk5.plotting(sp, user[0], user[1], background_file, elevation_file, ele_clip,
                 user_point, highest_point_list[0], nearest_user, nearest_hp)
    print("5. plotting finished")


if __name__ == '__main__':
    main()
