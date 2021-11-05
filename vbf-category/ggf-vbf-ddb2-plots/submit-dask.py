import os, sys
import subprocess
import json
import uproot
import awkward as ak

from coffea import processor, util, hist
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
from boostedhiggs import HbbPlotProcessor

from distributed import Client
from lpcjobqueue import LPCCondorCluster

from dask.distributed import performance_report
from dask_jobqueue import HTCondorCluster, SLURMCluster

env_extra = [
    f"export PYTHONPATH=$PYTHONPATH:{os.getcwd()}",
]

cluster = LPCCondorCluster(transfer_input_files=["boostedhiggs"],ship_env=True,memory="4GB")
cluster.adapt(minimum=1, maximum=10)
client = Client(cluster)

print("Waiting for at least one worker...")  # noqa
client.wait_for_workers(1)

year = sys.argv[1]

with performance_report(filename="dask-report.html"):

    # get list of input files                                                                                                 
    infiles = subprocess.getoutput("ls "+year+"_all.json").split()

    for this_file in infiles:
        index = this_file.split("_")[1].split(".json")[0]
        print(this_file, index)

        uproot.open.defaults["xrootd_handler"] = uproot.source.xrootd.MultithreadedXRootDSource

        p = HbbPlotProcessor(year=year,tagger='v2')
        args = {'savemetrics':True, 'schema':NanoAODSchema}

        output = processor.run_uproot_job(
            this_file,
            treename="Events",
            processor_instance=p,
            executor=processor.dask_executor,
            executor_args={
                "client": client,
                #            "skipbadfiles": args.skipbadfiles,
                "schema": processor.NanoAODSchema,
                "retries": 50,
            },
            chunksize=100000,
            #        maxchunks=args.max,
        )

        outfile = 'outfiles/'+str(year)+'_dask_'+index+'.coffea'
        util.save(output, outfile)
    

