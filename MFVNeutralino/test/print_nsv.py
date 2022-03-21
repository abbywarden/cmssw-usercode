#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

version_a = 'V30Lepm_fullsel'
#version_b = 'V29Lepm_onlytrig'

stoplb = Samples.mfv_stoplb_samples_2018
stopld = Samples.mfv_stopld_samples_2018
# background:
drellyan = Samples.drellyan_samples_2018
leptonic = Samples.leptonic_samples_2018
qcd = Samples.qcd_samples_2018
ttbar = Samples.ttbar_samples_2018
wjets = Samples.wjet_samples_2018
diboson = Samples.diboson_samples_2018

background = drellyan + qcd + ttbar + wjets + diboson



for sample in background + stoplb + stopld :
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version_a, sample.name + '.root')
    #fn_ot = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version_b, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name, version_a
        continue
    # if not os.path.exists(fn_ot):
    #     print 'no', sample.name, version_b
    #     continue
    
    f = ROOT.TFile(fn)
    # t3 = f.Get('MinNtk3mfvVertexHistosPreSel/h_nsv')
    # t4 = f.Get('MinNtk4mfvVertexHistosPreSel/h_nsv')
    # t5 = f.Get('mfvVertexHistosPreSel/h_nsv')
    hst = f.Get('MinNtk4vtxHst1VNoBs2derr/h_sv_all_bs2derr')

    axis = hst.GetXaxis()
   # bmin = axis.FindBin(0)
    bmax = axis.FindBin(0.0050)

    #hst.Integral(bmin, bmax)
   # print sample.name, ": bin for value of 50um ", bmax

   
    # f_ot = ROOT.TFile(fn_ot)
    # t3_ot = f_ot.Get('MinNtk3mfvVertexHistosPreSel/h_nsv')
    # t4_ot = f_ot.Get('MinNtk4mfvVertexHistosPreSel/h_nsv')
    # t5_ot = f_ot.Get('mfvVertexHistosPreSel/h_nsv')

    # print sample.name, ": min3trk_1sv ", t3_ot.GetBinContent(2), t3.GetBinContent(2)
    # print "             : min4trk_1sv ", t4_ot.GetBinContent(2), t4.GetBinContent(2)
    # print "             : min5trk_1sv ", t5_ot.GetBinContent(2), t5.GetBinContent(2)
    # print " "
    # print sample.name, ": min3trk_2sv ", t3_ot.GetBinContent(3), t3.GetBinContent(3)
    # print "             : min4trk_2sv ", t4_ot.GetBinContent(3), t4.GetBinContent(3)
    # print "             : min5trk_2sv ", t5_ot.GetBinContent(3), t5.GetBinContent(3)
    
