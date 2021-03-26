# Jennet's plotter for coffea histograms
# March 26, 2021

import uproot3
import numpy as np
from coffea import hist

import matplotlib.pyplot as plt

import mplhep as hep
plt.style.use([hep.style.CMS])

def plotter_1d(h, name, title, log=True, blind=False):
    fig = plt.figure()
    plt.suptitle(title)

    ax1 = fig.add_subplot(211)
    plt.subplots_adjust(hspace=0)

    if log:
        mc = ['QCD','Wjets','ttbar',['ZH','WH']]
        colors = ['gray','deepskyblue','purple','gold']
        # mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV',['ZH','WH','ttH','ggF']]
        # colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']

    # https://matplotlib.org/stable/gallery/color/named_colors.html
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})
    #data = hist.export1d(h.integrate('process','muondata')).numpy()
    #print(data)
    #ax1.plot(data[1][:-1],data[0])
    hist.plot1d(h.integrate('process','muondata'),error_opts={'marker':'o','c':'k','markersize':5})
    ax1.get_xaxis().set_visible(False)
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

    ax1.set_ylim(0,1000)
    if log:
        ax1.set_yscale('log')
        ax1.set_ylim(0.01,1000)

    # ratio
    ax2 = fig.add_subplot(212)
    hist.plotratio(num=h.integrate('process','muondata'),denom=h.integrate('process',mc),ax=ax2,error_opts={'marker':'o','c':'k','markersize':5})
    ax2.set_ylabel('Ratio')
    
    # Save as name
