#!/usr/bin/env python


import numpy as np
import ROOT
import os
from ROOT import TLegend
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

    
version = 'V30Lepm_fullsel'
signal = 'mfv_stopld_tau010000um_M1600_2018'

#Input Files -> get the bs2derr
sig_fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version, signal + '.root')
file_sig_in = ROOT.TFile(sig_fn) 
h_sig = file_sig_in.Get('MinNtk4vtxHst2VNoBs2derr/h_sv_all_bs2derr')

bkg_fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1025p1/src/JMTucker/Tools/scripts/background_V30_fullsel.root')
file_bkg_in = ROOT.TFile(bkg_fn)
h_bkg = file_bkg_in.Get('MinNtk4vtxHst2VNoBs2derr/h_sv_all_bs2derr')


# Output file and any histograms we want
file_out = ROOT.TFile('roc2sv_' + signal + '.root', 'recreate')

c_roc = ROOT.TCanvas('c_roc', '', 580, 620)
c_roc.SetGrid()
g_roc = ROOT.TGraph()

print_set = [50, 60, 70, 80, 90, 100, 120]
for i in range(h_sig.GetNbinsX()):
    eff_sig = h_sig.Integral(1, i + 1) / h_sig.Integral()
    eff_bkg = h_bkg.Integral(1, i + 1) / h_bkg.Integral()
    # try instead of 1 - eff_bkg, just eff_bkg ? yep. good
    g_roc.SetPoint(i, eff_bkg, eff_sig)
    if i in print_set :
        print "bin: ", i, "eff_sig & eff_bkg: ", eff_sig, eff_bkg,
        if eff_sig != 0 :
            print (eff_sig - eff_bkg)/eff_sig * 100
            print "-----------------------------------"
    
    g_roc.GetXaxis().SetRangeUser(0.0, 1.1)
    g_roc.GetYaxis().SetRangeUser(0.0, 1.1)
    g_roc.GetXaxis().SetTitle('Bkg eff')
    g_roc.GetYaxis().SetTitle('Sig eff')
    g_roc.SetLineWidth(2)
    g_roc.SetMarkerStyle(4)
    g_roc.SetTitle(signal + ' ROC')
    g_roc.Draw('ACP')
    
c_roc.Write()

file_out.Write()
file_out.Close()




    
