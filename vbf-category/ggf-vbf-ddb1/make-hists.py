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
lumis['2018'] = 59.9

systematics = ['nominal',
               'jet_triggerUp','jet_triggerDown',
               'btagWeightUp','btagWeightDown','btagEffStatUp','btagEffStatDown',
               'UESUp','UESDown','JESUp','JESDown','JERUp','JERDown',
               'pileup_weightUp','pileup_weightDown'
              ]

ddbthr = 0.89
coffeadir_prefix = '/myeosdir/ggf-vbf/outfiles/'

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
    if os.path.isfile(picklename):
        os.remove(picklename)

    nfiles = len(subprocess.getoutput("ls infiles-split/"+year+"*.json").split())
    for n in range(1,nfiles+1):

        with open('infiles-split/'+year+'_'+str(n)+'.json') as f:
            infiles = json.load(f)
    
        filename = coffeadir_prefix+year+'_'+str(n)+'.coffea'
        if os.path.isfile(filename):
            out = util.load(filename)
            outsum.add(out)
        else:
            print('Missing file '+str(n),infiles.keys())
            #print("File " + filename + " is missing")
        
    scale_lumi = {k: xs[k] * 1000 *lumis[year] / w for k, w in outsum['sumw'].items()} 
    outsum['templates'].scale(scale_lumi, 'dataset')
    print(outsum['templates'].identifiers('dataset'))
    templates = outsum['templates'].group('dataset', hist.Cat('process', 'Process'), pmap)
          
    outfile = open(picklename, 'wb')
    pickle.dump(templates, outfile, protocol=-1)
    outfile.close()

    # Read the histogram from the pickle file
    ggf = pickle.load(open(picklename,'rb')).integrate('region','signal-ggf')
    vbf = pickle.load(open(picklename,'rb')).integrate('region','signal-vbf')
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol')
    
    print("1 PT BIN SR")
    if os.path.isfile(year+'/1-signalregion.root'):
        os.remove(year+'/1-signalregion.root')
    fout = uproot3.create(year+'/1-signalregion.root')

    for p in pmap.keys():  
        if 'VBF_' in p or 'WH_' in p or 'ZH_' in p:
            continue
    
        print(p)
        if "data" in p:
            s = "nominal"
            h = vbf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["vbf_pass_"+p+"_"+s] = hist.export1d(h)
            h = vbf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["vbf_fail_"+p+"_"+s] = hist.export1d(h)
            
            h = ggf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["ggf_pass_"+p+"_"+s] = hist.export1d(h)
            h = ggf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["ggf_fail_"+p+"_"+s] = hist.export1d(h)
            
        else:
            for s in systematics:
                h = vbf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["vbf_pass_"+p+"_"+s] = hist.export1d(h)
                h = vbf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["vbf_fail_"+p+"_"+s] = hist.export1d(h)
                
                h = ggf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_"+p+"_"+s] = hist.export1d(h)
                h = ggf.sum('pt1').integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_"+p+"_"+s] = hist.export1d(h)
                
    fout.close()

    print("2 PT BINS SR")
    ptbins = [450, 550, 1200]
    if os.path.isfile(year+'/2pt-signalregion.root'):
        os.remove(year+'/2pt-signalregion.root')

    fout = uproot3.create(year+'/2pt-signalregion.root')

    for i,b in enumerate(ptbins[:-1]):
        for p in pmap.keys(): 
            if 'VBF_' in p or 'WH_' in p or 'ZH_' in p:
                continue
        
            print(p)
            if "data" in p:
                s = "nominal"
                h = vbf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["vbf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = vbf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["vbf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                
                h = ggf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = ggf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                
            else:
                for s in systematics:
                    h = vbf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                    fout["vbf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    h = vbf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                    fout["vbf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    
                    h = ggf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                    fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    h = ggf.integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                    fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                    
    fout.close()

    print("MUON CR")
    if os.path.isfile(year+'/muonCR.root'):
        os.remove(year+'/muonCR.root')
    fout = uproot3.create(year+'/muonCR.root')

    for p in pmap.keys():  
        if 'VBF_' in p or 'WH_' in p or 'ZH_' in p:
            continue
            
        print(p)
        if "data" in p:
            s = "nominal"
            h = mucr.integrate('systematic',s).sum('pt1').integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = mucr.integrate('systematic',s).sum('pt1').integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)
        else:
            for s in systematics:
                h = mucr.integrate('systematic',s).sum('pt1').integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["pass_"+p+"_"+s] = hist.export1d(h)
                h = mucr.integrate('systematic',s).sum('pt1').integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["fail_"+p+"_"+s] = hist.export1d(h)
    
    fout.close()

    return

if __name__ == "__main__":
    main()
