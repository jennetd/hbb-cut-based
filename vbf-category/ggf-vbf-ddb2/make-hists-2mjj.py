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

    raw = False

    if len(sys.argv) < 2:
        print("Enter year")
        return
    elif len(sys.argv) == 3:
        if int(sys.argv[2]) > 0:
            raw = True
    elif len(sys.argv) > 3:
        print("Incorrect number of arguments")
        return

    year = sys.argv[1]

    with open('xsec.json') as f:
        xs = json.load(f)
        
    with open('pmap.json') as f:
        pmap = json.load(f)
            
    nfiles = len(subprocess.getoutput("ls infiles-split/"+year+"*.json").split())
    outsum = processor.dict_accumulator()

    # Check if pickle exists
    picklename = 'pickles/'+str(year)+'_templates.pkl'
    if not os.path.isfile(picklename):
        print("You need to create the pickle")
        return

    # Read the histogram from the pickle file
    vbf = pickle.load(open(picklename,'rb')).integrate('region','signal-vbf')
    
    if raw:
        year = year+"-raw"
    if os.path.isfile(year+'/2mjj-signalregion.root'):
        os.remove(year+'/2mjj-signalregion.root')
    fout = uproot3.create(year+'/2mjj-signalregion.root')

    data = ['data','muondata']
    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    print("2 MJJ BINS SR")
    mjjbins = [1000,2000,10000]
    for i,b in enumerate(mjjbins[:-1]):

        for p in data:
            print(p)

            s = "nominal"
            h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["vbf_pass_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
            h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["vbf_fail_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

        for p in mc:
            print(p)

            if year == '2016' and p == 'ggF' and not raw:
                print("Taking shape for 2016 ggF from 2017")
                vbf17 = pickle.load(open('pickles/2017_templates.pkl','rb')).integrate('region','signal-vbf')
                vbf17.scale(lumis['2016']/lumis['2017'])

                for s in systematics:
                    h = vbf17.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                    fout["vbf_pass_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    h = vbf17.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                    fout["vbf_fail_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

            else:
                for s in systematics:
                    h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                    fout["vbf_pass_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                    fout["vbf_fail_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

        for p in ['Wjets','Zjets']:
            print(p)

            for s in systematics:
                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["vbf_pass_mjj"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)
                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["vbf_fail_mjj"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)

                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(1,3)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["vbf_pass_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(1,3)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["vbf_fail_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

    return

if __name__ == "__main__":
    main()
