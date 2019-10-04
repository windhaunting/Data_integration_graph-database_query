#read database data files operations

import csv
from os import listdir
from os.path import isdir,join

import pandas as pd
#import sys
#common_python_dir = sys.path.insert(0, '/home/fubao/workDir/ResearchProjects/CiscoWISH/CreateGraph/IdentifyExistingRelationship/common_python')

import unicodedata
from blist import blist
from preprocess import preprocess
from preprocess import TbfieldValue
from commonReadFile import commonReadFile

# create intermediateOutput automatically in mainEntry
Intermediate_files = ['intermediateOutput/allNumericalColumnTbFieldValues.tsv', 'intermediateOutput/allNonNumericalColumnTbFieldValues.tsv']
#import sys
#csv.field_size_limit(sys.maxsize)

dateFormatNotationSet = set(['time', 'calendar', 'date', 'quarter', 'year', 'month', 'week', 'day', 'hour', 'minutes', 'seconds', 'duration', 'dur'])          #time not times


class readDatabaseFile(object):

    primaryKeysSet = set()                           # storing tb.field primary keys 
    tbFieldAllNumericalValuesMap = {}               #all numerical tbfield: values
    tbFieldAllNonNumericalValuesMap = {}            # all non-numerical tbfield: values except small range and time-format columns
    tbFieldNonNumericalTimeFormatType = set()       # non-numerical time-format fields to filter
    
    def __init__(self):
        self.tablesNameList = blist([])               # all tables names

       # self.tbFieldAllNumericalValuesMap = {}               #all numerical tbfield: values
       # self.tbFieldAllNonNumericalValuesMap = {}            # all non-numerical tbfield: values
        #self.tbfieldsAllNumerical = blist([])              
       # self.primaryKeysSet = set()                           # storing tb.field primary keys 
    # get all table's name from directory
    def getTableNames(self, inputDataDir):                   # get the name of all the tables
        self.tablesNameList = sorted([str(dirt).strip().lower() for dirt in listdir(inputDataDir) if isdir(join(inputDataDir,dirt))])  #sort the result list, lowercase table name

    # get one table's field
    def getFields(self, inputDataDir, tableName):
        fileName = inputDataDir + tableName.upper()+ '/000000_1'
        #print fileName
        with open(fileName, 'rt', encoding='utf8') as tsvin:
            tsvin = csv.reader(tsvin, delimiter = '\t')
            preproc = preprocess()
            for row in tsvin:
                rowFields = preproc.word_strip_lower(row)            #strip and lowercase
               # for field in row:
               #     FieldOutList.append(str(tableName) + '.' + str(field))
              #  print type(tsvin), row
                break                         #the first line is the field
        return rowFields
        
    # read one table field and value
    def readOneTable(self, inputDataDir, tableName):
        fileNameValue = inputDataDir + tableName.upper() + '/000000_0'     #get value
        df = pd.read_csv(fileNameValue, sep = '\t',header = None, index_col = None, error_bad_lines=False,  warn_bad_lines=False)

        fieldsRead= self.getFields(inputDataDir, tableName)   #add column title to the table read
        fieldNameList =  list(fieldsRead)
        df.columns = fieldsRead

        columnList = blist([])
        for field in fieldNameList:
            tbValObj = TbfieldValue(tableName, field, df[field])
            columnList.append(tbValObj)
        #print ('fieldNameList', fieldNameList)
        return columnList

    #read all tables data to split into numerical field values and non-numerical fields and output the intermediate result to file(not necessary) and memory
   # @staticmethod    
    def getAllTablesDividedPrimary(self, inputDataDir, nonNumericalColumnSmallRange, InterMediateFileFlag):
        preproc = preprocess()
        comRdFileObj = commonReadFile()
        
        if (InterMediateFileFlag):              #have intermediate file or not
            comRdFileObj.clearFileContent(Intermediate_files[0])
            comRdFileObj.clearFileContent(Intermediate_files[1])  
        self.getTableNames(inputDataDir)
        for tbName in self.tablesNameList:
            print ('database table name: ', tbName)
            dataList = self.readOneTable(inputDataDir, tbName)
            
            typeFileOut = inputDataDir + tbName.upper() + '/desc_accurate.txt'    #column data type and primary key file
            strWrtRow = 'col_name' + '\t' + 'data_type' + '\t' + 'comment' + '\t' + '\n'
            comRdFileObj.writeStrRowToFileAppend(typeFileOut, strWrtRow)
            #[row, fieldOutList] = self.getFields(tbName)
            
            # get time-format type table.fields
            tbFieldNonNumericalTimeFormatType = self.getNonNumericalFieldsTimeFormatType(inputDataDir, tbName)
            
            for data in dataList:
                
                #remove date format column,   not matching requirement
                splitNameSet = set(data.fieldA.split('_'))
                if (dateFormatNotationSet & splitNameSet):
                    continue
                                       
                newcolNumericalList = blist([])
                newcolNonNumericalList = blist([])
                setVals = set(data.value.unique().flatten())
                colValSet = preproc.filterNullValueAndLowercaseSet(setVals)          #set, unique value considered
                                    #remove time format and small range
                if data.fieldA in tbFieldNonNumericalTimeFormatType or len(setVals) <= nonNumericalColumnSmallRange:
                        continue
                    
                if preproc.judgeListAllNumbers(colValSet):    
                    #judge the primary key and write into files           
                    if ((len(setVals) == len(data.value)) and len(setVals) != 0):
                    #write into database individual directory files about field type and primary keys
                        strWrtRow = data.fieldA + '\t' + 'numerical' + '\t' + 'primaryKey' + '\t' + '\n'
                        self.primaryKeysSet.add(data.tableA + '.' + data.fieldA)            #store primary keys, generally for numerical only
                    else:
                        strWrtRow = data.fieldA + '\t' + 'numerical' + '\t' + 'otherKey' + '\t' + '\n'
                    comRdFileObj.writeStrRowToFileAppend(typeFileOut, strWrtRow)
                    
                    #store numerical keys
                    strHead = data.tableA + '.' + data.fieldA
                    #newcolNumericalList.append(strHead)
                    for val in colValSet:
                        if preproc.is_number(val):
                            fval = float(val)
                            if fval >= 0:                                      #need to consider positive for matching
                                newcolNumericalList.append(int(fval))
                    self.tbFieldAllNumericalValuesMap[strHead] = newcolNumericalList
                    if (InterMediateFileFlag): 
                        comRdFileObj.writeListRowToFileTsv(Intermediate_files[0], [strHead] + newcolNumericalList)           #write to numerical file
                else:                                                #elif preproc.judgeListAllNonNumerical(set(colValList)):   
                                        
                    #judge the primary key and write into files
                    if ((len(setVals) == len(data.value)) and len(setVals) != 0):
                    #write into database individual directory files about field type and primary keys
                        strWrtRow = data.fieldA + '\t' + 'non-numerical' + '\t' + 'primaryKey' + '\t' + '\n'
                    else:
                        strWrtRow = data.fieldA + '\t' + 'non-numerical' + '\t' + 'otherKey' + '\t' + '\n'
                    comRdFileObj.writeStrRowToFileAppend(typeFileOut, strWrtRow)

                    #store non-numerical keys
                    strHead = data.tableA + '.' + data.fieldA
                    #newcolNonNumericalList.append(strHead)
                    newcolNonNumericalList += blist(colValSet)
                    self.tbFieldAllNonNumericalValuesMap[strHead] = newcolNonNumericalList
                    if (InterMediateFileFlag): 
                        comRdFileObj.writeListRowToFileTsv(Intermediate_files[1], [strHead] + newcolNonNumericalList)          # write to non-numerical file

    #get non numerical time format type
    def getNonNumericalFieldsTimeFormatType(self, inputDataDir, tableName):
        fileName = inputDataDir + tableName.upper()+ '/desc.txt'
        #print fileName
        tbFieldNonNumericalTimeFormatType = set()
        with open(fileName, 'rt', encoding='utf8') as tsvin:
            tsvin = csv.reader(tsvin, delimiter = '\t')
            preproc = preprocess()
            for row in tsvin:
                row = preproc.word_strip_lower(row)            #strip and lowercase

                if row[1] == 'timestamp':                    #non-numerical time format
                    tbFieldNonNumericalTimeFormatType.add(row[0])
                   # rowStr = tableName + '.' + row[0] + ',' + 'nonNum-time' + ','+ '\n'
                   # commFileOperObj.writeListRowToFileAppendWriter(fd, rowStr)
        return tbFieldNonNumericalTimeFormatType
    
    #get numerical field pairs， first line is neglected
    def getGTNumericalFields(self, gtNumericalFile):
        gtNumericalFieldsPairLst = []
        
        with open(gtNumericalFile, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter=',')
            i = 0
            for row in tsvin:
                if i == 0:
                    i += 1
                    continue
                f1 = row[0].lower().strip()
                f2 = row[1].lower().strip()
                if (f1, f2) not in gtNumericalFieldsPairLst:
                    gtNumericalFieldsPairLst.append((f1,f2))
        return gtNumericalFieldsPairLst
        
    #write numerical ground truth field and write into file for later read directly from file, not from the whole databases
    #gtNumericalFieldsPairLst format: ()
    def numericalFieldValuesWriteFile(self, gtNumericalFieldsPairLst, tbFieldAllNumericalValuesMap, outFile):
        gtNumericalFieldValsMap = {}
        comRdFileObj = commonReadFile()
        with open(outFile, "a") as fd:
            for pair in gtNumericalFieldsPairLst:
                tblfd1 = pair[0]
                tblfd2 = pair[1]
                if tblfd1 in tbFieldAllNumericalValuesMap:           #add hashmap value
                    if tblfd1 not in gtNumericalFieldValsMap:
                        gtNumericalFieldValsMap[tblfd1] = tbFieldAllNumericalValuesMap[tblfd1]
                        listRow = [tblfd1]  + gtNumericalFieldValsMap[tblfd1]
                        comRdFileObj.writeListRowToFileWriterTsv(fd, listRow)
                
                if tblfd2 in tbFieldAllNumericalValuesMap:
                    if tblfd2 not in gtNumericalFieldValsMap:
                        gtNumericalFieldValsMap[tblfd2] = tbFieldAllNumericalValuesMap[tblfd2]
                        listRow = [tblfd2]  + gtNumericalFieldValsMap[tblfd2]
                        comRdFileObj.writeListRowToFileWriterTsv(fd, listRow)
                    
        #return gtNumericalFieldValsMap
                
        
                
                
                
            