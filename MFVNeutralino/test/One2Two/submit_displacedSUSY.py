
'''
Very simple script which loops over datacards and saves the output:
or...combines datacards
. 

USAGE:
python submit_displacedSUSY.py
'''

import sys, os
#import JMTucker.Tools.Samples as sp

#now combines the datacards :
# year_2 = '2018'
# year_1 = '2017'
# year = '201718'
# ## old : (for datacards_jan)
# # #if want the susyxsec : use -> susyxsec/test/<year>
# # #if want sig1fbxsec : use -> sig1fbxsec/<year> 
# #if want test sig1fbxsec observed limits : use -> sig1fbxsec/observed_test/<year>
# ######################################################################################
# for datacard in os.listdir("/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/using_data/wABCDsysttest/%s"%(year_1)):
#     signal_name = datacard[:-18] 
#     card1 = "/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/using_data/wABCDsysttest/%s/%s_%s_datacard.txt"%(year_1,signal_name, year_1, )
#     card2 = "/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/using_data/wABCDsysttest/%s/%s_%s_datacard.txt"%(year_2, signal_name, year_2)
#     combinedcard = "/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/using_data/wABCDsysttest/%s/%s_%s_datacard.txt"%(year, signal_name, year)
#     cmd = 'combineCards.py Name1=%s Name2=%s > %s'%(card1, card2, combinedcard)
#     print(cmd)
#     os.system(cmd)
 

#trying --rMin=0 --rMax 150000
#if want verbose : --verbose 3 
# old -- for jan datacards 
# #if want the susyxsec : use -> susyxsec/test/<year>
# if want the sig1fbxsec : Use -> sig1fbxsec/<year> 
# if want test sig1fbxsec observed limits : use -> sig1fbxsec/observed_test/<year>
######################################

year = '201718'
for datacard in os.listdir("/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/%s"%(year)):
    signal_name = datacard[:-13] 
    #cmd = 'combine -M AsymptoticLimits --run blind /afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_jan/sig1fbxsec/%s/%s &> %s_limitsum.txt'%(year, datacard, signal_name)
    cmd = 'combine -M AsymptoticLimits --run blind /afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/using_data/wABCDsysttest/%s/%s &> %s_limitsum.txt'%(year, datacard, signal_name)
    #cmd = 'combine -M AsymptoticLimits /afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_apr/%s/%s &> %s_limitsum.txt'%(year, datacard, signal_name)
    #cmd = 'combine -M MultiDimFit /afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/datacards_jan/susyxsec/%s/%s &> %s_limitsum.txt'%(year, datacard, signal_name)
 
    print(cmd)
    os.system(cmd)
    
    
# for s in sp.mfv_stopld_samples_2017:
#     path = '~/work/llp/MFVNeutralino/test/datacards/'
#     cmd = 'combine -M AsymptoticLimits --run blind %s'%path + s.name + '_datacard.txt &> %s_limitsum.txt'%s.name
#     print(cmd)
#     os.system(cmd)







# # this script must be run from One2Two/

# import sys, os, shutil, time
# from JMTucker.Tools.general import save_git_status
# from JMTucker.Tools.CondorSubmitter import CondorSubmitter, crab_dirs_root
# import ROOT; ROOT.gROOT.SetBatch()
# import JMTucker.Tools.Samples as sp
# import limitsinput

# # The combine tarball is made in a locally checked-out combine
# # environment so the worker nodes don't have to git clone, etc.
# #
# # In this CMSSW environment, run
# #   cmsMakeTarball.py --standalone dummyarg > ~/tarball.py
# #
# # Set up combine *on a SL7 machine* following
# # http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
# # Directly for this version:
# #
# #   export SCRAM_ARCH=slc7_amd64_gcc700
# #   cmsrel CMSSW_10_2_13
# #   cd CMSSW_10_2_13/src
# #   cmsenv
# #   git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
# #   cd HiggsAnalysis/CombinedLimit
# #   patch -p1 < path/to/main/cmssw/src/JMTucker/MFVNeutralino/test/One2Two/patchSetHint
# #   git fetch origin
# #   git checkout v8.0.1
# #   scram b clean; scram b
# #
# # In that same combine environment, make the tarball with:
# #   python ~/tarball.py --include-bin combine.tgz
# # Copy the tarball to eos, hopefully with a versioned name,
# # and update the url below.

# script_template = '''#!/bin/bash
# echo combine script starting at $(date) with args $*

# REALJOB=$1
# mapfile -t JOBMAP < cs_jobmap
# export JOB=${JOBMAP[$REALJOB]}
# export WHICH=$2
# export WD=$(pwd)

# source /cvmfs/cms.cern.ch/cmsset_default.sh
# export SCRAM_ARCH=slc7_amd64_gcc700
# scram project CMSSW CMSSW_10_2_13 2>&1 >/dev/null
# cd CMSSW_10_2_13/src
# eval `scram runtime -sh`

# cd ..
# xrdcp -s root://cmsxrootd.hep.wisc.edu//store/user/acwarden/combine.tgz combine.tgz
# if [[ ! -f combine.tgz ]]; then
#     >&2 echo could not copy combine tarball
#     exit 1
# fi
# tar xf combine.tgz
# scram b 2>&1 >/dev/null
# hash -r
# which combine

# cd $WD

# {
#     echo "========================================================================="
#     echo datacard:
#     python datacard.py $WHICH __DATACARDARGS__ > datacard.txt
#     awk '{ print "DATACARD: " $0 }' datacard.txt

#     hint=$(awk '/hint/ { print $NF }' datacard.txt)
#     cmd="combine -M MarkovChainMC --noDefaultPrior=0 --tries 20 -b 200 --iteration 100000 datacard.txt"

#     if [[ $JOB == 0 ]]; then
#         echo "========================================================================="
#         echo Observed limit
#         eval $cmd
#         mv higgsCombine*root observed.root

# #       echo "========================================================================="
# #       echo Observed limit, no systematics
# #       eval $cmd -S0
# #       mv higgsCombine*root observed_S0.root
#     fi
#     # this lets us use cs_status to find missing files later but the _S0,, other extra files that are made by commented out lines aren't taken care of! 
#     touch observed_${JOB}.root

#     ntoys=100
#     seedbase=13068931

#     echo "========================================================================="
#     echo Expected limits
#     eval $cmd --toys $ntoys --saveToys -s $((JOB+seedbase))
#     mv higgsCombine*root expected_${JOB}.root

# #   echo "========================================================================="
# #   echo Expected limits, no systematics
# #   eval $cmd -S0 --toys $ntoys --saveToys -s $((JOB+seedbase))
# #   mv higgsCombine*root expected_S0_${JOB}.root

# ########################################################################

# '''

# if 'save_toys' not in sys.argv:
#     script_template = script_template.replace(' --saveToys', '')

# include_2016 = False
# njobs = 20

# jdl_template = '''universe = vanilla
# Executable = run.sh
# arguments = $(Process) %(isample)s
# Output = stdout.$(Process)
# Error = stderr.$(Process)
# Log = log.$(Process)
# stream_output = true
# stream_error  = false
# notification  = never
# should_transfer_files = YES
# when_to_transfer_output = ON_EXIT
# transfer_input_files = %(input_files)s,cs_jobmap
# +REQUIRED_OS = "rhel7"
# +DesiredOS = REQUIRED_OS
# Queue %(njobs)s
# '''

# batch_root = crab_dirs_root('combine_output_%i' % time.time())
# if os.path.isdir(batch_root):
#     raise IOError('%s exists' % batch_root)
# print(batch_root)
# os.mkdir(batch_root)
# os.mkdir(os.path.join(batch_root, 'inputs'))

# save_git_status(os.path.join(batch_root, 'gitstatus'))

# # input_files = []
# # for x in ['signal_efficiency.py', 'datacard.py', 'limitsinput.root']:
# #     nx = os.path.abspath(os.path.join(batch_root, 'inputs', os.path.basename(x)))
# #     shutil.copy2(x, nx)
# #     input_files.append(nx)
# # input_files = ','.join(input_files)

# input_files = []

# ctaus = [100, 300, 1000, 10000, 30000]
# mstop = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800]
# decay = ['ld', 'lb']
# for ctau in ctaus:
#   for m in mstop:
#       for d in decay:
#         signal = "mfv_stop%s_tau0%05ium_M%i_Histos_%s" % (d, ctau,m,year)
#         signal_output = "mfv_stop%s_tau0%05ium_M%i_%s" % (d, ctau,m,year)

# f = ROOT.TFile('limitsinput.root')

# years = ('2016','2017','2018') if include_2016 else ('2017','2018')
# # samples = limitsinput.sample_iterator(f,
# #                                       require_years=years,
# #                                       test='test_batch' in sys.argv,
# #                                       slices_1d='slices_1d' in sys.argv,
# #                                       )
# samples = 
# names = set(s.name for s in samples)
# allowed = [arg for arg in sys.argv if arg in names]

# for sample in samples:
#     if allowed and sample.name not in allowed:
#         continue

#     print sample.isample, sample.name,
#     isample = sample.isample # for locals use below

#     batch_dir = os.path.join(batch_root, 'signal_%05i' % sample.isample)
#     os.mkdir(batch_dir)
#     open(os.path.join(batch_dir, 'nice_name'), 'wt').write(sample.name)

#     run_fn = os.path.join(batch_dir, 'run.sh')
#     open(run_fn, 'wt').write(script_template % locals())

#     open(os.path.join(batch_dir, 'cs_dir'), 'wt')
#     open(os.path.join(batch_dir, 'cs_jobmap'), 'wt').write('\n'.join(str(i) for i in xrange(njobs)) + '\n')
#     open(os.path.join(batch_dir, 'cs_submit.jdl'), 'wt').write(jdl_template % locals())
#     open(os.path.join(batch_dir, 'cs_njobs'), 'wt').write(str(njobs))
#     open(os.path.join(batch_dir, 'cs_outputfiles'), 'wt').write('observed.root expected.root combine_output.txtgz')

#     CondorSubmitter._submit(batch_dir, njobs)

# # zcat signal_*/combine_output* | sort | uniq | egrep -v '^median expected limit|^mean   expected limit|^Observed|^Limit: r|^Generate toy|^Done in|random number generator seed is|^   ..% expected band|^DATACARD:' | tee /tmp/duh
