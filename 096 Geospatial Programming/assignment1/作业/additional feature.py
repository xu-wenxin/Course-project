from main_from_file import MBR, RCA
# additional feature 1
# import turtle
# additional feature 2
import matplotlib.pyplot as plt

###########################################################
# additional feature
###########################################################
# draw plot in another way


# class tur():
#     def __init__(self) -> None:
#         pass

#     def show_polygon(self, polygon_value):
#         turtle.screensize(800, 600)
#         turtle.penup()
#         turtle.pencolor('gray')
#         turtle.fillcolor('lightgray')
#         turtle.begin_fill()
#         turtle.goto(polygon_value[0][0]*50-150, polygon_value[0][1]*50-150)
#         turtle.pendown()
#         for i in range(len(polygon_value)):
#             turtle.goto(polygon_value[i][0]*50-150, polygon_value[i][1]*50-150)
#         turtle.end_fill()

#         turtle.mainloop()

#     def show_point(self, x, y, result):
#         turtle.penup()
#         if result == 'outside':
#             turtle.pencolor('red')
#         elif result == 'inside':
#             turtle.pencolor('gree')
#         else:
#             turtle.pencolor('blue')

#         turtle.goto(x*50-150, y*50-150)
#         turtle.pendown()
#         turtle.dot(10)

#         turtle.mainloop()


# bar graph and pie graph, adivice use in main_from_file.
class Figure():
    def __init__(self) -> None:
        pass

    def count(self, input_value, result_point):
        out = 0
        ins = 0
        bou = 0
        for i in range(len(input_value)):
            if result_point[i+1] == 'outside':
                out += 1
            elif result_point[i+1] == 'inside':
                ins += 1
            elif result_point[i+1] == 'boundary':
                bou += 1
        return out, ins, bou

    def show_bar(self, x, y):
        plt.bar(x=x, height=y, color=["salmon", 'lightgreen', 'skyblue'])

        for i in range(len(y)):
            plt.text(x=x[i], y=y[i]+2.5, s=str(y[i]), ha='center', va='top')

        plt.title("Statistical histogram of results")
        plt.xlabel("location", fontsize=15)
        plt.ylabel("quantity", fontsize=15)
        plt.show()

    def show_pie(self, x, y):
        plt.pie(x=y, labels=x, autopct='%1.2f%%', colors=[
                "salmon", 'lightgreen', 'skyblue'])
        plt.title('A scale diagram of result')
        plt.show()

###########################################################

# read csv file, and save as list


def csv(path):
    with open(path, 'r') as f:
        f_value = list()
        for n in f.readlines()[1:]:
            row = n.strip("\n").split(',')
            f_value.append([float(row[1]), float(row[2])])

    f.close()
    return f_value

###########################################################
###########################################################
# main function


def main():
    ###########################################################
    # read data
    ###########################################################
    # read polygon.csv as list

    polygon_path = '.\\polygon.csv'
    polygon_value = csv(polygon_path)
    print('read polygon.csv')

    input_path = '.\\input.csv'
    input_value = csv(input_path)
    print('read polygon.csv')

    #########################################################
    # categorize points
    #########################################################

    # Get categorize result.
    print('categorize points')

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
    # additional feature
    ###########################################################
    # plot

    ###########################################################

    # count feature
    figure = Figure()

    x = ['outside', 'inside', 'boundary']
    out, ins, bou = figure.count(input_value, result_point)
    y = [out, ins, bou]
    figure.show_bar(x, y)
    figure.show_pie(x, y)

    # # draw turtle
    # tu = tur()
    # tu.show_polygon(polygon_value)
    # for i in range(len(input_value)):
    #     tu.show_point(input_value[i][0], input_value[i]
    #                   [1], result_point.get(i+1))


###########################################################
###########################################################


if __name__ == '__main__':
    main()
