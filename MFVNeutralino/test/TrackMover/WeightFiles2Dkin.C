#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(const char* boson, int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  if (ctau < 1000)
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%ium_M%02i_all.root",boson,ctau,mg);
  else
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_AllEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_all.root",boson,ctau/1000,mg);
  TString fnb;
  // This is for 10mm->1mm ntuple
  
  if (ctau < 1000)
     fnb.Form("~/nobackup/crabdirs/TrackMover_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHists0p03onnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_all.root");
  else
     fnb.Form("~/nobackup/crabdirs/TrackMover_AllEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_all.root");
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);

  fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_lepton_histos/reweight_all_kin_sim_vetodr_tau%06ium_M%02i_2D.root", ctau, mg);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");


  std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den",}; // "nocuts_llp_sump_jetdphi_den",};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      int hs_entries = hs->Integral();
      int hb_entries = hb->Integral();
      //hb->RebinX(10);
      //hs->RebinX(10);
      //hb->RebinY(3);
      //hs->RebinY(3);
      hb->RebinX(60);  //60
      hs->RebinX(60); //60
      hb->RebinY(3);
      hs->RebinY(3);
      hb->Scale(1./hb->Integral());
      TH2D* nhb = (TH2D*)hb->Clone("nocuts_llp_sump_jetdr_den");
      hs->Scale(1./hs->Integral());
      TH2D* nhs = (TH2D*)hs->Clone("nocuts_llp_sump_jetdr_den");
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dkin()
{
  const char* bosons[1] = { "V" };
  std::vector<int> taus = {100, 300, 1000,3000,10000,30000};//{100, 300, 1000, 3000, 30000};
  std::vector<int> mgs = {15, 40, 55,};
  const char* years[1] = { "2017p8"}; //, "2017p8",};
  const char* etabins[1] = { "All"}; //"Low", "Mix", "High" };
  for (int i = 0; i < 1; i++){  
    for (int j = 0; j < 1; j++){
      for (int k = 0; k < 3; k++){
        for (int& tau:taus){
          for (int& mg:mgs){
            MakeWeightPlots(bosons[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
