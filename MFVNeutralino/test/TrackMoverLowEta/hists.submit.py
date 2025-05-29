from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

#version = 'ulv13lepmofftossv8'
version = 'ulv14lepm1jet1lep' #CHANGE FOR BJET
dataset = 'trackmover' + version
exe_fn = 'hists1j1lep.exe' #choose the executable (default is hists.exe)
apply_correction = True
# year = '2017p8'
#year = '20161'
year = '2018'
for nl in 1,: # 3
    for nb in 0,: # 1, 2: #CHANGE FOR BJET
      for tau in [1000] : #[100, 300,1000, 3000, 30000] :
        for mg in [200] : #[15,40,55,]:
          if apply_correction:
            #for tm in ["sim","dat"] :
            for tm in ["sim"]:
              w_fn_2d_move = ""
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False)
                w_fn_2d_move = "reweight_loweta_move_sim_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=True)
                w_fn_2d_move = "reweight_loweta_move_dat_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              batch_tag = "2DCorrection"
              w_fn_2d_kin = "reweight_stopld_kinjet0lep1p_tau%06ium_M%04i_2D.root" % (tau, mg) 
              #w_fn_2d_ang = "reweight_stopld_jet0lep1deatdphi_tau%06ium_M%04i_2D.root" % (tau, mg)
              
              #using 1d 
              w_fn_1d_kin = "reweight_2_stopld_tau%06ium_M%04i_1D_%s.root" % (tau, mg, year)
              #correction_args = '--jetlep-kinweights false  --jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, tm)
              
              correction_args = '--jetlep-kinweights true --w_fn_1d_kin "%s" --jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_1d_kin, w_fn_2d_kin, w_fn_2d_move, tm)
              w_fns = [w_fn_1d_kin, w_fn_2d_kin, w_fn_2d_move]
              #w_fns = [w_fn_2d_kin, w_fn_2d_move]


              batch = 'TrackMover_LowEta_' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i1 %s' % (nl, nb, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_fn, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
            #samples = [getattr(Samples, 'ww_20161')]
            #samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
            batch_tag = "noCorrection"
            correction_args = "--jetlep-kinweights false --jet-decayweights false "
            # batch = 'TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_%s' % (nl, nb, batch_tag)
            batch = 'TrackMover_LowEta_' + version.capitalize() + '_%i%i_%s' % (nl, nb, batch_tag)
            #for 1jet1lep it is 101; for 1bjet1lep it is 011
            args = '-t mfvMovedTree%i%i1 %s' % (nl, nb, correction_args) #CHANGE FOR BJET
            NtupleReader_submit(batch, dataset, samples, exe_fn, exe_args=args, input_fns_extra=[])

