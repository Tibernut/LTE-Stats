
import os
import glob
import datetime
import re
import file_manip


#SAMPLE INPUTS GO HERE
startDateTime = datetime.datetime(2016, 10, 28, 1, 0)
endDateTime = datetime.datetime(2016, 10, 29, 8, 0)
tNode = "100009_WCW_Main"

#Read path from path.txt.  This makes moving the program from computer to computer easier
pathread = open('path.txt')
pathlist = pathread.readlines()
pathread.close()
path = pathlist[1][:-1]






def getSiteList():
    '''
    Globs through \RawData\ and looks for eNodeB folders
    When found adds all unique eNodeBs to list
    Then returns sorted list to be used to build drop down
    :return:
    '''
    siteList = []
    rawSitesList = glob.glob(path + '\\*\*\*')

    for folder in rawSitesList:
        site = os.path.split(folder)[1]
        if site in siteList:
            pass
        else:
            siteList.append(site)
    sortSiteList = sorted(siteList)
    return sortSiteList[3:]




def availableDates():
    '''
    Globs through folders in RawData and adds all available dates to a list
    Can be used to populate GUI / CLI info
    :return:
    '''
    dateList = []
    rawDateList = glob.glob(path + '\\*')


    #Build list of dates that occur within start time and end time
    #This is to be used in the file path
    for dates in rawDateList:
        dateF = os.path.split(dates)[1]
        fileYear = int(dateF[0:4])
        fileMonth = int(dateF[4:6])
        fileDay = int(dateF[6:8])
        dateObj = datetime.date(fileYear, fileMonth, fileDay) - datetime.timedelta(hours=9)
        dateList.append(dateObj)
    return sorted(dateList)





def identifyFiles(folderName, startDateTime, endDateTime):
    '''
    Takes folderName (eNodeB), start date and time, and end date and time
    Returns list of files that match
    :return:
    '''
    #first delete all pcm files.  Not sure what these are for and I haven't built anything to make use/handle them
    file_manip.pmcDelete(folderName)
    dateList = []
    reducedFilesList = []
    filesList = []
    rawDateList = glob.glob(path + '\\*')


    #Build list of dates that occur within start time and end time.  Get these from the filename itself
    #This is to be used in the file path
    for dates in rawDateList:
        dateF = os.path.split(dates)[1]
        fileYear = int(dateF[0:4])
        fileMonth = int(dateF[4:6])
        fileDay = int(dateF[6:8])
        fileDate = datetime.date(fileYear, fileMonth, fileDay)
        if startDateTime.date() <= fileDate <= endDateTime.date():
            if dateF in dateList:
                pass
            else:
                dateList.append(dateF)


    #Build list of all files that occur with matched DATE and eNodeB NAME
    for x in dateList:
        tempReducedFileList = glob.glob(os.path.join(path, x, 'enodeB', folderName, '*'))
        reducedFilesList = reducedFilesList + tempReducedFileList


    #Check every file in the previously built list and check if it matches the time (HH:MM) specifications
    #If so, add to new list
    for y in reducedFilesList:
        fileName = os.path.split(y)[1]
        fileYear = int(fileName[1:5])
        fileMonth = int(fileName[5:7])
        fileDay = int(fileName[7:9])
        fileResplit = re.split('\.|\+', fileName)
        fileHour = int(fileResplit[1][0:2])
        fileMinute = int(fileResplit[1][2:4])
        fileDateTime = datetime.datetime(fileYear, fileMonth, fileDay, fileHour, fileMinute)
        # print(fileDateTime)
        if startDateTime <= fileDateTime < endDateTime:
            filesList.append(y)
            #print(fileName)
    return(filesList)


