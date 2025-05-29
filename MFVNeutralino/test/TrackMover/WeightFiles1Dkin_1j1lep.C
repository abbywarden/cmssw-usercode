#include <vector>
#include <string>
#include <iostream>


void MakeWeightPlots(const char* quark, int mg, int ctau, int year)
{
  // TString fns;
  // //This is for the previous signal samples
  // //This is for the new signal samples
  // if (ctau < 1000)
  //    fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_MixEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%ium_M%02i_%ip8.root",boson,ctau,mg,year);
  // else
  //    fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_MixEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%ip8.root",boson,ctau/1000,mg,year);
  // TString fnb;
  // // This is for 10mm->1mm ntuple
  // if (Is_bkg)
  //    fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/background_leptonpresel_%ip8.root", ctau, year);
  // else
  //    fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/SingleMuon%ip8.root", ctau, year);
  
  TString fns;

  if (ctau < 1000)
    fns.Form("~/crabdirs/TrackMoverMCTruth_AllEta/mfv_stopl%s_tau%06ium_M%04i_all.root",quark,ctau,mg);
  else
    //  fns.Form("~/crabdirs/TrackMoverMCTruth_AllEta/mfv_stopl%s_tau%imm_M%02i_all.root",quark,ctau/1000,mg);
    //test first w/ just ttbar loweta 
    fns.Form("~/crabdirs/TrackMoverMCTruth_LowEta/mfv_stopl%s_tau%06ium_M%04i_2018.root",quark,ctau,mg);

  TString fnb;
  // This is for 10mm->1mm ntuple
  
  if (ctau < 1000)
     fnb.Form("~/crabdirs/TrackMover_AllEta_0p3/background_leptonpresel_all.root");
  else
    //  fnb.Form("~/crabdirs/TrackMover_AllEta_10/background_leptonpresel_all.root");
    fnb.Form("~/crabdirs/TrackMover_LowEta_Ulv14lepm1jet1lep_10_noCorrection/ttbar_semilep_2018.root");

  
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  fnout.Form("~/crabdirs/TM_1D_kin_weight_sim_lepton_histos/reweight_2_stopl%s_tau%06ium_M%04i_1D_%d.root", quark, ctau, mg, year);

     std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");

  //og : "nocuts_jetmu_dr_den", "nocuts_jetele_dr_den", "nocuts_mu1_p_den", "nocuts_ele1_p_den", "nocuts_jet0_sump_den"
  // 2 : "nocuts_jetmu_dr_den", "nocuts_jetele_dr_den", "nocuts_mu1_p_den", "nocuts_ele1_p_den", "nocuts_elept1_den", "nocuts_mupt1_den"
  // std::vector<TString> hns_1d = {"nocuts_2logm_den","nocuts_jet_dr_den", "nocuts_jet0_eta_den", "nocuts_jet1_eta_den", "nocuts_jet0_sump_den","nocuts_jet1_sump_den", "nocuts_qrk0_dxybs_den", "nocuts_qrk1_dxybs_den", "nocuts_miscseedtracks_den","nocuts_nmovedtracks_den", "nocuts_movedseedtks_den"};
  std::vector<TString> hns_1d = {"nocuts_jetmu_dr_den", "nocuts_jetele_dr_den", "nocuts_mu1_p_den", "nocuts_ele1_p_den", "nocuts_jet0_sump_den", "nocuts_elept1_den", "nocuts_mupt1_den", "nocuts_pt0_den"};
  for (const auto& hn : hns_1d){
      std::cout << hn << std::endl;
      TH1D* hb = (TH1D*)fb->Get(hn);
      TH1D* hs = (TH1D*)fs->Get(hn);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles1Dkin_1j1lep()
{
  const char* quarks[1] = { "d" };
  std::vector<int> taus = {1000,};//{100, 300, 1000, 3000, 30000};
  std::vector<int> mgs = {200,};
  //std::vector<int> years = {20161, 20162, 2017, 2018};
  std::vector<int> years = {2018};
  for (int i = 0; i < 1; i++){  
    for (int& year:years){
      for (int& tau:taus){
        for (int& mg:mgs){
          if (tau==100 && mg==40)
            continue;
          // MakeWeightPlots(0,bosons[i],mg,tau,year);
          MakeWeightPlots(quarks[i],mg,tau,year);
        }
      }
    }
  }
}
