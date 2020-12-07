# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import json
import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

# returns dictionary of cross sections
def get_xs():
    
    xs = {}

    xs['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 8.839E-01*(1.-3.*0.0335962-0.201030)*5.824E-01
    xs['ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 8.839E-01*5.824E-01*0.201030
    xs['ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 1.23E-01*5.82E-01*0.6991
    xs['ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.824E-01*0.201030
    xs['GluGluHToBB_M125_13TeV_powheg_pythia8'] = 48.85*5.82E-01
    xs['VBFHToBB_M-125_13TeV_powheg_pythia8'] = 3.78*5.824E-01
    xs['WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 5.33E-01*(1.-3.*0.108)*5.82E-01
    xs['WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 8.40E-01*(1.-3.*0.108)*5.82E-01
    xs['ttHTobb_M125_13TeV-powheg-pythia8'] = 5.071E-01*5.82E-01
    xs['GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8'] = 27.8*5.82E-01
    xs['GluGluHToBB_M125_LHEHpT_250-Inf_13TeV_amcatnloFXFX_pythia8'] = xs['GluGluHToBB_M125_13TeV_powheg_pythia8']

    xs['QCD_HT500to700_13TeV-madgraphMLM-pythia8'] = 29370
    xs['QCD_HT700to1000_13TeV-madgraphMLM-pythia8'] = 6524
    xs['QCD_HT1000to1500_13TeV-madgraphMLM-pythia8'] = 1064
    xs['QCD_HT1500to2000_13TeV-madgraphMLM-pythia8'] = 121.5
    xs['QCD_HT2000toInf_13TeV-madgraphMLM-pythia8'] = 25.42

    xs['WJetsToQQ_HT400to600_qc19_3j_13TeV-madgraphMLM-pythia8'] = 315.6
    xs['WJetsToQQ_HT600to800_qc19_3j_13TeV-madgraphMLM-pythia8'] = 68.57
    xs['WJetsToQQ_HT800toInf_qc19_3j_13TeV-madgraphMLM-pythia8'] = 34.9
    xs['ZJetsToQQ_HT400to600_qc19_4j_13TeV-madgraphMLM-pythia8'] = 145.4
    xs['ZJetsToQQ_HT600to800_qc19_4j_13TeV-madgraphMLM-pythia8'] = 34.0
    xs['ZJetsToQQ_HT800toInf_qc19_4j_13TeV-madgraphMLM-pythia8'] = 18.67
    xs['WW_13TeV-pythia8'] = 63.21
    xs['ZZ_13TeV-pythia8'] = 10.32
    xs['WZ_13TeV-pythia8'] = 22.82
    
    xs['TTToHadronic_13TeV-powheg-pythia8'] = 377.96
    xs['TTToSemiLeptonic_13TeV-powheg-pythia8'] = 365.34
    xs['ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8'] = 80.95
    xs['ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8'] = 136.02
    xs['ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8'] = 34.91
    xs['ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8'] = 34.91
    xs['TTToHadronic_PSweights_13TeV_powheg_pythia8'] = 313.9

    # 2016 only
    xs['TT_13TeV-powheg-pythia8'] = 831.76
    xs['WJetsToQQ_HT180_13TeV-madgraphMLM-pythia8'] = 2788
    xs['DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8'] = 1187

    with open('xsec.json', 'w') as outfile:
        json.dump(xs, outfile)

    return

def get_pmap():
    pmap = {}

    pmap['ZH'] = ['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8',
                  'ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',
                  'ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8',
                  'ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',]

    pmap['WH'] = ['WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8',
                  'WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8',]

    pmap['ttH'] = ['ttHTobb_M125_13TeV-powheg-pythia8']
    pmap['VBF'] = ['VBFHToBB_M-125_13TeV_powheg_pythia8']

    #pmap['ggF-powheg'] = ['GluGluHToBB_M125_13TeV_powheg_pythia8']
    pmap['ggF'] = ['GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8']
    #pmap['ggF-amcnlo'] = ['GluGluHToBB_M125_LHEHpT_250-Inf_13TeV_amcatnloFXFX_pythia8']

    pmap['QCD'] = ['QCD_HT500to700_13TeV-madgraphMLM-pythia8',
                   'QCD_HT700to1000_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1000to1500_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1500to2000_13TeV-madgraphMLM-pythia8',
                   'QCD_HT2000toInf_13TeV-madgraphMLM-pythia8',
                   'QCD_HT500to700_13TeV-madgraphMLM-pythia8',
                   'QCD_HT700to1000_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1000to1500_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1500to2000_13TeV-madgraphMLM-pythia8',
                   'QCD_HT2000toInf_13TeV-madgraphMLM-pythia8',]
    
    pmap['VV'] = ['WW_13TeV-pythia8',
                  'ZZ_13TeV-pythia8',
                  'WZ_13TeV-pythia8',]
    
    pmap['Wjets'] = ['WJetsToQQ_HT800toInf_qc19_3j_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT400to600_qc19_3j_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT600to800_qc19_3j_13TeV-madgraphMLM-pythia8',]
    
    pmap['Zjets'] = ['ZJetsToQQ_HT800toInf_qc19_4j_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT400to600_qc19_4j_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT600to800_qc19_4j_13TeV-madgraphMLM-pythia8',]
    
    pmap['ttbar'] = ['TTToHadronic_13TeV-powheg-pythia8',
                     'TTToSemiLeptonic_13TeV-powheg-pythia8',]
    
    pmap['singlet'] = ['ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8',
                       'ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8',
                       'ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8',
                       'ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8',]
    
    # Other 2016 files
    #['DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8']                                                                 
    #['TT_13TeV-powheg-pythia8'] 

    with open('pmap.json', 'w') as outfile:
        json.dump(pmap, outfile)


# Main method
def main():

    # create json output file with xs
    get_xs()

    # create json output file with pmap
    get_pmap()

    return

if __name__ == "__main__":
    main()
