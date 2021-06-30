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

#    cluster = LPCCondorCluster(transfer_input_files="boostedhiggs")
#    cluster.adapt(minimum=1, maximum=200)
#    client = Client(cluster)

    from coffea import processor, util, hist
    from boostedhiggs import VHProcessor

    infiles=subprocess.getoutput("ls infiles-split/"+year+"_"+str(index)+".json").split()

    uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

    for this_file in infiles:
        print(this_file)

        p = VHProcessor(year=year,jet_arbitration='ddcvb',btagV2=True)
#        args = {'client': client, 'savemetrics':True, 'schema':NanoAODSchema, 'align_clusters':True, 'retries': 1}
        args = {'savemetrics':True, 'schema':NanoAODSchema, 'retries': 1}
        
#        print("Waiting for at least one worker...")
#        client.wait_for_workers(1)
#        out, metrics = processor.run_uproot_job(str(this_file), 'Events', p, processor.dask_executor, args, chunksize=10000)

        out, metrics = processor.run_uproot_job(str(this_file), 'Events', p, processor.futures_executor, args, chunksize=10000) 

        print(f"Output: {out}")
        print(f"Metrics: {metrics}")

        outfile = 'outfiles/'+str(year)+'_'+str(index)+'.coffea'
        util.save(out, outfile)

    return

if __name__ == "__main__":
    main()
