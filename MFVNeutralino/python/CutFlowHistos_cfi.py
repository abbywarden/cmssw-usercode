import FWCore.ParameterSet.Config as cms

mfvCutFlowHistos = cms.EDAnalyzer('MFVCutFlowHistos',
                                  mevent_src = cms.InputTag('mfvEvent'),
                                  # tk5_vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                  # tk4_vertex_src = cms.InputTag('mfvSelectedVerticesTightMinNtk4'),
                                  # tk3_vertex_src = cms.InputTag('mfvSelectedVerticesTightMinNtk3'),
                                  vertex_aux_src = cms.InputTag('mfvVerticesAux'),
                                  )
