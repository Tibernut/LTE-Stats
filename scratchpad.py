import xml.etree.ElementTree as etree
import os
import glob
import datetime
import re
pathread = open('path.txt')
pathlist = pathread.readlines()
path = pathlist[2]
fileList = glob.glob(os.path.join(path, '*'))
print(fileList)
counter = 'VS.ENBProcOverloadStatusChg.OverloadChgMinor'
outlist = []
def parseStat(fileList, counter):
    '''
    Will get file list and counter value from GUI/CLI
    Then returns csv file for Matplotlib (in LTE_Stat_Plot)
    CAUTION change the path information in this function if using on Linux
    YOU SHOULD COMMENT OUT os.remove(f) and replace with print(f) before running
    the first time to ensure nothing unintentional is deleted!!!!
    '''

    exceptcounter = 0
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "\\"
    abs_file_path = os.path.join(script_dir)



    csvwrite = open(abs_file_path + '\counter.csv', 'w')
    for filename in fileList:
        friendFile = os.path.split(filename)[1]
        fileYear = int(friendFile[1:5])
        fileMonth = int(friendFile[5:7])
        fileDay = int(friendFile[7:9])
        fileResplit = re.split('\.|\+', friendFile)
        fileHour = int(fileResplit[1][0:2])
        fileMinute = int(fileResplit[1][2:4])
        #Since we had to pull files marked requestedtime + 5H to deal with Sam's file marking offset
        #We need to subtract 5 hours from the time/date pulled from file to draw graph correctly.
        fileDateTime = datetime.datetime(fileYear, fileMonth, fileDay, fileHour, fileMinute) - datetime.timedelta(hours=5)


        #Nested loop time whooOO
        try:
            xmldoc = etree.parse(filename)
            root = xmldoc.getroot()
            main = root[1]
            valList = []
            moidList = []

            #Each block of counters is contained in an <mi></mi> group.
            #Find all of them and loop through them
            all_mi = main.findall('mi')

            #Build list of mt(counter names) and mv (counter value blocks)
            for c in all_mi:
                all_mt = c.findall('mt')
                all_mv = c.findall('mv')
                incr = 0
                for x in all_mt:
                    incr += 1

                    #If we've hit the counter we are looking for capture the value of our incrementor.  We will use this
                    #To select the correct <r> from the <mv> block
                    if x.text == counter:
                        keyval = incr
                        for y in all_mv:
                            valincr = 0
                            all_r = y.findall('r')

                            #Since we know we are in the right <mv> grab the <moid> to use for the graph's legend
                            for yy in y:
                                if yy.tag == 'moid':
                                    if yy.tag in moidList:
                                        pass
                                    else:
                                        moidList.append(yy.text)
                            #If we find that our value incrementer and our counter incrementer match we have found
                            #the counter value.
                            for z in all_r:
                                valincr += 1
                                if valincr == keyval:
                                    #print(keyval)
                                    valList.append(z.text)

        except:
            valList = []
            exceptcounter += 1

        #validate valList:
        if len(valList)>0:
            csvwrite.write(str(fileDateTime))
            outlist.append(fileDateTime)
            for zz in valList:
                outlist.append(str(zz))
                csvwrite.write(',' + str(zz))
            csvwrite.write('\n')
    print(outlist)

    print('Exceptions: {}'.format(exceptcounter))
    csvwrite.close()
    #Now I must look through the csv file and remove any entry of 'None'
    #For some reason some enodeBs do not report stats on certain sectors. in XML entry is <r></r>
    correctread = open('counter.csv', 'r')
    csv2write = open('counter2.csv', 'w')
    for line in correctread:
        #print(line.split(','))
        lines = line.split(',')
        newline = []
        for cell in lines:
            if cell == 'None':
                print(cell)
                newline.append('0')
            elif cell == 'None\n':
                newline.append('0\n')
            else:
                #print('good')
                newline.append(cell)
        correctline = ','.join(newline)
        print('Old: {}'.format(lines))
        print('New: {}'.format(newline))
        csv2write.write(correctline)
    csv2write.close()
parseStat(fileList, counter)
'''
def parseStatasdfasf2(fileList, counter):

Will get file list and counter value from GUI/CLI
Then returns csv file for Matplotlib (in LTE_Stat_Plot)
CAUTION change the path information in this function if using on Linux
YOU SHOULD COMMENT OUT os.remove(f) and replace with print(f) before running
the first time to ensure nothing unintentional is deleted!!!!


exceptcounter = 0
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "\\"
abs_file_path = os.path.join(script_dir)



#csvwrite = open(abs_file_path + '\counter.csv', 'w')
for filename in fileList:
    friendFile = os.path.split(filename)[1]
    fileYear = int(friendFile[1:5])
    fileMonth = int(friendFile[5:7])
    fileDay = int(friendFile[7:9])
    fileResplit = re.split('\.|\+', friendFile)
    fileHour = int(fileResplit[1][0:2])
    fileMinute = int(fileResplit[1][2:4])
    #Since we had to pull files marked requestedtime + 5H to deal with Sam's file marking offset
    #We need to subtract 5 hours from the time/date pulled from file to draw graph correctly.
    fileDateTime = datetime.datetime(fileYear, fileMonth, fileDay, fileHour, fileMinute) - datetime.timedelta(hours=5)


    #Nested loop time whooOO
    try:
        xmldoc = etree.parse(filename)
        root = xmldoc.getroot()
        main = root[1]
        valList = []
        moidList = []
        #print(main.tag)
        md = main.getchildren()
        for element in md:
            if element.tag == 'mi':
                mi = element.getchildren()
                print(mi)
                for x in mi:
                    #print(x)
                    if x.text == counter:
                        xindex = mi.index(x)
                        eindex = md.index(element)
                        print('{} is the {}th child of the {}th element'.format(x.text, xindex, eindex))
                    if x.tag == 'mv':
                        print(x.tag + 'aaah')

        #for elements in mi:
        #    #if elements.tag == 'mv':
        #    subel = elements.getchildren()
        #    print(subel)



    except Exception as err:
        print('RUHOH ' + filename)
        print(err)


        #print(element.tag)
'''


#parseStat(fileList, counter)

