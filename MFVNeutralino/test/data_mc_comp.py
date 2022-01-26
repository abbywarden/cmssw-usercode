#!/usr/bin/env python

import os
from functools import partial
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

#year = '2017p8'
#version = 'V23m'
#root_file_dir = '/uscms_data/d2/tucker/crab_dirs/Histos%s' % version

year = '2018'
version = 'V30Lepm_matchTrig_wfull'
#version = 'V30Lepm_wfull_lepsel'
root_file_dir = '/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version

set_style()
ps = plot_saver(plot_dir('data_mc_comp_%s_%s' % (year, version)))

qcd_samples = Samples.qcd_samples_2017[1:]
ttbar_samples = Samples.ttbar_samples_2017
signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
data_samples = [] # Samples.data_samples_2017
background_samples = ttbar_samples + qcd_samples
lumi = ac.int_lumi_2017 * ac.scale_factor_2017
lumi_nice = ac.int_lumi_nice_2017

if year == '2018':
    qcd_samples = Samples.qcd_samples_2018
    ttbar_samples = Samples.ttbar_samples_2018[:1]
    wjet_samples = Samples.wjet_samples_2018[:1]
    diboson_samples = Samples.diboson_samples_2018
    leptonic_samples = Samples.leptonic_samples_2018
    #signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
    signal_sample = Samples.mfv_stoplb_tau001000um_M1000_2018
    data_samples = [] # Samples.data_samples_2017
   # background_samples = []
    background_samples = ttbar_samples + wjet_samples + leptonic_samples
    lumi = ac.int_lumi_2018 * ac.scale_factor_2018
    lumi_nice = ac.int_lumi_nice_2018

if year == '2017p8':
    qcd_samples = Samples.qcd_samples_2018 + Samples.qcd_samples_2017[1:]
    ttbar_samples = Samples.ttbar_samples_2017
    signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
    data_samples = [] # Samples.data_samples_2017
    #background_samples = [],
    background_samples = qcd_samples + ttbar_samples
    lumi = ac.int_lumi_2017p8 * ac.scale_factor_2017p8
    lumi_nice = ac.int_lumi_nice_2017p8

for s in qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7
for s in wjet_samples:
    s.join_info = True, 'W+jets', ROOT.kMagenta-6
for s in leptonic_samples:
    s.join_info = True, 'QCD lept enriched', ROOT.kMagenta-3

signal_samples = [signal_sample]
signal_sample.nice_name = 'Signal: #sigma = 1 fb, c#tau = 1 mm, M = 1000 GeV'
signal_sample.color = 8

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = [],
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = lumi,
            int_lumi_nice = lumi_nice,
            canvas_top_margin = 0.08,
            poisson_intervals = True,
            legend_pos = (0.48, 0.78, 0.88, 0.88),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )


# unsure if this will work?
C('lepton_cutflow',
  histogram_path = 'mfvAnaCutFlowHistos/h_lepton_cutflow',
  y_title = 'Events',
  y_range = (1e-1, 1e7),
  )
  
C('presel_njets',
  histogram_path = 'mfvEventHistosPreSel/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_njets20',
  histogram_path = 'mfvEventHistosPreSel/h_njets20',
  x_title = 'Number of jets w p_{T} > 20 GeV',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_njets20_nm1',
  histogram_path = 'mfvEventHistosPreSelNoJet/h_njets20',
  x_title = 'Number of jets w p_{T} > 20 GeV',
  y_title = 'Events',
  y_range = (1, 1e8),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1)
  )

C('presel_nbjets',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_2',
  x_title = 'Number of tight bjets',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_bjet_pt',
  histogram_path = 'mfvEventHistosPreSel/h_bjet_pt',
  x_title = 'bjet p_{T} (GeV)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

# C('presel_bjet_eta',
#   histogram_path = 'mfvEventHistosPreSel/h_bjet_eta',
#   x_title = 'bjet #eta',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_bjet_phi',
#   histogram_path = 'mfvEventHistosPreSel/h_bjet_phi',
#   x_title = 'bjet #phi',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_ht40',
#   histogram_path = 'mfvEventHistosPreSel/h_jet_ht_40',
#   rebin = 4,
#   x_title = 'Jet H_{T} (GeV)',
#   y_title = 'Events/100 GeV',
#   y_range = (1, 1e8),
#   )

#C('presel_htall',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_ht',
#  )
#
#C('presel_jetpt1',
#  histogram_path = 'mfvEventHistosPreSel/h_jetpt1',
#  y_range = (1,1e6),
#  )
#
#C('presel_jetpt4',
#  histogram_path = 'mfvEventHistosPreSel/h_jetpt4',
#  y_range = (1,5e6),
#  )
#
#C('presel_jetpt',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_pt',
#  y_range = (1,5e7),
#  )
#
#C('presel_jeteta',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_eta',
#  )
#
#C('presel_jetphi',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_phi',
#  )
#
#C('presel_jetpairdphi',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_pairdphi',
#  )
#
#C('presel_met',
#  histogram_path = 'mfvEventHistosPreSel/h_met',
#  )
#
#C('presel_metphi',
#  histogram_path = 'mfvEventHistosPreSel/h_metphi',
#  )
#
#C('presel_nbtags_tight',
#  histogram_path = 'mfvEventHistosPreSel/h_nbtags_tight',
#  )
#
C('presel_nselleptons',
  histogram_path = 'mfvEventHistosPreSel/h_nselleptons_tight_e_med_mu',
  x_title = '# of tight/med leptons',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_nfull_selleptons',
  histogram_path = 'mfvEventHistosPreSel/h_fullsellep_tight_e_med_mu',
  x_title = '# of sel leptons',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_nfull_selelectrons',
  histogram_path = 'mfvEventHistosPreSel/h_nfullselel_tight',
  x_title = '# of sel electrons',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_nfull_selmuons',
  histogram_path = 'mfvEventHistosPreSel/h_nfullselmu_medium',
  x_title = '# of sel muons',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ndispleptons50',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl50_leptons',
  x_title = '# of leptons w/ |dxy| > 50um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ndispleptons100',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl100_leptons',
  x_title = '# of leptons w/ |dxy| > 100um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_nselleptons_nm1',
 histogram_path = 'mfvEventHistosPreSelNoLep/h_nselleptons_tight_e_med_mu',
 x_title = '# of sel. leptons',
 y_title = 'Events',
 y_range = (1, 1e8),
 )

C('presel_nfull_selleptons_nm1',
 histogram_path = 'mfvEventHistosPreSelNoLep/h_fullsellep_tight_e_med_mu',
 x_title = '# of sel leptons',
 y_title = 'Events',
 y_range = (1, 1e8),
 cut_line = ((1, 0, 1, 2.5e8), 2, 5, 1)
 )

C('presel_nfull_selelectrons_nm1',
 histogram_path = 'mfvEventHistosPreSelNoLep/h_nfullselel_tight',
 x_title = '# of sel electrons',
 y_title = 'Events',
 y_range = (1, 1e8),
# cut_line = ((1, 0, 1, 2.5e8), 2, 5, 1)
 )

C('presel_nfull_selmuons_nm1',
 histogram_path = 'mfvEventHistosPreSelNoLep/h_nfullselmu_medium',
 x_title = '# of sel muons',
 y_title = 'Events',
 y_range = (1, 1e8),
# cut_line = ((1, 0, 1, 2.5e8), 2, 5, 1)
 )

# C('presel_ndispleptons_nm1',
#   histogram_path = 'mfvEventHistosPreSelNoDxy/h_ndispl_leptons',
#   x_title = '# of leptons w/ |dxy| > 50um',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   cut_line = ((1, 0, 1, 2.5e8), 2, 5, 1)
#   )

C('presel_ndispelectrons50',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl50_electrons',
  x_title = '# of electrons w/ |dxy| > 50um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ndispmuons50',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl50_muons',
  x_title = '# of muons w/ |dxy| > 50um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ndispelectrons100',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl100_electrons',
  x_title = '# of electrons w/ |dxy| > 100um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ndispmuons100',
  histogram_path = 'mfvEventHistosPreSel/h_ndispl100_muons',
  x_title = '# of muons w/ |dxy| > 100um',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

# C('presel_ndispelectrons_nm1',
#   histogram_path = 'mfvEventHistosPreSelNoDxy/h_ndispl_electrons',
#   x_title = '# of electrons w/ |dxy| > 50um',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_ndispmuons_nm1',
#   histogram_path = 'mfvEventHistosPreSelNoDxy/h_ndispl_muons',
#   x_title = '# of muons w/ |dxy| > 50um',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

C('presel_nmuons_medium',
  histogram_path = 'mfvEventHistosPreSel/h_nmuons_medium',
  x_title = '# of med. muons',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_medmu_abs_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_muon_absdxybs_medium',
  x_title = 'abs dxybs of med. muons',
  y_title = 'Events',
  y_range = (1, 1e8)
  )

C('presel_medmu_nsigmadxy',
  histogram_path = 'mfvEventHistosPreSel/h_muon_nsigmadxy_medium',
  x_title = 'med. muons nsigmadxy',
  y_title = 'Events',
  y_range = (1, 1e8)
  )

C('presel_nelectrons_tight',
  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_tight',
  x_title = '# of tight ele',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_tightele_abs_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_electron_absdxybs_tight',
  x_title = 'abs dxybs of tight ele',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_tightele_nsigmadxy',
  histogram_path = 'mfvEventHistosPreSel/h_electron_nsigmadxy_tight',
  x_title = 'tight ele nsigmadxy',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_tightel_pt',
  histogram_path = 'mfvEventHistosPreSel/h_electron_pt_tight',
  x_title = 'tight ele p_{T} (GeV)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_medmu_pt',
  histogram_path = 'mfvEventHistosPreSel/h_muon_pt_medium',
  x_title = 'med. mu p_{T} (GeV)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_jetmu_dR',
  histogram_path = 'mfvEventHistosPreSel/h_highjetmu_pairdphi',
  x_title = 'jet-mu pair dR (rad)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_jetel_dR',
  histogram_path = 'mfvEventHistosPreSel/h_highjetel_pairdphi',
  x_title = 'jet-el pair dR (rad)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )



#C('presel_npv',
#  histogram_path = 'mfvEventHistosPreSel/h_npv',
#  y_range = (1,1e6),
#  )
#
#C('presel_pvntracks',
#  histogram_path = 'mfvEventHistosPreSel/h_pvntracks',
#  )
#
#C('presel_pvscore',
#  histogram_path = 'mfvEventHistosPreSel/h_pvscore',
#  )
#
#C('presel_pvrho',
#  histogram_path = 'mfvEventHistosPreSel/h_pvrho',
#  )
#
C('presel_nseedtracks',
  histogram_path = 'mfvEventHistosPreSel/h_n_vertex_seed_tracks',
  x_title = '# vertex seed tracks',
  y_title = 'Events',
  y_range = (1,1e7),
  )


C('presel_seedtrack_npxlayers',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
 y_range = (1,1e8),
 )

C('presel_seedtrack_nstlayers',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
 y_range = (1,1e8),
 )

C('presel_seedtrack_chi2dof',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_chi2dof',
 y_range = (1,1e8),
 )

C('presel_seedtrack_pt',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_pt',
 y_range = (1,1e8),
 )

C('presel_seedtrack_eta',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_eta',
 y_range = (1,6e6),
 )

C('presel_seedtrack_phi',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_phi',
 y_range = (1,6e6),
 )

C('presel_seedtrack_dxy',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dxy',
  x_title = 'vertex seed track dxy (cm)',
  y_title = 'tracks/10 #mum',
  y_range = (1,1e6),
  )
#
C('presel_seedtrack_dz',
 histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dz',
 y_range = (1,1e6),
 )


# C('onevtx_ntracks',
#   histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
#   x_title = 'Number of tracks per vertex',
#   y_title = 'Vertices',
#   y_range = (0.1, 1e6),
#   cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#   )

# C('onevtx_bs2derr',
#   histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#   x_title = 'Uncertainty in d_{BV} (cm)',
#   y_title = 'Vertices/5 #mum',
#   y_range = (1, 1e6),
#   cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#   )

# C('onevtx_dbv',
#   histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#   x_title = 'd_{BV} (cm)',
#   y_title = 'Vertices/50 #mum',
#   x_range = (0, 0.4),
#   y_range = (1, 1e6),
#   cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#   )

C('nsv_min3track',
  histogram_path = 'MinNtk3mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of min 3-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-3, 1e8),
  )

C('nsv_min4track',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of min4-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-3, 1e8),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1), 
  )

C('nsv_5track',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 5-or-more-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-3, 1e8),
 # cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
  )

C('sv_njetsntks',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_njetsntks',
  x_title = 'Number of jets assoc. by tracks to SV',
  y_title = 'arb. units',
  y_range = (1, 1e4),
  )

C('sv_ntracks_nm1',
  histogram_path = 'MinNtk3mfvVertexHistosPreSel/h_sv_all_ntracks',
  x_title = 'Number of tracks per SV',
  y_title = 'arb. units',
  y_range = (1, 1e5),
  cut_line = ((4, 0, 4, 2e5), 2, 5, 1),
  )

C('sv_chi2dof',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_chi2dof',
  x_title = 'SV #chi^2/dof',
  y_title = 'arb. units',
  )

C('sv_tkonlypt',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_tkonlypt',
  x_title = 'SV tracks-only p_{T} (GeV)',
  y_title = 'arb. units',
  )

C('sv_track_dxy',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_track_dxy',
  x_title = 'all SV tracks dxy (cm)',
  y_title = 'arb. units',
  )

C('sv_track_dxy_err',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_track_dxy_err',
  x_title = 'all SV tracks #sigma(dxy) (cm)',
  y_title = 'arb. units',
  )

C('sv_track_nsigmadxy',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_track_nsigmadxy',
  x_title = 'all SV tracks n#sigma(dxy) (cm)',
  y_title = 'arb. units',
  )

# C('rescaled_dbv_nm1',
#   histogram_path = 'MinNtk4vtxHst1VNoBsbs2ddist/h_sv_all_rescale_bsbs2ddist',
#   x_title = 'dbv (cm)',
#   y_title = 'arb. units',
#   x_range = (0, 0.4),
#  # y_range = (1, 15),
#   )

# C('rescaled_bs2derr_nm1',
#   histogram_path = 'MinNtk4vtxHst1VNoBs2derr/h_sv_all_rescale_bs2derr',
#   x_title = '#sigma(dist2d(SV, beamspot)) (cm)',
#   y_title = 'arb. units',
#   x_range = (0, 0.05),
#   y_range = (1e-1, 1e4),
#   )

C('dbv_nm1',
  histogram_path = 'MinNtk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  x_title = 'dbv (cm)',
  y_title = 'arb. units',
  x_range = (0, 0.4),
 # y_range = (1, 15),
  cut_line = ((0.01, 0, 0.01, 2.8e2), 2, 5, 1)
  )

C('bs2derr_nm1',
  histogram_path = 'MinNtk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  x_title = '#sigma(dist2d(SV, beamspot)) (cm)',
  y_title = 'arb. units',
  x_range = (0, 0.05),
  y_range = (1e-1, 1e4),
  cut_line = ((0.0025, 0, 0.0025, 2.0e4), 2, 5, 1)
  )


# C('dbv',
#   histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#   x_title = 'd_{BV} (cm)',
#   y_title = 'Vertices/50 #mum',
#   x_range = (0, 0.4),
#   y_range = (1, 1e4),
#   )

#unsure
# C('bsbs2ddist',
#   histogram_path = 'mfvVertexHistosFullSel/h_sv_all_rescale_bsbs2ddist',
#   x_title = 'd_{BV} (cm)',
#   y_title = 'Vertices/50 #mum',
#   x_range = (0, 0.4),
#   y_range = (1, 1e6),
#   )

C('dvv',
  histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
  rebin = 10,
  x_title = 'd_{VV} (cm)',
  y_title = 'Events/200 #mum',
  y_range = (1e-2, 10),
  )


# ## TrackerMapper
# C('track_pt',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_pt',
#   x_title = 'Track p_{T} (GeV)',
#   y_title = 'Tracks/0.1 GeV',
#   y_range = (1, 1e12),
#   cut_line = ((1, 0, 1, 2.8e12), 2, 5, 1),
#   )

# C('track_min_r',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_min_r',
#   x_title = 'Minimum layer number',
#   y_title = 'Tracks',
#   y_range = (1, 1e12),
#   cut_line = ((2, 0, 2, 2.8e12), 2, 5, 1),
#   )

# C('track_npxlayers',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_npxlayers',
#   x_title = 'Number of pixel layers',
#   y_title = 'Tracks',
#   y_range = (1, 1e12),
#   cut_line = ((2, 0, 2, 2.8e12), 2, 5, 1),
#   )

# C('track_nstlayers',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nstlayers',
#   x_title = 'Number of strip layers',
#   y_title = 'Tracks',
#   y_range = (1, 1e12),
#   cut_line = ((6, 0, 6, 2.8e12), 2, 5, 1),
#   )

# # C('track_nstlayers_etagt2',
# #   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
# #   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nstlayers_etagt2',
# #   x_title = 'Number of strip layers (|#eta| #geq 2)',
# #   y_title = 'Tracks',
# #   y_range = (1, 1e10),
# #   cut_line = ((7, 0, 7, 2.8e10), 2, 5, 1),
# #   )

# C('track_nsigmadxy',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nsigmadxy',
#   x_title = 'N#sigma(dxy)',
#   y_title = 'Tracks',
#   x_range = (0, 10),
#   y_range = (1, 1e10),
#   cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
#   )



#C('100pc_3t1v_ntracks',
#  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_bs2derr',
#  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_dbv',
#  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_onevtx_dbv',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t2v_dvv',
#  histogram_path = 'Ntk3mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  )
#
#C('100pc_4t1v_ntracks',
#  histogram_path = 'Ntk4vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_bs2derr',
#  histogram_path = 'Ntk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_dbv',
#  histogram_path = 'Ntk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_onevtx_dbv',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t2v_dvv',
#  histogram_path = 'Ntk4mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )
#
#C('100pc_5t1v_ntracks',
#  histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_bs2derr',
#  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_dbv',
#  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_onevtx_dbv',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t1v_onevtx_dbv_unzoom',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t2v_dvv',
#  histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )
