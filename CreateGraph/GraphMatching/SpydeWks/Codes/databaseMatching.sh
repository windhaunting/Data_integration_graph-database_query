#!/bin/bash

INPUTDATADIR=/home/fubao/Fubao/CiscoWish/data/test
RANGEDIFFTHRESHOLD=1.5
BUCKETSIZENUM=200000
OUTPUTNUMERICALRES=/home/fubao/Fubao/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/numericalOutput

NONNUMPREFIXLENGTH=2
NONSAMPLERECORDNUM=20
RECORDPAIRSIMITHRESHOLD=0.5
OUTPUTNONNUMDIR=/home/fubao/Fubao/CiscoWish/CreateGraph/GraphMatching/SpydeWks/Codes/output/nonNumericalOutput
INTERMEDIATEOUTFLAG=True

echo "Start Database Matching..."
python3 mainEntry.py -i $INPUTDATADIR -rdt $RANGEDIFFTHRESHOLD -bs $BUCKETSIZENUM -oNum $OUTPUTNUMERICALRES  -pl $NONNUMPREFIXLENGTH -spNum $NONSAMPLERECORDNUM -recsimt $RECORDPAIRSIMITHRESHOLD -oNonDir $OUTPUTNONNUMDIR -interOFlg $INTERMEDIATEOUTFLAG
echo "End"


