# import FWCore.ParameterSet.Config as cms

# mfvCutFlowCuts = cms.EDFilter('MFVCutFlowCuts',
#                               mevent_src = cms.InputTag('mfvEvent'),
#                               apply_presel = cms.int32(2),
#                               #to make trigger cuts work, have to set presel = 0
#                               apply_trigger = cms.int32(0),
#                               apply_vertex_cuts = cms.bool(True),
#                               tk5_vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
#                               tk4_vertex_src = cms.InputTag('mfvSelectedVerticesTightMinNtk4'),
#                               tk3_vertex_src = cms.InputTag('mfvSelectedVerticesTightMinNtk3'),
#                               )

                             
