set -e
for eta in 'Low' 'Mix' 'High'
do
  for tau in 1 3 10 30
  do
    for mass in 15 40 55
    do
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_${eta}Eta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
      hadd VHToSSTodddd_tau${tau}mm_M${mass}_20161p2.root *HToSSTodddd_tau${tau}mm_M${mass}_20161.root *HToSSTodddd_tau${tau}mm_M${mass}_20162.root 
    done
  done
done


for eta in 'Low' 'Mix' 'High'
do
  for tau in 100 300
  do
    for mass in 15 40 55
    do
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_${eta}Eta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
      hadd VHToSSTodddd_tau${tau}um_M${mass}_20161p2.root *HToSSTodddd_tau${tau}um_M${mass}_20161.root *HToSSTodddd_tau${tau}um_M${mass}_20162.root 
    done
  done
done

