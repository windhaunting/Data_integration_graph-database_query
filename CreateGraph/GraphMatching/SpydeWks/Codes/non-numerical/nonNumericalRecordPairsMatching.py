# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 10:45:23 2015

@author: fubao
"""

import numpy as np
import time
import itertools
import sys
import random
import cProfile, pstats, io
import os
from math import sqrt
from math import floor
from math import ceil
from blist import blist
from multiprocessing.dummy import Pool as ThreadPool 

sys.path.insert(0, 'common') 

from commonReadFile import commonReadFile
from preprocess import preprocess
from preprocess import fieldPairSim

Intermediate_DirFiles = ['intermediateOutput/nonNumericalInterOutput', 'intermediateOutput/nonNumericalInterOutput/nonNumericalSamplesMatchingRatio.tsv', 'intermediateOutput/nonNumericalInterOutput/second/partResultOutput']

        
#non-numerical matching algorithm class
class nonNumericalRecordPairsMatching(object):
     
    tbFieldAllNonNumericalValuesMap = {}
    prefixLength = 2
    sampleRecordsNum = 2000
    recordPrSimiThreshold = 0.5
    finalNonNumericalOutputDir = ""
    ratioPruning =0.2
    recordPartialResultTimeStart = None      #start time
    recordPartialResultTimeEnd = None          

    #outFileNonNumericalRatioScore = ""
    threadNum = 4
    
    def __init__(self):
        self.lstTopPairsTobeAllMatched = blist()     # every item is TbfieldPairSim object
    
    def generatePairsTupleTobeMatched(self, tbFieldAllNonNumericalValuesMap):
        pairsTupleTobeMatched = set()
        for tbfdA in tbFieldAllNonNumericalValuesMap:
            for tbfdB in tbFieldAllNonNumericalValuesMap:               
                tbA = tbfdA.strip().split('.')[0]
                tbB = tbfdB.strip().split('.')[0]
                if (tbA != tbB):
                    if tbfdA <= tbfdB:                        #in order, convenient to watch
                       # tuplePrs = (tbfdA, tbfdB)
                        prs = tbfdA + '-' + tbfdB
                    else:
                      #  tuplePrs = (tbfdB, tbfdA)
                        prs = tbfdB + '-' + tbfdA

                    pairsTupleTobeMatched.add(prs)
        print ('pairsTupleTobeMatched len ', len(pairsTupleTobeMatched))
        return pairsTupleTobeMatched
        
        

    def cosinSimiAmongRecord(self, recA, recB, vABCacheMap):
        preproc = preprocess()
        #print ('len vACacheMap', len(vACacheMap), len(vBCacheMap))
        #print ('in vBCacheMap')

      #  totalStartOne = time.time()
        resCos = preproc.cosSimilarity(vABCacheMap[recA], vABCacheMap[recB])
      #  totalEndOne = time.time()
       # timeConsume = totalEndOne - totalStartOne
        #print ('cosSimilarity time: ' , timeConsume)
        return resCos

    def getParsedSetMap(self, lsValA, lsValB, prefixLength):
        preproc = preprocess()
        vABCacheMap = {}
        lsVals = set(lsValA) | set(lsValB)
        vABCacheMap = {rec: preproc.parseStemOneRecord(rec, prefixLength) for rec in lsVals}
        #vABCacheMap = {recA: preproc.parseStemOneRecord(recA, adjustLength) for recA in lsValA}
        return vABCacheMap

     #decide which columns pair should be discarded 
    def filterColumnsWithSample(self, samplesFlag, lsValA, lsValB, prefixLength, sampleNumofRecords, recordPrSimiThreshold, pairsNameLstA, pairsNameLstB, cosResLst):
        #print ('xxxxxlen lsValA, lsValB': , len(lsValA), len(lsValB))
        if (samplesFlag):
        #if the column range is bigger than sampleNumofRecords only
            if sampleNumofRecords < len(set(lsValA)):
                #fetch the random sample to get a new lsValA
                lsValA = random.sample(set(lsValA), sampleNumofRecords)

            if sampleNumofRecords < len(set(lsValB)):
                lsValB = random.sample(set(lsValB), sampleNumofRecords)

        vABCacheMap = self.getParsedSetMap(lsValA, lsValB, prefixLength)
       # print ('vABCacheMap len' , len(vABCacheMap))
        countTruePairs = 0
        countAboveThrehold = 0
        for vA in set(lsValA):                  #matching between records
            for vB in set(lsValB):
                #calculate cosine similarity
                #strPr = vA + ";" + vB
               # if strPr not in cachedSet:          #too many memory consumed with cached pair                   
                cosRes = self.cosinSimiAmongRecord(vA, vB, vABCacheMap)
                #cachedSet.add(strPr)               #no matter threshold, all records visited need to be cached
                if (cosRes >= recordPrSimiThreshold):
                    vA = vA.replace('\t', ' ').strip()          #in case string contains 'tab'
                    vB = vB.replace('\t', ' ').strip()
                    pairsNameLstA.append(vA)
                    pairsNameLstB.append(vB)
                    cosResLst.append(cosRes)
                    countAboveThrehold += 1
                countTruePairs += 1
        return [countTruePairs, countAboveThrehold, len(vA), len(vB)]
   
    #calculate record-wise similarity, samplesFlag determines the sample or all    
    def getSamplesNonumericalCosSimiRecordWise(self, pair, samplesFlag, tbFieldAllNonNumericalValuesMap, prefixLength, sampleRecordsNum, recordPrSimiThreshold, finalNonNumericalOutputDir):
        comRdFileObj = commonReadFile()

        i = 0
        #get field values
        if (samplesFlag):
            prA = pair.strip().split('-')[0].lower()            #tb.field A
            prB = pair.strip().split('-')[1].lower()
        else:
            prA = pair.fieldA.strip()
            prB = pair.fieldB.strip()
        #get index 
        if prA in tbFieldAllNonNumericalValuesMap and prB in tbFieldAllNonNumericalValuesMap:
            #get all tb field values
           # print ('pairsDDDDDDDDD: ', prA, prB)

            lsValA = tbFieldAllNonNumericalValuesMap[prA]               #get values
            lsValB = tbFieldAllNonNumericalValuesMap[prB]
            # print ('newLsValA AAAA: ' , prA, prB, len(lsValA),lsValA[0], len(lsValB), lsValB[0])
            writeWholeLst = blist([])                   #write rows lists
            cosResLst = blist([])
            pairsNameLstA = blist([])
            pairsNameLstB = blist([])
            pairsNameLstA.append(str(prA))
            pairsNameLstB.append(str(prB))               
            cosResLst.append('Cosine Similarity')
            
            [countTruePairs, countAboveThrehold, laAllLen, lbAlllen] = self.filterColumnsWithSample(samplesFlag, lsValA, lsValB, prefixLength, sampleRecordsNum, recordPrSimiThreshold, pairsNameLstA, pairsNameLstB, cosResLst)
            # if any record pair similarity above threshold, run again sample record similarity
            if (len(pairsNameLstA) > 1):                                    #no any pair qualifies
                writeWholeLst.append(pairsNameLstA)
                writeWholeLst.append(pairsNameLstB)
                writeWholeLst.append(cosResLst)
                
                #fdprsObj = fieldPairSim(prA, prB, len(pairsNameLstA)/countTruePairs)
                #matching ratio score calcuation    1/2*(la/l_alla + lb/l_allb)
                laMatchLen = len(set(pairsNameLstA[0]))-1
                lbMatchLen = len(set(pairsNameLstB[1]))-1
                matchingRatio = 0.5 * (laMatchLen/laAllLen + lbMatchLen/lbAlllen)
                fdprsObj = fieldPairSim(prA, prB, matchingRatio)
                
                self.lstTopPairsTobeAllMatched.append(fdprsObj)
                
                if(len(writeWholeLst) >= 3):
                    #select records, numOfRecords,
                    tbA = prA.split('.')[0]
                    fdA = prA.split('.')[1]
                    tbB = prB.split('.')[0]
                    fdB = prB.split('.')[1]
                    outFile2 =  str(tbA).upper() + '__'+ str(fdA)+ '-' + str(tbB).upper() + '__' + str(fdB)
                
                    if (samplesFlag):                  #sample result output dir
                        finalNonNumericalOutputDir = Intermediate_DirFiles[0]
                        fd = open(finalNonNumericalOutputDir + '/' + outFile2 + '.tsv','w')
                    comRdFileObj.writeListsColumnsToFileAppendWriterTsv(fd, writeWholeLst)
                    i = i + 1
                    fd.close()
                    writeWholeLst = blist([])
                # totalEndOne = time.time()
                # print ('total time One', totalEndOne - totalEndOneFilter)
        #because the speed and time problem, write out part of result     

        if (len(self.lstTopPairsTobeAllMatched) != 0 and len(self.lstTopPairsTobeAllMatched)%200 == 0):
            if not os.path.exists('intermediateOutput/nonNumericalInterOutput/second'):
                os.makedirs('intermediateOutput/nonNumericalInterOutput/second')
            if not os.path.exists('intermediateOutput/nonNumericalInterOutput/second/partResultOutput'):
                os.makedirs('intermediateOutput/nonNumericalInterOutput/second/partResultOutput')
            comRdFileObj = commonReadFile()                                       # clear only matching ratio output file
            comRdFileObj.sortAndWritetoFile(self.lstTopPairsTobeAllMatched, Intermediate_DirFiles[2] + '/' + 'partRatioScoreAllResult00' + str(len(self.lstTopPairsTobeAllMatched)) + '.tsv')
 
 
    #multithread used map function samples record first
    def getSamplesNonumericalCosSimiRecordWiseMap(self, pair):
        self.getSamplesNonumericalCosSimiRecordWise(pair, True, self.tbFieldAllNonNumericalValuesMap, self.prefixLength, self.sampleRecordsNum, self.recordPrSimiThreshold, self.finalNonNumericalOutputDir)
        
    
    #read from filematching ratio file to get top k pair for all non-numerical matching
    def readSamplesResultTopKMatchingRatio(self, outFileNonNumericalRatioScoreSample, outFileNonNumericalRatioScoreAll):
        comRdFileObj = commonReadFile()
        pairLst = comRdFileObj.readTwoColumnTsvFileToList(outFileNonNumericalRatioScoreSample)
        self.multithreadgetAllNonNumericalCosinSimi(False, pairLst, outFileNonNumericalRatioScoreAll)


    #multithread used map function run all non-numerical records pairs
    def getNonumericalCosSimiRecordWiseSampleMap(self, pair):
        self.getSamplesNonumericalCosSimiRecordWise(pair, False, self.tbFieldAllNonNumericalValuesMap, self.prefixLength, self.sampleRecordsNum, self.recordPrSimiThreshold, self.finalNonNumericalOutputDir)
        
            
    #use thread pool to automatically iterate the set of all top pairsAllTop to do matching
    def multithreadgetAllNonNumericalCosinSimi(self, sampleFlag, pairsAllTop, outFileNonNumericalRatioScoreAll):
        #for pr in pairsTupleTobeMatched:
        #    print ('prrrrrr ', pr)
        self.recordPartialResultTimeStart = time.time()           #start time
        comRdFileObj = commonReadFile()                                       # clear only matching ratio output file
        comRdFileObj.clearFileContent(outFileNonNumericalRatioScoreAll)               #clear file
        
        self.lstTopPairsTobeAllMatched = blist()              #clear at the beginning
        pool = ThreadPool(self.threadNum)
        if sampleFlag:
            
            pool.map(self.getNonumericalCosSimiRecordWiseSampleMap, pairsAllTop)
        else:
            pool.map(self.getNonumericalCosSimiRecordWiseScalingMethodMap, pairsAllTop)
        pool.close() 
        pool.join()
                
         #write all matching ratio result
        comRdFileObj.sortAndWritetoFile(self.lstTopPairsTobeAllMatched, outFileNonNumericalRatioScoreAll)


    #use thread pool to automatically iterate the set of pairsTupleTobeMatched to do matching
    def multithreadgetNonNumericalCosinSimi(self, pairsTupleTobeMatched, outFileNonNumericalRatioScoreAll):
        #    print ('prrrrrr ', pr)
        #profile begin
       # pr = cProfile.Profile()
       # pr.enable()

        outFileNonNumericalRatioScoreSample = Intermediate_DirFiles[1]
        print ('multithreadgetNonNumericalCosinSimi to be paired len ', len(pairsTupleTobeMatched))

        comRdFileObj = commonReadFile()                                       # clear only matching ratio output file
        comRdFileObj.clearFileContent(outFileNonNumericalRatioScoreSample)               #clear file
        self.lstTopPairsTobeAllMatched = blist()              #clear at the beginning
        pool = ThreadPool(self.threadNum)
        pool.map(self.getSamplesNonumericalCosSimiRecordWiseMap, pairsTupleTobeMatched)
        pool.close() 
        pool.join()
        
        #write samples matching ratio result
        print ('multithreadgetNonNumericalCosinSimi pairs result len ', len(self.lstTopPairsTobeAllMatched), outFileNonNumericalRatioScoreSample)

        comRdFileObj.sortAndWritetoFile(self.lstTopPairsTobeAllMatched, outFileNonNumericalRatioScoreSample)

        #running all sample result, two ways. one way is to read file, the other way is to read from self.lstTopPairsTobeAllMatched
        #self.readSamplesResultTopKMatchingRatio(outFileNonNumericalRatioScoreSample, outFileNonNumericalRatioScoreAll)
        
        # the second way to do all mathcing
       # self.multithreadgetAllNonNumericalCosinSimi(False, self.lstTopPairsTobeAllMatched, outFileNonNumericalRatioScoreAll)
        '''
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print ('s.getvalue', s.getvalue())
       # pr.dump_stats('tttttt.txt')
        '''
        
    #use thread pool to automatically iterate the set of pairsTupleTobeMatched to do matching
    def multithreadGetFinalNonNumericalCosinSimiAllPairs(self, pairsTupleTobeMatched, outFileNonNumericalRatioScoreAll):
        #for pr in pairsTupleTobeMatched:
        #    print ('prrrrrr ', pr)
        
        #running all sample result, two ways. one way is to read file, the other way is to read from self.lstTopPairsTobeAllMatched
        #self.readSamplesResultTopKMatchingRatio(outFileNonNumericalRatioScoreSample, outFileNonNumericalRatioScoreAll)
        
        # the second way  to do all mathcing
        self.multithreadgetAllNonNumericalCosinSimi(False, pairsTupleTobeMatched, outFileNonNumericalRatioScoreAll)

    #scaling method method map
    def getNonumericalCosSimiRecordWiseScalingMethodMap(self, pair):
        self.getNonumericalCosSimiRecordWiseScalingMethod(pair, self.tbFieldAllNonNumericalValuesMap, self.prefixLength, self.sampleRecordsNum, self.ratioPruning, self.recordPrSimiThreshold, self.finalNonNumericalOutputDir)

    #another method for scaling non-numerical running
    #calculate record-wise similarity, scaling method
    def getNonumericalCosSimiRecordWiseScalingMethod(self, pair, tbFieldAllNonNumericalValuesMap, prefixLength, partFetchNum, ratioPruning, recordPrSimiThreshold, finalNonNumericalOutputDir):
        comRdFileObj = commonReadFile()
        if not os.path.exists(finalNonNumericalOutputDir + '/' + 'pruneResults'):
            os.makedirs(finalNonNumericalOutputDir + '/' + 'pruneResults')

        i = 0
        #get field values
        prA = pair.strip().split('-')[0].lower()            #tb.field A
        prB = pair.strip().split('-')[1].lower()
        #get index 
        if prA in tbFieldAllNonNumericalValuesMap and prB in tbFieldAllNonNumericalValuesMap:
            #get all tb field values
          #  print ('pairsDDDDDDDDD: ', prA, prB)

            lstValA = tbFieldAllNonNumericalValuesMap[prA]               #get values
            lstValB = tbFieldAllNonNumericalValuesMap[prB]
            # print ('newLsValA AAAA: ' , prA, prB, len(lsValA),lsValA[0], len(lsValB), lsValB[0])
            writeWholeLst = blist([])                   #write rows lists
            cosResLst = blist([])
            pairsNameLstA = blist([])
            pairsNameLstB = blist([])
            pairsNameLstA.append(str(prA))
            pairsNameLstB.append(str(prB))               
            cosResLst.append('Cosine Similarity')
            countTrueComparePairs = 0
           #partition A and B columns into several partitions respectively
            lenA = len(lstValA)
            lenB = len(lstValB)

            lenAPartition = min(partFetchNum, lenA)
            numAPartition = ceil(lenA/lenAPartition)
            lenBPartition = min(partFetchNum, lenB)
            numBPartition = ceil(lenB/lenBPartition)

            #scalable method, in partition times partion pairs, if in the first half of partition, the ratio of matching above threshod is less than ratioPruning, exit this column pairs.
            Bexit = False
            laAllLenWhole = 0
            lbAlllenWhole = 0
            for i in range(0, numAPartition):  
                if Bexit:
                    break
                if (i+1)*partFetchNum <= lenA:
                    lsValACur = lstValA[i*partFetchNum:(i+1)*partFetchNum]
                else:
                    lsValACur = lstValA[i*partFetchNum:lenA]
                
                for j in range(0, numBPartition):
                    if (j+1)*partFetchNum <= lenB:
                        lsValBCur = lstValB[j*partFetchNum:(j+1)*partFetchNum]
                    else:
                        lsValBCur = lstValB[j*partFetchNum:lenB]
                    #print ('countTruePairsAAAAAAAAAA ', lenA, lenB, prA, prB)
    
                    [countTrueComparePairsEvery, countAboveThreholdEvery, laAllLen, lbAlllen] = self.filterColumnsWithSample(False, lsValACur, lsValBCur, prefixLength, partFetchNum, recordPrSimiThreshold, pairsNameLstA, pairsNameLstB, cosResLst)
                    #print ('pairsccccccccc: ', prA, prB, countAboveThrehold, partFetchNum, numAPartition)
                    laAllLenWhole += laAllLen
                    lbAllLenWhole += lbAlllen
                    countTrueComparePairs += countTrueComparePairsEvery
                    if (countAboveThreholdEvery/((len(lsValACur)+len(lsValBCur))/2) < ratioPruning):      #  (numAPartition >=2) and (i <= 2*numAPartition/3) and  judge if the ratio of matching above threshold is low, exit and go to next column,until to the final partition?
                             Bexit = True
                             filetmp = finalNonNumericalOutputDir + '/' + 'pruneResults' + '/' +'prunePairs.tsv' 
                             rowStr= prA + '\t' + prB + '\t' + '\n'
                             comRdFileObj.writeStrRowToFileAppend(filetmp, rowStr)
                            # print ('pairsDDDDDDDDD: ', prA, prB)
                             break
                 #consider this column pair            
            # if any record pair similarity above threshold, run again sample record similarity
            if (not Bexit) and (len(pairsNameLstA) > 1):                                    #no any pair qualifies
                writeWholeLst.append(pairsNameLstA)
                writeWholeLst.append(pairsNameLstB)
                writeWholeLst.append(cosResLst)
                #print ('countTruePairsBBBBBBBB ', countTrueComparePairs,  prA, prB)
                ##fdprsObj = fieldPairSim(prA, prB, len(pairsNameLstA)/countTrueComparePairs)
                
                laMatchLen = len(set(pairsNameLstA[0]))-1
                lbMatchLen = len(set(pairsNameLstB[1]))-1
                matchingRatio = 0.5 * (laMatchLen/laAllLen + laAllLenWhole/lbAlllenWhole)
                fdprsObj = fieldPairSim(prA, prB, matchingRatio)

                self.lstTopPairsTobeAllMatched.append(fdprsObj)
                
                if(len(writeWholeLst) >= 3):
                    #select records, numOfRecords,
                    tbA = prA.split('.')[0]
                    fdA = prA.split('.')[1]
                    tbB = prB.split('.')[0]
                    fdB = prB.split('.')[1]
                    outFile2 =  str(tbA).upper() + '__'+ str(fdA)+ '-' + str(tbB).upper() + '__' + str(fdB)
                
                    fd = open(finalNonNumericalOutputDir + '/' + outFile2 + '.tsv','w')
                    comRdFileObj.writeListsColumnsToFileAppendWriterTsv(fd, writeWholeLst)
                    fd.close()
                    writeWholeLst = blist([])
                # totalEndOne = time.time()
                # print ('total time One', totalEndOne - totalEndOneFilter)
        #because the speed and time problem, write out part of result to look   
        self.recordPartialResultTimeEnd = time.time()           #start time
        if ((len(self.lstTopPairsTobeAllMatched) != 0 and len(self.lstTopPairsTobeAllMatched)%30 == 0) or ((self.recordPartialResultTimeEnd - self.recordPartialResultTimeStart) >= 86400)):               #86400seconds =1 days
            self.recordPartialResultTimeStart = time.time()          
            if not os.path.exists(finalNonNumericalOutputDir + '/' + 'partResultOutput'):
                os.makedirs(finalNonNumericalOutputDir + '/' + 'partResultOutput')
            comRdFileObj = commonReadFile()                                       # clear only matching ratio output file
            comRdFileObj.sortAndWritetoFile(self.lstTopPairsTobeAllMatched, finalNonNumericalOutputDir + '/' + 'partResultOutput'+ '/' + 'partRatioScoreAllResult00' + str(len(self.lstTopPairsTobeAllMatched)) + '.tsv')
                    
    #combine the different result files from different machines to get the file output
    def combineFinalResultFromMultipleMachine(self, inputDirPath, outFile):
        readLastNNum = 50
        comRdFileObj = commonReadFile()
        comRdFileObj.clearFileContent(outFile)               #clear file
        lstAllTriples = blist()
        
        for fileName in commonReadFile.yieldEveryFileIterativeInDirectoryTsv(inputDirPath):
            print ('fileNamexxxxxx ', fileName)
            lstAllTriples = lstAllTriples + comRdFileObj.readLastNLineFileTsvThreeColumnToLst(readLastNNum, fileName)
    
        fd = open(outFile,'w')
       
        strVar = 'TABLE.field A' + '\t' + 'TABLE.fieldB' + '\t' + 'matchingRatio' + '\t' + '\n'
        comRdFileObj.writeStrRowToFileAppendWriter(fd, strVar)
        fd.close()                        
        comRdFileObj.sortAndWritetoFile(lstAllTriples, outFile)
        
         
         
         
         
         
         
         
         