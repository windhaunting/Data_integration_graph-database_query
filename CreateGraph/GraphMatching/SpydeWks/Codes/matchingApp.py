# -*- coding: utf-8 -*-

import time

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *

sys.path.insert(0, 'common')                  #common folder at the same directory as this file

from preprocess import preprocess
from readDatabaseFile import readDatabaseFile

from mainEntry import dataMatching

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("Database Matching App")
        self.master.geometry('700x700-0+2')
        
        # constant variable
        self.inputFile = "Databases Folder : "
         
        #input variable
        self.inputDBdirPath = "/home/fubao/Fubao/CiscoWish/data/test"                 #Input database file name
        self.rdThreshold = 1.5            #StringVar() to double
        self.bucketNum = 20000
        self.outNumDir = "/home/fubao/Fubao/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/numericalOutput"                     #output numerical database directory, default value
        self.prefixLength = 2            
        self.sampleRecordNums = 4000
        self.recordPrSimiThreshold = 0.5
        self.OutputNonNumDir = "/home/fubao/Fubao/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/nonNumericalOutput"        
        
        
        #execute function
        self.createInputDataDiaglog(master)
        self.finalOperate(master)
        
       
    def createInputDataDiaglog(self, master):
        #self.entrythingy = Entry()
        #self.entrythingy.pack()
        
        #input DB frame
        frmInput = LabelFrame(master, text = "Input DB", padx=10, pady=10)
        #frmInput.pack(side=TOP, expand=Yes, padx=1, pady=2,)
        frmInput.grid(row=0, column=0, columnspan=12, sticky=W)
        
        #input database entry
        labInDir = Label(frmInput, text =self.inputFile)
        labInDir.grid(row=0, column=0, rowspan=1, padx=5, pady=5, sticky=W)        
        self.EntryInDB = Entry(frmInput, width = 50)
        self.EntryInDB.insert(0, self.inputDBdirPath)
        self.EntryInDB.grid(row=0, column=1, padx=5, pady=5)              
        btnOpen = Button(frmInput, text="Open", command=self.openInputFolder)
        btnOpen.grid(row=0, column=2, padx=5, pady=5, sticky=W)
        
        #input numerical paramter frame
        frmInPara = LabelFrame(master, text = "Input Numerical Parameters", padx=10, pady=10)
        frmInPara.grid(row=1, column=0, columnspan=12, sticky=W)
        
        #threshold entry
        labRdTh = Label(frmInPara, text ="Range difference threshold:")
        labRdTh.grid(row=1, column=0, rowspan=1, padx=5, pady=5, sticky=W)
        self.EntryInRdThr = Entry(frmInPara, width = 10)
        self.EntryInRdThr.insert(0, self.rdThreshold)
        self.EntryInRdThr.grid(row=1, column=1, padx=5, pady=5, sticky=W)          
        
        #bucket nums entry
        labBucketNum = Label(frmInPara, text ="Bucket num for bucket dot product:")        
        labBucketNum.grid(row=2, column=0, rowspan=1, padx=5, pady=5, sticky=W)
        self.EntryInBucketNum = Entry(frmInPara, width = 10)
        self.EntryInBucketNum.insert(0, self.bucketNum)
        self.EntryInBucketNum.grid(row=2, column=1, padx=5, pady=5, sticky=W)       
        
        #numerical file path output
        labOutDir = Label(frmInPara, text = "Numerical output directory:")
        labOutDir.grid(row=3, column=0, rowspan=1, padx=5, pady=5, sticky=W)        
        self.EntryNumOut = Entry(frmInPara, width = 50)
        self.EntryNumOut.insert(0, self.outNumDir)
        self.EntryNumOut.grid(row=3, column=1, padx=5, pady=5)              
        btnOpen = Button(frmInPara, text="Open", command=self.openOutNumFolder)
        btnOpen.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        
        
        #non-numerical output parameters below
        frmNonNumPara = LabelFrame(master, text = "Input Non-numerical Parameters", padx=10, pady=10)
        frmNonNumPara.grid(row=2, column=0, columnspan=12, sticky=W)
        
        #threshold entry
        labPrefixLen = Label(frmNonNumPara, text ="Prefix length:")
        labPrefixLen.grid(row=0, column=0,  rowspan=1, padx=5, pady=5, sticky=W)
        self.EntryPrefixLen = Entry(frmNonNumPara, width = 10)
        self.EntryPrefixLen.insert(0, self.prefixLength)
        self.EntryPrefixLen.grid(row=0, column=1, padx=5, pady=5, sticky=W)  
        
        labSampleNum= Label(frmNonNumPara, text ="Sample record nums:")
        labSampleNum.grid(row=1, column=0,  rowspan=1, padx=5, pady=5, sticky=W)
        self.EntrySampleNum = Entry(frmNonNumPara, width = 10)
        self.EntrySampleNum.insert(0, self.sampleRecordNums)
        self.EntrySampleNum.grid(row=1, column=1, padx=5, pady=5, sticky=W)  
    
        
        labRecSimiThr= Label(frmNonNumPara, text ="Record pair similarity threshold:")
        labRecSimiThr.grid(row=2, column=0,  rowspan=1, padx=5, pady=5, sticky=W)
        self.EntryRecSimiThr = Entry(frmNonNumPara, width = 10)
        self.EntryRecSimiThr.insert(0, self.recordPrSimiThreshold)
        self.EntryRecSimiThr.grid(row=2, column=1, padx=5, pady=5, sticky=W)  
    
         #non-numerical file path output
        labNonNumOutDir = Label(frmNonNumPara, text = "Non-numerical output directory:")
        labNonNumOutDir.grid(row=3, column=0, rowspan=1, padx=5, pady=5, sticky=W)        
        self.EntryNonNumOut = Entry(frmNonNumPara, width = 50)
        self.EntryNonNumOut.insert(0, self.OutputNonNumDir)
        self.EntryNonNumOut.grid(row=3, column=1, padx=5, pady=5)              
        btnOpen = Button(frmNonNumPara, text="Open", command=self.openOutNonNumFolder)
        btnOpen.grid(row=3, column=2, padx=5, pady=5, sticky=W)
        
        frmOptional = Frame(master, padx=100, pady=50)
        frmOptional.grid(row=3, column=0)
        self.varInter = IntVar()
        ckbtnInter = Checkbutton(frmOptional, text="Generate intermediate result files", variable=self.varInter)
        ckbtnInter.pack(side=LEFT, padx=55, pady=5)
        
       # self.varProfile = IntVar()
       # ckbtnProfile = Checkbutton(frmOptional, text="Profile running statistics", variable=self.varProfile)
       # ckbtnProfile.pack(side=LEFT, padx=55, pady=5)

    #final operate, execute or exit     
    def finalOperate(self, master):
        
        frmFinal = Frame(master,  padx=100, pady=50)
        frmFinal.grid(row=4, column=0)

        btnExit = Button(frmFinal, text="Exit", command=master.destroy)
        btnExit.pack(side=RIGHT, padx=55, pady=5)
        okButton = Button(frmFinal, text="Execute", command=self.executeCodes)
        okButton.pack(side=RIGHT)
        
    #open numerical input database folder
    def openInputFolder(self):
        print("hi open!")
       # filepath = askopenfilename(initialdir="/home/fubao",filetypes =(("Text File", "*"),("All Files","*.*")), title = "Choose a file.")
        inputDBdirPath = askdirectory()
        if inputDBdirPath:
            self.EntryInDB.delete(0, END)
            self.EntryInDB.insert(0, inputDBdirPath)
            self.inputDBdirPath = self.EntryInDB.get()           
            print(inputDBdirPath)

            if not os.path.exists(self.inputDBdirPath):  # folder not exists
                showwarning("No folder Exists", "Please select database folder.")
         

    #open numerical output folder
    def openOutNumFolder(self):
        outputNumericalDir = askdirectory()
        if outputNumericalDir:
            self.EntryNumOut.delete(0, END)
            self.EntryNumOut.insert(0, outputNumericalDir)
            self.outputNumericalDir = self.EntryNumOut.get()           
            print(outputNumericalDir)

            if not os.path.exists(self.outputNumericalDir):  # folder not exists
                showwarning("No folder Exists", "Please select numerical output folder.")
                
    #open non-numerical output folder               
    def openOutNonNumFolder(self):
        outputNonNumericalDir = askdirectory()
        if outputNonNumericalDir:
            self.EntryNonNumOut.delete(0, END)
            self.EntryNonNumOut.insert(0, outputNonNumericalDir)
            self.outputNonNumericalDir = self.EntryNonNumOut.get()           
            print(outputNonNumericalDir)

            if not os.path.exists(self.outputNonNumericalDir):  # folder not exists
                showwarning("No folder Exists", "Please select non-numerical output folder.")
                
    def executeCodes(self):
        
        #read all input paramters              
        if "" == self.EntryInDB.get() or not os.path.exists(self.EntryInDB.get()):    # folder not exists 
            showwarning("No folder Exists", "Please select effective database folder.")
            return
        else:
            self.inputDBdirPath = self.EntryInDB.get()

        preproc = preprocess()
        if "" == self.EntryInRdThr.get() or not preproc.is_number(self.EntryInRdThr.get()):
            showwarning("No RD Exists", "Please input range diffrence score threshold [0, 2]")
            return
        elif float(self.EntryInRdThr.get()) > 2 or float(self.EntryInRdThr.get()) < 0:
            showwarning("No RD Exists", "Please input effective range diffrence score threshold [0, 2]")
            return
        else:
            self.rdThreshold = self.EntryInRdThr.get();

        if "" == self.EntryInBucketNum.get() or not preproc.is_number(self.EntryInBucketNum.get()):
            showwarning("No bucket number Exists", "Please input bucket number for bucket dot product")
            return
        else:
            self.bucketNum = self.EntryInBucketNum.get();
            
        #numerical output
        if "" == self.EntryNumOut.get() or not os.path.exists(self.EntryNumOut.get()):    # folder not exists 
            showwarning("No folder Exists", "Please select effective numerical output directory.")
            return
        else:
            self.outNumDir = self.EntryNumOut.get()
            
        if "" == self.EntryPrefixLen.get() or not preproc.is_number(self.EntryPrefixLen.get()):
            showwarning("No prefix Exists", "Please input prefix length [1, 3]")
            return
        elif float(self.EntryPrefixLen.get()) > 2 or float(self.EntryPrefixLen.get()) < 0:
            showwarning("No prefix Exists", "Please input effective prefix length [1, 3]")
            return
        else:
            self.prefixLength = self.EntryPrefixLen.get();

        if "" == self.EntrySampleNum.get() or not preproc.is_number(self.EntrySampleNum.get()):
            showwarning("No sample number Exists", "Please input sample record number for iterative pair processing")
            return
        else:
            self.sampleRecordNums = self.EntrySampleNum.get();
            
        if "" == self.EntryRecSimiThr.get() or not preproc.is_number(self.EntryRecSimiThr.get()):
            showwarning("No prefix Exists", "Please input record pair similarity threshold [0, 1]")
            return
        elif float(self.EntryRecSimiThr.get()) > 1 or float(self.EntryRecSimiThr.get()) < 0:
            showwarning("No record simi threshold Exists", "Please input effective record pair similarity threshold [0, 1]")
            return
        else:
            self.recordPrSimiThreshold = self.EntryRecSimiThr.get();


         #non-numerical output
        if "" == self.EntryNonNumOut.get() or not os.path.exists(self.EntryNonNumOut.get()):    # folder not exists 
            showwarning("No folder Exists", "Please select effective numerical output directory.")
            return
        else:
            self.OutputNonNumDir = self.EntryNonNumOut.get()           

        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists('output/numericalOutput'):
            os.makedirs('output/numericalOutput')
        if not os.path.exists('output/nonNumericalOutput'):
            os.makedirs('output/nonNumericalOutput')
        if not os.path.exists('intermediateOutput'):
            os.makedirs('intermediateOutput')
        if not os.path.exists('intermediateOutput/numericalInterOutput'):
            os.makedirs('intermediateOutput/numericalInterOutput')
        if not os.path.exists('intermediateOutput/nonNumericalInterOutput'):
            os.makedirs('intermediateOutput/nonNumericalInterOutput')
        
        print("Welcome!")
        
        #if (self.varInter == 0):
        print ('varInter ', bool(self.varInter.get()), 'self.varProfile', self.varProfile.get())
        
        startTime = time.time()

        
        dataMtObj = dataMatching()
        rdDbFileObj = readDatabaseFile() 
        numericalColumnSmallRange = 200
        nonNumericalColumnSmallRange = 200                        #according to database range distribution, maybe change or not by different database, here temporarily hard code 200
        interMediateFileFlag = bool(self.varInter.get())         # generate intermediate files, checkbox later
#        profileStatisticsFlag = bool(self.varProfile.get())      #profile statistics or not
        inputDataFolderPath = self.inputDBdirPath + '/'
        inputRDThd = float(self.rdThreshold)
        inputBucketNum = int(self.bucketNum)
        outputNumerical = self.outNumDir + '/' + 'allNumericalFinalResult.tsv'
        threadNum = 8

        dataMtObj.readTsvDatabase(inputDataFolderPath, nonNumericalColumnSmallRange, interMediateFileFlag)
        # print ('len rdDbFileObj.tbFieldAllNumericalValuesMap ', len(rdDbFileObj.tbFieldAllNumericalValuesMap))

        #numerical matching processing
        dataMtObj.numericalMatching(threadNum, numericalColumnSmallRange, inputRDThd, inputBucketNum, rdDbFileObj.primaryKeysSet, rdDbFileObj.tbFieldAllNumericalValuesMap, interMediateFileFlag, outputNumerical)

        #non-numerical matching processing
        
        
        prefixLength = int(self.prefixLength)
        sampleRecordsNum = int(self.sampleRecordNums)
        recordPrSimiThreshold = float(self.recordPrSimiThreshold)
        finalNonNumericalOutputDir = self.OutputNonNumDir + '/'
        outFileNonNumericalRatioScoreAll = finalNonNumericalOutputDir + "nonNumericalFinalMatchingRatio.tsv"
    
        print ('tbFieldAllNonNumericalValuesMap len ', len(rdDbFileObj.tbFieldAllNonNumericalValuesMap.keys()))
        dataMtObj.nonNumericalMatching(rdDbFileObj.tbFieldAllNonNumericalValuesMap, threadNum, prefixLength, sampleRecordsNum, recordPrSimiThreshold, finalNonNumericalOutputDir, outFileNonNumericalRatioScoreAll)

        endTime = time.time()
        print("Congratulations! Finished")
        print ('Total runtime: ', endTime-startTime)
        

root = Tk()
app = Application(master=root)
app.mainloop()
