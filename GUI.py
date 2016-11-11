import tkinter
from tkinter import ttk
import fileListBuilder
import datetime
import LTE_stat_XMLparse
import LTE_stat_Plot
import file_manip
import glob
import atexit




#on Program exit delete contents of working directory
def exit_handler():
    #create empty list and pass to cleanup function
    emptyList = []
    file_manip.cleanupData(emptyList)


#Main function that calls other functions into action.
def main():
    stat = counter.get()
    enodeb = sitevar.get()
    startd = startDateVar.get()
    endDate = endDateVar.get()
    starth = datetime.time(int(startHourVar.get()))
    lasth =  datetime.time(int(lastHourVar.get()))
    #Sam's timestamps on the files are 5 hours ahead so I must offset here to grab the correct files
    #in LTE_stat_XMLparse.py I also correct the timestamp within the file so graph draws properly
    adjuststartdatetime = datetime.datetime.combine(datetime.datetime.strptime(startd, '%Y-%m-%d'), starth) + datetime.timedelta(hours=5)
    adjustenddatetime = datetime.datetime.combine(datetime.datetime.strptime(endDate, '%Y-%m-%d'), lasth) + datetime.timedelta(hours=5)
    print("I will collect the counter {0} from the site {1} between {2} on {3} and {4} on {5}.".format(stat, enodeb,
                                                                                                       starth, startd,
                                                                                                       lasth, endDate))

    #Perform sanity checks and let 'er rip
    if adjuststartdatetime <= adjustenddatetime:

        #Identify the files needed based on start/end time and eNodeB
        preList = fileListBuilder.identifyFiles(enodeb, adjuststartdatetime, adjustenddatetime)

        #send fileslist to cleanup, this will delete all files in directory that aren't needed
        #It ensures only the contents of your last query are in the working directory
        file_manip.cleanupData(preList)

        #Send list to unzip which will unzip all files in list not already in working directory
        file_manip.unzipList(preList)

        #Create list of files in working directory and send that list to the XML parse function to decode
        #the XML and pull the required counters.  Function also returns list of moids which we use
        #For the graph's legend
        fileList = []
        for file in glob.glob('C:\\Users\cjones84\PycharmProjects\LTE_Ran_statistics\\tempWorkingDirectory\\*'):
            fileList.append(file)
        moidList = LTE_stat_XMLparse.parseStat(fileList, stat)

        #finally start the graphing function
        LTE_stat_Plot.drawGraph(moidList, stat)

    else:
        print('I can\'t do that dave. (startdatetime >= enddatetime)')


#Build list of counters for display in GUI
with open('counters.txt', 'r') as f:
    counterList = [line.strip() for line in f]

#Build eNodeB List for display in GUI
siteList = fileListBuilder.getSiteList()

#Get available dates for display in GUI
dateList = []
dateObjList = fileListBuilder.availableDates()
for d in dateObjList:
    dateList.append(str(d))

#Generate list of hours
#For some reason tkinter.StringVar really doesn't like it if start and end share the same list
#So we create a list for each
#(Revisit this, I could be wrong)
starthourList=list(range(24))
endhourList=list(range(24))

#
#START GUI
#
window = tkinter.Tk()
window.resizable(0,1)
window.title("LTE RAN Stats")

#define GUI variables
lst1 = counterList
counter = tkinter.StringVar()
counter.set(counterList[0])
sitevar = tkinter.StringVar()
sitevar.set(siteList[0])
startDateVar = tkinter.StringVar()
startDateVar.set(dateList[-1])
endDateVar = tkinter.StringVar()
endDateVar.set(dateList[-1])
startHourVar = tkinter.StringVar()
startHourVar.set(starthourList[0])
lastHourVar = tkinter.StringVar()
lastHourVar.set(endhourList[0])




#Build Labels
sdateLBL = tkinter.Label(window, justify='left', text='Start Date')
edateLBL = tkinter.Label(window, justify='left', text='End Date')
shourLBL = tkinter.Label(window, justify='left', text='Start Hour')
ehourLBL = tkinter.Label(window, justify='left', text='End Hour')
enbLBL = tkinter.Label(window, justify='left', text='Target Site')
counterLBL = tkinter.Label(window, justify='left', text='Counter/KPI')

#Build Comboboxes and Button
drop = ttk.Combobox(window, values=counterList, state='readonly', textvariable= counter, width= 50)
eNodeBs = ttk.Combobox(window, values=siteList, state='readonly', textvariable= sitevar, width= 50)
startDate = ttk.Combobox(window, values=dateList, state='readonly', textvariable= startDateVar, width= 10)
endDate = ttk.Combobox(window, values=dateList, state='readonly', textvariable= endDateVar, width= 10)
lastHour = ttk.Combobox(window, values=endhourList, state='readonly', textvariable= lastHourVar, width= 5)
startHour = ttk.Combobox(window, values=starthourList, state='readonly', textvariable= startHourVar, width= 5)
Accept = tkinter.Button(window, text="Accept", command=lambda: main())


#
#Place objects in Window
#
sdateLBL.grid(row=1, column=1)
edateLBL.grid(row=2, column=1)
shourLBL.grid(row=1, column=3, sticky='e')
ehourLBL.grid(row=2, column=3, sticky='e')
enbLBL.grid(row=3, column=1)
counterLBL.grid(row=4, column=1, sticky='s')
startDate.grid(row=1, column=2, sticky='sw')
startHour.grid(row=1, column=4, sticky='sw')
endDate.grid(row=2, column=2, sticky='sw')
lastHour.grid(row=2, column=4, sticky='sw')
eNodeBs.grid(row=3, column=2, columnspan=3, sticky='se')
drop.grid(row=4, column=2, columnspan=3, sticky='se')
Accept.grid(row=5, column=2, columnspan=3, sticky='nesw')

#call exit handler on program exit to remove files from working directory
atexit.register(exit_handler)
window.mainloop()