# Run Jennet's (Nick's) processor on Higgs signal

#!/usr/bin/python

import os, sys
import json
import uproot
import awkward as ak
import numpy as np
import matplotlib.pyplot as plt

def get_muontriggers():
    muontriggers = {
        '2016': [ 'Mu50', 'TkMu50' ],
        '2017': [ 'Mu50', 'OldMu100', 'TkMu100'],
        '2018': [ 'Mu50', 'OldMu100', 'TkMu100' ],
    }

    with open('muon_triggers.json', 'w') as outfile:
        json.dump(muontriggers, outfile)

    return

def get_triggers():
    triggers = {
        '2016': [
            'PFHT800',
            'PFHT900',
            'AK8PFJet360_TrimMass30',
            'AK8PFHT700_TrimR0p1PT0p03Mass50',
            'PFHT650_WideJetMJJ950DEtaJJ1p5',
            'PFHT650_WideJetMJJ900DEtaJJ1p5',
            'AK8DiPFJet280_200_TrimMass30_BTagCSV_p20',
            'PFJet450',
        ],
        '2017': [
            'AK8PFJet330_PFAK8BTagCSV_p17',
            'PFHT1050',
            'AK8PFJet400_TrimMass30',
#            'AK8PFJet420_TrimMass30',
            'AK8PFHT800_TrimMass50',
            'PFJet500',
            'AK8PFJet500',
        ],
        '2018': [
            'AK8PFJet400_TrimMass30',
#            'AK8PFJet420_TrimMass30',
            'AK8PFHT800_TrimMass50',
            'PFHT1050',
            'PFJet500',
            'AK8PFJet500',
            'AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4',
        ],
    }

    with open('triggers.json', 'w') as outfile:
        json.dump(triggers, outfile)

    return
    
# from Martin
def get_xs():
    # Cross sections in pb
    xs = {}

    # QCD 2016 tune
#    xs['QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 2.486e+08
#    xs['QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 27990000.0
#    xs['QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1712000
#    xs['QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 347300
    xs['QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 32200
    xs['QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 6839
    xs['QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1207
    xs['QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 120.1
    xs['QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 25.24

    # QCD 2017/2018 tune
    xs['QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8'] = 322600 
    xs['QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8'] = 29980 
    xs['QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 6334 
    xs['QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 1088 
    xs['QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8'] = 99.11 
    xs['QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8'] = 20.23 

    # WJetsToQQ 2016 tune
    xs['WJetsToQQ_HT400to600_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 269.90
    xs['WJetsToQQ_HT600to800_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 59.52
    xs['WJetsToQQ_HT-800toInf_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 30.17

    # WJetsToQQ 2017/2018 tune 
    xs['WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 314.90
    xs['WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 68.64
    xs['WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 34.70

    # ZJetsToQQ 2016 tune
    xs['ZJetsToQQ_HT400to600_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 116.70
    xs['ZJetsToQQ_HT600to800_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 27.37
    xs['ZJetsToQQ_HT-800toInf_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 15.01

    # ZJetsToQQ 2017/2018 tune
    xs['ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 144.70
    xs['ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 34.06                    
    xs['ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8'] = 18.57

    # WJetsToLNu 2016 tune
    xs['WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 359.7*1.434
    xs['WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 48.91*1.532
    xs['WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 12.05*1.004
    xs['WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 5.501*1.004
    xs['WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1.329*1.004
    xs['WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 0.03216*1.004

    # WJetsToLNu 2017/2018 tune
    xs['WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8'] = 407.9*1.167
    xs['WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8'] = 57.48*1.167
    xs['WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8'] = 12.87*1.167
    xs['WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8'] = 5.366*1.167
    xs['WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 1.074*1.167
    xs['WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8'] = 0.008001*1.167

    # ZJetsToLL 2016 tune
#    xs['DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 40.99*1.438
    xs['DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 5.678*1.494
    xs['DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 1.367*1.139
    xs['DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 0.6304*1.139
    xs['DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 0.1514*1.139
    xs['DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8'] = 0.003565*1.139

    # ZJetsToLL 2017/2018 tune
#    xs['DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8'] = 48.66*1.137
    xs['DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8'] = 6.968*1.137
    xs['DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8'] = 1.743*1.137 
    xs['DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8'] = 0.8052*1.137
    xs['DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8'] = 0.1933*1.137
    xs['DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8'] = 0.003468*1.137
#    xs['DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 48.66*1.137
    xs['DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 6.968*1.137
    xs['DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 1.743*1.137
    xs['DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 0.8052*1.137
    xs['DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 0.1933*1.137
    xs['DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8'] = 0.003468*1.137
    
    # ttbar 
    xs['TTToHadronic_TuneCP5_13TeV_powheg_pythia8'] = 377.96
    xs['TTToSemiLeptonic_TuneCP5_13TeV_powheg_pythia8'] = 365.34
    xs['TTTo2L2Nu_TuneCP5_13TeV_powheg_pythia8'] = 88.29
    xs['TTToHadronic_TuneCP5_PSweights_13TeV_powheg_pythia8'] = 377.96
    xs['TTToSemiLeptonic_TuneCP5_PSweights_13TeV_powheg_pythia8'] = 365.34
    xs['TTTo2L2Nu_TuneCP5_PSweights_13TeV_powheg_pythia8'] = 88.29
    
    # single top
    xs['ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-madgraph-pythia8'] = 11.24
    xs['ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8'] = 3.36
    xs['ST_s-channel_4f_hadronicDecays_TuneCP5_PSweights_13TeV-madgraph-pythia8'] = 11.24
    xs['ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8'] = 3.36
    
    xs['ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8'] = 80.95
    xs['ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8'] = 136.02
    xs['ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_PSweights_13TeV-powhegV2-madspin-pythia8'] = 80.95
    xs['ST_t-channel_top_4f_inclusiveDecays_TuneCP5_PSweights_13TeV-powhegV2-madspin-pythia8'] = 136.02
    
    xs['ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8'] = 35.85
    xs['ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8'] = 35.85
    xs['ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8'] = 35.85
    xs['ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8'] = 35.85
    
    # VV
    xs['WW_TuneCP5_13TeV-pythia8'] = 75.90
    xs['WZ_TuneCP5_13TeV-pythia8'] = 27.57
    xs['ZZ_TuneCP5_13TeV-pythia8'] = 12.14 
    
    # Higgs
    xs['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 8.839E-01*(1.-3.*0.0335962-0.201030)*5.824E-01
    xs['ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8'] = 8.839E-01*3.*0.0335962*5.824E-01
    xs['ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 8.839E-01*5.824E-01*0.201030 
    
    xs['GluGluHToBB_M-125_13TeV_powheg_MINLO_NNLOPS_pythia8'] = 2.780e+01
    
    xs['VBFHToBB_M_125_13TeV_powheg_pythia8_weightfix'] = 3.782*5.824E-01
    
    xs['WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 5.328E-01*(1.-3.*0.108535)*5.824E-01
    xs['WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8'] = 8.400E-01*(1.-3.*0.108535)*5.824E-01
    xs['WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8'] = 5.328E-01*(3.*0.108535)*5.824E-01
    xs['WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8'] = 8.400E-01*(3.*0.108535)*5.824E-01
    
    xs['ttHTobb_M125_TuneCP5_13TeV_powheg_pythia8'] = 5.071E-01*5.824E-01
    
    xs['ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.824E-01*0.201030
    xs['ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.82E-01*0.6991
    xs['ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8'] = 1.227E-01*5.824E-01*0.0335962*3.
    
    with open('xsec.json', 'w') as outfile:
        json.dump(xs, outfile)

    return

def get_pmap():
    pmap = {}

    pmap['ZH'] = ['ZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8',
                  'ZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',
                  'ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8',
                  'ggZH_HToBB_ZToQQ_M125_13TeV_powheg_pythia8',
                  'ggZH_HToBB_ZToNuNu_M125_13TeV_powheg_pythia8',
                  'ggZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8,']

    pmap['WH'] = ['WminusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8',
                  'WminusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8',
                  'WplusH_HToBB_WToLNu_M125_13TeV_powheg_pythia8',
                  'WplusH_HToBB_WToQQ_M125_13TeV_powheg_pythia8',]

    pmap['ttH'] = ['ttHToBB_M125_13TeV-powheg-pythia8']
    pmap['VBF'] = ['VBFHToBB_M125_13TeV_powheg_pythia8']

    pmap['ggF'] = ['GluGluHToBB_M125_13TeV_powheg_MINLO_NNLOPS_pythia8']

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
    
    pmap['VV'] = ['WW_TuneCP5_13TeV-pythia8',
                  'ZZ_TuneCP5_13TeV-pythia8',
                  'WZ_TuneCP5_13TeV-pythia8',]
    
    pmap['Wjets'] = ['WJetsToQQ_HT-800toInf_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT400to600_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT600to800_qc19_3j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',                     
                     'WJetsToQQ_HT-800toInf_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT400to600_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToQQ_HT600to800_qc19_3j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-1200To2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-2500ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-600To800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'WJetsToLNu_HT-800To1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    
    pmap['Zjets'] = ['ZJetsToQQ_HT-800toInf_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT400to600_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT600to800_qc19_4j_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT-800toInf_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT400to600_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'ZJetsToQQ_HT600to800_qc19_4j_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',
                     'DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8',]
    
    pmap['ttbar'] = ['TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8',
                     'TTToHadronic_TuneCP5_13TeV-powheg-pythia8',
                     'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8',
                     'TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8',
                     'TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8',
                     'TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8',]
    
    pmap['singlet'] = ['ST_s-channel_4f_leptonDecays_TuneCP5_PSweights_13TeV-amcatnlo-pythia8',
                       'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
                       'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
                       'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
                       'ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8',
                       'ST_s-channel_4f_hadronicDecays_TuneCP5_13TeV-amcatnlo-pythia8',
                       'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8',
                       'ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8',
                       'ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8',
                       'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
                       'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',]

    
    pmap['data'] = ['JetHT']

    pmap['muondata'] = ['SingleMuon']

    with open('pmap.json', 'w') as outfile:
        json.dump(pmap, outfile)


# Main method
def main():

    # create json output file with xs from Martin's file
    get_xs()

    # create json output file with pmap
    get_pmap()

    # create output files with trigger info
    get_triggers()
    get_muontriggers()

    return

if __name__ == "__main__":
    main()
