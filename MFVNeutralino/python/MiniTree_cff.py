import FWCore.ParameterSet.Config as cms

from JMTucker.MFVNeutralino.VertexSelector_cfi import *
from JMTucker.MFVNeutralino.AnalysisCuts_cfi import *
from JMTucker.MFVNeutralino.WeightProducer_cfi import *


#standard minitree analyzer
mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                             event_src = cms.InputTag('mfvEvent'),
                             vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                             weight_src = cms.InputTag('mfvWeight'),
                             save_tracks = cms.bool(True),
                             )

# THIS NEEDS A BIT MORE WORK

##########################################################################################
#modify the analysis cuts 
mfvAnalysisCutsGE1Vtx = mfvAnalysisCuts.clone(min_nvertex = 1, apply_displept_cuts = False)

#for displaced lepton studies : modified analysis cuts 
#mfvAnalysisCutsGE1Vtx_dxy = mfvAnalysisCuts.clone(min_nvertex = 1, apply_displept_cuts = True, min_dxy = 0.005)
#mfvAnalysisCutsGE1Vtx_seldxy = mfvAnalysisCuts.clone(min_nvertex = 1, min_seldxy = 0.005, min_dxy = 0.0)

mfvAnalysisCutsGE1Vtx_loose = mfvAnalysisCuts.clone(min_nvertex = 1, vertex_src = cms.InputTag('mfvSelectedVerticesLoose'))

#both requirement on displaced lepton and loose vertices
#mfvAnalysisCutsGE1Vtx_dxyl = mfvAnalysisCuts.clone(min_nvertex = 1, min_dxy = 0.005, vertex_src = cms.InputTag('mfvSelectedVerticesTight'))
                                                    
                                                    


##########################################################################################

#Modified analysis cuts for different vertex src to relax the track requirement
mfvAnalysisCutsGE1VtxMinNtk3   =  mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
mfvAnalysisCutsGE1VtxMinNtk4   =  mfvAnalysisCutsGE1Vtx.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')

mfvAnalysisCutsGE1VtxMinNtk3_loose   =  mfvAnalysisCutsGE1Vtx_loose.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvAnalysisCutsGE1VtxMinNtk4_loose   =  mfvAnalysisCutsGE1Vtx_loose.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')

#now do the same but for displaced lepton studies
#mfvAnalysisCutsGE1VtxMinNtk3_dxy = mfvAnalysisCutsGE1Vtx_dxy.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
#mfvAnalysisCutsGE1VtxMinNtk3_seldxy = mfvAnalysisCutsGE1Vtx_seldxy.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
#mfvAnalysisCutsGE1VtxMinNtk3_dxyl = mfvAnalysisCutsGE1Vtx_dxyl.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')

#mfvAnalysisCutsGE1VtxMinNtk4_dxy = mfvAnalysisCutsGE1Vtx_dxy.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')
# mfvAnalysisCutsGE1VtxMinNtk4_seldxy = mfvAnalysisCutsGE1Vtx_seldxy.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')
#mfvAnalysisCutsGE1VtxMinNtk4_dxyl = mfvAnalysisCutsGE1Vtx_dxy.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')


##########################################################################################

#Modified minitree for different vertex src
mfvMiniTreeMinNtk3    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
mfvMiniTreeMinNtk4    = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')

mfvMiniTreeMinNtk3_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
mfvMiniTreeMinNtk4_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')


#mfvMiniTreeMinNtk3_dxy = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
#mfvMiniTreeMinNtk4_dxy = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')

#mfvMiniTreeMinNtk3_dxyl = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3')
#mfvMiniTreeMinNtk4_dxyl = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk4')

# mfvMiniTreeMinNtk3_seldxy = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk3')
# mfvMiniTreeMinNtk4_seldxy = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesTightMinNtk4')

mfvMiniTree_loose = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLoose')
#mfvMiniTree_dxy = mfvMiniTree.clone()
#mfvMiniTree_dxyl = mfvMiniTree.clone(vertex_src = 'mfvSelectedVerticesLoose')

# mfvMiniTree_seldxy = mfvMiniTree.clone()


#full path with weight, vertex src, analysis cuts, analyzer 
pMiniTree = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCutsGE1Vtx * mfvMiniTree)

#Modified path with weight, vertex src, analysis cuts, analyzer 
pMiniTreeMinNtk3    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk3    * mfvAnalysisCutsGE1VtxMinNtk3    * mfvMiniTreeMinNtk3)
pMiniTreeMinNtk4    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk4    * mfvAnalysisCutsGE1VtxMinNtk4    * mfvMiniTreeMinNtk4)


pMiniTree_loose = cms.Path(mfvWeight * mfvSelectedVerticesLoose *mfvAnalysisCutsGE1Vtx_loose  * mfvMiniTree_loose)
pMiniTreeMinNtk3_loose = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk3 *mfvAnalysisCutsGE1VtxMinNtk3_loose  * mfvMiniTreeMinNtk3_loose)
pMiniTreeMinNtk4_loose = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk4 *mfvAnalysisCutsGE1VtxMinNtk4_loose  * mfvMiniTreeMinNtk4_loose)
#Modified path for displaced lepton

#pMiniTree_dxy = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCutsGE1Vtx_dxy * mfvMiniTree_dxy)
#pMiniTree_dxyl = cms.Path(mfvWeight * mfvSelectedVerticesLoose * mfvAnalysisCutsGE1Vtx_dxyl * mfvMiniTree_dxyl)
# pMiniTree_seldxy = cms.Path(mfvWeight * mfvSelectedVerticesTight * mfvAnalysisCutsGE1Vtx_seldxy * mfvMiniTree_seldxy)

#pMiniTreeMinNtk3_dxy    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk3    * mfvAnalysisCutsGE1VtxMinNtk3_dxy    * mfvMiniTreeMinNtk3_dxy)
#pMiniTreeMinNtk3_dxyl    = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk3    * mfvAnalysisCutsGE1VtxMinNtk3_dxyl    * mfvMiniTreeMinNtk3_dxyl)

# pMiniTreeMinNtk3_seldxy    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk3    * mfvAnalysisCutsGE1VtxMinNtk3_seldxy    * mfvMiniTreeMinNtk3_seldxy)

#pMiniTreeMinNtk4_dxy    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk4    * mfvAnalysisCutsGE1VtxMinNtk4_dxy    * mfvMiniTreeMinNtk4_dxy)
#pMiniTreeMinNtk4_dxyl    = cms.Path(mfvWeight * mfvSelectedVerticesLooseMinNtk4    * mfvAnalysisCutsGE1VtxMinNtk4_dxyl    * mfvMiniTreeMinNtk4_dxyl)

# pMiniTreeMinNtk4_seldxy    = cms.Path(mfvWeight * mfvSelectedVerticesTightMinNtk4    * mfvAnalysisCutsGE1VtxMinNtk4_seldxy    * mfvMiniTreeMinNtk4_seldxy)
