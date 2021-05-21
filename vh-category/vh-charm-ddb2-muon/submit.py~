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

    tag = 'vh-charm-muon'
    script = 'process-one.py'

    homedir = '/store/user/jennetd/may-2021/'
    indir = '/store/user/jennetd/may-2021/infiles-split/'
    outdir = homedir + tag + '/outfiles/'

    # copy processor files
    os.system('rm -r boostedhiggs')
    os.system('cp -r boostedhiggs-vhhad/boostedhiggs/ .')
    
    # make local directory
    locdir = logdir
    os.system('mkdir -p  %s' %locdir)

    print('CONDOR work dir: ' + homedir)
    os.system('mkdir -p /eos/uscms'+outdir)

    nsubmit = 0
    
    # get list of input files
    infiles = subprocess.getoutput("ls infiles-split/"+year+"*.json").split()
    
    for this_file in infiles:
        index = this_file.split("_")[1].split(".json")[0]
        print(this_file, index)

        prefix = year+'_'+str(index)
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
    
        localsh=locdir+'/'+prefix+".sh"
        eosoutput="root://cmseos.fnal.gov/"+outdir+"/"+prefix+'.coffea'
        sh_file = open(localsh,"w")
        for line in sh_templ_file:
            line=line.replace('SCRIPTNAME',script)
            line=line.replace('YEAR',year)
            line=line.replace('SAMPLE',str(index))
            line=line.replace('EOSDIR',homedir)
            line=line.replace('TAG',tag)
            line=line.replace('EOSIN',indir)
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

    return 

if __name__ == "__main__":
    main()
