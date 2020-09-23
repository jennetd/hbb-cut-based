#!/usr/bin/python

import argparse
import os
import re
import fileinput

import json
import glob

script = 'process.py'

loc_base = os.environ['PWD']
logdir = 'test'
outdir = '/store/user/jennetd/september-2020/condor/'

os.chdir('..')
os.system('xrdcp -f %s root://cmseos.fnal.gov//store/user/jennetd/september-2020/'%script)
os.system('tar -zcf boostedhiggs.tar.gz boostedhiggs --exclude="*.root" --exclude="*.pdf" --exclude="*.pyc" --exclude=tmp --exclude="*.tgz" --exclude-vcs --exclude-caches-all')
os.system('xrdcp -f boostedhiggs.tar.gz root://cmseos.fnal.gov//store/user/jennetd/september-2020')
os.chdir(loc_base)

################################################
### Where is your list of root files to run over
################################################

#make local directory
locdir = logdir
os.system('mkdir -p  %s' %locdir)

print('CONDOR work dir: '+outdir)

os.system('mkdir -p /eos/uscms'+outdir)

nsubmit = 0

for year in ['2016']: #,'2017','2018']:
    for sample in ['HToBB']: #,'QCD','WandZ','top']:

        prefix = year+'_'+sample
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
            line=line.replace('SAMPLE',sample)
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

