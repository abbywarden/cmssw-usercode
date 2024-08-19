set -e
pth0="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_noCorrection"
pth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p4_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedistjetdrllpsumpcoarse60Correction"
sigpth0="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_HighEta_NoQrkEtaCut_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_HighEta_NoQrkEtaCutV2_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_HighEta_ExtraJetCuts_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
spl="VHToSSTodddd_tau1mm_M55_2017p8.root" 
spl0="ZHToSSTodddd_tau1mm_M55_20161.root" 
spl1="ZHToSSTodddd_tau1mm_M55_20162.root" 
spl2="ZHToSSTodddd_tau1mm_M55_2017.root" 
spl3="ZHToSSTodddd_tau1mm_M55_2018.root" 
spl4="mfv_stopbbarbbar_tau000100um_M0200_2017.root" 
spl5="mfv_stopbbarbbar_tau001000um_M0200_2017.root"
spl6="mfv_stopbbarbbar_tau030000um_M0200_2017.root"
data="SingleMuon2017p8.root"
bkg="background_leptonpresel_2017p8.root"
bkg0="background_leptonpresel_20161.root"
bkg1="background_leptonpresel_20162.root"
bkg2="background_leptonpresel_2017.root"
bkg3="background_leptonpresel_2018.root"
for year in 2017
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do

    #python drawden_comp.py TM_drawtau${tau}_B${year}_Stopdbardbar_normdzv6 ${pth}/background_btagpresel_2017.root ${pth}/BTagDisplacedJet${year}.root ${sigpth0}/${spl0}  ${sigpth0}/${spl0} ${sigpth0}/${spl0} ${sigpth0}/${spl0}  long Muon

    #python drawden_comp.py TM_drawtau${tau}_Mu${year}_normdzv6_nopreselrelaxsigbspnotw_TMData_ctau1mm_by_eta_2017p8 ${pth0}/${bkg} ${sigpth2}/${spl} ${pth0}/${bkg} ${pth1}/${data} ${pth2}/${data} ${pth3}/${data} long Muon
    
    #python drawden_comp.py TM_drawtau${tau}_Mu${year}_TMMC_normdzv6_nopreselrelaxsigbspnotw_vetodr0p4_ctau1mm_mixeta_by_year ${pth0}/${bkg0} ${pth0}/${bkg0} ${pth0}/${bkg1} ${pth0}/${bkg2} ${pth0}/${bkg3} ${pth0}/${bkg3} long Muon

    python drawden_comp.py TM_drawtau_Mu${year}_VH_normdzv6_nopreselrelaxsigbspnotw_vetodr0p4_ctau1mm_higheta_studyqrkcut ${sigpth0}/${spl} ${sigpth1}/${spl} ${sigpth0}/${spl} ${sigpth0}/${spl} ${sigpth0}/${spl} ${sigpth0}/${spl} long Muon

    #python drawnum_comp.py TM_drawtau${tau}_Mu${year}_MFVStopbarbar_normdzv6_nopreselrelaxbspnotw_onlysig_comparejets_studytkdr_all_num ${sigpth1}/${spl4} ${sigpth1}/${spl5} ${sigpth1}/${spl6} ${sigpth1}/${spl6} ${sigpth1}/${spl6} ${sigpth1}/${spl6} long Muon

  done

done
