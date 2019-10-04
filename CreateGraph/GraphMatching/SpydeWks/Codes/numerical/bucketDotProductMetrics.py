# -*- coding: utf-8 -*-
"""
Created on Wed Dec  12 00:13:18 2015

@author: fubao
"""
import numpy as np
from bitarray import bitarray
from blist import blist
import sys

sys.path.insert(0, 'common') 
from preprocess import preprocess
from commonReadFile import commonReadFile
from multiprocessing.dummy import Pool as ThreadPool 
from preprocess import fieldPairSim

class bucketDotProductMetrics(object):

    rangeDiffThd = 0
    inputBucketSizeNum = 0
    allNumericalValuesMap = {}
    
    def __init__(self):
        self.stored_vectors = blist([])             #store the vector for next run
        self.resassociation_vectors = blist([])               #store the vector for next run.  because generating vectors for dot product is so slow
        self.allNumericalBucketDPScoreTripleLst = blist()



    # dot product of two vectors
    def dotProduct(self, vecA, vecB, normalized):
        #print ('vecA vecB: ', len(vecA), len(vecB))
        A = np.asarray(vecA)
        B = np.asarray(vecB)
        dotRes = np.dot(A, B)
        if normalized is False:
           return dotRes
        else:
            magnA = np.sqrt(A.dot(A))
            magnB = np.sqrt(B.dot(B))
            if (magnA == 0) or (magnB == 0):
                normDotRes = 0
                return normDotRes
            normDotRes = dotRes / (magnA * magnB)           
            #print ('magnA magnB: ', dotRes, magnA, magnB, type(magnA), type(magnB))
            return normDotRes

     #unique Values input for listA, listB, as long as there is one in the bucket, the vector's corresponding value would be 1
    def bucketDotProduct(self, listA, listB, bucketNum, rangeXY, normalized):
         #union the range
        wholeRangeSmallest = min(min(listA), min(listB))
        vecA = blist([])
        vecB = blist([])

        if rangeXY < bucketNum:
            bucketNum = rangeXY
        #de the bucket size:
        bucketSize = int(rangeXY) /float(bucketNum)
        #print ('bucketNum bucketSize: ', bucketNum, bucketSize)
     #   print ('whole Range: ', wholeRangeSmallest, wholeRangelargest)

        #common value first
        commonSet = set(listA & listB)  
        #print ('common Set', commonSet)

        blocksRecord = bitarray(bucketNum) 		    # creates bucketNum allocated bits
        blocksRecord.setall(False)

        for comm in commonSet:
            blkIndex = int((comm-wholeRangeSmallest) / bucketSize)
            if(blocksRecord[blkIndex] == False):             # judge whether corresponding value to add (added before if == 1)
                if comm in listA and comm in listB:
                    vecA.append(1)
                    vecB.append(1)
                    blocksRecord[blkIndex] = True

        #union the set
        newUnionSet = set(listA | listB)
        #print ('newUnionSet:', len(newUnionSet))
        for sep in newUnionSet:
            if sep not in commonSet:
                blkIndex = int((sep-wholeRangeSmallest) / bucketSize)
                if(blocksRecord[blkIndex] == False):             # judge whether corresponding value to add (added before if == 1)
                    if sep in listA and sep in listB:
                        vecA.append(1)
                        vecB.append(1)
                    elif sep in listA:
                        vecA.append(1)
                        vecB.append(0)
                    elif sep in listB:
                        vecA.append(0)
                        vecB.append(1)
                    blocksRecord[blkIndex] = True

        #generateVectorEnd = time.time()
       # print ('generate vector time', generateVectorEnd - generateVectorStart)

        self.stored_vectors.append(vecA)       #store vectors
        self.stored_vectors.append(vecB)       #store vectors
        bucketDotProdRes = self.dotProduct(vecA, vecB, normalized)
        return bucketDotProdRes
   
    #after range difference score, use its score below threshold to calculate all the corresponding pairs bucket dot product
    def getAllNumericalBucketdotProductsScore(self, rangeDiffThd, inputBucketSizeNum, oneRangeDiffResPair, allNumericalValuesMap):
       # print ('oneRangeDiffResPair : ', type(oneRangeDiffResPair), oneRangeDiffResPair)
        preproc = preprocess()

        pair = oneRangeDiffResPair
        setX = set()
        setY = set()
        fieldX = str(pair[0])
        fieldXVal = allNumericalValuesMap[fieldX]
        for val in set(fieldXVal):           #unique value
            if preproc.is_number(val) and int(float(val)) >= 0 and int(float(val)) < 200000000000:
                setX.add(int(float(val)))
        
        fieldY = str(pair[1])
        fieldYVal = allNumericalValuesMap[fieldY]
        for val in set(fieldYVal):
            if preproc.is_number(val) and int(float(val)) >= 0 and int(float(val)) < 200000000000:
                #if selectNum <= 0.5*len(fieldBValue):
                setY.add(int(float(val)))

        rangeXY = int(max(min(setX), max(setX), min(setY), max(setY)) - min(min(setX), max(setX), min(setY), max(setY)) + 1)      #union of range to decide the
            # bucketNum       
        bdpRes = self.bucketDotProduct(setX, setY, int(inputBucketSizeNum), rangeXY, True)          #normalized buckete dot product score
        bdpScoreLst = blist() 
        bdpScoreLst.append(fieldX)
        bdpScoreLst.append(fieldY)
        bdpScoreLst.append(bdpRes)
        fdprsObj = fieldPairSim(fieldX, fieldY, bdpRes)
        self.allNumericalBucketDPScoreTripleLst.append(fdprsObj)

    # every thread map function
    def getAllNumericalBucketdotProductsScoreMap(self, oneRangeDiffResPair):
        self.getAllNumericalBucketdotProductsScore(self.rangeDiffThd, self.inputBucketSizeNum, oneRangeDiffResPair, self.allNumericalValuesMap)
        
        
    #multi thread pool management to execute bucket dot product score function
    def multiThreadsGetAllNumericalBucketdotProductsScore(self, threadNum, allNumericalPairsRangeDifferenceScoreMap, finalNumericalOutputFile):
        comRdFileObj = commonReadFile()
        comRdFileObj.clearFileContent(finalNumericalOutputFile)               #clear file

        headerLst = blist()
        headerLst.append('table.field A')
        headerLst.append('table.field B')
        headerLst.append('bucket dot product score')  
        comRdFileObj.writeListRowToFileTsv(finalNumericalOutputFile, headerLst)
        
        #remove range difference result above threshold pair
        tmpMap = allNumericalPairsRangeDifferenceScoreMap.copy()
        for pair, rdScore in tmpMap.items():
            if rdScore > float(self.rangeDiffThd):
                del allNumericalPairsRangeDifferenceScoreMap[pair]

        print ('allNumericalPairsRangeDifferenceScoreMap below threshold len : ', len(allNumericalPairsRangeDifferenceScoreMap))
       
        pool = ThreadPool(threadNum)
        pool.map(self.getAllNumericalBucketdotProductsScoreMap, allNumericalPairsRangeDifferenceScoreMap)
        pool.close() 
        pool.join()
        comRdFileObj.sortAndWritetoFile(self.allNumericalBucketDPScoreTripleLst, finalNumericalOutputFile)                              
        print ('allNumericalBucketDPScoreTripleLst len : ', len(self.allNumericalBucketDPScoreTripleLst))
      
