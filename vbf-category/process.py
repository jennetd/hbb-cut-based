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

from distributed import Client
from lpcjobqueue import LPCCondorCluster

# Main method
def main():

    if len(sys.argv) != 2:
        print("Enter year")
        return 

    year = sys.argv[1]

    cluster = LPCCondorCluster(transfer_input_files="boostedhiggs")
    cluster.adapt(minimum=1, maximum=200)
    client = Client(cluster)

    from coffea import processor, util, hist
    from boostedhiggs import VBFProcessor

    infiles=subprocess.getoutput("ls infiles/"+year+"*.json").split()

    for index, this_file in enumerate(infiles):
        print(this_file)

        p = VBFProcessor(year=year)
        args = {'client': client, 'savemetrics':True, 'schema':NanoAODSchema, 'align_clusters':True, 'retries': 1}
        
        print("Waiting for at least one worker...")
        client.wait_for_workers(1)
        out, metrics = processor.run_uproot_job(str(this_file), 'Events', p, processor.dask_executor, args, chunksize=10000)

        print(f"Output: {out}")
        print(f"Metrics: {metrics}")

        outfile = 'outfiles/'+str(year)+'_'+str(index)+'.coffea'
        util.save(out, outfile)

    return

if __name__ == "__main__":
    main()
