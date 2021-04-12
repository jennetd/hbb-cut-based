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

    labels = ['QCD','W+jets','Z+jets','$t\bar{t}$','single t', 'VV', 'Higgs']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV',['ZH','WH','ttH','ggF']]
    colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']
    
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

def plot_syst(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax1 = fig.add_subplot(211)
    plt.subplots_adjust(hspace=0)

#    labels = ['QCD','W+jets','Z+jets','$t\bar{t}$','single t']#, 'VV', 'Higgs']
#    mc = ['QCD','Wjets','Zjets','ttbar','singlet']#,'VV',['ZH','WH','ttH','ggF']]
#    colors=['gray','deepskyblue','blue','purple','hotpink']#,'darkorange','gold']

    nom = hist.export1d(h.integrate('systematic','nominal')).numpy()
    up = hist.export1d(h.integrate('systematic',name+'Up')).numpy()
    do = hist.export1d(h.integrate('systematic',name+'Down')).numpy()

    hist.plot1d(h.integrate('systematic','nominal'),line_opts={'color':'black'},error_opts={'color':'black'})
#    plt.hist(x=nom[1][:-1],weights=nom[0],bins=nom[1],histtype='step',color='black',linewidth=2)
    plt.hist(x=up[1][:-1],weights=up[0],bins=up[1],histtype='step',color='blue',linewidth=2)
    plt.hist(x=do[1][:-1],weights=do[0],bins=do[1],histtype='step',color='red',linewidth=2)

    plt.legend(labels=['nominal', name+' up', name + ' down'], bbox_to_anchor=(1.05, 1), loc='upper left')

    allweights = np.concatenate((up[0],do[0],nom[0]))
    ax1.set_ylim(0.9*np.amin(allweights),1.1*np.amax(allweights))

    # ratio
    up_ratio = np.array([up[0][i]/nom[0][i] for i in range(len(nom[0]))])
    do_ratio = np.array([do[0][i]/nom[0][i] for i in range(len(nom[0]))])
    ones = np.array([1 for i in range(len(nom[0]))])

    np.nan_to_num(up_ratio,copy=False,nan=0)
    np.nan_to_num(do_ratio,copy=False,nan=0)

    ax2 = fig.add_subplot(212)
    
    plt.hist(x=nom[1][:-1],weights=ones,bins=nom[1],histtype='step',color='black',linewidth=2)
    plt.hist(x=up[1][:-1],weights=up_ratio,bins=up[1],histtype='step',color='blue',linewidth=2)
    plt.hist(x=do[1][:-1],weights=do_ratio,bins=do[1],histtype='step',color='red',linewidth=2)

    allweights_ratio = np.concatenate((up_ratio,do_ratio))
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_ylim(0.95*np.amin(allweights_ratio),1.05*np.amax(allweights_ratio))
    ax2.set_ylabel('Ratio')

def plot_overlay(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax = fig.add_subplot(111)

    labels = ['QCD','W+jets','Z+jets','$t\bar{t}$','single t', 'VV', 'Higgs']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV',['ZH','WH','ttH','ggF']]
    colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']

    if not log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]

    # https://matplotlib.org/stable/gallery/color/named_colors.html                             
    hist.plot1d(h,order=mc,stack=False,fill_opts={'color':colors,'edgecolor':'black'})

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0,1000000)

    if log:
        ax.set_yscale('log')
        ax.set_ylim(0.01,1000000)

    # save as name


def plot_2d(h, xtitle, name, title, log=False):

    fig, ax = plt.subplots(2,2,sharex='col',sharey='row')
    plt.suptitle(title)

    plt.subplots_adjust(hspace=0)
    plt.subplots_adjust(wspace=0)

    if log:
        ax[0,1].set_logy()
        ax[0,1].set_logx()

    xprojection = hist.export1d(h.integrate(xtitle+'1')).numpy()
    yprojection = hist.export1d(h.integrate(xtitle+'2')).numpy()

    bins = yprojection[1]

    ax[1,1].hist(bins[:-1],weights=yprojection[0],bins=bins,
                 histtype='step',orientation='horizontal')
    ax[1,1].set_xlabel('Events')
    ax[0,0].hist(bins[:-1],weights=xprojection[0],bins=bins,
                 histtype='step')
    ax[0,0].set_ylabel('Events')

    X, Y = np.meshgrid(bins[:-1],bins[:-1])
    w = h.values()[()]

    ax[1,0].hist2d(X.flatten(),Y.flatten(),weights=w.flatten(),bins=bins)
    ax[1,0].set_xlabel('Jet 1 ' + xtitle)
    ax[1,0].set_ylabel('Jet 2 ' + xtitle)


#    hist.plot1d(h.integrate(xtitle+'1'),ax=ax[1,1])
#    hist.plot1d(h.integrate(xtitle+'2'),ax=ax[0,0])

