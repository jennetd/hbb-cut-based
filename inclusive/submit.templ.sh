#!/bin/bash

# make dir for input/output
mkdir infiles-split
xrdcp root://cmseos.fnal.gov/EOSIN/YEAR_SAMPLE.json infiles-split
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
