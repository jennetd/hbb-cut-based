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
#coffeadir_prefix = '/myeosdir/ggf-vbf/outfiles-ddb2/'
coffeadir_prefix = 'outfiles-ddb2/'

# Main method
def main():

    raw = False

    if len(sys.argv) < 3:
        print("Enter year and 0 for data")
        return 

    year = sys.argv[1]
    mconly = int(sys.argv[2])

    if mconly:
        print("Monte Carlo only")
    else:
        print("Data only")

    with open('xsec.json') as f:
        xs = json.load(f)
        
    with open('pmap.json') as f:
        pmap = json.load(f)
            
    indir = "infiles-split/"
    nfiles = len(subprocess.getoutput("ls "+indir+year+"*.json").split())
    outsum = processor.dict_accumulator()

    # Check if pickle exists, remove it if it does
    picklename = str(year)+'/templates-mc.pkl'
    if not mconly:
        picklename = str(year)+'/templates-data.pkl'
    if os.path.isfile(picklename):
        os.remove(picklename)

    nfiles = len(subprocess.getoutput("ls "+indir+year+"*.json").split())

    started = 0
    for n in range(1,nfiles+1):

        data = False

        # Jet HT
        if year == "2016" and n > 221 and n < 464:
            data = True
        if year == "2017" and n > 121 and n < 471:
            data = True
        if year == "2018" and n > 391 and n < 603:
            data = True

        if year == "2016" and n > 554 and n < 762:
            data = True
        if year == "2017" and n > 1131 and n < 1157:
            data = True
        if year == "2018" and n > 1127 and n < 1335:
            data = True

        if data and mconly:
            continue
        if not data and not mconly:
            continue

        with open(indir+year+'_'+str(n)+'.json') as f:
            infiles = json.load(f)

        filename = coffeadir_prefix+year+'/'+year+'_'+str(n)+'.coffea'
        if os.path.isfile(filename):
            out = util.load(filename)

            if started == 0:
                outsum['templates'] = out['templates']
                outsum['sumw'] = out['sumw']
                started += 1
            else:
                outsum['templates'].add(out['templates'])
                outsum['sumw'].add(out['sumw'])

            del out

        else:
            print('Missing file '+str(n),infiles.keys())
            #print("File " + filename + " is missing")
        
    scale_lumi = {k: xs[k] * 1000 *lumis[year] / w for k, w in outsum['sumw'].items()} 

    outsum['templates'].scale(scale_lumi, 'dataset')
    templates = outsum['templates'].group('dataset', hist.Cat('process', 'Process'), pmap)

    del outsum
          
    outfile = open(picklename, 'wb')
    pickle.dump(templates, outfile, protocol=-1)
    outfile.close()

    return

if __name__ == "__main__":

    main()
