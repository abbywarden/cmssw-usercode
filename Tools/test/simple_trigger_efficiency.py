import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, file_event_from_argv

#file_event_from_argv(process)
#stopBL_M_100_CTau_1000mm 

#from stopBL_samples import *



#inputFiles = stopBL_M400_CTau_0p1mm 
inputFiles = '/store/mc/RunIIAutumn18MiniAOD/ZH_HToSSTo4Tau_ZToLL_MH-125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/rp_102X_upgrade2018_realistic_v15-v1/20000/2627F944-796D-8F48-AAD6-081FC007914F.root'

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(inputFiles),
    #fileNames = cms.untracked.vstring(process),
)
#process.TFileService.fileName = 'stopBL_M400_CTau_0p1mm.root'
process.TFileService.fileName = 'ZH_HToSSTodddd_test.root'

process.RandomNumberGeneratorService = cms.Service('RandomNumberGeneratorService')
process.RandomNumberGeneratorService.SimpleTriggerEfficiency = cms.PSet(initialSeed = cms.untracked.uint32(1219))

#import prescales
process.load('JMTucker.Tools.SimpleTriggerEfficiency_cfi')
process.SimpleTriggerEfficiency.prescale_paths  = cms.vstring()  #*prescales.prescales.keys()),
process.SimpleTriggerEfficiency.prescale_values = cms.vuint32()  #*[o for l,h,o in prescales.prescales.itervalues()]),

process.p = cms.Path(process.SimpleTriggerEfficiency)


for x in sys.argv:
    if x.startswith('process='):
        process_name = x.replace('process=', '')
        process.SimpleTriggerEfficiency.trigger_results_src = cms.InputTag('TriggerResults', '', process_name)
