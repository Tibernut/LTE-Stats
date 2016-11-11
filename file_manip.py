import gzip
import glob
import os
import csv
source_dir = "C:\\Users\cjones84\PycharmProjects\LTE_Ran_statistics\dumps\server2"
dest_dir = source_dir
pathread = open('path.txt')
pathlist = pathread.readlines()
pathread.close()
path = pathlist[1][:-1]
wpath = pathlist[2]


def pmcDelete(folderName):
    tempReducedFileList = glob.glob(os.path.join(path, '*', 'eNodeB', folderName, 'pmcResult*'))
    for f in tempReducedFileList:
        os.remove(f)


def unzipList(list):
    #We want to see if file is already present in working directory
    outList=[]
    keepList=[]
    for src_name in glob.glob(os.path.join(wpath, '*')):
        keepList.append(src_name)
    for src_name in list:
        base = os.path.basename(src_name)
        dest_name = os.path.join(wpath, base[:-3])
        if dest_name in keepList:
            pass
        else:
            try:
                with gzip.open(src_name, 'rb') as infile:
                    with open(dest_name, 'wb') as outfile:
                        for line in infile:
                            outList.append(line)
                            outfile.write(line)
            except:
                pass
    return(outList)



def cleanupData(list):
    pList = []
    for l in list:
        pList.append(os.path.basename(l[:-3]))
    keepList = []
    #build list of non .gz files
    removeList = []

    for src_name in glob.glob(os.path.join(wpath, '*')):
        if src_name.find(wpath) != -1:
            if src_name[-2:] == 'gz':
                pass
            else:
                removeList.append(src_name)
        else:
            print('nooope')
            pass
    #Delete files
    for x in removeList:
        if os.path.basename(x) in pList:
            keepList.append(os.path.basename(x))
        else:
            os.remove(x)
