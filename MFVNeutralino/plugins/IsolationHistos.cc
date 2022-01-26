#include "TH2F.h"
#include "TRandom3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"

class MFVIsolationHistos : public edm::EDAnalyzer {
 public:
  explicit MFVIsolationHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
 
  
  TH1F* h_electron_had_iso_[5];
  TH1F* h_electron_neutral_iso_[5];
  TH1F* h_electron_photon_iso_[5];
  TH1F* h_electron_corr_[5];
  TH1F* h_muon_had_iso_[5];
  TH1F* h_muon_neutral_iso_[5];
  TH1F* h_muon_photon_iso_[5];
  TH1F* h_muon_corr_[5];

  TH1F* h_pfiso_muon;
  TH1F* h_pfiso_electron;
  TH1F* h_pfisonoPU_muon;
  TH1F* h_pfisonoPU_electron;

  TH1F* h_tight_electron_had_iso_[5];
  TH1F* h_tight_electron_neutral_iso_[5];
  TH1F* h_tight_electron_photon_iso_[5];
  TH1F* h_tight_electron_corr_[5];
  TH1F* h_med_muon_had_iso_[5];
  TH1F* h_med_muon_neutral_iso_[5];
  TH1F* h_med_muon_photon_iso_[5];
  TH1F* h_med_muon_corr_[5];


};


MFVIsolationHistos::MFVIsolationHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
  edm::Service<TFileService> fs;


  h_pfiso_muon = fs->make<TH1F>("h_pfiso_muon", "; Muon PFIso;muon/0.04", 50, 0, 2.0);
  h_pfisonoPU_muon = fs->make<TH1F>("h_pfisonoPU_muon", "; Muon PFIso no PU correction;muon/0.04", 50, 0, 2.0);
  h_pfiso_electron = fs->make<TH1F>("h_pfiso_electron", "; Electron PFIso;electron/0.04", 50, 0, 2.0);
  h_pfisonoPU_electron = fs->make<TH1F>("h_pfisonoPU_electron", "; Electron PFIso no PU correction;electron/0.04", 50, 0, 2.0);


  const char* dxy_ex[5] = {"a", "b", "c", "d", "e"};
  for (int i = 0; i < 5; ++i) {
    h_electron_had_iso_[i] = fs->make<TH1F>(TString::Format("h_electron_had_iso_%s", dxy_ex[i]), "; Electron Sum Pt Charged Hadron;electron/5 GeV", 20, 0, 100);
    h_electron_neutral_iso_[i] = fs->make<TH1F>(TString::Format("h_electron_neutral_iso_%s", dxy_ex[i]), "; Electron Sum Pt Neutral Hadron;electron/5 GeV", 20, 0, 100);
    h_electron_photon_iso_[i] = fs->make<TH1F>(TString::Format("h_electron_photon_iso_%s", dxy_ex[i]), "; Electron Sum Et Photon;electron/5 GeV", 20, 0, 100);
    h_electron_corr_[i] = fs->make<TH1F>(TString::Format("h_electron_corr_%s", dxy_ex[i]), "; Electron PU correction;electron/2 GeV", 25, 0, 50);

    h_muon_had_iso_[i] = fs->make<TH1F>(TString::Format("h_muon_had_iso_%s", dxy_ex[i]), "; Muon Sum Pt Charged Hadron;muon/5 GeV",40, 0, 200);
    h_muon_neutral_iso_[i] = fs->make<TH1F>(TString::Format("h_muon_neutral_iso_%s", dxy_ex[i]), "; Muon Sum Pt Neutral Hadron;muonn/5 GeV", 40, 0, 200);
    h_muon_photon_iso_[i] = fs->make<TH1F>(TString::Format("h_muon_photon_iso_%s", dxy_ex[i]), "; Muon Sum Et Photon;muon/5 GeV", 40, 0, 200);
    h_muon_corr_[i] = fs->make<TH1F>(TString::Format("h_muon_corr_%s", dxy_ex[i]), "; Muon PU correction;muon/3 GeV", 100, 0, 300);

    h_tight_electron_had_iso_[i] = fs->make<TH1F>(TString::Format("h_tight_electron_had_iso_%s", dxy_ex[i]), "; Tight Electron Sum Pt Charged Hadron;electron/5 GeV", 20, 0, 100);
    h_tight_electron_neutral_iso_[i] = fs->make<TH1F>(TString::Format("h_tight_electron_neutral_iso_%s", dxy_ex[i]),"; Tight Electron Sum Pt Neutral Hadron;electron/5 GeV", 20, 0, 100);
    h_tight_electron_photon_iso_[i] = fs->make<TH1F>(TString::Format("h_tight_electron_photon_iso_%s", dxy_ex[i]), "; Tight Electron Sum Et Photon;electron/5 GeV", 20, 0, 100);
    h_tight_electron_corr_[i] = fs->make<TH1F>(TString::Format("h_tight_electron_corr_%s", dxy_ex[i]), "; Tight Electron PU correction;electron/2 GeV", 25, 0, 50);

    h_med_muon_had_iso_[i] = fs->make<TH1F>(TString::Format("h_med_muon_had_iso_%s", dxy_ex[i]), "; Med. Muon Sum Pt Charged Hadron;muon/5 GeV", 40, 0, 200);
    h_med_muon_neutral_iso_[i] = fs->make<TH1F>(TString::Format("h_med_muon_neutral_iso_%s", dxy_ex[i]), "; Med. Muon Sum Pt Neutral Hadron;muon/5 GeV", 40, 0, 200);
    h_med_muon_photon_iso_[i] = fs->make<TH1F>(TString::Format("h_med_muon_photon_iso_%s",dxy_ex[i]), "; Med. Muon Sum Et Photon;muon/5 GeV", 40, 0, 200);
    h_med_muon_corr_[i] = fs->make<TH1F>(TString::Format("h_med_muon_corr_%s", dxy_ex[i]), "; Med. Muon PU correction;muon/3 GeV", 100, 0, 300);

  }
}

void MFVIsolationHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);
 
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
 
  
  //isolation histos
  for (int imu = 0; imu < mevent->nmuons(); ++imu) {
      

    int i = 99;
    float npPU = -1;
    float mu_iso = -1;
    float mu_isonoPU = -1;
    
    if (abs(mevent->muon_dxybs[imu]) < 0.01) 
      i = 0;
    else if (abs(mevent->muon_dxybs[imu]) >= 0.01 && abs(mevent->muon_dxybs[imu]) < 0.05) 
      i = 1;
    else if (abs(mevent->muon_dxybs[imu]) >= 0.05 && abs(mevent->muon_dxybs[imu]) < 0.1) 
      i = 2;
    else if (abs(mevent->muon_dxybs[imu]) >= 0.1 && abs(mevent->muon_dxybs[imu]) < 0.3) 
      i = 3;
    else if (abs(mevent->muon_dxybs[imu]) >=0.3) 
      i = 4;
    if (i == 99)
      continue;

    npPU = mevent->muon_neutral_iso[imu] + mevent->muon_photon_iso[imu] - 0.5*mevent->muon_PU_corr[imu];
    if (npPU > 0.0) {
      mu_iso = (mevent->muon_had_iso[imu] + npPU)/mevent->muon_pt[imu];
    }
    else {
      mu_iso = mevent->muon_had_iso[imu]/mevent->muon_pt[imu];
    }
    mu_isonoPU = (mevent->muon_had_iso[imu] + mevent->muon_neutral_iso[imu] + mevent->muon_photon_iso[imu])/mevent->muon_pt[imu];

    h_pfiso_muon->Fill(mu_iso, w);
    h_pfisonoPU_muon->Fill(mu_isonoPU, w);
    
    h_muon_had_iso_[i]->Fill(mevent->muon_had_iso[imu], w);
    h_muon_neutral_iso_[i]->Fill(mevent->muon_neutral_iso[imu], w);
    h_muon_photon_iso_[i]->Fill(mevent->muon_photon_iso[imu], w);
    h_muon_corr_[i]->Fill(mevent->muon_PU_corr[imu], w);

    if (mevent->muon_ID[imu][1] == 1) {
      h_med_muon_had_iso_[i]->Fill(mevent->muon_had_iso[imu], w);
      h_med_muon_neutral_iso_[i]->Fill(mevent->muon_neutral_iso[imu], w);
      h_med_muon_photon_iso_[i]->Fill(mevent->muon_photon_iso[imu], w);
      h_med_muon_corr_[i]->Fill(mevent->muon_PU_corr[imu], w);
      
    }
  }

  for (int iel = 0; iel < mevent->nelectrons(); ++iel) {

    int i = 99;
    float npPU = -1;
    float ele_iso = -1;
    float ele_isonoPU = -1;
    
    if (abs(mevent->electron_dxybs[iel]) < 0.01) 
      i = 0;   
    else if (abs(mevent->electron_dxybs[iel]) >= 0.01 && abs(mevent->electron_dxybs[iel]) < 0.05) 
      i = 1;   
    else if (abs(mevent->electron_dxybs[iel]) >= 0.05 && abs(mevent->electron_dxybs[iel]) < 0.1) 
      i = 2;	
    else if (abs(mevent->electron_dxybs[iel]) >= 0.1 && abs(mevent->electron_dxybs[iel]) < 0.3) 
        i = 3;	
    else if (abs(mevent->electron_dxybs[iel]) >=0.3)
      i = 4;

    if (i == 99)
      continue;

    
    npPU =  mevent->electron_neutral_iso[iel] + mevent->electron_photon_iso[iel] - mevent->electron_corr[iel];
    if (npPU > 0.0) {
      ele_iso = (mevent->electron_had_iso[iel] + npPU) / mevent->electron_pt[iel];
    }
    else {
      ele_iso = mevent->electron_had_iso[iel]/mevent->electron_pt[iel];
    }
    ele_isonoPU = (mevent->electron_had_iso[iel] + mevent->electron_neutral_iso[iel] + mevent->electron_photon_iso[iel]) / mevent->electron_pt[iel];
    
    h_pfiso_electron->Fill(ele_iso, w);
    h_pfisonoPU_electron->Fill(ele_isonoPU, w);
    h_electron_had_iso_[i]->Fill(mevent->electron_had_iso[iel], w);
    h_electron_neutral_iso_[i]->Fill(mevent->electron_neutral_iso[iel], w);
    h_electron_photon_iso_[i]->Fill(mevent->electron_photon_iso[iel], w);
    h_electron_corr_[i]->Fill(mevent->electron_corr[iel], w);

    if (mevent->electron_ID[iel][3] == 1) {
      h_tight_electron_had_iso_[i]->Fill(mevent->electron_had_iso[iel], w);
      h_tight_electron_neutral_iso_[i]->Fill(mevent->electron_neutral_iso[iel], w);
      h_tight_electron_photon_iso_[i]->Fill(mevent->electron_photon_iso[iel], w);
      h_tight_electron_corr_[i]->Fill(mevent->electron_corr[iel], w);
	
    }
  }

}
DEFINE_FWK_MODULE(MFVIsolationHistos);
