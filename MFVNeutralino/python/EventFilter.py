import FWCore.ParameterSet.Config as cms

def setup_event_filter(process,
                       path_name='p',
                       trigger_filter = True,
                       trigger_filter_name = 'mfvTriggerFilter',
                       event_filter = False,
                       event_filter_jes_mult = 2,
                       event_filter_name = 'mfvEventFilter',
                       event_filter_require_vertex = True,
                       input_is_miniaod = False,
                       mode = None,
                       sequence_name = 'mfvEventFilterSequence',
                       name_ex = None,
                       ):

    if name_ex:
        trigger_filter_name += name_ex
        event_filter_name += name_ex
        sequence_name += name_ex

    if mode == 'trigger only':
        pass
    elif mode == 'trigger jets only':
        trigger_filter = 'jets only'
    elif mode == 'trigger bjets only':
        trigger_filter = 'bjets only'
    elif mode == 'trigger displaced dijet only':
        trigger_filter = 'displaced dijet only'
    elif mode == 'trigger HT OR bjets OR displaced dijet':
        trigger_filter = 'HT OR bjets OR displaced dijet'
    elif mode == 'trigger bjets OR displaced dijet veto HT':
        trigger_filter = 'bjets OR displaced dijet veto HT'
        
    elif mode == 'trigger leptons only':
        trigger_filter = 'leptons only'
    elif mode == 'lepton slim 2':
        trigger_filter = 'lepton2'
    elif mode == 'lepton slim 3':
        trigger_filter = 'lepton3'
        
    elif mode == 'jets only':
        trigger_filter = event_filter = 'jets only'
    elif mode == 'leptons only':
        trigger_filter = event_filter = 'leptons only'
        
    elif mode == 'trigger displaced leptons':
        trigger_filter = 'displaced leptons'
    elif mode == 'trigger cross':
        trigger_filter = 'cross'
    elif mode == 'trigger cross only':
        trigger_filter = 'cross only'    
    elif mode == 'HT OR bjets OR displaced dijet':
        trigger_filter = event_filter = 'HT OR bjets OR displaced dijet'
    elif mode == 'bjets OR displaced dijet veto HT':
        trigger_filter = event_filter = 'bjets OR displaced dijet veto HT'
    elif mode == 'jets only novtx':
        trigger_filter = event_filter = 'jets only'
        event_filter_require_vertex = False
    elif mode == 'bjets OR displaced dijet veto HT novtx':
        trigger_filter = event_filter = 'bjets OR displaced dijet veto HT'
        event_filter_require_vertex = False

    elif mode == 'trigger dileptons':
        trigger_filter = 'dileptons'
    elif mode == 'dileptons slim 2':
        trigger_filter = 'dilepton2'
    elif mode == 'dileptons slim 3':
        trigger_filter = 'dilepton3'  
  #  elif mode == 'trigger dileptons wDZ':
   #     trigger_filter = 'dileptons wDZ'
    elif mode == 'DispLeptons OR Single Leptons':
        trigger_filter = 'displeptons OR leptons'
    elif mode == 'DispLeptons OR DiLeptons':
        trigger_filter = 'displeptons OR dileptons'
  #  elif mode == 'DispLeptons OR DiLeptons wDZ':
     #   trigger_filter = 'displeptons OR dileptons wDZ'
  #  elif mode == 'SingleLeptons OR DiLeptons wDZ':
   #     trigger_filter = 'leptons or dileptons wDZ'

    elif mode == 'DispLeptons OR Single Lepton2':
        trigger_filter = 'displeptons OR lepton2'
    elif mode == 'DispLeptons OR Single Lepton3':
        trigger_filter = 'displeptons OR lepton3'

    #all the single leptons and dilepton pairs along w/ slimmed 
    elif mode == 'SingleLeptons OR DiLeptons':
        trigger_filter = 'leptons OR dileptons'
    elif mode == 'SingleLeptons OR DiLepton2':
        trigger_filter = 'leptons OR dilepton2'     
    elif mode == 'SingleLeptons OR DiLepton3':
        trigger_filter = 'leptons OR dilepton3'
        
    elif mode == 'SingleLepton2 OR DiLeptons':
        trigger_filter = 'lepton2 OR dileptons'
    elif mode == 'SingleLepton3 OR DiLeptons':
        trigger_filter = 'lepton3 OR dileptons'
        
    elif mode == 'SingleLepton2 OR DiLepton2':
        trigger_filter = 'lepton2 OR dilepton2'
    elif mode == 'SingleLepton2 OR DiLepton3':
        trigger_filter = 'lepton3 OR dilepton3'
    elif mode == 'SingleLepton3 OR DiLepton2':
        trigger_filter = 'lepton3 OR dilepton2'
    elif mode == 'SingleLepton3 OR DiLepton3':
        trigger_filter = 'lepton3 OR dilepton3'


    #logical OR w/ displaced leptons and HT 
    elif mode == 'DispLeptons OR HT':
        trigger_filter = 'displeptons OR ht'
    elif mode == 'Leptons OR HT':
        trigger_filter = 'leptons OR ht'
    elif mode == 'Lepton2 OR HT':
        trigger_filter = 'lepton2 OR ht'
    elif mode == 'Lepton3 OR HT':
        trigger_filter = 'lepton3 OR ht'
        
        
    #all the singles
    elif mode == 'Ele32':
        trigger_filter = 'ele32'
    elif mode == 'Ele35':
        trigger_filter = 'ele35'
    elif mode == 'Ele115':
        trigger_filter = 'ele115'
    elif mode == 'Ele50':
        trigger_filter = 'ele50'
    elif mode == 'IsoMu27':
        trigger_filter = 'isomu27'
    elif mode == 'IsoMu24':
        trigger_filter = 'isomu24'
    elif mode == 'Mu50':
        trigger_filter = 'mu50'
        
    elif mode == 'Mu43Photon43':
        trigger_filter = 'mu43photon43'
    elif mode == 'DiPhoton30_22':
        trigger_filter = 'diphoton30_22'
    elif mode == 'DoublePhoton70':
        trigger_filter = 'doublephoton70'
    elif mode == 'DoubleMu43':
        trigger_filter = 'doublemu43'

    elif mode == 'Ele23_12':
        trigger_filter = 'ele23_12'
    elif mode == 'DoubleEle25':
        trigger_filter = 'doubleele25'
    elif mode == 'DoubleEle27':
        trigger_filter = 'doubleele27'
    elif mode == 'DoubleEle33':
        trigger_filter = 'doubleele33'
    elif mode == 'DoubleEle8':
        trigger_filter = 'doubleele8'
    elif mode == 'Mu37_TkMu27':
        trigger_filter = 'mu37_tkmu27'
    elif mode == 'DoubleL2Mu50':
        trigger_filter = 'doubleL2mu50'
    elif mode == 'Mu27_Ele37':
        trigger_filter = 'mu27_ele37'
    elif mode == 'Mu8_Ele23':
        trigger_filter = 'mu8_ele23'
    elif mode == 'Mu37_Ele27':
        trigger_filter = 'mu37_ele27'
    elif mode == 'Mu23_Ele12':
        trigger_filter = 'mu23_ele12'
    elif mode == 'Mu17_Photon30':
        trigger_filter = 'mu17_photon30'

    # elif mode == 'DZ_Ele23_12':
    #     trigger_filter = 'dz_ele23_12'
    # elif mode == 'DZ_DoubleEle8_PFHT350':
    #     trigger_filter = 'dz_doubleele8_pfht350'
    # elif mode == 'DZ_Mu17_8':
    #     trigger_filter = 'dz_mu17_8'
    # elif mode == 'DZ_Mu19_9':
    #     trigger_filter = 'dz_mu19_9'
    # elif mode == 'DZ_Mu17_8':
    #     trigger_filter = 'dz_mu17_8'
    # elif mode == 'DZ_Mu12_Ele23':
    #     trigger_filter = 'dz_mu12_ele23'
    # elif mode == 'DZ_Mu8_Ele8':
    #     trigger_filter = 'dz_mu8_ele8'
    # elif mode == 'DZ_Mu8_Ele23':
    #     trigger_filter = 'dz_mu8_ele23'

            
    
    
           
    elif mode == 'novtx':
        event_filter = True
        event_filter_require_vertex = False
    elif mode:
        if mode is not True:
            raise ValueError('bad mode %r' % mode)
        event_filter = True

    if trigger_filter == 'jets only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterJetsOnly as triggerFilter
    elif trigger_filter == 'bjets only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterBJetsOnly as triggerFilter
    elif trigger_filter == 'displaced dijet only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDisplacedDijetOnly as triggerFilter
    elif trigger_filter == 'HT OR bjets OR displaced dijet':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterHTORBjetsORDisplacedDijet as triggerFilter
    elif trigger_filter == 'bjets OR displaced dijet veto HT':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterBjetsORDisplacedDijetVetoHT as triggerFilter
    elif trigger_filter == 'cross':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilter as triggerFilter
    elif trigger_filter == 'cross only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterCross as triggerFilter
        
    elif trigger_filter == 'leptons only':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterLeptons as triggerFilter
    elif trigger_filter == 'lepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterLepton2 as triggerFilter
    elif trigger_filter == 'lepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterLepton3 as triggerFilter
    elif trigger_filter == 'displaced leptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDisplacedLeptons as triggerFilter
    elif trigger_filter == 'dileptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDileptons as triggerFilter
    elif trigger_filter == 'dilepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDilepton2 as triggerFilter
    elif trigger_filter == 'dilepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDilepton3 as triggerFilter
  #  elif trigger_filter == 'dileptons wDZ':
   #     from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDileptonswDZ as triggerFilter
        
    elif trigger_filter == 'displeptons OR leptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORSingleLeptons as triggerFilter
    elif trigger_filter == 'displeptons OR lepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORSingleLepton2 as triggerFilter
    elif trigger_filter == 'displeptons OR lepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORSingleLepton3 as triggerFilter
        
    elif trigger_filter == 'displeptons OR dileptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORDiLeptons as triggerFilter
   # elif trigger_filter == 'displeptons OR dileptons wDZ':
   #     from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORDiLeptons_wDZ as triggerFilter
    elif trigger_filter == 'leptons OR dileptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLeptonsORDiLeptons as triggerFilter
    elif trigger_filter == 'lepton2 OR dileptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton2ORDiLeptons as triggerFilter
    elif trigger_filter == 'lepton3 OR dileptons':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton3ORDiLeptons as triggerFilter
    elif trigger_filter == 'leptons OR dilepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLeptonsORDiLepton2 as triggerFilter
    elif trigger_filter == 'leptons OR dilepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLeptonsORDiLepton3 as triggerFilter
   # elif trigger_filter == 'leptons or dileptons wDZ':
     #   from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLeptonsORDiLeptons_wDZ as triggerFilter
    elif trigger_filter == 'lepton2 OR dilepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton2ORDiLepton2 as triggerFilter
    elif trigger_filter == 'lepton2 OR dilepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton2ORDiLepton3 as triggerFilter
    elif trigger_filter == 'lepton3 OR dilepton2':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton3ORDiLepton2 as triggerFilter
    elif trigger_filter == 'lepton3 OR dilepton3':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton3ORDiLepton3 as triggerFilter

    elif trigger_filter == 'displeptons OR ht':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDispLeptonsORHT as triggerFilter
    elif trigger_filter == 'leptons OR ht':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLeptonsORHT as triggerFilter
    elif trigger_filter == 'lepton2 OR ht':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton2ORHT as triggerFilter
    elif trigger_filter == 'lepton3 OR ht':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterSingleLepton3ORHT as triggerFilter
        
#all the singles; first lepton
    elif trigger_filter == 'ele32':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterEle32 as triggerFilter
    elif trigger_filter == 'ele35':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterEle35 as triggerFilter
    elif trigger_filter == 'ele115':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterEle115 as triggerFilter
    elif trigger_filter == 'ele50':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterEle50 as triggerFilter
    elif trigger_filter == 'isomu27':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterIsoMu27 as triggerFilter
    elif trigger_filter == 'isomu24':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterIsoMu24 as triggerFilter
    elif trigger_filter == 'mu50':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu50 as triggerFilter

#displaced lepton
    elif trigger_filter == 'mu43photon43':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu43Photon43 as triggerFilter
    elif trigger_filter == 'diphoton30_22':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDiPhoton30_22 as triggerFilter
    elif trigger_filter == 'doublephoton70':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoublePhoton70 as triggerFilter
    elif trigger_filter == 'doublemu43':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleMu43 as triggerFilter
        
#dileptons
    elif trigger_filter == 'ele23_12':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterEle23_12 as triggerFilter
    elif trigger_filter == 'doubleele25':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleEle25 as triggerFilter
    elif trigger_filter == 'doubleele27':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleEle27 as triggerFilter
    elif trigger_filter == 'doubleele33':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleEle33 as triggerFilter
    elif trigger_filter == 'doubleele8':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleEle8 as triggerFilter
    elif trigger_filter == 'mu37_tkmu27':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu37_TkMu27 as triggerFilter
    elif trigger_filter == 'doubleL2mu50':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDoubleL2Mu50 as triggerFilter
    elif trigger_filter == 'mu27_ele37':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu27_Ele37 as triggerFilter
    elif trigger_filter == 'mu8_ele23':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu8_Ele23 as triggerFilter
    elif trigger_filter == 'mu37_ele27':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu37_Ele27 as triggerFilter
    elif trigger_filter == 'mu23_ele12':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu23_Ele12 as triggerFilter
    elif trigger_filter == 'mu17_photon30':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterMu17_Photon30 as triggerFilter

#dilepton wDZ

    elif trigger_filter == 'dz_ele23_12':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Ele23_12 as triggerFilter
    elif trigger_filter == 'dz_doubleele8_pfht350':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_DoubleEle8_PFHT350 as triggerFilter
    elif trigger_filter == 'dz_mu17_8':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu17_8 as triggerFilter
    elif trigger_filter == 'dz_mu19_9':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu19_9 as triggerFilter
    elif trigger_filter == 'dz_mu17_8':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu17_8 as triggerFilter
    elif trigger_filter == 'dz_mu12_ele23':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu12_Ele23 as triggerFilter
    elif trigger_filter == 'dz_mu8_ele8':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu8_Ele8 as triggerFilter
    elif trigger_filter == 'dz_mu8_ele23':
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilterDZ_Mu8_Ele23 as triggerFilter


        
    elif trigger_filter is True:
        from JMTucker.MFVNeutralino.TriggerFilter_cfi import mfvTriggerFilter as triggerFilter
    elif trigger_filter is not False:
        raise ValueError('trigger_filter %r bad: must be one of ("jets only", "leptons only", "bjets only", "displaced dijet only", "HT OR bjets OR displaced dijet", "bjets OR displaced dijet veto HT", "displaced leptons", "displaced lepton pair", True, False)' % trigger_filter)

    overall = cms.Sequence()

    if trigger_filter:
        triggerFilter = triggerFilter.clone()
        setattr(process, trigger_filter_name, triggerFilter)
        overall *= triggerFilter

    if event_filter:
        if event_filter == 'jets only':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterJetsOnly as eventFilter
        elif event_filter == 'leptons only':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterLeptonsOnly as eventFilter
            
        elif event_filter == 'HT OR bjets OR displaced dijet':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterHTORBjetsORDisplacedDijet as eventFilter
        elif event_filter == 'bjets OR displaced dijet veto HT':
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilterBjetsORDisplacedDijetVetoHT as eventFilter

        elif event_filter is True:
            from JMTucker.MFVNeutralino.EventFilter_cfi import mfvEventFilter as eventFilter
        elif event_filter is not False:
            raise ValueError('event_filter must be one of ("jets only", "leptons only", "HT OR bjets OR displaced dijet", "bjets OR displaced dijet veto HT", "displaced leptons, "displaced lepton pair", True, False)')

        eventFilter = eventFilter.clone()
        if input_is_miniaod:
            process.load('JMTucker.Tools.UpdatedJets_cff')
            overall *= process.updatedJetsSeqMiniAOD
            eventFilter.jets_src = 'updatedJetsMiniAOD'
            eventFilter.muons_src = 'slimmedMuons'
            eventFilter.electrons_src = 'slimmedElectrons'
        setattr(process, event_filter_name, eventFilter)

        if event_filter_jes_mult > 0:
            from JMTucker.Tools.JetShifter_cfi import jmtJetShifter as jetShifter
            jetShifter = jetShifter.clone()
            if input_is_miniaod:
                jetShifter.jets_src = 'updatedJetsMiniAOD'
            jetShifter.mult = event_filter_jes_mult
            jetShifter_name = event_filter_name + 'JetsJESUp%iSig' % event_filter_jes_mult
            eventFilter.jets_src = jetShifter_name
            setattr(process, jetShifter_name, jetShifter)
            overall *= jetShifter

        overall *= eventFilter

        
        if event_filter_require_vertex:
            if not hasattr(process, 'mfvVertices'):
                # assume if mfvVertices is set up, then the rest of this is too
                process.load('CommonTools.ParticleFlow.goodOfflinePrimaryVertices_cfi')
                process.load('JMTucker.MFVNeutralino.Vertexer_cff')
                if input_is_miniaod:
                    process.goodOfflinePrimaryVertices.src = 'offlineSlimmedPrimaryVertices'
                    process.load('JMTucker.Tools.UnpackedCandidateTracks_cfi')
                    process.mfvVertexTracks.tracks_src = 'jmtUnpackedCandidateTracks'
                    process.jmtRescaledTracks.tracks_src = 'jmtUnpackedCandidateTracks' # JMTBAD use rescaled tracks
            vertexFilter = cms.EDFilter('VertexSelector', src = cms.InputTag('mfvVertices'), cut = cms.string('nTracks > 2'), filter = cms.bool(True))
            setattr(process, event_filter_name + 'W1Vtx', vertexFilter)
            if input_is_miniaod:
                overall *= process.goodOfflinePrimaryVertices * process.jmtUnpackedCandidateTracks * process.mfvVertexSequenceBare * vertexFilter
            else:
                overall *= process.goodOfflinePrimaryVertices                                      * process.mfvVertexSequenceBare * vertexFilter

    setattr(process, sequence_name, overall)

    if not path_name:
        return overall
    elif hasattr(process, path_name):
        getattr(process, path_name).insert(0, overall)
    else:
        setattr(process, path_name, cms.Path(overall))

    if hasattr(process, 'out'):
        assert not hasattr(process.out, 'SelectEvents')
        process.out.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(path_name))
