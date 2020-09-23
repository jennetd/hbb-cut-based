#!/bin/bash

# set up code
source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-centos7-gcc8-opt/setup.sh
source /cvmfs/cms.cern.ch/cmsset_default.sh

# copy code
xrdcp root://cmseos.fnal.gov//store/user/jennetd/september-2020/boostedhiggs.tar.gz .
tar -zxvf boostedhiggs.tar.gz 
xrdcp -f root://cmseos.fnal.gov//store/user/jennetd/september-2020/SCRIPTNAME .

# make dir for output
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
