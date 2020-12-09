# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import json
import uproot
import awkward as ak
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
    from boostedhiggs import HbbProcessor

    p = HbbProcessor(year=year)
    args = {'nano': True, 'workers': 4, 'savemetrics': True}
 
    this_file = 'infiles/'+str(year)+'_'+str(index)+'.json'
    out, metrics = processor.run_uproot_job(this_file, 'Events', p, processor.futures_executor, args, chunksize=50000)

    outfile = 'outfiles/'+str(year)+'_'+str(index)+'.coffea'
    util.save(out, outfile)

    return

if __name__ == "__main__":
    main()
