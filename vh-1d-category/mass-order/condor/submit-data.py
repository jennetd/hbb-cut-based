#!/usr/bin/python

import argparse
import os
import re
import fileinput

import json
import glob

script = 'process.py'

loc_base = os.environ['PWD']
logdir = 'logs-data'

tag = 'vh-1d-category/mass-order'
homedir = '/store/user/jennetd/december-2020/'+tag
indir = homedir + '/indata/'
outdir = homedir + '/outdata/'

os.chdir('..')
os.system('xrdcp -rf indata/ root://cmseos.fnal.gov/'+homedir)
os.system('xrdcp -f '+script+' root://cmseos.fnal.gov/'+homedir)
#os.system('tar -zcf boostedhiggs.tar.gz boostedhiggs --exclude="*.root" --exclude="*.pdf" --exclude="*.pyc" --exclude=tmp --exclude="*.tgz" --exclude="*.ipynb" --exclude-vcs --exclude-caches-all')
os.system('xrdcp -f boostedhiggs.tar.gz root://cmseos.fnal.gov/'+homedir)
os.system('xrdcp -f coffeaenv.tar.gz root://cmseos.fnal.gov/'+homedir)
os.chdir(loc_base)

################################################
### Where is your list of root files to run over
################################################

#make local directory
locdir = logdir
os.system('mkdir -p  %s' %locdir)

print('CONDOR work dir: ' + homedir)

os.system('mkdir -p /eos/uscms'+outdir)

nsubmit = 0

nfiles = {}
nfiles['2016'] = 16
nfiles['2017'] = 19
nfiles['2018'] = 27

for year in ['2016','2017','2018']:
    for f in range(1,nfiles[year]+1):

        prefix = year+'_'+str(f)
        print('Submitting '+prefix)

        condor_templ_file = open(loc_base+"/submit.templ.condor")
        sh_templ_file    = open(loc_base+"/submit.templ.sh")
    
        localcondor = locdir+'/'+prefix+".condor"
        condor_file = open(localcondor,"w")
        for line in condor_templ_file:
            line=line.replace('DIRECTORY',locdir)
            line=line.replace('PREFIX',prefix)
            condor_file.write(line)
        condor_file.close()
    
        #copy local to eos
        #os.system('xrdcp -f %s %s' % (localcondor,eoscondor))
        #remove local copy
        #os.system('rm %s' % localcondor)
    
        localsh=locdir+'/'+prefix+".sh"
        eosoutput="root://cmseos.fnal.gov/"+outdir+"/"+prefix+'.coffea'
        sh_file = open(localsh,"w")
        for line in sh_templ_file:
            line=line.replace('SCRIPTNAME',script)
            line=line.replace('YEAR',year)
            line=line.replace('SAMPLE',str(f))
            line=line.replace('EOSDIR',homedir)
            line=line.replace('EOSINDIR',indir)
            line=line.replace('EOSOUT',eosoutput)
            sh_file.write(line)
        sh_file.close()

        os.system('chmod u+x '+locdir+'/'+prefix+'.sh')

        if (os.path.exists('%s.log'  % localcondor)):
            os.system('rm %s.log' % localcondor)
        os.system('condor_submit %s' % localcondor)

        condor_templ_file.close()
        sh_templ_file.close()

        nsubmit = nsubmit + 1

print(nsubmit,"jobs submitted.")

