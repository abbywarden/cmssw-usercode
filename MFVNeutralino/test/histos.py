from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.Year import year

is_mc = True # for blinding
do_track = False # this can onlky be used for ntuple with keep_tk=True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers, use_Muon_triggers, use_Electron_triggers, use_Lepton_triggers
#currently : keep histos slim -> do only Loose Vertices & NoCuts, Minntk = 3, 4, 5 
#update : Selected Loose Vertices are changed to Tight Vertices
#input_files(process, '/eos/uscms/store/group/lpclonglived/pkotamni/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/NtupleOffdzULV30LepMum_2017/240131_215245/0000/ntuple_0.root')
#max_events(process, 100)

dataset += '_wgen'

#sample_files(process, 'qcdmupt15_2017' if is_mc else 'JetHT2017B', dataset, 10)
#sample_files(process, 'mfv_stopld_tau010000um_M0200_2018' if is_mc else 'SingleMuon2017B', dataset, 2)
sample_files(process, 'mfv_stoplb_tau000300um_M0300_2017' if is_mc else 'SingleMuon2017B', dataset, 2)
#sample_files(process, 'test', dataset, 1)
#sample_files(process, 'ttbar_semilep_2018' if is_mc else 'SingleMuon2017B', dataset, 3)
#sample_files(process, 'SingleMuon2018B', dataset, 1)

tfileservice(process, 'histos.root')
global_tag(process)
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.TrackHistos_cfi')
process.load('JMTucker.MFVNeutralino.FilterHistos_cfi')
process.load('JMTucker.MFVNeutralino.JetTksHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.CutFlowHistos_cfi')

import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)

## comment out when running data
#common_a= cms.Sequence(process.mfvWeight)
#process.CutFlowHistos = cms.Path(common_a * process.mfvCutFlowHistos)

process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.mfvVertexHistosNoCutsNtk3 = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLooseNtk3')
#process.mfvVertexHistosNoCutsMinNtk3 = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose') ## COMMENT OUT WHEN RUN DATA

########process.pSkimSelVtx = cms.Path(common * process.mfvVertexHistosNoCuts)

process.pSkimSelNtk3 = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvVertexHistosNoCutsNtk3) # just trigger
#process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts * process.mfvVertexHistosNoCutsMinNtk3) # just trigger  ## COMMENT OUT WHEN RUN DATA


process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)
process.mfvEventHistosPreSel = process.mfvEventHistos.clone()

#process.mfvVertexHistosPreSelMinNtk3 = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesExtraLoose') ##COMMENT OUT WHEN RUN DATA
#process.pPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel * process.mfvVertexHistosPreSelMinNtk3) # w/ event presel but no vertex cuts; ## COMMENT OUT WHEN RUN DATA

##### COMMENT OUT WHEN NOT RUNNING DATA 
##### process.mfvAnalysisCutsSel = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesLoose', min_nvertex = 1)
##### process.mfvEventHistosSel = process.mfvEventHistos.clone()
##### process.mfvVertexHistosSel = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesLoose')


process.mfvAnalysisCutsSelNtk3 = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesLooseNtk3', min_nvertex = 1)
#process.mfvAnalysisCutsSelMinNtk3 = process.mfvAnalysisCuts.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3', min_nvertex = 1) ##COMMENT OUT WHEN RUN DATA

process.mfvEventHistosSel = process.mfvEventHistos.clone()
process.mfvVertexHistosSelNtk3 = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesLooseNtk3')
#process.mfvVertexHistosSelMinNtk3 = process.mfvVertexHistos.clone(vertex_src = 'mfvSelectedVerticesLooseMinNtk3') ##COMMENT OUT WHEN RUN DATA

process.pSelNtk3 = cms.Path(common * process.mfvAnalysisCutsSelNtk3 * process.mfvEventHistosSel * process.mfvVertexHistosSelNtk3) # w/ event presel and vertex cuts 
#process.pSelMinNtk3 = cms.Path(common * process.mfvAnalysisCutsSelMinNtk3 * process.mfvEventHistosSel * process.mfvVertexHistosSelMinNtk3) # w/ event presel and vertex cuts  ##COMMENT OUT WHEN RUN DATA



nm1s = [
   ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
   ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
   ]


ntks = [3]
#ntks = [3,4]
nvs = [0,1]
#EX1 = 'Ntk3'
#EX2 = "vertex_src = 'mfvSelectedVerticesLoose%s', " % EX1
for ntk in ntks:
    if ntk == 3:
        EX1 = 'Ntk3'
    else: 
        #EX1 = 'MinNtk%i' % ntk #when not going over data 
        EX1 = 'MinNtk3' #when not going over data 
    # EX1 = 'Ntk%i'

    if EX1:
        EX2 = "vertex_src = 'mfvSelectedVerticesLoose%s', " % EX1

    exec '''
process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel * process.EX1mfvVertexHistosPreSel)

'''.replace('EX1', EX1).replace('EX2', EX2)

    # exec '''
    # # process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)

    # # process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
    # # process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
    # # process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

    # process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2) 
    # # process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
    # # process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
    # # process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

    # process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)

    # # process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
    # '''.replace('EX1', EX1).replace('EX2', EX2) 

    for name, cut in nm1s:
        evt_cut = ''
        if type(cut) == tuple:
            cut, evt_cut = cut

        vtx = eval('process.mfvSelectedVerticesLoose%s.clone(%s)' % (EX1, cut))
        vtx_name = '%svtxNo' % EX1 + name

        for nv in nvs:
            if nv == 0 and (cut != '' or EX1 != ''):
                continue

            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
            ana.vertex_src = vtx_name
            ana.min_nvertex = nv
            # if nv == 1:
            #     ana.max_nvertex = nv
            # ana.min_nvertex = nv
            # if nv == 2 and ntk == 7:
            #     ana.min_ntracks01 = ana.max_ntracks01 = 7
            # if nv == 2 and ntk == 8:
            #     ana.ntracks01_0 = 5
            #     ana.ntracks01_1 = 3
            # if nv == 2 and ntk == 9:
            #     ana.ntracks01_0 = 5
            #     ana.ntracks01_1 = 4
            ana_name = '%sana%iVNo' % (EX1, nv) + name

            evt_hst = process.mfvEventHistos.clone()
            evt_hst_name = '%sevtHst%iVNo' % (EX1, nv) + name

            vtx_hst = process.mfvVertexHistos.clone(vertex_src = vtx_name)
            vtx_hst_name = '%svtxHst%iVNo' % (EX1, nv) + name

            setattr(process, vtx_name, vtx)
            setattr(process, ana_name, ana)
            setattr(process, evt_hst_name, evt_hst)
            setattr(process, vtx_hst_name, vtx_hst)
            setattr(process, '%sp%iV' % (EX1, nv) + name, cms.Path(process.mfvWeight * vtx * ana * evt_hst * vtx_hst))

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = Samples.DisplacedJet_data_samples_2016APV + Samples.qcd_samples_2016APV
        #samples = Samples.ttbar_alt_samples_2016APV + Samples.MuonEG_data_samples_2016APV + Samples.ttbar_samples_2016APV + Samples.DisplacedJet_data_samples_2016APV + Samples.SingleMuon_data_samples_2016APV + Samples.qcd_samples_2016APV
        samples = Samples.all_signal_samples_2016
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers:
        #samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
    elif use_Lepton_triggers : 
        samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=False, qcd_lep = False, leptonic=False, met=False, diboson=False, Zqq=False, Lepton_data=True )
        #samples = [getattr(Samples, 'mfv_stopld_tau001000um_M0300_2017'), getattr(Samples, 'mfv_stopld_tau001000um_M0600_2017'), getattr(Samples, 'mfv_stopld_tau001000um_M1000_2017'), getattr(Samples, 'mfv_stopld_tau001000um_M1600_2017'), getattr(Samples, 'mfv_stopld_tau000100um_M1000_2017'), getattr(Samples, 'mfv_stopld_tau010000um_M1000_2017'), ] 
        #samples = [getattr(Samples, 'qcdempt020_2018'), getattr(Samples, 'mfv_stopld_tau001000um_M0600_2018')]
        #samples = [getattr(Samples, 'ttbar_semilep_2018')]
        
        pset_modifier = chain_modifiers(is_mc_modifier)
    elif use_Muon_triggers :
        #samples = pick_samples(dataset, qcd=True, all_signal=True, qcd_lep = True, leptonic=True, met=True, diboson=True, Lepton_data=False )
        #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=True, met=True, diboson=True, Lepton_data=False)
        #samples = pick_samples(dataset, all_signal=True)
        #samples = [getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_2017')] 
        pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier())
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, all_signal=False, qcd_lep = False, leptonic=False, met=False, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier())
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())


    #set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'))
    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017_EgammaMu.json'))

    cs = CondorSubmitter('Histos' + version + '_SingleLep',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
