import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import signal_uses_random_pars_modifier

settings = CMSSWSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.cross = '' # 2017to2018' # 2017to2017p8'

#for local test
# 10 -> 10mm
# 0.05 -> 50um 
#randpars_filter = 'randpar HToSSTodddd M07_ct0p05-'

#for submission to condor
randpars_filter = False

sample_files(process, 'qcdht1000_2018', 'miniaod')
#sample_files(process, 'ZH_HToSSTodddd_ZToll_tau000050um_M15_2018', 'miniaod')
geometry_etc(process, settings)
tfileservice(process, 'filtercheck.root')
cmssw_from_argv(process)


from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
sef = lambda *a,**kwa: setup_event_filter(process, *a, input_is_miniaod=True, rp_mode = randpars_filter,  **kwa)
sef('pTrigger', mode = 'trigger jets only')
sef('pTriggerBjets', mode = 'trigger bjets only',name_ex = 'bjets')
sef('pTriggerDispDijet', mode = 'trigger displaced dijet only',name_ex = 'displaced_dijet')
sef('pTriggerOR', mode = 'trigger HT OR bjets OR displaced dijet', name_ex = 'HT_OR_bjets_OR_displaced_dijet')
#sef('pJets',    mode = 'jets only novtx',   name_ex = 'NoVtx') # be sure to generate a different name for each subsequent use
#sef('pNoJESUp', mode = 'jets only novtx',   name_ex = 'NoJESUp', event_filter_jes_mult = 0)
#sef('pFull',    mode = 'jets only',         name_ex = 'Full') # uncomment to get efficiency of ntuple-level vertex filter
sef('pTriggerLeptons', mode = 'trigger leptons only', name_ex = 'leptons')
sef('pTriggerDispLeptons', mode = 'trigger displaced leptons', name_ex = 'displaced_leptons')


sef('pTriggerDiLeptons', mode = 'trigger dileptons', name_ex = 'dileptons')

sef('pTriggerDispLeptonsORLeptons', mode = 'DispLeptons OR Single Leptons', name_ex = 'displeptons_OR_lepton')

#sef('pTriggerDispLeptonsORDiLeptons', mode = 'DispLeptons OR DiLeptons', name_ex = 'displeptons_OR_dileptons')
sef('pTriggerLeptonsORDiLeptons', mode = 'DiLeptons OR Single Leptons', name_ex = 'lepton_OR_dileptons')


# #all the singles; first lepton
# sef('pTriggerEle32', mode = 'Ele32', name_ex = 'ele32')
# sef('pTriggerEle35', mode = 'Ele35', name_ex = 'ele35')
# sef('pTriggerEle115', mode = 'Ele115', name_ex = 'ele115')
# sef('pTriggerEle50', mode = 'Ele50', name_ex = 'ele50')
# sef('pTriggerIsoMu24', mode = 'IsoMu24', name_ex = 'isomu24')
# sef('pTriggerIsoMu27', mode = 'IsoMu27', name_ex = 'isomu27')
# sef('pTriggerMu50', mode = 'Mu50', name_ex = 'mu50')

# #displaced lepton
# sef('pTriggerMu43Photon43', mode = 'Mu43Photon43', name_ex = 'mu43photon43')
# sef('pTriggerDiPhoton30_22', mode = 'DiPhoton30_22', name_ex = 'diphoton30_22')
# sef('pTriggerDoublePhoton70', mode = 'DoublePhoton70', name_ex = 'doublephoton70')
# sef('pTriggerDoubleMu43', mode = 'DoubleMu43', name_ex = 'doublemu43')



if len(process.mfvTriggerFilter.HLTPaths) > 1:
    for x in process.mfvTriggerFilter.HLTPaths:
        filt_name = ''.join(x.split('_')[1:-1])
        sef('p%s' % filt_name, name_ex=x)
        print x
        getattr(process, filt_name).HLTPaths = [x]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process, randpars_filter)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.mfv_stoplb_samples_2017 + Samples.mfv_stopld_samples_2017
        #have not yet added 2017 samples 
    elif year == 2018:
        samples = Samples.mfv_stoplb_samples_2018 + Samples.mfv_stopld_samples_2018
       # samples = Samples.ZH_HToSSTodddd_ZToLL_samples_2018 + Samples.ZH_HToSSTobbbb_ZToLL_samples_2018 + Samples.ZH_HToSSTo4Tau_ZToLL_samples_2018
        
    ms = MetaSubmitter('TrigFiltCheckV1_lept', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), per_sample_pileup_weights_modifier(cross=settings.cross), signal_uses_random_pars_modifier)
    ms.submit(samples)
