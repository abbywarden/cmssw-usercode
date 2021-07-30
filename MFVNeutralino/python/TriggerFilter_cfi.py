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
    "HLT_Ele35_WPTight_Gsf_v*",
   # "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
  #  "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
    "HLT_IsoMu27_v*",
    "HLT_IsoMu24_v*",
    "HLT_Mu50_v*",
    ]

#most efficiency ele and mu 
lepton_path2 = [
    #is there just a single electron? yes but doesn't perform as good as this one. 
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
    "HLT_Mu50_v*",
]

#1st and 2nd most eff. ele and mu
lepton_path3 = [
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
    "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
    "HLT_Mu50_v*",
    "HLT_IsoMu27_v*",
]

displaced_lepton_paths = [
    "HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v*",
    "HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*",
    "HLT_DoublePhoton70_v*",
    "HLT_DoubleMu43NoFiltersNoVtx_v*",
    ]

dilepton_paths = [
    "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_DoubleEle25_CaloIdL_MW_v*",
    "HLT_DoubleEle27_CaloIdL_MW_v*",
    "HLT_DoubleEle33_CaloIdL_MW_v*",
    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*",
    "HLT_Mu37_TkMu27_v*",
    "HLT_DoubleL2Mu50_v*",
    "HLT_Mu27_Ele37_CaloIdL_MW_v*",
    "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_Mu37_Ele27_CaloIdL_MW_v*",
    "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
    # "HLT_Mu17_Photon30_IsoCaloId_v*", Originally have this in, but as I am unsure about its validity as a dilepton
    #trigger, I am leaving it out for the second round. ah, we would have to have a further selection to remove just the photons
    ]

dilepton_path2 = [
    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*",
    "HLT_Mu27_Ele37_CaloIdL_MW_v*",
    "HLT_DoubleL2Mu50_v*",
    ]


#two ee, two emu, one mumu since it does well enough...
dilepton_path3 = [
    "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*",
    "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_Mu27_Ele37_CaloIdL_MW_v*",
    "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_DoubleL2Mu50_v*",
    ]

#most of these have a counterpart without DZ; and their counterparts have higher eff. so nevermind.
# dilepton_paths_wDZ = [
#     "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#     "HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v*",
#     "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*",
#     "HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v*",
#     "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*",
#     "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#     "HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v*",
#     "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*",
#     ]


#not finding a good selection for muon + jet so probably discard... 
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
#mfvTriggerFilterLepton2 = mfvTriggerFilter.clone(HLTPaths = lepton_path2)
#mfvTriggerFilterLepton3 = mfvTriggerFilter.clone(HLTPaths = lepton_path3)

mfvTriggerFilterDisplacedLeptons = mfvTriggerFilter.clone(HLTPaths = displaced_lepton_paths)
#mfvTriggerFilterCross = mfvTriggerFilter.clone(HLTPaths = cross_paths)
#mfvTriggerFilterDileptonswDZ = mfvTriggerFilter.clone(HLTPaths = dilepton_paths_wDZ)
mfvTriggerFilterDileptons = mfvTriggerFilter.clone(HLTPaths = dilepton_paths)
#mfvTriggerFilterDilepton2 = mfvTriggerFilter.clone(HLTPaths = dilepton_path2)
#mfvTriggerFilterDilepton3 = mfvTriggerFilter.clone(HLTPaths = dilepton_path3)

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

# mfvTriggerFilterDispLeptonsORDiLeptons_wDZ = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = displaced_lepton_paths + dilepton_paths_wDZ,
#         andOr = True, # OR
#         throw = False,
#         )

mfvTriggerFilterSingleLeptonsORDiLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_paths + dilepton_paths,
        andOr = True, # OR
        throw = False,
        )
#new logical OR with slimmed lepton + dileptons (doing this all in one go; may be overkill but I don't want to rerun everything again... but probs will

#w/ slimmed single leptons
# mfvTriggerFilterSingleLepton2ORDiLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path2 + dilepton_paths,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLepton3ORDiLeptons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path3 + dilepton_paths,
#         andOr = True, # OR
#         throw = False,
#         )
# mfvTriggerFilterDispLeptonsORSingleLepton2 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = displaced_lepton_paths + lepton_path2,
#         andOr = True, # OR
#         throw = False,
#         )
# mfvTriggerFilterDispLeptonsORSingleLepton3 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = displaced_lepton_paths + lepton_path3,
#         andOr = True, # OR
#         throw = False,
#         )


# #w/ slimmed dileptons and single leptons
# mfvTriggerFilterSingleLeptonsORDiLepton2 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_paths + dilepton_path2,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLeptonsORDiLepton3 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_paths + dilepton_path3,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLepton2ORDiLepton2 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path2 + dilepton_path2,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLepton2ORDiLepton3 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path2 + dilepton_path3,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLepton3ORDiLepton2 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path3 + dilepton_path2,
#         andOr = True, # OR
#         throw = False,
#         )

# mfvTriggerFilterSingleLepton3ORDiLepton3 = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_path3 + dilepton_path3,
#         andOr = True, # OR
#         throw = False,
#         )

#single leptons or HT (not bothering w/ di leptons
mfvTriggerFilterSingleLeptonsORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_paths + jet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterSingleLepton2ORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_path2 + jet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterSingleLepton3ORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = lepton_path3 + jet_paths,
        andOr = True, # OR
        throw = False,
        )


mfvTriggerFilterDispLeptonsORHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = displaced_lepton_paths + jet_paths,
        andOr = True, # OR
        throw = False,
        )

# mfvTriggerFilterSingleLeptonsORDiLeptons_wDZ = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
#         HLTPaths = lepton_paths + dilepton_paths_wDZ,
#         andOr = True, # OR
#         throw = False,
#         )


# investigating lepton triggers individually #brute forcing cause I'm spending too much time on this

#lepton_paths

mfvTriggerFilterEle35 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele35_WPTight_Gsf_v*"])
mfvTriggerFilterEle32 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele32_WPTight_Gsf_v*"])
mfvTriggerFilterEle115 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele115_CaloIdVT_GsfTrkIdT_v*"])
mfvTriggerFilterEle50 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*"])
mfvTriggerFilterIsoMu27 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_IsoMu27_v*"])
mfvTriggerFilterIsoMu24 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_IsoMu24_v*"])
mfvTriggerFilterMu50 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu50_v*"])


#displaced_lepton_paths
mfvTriggerFilterMu43Photon43 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v*"])
mfvTriggerFilterDiPhoton30_22 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v*"])
mfvTriggerFilterDoublePhoton70 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoublePhoton70_v*"])
mfvTriggerFilterDoubleMu43 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleMu43NoFiltersNoVtx_v*"])

# #dilepton_paths 
# mfvTriggerFilterEle23_12 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*"])
# mfvTriggerFilterDoubleEle25 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleEle25_CaloIdL_MW_v*"])
# mfvTriggerFilterDoubleEle27 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleEle27_CaloIdL_MW_v*"])
# mfvTriggerFilterDoubleEle33 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleEle33_CaloIdL_MW_v*"])
# mfvTriggerFilterDoubleEle8 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v*"])
# mfvTriggerFilterMu37_TkMu27 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu37_TkMu27_v*"])
# mfvTriggerFilterDoubleL2Mu50 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleL2Mu50_v*"])
# mfvTriggerFilterMu27_Ele37 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu27_Ele37_CaloIdL_MW_v*"])
# mfvTriggerFilterMu8_Ele23 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*"])
# mfvTriggerFilterMu37_Ele27 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu37_Ele27_CaloIdL_MW_v*"])
# mfvTriggerFilterMu23_Ele12 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",])
# mfvTriggerFilterMu17_Photon30 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu17_Photon30_IsoCaloId_v*"])
  
  
    
# #dilepton_paths_wDZ
# mfvTriggerFilterDZ_Ele23_12 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*"])
# mfvTriggerFilterDZ_DoubleEle8_PFHT350 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v*"])
# mfvTriggerFilterDZ_Mu17_8 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*"])
# mfvTriggerFilterDZ_Mu19_9 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v*"])
# mfvTriggerFilterDZ_Mu17_8 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*"])
# mfvTriggerFilterDZ_Mu12_Ele23 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*"])
# mfvTriggerFilterDZ_Mu8_Ele8 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v*"])
# mfvTriggerFilterDZ_Mu8_Ele23 = mfvTriggerFilterSingle.clone(HLTPaths = ["HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*"])


    
