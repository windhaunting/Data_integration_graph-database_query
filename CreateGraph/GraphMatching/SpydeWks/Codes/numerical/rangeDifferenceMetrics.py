# -*- coding: utf-8 -*-
"""
Created on Tue Nov  23 18:50:37 2015

@author: fubao
"""

import csv
from os import listdir
from os.path import isdir,join
from blist import blist

import numpy as np
import pandas as pd
import time
import itertools
import sys
sys.path.insert(0, 'common') 

from preprocess import preprocess
from commonReadFile import commonReadFile
from multiprocessing.dummy import Pool as ThreadPool 
from preprocess import fieldPairSim

Intermediate_files = ['intermediateOutput/numericalInterOutput/allNumericalRangePercentile.tsv', 'intermediateOutput/numericalInterOutput/allNumericalFinalRangeDifferenceScore.tsv']

class rangeDifferenceMetrics(object):

    allNumericalfieldRangeMap = {}                #key is table.field, value is the min, max, 10% percentile, 20% percentile....
    allNumericalPairsRangeDifferenceScoreMap = {} #key is table.field pairs tuple, value is the range difference score
    outRangeFileGenerateFlag = True
    
    def __init__(self):
       self.allNumericalRangeDifferenceScoreTripleLst = blist()

   
   # calculate the percentile according to different percentages
    def getRangePercentiles(self, valsSet, percentA1, percentA2, percentA3, percentA4, percentA5, percentA6, percentA7, percentA8, percentA9):   
        valList = list(map(float, valsSet))                 # to float,  some contains float, integer
       # valArray = np.array(valList)
        valArray = np.array(valList)                #consider unique for percentile calculation or not
         
       # print (valArray)
        #print (min(valArray), max(valArray))
        if (min(valArray) == float("inf") or max(valArray) == float("inf")):
          #  print ('222', min(valArray), max(valArray))
            return ['Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan']
        minVal = int(min(valArray))
        maxVal = int(max(valArray))
        percValA1 = int(np.percentile(valArray, percentA1))
        percValA2 = int(np.percentile(valArray, percentA2))
        percValA3 = int(np.percentile(valArray, percentA3))
        percValA4 = int(np.percentile(valArray, percentA4))
        percValA5 = int(np.percentile(valArray, percentA5))
        percValA6 = int(np.percentile(valArray, percentA6))
        percValA7 = int(np.percentile(valArray, percentA7))
        percValA8 = int(np.percentile(valArray, percentA8))
        percValA9 = int(np.percentile(valArray, percentA9))
       # print ('percValA, B', minVal, maxVal, percValA, percValB)
        return [minVal, maxVal, percValA1, percValA2, percValA3, percValA4, percValA5, percValA6, percValA7, percValA8, percValA9]
        
        
    #use 20%, 30%, 80%, 90% (D2, D3, D8, D9) to get the final range difference
    def getRangeMetricNumericalUsed(self, x2, y2, x3, y3, x8, y8, x9, y9):
        if abs(x2+y2) != 0:
            d2 = 2 * abs(x2-y2) / abs(x2+y2)
        else:
            d2 = 0
        if abs(x3+y3) != 0:
            d3 = 2 * abs(x3-y3) / abs(x3+y3)
        else:
            d3 = 0

        if abs(x8+y8) != 0:
            d8 = 2 * abs(x8-y8) / abs(x8+y8)
        else:
            d8 = 0
        if abs(x9+y9) != 0:
            d9 = 2 * abs(x9-y9) / abs(x9+y9)
        else:
            d9 = 0
        d2389 = (d2+d3+d8+d9)/4
        return d2389

  #get percentiles of all numerical values and output to files or not(optional)
    def getPercentilesAllNumerical(self, allNumericalValuesMap, outRangeFileFlag):
        comRdFileObj = commonReadFile()
        if (outRangeFileFlag):
            comRdFileObj.clearFileContent(Intermediate_files[0])               #clear file
            headerLst = blist()

            headerLst.append('table.field')
            headerLst.append('20% percentile')
            headerLst.append('30% percentile')
            headerLst.append('80% percentile')
            headerLst.append('90% percentile')                                    
            comRdFileObj.writeListRowToFileTsv(Intermediate_files[0], headerLst)
        print ('len allNumericalValuesMap ', len(allNumericalValuesMap))
        for tbField, valsSet in allNumericalValuesMap.items():
            if len(valsSet[1:]) != 0:              #the tb.field values except tb.field
                [minVal, maxVal, percValA1, percValA2, percValA3, percValA4, percValA5, percValA6, percValA7, percValA8, percValA9] = self.getRangePercentiles(valsSet[1:], 10, 20, 30, 40, 50, 60, 70, 80, 90)
                if [minVal, maxVal, percValA1, percValA2, percValA3, percValA4, percValA5, percValA6, percValA7, percValA8, percValA9] != ['Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan']:
                    percentLst = blist()
                    percentLst.append(tbField)
                    percentLst.append(str(percValA2))
                    percentLst.append(str(percValA3))
                    percentLst.append(str(percValA8))
                    percentLst.append(str(percValA9))    
                    self.allNumericalfieldRangeMap[tbField] = percentLst
                    if (outRangeFileFlag):
                        comRdFileObj.writeListRowToFileTsv(Intermediate_files[0],percentLst)
                        
    #get final range difference score, use primary key 
    def getAllNumericalRangeDiffScore(self, onePrimaryKey, allNumericalfieldRangeMap):

        #matching using primary key to calculate range difference score, not considering the same table matching
        if onePrimaryKey in allNumericalfieldRangeMap:                    #primary key is in the numerical algorithm,  run numerical algorithm
            for tbFd in allNumericalfieldRangeMap:   
                if (onePrimaryKey, tbFd) in self.allNumericalPairsRangeDifferenceScoreMap or (tbFd, onePrimaryKey) in self.allNumericalPairsRangeDifferenceScoreMap:
                    continue
                tableNm1 = onePrimaryKey.split('.')[0]
                tableNm2 = tbFd.split('.')[0]
                if  onePrimaryKey != tbFd and tableNm1 != tableNm2:    #judge the other field not in the same table matching etc.
                   # print ('len allNumericalFieldsList', tbfdPri + ',' + tbFd)
                    percentileListA = allNumericalfieldRangeMap[onePrimaryKey][1:]
                    percentileListB = allNumericalfieldRangeMap[tbFd][1:]
                    rangeDiffScore = self.getRangeMetricNumericalUsed(int(percentileListA[0]), int(percentileListB[0]), int(percentileListA[1]), int(percentileListB[1]), int(percentileListA[2]), int(percentileListB[2]), int(percentileListA[3]), int(percentileListB[3]))
                    rdScoreLst = blist() 
                    rdScoreLst.append(onePrimaryKey)
                    rdScoreLst.append(tbFd)
                    rdScoreLst.append(rangeDiffScore)
                    self.allNumericalPairsRangeDifferenceScoreMap[(onePrimaryKey, tbFd)] = rangeDiffScore
                    fdprsObj = fieldPairSim(onePrimaryKey, tbFd, rangeDiffScore)
                    self.allNumericalRangeDifferenceScoreTripleLst.append(fdprsObj)
                   
                       
    # every thread map function
    def getAllNumericalRangeDiffScoreMap(self, onePrimaryKey):
        self.getAllNumericalRangeDiffScore(onePrimaryKey, self.allNumericalfieldRangeMap)

    #multi thread pool management to execute range difference score function
    def multiThreadGetAllNumericalRangeDiffScore(self, threadNum, numericalColumnSmallRange, primaryKeysSet):
        comRdFileObj = commonReadFile()
        if (self.outRangeFileGenerateFlag):
            comRdFileObj.clearFileContent(Intermediate_files[1])               #clear file
            headerLst = blist()
            headerLst.append('table.field A')
            headerLst.append('table.field B')
            headerLst.append('range difference score')    
            comRdFileObj.writeListRowToFileTsv(Intermediate_files[1],headerLst)
        
        #remove numerical small range
        tmpMap = self.allNumericalfieldRangeMap.copy()
        for tbfield, Percentiles in tmpMap.items():
            if (int(Percentiles[4]) - int(Percentiles[1])) <= numericalColumnSmallRange:
                del self.allNumericalfieldRangeMap[tbfield]

        print ('len primaryKeysSet, allNumericalfieldRangeMap ', len(primaryKeysSet), len(self.allNumericalfieldRangeMap))
                
        

        pool = ThreadPool(threadNum)
        pool.map(self.getAllNumericalRangeDiffScoreMap, primaryKeysSet)
        pool.close() 
        pool.join()
        
        if (self.outRangeFileGenerateFlag):
            comRdFileObj = commonReadFile()
            comRdFileObj.sortAndWritetoFile(self.allNumericalRangeDifferenceScoreTripleLst, Intermediate_files[1])                       