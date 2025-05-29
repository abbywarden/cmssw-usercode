#include <vector>
#include <string>
#include <iostream>
#include "TMath.h"

void MakeWeightPlots(bool Is_bkg, const char* quark, int mg, int ctau, const char* etabin, const char* year)
{
  /*
  TString fn30;
  fn30.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_loweta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", 30000, mg, year);
  TString fn10;
  fn10.Form("~/nobackup/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_loweta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", 10000, mg, year);

  TFile* f30 = TFile::Open(fn30, "read");
  TFile* f10 = TFile::Open(fn10, "read");
  */
  TString fns;
  
  if (ctau < 1000)
     fns.Form("~/crabdirs/TrackMoverMCTruth_%sEta/mfv_stopl%s_tau%ium_M%04i_%s.root",etabin, quark,ctau,mg, year);
  else
    //  fns.Form("~/crabdirs/TrackMoverMCTruth_%sEta/mfv_stopl%s_tau%imm_M%02i_%s.root",etabin, quark,ctau/1000,mg, year);
    fns.Form("~/crabdirs/TrackMoverMCTruth_%sEta/mfv_stopl%s_tau%06ium_M%04i_%s.root",etabin, quark,ctau,mg, year);

  TString fnb;
  // This is for 10mm->1mm ntuple
  
  // for ctau < 1000, use 300um; for ctau > 1000, use 10mm ... 
  if (ctau < 1000)
     if (Is_bkg)
         fnb.Form("~/crabdirs/TrackMover_%sEta_0p03_noCorrection/background_leptonpresel_%s.root",etabin, year);
     else
         fnb.Form("~/crabdirs/TrackMover_%sEta_0p03_noCorrection/SingleMuon%s.root",etabin, year);
  else
     if (Is_bkg)
        //  fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_10_noCorrection/background_leptonpresel_%s.root",etabin, year);
         fnb.Form("~/crabdirs/TrackMover_%sEta_Ulv14lepm1jet1lep_10_noCorrection/ttbar_semilep_%s.root",etabin, year);

     else
         fnb.Form("~/nobackup/crabdirs/TrackMover_%sEta_10_noCorrection/SingleMuon%s.root",etabin, year);


  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");

  TString fnout;
  TString fnout2;
  TString fnout3;
  
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);
  
  if (Is_bkg){
     fnout.Form("~/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout2.Form("~/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_num_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout3.Form("~/crabdirs/TM_2D_move_weight_sim_lepton_histos/reweight_den_%seta_move_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  }
  else { 
     fnout.Form("~/crabdirs/TM_2D_move_weight_dat_lepton_histos/reweight_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout2.Form("~/crabdirs/TM_2D_move_weight_dat_lepton_histos/reweight_num_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
     fnout3.Form("~/crabdirs/TM_2D_move_weight_dat_lepton_histos/reweight_den_%seta_move_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  }
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");
  TFile* fout2 = new TFile(fnout2, "recreate");
  TFile* fout3 = new TFile(fnout3, "recreate");
  
  std::vector<TString> hns_2d_md = {"nocuts_movedist3_movedist2_den"};
  for (const auto& hn : hns_2d_md){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      //TH2D* h10 = (TH2D*)f10->Get(hn);
      //TH2D* h30 = (TH2D*)f30->Get(hn);
      //h30->Divide(h10);
      //fout2->WriteObject(h30,hn);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
      
      std::vector<double> b_Int_idx = {}; 
      std::vector<double> b_error_Int_idx = {}; 
      std::vector<double> s_Int_idx = {}; 
      std::vector<double> s_error_Int_idx = {}; 
      //std::vector<int> b_x = {16, 18, 20, 22, 24, 26, 30, 38, 50}; //{19, 21, 23, 25, 27, 29, 31, 50}; 
      //std::vector<int> b_y = {0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 36, 42, 50}; 
      //std::vector<int> b_x = {16, 18, 20, 22, 24, 26, 30, 38, 50}; //{19, 21, 23, 25, 27, 29, 31, 50}; 
      //std::vector<int> b_y = {0, 8, 12, 14, 15, 16, 18, 20, 22, 24, 26, 30, 38, 50}; 
      std::vector<int> b_x = {16, 18, 20, 22, 24, 26, 30, 38, 50}; //{19, 21, 23, 25, 27, 29, 31, 50}; 
      std::vector<int> b_y = {0, 10, 14, 16, 17, 18, 19, 20, 22, 26, 34, 50}; 
      
      for (int i = 0; i < b_x.size()-1; ++i){
         for (int j = 5-i; j < 8+i; ++j){
            if (j < 0)
              j = 0;
            double b_error_Int = 0, s_error_Int = 0;
            double b_Int = hb->IntegralAndError(b_x[i]+1,b_x[i+1],b_y[j]+1,b_y[j+1],b_error_Int, "");
            //std::cout << "Integrate h b_x " << b_x[i] << " b_y " << b_y[j] << " Int " << b_Int << " +- " <<b_error_Int << std::endl;
            b_Int_idx.push_back(b_Int);
            b_error_Int_idx.push_back(b_error_Int);

            double s_Int = hs->IntegralAndError(b_x[i]+1,b_x[i+1],b_y[j]+1,b_y[j+1],s_error_Int, "");
            //std::cout << "Integrate h b_x " << b_x[i] << " b_y " << b_y[j] << " Int " << s_Int << " +- " <<s_error_Int << std::endl;
            s_Int_idx.push_back(s_Int);
            s_error_Int_idx.push_back(s_error_Int);
         }
      }

      int ij = 0;
      for (int i = 0; i < b_x.size()-1; ++i){
        for (int j = 5-i; j < 8+i; ++j){
           if (j < 0) 
             j = 0;
           double exp_Int_idx = 0.0;
           for (int bx = 1; bx < hs->GetNbinsX()+1; bx++){
               for (int by = 1; by < hs->GetNbinsY()+1; by++){
                  if (  hs->GetBinContent(bx, by) != 0 && b_x[i] < bx && bx < b_x[i+1]+1 && b_y[j] < by && by < b_y[j+1]+1) {
                     exp_Int_idx +=  hs->GetBinContent(bx, by);
                     hb->SetBinContent(bx, by, b_Int_idx[ij]);
                     hb->SetBinError(bx, by, b_error_Int_idx[ij]);
                     hs->SetBinContent(bx, by, s_Int_idx[ij]);
                     hs->SetBinError(bx, by, s_error_Int_idx[ij]);
                  }
               }
           }
           //std::cout << "Test Integrate h b_x " << exp_Int_idx << std::endl;
           ij++;
         }
      }
      
      fout2->WriteObject(hs,hn);
      fout3->WriteObject(hb,hn);
      
      hs->Divide(hb);
      fout->WriteObject(hs,hn);
  }

  fs->Close();
  fb->Close();
  fout->Close();
  fout2->Close();
  fout3->Close();
}


void WeightFiles2Dmove_1j1lep()
{
  const char* quark[1] = { "d"}; //, "b"};
  // std::vector<int> taus = {100, 300, 1000, 3000, 10000, 30000};
  // std::vector<int> mgs = {15, 40, 55,};
  // const char* years[2] = {"20161p2", "2017p8"};
  std::vector<int> taus = {1000};
  std::vector<int> mgs = {200};
  const char* years[1] = {"2018"};
  const char* etabins[1] = {"Low"}; //, "Mix", "High"};
  for (int i = 0; i < 1; i++){   //loop on quarks 
    for (int j = 0; j < 1; j++){ //loop on years
      for (int k = 0; k < 1; k++){ //loop on etabins
        for (int& tau:taus){
          for (int& mg:mgs){
            // MakeWeightPlots(0,quark[i],mg,tau,etabins[k],years[j]);
            MakeWeightPlots(1,quark[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
