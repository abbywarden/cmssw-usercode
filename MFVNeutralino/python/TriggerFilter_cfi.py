import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.hltHighLevel_cfi

jet_paths = [
    "HLT_PFHT1050_v*",
    ]

bjet_paths = [
    # bjet triggers 2017 - only use the first two, since they contribute most of the efficiency
    "HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v*",
    "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v*",
    #"HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v*",
    #"HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v*",
    #"HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v*",
    # bjet triggers 2018  - only use the first two, since they contribute most of the efficiency
    "HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v*",
    "HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v*",
    #"HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v*",
    #"HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v*",
    #"HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v*",
    ]

displaced_dijet_paths = [
    "HLT_HT430_DisplacedDijet40_DisplacedTrack_v*",
    "HLT_HT650_DisplacedDijet60_Inclusive_v*",
    ]

lepton_paths = [
    "HLT_Ele32_WPTight_Gsf_v*",
   # "HLT_Ele35_WPTight_Gsf_v*",
    "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
  #  "HLT_IsoMu27_v*",
    "HLT_IsoMu24_v*",
    "HLT_Mu50_v*",
    ]

displaced_lepton_paths = [
    "HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v*",
    "HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*",
    "HLT_DoublePhoton70_v*",
    "HLT_DoubleMu43NoFiltersNoVtx_v*",
    ]

dilepton_paths = [
    "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
   # "HLT_DoubleEle25_CaloIdL_MW_v*",
   # "HLT_DoubleEle27_CaloIdL_MW_v*",
  #  "HLT_DoubleEle33_CaloIdL_MW_v*",
  #  "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*",
    "HLT_Mu37_TkMu27_v*",
    "HLT_DoubleL2Mu50_v*",
  #  "HLT_Mu27_Ele37_CaloIdL_MW_v*",
    "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
   # "HLT_Mu37_Ele27_CaloIdL_MW_v*",
    "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
    # "HLT_Mu17_Photon30_IsoCaloId_v*", 
    ]



cross_paths = [
    "HLT_Ele15_IsoVVVL_PFHT450_v*", # JMTBAD these two cross triggers are rendered useless with the offline ht and lepton pt cuts imposed in eventFilter 
    #"HLT_Mu15_IsoVVVL_PFHT450_v*",
    "HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v*",
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
]  


mfvTriggerFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = jet_paths + lepton_paths + cross_paths,
    andOr = True, # = OR
    throw = False,
    )

#stand-in hltpath; think it would work for an empty path but feel more comfortable with a stand in.
mfvTriggerFilterSingle = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = ["HLT_Ele15_IsoVVVL_PFHT4500_v*"],
    throw = False,
    )

mfvTriggerFilterJetsOnly = mfvTriggerFilter.clone(HLTPaths = jet_paths)
mfvTriggerFilterBJetsOnly = mfvTriggerFilter.clone(HLTPaths = bjet_paths)
mfvTriggerFilterDisplacedDijetOnly = mfvTriggerFilter.clone(HLTPaths = displaced_dijet_paths)
mfvTriggerFilterLeptons = mfvTriggerFilter.clone(HLTPaths = lepton_paths)
mfvTriggerFilterDisplacedLeptons = mfvTriggerFilter.clone(HLTPaths = displaced_lepton_paths)
mfvTriggerFilterDileptons = mfvTriggerFilter.clone(HLTPaths = dilepton_paths)

mfvTriggerFilterHTORBjetsORDisplacedDijet = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = jet_paths + bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterBjetsORDisplacedDijetVetoHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

#new Logical OR 

mfvTriggerFilterDispLeptonsORSingleLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = displaced_lepton_paths + lepton_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterDispLeptonsORDiLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = displaced_lepton_paths + dilepton_paths,
        andOr = True, # OR
        throw = False,
        )


mfvTriggerFilterSingleLeptonsORDiLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_paths + dilepton_paths,
        andOr = True, # OR
        throw = False,
        )

#single leptons or HT (not bothering w/ di leptons
mfvTriggerFilterSingleLeptonsORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_paths + jet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterDispLeptonsORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = displaced_lepton_paths + jet_paths,
        andOr = True, # OR
        throw = False,
        )
