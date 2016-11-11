import csv
from collections import defaultdict
def transcell():
    with open('/home/chris/scripts/Python/PingCSV/3Gtrans.csv', mode='r') as infile:
        reader = csv.reader(infile)
        #mydict = defaultdict(str, '')
        mydict = {rows[0]:rows[1] for rows in reader}
        #mydict.setdefault(str, 'None')
        #print(mydict)
    return mydict

input = open('/home/chris/docs/3Glatency.txt',)
output = open('/home/chris/docs/3Glatencydaily.txt', 'w')
output2 = open('/home/chris/docs/3Gtotal.csv', 'a')
output3 = open('/home/chris/docs/3Glatency.csv', 'w')
stringhold = []
plosshold = []
namehold = []
mytrans = transcell()
for x in input:
    #print(x)
    if x == '\n':
        if len(stringhold) == 7:
            print(stringhold)
            time = stringhold[3]
            date = [stringhold[1], stringhold[2], stringhold[5]]
            ip_add = stringhold[6]
            if ip_add in mytrans:
                temptrans = mytrans[str(ip_add)]
            else:
                temptrans = ''
            ploss = str(100)
            date = " ".join(date)
            namehold.extend([temptrans])
            plosshold.extend([ploss])
            rowlist = [date, time, temptrans, ip_add, ploss]
            trow = (",".join(rowlist) + '\n')
            output3.write(trow)
            output.write(date + ' ' + time + '\n'
                         + temptrans + ' ' + ip_add + '\n'
                         + 'Packet Loss: ' + ploss + '%\n\n')
            stringhold = []


        elif len(stringhold) == 22:
            #print('22')
            time = stringhold[3]
            date = [stringhold[1], stringhold[2], stringhold[5]]
            ip_add = stringhold[6]
            #print('this is right before error' + str(stringhold[6]))
            if ip_add in mytrans:
                temptrans = mytrans[str(ip_add)]
            else:
                temptrans = ''
            received = stringhold[10]
            ploss = stringhold[12]
            ploss = ploss.split('%')
            ploss = ploss[0]
            date = " ".join(date)
            tlist = stringhold[20]
            tlist = tlist.split("/")
            pmin = tlist[0]
            pmax = tlist[2]
            pavg = tlist[1]
            pdev = tlist[3]
            namehold.extend([temptrans])
            plosshold.extend([ploss])
            rowlist = [date, time, temptrans, ip_add, ploss, pmin, pmax, pavg, pdev, received]
            trow = (",".join(rowlist) + '\n')
            output3.write(trow)
            output.write(date + ' ' + time + '\n'
                         + temptrans + ' ' + ip_add + '\n'
                         + 'Packet Loss: ' + ploss + '%\n'
                         + 'min: ' + pmin + ' max: ' + pmax + '\n'
                         + 'avg: ' + pavg + ' dev: ' + pdev + '\n\n')
            stringhold = []
        #print(stringhold)
        #print(len(stringhold))
        stringhold = []
    else:

        #print('found newline*******************************')
        y = x.split()
        stringhold.extend(y)
output.close()
#Only use if generating new file instead of appending
#output2.write('date,' + ','.join(namehold) + '\n')
output2.write(date + ',' + ','.join(plosshold) + '\n')
output2.close()
output3.close()
