#!/bin/bash

# set up code
xrdcp root://cmseos.fnal.gov/EOSDIR/coffeaenv.tar.gz .
tar -zxvf coffeaenv.tar.gz
source coffeaenv/bin/activate

# copy code
xrdcp root://cmseos.fnal.gov/EOSDIR/boostedhiggs.tar.gz .
tar -zxvf boostedhiggs.tar.gz 
xrdcp root://cmseos.fnal.gov/EOSDIR/SCRIPTNAME .

# make dir for input/output
mkdir infiles
xrdcp root://cmseos.fnal.gov/EOSINDIR/YEAR_SAMPLE.json infiles
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
