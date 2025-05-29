#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True #FIXME
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False #FIXME 
settings.keep_gen = True #FIXME needed to run histos currently :(
settings.keep_tk = False
#settings.event_filter = 'bjets OR displaced dijet veto leptons and HT' # for new trigger studies
settings.event_filter = 'leptons only'
"""
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
if use_btag_vetoLepHT_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto leptons and HT' # for new trigger studies
elif use_MET_triggers :
    settings.event_filter = 'met only'
elif use_Lepton_triggers :
    settings.event_filter = 'leptons only'
elif use_Muon_triggers :
    settings.event_filter = 'muons only' 
elif use_Electron_triggers :
    settings.mode = 'electrons only' #FIXME
elif use_Lepton_triggers :
    settings.mode = 'leptons only'
else :
    settings.event_filter = 'jets only'
"""
settings.randpars_filter = False
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M15_ct10-'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'ttbar_semilep_2018', dataset, 3)
#sample_files(process, 'mfv_stoplb_tau000300um_M0800_2018', dataset, 1)
#sample_files(process, 'SingleMuon2018D', dataset, 1)
#sample_files(process, 'test', dataset, 1)
#sample_files(process, 'qcdbctoept030_2018', dataset, 2)
sample_files(process, 'mfv_stopld_tau010000um_M0800_2018', dataset, 1)
#sample_files(process, 'mfv_stopld_tau010000um_M0800_20161', dataset, 1)
#sample_files(process, 'mfv_stopld_tau000100um_M1400_20162', dataset, 1)

max_events(process, 1000)
cmssw_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
       samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
       #samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False
    elif use_btag_vetoLepHT_triggers :
        #samples = [getattr(Samples, 'mfv_neu_tau001000um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_2017')]
        #samples = [getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2017')]

        if settings.is_mc :
            #samples = [getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2017')]
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=True, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
            #samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
        else :
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False

    elif use_MET_triggers :
       samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=True)
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
    elif use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=True, met=False, leptonic=True, ttbar=True, diboson=True, Zqq=False, Lepton_data=True)
        #samples = [getattr(Samples, 'mfv_stoplb_tau030000um_M0200_2018'), getattr(Samples, 'mfv_stoplb_tau001000um_M0300_2018'), getattr(Samples, 'mfv_stoplb_tau010000um_M0300_2018'), getattr(Samples, 'mfv_stoplb_tau000300um_M0400_2018'), getattr(Samples, 'mfv_stoplb_tau030000um_M0400_2018'), getattr(Samples, 'mfv_stoplb_tau000100um_M0600_2018'), getattr(Samples, 'mfv_stoplb_tau010000um_M0600_2018') ]
        #samples = [getattr(Samples, 'SingleMuon2018D')]
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)
        
        
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2016_EgammaMu.json'), limit_ttbar=False)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, bjet_trigger_veto_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
