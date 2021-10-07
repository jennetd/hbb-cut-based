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
    'nominal',
    'jet_triggerUp','jet_triggerDown','mu_triggerUp','mu_triggerDown',
    'btagWeightUp','btagWeightDown','btagEffStatUp','btagEffStatDown',
    'UESUp','UESDown','JESUp','JESDown','JERUp','JERDown',
    'pileup_weightUp','pileup_weightDown',
    'mu_idweightUp','mu_idweightDown','mu_isoweightUp','mu_isoweightDown',
    'UEPS_ISRUp','UEPS_ISRDown','UEPS_FSRUp','UEPS_FSRDown',
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
coffeadir_prefix = 'outfiles-ddb2/'

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

    global systematics
    if year == "2016" or year == "2017":
        systematics += ['L1PrefiringUp','L1PrefiringDown']

    with open('xsec.json') as f:
        xs = json.load(f)

    with open('pmap.json') as f:
        pmap = json.load(f)

    nfiles = len(subprocess.getoutput("ls infiles-split/"+year+"*.json").split())
    outsum = processor.dict_accumulator()

    data = ['data','muondata']
    mc = ['QCD','ttbar','singlet','VV','ggF','VBF','WH','ZH','ttH']

    print("MUON CR")
    if os.path.isfile(year+'/muonCR.root'):
        os.remove(year+'/muonCR.root')
    fout = uproot3.create(year+'/muonCR.root')

    # Check if pickle exists                                                                                                                                             
    picklename = year+'/templates-data.pkl'
    if not os.path.isfile(picklename):
        print("You need to create the pickle")
        return

    # Read the histogram from the pickle file                                                                                                                            
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol').integrate('mjj',overflow='allnan')

    for p in data:
        print(p)
        s = "nominal"
        h = mucr.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
        fout["pass_"+p+"_"+s] = hist.export1d(h)
        h = mucr.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
        fout["fail_"+p+"_"+s] = hist.export1d(h)

    # Check if pickle exists                                                                                                                                             
    picklename = year+'/templates-mc.pkl'
    if not os.path.isfile(picklename):
        print("You need to create the pickle")
        return

    # Read the histogram from the pickle file                                                                                                               
    mucr = pickle.load(open(picklename,'rb')).integrate('region','muoncontrol').integrate('mjj',overflow='allnan')
    print(mucr.identifiers('systematic'))

    for p in mc:
        print(p)
        if year == '2016' and p == 'ggF' and not raw:
            print("Taking shape for 2016 ggF from 2017")
            mucr17 = pickle.load(open('2017/templates-mc.pkl','rb')).integrate('region','muoncontrol').integrate('mjj',overflow='allnan')
            mucr17.scale(lumis['2016']/lumis['2017'])

            for s in systematics:
                h = mucr17.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
                fout["pass_"+p+"_"+s] = hist.export1d(h)
                h = mucr17.integrate('systematic',s).sum('pt1','genflavor').integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
                fout["fail_"+p+"_"+s] = hist.export1d(h)
        else:
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

            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(1,3)).integrate('ddb1',int_range=slice(ddbthr,1)).integrate('process',p)
            fout["pass_"+p+"_"+s] = hist.export1d(h)
            h = mucr.integrate('systematic',s).sum('pt1').integrate('genflavor',int_range=slice(1,3)).integrate('ddb1',int_range=slice(0,ddbthr)).integrate('process',p)
            fout["fail_"+p+"_"+s] = hist.export1d(h)

    fout.close()

    return

if __name__ == "__main__":

    main()