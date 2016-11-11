from matplotlib import pyplot as plt
from matplotlib import style
import csv
import datetime
import os




def drawGraph(moidList, counter):
    plt.close()
    #siteParse.parseAll()
    #statParse.pullStat(stat)
    #var = ''
    time_format = '%I:%M'
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    #rel_path = "tempWorkingDirectory"
    #abs_file_path = os.path.join(script_dir, rel_path)
    #fullfilen = abs_file_path + '/counter.csv', 'r'
    filename = 'counter2.csv'
    def getColumn(filename, column):
        f = open(filename, 'r')
        results = csv.reader(f, delimiter=",")
        #f.close()
        #results = csv.reader(open(filename), delimiter=",")
        try:
            list = [result[column] for result in results]
            f.close()
            return list
            #return [result[column] for result in results]
        except:
            print('Its dead Jim')
            #print( [result[column] for result in results])
    f = open(filename, 'r')
    results = csv.reader(f, delimiter=",")



    def convert_time(list):
        output = []
        for x in list:
            pretime = (datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
            output.append(pretime)
        return output



    #Get time information and then convert it for Matplotlib
    #print(getColumn(filename, 0))
    time = getColumn(filename, 0)
    ctime = convert_time(time)

    #print(ctime)
    #print(time)
    #print(stat)
    style.use('fivethirtyeight')
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = 8
    plt.rcParams["figure.figsize"]= fig_size
    #plt.figure("Time/")
    plt.xlabel("Time")
    plt.ylabel("Counter value")


    #print(len(next(results)))

    for i in range(len(next(results))):
        #Pass on first column because it is timestamp
        if i == 0:
            pass
        #Plot a line for each column with counter values
        else:
            h = i - 1
            if h < 0:
                h=0
            try:
                labelList = moidList[h].split(',')

            except:
                labelList = moidList[h]

            try:
                label = labelList[-1]

            except:
                label = labelList[0]
            plt.plot(ctime, getColumn(filename, i), label=label)
            plt.legend(fontsize='10', loc='upper center', bbox_to_anchor=(0.5, 1.08), ncol=2, fancybox=True, shadow=True)



    #plt.plot(ctime, getColumn(filename, 1))
    plt.xticks(rotation=30)
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.15)
    plt.suptitle(counter)
    #Showing what we plotted
    zzz = open(filename, 'r')
    zzz.close()
    f.close()

    #plt.legend
    plt.subplots_adjust(left=0.05, bottom=0.17, right=0.99, top=0.90, wspace=0.2, hspace=0.2)
    plt.show()
#drawGraph()

