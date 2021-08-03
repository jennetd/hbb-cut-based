#!/usr/bin/python  

import os, sys
import subprocess
import json
import uproot3
import awkward as ak
import numpy as np
from coffea import processor, util, hist
import pickle

lumis = {}
lumis['2016'] = 35.9
lumis['2017'] = 41.5
lumis['2018'] = 59.2


systematics = ['nominal',
               'jet_triggerUp','jet_triggerDown','mu_triggerUp','mu_triggerDown',
               'btagWeightUp','btagWeightDown','btagEffStatUp','btagEffStatDown',
               'UESUp','UESDown','JESUp','JESDown','JERUp','JERDown',
               'pileup_weightUp','pileup_weightDown',
               'mu_idweightUp','mu_idweightDown','mu_isoweightUp','mu_isoweightDown',
              ]

ddbthr = 0.64
coffeadir_prefix = '/myeosdir/ggf-vbf/outfiles-ddb2/'

# Main method
def main():

    if len(sys.argv) != 2:
        print("Enter year")
        return 

    year = sys.argv[1]

    with open('xsec.json') as f:
        xs = json.load(f)
        
    with open('pmap.json') as f:
        pmap = json.load(f)
            
    nfiles = len(subprocess.getoutput("ls infiles-split/"+year+"*.json").split())
    outsum = processor.dict_accumulator()

    # Check if pickle exists, remove it if it does
    picklename = 'pickles/'+str(year)+'_templates.pkl'
    if not os.path.isfile(picklename):
        print("You need to create the pickle")
        return
    
    # Read the histogram from the pickle file
    ggf = pickle.load(open(picklename,'rb')).integrate('region','signal-ggf').integrate('mjj',overflow='allnan')
    vbf = pickle.load(open(picklename,'rb')).integrate('region','signal-vbf').integrate('mjj',overflow='allnan')
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol')
    
    if os.path.isfile(year+'/6pt-signalregion.root'):
        os.remove(year+'/6pt-signalregion.root')
    fout = uproot3.create(year+'/6pt-signalregion.root')

    data = ['data','muondata']
    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    print("6 PT BINS ggF SR")
    ptbins = [450, 500, 550, 600, 675, 800, 1200]

    for i,b in enumerate(ptbins[:-1]):

        for p in data:
            print(p)
            s = "nominal"
            
            h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
            h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

        for p in mc:         
            print(p)

            for s in systematics:
                h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)                    

        for p in ['Wjets','Zjets']:
            print(p)

            for s in systematics:
                h = ggf.integrate('mjj','genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_pt"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)
                h = ggf.integrate('mjj','genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_pt"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)

                h = ggf.integrate('mjj','genflavor',int_range=slice(1,3)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = ggf.integrate('mjj','genflavor',int_range=slice(1,3)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

    fout.close()

    return

if __name__ == "__main__":
    main()
