# Jennet's plotter for coffea histograms
# March 26, 2021

import uproot3
import numpy as np
from coffea import hist

import matplotlib.pyplot as plt

import mplhep as hep
plt.style.use([hep.style.CMS])

def plot_datamc_muoncr(h, name, title, log=True, blind=False):

    fig = plt.figure()
    plt.suptitle(title)

    ax1 = fig.add_subplot(211)
    plt.subplots_adjust(hspace=0)

    # https://matplotlib.org/stable/gallery/color/named_colors.html                                                       
    labels = ['Higgs','VV','W+jets','Z+jets','QCD','single t','tt']
    mc = ['ttbar','singlet','QCD','Wjets','Zjets','VV',['ZH','WH','ttH','ggF']]                                                     
    colors=['purple','hotpink','gray','deepskyblue','blue','darkorange','gold']

    if log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]                                                                  

    # Plot stacked hist                                                                                                   
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})                              
    # Overlay data                                                                                                            
    hist.plot1d(h.integrate('process','muondata'),error_opts={'marker':'o','color':'k','markersize':5}) 
    labels = ['Process'] + labels + ['Data']

    ax1.get_xaxis().set_visible(False)                                                                                               
    plt.legend(labels=labels,bbox_to_anchor=(1.05, 1), loc='upper left')                                                     

    allweights =  hist.export1d(h.integrate('process','muondata')).numpy()[0] 
    if log:
        ax1.set_yscale('log')
        ax1.set_ylim(0.01,5*np.amax(allweights))                                                                               

    # ratio                                                                                                                   
    ax2 = fig.add_subplot(212)
    hist.plotratio(num=h.integrate('process','muondata'),denom=h.integrate('process',mc),ax=ax2,unc='num',error_opts={'marker':'o','color':'k','markersize':5},guide_opts={})
    ax2.set_ylabel('Ratio')                                                    
    ax2.set_xlim(ax1.get_xlim())

    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

def plot_syst(h, syst, title, name, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax1 = fig.add_subplot(211)
    plt.subplots_adjust(hspace=0)

    nom = h.integrate('systematic','nominal')
    up = h.integrate('systematic',syst+'Up')
    do = h.integrate('systematic',syst+'Down')

    hist.plot1d(nom,line_opts={'color':'black'},error_opts={'color':'black'})
    hist.plot1d(up,line_opts={'color':'blue'},error_opts={'color':'blue'})
    hist.plot1d(do,line_opts={'color':'red'},error_opts={'color':'red'})
    plt.legend(labels=['nominal', syst+' up', syst + ' down'], bbox_to_anchor=(1.05, 1), loc='upper left')

    nom_array = hist.export1d(nom).numpy()[0]
    up_array = hist.export1d(up).numpy()[0]
    do_array = hist.export1d(do).numpy()[0]
    msd = hist.export1d(nom).numpy()[1]

    allweights = np.concatenate([nom_array,up_array,do_array])
    ax1.set_ylim(0.9*np.amin(allweights),1.1*np.amax(allweights))

    # ratio
    up_ratio = np.array([up_array[i]/nom_array[i] for i in range(len(nom_array))])
    do_ratio = np.array([do_array[i]/nom_array[i] for i in range(len(nom_array))])

    np.nan_to_num(up_ratio,copy=False,nan=0,posinf=1)
    np.nan_to_num(do_ratio,copy=False,nan=0,posinf=1)

    ax2 = fig.add_subplot(212)

    ax2.hist(msd[:-1],weights=np.ones(len(up_ratio)),bins=msd,histtype='step',color='gray',linestyle='--')
#    hist.plotratio(num=up,denom=nom,unc='num',error_opts={'color':'blue'},guide_opts={},ax=ax2)
    ax2.hist(x=msd[:-1],weights=up_ratio,bins=msd,histtype='step',color='blue',linewidth=2)
#    hist.plotratio(num=do,denom=nom,unc='num',error_opts={'color':'red'},guide_opts={},ax=ax2)
    ax2.hist(x=msd[:-1],weights=do_ratio,bins=msd,histtype='step',color='red',linewidth=2)

    allweights_ratio = np.concatenate([up_ratio,do_ratio])
    ax2.set_xlim(ax1.get_xlim())

    ratmin = 0
    ratmax = 1
    if np.amin(allweights_ratio) > 0:
        ratmin = 0.95*np.amin(allweights_ratio)
    if np.amax(allweights_ratio) > 1:
        ratmax = 1.05*np.amax(allweights_ratio)
    ax2.set_ylim(ratmin,ratmax)
    ax2.set_ylabel('Ratio')

    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

def plot_mconly_inc(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax = fig.add_subplot(111)

    labels = ['VV','single t','tt','W+jets','Z+jets','QCD']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV']
    colors=['gray','deepskyblue','blue','purple','hotpink','darkorange']

    if log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]

        # https://matplotlib.org/stable/gallery/color/named_colors.html                                                                     
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})

    sig = h.integrate('process',['ggF','VBF','WH','ZH','ttH'])                                                                      
    hist.plot1d(sig,stack=False,line_opts={'color':'green'})

    labels = ['Process'] + labels + ['Higgs']
    plt.legend(labels,bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0,1000000)

    if log:
        ax.set_yscale('log')
        ax.set_ylim(0.01,1000000)

    # save as name                                                                                                                  
    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

def plot_mconly_vbf(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax = fig.add_subplot(111)

    # https://matplotlib.org/stable/gallery/color/named_colors.html                                                             
    labels = ['bkg H', 'VV','single t','tt','W+jets','Z+jets','QCD']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV', ['ttH','WH','ZH','ggF']]
    colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']

    if log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]

    # Plot stacked hist                                                                                                         
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})

    sig = h.integrate('process','VBF')
    hist.plot1d(sig,stack=False,line_opts={'color':'green'})
    labels = labels + ['VBF']
    plt.legend(labels,bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0,1000000)

    if log:
        ax.set_yscale('log')
        ax.set_ylim(0.01,10000000)

    # save as name
    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

def plot_mconly_vh(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax = fig.add_subplot(111)

    labels = ['bkg H', 'VV','single t','tt','W+jets','Z+jets','QCD']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV',['ggF','VBF','ttH']]
    colors=['gray','deepskyblue','blue','purple','hotpink','darkorange','gold']

    if log:
        mc = [x for x in reversed(mc)]
        colors = [x for x in reversed(colors)]
        labels = [x for x in reversed(labels)]

    # https://matplotlib.org/stable/gallery/color/named_colors.html                             
    hist.plot1d(h,order=mc,stack=True,fill_opts={'color':colors,'edgecolor':'black'})

    sig = h.integrate('process',['WH','ZH'])
    hist.plot1d(sig,stack=False,line_opts={'color':'green'})
    plt.legend(['VH']+labels,bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_ylim(0,1000000)

    if log:
        ax.set_yscale('log')
        ax.set_ylim(0.01,1000000)

    # save as name
    png_name = name+'.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')

    
def plot_overlay(h, name, title, log=True):
    fig = plt.figure()
    plt.suptitle(title)

    ax = fig.add_subplot(111)

    labels = ['QCD','W+jets','Z+jets','$t\bar{t}$','single t', 'VV', 'Higgs']
    mc = ['QCD','Wjets','Zjets','ttbar','singlet','VV'] #,['ZH','WH','ttH','ggF']]
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
    ax[1,0].set_xlabel('Jet 2 ' + xtitle)
    ax[1,0].set_ylabel('Jet 1 ' + xtitle)

    png_name = name+'_'+xtitle+'_2d.png'
    plt.savefig(png_name,bbox_inches='tight')

    pdf_name = name+'_'+xtitle+'_2d.pdf'
    plt.savefig(pdf_name,bbox_inches='tight')
