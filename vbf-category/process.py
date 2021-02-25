# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import json
import uproot
import awkward1 as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import matplotlib.pyplot as plt

# Main method
def main():

    if len(sys.argv) != 3:
        print("Enter year and index of json listing input files as arguments")
        return 

    year = sys.argv[1]
    index = sys.argv[2]

    from coffea import processor, util, hist
    from boostedhiggs import VBFProcessor

    uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

    p = VBFProcessor(year=year)
    args = {'schema': NanoAODSchema, 'workers': 4}
 
    this_file = 'infiles/'+str(year)+'_'+str(index)+'.json'
    out = processor.run_uproot_job(this_file, 'Events', p, processor.iterative_executor, args, chunksize=10000)

    outfile = 'outfiles/'+str(year)+'_'+str(index)+'.coffea'
    util.save(out, outfile)

    return

if __name__ == "__main__":
    main()
