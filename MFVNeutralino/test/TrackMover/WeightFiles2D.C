#include <vector>
#include <string>
#include <iostream>


void MakeWeightPlots(bool Is_bkg, const char* boson, int mg, int ctau, int year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%i.root",boson,ctau/1000,mg,year);
  TString fnb;
  // This is for 10mm->1mm ntuple
  if (Is_bkg)
     fnb.Form("~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwJetByJetHistsOnnormdzulv30lepmumv6_20_tau%06ium_noCorrection/wjetstolnu_2j_%i.root", ctau, year);
  else
     fnb.Form("~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwJetByJetHistsOnnormdzulv30lepmumv6_20_tau%06ium_noCorrection/SingleMuon%i.root", ctau, year);
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  if (Is_bkg)
     fnout.Form("~/nobackup/crabdirs/TM_2D_weight_sim_lepton_histos/reweight_nopreselrelaxbspnotw_tau%imm_M%02i_%i_2D.root", ctau/1000, mg, year);
  else 
     fnout.Form("~/nobackup/crabdirs/TM_2D_weight_dat_lepton_histos/reweight_nopreselrelaxbspnotw_tau%imm_M%02i_%i_2D.root", ctau/1000, mg, year);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");
     
  std::vector<TString> hns_2d = {"nocuts_jet1_sump_jetdr_den", "nocuts_2logm_jetdr_den", "nocuts_2logm_costheta_den", "nocuts_jet_dr_closeseedtks_den", "nocuts_jet1_sump_jet_costheta_den", "nocuts_movedist3_movedist2_den"};
  //std::vector<TString> hns_2d = {"nocuts_jet1_sump_jetdr_den"};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      //hb->GetXaxis()->SetRangeUser(1.0,5.0);
      //hs->GetXaxis()->SetRangeUser(1.0,5.0);
      //hb->RebinY(2);
      //hs->RebinY(2);
      //hb->RebinX(7);
      //hs->RebinX(7);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }
  fs->Close();
  fb->Close();
  fout->Close();
}


void WeightFiles2D()
{
  const char* bosons[1]
          = { "Wplus" };
  std::vector<int> taus = {1000, 30000};//,300};
  std::vector<int> mgs = {55};
  //std::vector<int> years = {20161, 20162, 2017, 2018};
  std::vector<int> years = {2017};
  for (int i = 0; i < 1; i++){  
    for (int& year:years){
      for (int& tau:taus){
        for (int& mg:mgs){
          MakeWeightPlots(1,bosons[i],mg,tau,year);
        }
      }
    }
  }
}
