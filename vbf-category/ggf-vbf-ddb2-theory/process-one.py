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

    if len(sys.argv) != 3:
        print("Enter year and index")
        return 

    year = sys.argv[1]
    index = sys.argv[2]

    from coffea import processor, util, hist
    from boostedhiggs import HbbTheoryProcessor

    infiles=subprocess.getoutput("ls infiles-split/"+year+"_"+str(index)+".json").split()

    uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

    for this_file in infiles:
        print(this_file)

        p = HbbTheoryProcessor(year=year,tagger='v2')
        args = {'savemetrics':True, 'schema':NanoAODSchema, 'retries': 1}
        
        out, metrics = processor.run_uproot_job(str(this_file), 'Events', p, processor.futures_executor, args, chunksize=10000) 
        print(f"Output: {out}")
        print(f"Metrics: {metrics}")

        outfile = 'outfiles/'+str(year)+'_'+str(index)+'.coffea'
        util.save(out, outfile)

    return

if __name__ == "__main__":
    main()
