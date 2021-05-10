
import csv
import sys
import pandas as pd
from blist import blist
import linecache
import os
from numpy import genfromtxt, savetxt
from six.moves import filterfalse, zip_longest        #python2 and 3 OK
from preprocess import preprocess
from preprocess import fieldPairSim
csv.field_size_limit(sys.maxsize)


class commonReadFile(object):

    def __init__(self):
        self.ExamplesColumnValueMap = {}             # non_numerical column values


    #clear file content
    def clearFileContent(self, fileName):
        f = open(fileName, "w")                    # clear file content
        f.truncate()
        f.close()

    # write Row of List to File
    def writeListRowToFileTsv(self, outFile, listRow):
        with open(outFile, "a") as f:
            writer = csv.writer(f, delimiter = '\t', lineterminator='\n')
            writer.writerows([listRow])
 
    # write Row of List to File
    def writeListRowToFileWriterTsv(self, fd, listRow):
     #   with open(outFile, "a") as fd
        writer = csv.writer(fd, delimiter = '\t', lineterminator='\n')
        writer.writerows([listRow])

    #append row string to file
    def writeStrRowToFileAppend(self, outFile, rowStr):
        fd = open(outFile,'a')
        fd.write(rowStr)
        fd.close()
        
    #append row  string to file
    def writeStrRowToFileAppendWriter(self, fd, rowStr):
        #fd = open(outFile,'a')
        fd.write(rowStr)
       # fd.close()

    #read sample data (rows store format)
    def readSamplesTsvFile(self, sampleExamplesValsFile):
        with open(sampleExamplesValsFile, 'r') as csvfile:
            tsvin = csv.reader(csvfile, delimiter='\t')
            preproc = preprocess()
            for row in tsvin:
                # negelect header
                row = preproc.word_strip_lower(row)            # strip and lowercase
                self.ExamplesColumnValueMap[row[0]] = row[1:]

    #read two columns as every string into a list
    def readTwoColumnTsvFileToList(self, inputFile):
        twoColumnLst = []
        for line in open(inputFile):
            row = line.split('\t')
            tbfield1 = row[0].strip().lower()           # strip and lowercase
            tbfield2 = row[1].strip().lower()           # strip and lowercase
            key = tbfield1 + '-' + tbfield2
            twoColumnLst.append(key)
        return twoColumnLst


    #save similarity score matrix result into the tsv file
    def writeNpArrayToFile(self, out_file, npArray, headerList):
        self.clearFileContent(out_file)               #clear file
        names = [_ for _ in headerList]
        df = pd.DataFrame(npArray, index=names, columns=names)
        df.to_csv(out_file, index=True, header=True, sep='\t')

    #write lists by columns into Tsv
    def writeListsColumnsToFileAppendWriterTsv(self, fd, rowsLst):
        #rowsLst.append(lst)
        writer = csv.writer(fd, delimiter = '\t', lineterminator='\n')
        rows = zip_longest(*rowsLst)
        for row in rows:
            writer.writerow(row)

    #write lists by columns into csv
    def writeListsColumnsToFileAppendWriterCsv(self, fd, rowsLst):
        #rowsLst.append(lst)
        writer = csv.writer(fd, delimiter = ',', lineterminator='\n')
        rows = zip_longest(*rowsLst)
        for row in rows:
            writer.writerow(row)

    #only one clumn read as a list
    def getOneColumn(self, InputFile):
        df = pd.read_csv(InputFile, sep = ',',header = 0, index_col = 0, error_bad_lines=False,  warn_bad_lines=False)
        print ('length ', len(blist(df.index)))
        return blist(df.index)

    #read two column, first column is key, the second column is value    
    def readFileTwoColumnIntoMapTsv(self, inputFile):
        twoColumnMap = {}
        with open(inputFile, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter='\t',quoting=csv.QUOTE_NONE)
            preproc = preprocess()
            for row in tsvin:
                # negelect header
                row = preproc.filterNullValueAndLowercaseLst(row)            # strip and lowercase
                #print ('row[0]', row[0])
                twoColumnMap[row[0]]= row[1]
        return twoColumnMap

    #read three column, first and second column combined is the key, the third column is value    
    def readFileThreeColumnIntoMapTsv(self, InputFile):
        threeColumnMap = {}
        with open(InputFile, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter='\t',quoting=csv.QUOTE_NONE)
            for row in tsvin:
                # negelect header
               #row = preproc.filterNullValueAndLowercaseLst(row)            # strip and lowercase
                k1 = row[0].strip().lower()           # strip and lowercase
                k2 = row[1].strip().lower()           # strip and lowercase
                key = k1 + '-' + k2
                threeColumnMap[key]= row[2]
        return threeColumnMap

        
    #read two column, first column is key, the extra columns as value
    def readFileTbFieldValueIntoMapTsv(self, inputFile):
        twoColumnMap = {}
        with open(inputFile, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter='\t',quoting=csv.QUOTE_NONE)
            for row in tsvin:
                # negelect header
               # print('len(rowrrrrrrrrrrrrrrrrrrrr ', len(row), row[1:], type(row[1:]))
                key = row[0].strip().lower()
                twoColumnMap[key]= row[1::]
        return twoColumnMap
        

    #write two column, first column is key, the extra columns as value
    def writeFileTbFieldValueIntoMapTsv(self, twoColumnMapValues, outFile):
        
        with open(outFile, mode='w') as twoColumn_file:
            twoColumn_writer = csv.writer(twoColumn_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar='\\')
            
            for k,v in twoColumnMapValues.items():
                twoColumn_writer.writerow([k] + v)
        
    
    #get non-numerical fields index for linecache.getline(inputFile, lineNum) in the future
    def getIndexofTbFieldsNonNumericalCsv(self, inputFile):
        IndexTbFieldMap = {}
        lineNum = 1
        for line in open(inputFile):
            row = line.split(',')
            tbfield = row[0].strip().lower()           # strip and lowercase
            IndexTbFieldMap[tbfield]= lineNum
            lineNum = lineNum + 1;
        return IndexTbFieldMap

    # read lines from files
    def readLine(self, inputFile, lineNum):
        line = linecache.getline(inputFile, lineNum)
        return line

    def transposeRowToColumns(self, inputFile, outFile):
        data = genfromtxt(inputFile)
        savetxt(outFile,data.T)

    '''
    #get two field value which is stored by column
    def getNonNumericalTwoPossibleGroundTruthFieldValues(self, inputFileGtValues):
        df = pd.read_csv(inputFileGtValues, sep = ',',header = 0, index_col = None, error_bad_lines=False,  warn_bad_lines=False)
        fields = df.columns;

        print ('field xxxtt: ', fields)
        preproc = preprocess() 
        for tbfd in fields:
          #  print(pairs)
            val = preproc.filterNullValueAndLowercase(df[tbfd])
            self.TwoPossibleGtValuesMap[tbfd.strip().lower()] = val

            #print ('len A, lenB', len(set(A)), len(set(B)))
            print ('TwoPossibleGtValuesMap :', len(self.TwoPossibleGtValuesMap))
    '''
    
   #get two field value which is stored by column with header the first row(header = 0)  tsv
    @staticmethod
    def getAllFieldValuesbyColumnsTsvToLst(inputFile):
        df = pd.read_csv(inputFile, sep = '\t', header = 0, index_col = None, quoting=csv.QUOTE_NONE)
        fields = df.columns;
        #print ('field xxx: ', len(fields))
        fieldValLsts = []
        preproc = preprocess() 
        for tbfd in fields:
            valst = preproc.filterNullValue(df[tbfd])
            newLst = blist([tbfd]) + valst
            fieldValLsts.append(newLst)
        return fieldValLsts


   #get two field value which is stored by column with header the first row(header = 0)  tsv
    @staticmethod
    def getAllFieldValuesbyColumnsTsv(inputFile):
        df = pd.read_csv(inputFile, sep = '\t',header = 0, index_col = None)
        fields = df.columns;
        fieldValuesMap = {}
        #print ('field xxx: ', fields)
        preproc = preprocess() 
        for tbfd in fields:
          #  print(pairs)
            val = preproc.filterNullValue(df[tbfd])
            fieldValuesMap[tbfd.strip().lower()] = val

            #print ('len A, lenB', len(set(A)), len(set(B)))
        #print ('fieldValuesMap :', len(fieldValuesMap))
        return fieldValuesMap

    '''
   #get two field value which is stored by column with header the first row(header = 0) csv
    @staticmethod
    def getAllFieldValuesbyColumnsCsv(inputFile):
        df = pd.read_csv(inputFile, sep = ',',header = 0, index_col = None, error_bad_lines=False,  warn_bad_lines=False)
        fields = df.columns;
        fieldValuesMap = {}
        #print ('field xxx: ', fields)
        preproc = preprocess() 
        for tbfd in fields:
          #  print(pairs)
            val = preproc.filterNullValueAndLowercase(df[tbfd])
            fieldValuesMap[tbfd.strip().lower()] = val

            #print ('len A, lenB', len(set(A)), len(set(B)))
        print ('fieldValuesMap :', len(fieldValuesMap))
        return fieldValuesMap
    '''
    #get two files first columns' common and output common item with file1's other columns
    def getCommonFieldTwoFilesTsv(self, inputFile1, inputFile2, outFile):
        self.clearFileContent(outFile)
        File1ColumnMap = {}

        with open(inputFile1, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter='\t')
            preproc = preprocess()
            for row in tsvin:
                # negelect header
                row = preproc.word_strip_lower(row)            # strip and lowercase
                File1ColumnMap[row[0]]= row
        print ('File1ColumnMap :', len(File1ColumnMap))
        file2Lst = blist([])

        with open(inputFile2, 'r') as tsvfile:
            tsvin = csv.reader(tsvfile, delimiter='\t')
            preproc = preprocess()
            for row in tsvin:
                # negelect header
                row = preproc.word_strip_lower(row)            # strip and lowercase
                file2Lst.append(row[0])
        print ('file2Lst :', len(file2Lst))
        for ls in file2Lst:
      #      print ('ls :', ls)
            if ls in File1ColumnMap:
                print ('xxxxx :', len(file2Lst))
                self.writeListRowToFileCsv(outFile, File1ColumnMap[ls])

    @staticmethod
    def yieldEveryFileIterativeInDirectoryTsv(inputDir):
        #print ('inputDirdddddd ', inputDir)

        for root, directories, filenames in os.walk(inputDir):
            for filename in filenames: 
                if filename.endswith('.tsv'):
                # if 'allNonNumericalPairsRecordsMatchingStoredbyColumnsNoTimeNoPriKeyNoSmallRange' in filename:
                    #print ('filedddd ', filename)
                    yield (os.path.join(root,filename))
                    

    #sort the matching ratio and write into file
    def sortAndWritetoFile(self, lstTriple, outFile):
        # sort the matching ratio
        comRdFileObj = commonReadFile()
        lstTripleSorted = sorted(lstTriple, key=lambda pairval: pairval.value, reverse=True)
        #write sample running result
        fd = open(outFile,'a')
        for pr in lstTripleSorted:
            prATbField = pr.fieldA.split('.')[0].strip().upper() + '.' +  pr.fieldA.split('.')[1].strip().lower()
            prBTbField = pr.fieldB.split('.')[0].strip().upper() + '.' +  pr.fieldB.split('.')[1].strip().lower()
            if prATbField <= prBTbField:                        #in order, convenient to watch
     
                strVar = prATbField + '\t' + prBTbField + '\t' + str(pr.value) + '\t' + '\n'
            else:
                      #  tuplePrs = (tbfdB, tbfdA)
                strVar = prBTbField + '\t' + prATbField + '\t' + str(pr.value) + '\t' + '\n'                        
            comRdFileObj.writeStrRowToFileAppendWriter(fd, strVar)
        fd.close()
        
    #read the last N line number to map
    def readLastNLineFileTsvThreeColumnToLst(self,  lastNLine, inputFile):
        indexLastN = -1 * lastNLine;
        lstTriples = blist()
        f = open (inputFile)
        lineList = f.readlines()
        f.close()
        #print (lineList)
        print ("The last line is:", len(lineList))
        #print (lineList[-1])
        for row in lineList[indexLastN:-1]:
            #print ('row ', row, type(row))
            prA = row.split('\t')[0].strip().lower()           # strip and lowercase
            prB = row.split('\t')[1].strip().lower()           # strip and lowercase
            matchingRatio = row.split('\t')[2].strip().lower()           # strip and lowercase
            fdprsObj = fieldPairSim(prA, prB, matchingRatio)
            lstTriples.append(fdprsObj)
        return lstTriples
    

                
    #write similarity map , similarityMap key is pair(), value is a double type
    def writeEstimateSimilarityMap(self, outFile, similarityMap):
        #print ('len129: ', len(self.estMinHashSimilarityMap))
        commonReadFileObj = commonReadFile()
        
        with open(outFile, "a") as fd:
            for pair, sim in similarityMap.items():
                rowStr = pair[0] + '\t' + pair[1] + '\t' + str(sim) + '\n'
                commonReadFileObj.writeStrRowToFileAppendWriter(fd, rowStr)