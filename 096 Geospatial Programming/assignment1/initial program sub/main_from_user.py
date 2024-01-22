from plotter import Plotter
from main_from_file import MBR, RCA, Point

###########################################################
# read csv file, and save as list


def csv(path):
    with open(path, 'r') as f:
        f_value = list()

        for n in f.readlines()[1:]:
            row = n.strip("\n").split(',')
            point = Point(int(row[0]), float(row[1]), float(row[2]))
            f_value.append(point.get_point())

###########################################################
# main function


def main():
    ###########################################################
    # read data
    ###########################################################
    # read polygon.csv as list
    print('read polygon.csv')
    try:
        polygon_path = '.\\polygon.csv'
        polygon_value = csv(polygon_path)
    except:
        print('Make sure pologon.csv is in the same folder.')
        # pause, it would be better to use os.system("pause") here.
        input()
        polygon_path = '.\\polygon.csv'
        polygon_value = csv(polygon_path)

    # insert point
    print('\nInsert point information')

    # allow user put multiple points
    a = 1
    input_value = []
    while a == 1:
        try:
            x = float(input('x coordinate: '))
            y = float(input('y coordinate: '))
        except:
            print('Data error, please re-enter.')
            print('If you want to stop typing, press Enter.')
            try:
                x = float(input('x coordinate: '))
                y = float(input('y coordinate: '))
            except:
                break

        input_value.append([x, y])

    #########################################################
    # categorize points
    #########################################################
    print('\ncategorize points')

    # Get categorize result.
    rca_judge = RCA()
    mbr_judge = MBR()

    result_point = dict()

    # The point out MBR, result is outside.
    for i in range(len(input_value)):
        if mbr_judge.mbr_result(polygon_value, input_value[i]):
            result_point[i+1] = 'outside'
        # The point in MBR, RCA judgment, return the result.
        else:
            result_point[i +
                         1] = rca_judge.line_judge(polygon_value, input_value[i])

        print("point", i+1, " is ", result_point[i+1], ' the polygon')

    ###########################################################
    # plot
    ###########################################################
    print('\nplot polygon and points')
    plotter = Plotter()

    # plot polygon
    polygon_x, polygon_y = mbr_judge.get_x_y(polygon_value)
    plotter.add_polygon(polygon_x, polygon_y)

    # plot points
    for i in range(len(input_value)):
        # plot ray for point inside MBR and not 'boundary'
        if mbr_judge.mbr_result(polygon_value, input_value[i]) == False:
            x_max = max(polygon_x)
            plotter.add_ray(
                input_value[i][0], input_value[i][1], x_max, result_point[i+1])

        plotter.add_point(input_value[i][0],
                          input_value[i][1], result_point[i+1], i+1)

    plotter.show()


###########################################################
###########################################################
if __name__ == '__main__':
    main()
