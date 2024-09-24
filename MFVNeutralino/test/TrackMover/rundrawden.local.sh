set -e
pth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p5_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedist2jetdrllpsumpcoarse60alletaCorrection"
pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p5_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedist2jetdrllpsumpcoarse60alletaCorrection"
pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_StudyV2p5_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2Dmovedist3movedist2jetdrllpsumpcoarse60alletaCorrection"
sigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_MixEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_HighEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6"
incsigpthlow="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_VtxUnc10to30umClSed3to5_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
incsigpthhigh="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_VtxUnc15to35umClSed3to5_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
incsigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
incsigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_MixEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
incsigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_HighEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
spl="VHToSSTodddd_tau1mm_M55_2017p8.root" 
data="SingleMuon2017p8.root"
bkg="background_leptonpresel_2017p8.root"
for year in "2017p8"
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    for mass in 55 
    do
      #python drawden_comp.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_loweta_VHSS4d_ONLYREWEIGHT ${pth1}/${bkg} ${pth1}/${data} ${incsigpth1}/${spl} ${sigpth1}/${spl} ${pth1}/${bkg} ${pth1}/${bkg} long Low
      #python drawden_comp.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_mixeta_VHSS4d ${pth2}/${bkg} ${pth2}/${data} ${incsigpth2}/${spl} ${sigpth2}/${spl} ${pth2}/${bkg} ${pth2}/${bkg} long Mix
      #python drawden_comp.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_higheta_VHSS4d ${pth3}/${bkg} ${pth3}/${data} ${incsigpth3}/${spl} ${sigpth3}/${spl} ${pth3}/${bkg} ${pth3}/${bkg} long High
      python drawden_comp.py TM_DENOM_Mu_year2017p8_ctau${tau}um_mass${mass}_byvtxuncnclsedtk3to_by5um_VHSS4d ${incsigpthlow}/${spl} ${incsigpthlow}/${spl} ${incsigpthlow}/${spl}  ${incsigpthhigh}/${spl} ${incsigpthhigh}/${spl} ${incsigpthlow}/${spl} long All
    done

  done

done
