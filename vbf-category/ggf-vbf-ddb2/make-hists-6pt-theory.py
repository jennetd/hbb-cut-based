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

    picklename = 'pickles/'+str(year)+'_templates-th.pkl'
    if not os.path.isfile(picklename):
        print("You need to create the pickle")
        return

    # Read the histogram from the pickle file
    ggf = pickle.load(open(picklename,'rb')).integrate('region','signal-ggf').integrate('mjj',overflow='allnan')
    
    if os.path.isfile(year+'/6pt-signalregion-th.root'):
        os.remove(year+'/6pt-signalregion-th.root')
    fout = uproot3.create(year+'/6pt-signalregion-th.root')

    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    print("6 PT BINS ggF SR")
    ptbins = [450, 500, 550, 600, 675, 800, 1200]

    for i,b in enumerate(ptbins[:-1]):

        for p in mc:         
            print(p)

            for s in systematics:
                h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["ggf_pass_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)
                h = ggf.sum('mjj','genflavor').integrate('systematic',s).integrate('pt1',int_range=slice(ptbins[i],ptbins[i+1])).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["ggf_fail_pt"+str(i+1)+"_"+p+"_"+s] = hist.export1d(h)                    

        for p in ['Wjets','Zjets']:
            print(p)
            
            if 'W' in p:
                systematics_boson = systematics + systematics_Wjets
            if 'Z' in p:
                systematics_boson = systematics + systematics_Zjets

            for s in systematics_boson:
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
