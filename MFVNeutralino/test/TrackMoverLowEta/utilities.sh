set -e
for tau in 030000
do
    for mass in 55
    do
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_MoveGrid_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
      #mhadd . --ignore-done & 
      ~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py leptonpresel histos 2017 &
      ~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py leptonpresel histos 2018 &
      #hadd.py background_leptonpresel_2017p8.root background_leptonpresel_2017.root background_leptonpresel_2018.root
      #hadd.py SingleMuon2017p8.root SingleMuon2017.root SingleMuon2018.root
    done
done


#for tau in 000100 000300
#do
#    for mass in 15 40 55
#    do
#      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists0p03onnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
#      #mhadd . --ignore-done & 
#      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py leptonpresel histos 2017 &
#      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py leptonpresel histos 2018 &
#      hadd.py background_leptonpresel_2017p8.root background_leptonpresel_2017.root background_leptonpresel_2018.root
#      hadd.py SingleMuon2017p8.root SingleMuon2017.root SingleMuon2018.root
#    done
#done
