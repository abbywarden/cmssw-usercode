import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.MFVNeutralino.NtupleCommon import use_btag_triggers, signal_uses_random_pars_modifier

settings = CMSSWSettings()
settings.is_mc = True
settings.cross = ''

randpars_filter = False
#for local test
#randpars_filter = 'randpar HToSSTodddd M15_ct10-'

max_events(process, 1000)
report_every(process, 1000000)
geometry_etc(process, which_global_tag(settings))
tfileservice(process, 'tracker_mapper.root')
<<<<<<< Updated upstream
#ww_2018, wjetstolnu_ht0400_2018, qcdempt170_2018, mfv_stopld_tau010000um_M1600_2018, mfv_stopld_tau100000um_M0600_2018
#sample_files(process, 'mfv_stopld_tau010000um_M1200_2018', 'miniaod')
sample_files(process, 'ZH_HToSSTodddd_ZToll_tau010000um_M15_2018', 'miniaod')
=======
#sample_files(process, 'qcdht0200_2017', 'miniaod')
sample_files(process, 'qcdmupt15_2017', 'miniaod')
>>>>>>> Stashed changes
file_event_from_argv(process)
#want_summary(process)

process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
process.load('JMTucker.Tools.GenParticleFilter_cfi')
process.load('JMTucker.Tools.MCStatProducer_cff')
process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
process.load('JMTucker.Tools.WeightProducer_cfi')

process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
process.goodOfflinePrimaryVertices.filter = True

process.jmtGenParticleFilter.gen_particles_src = 'prunedGenParticles'

process.lightFlavor = process.jmtGenParticleFilter.clone(max_flavor_code = 0)
process.heavyFlavor = process.jmtGenParticleFilter.clone(min_flavor_code = 1)
process.bFlavor = process.jmtGenParticleFilter.clone(min_flavor_code = 2)
process.displacedGenPV = process.jmtGenParticleFilter.clone(min_pvrho = 0.0036)

process.TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                                       track_src = cms.InputTag('jmtUnpackedCandidateTracks'),
                                       heavy_flavor_src = cms.InputTag(''),
                                       beamspot_src = cms.InputTag('offlineBeamSpot'),
                                       primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                       weight_src = cms.InputTag('jmtWeightMiniAOD'),
                                       use_duplicateMerge = cms.int32(-1),
                                       old_stlayers_cut = cms.bool(False),
                                       )

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
if use_btag_triggers :
    event_filter = setup_event_filter(process,
                              path_name = '',
                              trigger_filter = 'bjets OR displaced dijet veto HT',
                              event_filter = 'bjets OR displaced dijet veto HT',
                              event_filter_jes_mult = 0,
                              event_filter_require_vertex = False,
                              input_is_miniaod = True)

# try : turn off trigger filter
# turn off event filter 
else :
    # event_filter = setup_event_filter(process,
    #                           path_name = '',
    #                           trigger_filter = 'jets only',
    #                           event_filter = 'jets only',
    #                           event_filter_jes_mult = 0,
    #                           event_filter_require_vertex = False,
    #                           input_is_miniaod = True)
    event_filter = setup_event_filter(process,
<<<<<<< Updated upstream
                                path_name = '',
                                trigger_filter = 'displeptons OR leptons',
                                #trigger_filter = False,      
                                event_filter = 'leptons only',
                                #event_filter = False,
                                event_filter_jes_mult = 0,
                                event_filter_require_vertex = False,
                                input_is_miniaod = True,
                                rp_mode = randpars_filter)

=======
                              path_name = '',
                             # trigger_filter = 'jets only',
                             # event_filter = 'jets only',
                              trigger_filter = 'leptons only',
                              event_filter = 'leptons only',
                              event_filter_jes_mult = 0,
                              event_filter_require_vertex = False,
                              input_is_miniaod = True)
>>>>>>> Stashed changes

common = cms.Sequence(event_filter * process.goodOfflinePrimaryVertices * process.jmtUnpackedCandidateTracks * process.jmtWeightMiniAOD)

if False:
    process.load('JMTucker.Tools.RescaledTracks_cfi')
    process.jmtRescaledTracks.tracks_src = 'jmtUnpackedCandidateTracks'
    common *= process.jmtRescaledTracks
    process.TrackerMapper.track_src = 'jmtRescaledTracks'

process.p = cms.Path(common * process.TrackerMapper)

for name, filt in ('LightFlavor', process.lightFlavor), ('HeavyFlavor', process.heavyFlavor): #, ('BFlavor', process.bFlavor), ('DisplacedGenPV', process.displacedGenPV):
    tk = process.TrackerMapper.clone()
    if name == 'HeavyFlavor':
        tk.heavy_flavor_src = cms.InputTag('heavyFlavor', 'heavyFlavor')
    setattr(process, 'TrackerMapper%s' % name, tk)
    setattr(process, 'p%s' % name, cms.Path(common * filt * tk))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.Year import year

    dataset = 'miniaod'

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=False, data=False, bjet=False, span_signal=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
<<<<<<< Updated upstream
        samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=False, diboson=False, wjet=False, leptonic=False, drellyan=True, data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), signal_uses_random_pars_modifier)
=======
        samples = pick_samples(dataset, all_signal=False, data=False, qcd_lept=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
>>>>>>> Stashed changes

    set_splitting(samples, 'miniaod', 'default', json_path('ana_2017_1pc.json'), 16)

    outputname = 'TrackerMapper'
    if use_btag_triggers :
        outputname += 'BtagTriggered'
    outputname += 'V1'
    ms = MetaSubmitter(outputname, dataset=dataset)
    ms.common.pset_modifier = pset_modifier
    ms.condor.stageout_files = 'all'
    ms.submit(samples)
