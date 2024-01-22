from tkinter import *

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

# # read input.csv
# print('read input.csv')
# try:
#     input_path = '.\\input.csv'
#     input_value = csv(input_path)
# except:
#     print('Make sure input.csv is in the same folder.')
#     # pause, it would be better to use os.system("pause") here.
#     input()
#     polygon_path = '.\\polygon.csv'
#     polygon_value = csv(polygon_path)

plot_value=[]
for i in range(len(polygon_value)):
    plot_value.append(polygon_value[i][0]*100+500)
    plot_value.append(polygon_value[i][1]*100+500)


#画图

tk=Tk()

scrolly_y=tk.Scrollbar(tk)
scrolly_y.pack(side=RIGHT,fill=Y)

scrolly_x=tk.Scrollbar(tk)
scrolly_x.pack(side=END,fill=X)

w=Canvas(tk,width=3000,height=3000,background='white',xscrollcommand=scrolly_x.set,yscrollcommand=scrolly_y.set)
w.pack()



w.create_polygon(plot_value,fill='lightgray')


