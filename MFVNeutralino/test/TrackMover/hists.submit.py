from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'onnormdzulv30lepmumv9'
dataset = 'trackmover' + version
apply_correction = False
year = 2018
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      for tau in [1000, ] : #[100, 300,1000, 3000, 30000] :
        for mg in [55, ] : #[15,40,55,]:
          if tau==100 and mg==40:
            continue
          if apply_correction:
            for tm in ["sim",] :
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=False)
                #samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=True)
              batch_tag = "2Dmovedist3movedistjetdrllpsumpcoarse8Correction"
              #batch_tag = "2Dmovedist3movedist2logmCorrection"
              #batch_tag = "2Dmovedist3movedist2jetdrjet0sumpjet1sumpCorrection"
              w_fn_2d_kin = "reweight_v2p4_mixeta_kin_vetodr_tau%06ium_M%02i_%i_2D.root" % (tau, mg, year) 
              w_fn_2d_move = "reweight_v2p4_mixeta_move_vetodr_tau%06ium_M%02i_%i_2D.root" % (tau, mg, year) 
              w_fn_1d_kin = "reweight_v2p4_mixeta_kin_vetodr_tau%06ium_M%02i_%i_1D.root" % (tau, mg, year) 
              correction_args = '--jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --w_fn_1d_kin "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, w_fn_1d_kin, tm)
              w_fns = [w_fn_2d_kin, w_fn_2d_move, w_fn_1d_kin]
              batch = 'TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=True)
            #samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
            args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
