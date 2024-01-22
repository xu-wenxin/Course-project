from main_from_file import MBR, RCA
import matplotlib.pyplot as plt

##########################################################
# additional feature
##########################################################
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
# main function
###########################################################


def main():
    # read data
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
    # additional, plot figure
    figure = Figure()

    x = ['outside', 'inside', 'boundary']
    out, ins, bou = figure.count(input_value, result_point)
    y = [out, ins, bou]
    figure.show_bar(x, y)
    figure.show_pie(x, y)

###########################################################
###########################################################


if __name__ == '__main__':
    main()
