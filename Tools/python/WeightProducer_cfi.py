import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.PileupWeights import get_pileup_weights
import os 
from JMTucker.Tools.Year import year

if (year == 2018) :
    pujson_path = '/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/LUM/2018_UL/puWeights.json.gz'
elif (year == 2017) : 
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/17UL/puWeights.json.gz')
elif (year == 20161) :
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/161UL/puWeights.json.gz')
elif (year == 20162) :
    pujson_path = os.path.join(os.environ['CMSSW_BASE'], 'src/JMTucker/MFVNeutralino/python/central_jsons/PU_json/162UL/puWeights.json.gz')
else :
    print("NO YEAR MATCHED; YEARS ARE 2018, 2017, 20161, and 20162")
    

jmtWeight = cms.EDProducer('JMTWeightProducer',
                           enable = cms.bool(True),
                           prints = cms.untracked.bool(False),
                           histos = cms.untracked.bool(True),
                           gen_info_src = cms.InputTag('generator'),
                           pileup_info_src = cms.InputTag('addPileupInfo'),
                           primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                           weight_gen = cms.bool(True),
                           weight_gen_sign_only = cms.bool(False),
                           weight_pileup = cms.bool(False), #new May25 2025 -> turn off 
                           weight_pileup_2 = cms.bool(True), #using central values from json 
                           pujson = cms.string(pujson_path),
                           pileup_weights = cms.vdouble(*get_pileup_weights('default')),
                           weight_npv = cms.bool(False),
                           npv_weights = cms.vdouble(),
                           weight_misc = cms.bool(False),
                           misc_srcs = cms.VInputTag(),
                           )

jmtWeightMiniAOD = jmtWeight.clone(
    pileup_info_src = 'slimmedAddPileupInfo',
    primary_vertex_src = 'offlineSlimmedPrimaryVertices'
    )
