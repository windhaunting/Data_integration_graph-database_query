# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:50:20 2016

@author: root
"""
import sys
import os
import argparse
import time

sys.path.insert(0, 'common')                  #common folder at the same directory as this file
sys.path.insert(1, 'numerical')               #numerical folder at the same directory as this file
sys.path.insert(2, 'non-numerical')           #non-numerical folder at the same directory as this file
sys.path.insert(3, 'lib')
sys.path.insert(4, 'lib/pycana')

import doctest

from preprocess import preprocess
from readDatabaseFile import readDatabaseFile
from commonReadFile import commonReadFile
from rangeDifferenceMetrics import rangeDifferenceMetrics
from bucketDotProductMetrics import bucketDotProductMetrics
from nonNumericalRecordPairsMatching import nonNumericalRecordPairsMatching

class dataMatching(object):
    def __init__(self):
        self.tblFieldName = []
    
     # reading all the database data  and preprocessing (like removing \n, na, tab') into memory
    def readTsvDatabase(self, dataInputDir, nonNumericalColumnSmallRange, interMediateFileFlag):
        rdDbFileObj = readDatabaseFile() 
         #read database files
        rdDbFileObj.getAllTablesDividedPrimary(dataInputDir, nonNumericalColumnSmallRange, interMediateFileFlag)

     #numerical matching algorithm column-wise, first range difference then bucket dot product metrics
    def numericalMatching(self, threadNum, numericalColumnSmallRange, rangeDiffThd, inputBucketSizeNum, primaryKeysSet, allNumericalValuesMap, outRangeFileFlag, finalNumericalOutputFile):
        print ('------------------------------- ')
        print ('begin numerical matching... ')
         # first calculate range difference score
        rangeDiffObj = rangeDifferenceMetrics()
        bucketdpObj = bucketDotProductMetrics()
        rangeDiffObj.outRangeFileGenerateFlag = outRangeFileFlag
        rangeDiffObj.getPercentilesAllNumerical(allNumericalValuesMap, rangeDiffObj.outRangeFileGenerateFlag)

        #calculate primary key's column range score with every other columns in other tables
        rangeDiffObj.multiThreadGetAllNumericalRangeDiffScore(threadNum, numericalColumnSmallRange, primaryKeysSet)
        
        bucketdpObj.rangeDiffThd = rangeDiffThd
        bucketdpObj.inputBucketSizeNum = inputBucketSizeNum
        bucketdpObj.allNumericalValuesMap = allNumericalValuesMap
        #calculate the bucket dot product using the range difference score below the threshold values
        bucketdpObj.multiThreadsGetAllNumericalBucketdotProductsScore(threadNum, rangeDiffObj.allNumericalPairsRangeDifferenceScoreMap, finalNumericalOutputFile)

     #nonumerical matching algorithm,  record-wise matching
    def nonNumericalMatching(self, tbFieldAllNonNumericalValuesMap, threadNum, prefixLength, sampleRecordsNum, recordPrSimiThreshold, finalNonNumericalOutputDir, outFileNonNumericalRatioScoreAll):
        print ('------------------------------- ')
        print ('begin non-numerical matching... ')
        nonNumMatchObj = nonNumericalRecordPairsMatching()
        #get non-numerical pairs to be matched
        pairsTupleTobeMatched = nonNumMatchObj.generatePairsTupleTobeMatched(tbFieldAllNonNumericalValuesMap)
        
        nonNumMatchObj.tbFieldAllNonNumericalValuesMap = tbFieldAllNonNumericalValuesMap
        nonNumMatchObj.prefixLength = prefixLength
        nonNumMatchObj.sampleRecordsNum = sampleRecordsNum
        nonNumMatchObj.recordPrSimiThreshold = recordPrSimiThreshold
        nonNumMatchObj.finalNonNumericalOutputDir = finalNonNumericalOutputDir
        nonNumMatchObj.threadNum = threadNum
        #non-numerical matching algorithm, multithread running
        nonNumMatchObj.multithreadgetNonNumericalCosinSimi(pairsTupleTobeMatched, outFileNonNumericalRatioScoreAll)



#main function
def main(argv):
    startTime = time.time()
    #doctest.testmod()
    #create directory automatically
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
        
    #input parameters generators
    parser = argparse.ArgumentParser(description='This is a matching script by fubao.')
    parser.add_argument('-i','--inputDBDir', help='Input file name',required=True)
    parser.add_argument('-rdt','--inputRDThd', help='Range difference threshold',required=True)
    parser.add_argument('-bs','--inputBucketNum', help='Bucket dot product size',required=True)
    parser.add_argument('-oNum','--outputNumericalDir',help='numerical output file name', required=True)

    parser.add_argument('-pl','--prefixLength',help='non-numerical prefix length', required=True)
    parser.add_argument('-spNum','--sampleNumofRecords',help='non-numerical sample record num', required=True)
    parser.add_argument('-recsimt','--recordPrSimiThreshold',help='non-numerical record similarity threshold', required=True)
    parser.add_argument('-oNonDir','--outputNonNumericalDir',help='non-numerical output dir', required=True)   #non-numerical has one dir and one file output

    parser.add_argument('-interOFlg','--interoutFlag',help='indicate intermediate output Flag', required=True)

    args = parser.parse_args()
 
    ## show values ##
    print ("Input file: %s" % args.inputDBDir)
   # print ("Output file: %s" % args.outputNumericalDir)
    
    dataMtObj = dataMatching()
    rdDbFileObj = readDatabaseFile() 
    numericalColumnSmallRange = 200
    nonNumericalColumnSmallRange = 200            #according to database range distribution, maybe change or not by different database, here temporarily hard code 200
    interMediateFileFlag = args.interoutFlag 
    
    inputDataFolderPath = args.inputDBDir + '/'
    inputRDThd = float(args.inputRDThd)
    inputBucketNum = int(args.inputBucketNum)
    outputNumerical = args.outputNumericalDir + '/' + 'allNumericalFinalResult.tsv'
    threadNum = 6

    dataMtObj.readTsvDatabase(inputDataFolderPath, nonNumericalColumnSmallRange, interMediateFileFlag)
  #  print ('len rdDbFileObj.tbFieldAllNumericalValuesMap ', len(rdDbFileObj.tbFieldAllNumericalValuesMap))

    #numerical matching processing
   # dataMtObj.numericalMatching(threadNum, numericalColumnSmallRange, inputRDThd, inputBucketNum, rdDbFileObj.primaryKeysSet, rdDbFileObj.tbFieldAllNumericalValuesMap, interMediateFileFlag, outputNumerical)

    #non-numerical matching processing
    prefixLength = int(args.prefixLength)
    sampleRecordsNum = int(args.sampleNumofRecords)
    recordPrSimiThreshold = float(args.recordPrSimiThreshold)
    finalNonNumericalOutputDir = args.outputNonNumericalDir
    outFileNonNumericalRatioScoreAll = finalNonNumericalOutputDir + '/'  + 'nonNumericalFinalMatchingRatio.tsv'
    
    print ('tbFieldAllNonNumericalValuesMap len ', len(rdDbFileObj.tbFieldAllNonNumericalValuesMap.keys()))
    dataMtObj.nonNumericalMatching(rdDbFileObj.tbFieldAllNonNumericalValuesMap, threadNum, prefixLength, sampleRecordsNum, recordPrSimiThreshold, finalNonNumericalOutputDir, outFileNonNumericalRatioScoreAll)

    endTime = time.time()
    print("Congratulations! Finished")
    print ('Total runtime: ', endTime-startTime)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
    
