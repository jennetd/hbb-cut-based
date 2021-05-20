#!/bin/bash

# make sure this is installed
python3 -m pip install correctionlib==2.0.0rc6

# make dir for input/output
mkdir infiles-split
xrdcp root://cmseos.fnal.gov/EOSIN/YEAR_SAMPLE.json infiles-split
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
