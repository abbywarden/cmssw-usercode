import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *

#mfvAnalysisCutsGE1Vtx_Extraloose = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = 'mfvSelectedVerticesExtraLoose')
#mfvAnalysisCutsGE1Vtx_Extraloose_wDispLep = mfvAnalysisCuts.clone(apply_displacedlepton_triggers = True, min_nvertex = 1, vertex_src = 'mfvSelectedVerticesExtraLoose')

#mfvAnalysisCutsGE1VtxwLep_Extraloose = mfvAnalysisCuts.clone(min_nvertex = 1, min_nvertex_wlep = 1, vertex_src = 'mfvSelectedVerticesExtraLoose')
mfvAnalysisCutsGE1Vtx_Standard = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = 'mfvSelectedVerticesLoose')
#mfvAnalysisCutsGE1Vtx_Standard = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = 'mfvSelectedVerticesLooseNtk3') #for data

#mfvAnalysisCutsGE1Vtx_Orig = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = 'mfvSelectedVerticesTight')


mfvMiniTree = cms.EDAnalyzer('MFVMiniTreerBDT',
                             event_src = cms.InputTag('mfvEvent'),
                             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                             weight_src = cms.InputTag('mfvWeight'),
                             do_genmatching = cms.bool(False), #should only turn on for signal to train. turn off and run signal again for the full evaluation? turned on will only work for signal; may need rework?
                             )


#apply bs2derr & bs2ddist at this level to reduce large amounts of ttbar (will have to also change other files...)
#mfvMiniTree_Extraloose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
#mfvMiniTree_Extraloose_wDispLep = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesExtraLoose')
#pMiniTree_loose = cms.Path(mfvWeight * mfvSelectedVerticesExtraLoose *mfvAnalysisCutsGE1Vtx_Extraloose  * mfvMiniTree_Extraloose)
#pMiniTree_loose_wDispLep = cms.Path(mfvWeight * mfvSelectedVerticesExtraLoose *mfvAnalysisCutsGE1Vtx_Extraloose_wDispLep  * mfvMiniTree_Extraloose_wDispLep)

#mfvAnalysisCutsGE1VtxMinNtk4_standard = mfvAnalysisCutsGE1Vtx_Standard.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')

#my slightly looser vertex selections
#mfvMiniTree_Standard = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseNtk3') #for data
mfvMiniTree_Standard = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLoose')

#pMiniTree_standard = cms.Path(mfvWeight * mfvSelectedVerticesLooseNtk3 *mfvAnalysisCutsGE1Vtx_Standard  * mfvMiniTree_Standard) #for data
pMiniTree_standard = cms.Path(mfvWeight * mfvSelectedVerticesLoose *mfvAnalysisCutsGE1Vtx_Standard  * mfvMiniTree_Standard)

# the previous analysis vertex selections 
#pMiniTree_orig = cms.Path(mfvWeight * mfvSelectedVerticesTight *mfvAnalysisCutsGE1Vtx_Orig  * mfvMiniTree)