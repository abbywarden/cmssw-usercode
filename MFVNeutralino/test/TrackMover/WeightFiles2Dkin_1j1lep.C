#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(const char* quark, int mg, int ctau, const char* etabin, const char* year)
{
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
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);

  fnout.Form("~/crabdirs/TM_2D_kin_weight_sim_lepton_histos/reweight_stopl%s_kinjet0lep1p_tau%06ium_M%04i_2D.root", quark, ctau, mg);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");


  //we need to do this for electrons and muons individually? or no? 
  // std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den",}; // "nocuts_llp_sump_jetdphi_den",};
  // std::vector<TString> hns_2d = {"nocuts_jet0_sump_jetlepdr_den",}; // "nocuts_jet0_sump_ele1_p_den"}; // "nocuts_llp_sump_jetdphi_den",};
  // std::vector<TString> hns_2d = {"nocuts_jet0_sump_lep1_p_den",};
  std::vector<TString> hns_2d = {"nocuts_jet0_sump_jetlepdr_den", "nocuts_lep1_pT_jetdr_den", "nocuts_ele1_pT_jetdr_den", "nocuts_mu1_pT_jetdr_den"}; //, "nocuts_mu1_p_eta_den", "nocuts_ele1_p_eta_den"};

  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      std::cout << hb << " " << hs << std::endl;
      int hs_entries = hs->Integral();
      int hb_entries = hb->Integral();
      //hb->RebinX(10);
      //hs->RebinX(10);
      //hb->RebinY(3);
      //hs->RebinY(3);
      
      // hs->GetXaxis()->SetRangeUser(5, 500); //for jet0_sump_jetlepdr
      // hb->GetXaxis()->SetRangeUser(5, 500); //for jet0_sump_jetlepdr
      // hb->RebinX(10);  //60
      // hs->RebinX(10); //60
      // hb->RebinY(3);
      // hs->RebinY(3);
      hb->Scale(1./hb->Integral());
      TH2D* nhb = (TH2D*)hb->Clone(hn);
      hs->Scale(1./hs->Integral());
      TH2D* nhs = (TH2D*)hs->Clone(hn);

      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2Dkin_1j1lep()
{
  const char* quark[2] = { "d"};//, "b" };
  // std::vector<int> taus = {100, 300, 1000,3000,10000,30000};//{100, 300, 1000, 3000, 30000};
  std::vector<int> taus = {1000};//{100, 300, 1000, 3000, 30000};
  std::vector<int> mgs = {200}; //what masses? 
  const char* years[1] = { "2018"}; //, "2017p8",};
  const char* etabins[1] = { "Low"}; //"Low", "Mix", "High" };
  for (int i = 0; i < 1; i++){  //loop over quarks
    for (int j = 0; j < 1; j++){ //loop over years
      for (int k = 0; k < 1; k++){ //loop over etabins
        for (int& tau:taus){
          for (int& mg:mgs){
            MakeWeightPlots(quark[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
