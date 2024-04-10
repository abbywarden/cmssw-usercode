from JMTucker.Tools.MetaSubmitter import *
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers

version = 'onnormdzulv30lepmumv6'
dataset = 'trackmover' + version
apply_correction = False
year = 2017
for nl in 2,: # 3:
    for nb in 0,: # 1, 2:
      for tau in [1000,30000] :#[100,300,3000,10000,30000] :
        for mg in [55,]:
          if apply_correction:
            for tm in ["sim",] : #"dat"] :
              if tm == "sim":
                #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=False)
                samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
              else:
                samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=True)
              #batch_tag = "2Djetdrjet1sump1Dmovedist2Correction"
              #batch_tag = "2Djetdrjet1sump1Dmovedist2Correction"
              #batch_tag = "2Djetdrjet1sumpCorrection"
              #batch_tag = "2Djetdr2logmCorrection"
              batch_tag = "2Dmovedist3movedist2Correction"
              #batch_tag = "1Djetdr1Djet1sump1Dmovedist3Correction"
              #batch_tag = "1DcloseseedtksCorrection"
              #batch_tag = "2Djetdrcloseseedtks1Dmovedist3Correction"
              #batch_tag = "2Dm3djetdrCorrection"
              w_fn_2d = "reweight_nopreselnobspnotw_tau%imm_M%02i_%i_2D.root" % (tau/1000, mg, year)
              w_fn_1d = "reweight_nopreselnobspnotw_tau%imm_M%02i_%i_1D.root" % (tau/1000, mg, year)
              
              correction_args = '--jet-decayweights true --w_fn_2d "%s" --w_fn_1d "%s" --tm "%s"' % (w_fn_2d, w_fn_1d, tm)
              w_fns = [w_fn_2d, w_fn_1d]
              #w_fns = []
              batch = 'TrackMoverNoPreSelNoBSPNotwJetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_M%02i_%s' % (nl, nb, tau, mg, batch_tag)
              args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
              NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=w_fns)
          else:
            #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=True)
            samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
            batch_tag = "noCorrection"
            correction_args = "--jet-decayweights false "
            batch = 'TrackMoverNoPreSelNoBSPNotwJetByJetHists' + version.capitalize() + '_%i%i_tau%06ium_%s' % (nl, nb, tau, batch_tag)
            args = '-t mfvMovedTree%i%i --tau %i %s' % (nl, nb, tau, correction_args) 
            NtupleReader_submit(batch, dataset, samples, exe_args=args, input_fns_extra=[])
