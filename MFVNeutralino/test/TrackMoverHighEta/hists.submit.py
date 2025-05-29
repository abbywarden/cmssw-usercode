from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset

# version = '0p03onnormdzulv30lepmumv8'
version = 'ulv13lepm1jet1lep' #bjet #CHANGE FOR BJET
dataset = 'trackmover' + version
exe_fn = 'hists1j1lep.exe' #choose the executable (default is hists.exe)
apply_correction = False
year = '2018'
for nl in 1,: # 3:
    for nb in 0,: # 1, 2: #CHANGE FOR BJET
      for tau in [1000] : #[100, 300,1000, 3000, 30000] :
        for mg in [200] : #[15,40,55,]:
          if apply_correction:
            #for tm in ["sim","dat"] :
            for tm in ["sim"]:
              w_fn_2d_move = ""
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, ttbar=True, diboson=True, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
                if mg < 100 :
                    w_fn_2d_move = "reweight_higheta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
                else :
                    w_fn_2d_move = "reweight_higheta_move_sim_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=True, JetHT_data=False, BTagCSV_data=True, DisplacedJet_data=True)
                if mg < 100 :
                    w_fn_2d_move = "reweight_higheta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root" % (tau, mg, year) 
                else :
                    w_fn_2d_move = "reweight_higheta_move_dat_vetodr_tau%06ium_M%04i_%s_2D.root" % (tau, mg, year) 
              batch_tag = "2DCorrection"
              if mg < 100 :
                  w_fn_2d_kin = "reweight_all_kin_sim_vetodr_tau%06ium_M%02i_2D.root" % (tau, mg) 
              else :
                  w_fn_2d_kin = "reweight_all_kin_sim_vetodr_tau%06ium_M%04i_2D.root" % (tau, mg) 
              correction_args = '--jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, tm)
              w_fns = [w_fn_2d_kin, w_fn_2d_move]
              batch = 'TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i1 %s' % (nl, nb, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
            
            #samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMover_HighEta_' + version.capitalize() + '_%i%i_%s' % (nl, nb, batch_tag)
            #for 1jet1lep it is 101; for 1bjet1lep it is 011
            args = '-t mfvMovedTree%i%i1 %s' % (nl, nb, correction_args)  #CHANGE FOR BJET
            NtupleReader_submit(batch, dataset, samples, exe_fn, exe_args=args, input_fns_extra=[])
