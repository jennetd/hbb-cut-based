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
coffeadir_prefix = '/myeosdir/ggf-vbf-theory/outfiles-ddb2/'

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
    templates = outsum['templates'].group('dataset', hist.Cat('process', 'Process'), pmap)
          
    outfile = open(picklename, 'wb')
    pickle.dump(templates, outfile, protocol=-1)
    outfile.close()

    # Read the histogram from the pickle file
    ggf = pickle.load(open(picklename,'rb')).integrate('region','signal-ggf')
    vbf = pickle.load(open(picklename,'rb')).integrate('region','signal-vbf')
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol')
    
    if os.path.isfile(year+'/2mjj-signalregion.root'):
        os.remove(year+'/2mjj-signalregion.root')
    fout = uproot3.create(year+'/2mjj-signalregion.root')

    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    print("2 MJJ BINS SR")
    mjjbins = [1000,2000,4000]
    for i,b in enumerate(mjjbins[:-1]):

        for p in mc:
            print(p)

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

                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["vbf_pass_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = vbf.sum('pt1').integrate('genflavor',int_range=slice(0,3)).integrate('systematic',s).integrate('mjj',int_range=slice(mjjbins[i],mjjbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["vbf_fail_mjj"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)

    return

if __name__ == "__main__":
    main()
