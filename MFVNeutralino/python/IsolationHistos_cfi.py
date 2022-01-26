import FWCore.ParameterSet.Config as cms

mfvIsolationHistos = cms.EDAnalyzer('MFVIsolationHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                              
                                )
