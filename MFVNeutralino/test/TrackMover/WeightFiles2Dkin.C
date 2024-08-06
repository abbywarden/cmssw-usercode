#include <vector>
#include <string>
#include <iostream>


void MakeWeightPlots(bool Is_bkg, const char* boson, int mg, int ctau, const char* etabin, const char* year)
{
  TString fns;
  //This is for the previous signal samples
  //This is for the new signal samples
  if (ctau < 1000)
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_%sEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%ium_M%02i_%s.root",etabin,boson,ctau,mg,year);
  else
     fns.Form("~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_%sEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/%sHToSSTodddd_tau%imm_M%02i_%s.root",etabin,boson,ctau/1000,mg,year);
  TString fnb;
  // This is for 10mm->1mm ntuple
  if (Is_bkg)
     fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/background_leptonpresel_%s.root", etabin, ctau, year);
  else
     fnb.Form("~/nobackup/crabdirs/TrackMover_StudyV2p4_%sEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/SingleMuon%s.root", etabin, ctau, year);
  TFile* fs = TFile::Open(fns, "read");
  TFile* fb = TFile::Open(fnb, "read");
  // This is for 10mm->1mm ntuple after sump weighting
  TString fnout;
  char *low_etabin = new char[20];
  strcpy(low_etabin, etabin);
  auto it = low_etabin;
  *it = (char) tolower(*it);

  if (Is_bkg)
     fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_sim_lepton_histos/reweight_v2p4_%seta_kin_sim_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  else
     fnout.Form("~/nobackup/crabdirs/TM_2D_kin_weight_dat_lepton_histos/reweight_v2p4_%seta_kin_dat_vetodr_tau%06ium_M%02i_%s_2D.root", low_etabin, ctau, mg, year);
  std::cout << "Getting weights from: " << std::endl;
  std::cout << fns << std::endl;
  std::cout << fnb << std::endl;
  TFile* fout = new TFile(fnout, "recreate");


  //std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den", "nocuts_llp_sump_jetdphi_den", "nocuts_nmovedseedtks0_jet0_sump_den", "nocuts_nmovedseedtks1_jet1_sump_den","nocuts_jet0_sump_jetdr_den","nocuts_jet1_sump_jetdr_den","nocuts_nmovedtks_jet_dr_den","nocuts_2logm_jetdr_den", "nocuts_jet0_sump_qrk0_dxybs_den", "nocuts_jet1_sump_qrk1_dxybs_den"}; //"nocuts_jetdr_qrk0_dxybs_den","nocuts_jetdr_qrk1_dxybs_den"};
  std::vector<TString> hns_2d = {"nocuts_llp_sump_jetdr_den", "nocuts_llp_sump_jetdphi_den",};
  for (const auto& hn : hns_2d){
      std::cout << hn << std::endl;
      TH2D* hb = (TH2D*)fb->Get(hn);
      TH2D* hs = (TH2D*)fs->Get(hn);
      //hb->RebinX(10);
      //hs->RebinX(10);
      //hb->RebinY(3);
      //hs->RebinY(3);
      hb->RebinX(60);  //60
      hs->RebinX(60); //60
      hb->RebinY(3);
      hs->RebinY(3);
      hb->Scale(1./hb->Integral());
      hs->Scale(1./hs->Integral());
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
  std::vector<int> taus = {1000,};//{100, 300, 1000, 3000, 30000};
  std::vector<int> mgs = {55,};
  const char* years[1] = { "20161p2", "2017p8",};
  const char* etabins[3] = { "Low","Mix","High" };
  for (int i = 0; i < 1; i++){  
    for (int j = 0; j < 1; j++){
      for (int k = 0; k < 3; k++){
        for (int& tau:taus){
          for (int& mg:mgs){
            if (tau==100 && mg==40)
              continue;
            MakeWeightPlots(0,bosons[i],mg,tau,etabins[k],years[j]);
            MakeWeightPlots(1,bosons[i],mg,tau,etabins[k],years[j]);
          }
        }
      }
    }
  }
}
