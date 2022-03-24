from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

#from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_Lepton_triggers

#dataset = dataset + '_noef'
#version = version + '_NoEF'
#version = version + '_loose'
#as of Jan20th making sure the lepton pt matches with what trigger was fired (see AnalysisCuts; satisfiesLepTrigger)
# also have standard iso cuts for leptons 
version = version + '_fullsel'



#sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
#sample_files(process, 'mfv_stoplb_tau010000um_M1000_2018', dataset, 1)
sample_files(process, 'ZH_HToSSTodddd_ZToll_tau001000um_M40_2018', dataset, 1)

tfileservice(process, 'histos.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexHistos_cfi')
process.load('JMTucker.MFVNeutralino.EventHistos_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.CutFlowHistos_cfi')
#process.load('JMTucker.MFVNeutralino.IsolationHistos_cfi')


import JMTucker.Tools.SimpleTriggerResults_cfi as SimpleTriggerResults
SimpleTriggerResults.setup_endpath(process, weight_src='mfvWeight')

common = cms.Sequence(process.mfvSelectedVerticesSeq * process.mfvWeight)
common_a = cms.Sequence(process.mfvWeight)
process.mfvEventHistosNoCuts = process.mfvEventHistos.clone()
process.pSkimSel = cms.Path(common * process.mfvEventHistosNoCuts) # just trigger for now

process.mfvEventHistosPreSel = process.mfvEventHistos.clone()
process.mfvAnalysisCutsPreSel = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False) #, apply_displept_cuts = False)

#process.mfvIsolationHistosPreSel = process.mfvIsolationHistos.clone()
#process.mfvAnalysisCutsPreSelIso = process.mfvAnalysisCuts.clone(apply_vertex_cuts = False)

# process.mfvEventHistosPreSelNoJet = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSelNoJet = process.mfvAnalysisCuts.clone(min_njets = cms.int32(0), apply_vertex_cuts = False)


#process.mfvEventHistosPreSelNoLep = process.mfvEventHistos.clone()
#process.mfvAnalysisCutsPreSelNoLep = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_vertex_cuts = False)

# only trigger applied
# process.mfvEventHistosPreSelEl = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSelEl = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_singleel_trig = True, apply_vertex_cuts = False)
# process.mfvEventHistosPreSelMu = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSelMu = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_singlemu_trig = True, apply_vertex_cuts = False)
# process.mfvEventHistosPreSel2El = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSel2El = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_doubleel_trig = True, apply_vertex_cuts = False)
# process.mfvEventHistosPreSel2Mu = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSel2Mu = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_doublemu_trig = True, apply_vertex_cuts = False)
# process.mfvEventHistosPreSelMuEl = process.mfvEventHistos.clone()
# process.mfvAnalysisCutsPreSelMuEl = process.mfvAnalysisCuts.clone(apply_lept_cuts = False, apply_doublemuel_trig = True, apply_vertex_cuts = False)

#process.mfvEventHistosPreSelNoDxy = process.mfvEventHistos.clone()
#process.mfvAnalysisCutsPreSelNoDxy = process.mfvAnalysisCuts.clone(apply_displept_cuts = False, apply_vertex_cuts = False)

process.mfvAnaCutFlowHistos = process.mfvCutFlowHistos.clone()


process.pCutFlow = cms.Path(common_a * process.mfvAnaCutFlowHistos)
process.pEventPreSel = cms.Path(common * process.mfvAnalysisCutsPreSel * process.mfvEventHistosPreSel)
#process.pIsoPreSel = cms.Path(common * process.mfvAnalysisCutsPreSelIso * process.mfvIsolationHistosPreSel)

#process.pEventPreSelNoJet = cms.Path(common * process.mfvAnalysisCutsPreSelNoJet * process.mfvEventHistosPreSelNoJet)
#process.pEventPreSelNoLep = cms.Path(common * process.mfvAnalysisCutsPreSelNoLep * process.mfvEventHistosPreSelNoLep)

# process.pEventPreSelEl = cms.Path(common * process.mfvAnalysisCutsPreSelEl * process.mfvEventHistosPreSelEl)
# process.pEventPreSelMu = cms.Path(common * process.mfvAnalysisCutsPreSelMu * process.mfvEventHistosPreSelMu)
# process.pEventPreSel2El = cms.Path(common * process.mfvAnalysisCutsPreSel2El * process.mfvEventHistosPreSel2El)
# process.pEventPreSel2Mu = cms.Path(common * process.mfvAnalysisCutsPreSel2Mu * process.mfvEventHistosPreSel2Mu)
# process.pEventPreSelMuEl = cms.Path(common * process.mfvAnalysisCutsPreSelMuEl * process.mfvEventHistosPreSelMuEl)





#process.pEventPreSelNoDxy = cms.Path(common * process.mfvAnalysisCutsPreSelNoDxy * process.mfvEventHistosPreSelNoDxy)



nm1s = [
    ('Bsbs2ddist', 'min_bsbs2ddist = 0'),
    ('Bs2derr',    'max_rescale_bs2derr = 1e9'),
    ('ntracks',    'min_ntracks = 2'),
   # ('geo2ddist',  'exclude_beampipe = False'),
    ]
# evt_nm1s = [
#     # ('Ntks',       'min_ntracks = 0'),
#     ('Njets',      'min_njets = cms.int32(0)'),
#     ('Nlep',       'apply_lep_cuts = cms.bool(False)'),
#     ('DispLep',    'apply_displept_cuts = cms.bool(False)'),
#     ]

#slight modification; instead of exactly 3 or 4 tracks, switching to min 3, 4 tracks
#additionally : instead of nvs being exactly 1, switch to min 1; try to get rid of 2 altogether? 

ntks = [5,3,4]#,7,8,9]
nvs = [0,1,2]


for ntk in ntks:
    if ntk == 5:
        EX1 = EX2 = EX3 = ''
    # elif ntk == 7:
    #     EX1 = 'Ntk3or4'
    # elif ntk == 8:
    #     EX1 = 'Ntk3or5'
    # elif ntk == 9:
    #     EX1 = 'Ntk4or5'
    else:
        if ntk == 3:
            EX1 = 'Ntk3'
        else: 
            EX1 = 'MinNtk%i' % ntk

    if EX1:
        EX2 = "vertex_src = 'mfvSelectedVerticesTight%s', " % EX1
    # if ntk == 7:
    #     EX3 = 'min_ntracks01 = 7, max_ntracks01 = 7, '
    # if ntk == 8:
    #     EX3 = 'ntracks01_0 = 5, ntracks01_1 = 3, '
    # if ntk == 9:
    #     EX3 = 'ntracks01_0 = 5, ntracks01_1 = 4, '

#     exec '''
# process.EX1mfvAnalysisCutsOnlyOneVtx = process.mfvAnalysisCuts.clone(EX2min_nvertex = 1, max_nvertex = 1)
# process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2EX3)
# process.EX1mfvAnalysisCutsSigReg     = process.mfvAnalysisCuts.clone(EX2EX3min_svdist2d = 0.04)

# process.EX1mfvEventHistosOnlyOneVtx = process.mfvEventHistos.clone()
# process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()
# process.EX1mfvEventHistosSigReg     = process.mfvEventHistos.clone()

# process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosOnlyOneVtx = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)
# process.EX1mfvVertexHistosSigReg     = process.mfvVertexHistos.clone(EX2)

# process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
# process.EX1pOnlyOneVtx = cms.Path(common * process.EX1mfvAnalysisCutsOnlyOneVtx * process.EX1mfvEventHistosOnlyOneVtx * process.EX1mfvVertexHistosOnlyOneVtx)
# '''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

#     if 2 in nvs:
#         exec '''
# process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
# process.EX1pSigReg     = cms.Path(common * process.EX1mfvAnalysisCutsSigReg     * process.EX1mfvEventHistosSigReg     * process.EX1mfvVertexHistosSigReg)
# '''.replace('EX1', EX1)

    exec '''
process.EX1mfvAnalysisCutsFullSel    = process.mfvAnalysisCuts.clone(EX2EX3)

process.EX1mfvEventHistosFullSel    = process.mfvEventHistos.clone()

process.EX1mfvVertexHistosPreSel     = process.mfvVertexHistos.clone(EX2)
process.EX1mfvVertexHistosFullSel    = process.mfvVertexHistos.clone(EX2)

process.EX1pPreSel     = cms.Path(common * process.mfvAnalysisCutsPreSel                                              * process.EX1mfvVertexHistosPreSel)
'''.replace('EX1', EX1).replace('EX2', EX2).replace('EX3', EX3)

    if 2 in nvs:
        exec '''
process.EX1pFullSel    = cms.Path(common * process.EX1mfvAnalysisCutsFullSel    * process.EX1mfvEventHistosFullSel    * process.EX1mfvVertexHistosFullSel)
'''.replace('EX1', EX1)

  
    for name, cut in nm1s:
        evt_cut = ''
        if type(cut) == tuple:
            cut, evt_cut = cut

        vtx = eval('process.mfvSelectedVerticesTight%s.clone(%s)' % (EX1, cut))
        vtx_name = '%svtxNo' % EX1 + name

        for nv in nvs:
            if nv == 0 and (cut != '' or EX1 != ''):
                continue

            
            ana = eval('process.mfvAnalysisCuts.clone(%s)' % evt_cut)
            ana.vertex_src = vtx_name
                       
            #     ana.max_nvertex = nv
            ana.min_nvertex = nv
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

   # if use_btag_triggers :
    #    samples = pick_samples(dataset, qcd=True, ttbar=False, span_signal=True, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
     #   pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    if use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=True, all_signal=True, data=False, wjet=False, diboson=False, drellyan=False, leptonic=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
                
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('Histos' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)
