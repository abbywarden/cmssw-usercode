// #include "TH2F.h"
// #include "TRandom3.h"
// #include "CommonTools/UtilAlgos/interface/TFileService.h"
// #include "DataFormats/Math/interface/deltaR.h"
// #include "DataFormats/PatCandidates/interface/Jet.h"
// #include "FWCore/Framework/interface/EDAnalyzer.h"
// #include "FWCore/Framework/interface/Event.h"
// #include "FWCore/Framework/interface/MakerMacros.h"
// #include "FWCore/ServiceRegistry/interface/Service.h"
// #include "JMTucker/Tools/interface/ExtValue.h"
// #include "JMTucker/Tools/interface/Utilities.h"
// #include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
// #include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
// #include "JMTucker/MFVNeutralino/interface/EventTools.h"

// // if we apply this just like Event/VertexHistos ...
// // can do PreSel ...
// // OnlyOneVtx ...
// // FullSel ...

// // then in that case don't need to worry about making individual 3,4,5 trk sv here!
// // just need to be cautious in histos.py

// // create either case a): the lepton is selected --> passing lepton id or
// // b) the lepton fails lepton id but in event with a selected lepton ? 

// class MFVDispLeptHistos : public edm::EDAnalyzer {
//  public:
//   explicit MFVCutFlowHistos(const edm::ParameterSet&);
//   void analyze(const edm::Event&, const edm::EventSetup&);
   
//  private:
//   const edm::EDGetTokenT<MFVEvent> mevent_token;
//   const edm::EDGetTokenT<double> weight_token;
//   const edm::EDGetTokenT<MFVVertexAuxCollection> secondary_vertex_token;

//   //consider instead d0?
//   //consider instead dsz?

//   TH1D* h_electron_dxybs_[2];
//   TH1D* h_electron_dxypv_[2];
//   TH1D* h_electron_dzpv_[2];
//   TH1D* h_electron_dxyerr_[2];
//   TH1D* h_electron_dzerr_[2];
//   TH1D* h_electron_bs2ddist_[2];
  
//   TH1D* h_muon_dxybs_[2];
//   TH1D* h_muon_dxypv_[2];
//   TH1D* h_muon_dzpv_[2];
//   TH1D* h_muon_dxyerr_[2];
//   TH1D* h_muon_dzerr_[2];
//   TH1D* h_muon_bs2ddist_[2];


//   //consider breaking it up into elel, mumu, and elmu?
//   //one lepton needs to be a good one? 
//   TH1D* h_leppair_2ddist;
//   TH1D* h_leppair_2derr;
//   TH1D* h_leppair_2dsig;

//   TH1D* h_lepsv_2ddist;
//   TH1D* h_lepsv_2derr;
//   TH1D* h_lepsv_2dsig;

  
// };

// MFVDispLeptHistos::MFVDispLeptHistos(const edm::ParameterSet& cfg)
//   : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
//     weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
//     secondary_vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src")))


// {
//   edm::Service<TFileService> fs;

//   //TODO : Change bin and xaxis ; add better x-axis
//   h_tightel_dxybs = fs->make<TH1D>("h_tightel_dxybs", ";events", 10, 0, 2);
//   h_tightel_dxypv = fs->make<TH1D>("h_tightel_dxypv", ";events", 10, 0, 2);
//   h_tightel_dzpv = fs->make<TH1D>("h_tightel_dzpv", ";events", 10, 0, 2);
//   h_tightel_dxyerr = fs->make<TH1D>("h_tightel_dxyerr", ";events", 10, 0, 2);
//   h_tightel_dzerr = fs->make<TH1D>("h_tightel_dzerr", ";events", 10, 0, 2);

//   h_tightel_bs2ddist = fs->make<TH1D>("h_tightel_bs2ddist", ";events", 10, 0, 2);

//   h_medmu_dxybs = fs->make<TH1D>("h_medmu_dxybs", ";events", 10, 0, 2);
//   h_medmu_dxypv = fs->make<TH1D>("h_medmu_dxypv", ";events", 10, 0, 2);
//   h_medmu_dzpv = fs->make<TH1D>("h_medmu_dzpv", ";events", 10, 0, 2);
//   h_medmu_dxyerr = fs->make<TH1D>("h_medmu_dxyerr", ";events", 10, 0, 2);
//   h_medmu_dzerr = fs->make<TH1D>("h_medmu_dzerr", ";events", 10, 0, 2);
   
//   h_leppair_3ddist = fs->make<TH1D>("h_leppair_3ddist", ";events", 10, 0, 2);
//   h_leppair_3derr = fs->make<TH1D>("h_leppair_3derr", ";events", 10, 0, 2);
//   h_leppair_3dsig = fs->make<TH1D>("h_leppair_3dsig", ";events", 10, 0, 2);
  
//   h_lepsv_3ddist = fs->make<TH1D>("h_lepsv_3ddist", ";events", 10, 0, 2);
//   h_lepsv_3derr = fs->make<TH1D>("h_lepsv_3derr", ";events", 10, 0, 2);
//   h_lepsv_3dsig = fs->make<TH1D>("h_lepsv_3dsig", ";events", 10, 0, 2);


// }

// void MFVDispLeptHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
//   edm::Handle<MFVEvent> mevent;
//   event.getByToken(mevent_token, mevent);

//   edm::Handle<double> weight;
//   event.getByToken(weight_token, weight);
//   const double w = *weight;
  
//   edm::Handle<MFVVertexAuxCollection> secondary_vertices;
//   event.getByToken(secondary_vertices_token, secondary_vertices);

//   //     {"rescale_bsbs2ddist", mag(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z))},
//   //aux.x is from sv.x() etc. 

//   const int nsv = int(secondary_vertices->size());

//   for (int iel = 0; iel < mevent->nelectrons(); ++iel) {
//     if (mevent->electron_ID[iel][3] == 1) {
      
//       h_tightel_dxybs->Fill(mevent->electron_dxybs[iel], w);
//       h_tightel_dxypv->Fill(mevent->electron_dxy[iel], w);
//       h_tightel_dzpv->Fill(mevent->electron_dz[iel], w);
//       h_tightel_dxyerr->Fill(mevent->electron_dxyerr[iel], w);
//       h_tightel_dzerr->Fill(mevent->electron_dzerr[iel], w);

//     }
//   }

//   for (int imu = 0; imu < mevent->nmuons(); ++imu) {
//     if (mevent->muon_ID[imu][1] == 1) {
      
//       h_medmu_dxybs->Fill(mevent->muon_dxybs[imu], w);
//       h_medmu_dxypv->Fill(mevent->muon_dxy[imu], w);
//       h_medmu_dzpv->Fill(mevent->muon_dz[imu], w);
//       h_medmu_dxyerr->Fill(mevent->muon_dxyerr[imu], w);
//       h_medmu_dzerr->Fill(mevent->muon_dzerr[imu], w);

//     }
//   }

//   for (int isv = 0; isv < nsv; ++isv) {
    
      


  

