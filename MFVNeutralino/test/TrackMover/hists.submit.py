from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'onnormdzulv30lepmumv7'
dataset = 'trackmover' + version
apply_correction = True
year = 2017
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      for tau in [100, 300,1000, 3000, 30000] :
        for mg in [15,40,55,]:
          if apply_correction:
            for tm in ["sim",] :
              if tm == "sim":
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=False)
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=True)
              batch_tag = "2Dmovedist3movedist2jetdrjet1sumpCorrection"
              w_fn_2d_kin = "reweight_kin_vetodr_tau%06ium_M%02i_%i_2D.root" % (tau, mg, year) 
              w_fn_2d_move = "reweight_move_vetodr_tau%06ium_M%02i_%i_2D.root" % (tau, mg, year) 
              
              correction_args = '--jet-decayweights true --w_fn_2d_kin "%s" --w_fn_2d_move "%s" --tm "%s"' % (w_fn_2d_kin, w_fn_2d_move, tm)
              w_fns = [w_fn_2d_kin, w_fn_2d_move]
              batch = 'TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=True)
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
            args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
