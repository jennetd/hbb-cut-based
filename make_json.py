# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import json
import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

# from AN
def get_xs_an():
    xs = {}

    xs['QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 366800
    xs['QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8'] = 29370
    xs['QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 6524
    xs['QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 1064
    xs['QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 121.5
    xs['QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8'] = 25.42

    xs['QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 366800
    xs['QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 29370
    xs['QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 6524
    xs['QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1064
    xs['QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 121.5
    xs['QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 25.42

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

    xs['GluGluHToBB_M125_13TeV_powheg_pythia8'] = 48.85*5.82E-01
    xs['GluGluHToBB_M125_13TeV_powheg_MINLO_NNLOPS_pythia8'] = 27.8*5.82E-01

    xs['VBFHToBB_M125_13TeV_powheg_pythia8'] = 3.78*5.824E-01

    xs['WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 5.33E-01*(1.-3.*0.108)*5.82E-01
    xs['WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 8.40E-01*(1.-3.*0.108)*5.82E-01

    xs['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 8.839E-01*(1.-3.*0.0335962-0.201030)*5.824E-01
    xs['ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 8.839E-01*5.824E-01*0.201030
    xs['ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 1.23E-01*5.82E-01*0.6991
    xs['ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.824E-01*0.201030

    xs['ttHToBB_M125_13TeV-powheg-pythia8'] = 5.071E-01*5.82E-01

    with open('xsec_an.json', 'w') as outfile:
        json.dump(xs, outfile)

    return 

# returns dictionary of cross sections
def get_xs():
    
    xs = {}

    xs['QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 322600
    xs['QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8'] = 29980
    xs['QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 6334
    xs['QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 1088
    xs['QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 99.11
    xs['QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8'] = 20.23
    
    xs['QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 347700
    xs['QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 32100                                            
    xs['QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 6831                                                    
    xs['QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1207
    xs['QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 119.9
    xs['QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 25.24  

    xs['WJetsToQQ_HT400to600_qc19_3j_13TeV-madgraphMLM-pythia8'] = 315.6
    xs['WJetsToQQ_HT600to800_qc19_3j_13TeV-madgraphMLM-pythia8'] = 68.57
    xs['WJetsToQQ_HT800toInf_qc19_3j_13TeV-madgraphMLM-pythia8'] = 34.9
    xs['ZJetsToQQ_HT400to600_qc19_4j_13TeV-madgraphMLM-pythia8'] = 145.4
    xs['ZJetsToQQ_HT600to800_qc19_4j_13TeV-madgraphMLM-pythia8'] = 34.0
    xs['ZJetsToQQ_HT800toInf_qc19_4j_13TeV-madgraphMLM-pythia8'] = 18.67

    xs['WW_13TeV-pythia8'] = 75.82
    xs['ZZ_13TeV-pythia8'] = 12.14
    xs['WZ_13TeV-pythia8'] = 27.6

    xs['TTToHadronic_13TeV-powheg-pythia8'] = 377.96
    xs['TTToSemiLeptonic_13TeV-powheg-pythia8'] = 365.34

    xs['ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8'] = 67.91
    xs['ST_t-channel_top_4f_inclusiveDecays_13TeV-powheg-madspin-pythia8'] = 113.3
    xs['ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8'] = 34.97
    xs['ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8'] = 34.91

    xs['GluGluHToBB_M125_13TeV_powheg_pythia8'] = 48.85*5.824E-01
    xs['GluGluHToBB_M125_13TeV_powheg_MINLO_NNLOPS_pythia8'] = 16.17

    xs['VBFHToBB_M125_13TeV_powheg_pythia8'] = 3.782*5.824E-01
    
    xs['WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 5.328E-01*(1.-3.*0.108535)*5.824E-01
    xs['WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 8.400E-01*(1.-3.*0.108535)*5.824E-01
    
    xs['ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.824E-01*0.201030
    xs['ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.82E-01*0.6991
    xs['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 8.839E-01*(1.-3.*0.0335962-0.201030)*5.824E-01
    xs['ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 8.839E-01*5.824E-01*0.201030
    
    xs['ttHToBB_M125_13TeV-powheg-pythia8'] = 5.071E-01*5.824E-01

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

    pmap['ttH'] = ['ttHToBB_M125_13TeV-powheg-pythia8']
    pmap['VBF'] = ['VBFHToBB_M125_13TeV_powheg_pythia8']

#    pmap['ggF-powheg'] = ['GluGluHToBB_M125_13TeV_powheg_pythia8']
    pmap['ggF'] = ['GluGluHToBB_M125_13TeV_powheg_MINLO_NNLOPS_pythia8']
    #pmap['ggF-amcnlo'] = ['GluGluHToBB_M125_LHEHpT_250-Inf_13TeV_amcatnloFXFX_pythia8']

    pmap['QCD'] = ['QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
                   'QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                   'QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                   'QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                   'QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    
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
    
    pmap['data'] = ['JetHT']
    pmap['muondata'] = ['SingleMuon']

    # Other 2016 files
    #['DYJetsToQQ_HT180_13TeV-madgraphMLM-pythia8']                                                                 
    #['TT_13TeV-powheg-pythia8'] 

    with open('pmap.json', 'w') as outfile:
        json.dump(pmap, outfile)


# Main method
def main():

    # create json output file with xs from AN
    get_xs_an()

    # create json output file with xs from Martin's file
    get_xs()

    # create json output file with pmap
    get_pmap()

    return

if __name__ == "__main__":
    main()
