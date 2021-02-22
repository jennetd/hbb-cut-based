#!/bin/bash

# set up code
xrdcp root://cmseos.fnal.gov/EOSDIR/coffeaenv.tar.gz .
tar -zxvf coffeaenv.tar.gz
source coffeaenv/bin/activate
xrdcp root://cmseos.fnal.gov/EOSDIR/boostedhiggs.tar.gz .
tar -zxvf boostedhiggs.tar.gz

# copy code
xrdcp root://cmseos.fnal.gov/EOSDIR/SCRIPTNAME .
xrdcp root://cmseos.fnal.gov/EOSDIR/triggers.json .
xrdcp root://cmseos.fnal.gov/EOSDIR/muon_triggers.json .

# make dir for input/output
mkdir infiles
xrdcp root://cmseos.fnal.gov/EOSINDIR/YEAR_SAMPLE.json infiles
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
