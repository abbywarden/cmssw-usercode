import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvEvent = cms.EDProducer('MFVEventProducer',
                          input_is_miniaod = cms.bool(False),
                          packed_candidates_src = cms.InputTag('packedPFCandidates'),
                          triggerfloats_src = cms.InputTag('mfvTriggerFloats'),
                          beamspot_src = cms.InputTag('offlineBeamSpot'),
                          primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                          gen_info_src = cms.InputTag('generator'),
                          gen_jets_src = cms.InputTag('ak4GenJetsNoNu'),
                          gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
                          gen_particles_src = cms.InputTag('genParticles'),
                          mci_src = cms.InputTag('mfvGenParticles'),
                          pileup_info_src = cms.InputTag('addPileupInfo'),
                          jets_src = cms.InputTag('selectedPatJets'),
                          rho_src = cms.InputTag('fixedGridRhoFastjetAll'),
                          met_src = cms.InputTag('patMETsNoHF'),
                          muons_src = cms.InputTag('selectedPatMuons'),
                          electrons_src = cms.InputTag('selectedPatElectrons'),
                          electron_effective_areas = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'),
                          vertex_seed_tracks_src = cms.InputTag('mfvVertices', 'seed'),
                          misc_srcs = cms.VInputTag(cms.InputTag('prefiringweight', "NonPrefiringProb"),
                                                    cms.InputTag('prefiringweight', "NonPrefiringProbUp"),
                                                    cms.InputTag('prefiringweight', "NonPrefiringProbDown"),
                                                    ),
                          lightweight = cms.bool(False),
                          )
