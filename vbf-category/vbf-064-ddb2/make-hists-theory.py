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

systematics = [
    'PS_weightUp','PS_weightDown',
    'PDF_weightUp','PDF_weightDown',
    'scalevar_7ptUp','scalevar_7ptDown','scalevar_3ptUp','scalevar_3ptDown'
    ]

systematics_Wjets = [
    'W_d2kappa_EWDown','W_d2kappa_EWUp','W_d3kappa_EWDown','W_d3kappa_EWUp',
    'd1K_NLODown','d1K_NLOUp','d1kappa_EWDown','d1kappa_EWUp',
    'd2K_NLODown','d2K_NLOUp','d3K_NLODown','d3K_NLOUp',
    ]

systematics_Zjets = [
    'Z_d2kappa_EWDown','Z_d2kappa_EWUp','Z_d3kappa_EWDown','Z_d3kappa_EWUp',
    'd1K_NLODown','d1K_NLOUp','d1kappa_EWDown','d1kappa_EWUp',
    'd2K_NLODown','d2K_NLOUp','d3K_NLODown','d3K_NLOUp',
    ]

ddbthr = 0.64
coffeadir_prefix = '/myeosdir/vbf-theory/outfiles-ddb2/'

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
    outsum['templates-vbf'].scale(scale_lumi, 'dataset')
    templates = outsum['templates-vbf'].group('dataset', hist.Cat('process', 'Process'), pmap)
          
    outfile = open(picklename, 'wb')
    pickle.dump(templates, outfile, protocol=-1)
    outfile.close()

    del outsum

    # Read the histogram from the pickle file
    vbf = pickle.load(open(picklename,'rb')).integrate('region','signal').integrate('mjj',int_range=slice(1000,4000)).integrate('deta',int_range=slice(3.5,7))
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol').sum('mjj','deta')
    
    print("1 PT BIN SR")
    if os.path.isfile(year+'/1-signalregion-th.root'):
        os.remove(year+'/1-signalregion-th.root')
    fout = uproot3.create(year+'/1-signalregion-th.root')

    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    for p in mc:      
        print(p)
        for s in systematics:
            h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = vbf.sum('pt1','genflavor').integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)
            
    for p in ['Wjets','Zjets']:
        print(p)

        if 'W' in p:
            systematics_boson = systematics + systematics_Wjets
        if 'Z' in p:
            systematics_boson = systematics + systematics_Zjets

        for s in systematics_boson:
            h = vbf.sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"bb_"+s] = hist.export1d(h)
            h = vbf.sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"bb_"+s] = hist.export1d(h)

            h = vbf.sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = vbf.sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)

    fout.close()

    print("2 PT BINS SR")
    ptbins = [450, 550, 1200]
    if os.path.isfile(year+'/2pt-signalregion-th.root'):
        os.remove(year+'/2pt-signalregion-th.root')

    fout = uproot3.create(year+'/2pt-signalregion-th.root')

    for i,b in enumerate(ptbins[:-1]):

        for p in mc: 
            print(p)

            for s in systematics:
                h = vbf.sum('genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = vbf.sum('genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                
        for p in ['Wjets','Zjets']:
            print(p)

            if 'W' in p:
                systematics_boson = systematics + systematics_Wjets
            if 'Z' in p:
                systematics_boson = systematics + systematics_Zjets

            for s in systematics_boson:
                h = vbf.integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["pass_pt"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)
                h = vbf.integrate('genflavor',int_range=slice(3,4)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["fail_pt"+str(i+1)+"_"+p+"bb_"+s] = hist.export1d(h)

                h = vbf.integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = vbf.integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

    fout.close()

    print("MUON CR")
    if os.path.isfile(year+'/muonCR-th.root'):
        os.remove(year+'/muonCR-th.root')
    fout = uproot3.create(year+'/muonCR-th.root')

    for p in mc:
        print(p)
        for s in systematics:
            h = mucr.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = mucr.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)
            
    for p in ['Wjets','Zjets']:
        print(p)

        if 'W' in p:
            systematics_boson = systematics + systematics_Wjets
        if 'Z' in p:
            systematics_boson = systematics + systematics_Zjets

        for s in systematics_boson:
            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"bb_"+s] = hist.export1d(h)
            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(3,4)).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"bb_"+s] = hist.export1d(h)

            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)

    fout.close()

    return

if __name__ == "__main__":
    main()
