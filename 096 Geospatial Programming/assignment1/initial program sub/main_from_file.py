from plotter import Plotter

###########################################################
###########################################################

# class geometry and it subclasses.


class geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y

    def get_point(self):
        self.__point = [self.__x, self.__y]
        return self.__point


class Line(geometry):
    def __init__(self):
        pass

    def lines(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2
        self.line = [point1, point2]
        return self.line


class Polygon(geometry):
    def __init__(self):
        pass

    def polygon_lines(self, m, value):
        polygon_line_point = []
        line = Line()

        # line 1
        if m == 1:
            for i in range(len(value)-1):
                point_1 = value[i]
                point_2 = value[i+1]
                polygon_line_point.append(line.lines(point_1, point_2))
            polygon_line_point.append(line.lines(point_2, value[0]))

        # line 2
        elif m == 2:
            for i in range(len(value)-2):
                point_1 = value[i+1]
                point_2 = value[i+2]
                polygon_line_point.append(line.lines(point_1, point_2))
            polygon_line_point.append(line.lines(point_2, value[0]))
            polygon_line_point.append(line.lines(value[0], value[1]))

        # line 3
        elif m == 3:
            for i in range(len(value)-3):
                point_1 = value[i+2]
                point_2 = value[i+3]
                polygon_line_point.append(line.lines(point_1, point_2))
            polygon_line_point.append(line.lines(point_2, value[0]))
            polygon_line_point.append(line.lines(value[0], value[1]))
            polygon_line_point.append(line.lines(value[1], value[2]))

        else:
            print('error')
            raise

        return polygon_line_point

###########################################################
###########################################################

# Determine if the value is between the two values(with and without boundaries).


class max_min:
    def __init__(self) -> None:
        pass

    # with boundaries
    def judge_boundary(self, n_max, n_min, m):
        if n_min <= m <= n_max:
            return True
        else:
            return False

    # without boundaries
    def judge_location(self, n_max, n_min, m):
        if n_min < m < n_max:
            return True
        else:
            return False


###########################################################
###########################################################

# Determine whether the point is outside the minimum Bounding Rectangle (MBR).
class MBR(max_min):
    def __init__(self) -> None:
        super().__init__()

    def get_x_y(self, value):
        x = []
        y = []
        for i in range(len(value)):
            x.append(value[i][0])
            y.append(value[i][1])
        return x, y

    def mbr_result(self, polygon_value, point):

        polygon_x, polygon_y = self.get_x_y(polygon_value)

        # The range of MBR.
        xmin = min(polygon_x)
        xmax = max(polygon_x)
        ymin = min(polygon_y)
        ymax = max(polygon_y)

        x = point[0]
        y = point[1]

        if self.judge_boundary(xmax, xmin, x) == False:
            return True
        elif self.judge_boundary(ymax, ymin, y) == False:
            return True
        else:
            return False


###########################################################
###########################################################

# Use the ray casting algorithm (RCA) to determine whether the point is in the graph and return the result.
class RCA(max_min):
    def __init__(self) -> None:
        super().__init__()

    # RCA main program.
    def line_judge(self, polygon_value, point):

        count = 0
        result = 'not know'

        x_p = point[0]
        y_p = point[1]

        # Gets the endpoints list of three adjacent line segments.
        polygon = Polygon()

        line_1_list = polygon.polygon_lines(1, polygon_value)
        line_2_list = polygon.polygon_lines(2, polygon_value)
        line_3_list = polygon.polygon_lines(3, polygon_value)

        # Use line 2 to determine the number of times the ray passes through the polygon and the boundary point.
        for i in range(len(polygon_value)):

            y_1_1 = line_1_list[i][0][1]

            x_2_1 = line_2_list[i][0][0]
            y_2_1 = line_2_list[i][0][1]

            x_2_2 = line_2_list[i][1][0]
            y_2_2 = line_2_list[i][1][1]

            y_3_2 = line_3_list[i][1][1]

            # The slope of the line segment (k) is 0.
            if y_2_1 == y_2_2:
                # Continue to judge when the point is on a straight line, otherwise jump to the end of the loop (continue).
                if y_p == y_2_1:
                    x_2_max = max(x_2_2, x_2_1)
                    x_2_min = min(x_2_2, x_2_1)

                    # Return 'boundary' when the point is on the line segment and break out of the loop.
                    if self.judge_boundary(x_2_max, x_2_min, x_p):
                        result = 'boundary'
                        break
                    # Line 1 and line 3 are counted on both sides of the ray, otherwise (line 1 and line 3 are on the same side of the ray) they are not counted.
                    elif self.judge_line(y_p, y_1_1, y_3_2) and x_p < x_2_min:
                        count += 1
                    else:
                        continue

                else:
                    continue

            # k does not exist (infinity).
            elif x_2_1 == x_2_2:
                # Return 'boundary' when the point is on the line segment and break out of the loop.
                if x_p == x_2_1:
                    y_2_max = max(y_2_2, y_2_1)
                    y_2_min = min(y_2_2, y_2_1)
                    if self.judge_boundary(y_2_max, y_2_min, y_p):
                        result = 'boundary'
                        break
                    else:
                        continue

                # If there is ray intersection to the right of point, count.
                else:
                    if self.judge_count(y_1_1, y_2_2, y_2_1, y_p) == True and x_p < x_2_1:
                        count += 1
                    else:
                        continue

            # There is k non-zero.
            else:
                k = (y_2_2-y_2_1)/(x_2_2-x_2_1)
                x_joint = (y_p - y_2_1)*(1/k)+x_2_1

                # Return 'boundary' when the point is on the line segment and break out of the loop.
                if self.on_line(x_joint, x_2_1, x_2_2, x_p):
                    result = 'boundary'
                    break

                # If there is ray intersection to the right of point, count.
                else:
                    if self.judge_count(y_1_1, y_2_2, y_2_1, y_p) == True and x_p < x_joint:
                        count += 1
                    else:
                        continue

        # Determine the position of the point and assign the value
        if result == 'boundary':
            m = 'boundary'
        else:
            if count % 2 == 0:
                m = 'outside'
            elif count % 2 == 1:
                m = 'inside'
            else:
                m = 'not know'

        return m

    ###########################################################

    # Determine whether there is an intersection between point ray and line segment that needs to be counted.
    def judge_count(self, y_1_1, y_2_2, y_2_1, y_p):

        y_2_max = max(y_2_2, y_2_1)
        y_2_min = min(y_2_2, y_2_1)
        y_joint = y_p

        # The ray is in the middle of the line segment, have a intersection, return true.
        if self.judge_location(y_2_max, y_2_min, y_joint):
            return True

        # The ray passes through the end of the line segment to judge the position of the two lines. The same side is not counted(True), the different side is counted(False).
        elif y_joint == y_2_1:
            if self.judge_line(y_joint, y_1_1, y_2_2):
                return True
            else:
                return False

        else:
            return False

    # The ray passes through the end of the line segment to judge the position of the two lines. The same side is not counted(True), the different side is counted(False).
    def judge_line(self, y_joint, y_1_1, y_2_2):
        if y_joint < y_1_1 and y_joint > y_2_2:
            return True
        elif y_joint > y_1_1 and y_joint < y_2_2:
            return True
        else:
            return False

    # Determine whether a point is on a line segment.
    def on_line(self, x, x_2_1, x_2_2, x_p):
        if x == x_p:
            x_max = max(x_2_2, x_2_1)
            x_min = min(x_2_2, x_2_1)
            if self.judge_boundary(x_max, x_min, x):
                return True
            else:
                return False
        else:
            return False


###########################################################
###########################################################


# read csv file, and save as list
# can be save as class
def csv(path):
    with open(path, 'r') as f:
        f_value = list()

        for n in f.readlines()[1:]:
            row = n.strip("\n").split(',')
            point = Point(int(row[0]), float(row[1]), float(row[2]))
            f_value.append(point.get_point())

    f.close()
    return f_value


def output(input_value, result_point):

    with open(".\\output.csv", 'x') as f:
        f.write('id'+','+'category'+'\n')

        for i in range(len(input_value)):
            output_list = []
            # class
            name = int(i+1)
            result = result_point.get(name)
            f.write(str(name)+','+str(result)+'\n')

    f.close()


###########################################################
###########################################################
# main function


def main():
    ###########################################################
    # read data
    ###########################################################

    # read polygon.csv
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

    # read input.csv
    print('read input.csv')
    try:
        input_path = '.\\input.csv'
        input_value = csv(input_path)
    except:
        print('Make sure input.csv is in the same folder.')
        # pause, it would be better to use os.system("pause") here.
        input()
        input_path = '.\\input.csv'
        input_value = csv(input_path)

    #########################################################
    # categorize points
    #########################################################
    print('\ncategorize points')

    # Data classification is initialized to 'not know', dictionary type.
    result_point = dict()
    for i in range(len(input_value)):
        result_point[i+1] = 'not know'

    # Get categorize result.
    for i in range(len(input_value)):

        rca_judge = RCA()
        mbr_judge = MBR()

        # The point out MBR, result is outside.
        if mbr_judge.mbr_result(polygon_value, input_value[i]):
            result_point[i+1] = 'outside'
        # The point in MBR, RCA judgment, return the result.
        else:
            result_point[i +
                         1] = rca_judge.line_judge(polygon_value, input_value[i])

    ###########################################################
    # write output.csv
    ###########################################################
    print('\nwrite output.csv')

    try:
        output(input_value, result_point)

    except:
        print('Check whether output.csv exists in the same folder')
        input()

        output(input_value, result_point)

    ###########################################################
    # plot
    ###########################################################
    print('\nplot polygon and points')
    plotter = Plotter()

    # plot polygon
    polygon_x, polygon_y = mbr_judge.get_x_y(polygon_value)
    plotter.add_polygon(polygon_x, polygon_y)

    # plot point
    for i in range(len(input_value)):
        plotter.add_point(input_value[i][0],
                          input_value[i][1], result_point.get(i+1))

    plotter.show()


###########################################################
###########################################################


if __name__ == '__main__':
    main()
