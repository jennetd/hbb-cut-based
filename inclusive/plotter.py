# Jennet's plotter for coffea histograms
# March 26, 2021

import uproot3
import numpy as np
from coffea import hist

import matplotlib.pyplot as plt

import mplhep as hep
plt.style.use([hep.style.CMS])

def plot_datamc(h, name, title, log=True, blind=False):
    fig = plt.figure()
    plt.suptitle(title)

    ax1 = fig.add_subplot(211)
    plt.subplots_adjust(hspace=0)

    mc = ['QCD','Wjets','ttbar',['ZH','WH']]
    colors = ['gray','deepskyblue','purple','gold']
    labels = ['QCD','W+jets','$t\bar{t}$','Higgs']
    # mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV',['ZH','WH','ttH','ggF']]
    # colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']
    if not log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]

    # https://matplotlib.org/stable/gallery/color/named_colors.html

    # Plot stacked hist
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})
    # Overlay data
    hist.plot1d(h.integrate('process','muondata'),error_opts={'marker':'o','c':'k','markersize':5})

    ax1.get_xaxis().set_visible(False)    
    plt.legend(labels=labels, bbox_to_anchor=(1.05, 1), loc='upper left')

    ax1.set_ylim(0,1000)
    if log:
        ax1.set_yscale('log')
        ax1.set_ylim(0.01,1000)

    # ratio
    ax2 = fig.add_subplot(212)
#    hist.plotratio(num=h.integrate('process','muondata'),denom=h.integrate('process',mc),ax=ax2,error_opts={'marker':'o','c':'k','markersize':5})
    ax2.set_ylabel('Ratio')
    
    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')
    
    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

def plot_vbfcr(h, cuts, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)
    
    sr = h.integrate('region','signal').integrate('deta',int_range=slice(3.5,7)).integrate('mjj',int_range=slice(1000,4000))

    hist.plot1d(sr,line_opts={'color':'black'}, density=True)
     
    cr = h.integrate('region','muoncontrol').integrate('deta',int_range=slice(3,7)).integrate('mjj',int_range=slice(900,4000))

    hist.plot1d(cr,fill_opts={'color':'red'}, density=True)

    return

def plot_onlymc(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    if log:
        mc = ['QCD','Wjets','ttbar',['ZH','WH']]
        colors = ['gray','deepskyblue','purple','gold']

    # https://matplotlib.org/stable/gallery/color/named_colors.html                             
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.set_ylim(0,1000)

    if log:
        plt.set_yscale('log')
        plt.set_ylim(0.01,1000)

    # save as name
