set -e
for year in 2017
do
  for tau in 003000 #000100 000300 003000
  do
    for mass in 15
    do
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv7_20_tau${tau}um_M${mass}_2Dmovedist3movedist2jetdrjet1sumpCorrection"
      #mhadd . --ignore-done & 
      ~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py leptonpresel histos &
      #hadd.py background_leptonpresel_2017.root wjetstolnu_leptonpresel_2017.root dyjets_leptonpresel_2017.root others_leptonpresel_2017.root
    done
  done
done
