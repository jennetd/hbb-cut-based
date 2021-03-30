#!/bin/bash

# make dir for input/output
mkdir infiles
xrdcp root://cmseos.fnal.gov/EOSIN/YEAR_SAMPLE.json infiles
mkdir outfiles

# run code
python SCRIPTNAME YEAR SAMPLE

#move output to eos
xrdcp -f outfiles/*.coffea EOSOUT
