import sys, os
from ROOT import gStyle
from JMTucker.Tools.ROOTTools import *
set_style()

ps = plot_saver(plot_dir('misc_plots'), size=(1400,900), log=False)
#root_fname = '/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosV27Lepm/condor_mfv_stoplb_tau010000um_M0800_2018/histos_0.root'
root_fname = '/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosV29Lepm_displept_info/mfv_stoplb_tau001000um_M1600_2018.root'
f = ROOT.TFile(root_fname)
#h = f.Get('mfvEventHistosPreSel/h_vertex_seed_track_phi_v_eta')
#gStyle.SetOptStat(0)

h = f.Get('MinNtk4mfvVertexHistosPreSel/h_pvrho20_sv_all_bsbs2ddist')
gStyle.SetOptStat(0)

h.Draw('COLZ')
#ps.save('nice_eta_phi')
ps.save('nice_pvrho20_bsbs2ddist_stoplb_tau1mm_M1600')


