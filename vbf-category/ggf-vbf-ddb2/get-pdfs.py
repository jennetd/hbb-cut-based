# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import subprocess
import json
import uproot
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import matplotlib.pyplot as plt

#from distributed import Client
#from lpcjobqueue import LPCCondorCluster

# Main method
def main():

    if len(sys.argv) != 2:
        print("Enter year")
        return 

    year = sys.argv[1]

    from coffea import processor, util, hist
    from boostedhiggs import HbbPDFProcessor

    infiles0=subprocess.getoutput("ls infiles-split/"+year+"_*.json").split()

    for this_file in infiles:
        print(this_file)

        p = HbbPDFProcessor(year=year)
        args = {'savemetrics':True, 'schema':NanoAODSchema}

        processor.run_uproot_job(str(this_file), 'Events', p, processor.futures_executor, args, chunksize=10000)


    return

if __name__ == "__main__":
    main()
