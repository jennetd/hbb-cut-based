#!/usr/bin/python
import os, sys
import subprocess

# Main method                                                                          
def main():

    if len(sys.argv) != 2:
        print("Enter year")
        return

    year = sys.argv[1]

    loc_base = os.environ['PWD']
    logdir = 'logs'

    tag = 'ggf-vbf'
    script = 'process-one.py'

    homedir = '/store/user/jennetd/october-2021/'
    outdir = homedir + tag + '/histograms/'

    # make local directory
    locdir = logdir
    os.system('mkdir -p  %s' %locdir)

    print('CONDOR work dir: ' + homedir)
    os.system('mkdir -p /eos/uscms'+outdir)

    prefix = year + "_hists"

    condor_templ_file = open(loc_base+"/make-pkl.templ.condor")
    sh_templ_file    = open(loc_base+"/make-pkl.templ.sh")

    localcondor = locdir+'/'+prefix+".condor"
    condor_file = open(localcondor,"w")
    for line in condor_templ_file:
        line=line.replace('YEAR',year)
        line=line.replace('PREFIX',prefix)
        condor_file.write(line)
    condor_file.close()

    localsh=locdir+'/'+prefix+".sh"
    eosoutput=outdir+"/"
    eosinput=homedir+tag+"/outfiles-ddb2/"
    sh_file = open(localsh,"w")
    for line in sh_templ_file:
        line=line.replace('YEAR',year)
        line=line.replace('EOSIN',eosinput)
        line=line.replace('EOSOUT',eosoutput)
        sh_file.write(line)
    sh_file.close()
 
    os.system('condor_submit %s' % localcondor)

    return 

if __name__ == "__main__":
    main()
