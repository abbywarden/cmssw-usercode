set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_MixEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_HighEta_ExtraJetCuts_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
pth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
spl="SingleMuon"

for year in 2017
do
  for tau in 0001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python draw2.py TM_config20_TMData_compare_1mm_by_eta_2017p8 ${pth}/SingleMuon2017p8.root  ${pth}/${spl}2017p8.root ${pth}/background_leptonpresel_2017p8.root  ${pth2}/${spl}2017p8.root ${pth3}/${spl}2017p8.root  

    #python draw.py TM_config20_VH_compare_1mm_M55_mixeta_by_2017p8_by_typeclsed ${pth}/background_leptonpresel_2017p8.root  ${sigpth}/VHToSSTodddd_tau1mm_M55_2017p8.root ${sigpth2}/VHToSSTodddd_tau1mm_M55_2017p8.root 

    
    #python draw2.py TM_config20_WplusH_compare_1mm_study_mixeta_studyalt ${pth}/background_leptonpresel_${year}.root  ${pth2}/background_leptonpresel_${year}.root ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root  ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root ${pth3}/background_leptonpresel_${year}.root  

    #python draw.py TM_config20_WplusH_compare_1mm_studyvtxunc_v2 ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root  ${sigpth2}/WplusHToSSTodddd_tau1mm_M55_2017.root ${sigpth3}/WplusHToSSTodddd_tau1mm_M55_2017.root 

    #python draw.py TM_config20_M55_tau000${tau}um_all_2djetdrllpsump_studyv2p3 ${pth}/background_leptonpresel_${year}.root ${pth}/background_leptonpresel_${year}.root ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root  

    #python draw.py TM_config20_M0800_tau000${tau}um_Stopdbardbar_normdzv6 ${pth}/BTagDisplacedJet${year}.root  ${pth}/background_btagpresel_${year}.root  ${pthdata}/mfv_stopdbardbar_tau001000um_M0800_2017.root 
    
    #python draw.py TM_config20_M55_tau000${tau}um_studytk ${pth}/SingleMuon${year}.root ${pth}/background_leptonpresel_${year}.root ${pth}/background_leptonpresel_${year}.root 
    
  done
done
