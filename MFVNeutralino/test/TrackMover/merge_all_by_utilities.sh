set -e

for tau in 1 3 10 30 
do
  for mass in 15 40 55
  do
    cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
    hadd VHToSSTodddd_tau${tau}mm_M${mass}_all.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_20161p2.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_20161p2.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}mm_M${mass}_20161p2.root 
  done
done


for tau in 100 300
do
  for mass in 15 40 55
  do
    cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
    hadd VHToSSTodddd_tau${tau}um_M${mass}_all.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_20161p2.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_20161p2.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_2017p8.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/*HToSSTodddd_tau${tau}um_M${mass}_20161p2.root 
  done
done
