#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
elif use_Lepton_triggers :
    settings.event_filter = 'leptons only'
# #elif use_Lept_and_Disp_triggers :
# #    settings.event_filter = 'leptons and displaced leptons only'
else :
    settings.event_filter = 'jets only'

    
#settings.rp_filter = 'True'
settings.rp_mode = 'randpar M15_ct10-'
#this_rp_mode = 'randpar M15_ct10-'


process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'ZH_HToSSTodddd_ZToLL_tau010000um_M15_2018', dataset, 1)
#sample_files(process, 'qcdht1000_2018', dataset, 1)
max_events(process, 5000)
cmssw_from_argv(process)

# from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
# sef = lambda *a,**kwa: setup_event_filter(process, *a, input_is_miniaod=True, rp_mode = this_rp_mode, **kwa)
# sef('pTriggerLeptons', mode = 'trigger leptons only', name_ex = 'leptons')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=not settings.run_n_tk_seeds, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
    if use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, wjet=False, diboson=False, drellyan=False, all_signal = True, leptonic = False, data=False)
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, signal_uses_random_pars_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

