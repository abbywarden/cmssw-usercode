#include "TH2.h"
#include "JMTucker/MFVNeutralino/interface/Ntuple.h"
#include "JMTucker/Tools/interface/NtupleReader.h"

//slim -- since I need to rerun w/ rescaling applied per era - will produce ALOT -> narrow down to only what I need for absdxydzcov 
// dxyerr_vs_pt
// dszerr_vs_pt
// absdxydsz vs pt 

// TODO : clean up and make easier either running rescaled tracks --> save per era rescaling, or with no rescaling 
int main(int argc, char** argv) {
  jmt::NtupleReader<jmt::TrackingAndJetsNtuple> nr;
  
  // nr.init_options("tt/t", "TrackingTreerULV2_Lepm_cut0_etalt1p5_2016", "trackingtreerulv2_lepm", "ttbar=True, leptonic=True, all_signal=False, qcd_lep=True, met=False, diboson=True, Lepton_data=True ");
  nr.init_options("tt/t", "TrackingTreerULV2_Lepm_etagt1p5_rescaled_2016", "trackingtreerulv2_lepm", "ttbar=True, leptonic=True, all_signal=False, qcd_lep=True, met=False, diboson=True, Lepton_data=False ");
  
  if (!nr.parse_options(argc, argv) || !nr.init()) return 1;
  auto& nt = nr.nt();
  auto& ntt = nt.tracks();
  auto& ntm = nt.mu_tracks();
  auto& nte = nt.ele_tracks();

  //slimming 
  // TH1D* h_npv = new TH1D("h_npv", ";number of primary vertices", 50, 0, 50);
  // TH1D* h_bsx = new TH1D("h_bsx", ";beamspot x", 400, -0.15, 0.15);
  // TH1D* h_bsy = new TH1D("h_bsy", ";beamspot y", 400, -0.15, 0.15);
  // TH1D* h_bsz = new TH1D("h_bsz", ";beamspot z", 800, -5, 5);


  // TH1D* h_bsdxdz = new TH1D("h_bsdxdz", ";beamspot dx/dz", 100, -1e-4, 5e-4);
  // TH1D* h_bsdydz = new TH1D("h_bsdydz", ";beamspot dy/dz", 100, -1e-4, 1e-4);
  // TH1D* h_pvbsx = new TH1D("h_pvbsx", ";pvx - bsx", 400, -0.05, 0.05);
  // TH1D* h_pvbsy = new TH1D("h_pvbsy", ";pvy - bsy", 400, -0.05, 0.05); 
  // TH1D* h_pvbsz = new TH1D("h_pvbsz", ";pvz - bsz", 500, -15, 15);
  // TH2D* h_bsy_v_bsx = new TH2D("h_bsy_v_bsx", ";beamspot x;beamspot y", 4000, -1, 1, 4000, -1, 1);
  // TH2D* h_pvy_v_pvx = new TH2D("h_pvy_v_pvx", ";pvx;pvy", 400, -1, 1, 400, -1, 1);

  // enum { ele_all, ele_sel, ele_seed, max_ele_type };
  enum { ele_sel, max_ele_type };

  // TH1D* h_eletracks_pt[max_ele_type];
  // TH1D* h_eletracks_eta[max_ele_type];
  // TH1D* h_eletracks_phi[max_ele_type];
  // TH1D* h_eletracks_dxy[max_ele_type];
  // //TH1D* h_eletracks_absdxy[max_ele_type];
  // TH1D* h_eletracks_dsz[max_ele_type];
  // TH1D* h_eletracks_dz[max_ele_type];
  // TH1D* h_eletracks_absnsigmadxy[max_ele_type];
  // TH1D* h_eletracks_nsigmadxy[max_ele_type];
  // TH1D* h_eletracks_nsigmadsz[max_ele_type];
  // TH1D* h_eletracks_dxyerr[max_ele_type];
  // //TH1D* h_eletracks_dxyerr_pt[max_ele_type][max_ptslice];
  // TH1D* h_eletracks_dxydszcov[max_ele_type];
  // TH1D* h_eletracks_absdxydszcov[max_ele_type];
  // TH1D* h_eletracks_dzerr[max_ele_type];
  // TH1D* h_eletracks_dszerr[max_ele_type];
  ////////////////////////////////////////////////
  // TH1D* h_eletracks_lambdaerr[max_ele_type];
  // TH1D* h_eletracks_pterr[max_ele_type];
  // TH1D* h_eletracks_phierr[max_ele_type];
  // TH1D* h_eletracks_etaerr[max_ele_type];

  TH2D* h_eletracks_dxyerr_v_pt[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_pt_bc[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_pt_def[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_pt_d[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_pt_e[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_pt_f[max_ele_type];


  // TH2D* h_eletracks_dxyerr_v_minr[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_eta[max_ele_type];
  // TH2D* h_eletracks_dxyerr_v_phi[max_ele_type];
  
  TH2D* h_eletracks_dszerr_v_pt[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_pt_bc[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_pt_def[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_pt_d[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_pt_e[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_pt_f[max_ele_type];


  // TH2D* h_eletracks_dszerr_v_eta[max_ele_type];
  // TH2D* h_eletracks_dszerr_v_phi[max_ele_type];

  //TH2D* h_eletracks_dxydszcov_v_pt[max_ele_type];
  // TH2D* h_eletracks_dxydszcov_v_eta[max_ele_type];
  // TH2D* h_eletracks_dxydszcov_v_phi[max_ele_type];

  TH2D* h_eletracks_absdxydszcov_v_pt[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_pt_bc[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_pt_def[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_pt_d[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_pt_e[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_pt_f[max_ele_type];

  // TH2D* h_eletracks_absdxydszcov_v_eta[max_ele_type];
  // TH2D* h_eletracks_absdxydszcov_v_phi[max_ele_type];
  // TH2D* h_eletracks_eta_v_phi[max_ele_type];


  // enum { mu_all, mu_sel, mu_seed, max_mu_type };
  enum { mu_sel, max_mu_type };

  // TH1D* h_mutracks_pt[max_mu_type];
  // TH1D* h_mutracks_eta[max_mu_type];
  // TH1D* h_mutracks_phi[max_mu_type];
  // TH1D* h_mutracks_dxy[max_mu_type];
  // //TH1D* h_mutracks_absdxy[max_mu_type];
  // TH1D* h_mutracks_dsz[max_mu_type];
  // TH1D* h_mutracks_dz[max_mu_type];
  // TH1D* h_mutracks_absnsigmadxy[max_mu_type];
  // TH1D* h_mutracks_nsigmadxy[max_mu_type];
  // TH1D* h_mutracks_nsigmadsz[max_mu_type];
  // TH1D* h_mutracks_dxyerr[max_mu_type];
  // //TH1D* h_mutracks_dxyerr_pt[max_mu_type][max_ptslice];
  // TH1D* h_mutracks_dxydszcov[max_mu_type];
  // TH1D* h_mutracks_absdxydszcov[max_mu_type];
  // TH1D* h_mutracks_dzerr[max_mu_type];
  // TH1D* h_mutracks_dszerr[max_mu_type];
  ///////////////////////////////////////////////
  // TH1D* h_mutracks_lambdaerr[max_mu_type];
  // TH1D* h_mutracks_pterr[max_mu_type];
  // TH1D* h_mutracks_phierr[max_mu_type];
  // TH1D* h_mutracks_etaerr[max_mu_type];

  TH2D* h_mutracks_dxyerr_v_pt[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_pt_bc[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_pt_def[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_pt_d[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_pt_e[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_pt_f[max_mu_type];

  // TH2D* h_mutracks_dxyerr_v_minr[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_eta[max_mu_type];
  // TH2D* h_mutracks_dxyerr_v_phi[max_mu_type];

  TH2D* h_mutracks_dszerr_v_pt[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_pt_bc[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_pt_def[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_pt_d[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_pt_e[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_pt_f[max_mu_type];

  // TH2D* h_mutracks_dszerr_v_eta[max_mu_type];
  // TH2D* h_mutracks_dszerr_v_phi[max_mu_type];

  // TH2D* h_mutracks_dxydszcov_v_pt[max_mu_type];
  // TH2D* h_mutracks_dxydszcov_v_eta[max_mu_type];
  // TH2D* h_mutracks_dxydszcov_v_phi[max_mu_type];

  TH2D* h_mutracks_absdxydszcov_v_pt[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_pt_bc[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_pt_def[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_pt_d[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_pt_e[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_pt_f[max_mu_type];

  // TH2D* h_mutracks_absdxydszcov_v_eta[max_mu_type];
  // TH2D* h_mutracks_absdxydszcov_v_phi[max_mu_type];
  // TH2D* h_mutracks_eta_v_phi[max_mu_type];


  // these now by default do not have leptons with pt ≥ 20 GeV
  // enum { tk_all, tk_sel, tk_seed, max_tk_type };
  enum { tk_sel, max_tk_type };

  TH1D* h_ntracks[max_tk_type];
  // TH1D* h_tracks_pt[max_tk_type];
  // TH1D* h_tracks_eta[max_tk_type];
  // TH1D* h_tracks_phi[max_tk_type];
  // TH1D* h_tracks_dxy[max_tk_type];
  // //TH1D* h_tracks_absdxy[max_tk_type];
  // TH1D* h_tracks_dsz[max_tk_type];
  // TH1D* h_tracks_dz[max_tk_type];
  // // TH1D* h_tracks_dzpv[max_tk_type];
  // // TH1D* h_tracks_nhits[max_tk_type];
  // // TH1D* h_tracks_npxhits[max_tk_type];
  // // TH1D* h_tracks_nsthits[max_tk_type];
  // // TH1D* h_tracks_min_r[max_tk_type];
  // // TH1D* h_tracks_npxlayers[max_tk_type];
  // // TH1D* h_tracks_nstlayers[max_tk_type];
  // TH1D* h_tracks_absnsigmadxy[max_tk_type];
  // TH1D* h_tracks_nsigmadxy[max_tk_type];
  // TH1D* h_tracks_nsigmadsz[max_tk_type];

  // TH1D* h_tracks_dxyerr[max_tk_type];
  // //TH1D* h_tracks_dxyerr_pt[max_tk_type][max_ptslice];
  // TH1D* h_tracks_dxydszcov[max_tk_type];
  // TH1D* h_tracks_absdxydszcov[max_tk_type];
  // TH1D* h_tracks_dzerr[max_tk_type];
  // TH1D* h_tracks_dszerr[max_tk_type];
  // TH1D* h_tracks_lambdaerr[max_tk_type];
  // TH1D* h_tracks_pterr[max_tk_type];
  // TH1D* h_tracks_phierr[max_tk_type];
  // TH1D* h_tracks_etaerr[max_tk_type];

  // TH2D* h_tracks_nstlayers_v_eta[max_tk_type];
  // TH2D* h_tracks_dxy_v_eta[max_tk_type];
  // TH2D* h_tracks_dxy_v_phi[max_tk_type];
  // TH2D* h_tracks_dxy_v_nstlayers[max_tk_type];
  // TH2D* h_tracks_nstlayers_v_phi[max_tk_type];
  // TH2D* h_tracks_npxlayers_v_phi[max_tk_type];
  // TH2D* h_tracks_nhits_v_phi[max_tk_type];
  // TH2D* h_tracks_npxhits_v_phi[max_tk_type];
  // TH2D* h_tracks_nsthits_v_phi[max_tk_type];

  // TH2D* h_tracks_nsigmadxy_v_eta[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_nstlayers[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_dxy[max_tk_type];
  // TH2D* h_tracks_nsigmadxy_v_dxyerr[max_tk_type];

  TH2D* h_tracks_dxyerr_v_pt[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_pt_bc[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_pt_def[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_pt_d[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_pt_e[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_pt_f[max_tk_type];

  // TH2D* h_tracks_dxyerr_v_eta[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_phi[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_minr[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_dzpv[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_dxyerr_v_nstlayers[max_tk_type];

  TH2D* h_tracks_dszerr_v_pt[max_tk_type];
  // TH2D* h_tracks_dszerr_v_pt_bc[max_tk_type];
  // TH2D* h_tracks_dszerr_v_pt_def[max_tk_type];
  // TH2D* h_tracks_dszerr_v_pt_d[max_tk_type];
  // TH2D* h_tracks_dszerr_v_pt_e[max_tk_type];
  // TH2D* h_tracks_dszerr_v_pt_f[max_tk_type];


  // TH2D* h_tracks_dszerr_v_eta[max_tk_type];
  // TH2D* h_tracks_dszerr_v_phi[max_tk_type];
  // TH2D* h_tracks_dszerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_dszerr_v_dz[max_tk_type];
  // TH2D* h_tracks_dszerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_dszerr_v_nstlayers[max_tk_type];

  // TH2D* h_tracks_dxydszcov_v_pt[max_tk_type];
  // TH2D* h_tracks_dxydszcov_v_eta[max_tk_type];
  // TH2D* h_tracks_dxydszcov_v_phi[max_tk_type];

  TH2D* h_tracks_absdxydszcov_v_pt[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_pt_bc[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_pt_def[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_pt_d[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_pt_e[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_pt_f[max_tk_type];

  // TH2D* h_tracks_absdxydszcov_v_eta[max_tk_type];
  // TH2D* h_tracks_absdxydszcov_v_phi[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_pt[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_eta[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_phi[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dxy[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_dz[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_npxlayers[max_tk_type];
  // TH2D* h_tracks_lambdaerr_v_nstlayers[max_tk_type];

  //TH2D* h_tracks_eta_v_phi[max_tk_type];
  
  // const char* ex[max_tk_type] = {"all", "sel", "seed"};
  const char* ex[max_tk_type] = {"sel"};

  for (int i = 0; i < max_tk_type; ++i) {
    h_ntracks[i] = new TH1D(TString::Format("h_%s_ntracks", ex[i]), TString::Format(";number of %s tracks;events", ex[i]), 2000, 0, 2000);
    // h_tracks_pt[i] = new TH1D(TString::Format("h_%s_tracks_pt", ex[i]), TString::Format("%s tracks;tracks pt (GeV);arb. units", ex[i]), 2000, 0, 200);
    // h_tracks_eta[i] = new TH1D(TString::Format("h_%s_tracks_eta", ex[i]), TString::Format("%s tracks;tracks eta;arb. units", ex[i]), 50, -4, 4);
    // h_tracks_phi[i] = new TH1D(TString::Format("h_%s_tracks_phi", ex[i]), TString::Format("%s tracks;tracks phi;arb. units", ex[i]), 315, -3.15, 3.15);
    // h_tracks_dxy[i] = new TH1D(TString::Format("h_%s_tracks_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", ex[i]), 400, -0.2, 0.2);
    // //h_tracks_absdxy[i] = new TH1D(TString::Format("h_%s_tracks_absdxy", ex[i]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", ex[i]), 200, 0, 0.2);
    // h_tracks_dsz[i] = new TH1D(TString::Format("h_%s_tracks_dsz", ex[i]), TString::Format("%s tracks;tracks dsz (cm);arb. units", ex[i]), 400, -20, 20);
    // h_tracks_dz[i] = new TH1D(TString::Format("h_%s_tracks_dz", ex[i]), TString::Format("%s tracks;tracks dz (cm);arb. units", ex[i]), 400, -20, 20);
    // // h_tracks_dzpv[i] = new TH1D(TString::Format("h_%s_tracks_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV (cm);arb. units", ex[i]), 400, -20, 20);
    // // h_tracks_nhits[i] = new TH1D(TString::Format("h_%s_tracks_nhits", ex[i]), TString::Format("%s tracks;tracks nhits;arb. units", ex[i]), 40, 0, 40);
    // // h_tracks_npxhits[i] = new TH1D(TString::Format("h_%s_tracks_npxhits", ex[i]), TString::Format("%s tracks;tracks npxhits;arb. units", ex[i]), 40, 0, 40);
    // // h_tracks_nsthits[i] = new TH1D(TString::Format("h_%s_tracks_nsthits", ex[i]), TString::Format("%s tracks;tracks nsthits;arb. units", ex[i]), 40, 0, 40);

    // // h_tracks_min_r[i] = new TH1D(TString::Format("h_%s_tracks_min_r", ex[i]), TString::Format("%s tracks;tracks min_r;arb. units", ex[i]), 20, 0, 20);
    // // h_tracks_npxlayers[i] = new TH1D(TString::Format("h_%s_tracks_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;arb. units", ex[i]), 20, 0, 20);
    // // h_tracks_nstlayers[i] = new TH1D(TString::Format("h_%s_tracks_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;arb. units", ex[i]), 20, 0, 20);
    // h_tracks_absnsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", ex[i]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", ex[i]), 400, 0, 40);
    // h_tracks_nsigmadxy[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", ex[i]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", ex[i]), 2000, -20, 20);
    // h_tracks_nsigmadsz[i] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", ex[i]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", ex[i]), 2000, -20, 20);
    
    // h_tracks_dxyerr[i] = new TH1D(TString::Format("h_%s_tracks_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;arb. units", ex[i]), 2000, 0, 0.2);
    // h_tracks_dxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, -0.00002, 0.00002);
    // h_tracks_absdxydszcov[i] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", ex[i]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", ex[i]), 2000, 0, 0.00002);
    // h_tracks_dzerr[i] = new TH1D(TString::Format("h_%s_tracks_dzerr", ex[i]), TString::Format("%s tracks;tracks dzerr;arb. units", ex[i]), 2000, 0, 0.2);
    // h_tracks_dszerr[i] = new TH1D(TString::Format("h_%s_tracks_dszerr", ex[i]), TString::Format("%s tracks;tracks dszerr;arb. units", ex[i]), 2000, 0, 0.2);
    // // h_tracks_lambdaerr[i] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", ex[i]), TString::Format("%s tracks;tracks lambdaerr;arb. units", ex[i]), 2000, 0, 0.2);
    // // h_tracks_pterr[i] = new TH1D(TString::Format("h_%s_tracks_pterr", ex[i]), TString::Format("%s tracks;tracks pterr;arb. units", ex[i]), 200, 0, 0.2);
    // // h_tracks_phierr[i] = new TH1D(TString::Format("h_%s_tracks_phierr", ex[i]), TString::Format("%s tracks;tracks phierr;arb. units", ex[i]), 200, 0, 0.2);
    // // h_tracks_etaerr[i] = new TH1D(TString::Format("h_%s_tracks_etaerr", ex[i]), TString::Format("%s tracks;tracks etaerr;arb. units", ex[i]), 200, 0, 0.2);

    // // h_tracks_nstlayers_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nstlayers", ex[i]), 80, -4, 4, 20, 0, 20);
    // // h_tracks_dxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxy to beamspot", ex[i]), 80, -4, 4, 400, -0.2, 0.2);
    // // h_tracks_dxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxy to beamspot", ex[i]), 20, 0, 20, 400, -0.2, 0.2);
    // // h_tracks_nsigmadxy_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks nsigmadxy", ex[i]), 80, -4, 4, 200, 0, 20);
    // // h_tracks_nsigmadxy_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks nsigmadxy", ex[i]), 20, 0, 20, 200, 0, 20);
    // // h_tracks_nsigmadxy_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks nsigmadxy", ex[i]), 400, -0.2, 0.2, 200, 0, 20);
    // // h_tracks_nsigmadxy_v_dxyerr[i] = new TH2D(TString::Format("h_%s_tracks_nsigmadxy_v_dxyerr", ex[i]), TString::Format("%s tracks;tracks dxyerr;tracks nsigmadxy", ex[i]), 200, 0, 0.2, 200, 0, 20);
    // // h_tracks_dxy_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxy_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxy to beamspot", ex[i]), 315, -3.15, 3.15, 400, -0.2, 0.2);
    // // h_tracks_nstlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nstlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nstlayers", ex[i]), 315, -3.15, 3.15, 20, 0, 20);
    // // h_tracks_npxlayers_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxlayers_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxlayers", ex[i]), 315, -3.15, 3.15, 10, 0, 10);
    // // h_tracks_nhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    // // h_tracks_npxhits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_npxhits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks npxhits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);
    // // h_tracks_nsthits_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_nsthits_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks nsthits", ex[i]), 315, -3.15, 3.15, 40, 0, 40);

    h_tracks_dxyerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_pt_bc[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_BC", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_pt_def[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_DEF", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_pt_d[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_d", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_pt_e[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_e", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_pt_f[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_f", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxyerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);

    // h_tracks_dxyerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxyerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    // h_tracks_dxyerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxyerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_dxyerr_v_minr[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", ex[i]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dxyerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dxyerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_dxyerr_v_dzpv[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_dzpv", ex[i]), TString::Format("%s tracks;tracks dz to PV;tracks dxyerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_dxyerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks dxyerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dxyerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dxyerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    h_tracks_dszerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dszerr_v_pt_bc[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_BC", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dszerr_v_pt_def[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_DEF", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dszerr_v_pt_d[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_d", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dszerr_v_pt_e[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_e", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_dszerr_v_pt_f[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_f", ex[i]), TString::Format("%s tracks;tracks pt;tracks dszerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);


    // h_tracks_dszerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dszerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    // h_tracks_dszerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dszerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_dszerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks dszerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_dszerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks dszerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_dszerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks dszerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_dszerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks dszerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    // h_tracks_dxydszcov_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    // h_tracks_dxydszcov_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", ex[i]), 80, -4, 4, 2000, -0.00002, 0.00002);
    // h_tracks_dxydszcov_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", ex[i]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
    
    h_tracks_absdxydszcov_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_pt_bc[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_BC", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_pt_def[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_DEF", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_pt_d[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_d", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_pt_e[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_e", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_pt_f[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_f", ex[i]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", ex[i]), 2000, 0, 200, 2000, 0, 0.00002);
    
    // h_tracks_absdxydszcov_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", ex[i]), 80, -4, 4, 2000, 0, 0.00002);
    // h_tracks_absdxydszcov_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", ex[i]), 126, -3.15, 3.15, 2000, 0, 0.00002);

    // h_tracks_lambdaerr_v_pt[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_pt", ex[i]), TString::Format("%s tracks;tracks pt;tracks lambdaerr", ex[i]), 2000, 0, 200, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_eta[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_eta", ex[i]), TString::Format("%s tracks;tracks eta;tracks lambdaerr", ex[i]), 80, -4, 4, 2000, 0, 0.2);
    // h_tracks_lambdaerr_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks lambdaerr", ex[i]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dxy[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dxy", ex[i]), TString::Format("%s tracks;tracks dxy to beamspot;tracks lambdaerr", ex[i]), 400, -0.2, 0.2, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_dz[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_dz", ex[i]), TString::Format("%s tracks;tracks dz to beamspot;tracks lambdaerr", ex[i]), 400, -20, 20, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_npxlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_npxlayers", ex[i]), TString::Format("%s tracks;tracks npxlayers;tracks lambdaerr", ex[i]), 10, 0, 10, 200, 0, 0.2);
    // h_tracks_lambdaerr_v_nstlayers[i] = new TH2D(TString::Format("h_%s_tracks_lambdaerr_v_nstlayers", ex[i]), TString::Format("%s tracks;tracks nstlayers;tracks lambdaerr", ex[i]), 20, 0, 20, 200, 0, 0.2);

    //h_tracks_eta_v_phi[i] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", ex[i]), TString::Format("%s tracks;tracks phi;tracks eta", ex[i]), 126, -3.15, 3.15, 80, -4, 4);
  }

  //the pass mu and pass el is pt >= 20 
  // const char* eleex[max_ele_type] = {"all_ele", "sel_ele", "seed_ele"};  
  const char* eleex[max_ele_type] = {"sel_ele"};

  for (int j = 0; j < max_ele_type; ++j) {
    // h_eletracks_pt[j] = new TH1D(TString::Format("h_%s_tracks_pt", eleex[j]), TString::Format("%s tracks;tracks pt (GeV);arb. units", eleex[j]), 2000, 0, 200);
    // h_eletracks_eta[j] = new TH1D(TString::Format("h_%s_tracks_eta", eleex[j]), TString::Format("%s tracks;tracks eta;arb. units", eleex[j]), 50, -4, 4);
    // h_eletracks_phi[j] = new TH1D(TString::Format("h_%s_tracks_phi", eleex[j]), TString::Format("%s tracks;tracks phi;arb. units", eleex[j]), 315, -3.15, 3.15);
    // h_eletracks_dxy[j] = new TH1D(TString::Format("h_%s_tracks_dxy", eleex[j]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", eleex[j]), 400, -0.2, 0.2);
    // //h_eletracks_absdxy[j] = new TH1D(TString::Format("h_%s_tracks_absdxy", eleex[j]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", eleex[j]), 200, 0, 0.2);
    // h_eletracks_dsz[j] = new TH1D(TString::Format("h_%s_tracks_dsz", eleex[j]), TString::Format("%s tracks;tracks dsz (cm);arb. units", eleex[j]), 400, -20, 20);
    // h_eletracks_dz[j] = new TH1D(TString::Format("h_%s_tracks_dz", eleex[j]), TString::Format("%s tracks;tracks dz (cm);arb. units", eleex[j]), 400, -20, 20);
    // h_eletracks_absnsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", eleex[j]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", eleex[j]), 400, 0, 40);
    // h_eletracks_nsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", eleex[j]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", eleex[j]), 2000, -20, 20);
    // h_eletracks_nsigmadsz[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", eleex[j]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", eleex[j]), 2000, -20, 20);
    // h_eletracks_dxyerr[j] = new TH1D(TString::Format("h_%s_tracks_dxyerr", eleex[j]), TString::Format("%s tracks;tracks dxyerr;arb. units", eleex[j]), 2000, 0, 0.2);
    // h_eletracks_dxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", eleex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eleex[j]), 2000, -0.00002, 0.00002);
    // h_eletracks_absdxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", eleex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", eleex[j]), 2000, 0, 0.00002);
    // h_eletracks_dzerr[j] = new TH1D(TString::Format("h_%s_tracks_dzerr", eleex[j]), TString::Format("%s tracks;tracks dzerr;arb. units", eleex[j]), 2000, 0, 0.2);
    // h_eletracks_dszerr[j] = new TH1D(TString::Format("h_%s_tracks_dszerr", eleex[j]), TString::Format("%s tracks;tracks dszerr;arb. units", eleex[j]), 2000, 0, 0.2);
    
    // h_eletracks_lambdaerr[j] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", eleex[j]), TString::Format("%s tracks;tracks lambdaerr;arb. units", eleex[j]), 2000, 0, 0.2);
    // h_eletracks_pterr[j] = new TH1D(TString::Format("h_%s_tracks_pterr", eleex[j]), TString::Format("%s tracks;tracks pterr;arb. units", eleex[j]), 200, 0, 0.2);
    // h_eletracks_phierr[j] = new TH1D(TString::Format("h_%s_tracks_phierr", eleex[j]), TString::Format("%s tracks;tracks phierr;arb. units", eleex[j]), 200, 0, 0.2);
    // h_eletracks_etaerr[j] = new TH1D(TString::Format("h_%s_tracks_etaerr", eleex[j]), TString::Format("%s tracks;tracks etaerr;arb. units", eleex[j]), 200, 0, 0.2);
   
    h_eletracks_dxyerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_BC", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_DEF", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_d", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_e", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_f", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);

    // h_eletracks_dxyerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxyerr", eleex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_eletracks_dxyerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxyerr", eleex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_eletracks_dxyerr_v_minr[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", eleex[j]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", eleex[j]), 10, 0, 10, 200, 0, 0.2);
    
    h_eletracks_dszerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_BC", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_DEF", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_d", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_e", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_f", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", eleex[j]), 2000, 0, 400, 2000, 0, 0.2);

    // h_eletracks_dszerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dszerr", eleex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_eletracks_dszerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dszerr", eleex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    
    // h_eletracks_dxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    // h_eletracks_dxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", eleex[j]), 80, -4, 4, 2000, -0.00002, 0.00002);
    // h_eletracks_dxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", eleex[j]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
    
    h_eletracks_absdxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_BC", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_DEF", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_d", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_e", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_f", eleex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", eleex[j]), 2000, 0, 200, 2000, 0, 0.00002);

    // h_eletracks_absdxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", eleex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", eleex[j]), 80, -4, 4, 2000, 0, 0.00002);
    // h_eletracks_absdxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", eleex[j]), 126, -3.15, 3.15, 2000, 0, 0.00002);
    // h_eletracks_eta_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", eleex[j]), TString::Format("%s tracks;tracks phi;tracks eta", eleex[j]), 126, -3.15, 3.15, 80, -4, 4);

  }

  // const char* muex[max_mu_type] = {"all_mu", "sel_mu", "seed_mu"};
  const char* muex[max_mu_type] = {"sel_mu"};

  for (int j = 0; j < max_mu_type; ++j) {
  //   h_mutracks_pt[j] = new TH1D(TString::Format("h_%s_tracks_pt", muex[j]), TString::Format("%s tracks;tracks pt (GeV);arb. units", muex[j]), 2000, 0, 200);
  //   h_mutracks_eta[j] = new TH1D(TString::Format("h_%s_tracks_eta", muex[j]), TString::Format("%s tracks;tracks eta;arb. units", muex[j]), 50, -4, 4);
  //   h_mutracks_phi[j] = new TH1D(TString::Format("h_%s_tracks_phi", muex[j]), TString::Format("%s tracks;tracks phi;arb. units", muex[j]), 315, -3.15, 3.15);
  //   h_mutracks_dxy[j] = new TH1D(TString::Format("h_%s_tracks_dxy", muex[j]), TString::Format("%s tracks;tracks dxy to beamspot (cm);arb. units", muex[j]), 400, -0.2, 0.2);
  //  // h_mutracks_absdxy[j] = new TH1D(TString::Format("h_%s_tracks_absdxy", muex[j]), TString::Format("%s tracks;tracks |dxy| to beamspot (cm);arb. units", muex[j]), 200, 0, 0.2);
  //   h_mutracks_dsz[j] = new TH1D(TString::Format("h_%s_tracks_dsz", muex[j]), TString::Format("%s tracks;tracks dsz (cm);arb. units", muex[j]), 400, -20, 20);
  //   h_mutracks_dz[j] = new TH1D(TString::Format("h_%s_tracks_dz", muex[j]), TString::Format("%s tracks;tracks dz (cm);arb. units", muex[j]), 400, -20, 20);
  //   h_mutracks_absnsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_absnsigmadxy", muex[j]), TString::Format("%s tracks;tracks abs nsigmadxy;arb. units", muex[j]), 400, 0, 40);
  //   h_mutracks_nsigmadxy[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadxy", muex[j]), TString::Format("%s tracks;tracks nsigmadxy;arb. units", muex[j]), 2000, -20, 20);
  //   h_mutracks_nsigmadsz[j] = new TH1D(TString::Format("h_%s_tracks_nsigmadsz", muex[j]), TString::Format("%s tracks;tracks nsigmadsz;arb. units", muex[j]), 2000, -20, 20);
  //   h_mutracks_dxyerr[j] = new TH1D(TString::Format("h_%s_tracks_dxyerr", muex[j]), TString::Format("%s tracks;tracks dxyerr;arb. units", muex[j]), 2000, 0, 0.2);
  //   h_mutracks_dxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_dxydszcov", muex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", muex[j]), 2000, -0.00002, 0.00002);
  //   h_mutracks_absdxydszcov[j] = new TH1D(TString::Format("h_%s_tracks_absdxydszcov", muex[j]), TString::Format("%s tracks;tracks dxy-dsz covariance;arb. units", muex[j]), 2000, 0, 0.00002);
  //   h_mutracks_dzerr[j] = new TH1D(TString::Format("h_%s_tracks_dzerr", muex[j]), TString::Format("%s tracks;tracks dzerr;arb. units", muex[j]), 2000, 0, 0.2);
  //   h_mutracks_dszerr[j] = new TH1D(TString::Format("h_%s_tracks_dszerr", muex[j]), TString::Format("%s tracks;tracks dszerr;arb. units", muex[j]), 2000, 0, 0.2);
    
    // h_mutracks_lambdaerr[j] = new TH1D(TString::Format("h_%s_tracks_lambdaerr", muex[j]), TString::Format("%s tracks;tracks lambdaerr;arb. units", muex[j]), 2000, 0, 0.2);
    // h_mutracks_pterr[j] = new TH1D(TString::Format("h_%s_tracks_pterr", muex[j]), TString::Format("%s tracks;tracks pterr;arb. units", muex[j]), 200, 0, 0.2);
    // h_mutracks_phierr[j] = new TH1D(TString::Format("h_%s_tracks_phierr", muex[j]), TString::Format("%s tracks;tracks phierr;arb. units", muex[j]), 200, 0, 0.2);
    // h_mutracks_etaerr[j] = new TH1D(TString::Format("h_%s_tracks_etaerr", muex[j]), TString::Format("%s tracks;tracks etaerr;arb. units", muex[j]), 200, 0, 0.2);
    
    h_mutracks_dxyerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_BC", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_DEF", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_d", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_e", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_pt_f", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxyerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);

    // h_mutracks_dxyerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxyerr", muex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_mutracks_dxyerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxyerr", muex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    // h_mutracks_dxyerr_v_minr[j] = new TH2D(TString::Format("h_%s_tracks_dxyerr_v_minr", muex[j]), TString::Format("%s tracks;tracks minr;tracks dxyerrr", muex[j]), 10, 0, 10, 200, 0, 0.2);
    
    h_mutracks_dszerr_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_BC", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_DEF", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_d", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_e", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_pt_f", muex[j]), TString::Format("%s tracks;tracks pt;tracks dszerr", muex[j]), 2000, 0, 400, 2000, 0, 0.2);

    // h_mutracks_dszerr_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dszerr", muex[j]), 80, -4, 4, 2000, 0, 0.2);
    // h_mutracks_dszerr_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dszerr_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dszerr", muex[j]), 126, -3.15, 3.15, 200, 0, 0.2);
    
    // h_mutracks_dxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, -0.00002, 0.00002);
    // h_mutracks_dxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", muex[j]), 80, -4, 4, 2000, -0.00002, 0.00002);
    // h_mutracks_dxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_dxydszcov_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", muex[j]), 126, -3.15, 3.15, 200, -0.00002, 0.00002);
   
    h_mutracks_absdxydszcov_v_pt[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_pt_bc[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_BC", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_pt_def[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_DEF", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_pt_d[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_d", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_pt_e[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_e", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_pt_f[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_pt_f", muex[j]), TString::Format("%s tracks;tracks pt;tracks dxydszcov", muex[j]), 2000, 0, 200, 2000, 0, 0.00002);

   // h_mutracks_absdxydszcov_v_eta[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_eta", muex[j]), TString::Format("%s tracks;tracks eta;tracks dxydszcov", muex[j]), 80, -4, 4, 2000, 0, 0.00002);
    // h_mutracks_absdxydszcov_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_absdxydszcov_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks dxydszcov", muex[j]), 126, -3.15, 3.15, 2000, 0, 0.00002);
    // h_mutracks_eta_v_phi[j] = new TH2D(TString::Format("h_%s_tracks_eta_v_phi", muex[j]), TString::Format("%s tracks;tracks phi;tracks eta", muex[j]), 126, -3.15, 3.15, 80, -4, 4);

  }

  auto fcn = [&]() {
    const double w = nr.weight();
    if (nt.pvs().n() == 0)
      return std::make_pair(true, w);

    // h_npv->Fill(nt.pvs().n(), w);

    // h_bsx->Fill(nt.bs().x(), w);
    // h_bsy->Fill(nt.bs().y(), w);
    // h_bsz->Fill(nt.bs().z(), w);


    // h_bsdxdz->Fill(nt.bs().dxdz(), w);
    // h_bsdydz->Fill(nt.bs().dydz(), w);
    // h_bsy_v_bsx->Fill(nt.bs().x(), nt.bs().y(), w);

    // h_pvbsx->Fill(nt.pvs().x(0) - nt.bs().x(nt.pvs().z(0)), w);
    // h_pvbsy->Fill(nt.pvs().y(0) - nt.bs().y(nt.pvs().z(0)), w);
    // h_pvbsz->Fill(nt.pvs().z(0) - nt.bs().z(),              w);

    // h_pvy_v_pvx->Fill(nt.pvs().x(0), nt.pvs().y(0), w);

    int ntracks[max_tk_type] = {0};
    int neletracks[max_ele_type] = {0};
    int nmutracks[max_mu_type] = {0};
    // std::cout << "made it 2 here" << std::endl;

    //////////////////////////////////////////////
    ///                                        ///
    ///    working  with electrons & muons     ///
    ///  try 1 : no selections on lep tracks   ///
    ///     besides usual track & pt ≥ 20      ///
    //////////////////////////////////////////////

    for (int ie = 0, iee = nte.n(); ie < iee; ++ie) {
      const double pt = nte.pt(ie);
      const int min_r = nte.min_r(ie);
      const int losthits = nte.losthit(ie);
      const int npxlayers = nte.npxlayers(ie);
      const int nstlayers = nte.nstlayers(ie);
      const double dxybs = nte.dxybs(ie, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      const bool etagt1p5 = true;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(nte.eta(ie)) > 1.5;
      else
        etarange = fabs(nte.eta(ie)) < 1.5;

      double rescaled_dxyerr_el = nte.err_dxy(ie);
      double rescaled_dszerr_el = nte.err_dsz(ie);
      double rescaled_dxydszcov_el = nte.cov_34(ie);
  
      // double rescaled_dxyerr_el_bc = nte.err_dxy(ie);
      // double rescaled_dszerr_el_bc = nte.err_dsz(ie);
      // double rescaled_dxydszcov_el_bc = nte.cov_34(ie);

      // double rescaled_dxyerr_el_def = nte.err_dxy(ie);
      // double rescaled_dszerr_el_def = nte.err_dsz(ie);
      // double rescaled_dxydszcov_el_def = nte.cov_34(ie);

      // double rescaled_dxyerr_el_d = nte.err_dxy(ie);
      // double rescaled_dszerr_el_d = nte.err_dsz(ie);
      // double rescaled_dxydszcov_el_d = nte.cov_34(ie);

      // double rescaled_dxyerr_el_e = nte.err_dxy(ie);
      // double rescaled_dszerr_el_e = nte.err_dsz(ie);
      // double rescaled_dxydszcov_el_e = nte.cov_34(ie);

      // double rescaled_dxyerr_el_f = nte.err_dxy(ie);
      // double rescaled_dszerr_el_f = nte.err_dsz(ie);
      // double rescaled_dxydszcov_el_f = nte.cov_34(ie);
      
      const bool rescale_tracks = true;
      if (rescale_tracks) {
        double dxyerr_scale_el = 1.;
        double dszerr_scale_el = 1.;
        // double dxyerr_scale_el_bc = 1.;
        // double dszerr_scale_el_bc = 1.;
        // double dxyerr_scale_el_def = 1.;
        // double dszerr_scale_el_def = 1.;
        // double dxyerr_scale_el_d = 1.;
        // double dszerr_scale_el_d = 1.;
	      // double dxyerr_scale_el_e = 1.;
        // double dszerr_scale_el_e = 1.;        
        // double dxyerr_scale_el_f = 1.;
        // double dszerr_scale_el_f = 1.;
      
        if (fabs(nte.eta(ie)) < 1.5) {
          const double x = pt;

          // 2016 (comb)
          // electron
          const double e_dxy[2] = {0.9872475165147006, -8.850994623565544e-05};
          const double e_dsz[2] = {0.9642578620320479, 7.58112528781987e-05}; 

          dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

          //2016APV BC
          //electron 
          // const double e_dxy_bc[2] = {0.8405202356126538, -2.3270456678122983e-05};
          // const double e_dsz_bc[2] = {0.8333626429820029, 3.164062283057042e-05}; 

          // dxyerr_scale_el_bc = (x>=20&&x<=200)*(e_dxy_bc[0]+e_dxy_bc[1]*x);
          // dszerr_scale_el_bc = (x>=20&&x<=200)*(e_dsz_bc[0]+e_dsz_bc[1]*x);

          // //2016APV DEF
          // const double e_dxy_def[2] = {0.9178492406629266, 0.00029670459299170615};
          // const double e_dsz_def[2] = {0.923474236513722, 0.00012267456321549217}; 

          // dxyerr_scale_el_def = (x>=20&&x<=200)*(e_dxy_def[0]+e_dxy_def[1]*x);
          // dszerr_scale_el_def = (x>=20&&x<=200)*(e_dsz_def[0]+e_dsz_def[1]*x);

          // 2017 (comb)
          // electron
          // const double e_dxy[2] = {1.2004562604316833, 0.00013810883259350766};
          // const double e_dsz[2] = {1.1480361148677893, 0.0001197359400128056}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

          // // 2017B
          // // electron
          // const double e_dxy_b[2] = {1.2312900296981657, 0.00032433882405982946};
          // const double e_dsz_b[2] = {1.1302393516818257, 1.5231586100905754e-05}; 

          // dxyerr_scale_el_b = (x>=20&&x<=200)*(e_dxy_b[0]+e_dxy_b[1]*x);
          // dszerr_scale_el_b = (x>=20&&x<=200)*(e_dsz_b[0]+e_dsz_b[1]*x);

          // // 2017C
          // // electron
          // const double e_dxy_c[2] = {1.24632778626058, 8.122188831585601e-05};
          // const double e_dsz_c[2] = {1.2223777762328998, 7.452056333705388e-05}; 

          // dxyerr_scale_el_c = (x>=20&&x<=200)*(e_dxy_c[0]+e_dxy_c[1]*x);
          // dszerr_scale_el_c = (x>=20&&x<=200)*(e_dsz_c[0]+e_dsz_c[1]*x);

          // // 2017D
          // // electron
          // const double e_dxy_d[2] = {1.188122572539288, 0.00010935634624026011};
          // const double e_dsz_d[2] = {1.181020469627855, 5.292700751270349e-05}; 

          // dxyerr_scale_el_d = (x>=20&&x<=200)*(e_dxy_d[0]+e_dxy_d[1]*x);
          // dszerr_scale_el_d = (x>=20&&x<=200)*(e_dsz_d[0]+e_dsz_d[1]*x);

          // // 2017E
          // // electron
          // const double e_dxy_e[2] = {1.1056648736687922, 0.0003349657998984838};
          // const double e_dsz_e[2] = {1.0720434659109024, 7.156351872521314e-05}; 

          // dxyerr_scale_el_e = (x>=20&&x<=200)*(e_dxy_e[0]+e_dxy_e[1]*x);
          // dszerr_scale_el_e = (x>=20&&x<=200)*(e_dsz_e[0]+e_dsz_e[1]*x);

          // // 2017F
          // // electron
          // const double e_dxy_f[2] = {1.217188167627008, 0.00037961215262325397};
          // const double e_dsz_f[2] = {1.1444183556294516, 0.00026021327096494625}; 

          // dxyerr_scale_el_f = (x>=20&&x<=200)*(e_dxy_f[0]+e_dxy_f[1]*x);
          // dszerr_scale_el_f = (x>=20&&x<=200)*(e_dsz_f[0]+e_dsz_f[1]*x);


          // 2018 
          // electron
          // const double e_dxy[2] = {1.0887960716162157, 0.0004003433426757602};
          // const double e_dsz[2] = {1.0795673316558174, 6.955423249170069e-05}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

      	}
      	else {
      	  const double x = pt;

          // 2016 (comb)
          // electron
          const double e_dxy[2] = {0.9628578293270929, 5.133752910193006e-05};
          const double e_dsz[2] = {1.0240437296961853, 0.00013154054768041174}; 

          dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

          //2016APV BC
          //electron 
          // const double e_dxy_bc[2] = {0.8278857464272988, 9.89827118842478e-05};
          // const double e_dsz_bc[2] = {0.8208769563746516, -0.00039840657905866866}; 

          // dxyerr_scale_el_bc = (x>=20&&x<=200)*(e_dxy_bc[0]+e_dxy_bc[1]*x);
          // dszerr_scale_el_bc = (x>=20&&x<=200)*(e_dsz_bc[0]+e_dsz_bc[1]*x);

          // //2016APV DEF
          // const double e_dxy_def[2] = {0.8966130887918794, 0.0003231029044753978};
          // const double e_dsz_def[2] = {0.9835128580273846, -2.3729181926182563e-05}; 

          // dxyerr_scale_el_def = (x>=20&&x<=200)*(e_dxy_def[0]+e_dxy_def[1]*x);
          // dszerr_scale_el_def = (x>=20&&x<=200)*(e_dsz_def[0]+e_dsz_def[1]*x);

          //2017
          //electron
          // const double e_dxy[2] = {1.2229654232763405, -0.0003317884256202105};
          // const double e_dsz[2] = {1.2484828975970736, -9.174600320183135e-06}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

          // // 2017B
          // // electron
          // const double e_dxy_b[2] = {1.194475778317351, -0.0005006930665749348};
          // const double e_dsz_b[2] = {1.1416269064698705, -0.0003048956175720624}; 

          // dxyerr_scale_el_b = (x>=20&&x<=200)*(e_dxy_b[0]+e_dxy_b[1]*x);
          // dszerr_scale_el_b = (x>=20&&x<=200)*(e_dsz_b[0]+e_dsz_b[1]*x);

          // // 2017C
          // // electron
          // const double e_dxy_c[2] = {1.235725067834602, -0.00044893846880360126};
          // const double e_dsz_c[2] = {1.3125861351498498, -0.00023593138502184946}; 

          // dxyerr_scale_el_c = (x>=20&&x<=200)*(e_dxy_c[0]+e_dxy_c[1]*x);
          // dszerr_scale_el_c = (x>=20&&x<=200)*(e_dsz_c[0]+e_dsz_c[1]*x);

          // // 2017D
          // // electron
          // const double e_dxy_d[2] = {1.192866479086086, -0.0003907170600610122};
          // const double e_dsz_d[2] = {1.1540523564016911, -0.00011511528792911702}; 

          // dxyerr_scale_el_d = (x>=20&&x<=200)*(e_dxy_d[0]+e_dxy_d[1]*x);
          // dszerr_scale_el_d = (x>=20&&x<=200)*(e_dsz_d[0]+e_dsz_d[1]*x);

          // // 2017E
          // // electron
          // const double e_dxy_e[2] = {1.1610729141155178, -0.00010401122022239868};
          // const double e_dsz_e[2] = {1.0735338555957084, -3.271202258233602e-06}; 

          // dxyerr_scale_el_e = (x>=20&&x<=200)*(e_dxy_e[0]+e_dxy_e[1]*x);
          // dszerr_scale_el_e = (x>=20&&x<=200)*(e_dsz_e[0]+e_dsz_e[1]*x);

          // // 2017F
          // // electron
          // const double e_dxy_f[2] = {1.2776378220566587, -8.512519627691499e-05};
          // const double e_dsz_f[2] = {1.4197911888731871, 0.00029376220042454283}; 

          // dxyerr_scale_el_f = (x>=20&&x<=200)*(e_dxy_f[0]+e_dxy_f[1]*x);
          // dszerr_scale_el_f = (x>=20&&x<=200)*(e_dsz_f[0]+e_dsz_f[1]*x);


          //2018 
          //electron
          // const double e_dxy[2] = {1.1690789120778935, -0.0002688867684453441};
          // const double e_dsz[2] = {1.0601076771323432, 0.00017122579884616858}; 

          // dxyerr_scale_el = (x>=20&&x<=200)*(e_dxy[0]+e_dxy[1]*x);
          // dszerr_scale_el = (x>=20&&x<=200)*(e_dsz[0]+e_dsz[1]*x);

        }
        rescaled_dxyerr_el *= dxyerr_scale_el;
        rescaled_dxydszcov_el *= sqrt(dxyerr_scale_el);
        rescaled_dszerr_el *= dszerr_scale_el;
        rescaled_dxydszcov_el *= sqrt(dszerr_scale_el);

        // rescaled_dxyerr_el_bc *= dxyerr_scale_el_bc;
        // rescaled_dxydszcov_el_bc *= sqrt(dxyerr_scale_el_bc);
        // rescaled_dszerr_el_bc *= dszerr_scale_el_bc;
        // rescaled_dxydszcov_el_bc *= sqrt(dszerr_scale_el_bc);

        // rescaled_dxyerr_el_def *= dxyerr_scale_el_def;
        // rescaled_dxydszcov_el_def *= sqrt(dxyerr_scale_el_def);
        // rescaled_dszerr_el_def *= dszerr_scale_el_def;
        // rescaled_dxydszcov_el_def *= sqrt(dszerr_scale_el_def);

        // rescaled_dxyerr_el_d *= dxyerr_scale_el_d;
        // rescaled_dxydszcov_el_d *= sqrt(dxyerr_scale_el_d);
        // rescaled_dszerr_el_d *= dszerr_scale_el_d;
        // rescaled_dxydszcov_el_d *= sqrt(dszerr_scale_el_d);

        // rescaled_dxyerr_el_e *= dxyerr_scale_el_e;
        // rescaled_dxydszcov_el_e *= sqrt(dxyerr_scale_el_e);
        // rescaled_dszerr_el_e *= dszerr_scale_el_e;
        // rescaled_dxydszcov_el_e *= sqrt(dszerr_scale_el_e);

        // rescaled_dxyerr_el_f *= dxyerr_scale_el_f;
        // rescaled_dxydszcov_el_f *= sqrt(dxyerr_scale_el_f);
        // rescaled_dszerr_el_f *= dszerr_scale_el_f;
        // rescaled_dxydszcov_el_f *= sqrt(dszerr_scale_el_f);


      }
      const double nsigmadxy_el = dxybs / rescaled_dxyerr_el;

      const bool nm1[5] = {
        pt > 1,
        min_r <= 1 || (min_r == 2 && losthits == 0),
        npxlayers >= 2,
        nstlayers >= 6,
        nsigmadxy_el > 3
  
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      // const bool seed = sel && nm1[4];

      // const bool tk_ok[max_ele_type] = { true, sel, seed };
      const bool tk_ok[max_ele_type] = { sel };

      for (int i = 0; i < max_ele_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++neletracks[i];

        // h_eletracks_pt[i]->Fill(pt, w);
        // h_eletracks_eta[i]->Fill(nte.eta(ie), w);
        // h_eletracks_phi[i]->Fill(nte.phi(ie), w);
        // h_eletracks_dxy[i]->Fill(dxybs, w);
        // h_eletracks_dsz[i]->Fill(nte.dsz(ie), w);
        // h_eletracks_dz[i]->Fill(nte.dz(ie), w);

        // h_eletracks_absnsigmadxy[i]->Fill(nsigmadxy_el, w);
        // h_eletracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr_el, w);
        // h_eletracks_nsigmadsz[i]->Fill(nte.dsz(ie) / rescaled_dszerr_el, w);
        
        // h_eletracks_dxyerr[i]->Fill(rescaled_dxyerr_el, w);
        // h_eletracks_dxydszcov[i]->Fill(rescaled_dxydszcov_el, w);
        // h_eletracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov_el), w);
        // h_eletracks_dzerr[i]->Fill(nte.err_dz(ie), w);
        // h_eletracks_dszerr[i]->Fill(rescaled_dszerr_el, w);
        // // h_eletracks_lambdaerr[i]->Fill(nte.err_lambda(ie), w);
        // // h_eletracks_pterr[i]->Fill(nte.err_pt(ie), w);
        // // h_eletracks_phierr[i]->Fill(nte.err_phi(ie), w);
        // // h_eletracks_etaerr[i]->Fill(nte.err_eta(ie), w);

        h_eletracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr_el, w);
        // h_eletracks_dxyerr_v_pt_bc[i]->Fill(pt, rescaled_dxyerr_el_bc, w);
        // h_eletracks_dxyerr_v_pt_def[i]->Fill(pt, rescaled_dxyerr_el_def, w);
        // h_eletracks_dxyerr_v_pt_d[i]->Fill(pt, rescaled_dxyerr_el_d, w);
        // h_eletracks_dxyerr_v_pt_e[i]->Fill(pt, rescaled_dxyerr_el_e, w);
        // h_eletracks_dxyerr_v_pt_f[i]->Fill(pt, rescaled_dxyerr_el_f, w);

        // h_eletracks_dxyerr_v_eta[i]->Fill(nte.eta(ie), rescaled_dxyerr_el, w);
        // h_eletracks_dxyerr_v_phi[i]->Fill(nte.phi(ie), rescaled_dxyerr_el, w);
        // h_eletracks_dxyerr_v_minr[i]->Fill(nte.min_r(ie), rescaled_dxyerr_el, w);

        h_eletracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr_el, w);
        // h_eletracks_dszerr_v_pt_bc[i]->Fill(pt, rescaled_dszerr_el_bc, w);
        // h_eletracks_dszerr_v_pt_def[i]->Fill(pt, rescaled_dszerr_el_def, w);
        // h_eletracks_dszerr_v_pt_d[i]->Fill(pt, rescaled_dszerr_el_d, w);
        // h_eletracks_dszerr_v_pt_e[i]->Fill(pt, rescaled_dszerr_el_e, w);
        // h_eletracks_dszerr_v_pt_f[i]->Fill(pt, rescaled_dszerr_el_f, w);

        // h_eletracks_dszerr_v_eta[i]->Fill(nte.eta(ie), rescaled_dszerr_el, w);
        // h_eletracks_dszerr_v_phi[i]->Fill(nte.phi(ie), rescaled_dszerr_el, w);
        
        // h_eletracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov_el, w);
        // h_eletracks_dxydszcov_v_eta[i]->Fill(nte.eta(ie), rescaled_dxydszcov_el, w);
        // h_eletracks_dxydszcov_v_phi[i]->Fill(nte.phi(ie), rescaled_dxydszcov_el, w);

        h_eletracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov_el), w);
        // h_eletracks_absdxydszcov_v_pt_bc[i]->Fill(pt, fabs(rescaled_dxydszcov_el_bc), w);
        // h_eletracks_absdxydszcov_v_pt_def[i]->Fill(pt, fabs(rescaled_dxydszcov_el_def), w);
        // h_eletracks_absdxydszcov_v_pt_d[i]->Fill(pt, fabs(rescaled_dxydszcov_el_d), w);
        // h_eletracks_absdxydszcov_v_pt_e[i]->Fill(pt, fabs(rescaled_dxydszcov_el_e), w);
        // h_eletracks_absdxydszcov_v_pt_f[i]->Fill(pt, fabs(rescaled_dxydszcov_el_f), w);

        // h_eletracks_absdxydszcov_v_eta[i]->Fill(nte.eta(ie), fabs(rescaled_dxydszcov_el), w);
        // h_eletracks_absdxydszcov_v_phi[i]->Fill(nte.phi(ie), fabs(rescaled_dxydszcov_el), w);
        // h_eletracks_eta_v_phi[i]->Fill(nte.phi(ie), nte.eta(ie), w);
      }
    }


    for (int im = 0, imm = ntm.n(); im < imm; ++im) {
      const double pt = ntm.pt(im);
      const int min_r = ntm.min_r(im);
      const int losthits = ntm.losthit(im);
      const int npxlayers = ntm.npxlayers(im);
      const int nstlayers = ntm.nstlayers(im);
      const double dxybs = ntm.dxybs(im, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      const bool etagt1p5 = true;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntm.eta(im)) > 1.5;
      else
        etarange = fabs(ntm.eta(im)) < 1.5;

      double rescaled_dxyerr_mu = ntm.err_dxy(im);
      double rescaled_dszerr_mu = ntm.err_dsz(im);
      double rescaled_dxydszcov_mu = ntm.cov_34(im);
      
      // double rescaled_dxyerr_mu_bc = ntm.err_dxy(im);
      // double rescaled_dszerr_mu_bc = ntm.err_dsz(im);
      // double rescaled_dxydszcov_mu_bc = ntm.cov_34(im);

      // double rescaled_dxyerr_mu_def = ntm.err_dxy(im);
      // double rescaled_dszerr_mu_def = ntm.err_dsz(im);
      // double rescaled_dxydszcov_mu_def = ntm.cov_34(im);

      // double rescaled_dxyerr_mu_d = ntm.err_dxy(im);
      // double rescaled_dszerr_mu_d = ntm.err_dsz(im);
      // double rescaled_dxydszcov_mu_d = ntm.cov_34(im);

      // double rescaled_dxyerr_mu_e = ntm.err_dxy(im);
      // double rescaled_dszerr_mu_e = ntm.err_dsz(im);
      // double rescaled_dxydszcov_mu_e = ntm.cov_34(im);

      // double rescaled_dxyerr_mu_f = ntm.err_dxy(im);
      // double rescaled_dszerr_mu_f = ntm.err_dsz(im);
      // double rescaled_dxydszcov_mu_f = ntm.cov_34(im);


      const bool rescale_tracks = true;
      if (rescale_tracks) {
        double dxyerr_scale_mu = 1.;
        double dszerr_scale_mu = 1.;

        // double dxyerr_scale_mu_bc = 1.;
        // double dszerr_scale_mu_bc = 1.;
        // double dxyerr_scale_mu_def = 1.;
        // double dszerr_scale_mu_def = 1.;
        // double dxyerr_scale_mu_d = 1.;
        // double dszerr_scale_mu_d = 1.;
	      // double dxyerr_scale_mu_e = 1.;
        // double dszerr_scale_mu_e = 1.;        
        // double dxyerr_scale_mu_f = 1.;
        // double dszerr_scale_mu_f = 1.;
	
        if (fabs(ntm.eta(im)) < 1.5) {
          const double x = pt;

          //2016 
          //muon
          const double m_dxy[2] = {0.9611958864356989, -0.00016690120737859228};
          const double m_dsz[2] = {0.9791557354765856, -2.8698379505563004e-05}; 

          dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);


          // // 2016APVBC
          // // muon
          // const double m_dxy_bc[2] = {0.8500429770635187, -0.0004664947608015134};
          // const double m_dsz_bc[2] = {0.8508937795307924, -5.303767310161755e-05}; 

          // dxyerr_scale_mu_bc = (x>=20&&x<=200)*(m_dxy_bc[0]+m_dxy_bc[1]*x);
          // dszerr_scale_mu_bc = (x>=20&&x<=200)*(m_dsz_bc[0]+m_dsz_bc[1]*x);

          // // // 2016APVDEF
          // // // muon
          // const double m_dxy_def[2] = {0.9172351455486711, -0.00022646993488081423};
          // const double m_dsz_def[2] = {0.9360279135890588, -0.00010470257461797812}; 

          // dxyerr_scale_mu_def = (x>=20&&x<=200)*(m_dxy_def[0]+m_dxy_def[1]*x);
          // dszerr_scale_mu_def = (x>=20&&x<=200)*(m_dsz_def[0]+m_dsz_def[1]*x);


          //2017
          //muon
          // const double m_dxy[2] = {1.1679130430612024, 4.4506497840034534e-05};
          // const double m_dsz[2] = {1.1696142184228187, -1.3767516703471275e-05}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);

          // // 2017B
          // // muon
          // const double m_dxy_b[2] = {1.2029378995872801, 0.00021194662169056293};
          // const double m_dsz_b[2] = {1.1537696465420137, -0.00013815080455450643}; 

          // dxyerr_scale_mu_b = (x>=20&&x<=200)*(m_dxy_b[0]+m_dxy_b[1]*x);
          // dszerr_scale_mu_b = (x>=20&&x<=200)*(m_dsz_b[0]+m_dsz_b[1]*x);

          // // 2017C
          // // muon
          // const double m_dxy_c[2] = {1.2186236617871937, 0.00019568422325389953};
          // const double m_dsz_c[2] = {1.2558210890130663, -6.763380220721829e-05}; 

          // dxyerr_scale_mu_c = (x>=20&&x<=200)*(m_dxy_c[0]+m_dxy_c[1]*x);
          // dszerr_scale_mu_c = (x>=20&&x<=200)*(m_dsz_c[0]+m_dsz_c[1]*x);

          // // 2017D
          // // muon
          // const double m_dxy_d[2] = {1.1834123898295137, -0.00016479766652728427};
          // const double m_dsz_d[2] = {1.210289871203046, -6.925115365641853e-05}; 

          // dxyerr_scale_mu_d = (x>=20&&x<=200)*(m_dxy_d[0]+m_dxy_d[1]*x);
          // dszerr_scale_mu_d = (x>=20&&x<=200)*(m_dsz_d[0]+m_dsz_d[1]*x);

          // // 2017E
          // // muon
          // const double m_dxy_e[2] = {1.093483370852844, -0.00014788035113845466};
          // const double m_dsz_e[2] = {1.0968191324161674, -6.744217018386962e-05}; 

          // dxyerr_scale_mu_e = (x>=20&&x<=200)*(m_dxy_e[0]+m_dxy_e[1]*x);
          // dszerr_scale_mu_e = (x>=20&&x<=200)*(m_dsz_e[0]+m_dsz_e[1]*x);

          // // 2017F
          // // muon
          // const double m_dxy_f[2] = {1.17893831060346, -2.9194708819218346e-05};
          // const double m_dsz_f[2] = {1.1691102052500675, -0.000125854364936848}; 

          // dxyerr_scale_mu_f = (x>=20&&x<=200)*(m_dxy_f[0]+m_dxy_f[1]*x);
          // dszerr_scale_mu_f = (x>=20&&x<=200)*(m_dsz_f[0]+m_dsz_f[1]*x);


          //2018 
          //muon
          // const double m_dxy[2] = {1.0733321649423013, -0.00022381355239655103};
          // const double m_dsz[2] = {1.0970797050838033, -5.003201772685838e-05}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);

        }
        else {
      	  const double x = pt;

          //2016 
          //muon
          const double m_dxy[2] = {1.0044056231377168, -0.00017349440187459757};
          const double m_dsz[2] = {0.9923656375200799, -6.14950227197427e-05}; 

          dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);

          // 2016APVBC
          // muon
          // const double m_dxy_bc[2] = {0.8500429770635187, -0.0004664947608015134};
          // const double m_dsz_bc[2] = {0.7791737786137813, -0.0002245943684251652}; 

          // dxyerr_scale_mu_bc = (x>=20&&x<=200)*(m_dxy_bc[0]+m_dxy_bc[1]*x);
          // dszerr_scale_mu_bc = (x>=20&&x<=200)*(m_dsz_bc[0]+m_dsz_bc[1]*x);

          // // 2016APVDEF
          // // muon
          // const double m_dxy_def[2] = {0.889415454682025, -0.00025668237298784227};
          // const double m_dsz_def[2] = {0.93585793804968, -0.00012668122442242163}; 

          // dxyerr_scale_mu_def = (x>=20&&x<=200)*(m_dxy_def[0]+m_dxy_def[1]*x);
          // dszerr_scale_mu_def = (x>=20&&x<=200)*(m_dsz_def[0]+m_dsz_def[1]*x);

          //2017
          //muon
          // const double m_dxy[2] = {1.2717323290582505, -0.0003612243743505595};
          // const double m_dsz[2] = {1.214371356004094, -0.00013090803667572745}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);

          // // 2017B
          // // muon
          // const double m_dxy_b[2] = {1.2805288429006463, -0.0004655395286243015};
          // const double m_dsz_b[2] = {1.094802867952775, -0.00016840018580808504}; 

          // dxyerr_scale_mu_b = (x>=20&&x<=200)*(m_dxy_b[0]+m_dxy_b[1]*x);
          // dszerr_scale_mu_b = (x>=20&&x<=200)*(m_dsz_b[0]+m_dsz_b[1]*x);

          // // 2017C
          // // muon
          // const double m_dxy_c[2] = {1.3114715883411945, -0.0005460967294515021};
          // const double m_dsz_c[2] = {1.2567894389648686, -0.00010318384636457192}; 

          // dxyerr_scale_mu_c = (x>=20&&x<=200)*(m_dxy_c[0]+m_dxy_c[1]*x);
          // dszerr_scale_mu_c = (x>=20&&x<=200)*(m_dsz_c[0]+m_dsz_c[1]*x);

          // // 2017D
          // // muon
          // const double m_dxy_d[2] = {1.2809735039671792, -0.0004336302757189936};
          // const double m_dsz_d[2] = {1.1532203568642658, 4.971779367657185e-05}; 

          // dxyerr_scale_mu_d = (x>=20&&x<=200)*(m_dxy_d[0]+m_dxy_d[1]*x);
          // dszerr_scale_mu_d = (x>=20&&x<=200)*(m_dsz_d[0]+m_dsz_d[1]*x);

          // // 2017E
          // // muon
          // const double m_dxy_e[2] = {1.2215271549920654, -0.00032050405912464365};
          // const double m_dsz_e[2] = {1.0482975828506627, -8.024159003983122e-05}; 

          // dxyerr_scale_mu_e = (x>=20&&x<=200)*(m_dxy_e[0]+m_dxy_e[1]*x);
          // dszerr_scale_mu_e = (x>=20&&x<=200)*(m_dsz_e[0]+m_dsz_e[1]*x);

          // // 2017F
          // // muon
          // const double m_dxy_f[2] = {1.2793171801775352, -0.00028276241463419047};
          // const double m_dsz_f[2] = {1.3491903590651946, -5.7680167988726286e-05}; 

          // dxyerr_scale_mu_f = (x>=20&&x<=200)*(m_dxy_f[0]+m_dxy_f[1]*x);
          // dszerr_scale_mu_f = (x>=20&&x<=200)*(m_dsz_f[0]+m_dsz_f[1]*x);


          //2018 
          //muon
          // const double m_dxy[2] = {1.1671282639537564, -0.00011353017593021021};
          // const double m_dsz[2] = {1.052454790745076, 7.30128423571258e-07}; 

          // dxyerr_scale_mu = (x>=20&&x<=200)*(m_dxy[0]+m_dxy[1]*x);
          // dszerr_scale_mu = (x>=20&&x<=200)*(m_dsz[0]+m_dsz[1]*x);

        }
        rescaled_dxyerr_mu *= dxyerr_scale_mu;
        rescaled_dxydszcov_mu *= sqrt(dxyerr_scale_mu);
        rescaled_dszerr_mu *= dszerr_scale_mu;
        rescaled_dxydszcov_mu *= sqrt(dszerr_scale_mu);

        // rescaled_dxyerr_mu_bc *= dxyerr_scale_mu_bc;
        // rescaled_dxydszcov_mu_bc *= sqrt(dxyerr_scale_mu_bc);
        // rescaled_dszerr_mu_bc *= dszerr_scale_mu_bc;
        // rescaled_dxydszcov_mu_bc *= sqrt(dszerr_scale_mu_bc);

        // rescaled_dxyerr_mu_def *= dxyerr_scale_mu_def;
        // rescaled_dxydszcov_mu_def *= sqrt(dxyerr_scale_mu_def);
        // rescaled_dszerr_mu_def *= dszerr_scale_mu_def;
        // rescaled_dxydszcov_mu_def *= sqrt(dszerr_scale_mu_def);

        // rescaled_dxyerr_mu_d *= dxyerr_scale_mu_d;
        // rescaled_dxydszcov_mu_d *= sqrt(dxyerr_scale_mu_d);
        // rescaled_dszerr_mu_d *= dszerr_scale_mu_d;
        // rescaled_dxydszcov_mu_d *= sqrt(dszerr_scale_mu_d);

        // rescaled_dxyerr_mu_e *= dxyerr_scale_mu_e;
        // rescaled_dxydszcov_mu_e *= sqrt(dxyerr_scale_mu_e);
        // rescaled_dszerr_mu_e *= dszerr_scale_mu_e;
        // rescaled_dxydszcov_mu_e *= sqrt(dszerr_scale_mu_e);

        // rescaled_dxyerr_mu_f *= dxyerr_scale_mu_f;
        // rescaled_dxydszcov_mu_f *= sqrt(dxyerr_scale_mu_f);
        // rescaled_dszerr_mu_f *= dszerr_scale_mu_f;
        // rescaled_dxydszcov_mu_f *= sqrt(dszerr_scale_mu_f);
      }
      const double nsigmadxy_mu = dxybs / rescaled_dxyerr_mu;

      const bool nm1[5] = {
	      pt > 1,
	      min_r <= 1 || (min_r == 2 && losthits == 0),
	      npxlayers >= 2,
	      nstlayers >= 6,
	      nsigmadxy_mu > 3
	
      };

      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      // const bool seed = sel && nm1[4];

      // const bool tk_ok[max_mu_type] = { true, sel, seed };
      const bool tk_ok[max_mu_type] = {sel};

      for (int i = 0; i < max_mu_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++nmutracks[i];

        // h_mutracks_pt[i]->Fill(pt, w);
        // h_mutracks_eta[i]->Fill(ntm.eta(im), w);
        // h_mutracks_phi[i]->Fill(ntm.phi(im), w);
        // h_mutracks_dxy[i]->Fill(dxybs, w);
        // h_mutracks_dsz[i]->Fill(ntm.dsz(im), w);
        // h_mutracks_dz[i]->Fill(ntm.dz(im), w);

        // h_mutracks_absnsigmadxy[i]->Fill(nsigmadxy_mu, w);
        // h_mutracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr_mu, w);
        // h_mutracks_nsigmadsz[i]->Fill(ntm.dsz(im) / rescaled_dszerr_mu, w);
        
        // h_mutracks_dxyerr[i]->Fill(rescaled_dxyerr_mu, w);
        // h_mutracks_dxydszcov[i]->Fill(rescaled_dxydszcov_mu, w);
        // h_mutracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov_mu), w);
        // h_mutracks_dzerr[i]->Fill(ntm.err_dz(im), w);
        // h_mutracks_dszerr[i]->Fill(rescaled_dszerr_mu, w);
        // // h_mutracks_lambdaerr[i]->Fill(ntm.err_lambda(im), w);
        // // h_mutracks_pterr[i]->Fill(ntm.err_pt(im), w);
        // // h_mutracks_phierr[i]->Fill(ntm.err_phi(im), w);
        // // h_mutracks_etaerr[i]->Fill(ntm.err_eta(im), w);

        h_mutracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr_mu, w);
        // h_mutracks_dxyerr_v_pt_bc[i]->Fill(pt, rescaled_dxyerr_mu_bc, w);
        // h_mutracks_dxyerr_v_pt_def[i]->Fill(pt, rescaled_dxyerr_mu_def, w);
        // h_mutracks_dxyerr_v_pt_d[i]->Fill(pt, rescaled_dxyerr_mu_d, w);
        // h_mutracks_dxyerr_v_pt_e[i]->Fill(pt, rescaled_dxyerr_mu_e, w);
        // h_mutracks_dxyerr_v_pt_f[i]->Fill(pt, rescaled_dxyerr_mu_f, w);

        // h_mutracks_dxyerr_v_eta[i]->Fill(ntm.eta(im), rescaled_dxyerr_mu, w);
        // h_mutracks_dxyerr_v_phi[i]->Fill(ntm.phi(im), rescaled_dxyerr_mu, w);
        // h_mutracks_dxyerr_v_minr[i]->Fill(ntm.min_r(im), rescaled_dxyerr_mu, w);

        h_mutracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr_mu, w);
        // h_mutracks_dszerr_v_pt_bc[i]->Fill(pt, rescaled_dszerr_mu_bc, w);
        // h_mutracks_dszerr_v_pt_def[i]->Fill(pt, rescaled_dszerr_mu_def, w);
        // h_mutracks_dszerr_v_pt_d[i]->Fill(pt, rescaled_dszerr_mu_d, w);
        // h_mutracks_dszerr_v_pt_e[i]->Fill(pt, rescaled_dszerr_mu_e, w);
        // h_mutracks_dszerr_v_pt_f[i]->Fill(pt, rescaled_dszerr_mu_f, w);

        // h_mutracks_dszerr_v_eta[i]->Fill(ntm.eta(im), rescaled_dszerr_mu, w);
        // h_mutracks_dszerr_v_phi[i]->Fill(ntm.phi(im), rescaled_dszerr_mu, w);
        
        // h_mutracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov_mu, w);
        // h_mutracks_dxydszcov_v_eta[i]->Fill(ntm.eta(im), rescaled_dxydszcov_mu, w);
        // h_mutracks_dxydszcov_v_phi[i]->Fill(ntm.phi(im), rescaled_dxydszcov_mu, w);

        h_mutracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov_mu), w);
        // h_mutracks_absdxydszcov_v_pt_bc[i]->Fill(pt, fabs(rescaled_dxydszcov_mu_bc), w);
        // h_mutracks_absdxydszcov_v_pt_def[i]->Fill(pt, fabs(rescaled_dxydszcov_mu_def), w);
        // h_mutracks_absdxydszcov_v_pt_d[i]->Fill(pt, fabs(rescaled_dxydszcov_mu_d), w);
        // h_mutracks_absdxydszcov_v_pt_e[i]->Fill(pt, fabs(rescaled_dxydszcov_mu_e), w);
        // h_mutracks_absdxydszcov_v_pt_f[i]->Fill(pt, fabs(rescaled_dxydszcov_mu_f), w);

        // h_mutracks_absdxydszcov_v_eta[i]->Fill(ntm.eta(im), fabs(rescaled_dxydszcov_mu), w);
        // h_mutracks_absdxydszcov_v_phi[i]->Fill(ntm.phi(im), fabs(rescaled_dxydszcov_mu), w);
        // h_mutracks_eta_v_phi[i]->Fill(ntm.phi(im), ntm.eta(im), w);
      }
    }

    for (int itk = 0, itke = ntt.n(); itk < itke; ++itk) {
      const double pt = ntt.pt(itk);
      const int min_r = ntt.min_r(itk);
      //const int losthits = ntt.losthit(itk); //not in the ntuple :(
      const int npxlayers = ntt.npxlayers(itk);
      const int nstlayers = ntt.nstlayers(itk);
      const double dxybs = ntt.dxybs(itk, nt.bs());
      //const double nsigmadxy = ntt.nsigmadxybs(itk, nt.bs());
      
      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;
      const bool etagt1p5 = true;
      bool etarange =false;
      if (etagt1p5)
        etarange = fabs(ntt.eta(itk)) > 1.5;
      else
        etarange = fabs(ntt.eta(itk)) < 1.5;
      //const bool etagt1p5 = fabs(ntt.eta(itk)) > 1.5;
      //const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;


      double rescaled_dxyerr = ntt.err_dxy(itk);
      double rescaled_dszerr = ntt.err_dsz(itk);
      double rescaled_dxydszcov = ntt.cov_34(itk);
      
      // double rescaled_dxyerr_bc = ntt.err_dxy(itk);
      // double rescaled_dszerr_bc = ntt.err_dsz(itk);
      // double rescaled_dxydszcov_bc = ntt.cov_34(itk);

      // double rescaled_dxyerr_def = ntt.err_dxy(itk);
      // double rescaled_dszerr_def = ntt.err_dsz(itk);
      // double rescaled_dxydszcov_def = ntt.cov_34(itk);

      // double rescaled_dxyerr_d = ntt.err_dxy(itk);
      // double rescaled_dszerr_d = ntt.err_dsz(itk);
      // double rescaled_dxydszcov_d = ntt.cov_34(itk);

      // double rescaled_dxyerr_e = ntt.err_dxy(itk);
      // double rescaled_dszerr_e = ntt.err_dsz(itk);
      // double rescaled_dxydszcov_e = ntt.cov_34(itk);

      // double rescaled_dxyerr_f = ntt.err_dxy(itk);
      // double rescaled_dszerr_f = ntt.err_dsz(itk);
      // double rescaled_dxydszcov_f = ntt.cov_34(itk);

      const bool rescale_tracks = true;
      if (rescale_tracks) {

        double dxyerr_scale = 1.;
        double dszerr_scale = 1.;

        // double dxyerr_scale_bc = 1.;
        // double dszerr_scale_bc = 1.;

        // double dxyerr_scale_def = 1.;
        // double dszerr_scale_def = 1.;

        // double dxyerr_scale_d = 1.;
        // double dszerr_scale_d = 1.;

        // double dxyerr_scale_e = 1.;
        // double dszerr_scale_e = 1.;

        // double dxyerr_scale_f = 1.;
        // double dszerr_scale_f = 1.;
	
        if (fabs(ntt.eta(itk)) < 1.5) {
          const double x = pt;

         //2016
          const double p_dxy[7] = {0.9920010571552422, -0.005944506409745561, 0.0006862176797598997, 0.9876253292452375, -0.0009684217020550416, 0.9559174361550364, -0.00031899089857540495};
          const double p_dsz[5] = {0.9911385693983847, -0.006446225309624326, 0.0004882812680430705, 0.9726596696027426, -0.0002374674568048638}; 

          dxyerr_scale = (x<=6)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>=6&&x<=60)*(p_dxy[3]+p_dxy[4]*x)+(x>=60&&x<=200)*(p_dxy[5]+p_dxy[6]*x);
          dszerr_scale = (x<=8)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>=8&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        

          //2016APVBC
          // const double p_dxy_bc[5] = {0.9638261039563735, -0.03207712440971401, 0.0024671875339926687, 0.8645380430245057, -0.0007722240737755249};
          // const double p_dsz_bc[5] = {0.9522541199642603, -0.02708900196942797, 0.0019008442417165657, 0.8529663941762214, -0.00015063163556874783}; 

          // dxyerr_scale_bc = (x<=8)*(p_dxy_bc[0]+p_dxy_bc[1]*x+p_dxy_bc[2]*pow(x,2))+(x>=8&&x<=200)*(p_dxy_bc[3]+p_dxy_bc[4]*x);
          // dszerr_scale_bc = (x<=8)*(p_dsz_bc[0]+p_dsz_bc[1]*x+p_dsz_bc[2]*pow(x,2))+(x>=8&&x<=200)*(p_dsz_bc[3]+p_dsz_bc[4]*x);

          // //2016APVDEF
          // const double p_dxy_def[5] = {0.9769462281451897, -0.018874363410992162, 0.0016436714447148268, 0.93073463585661, -0.0005236542947519192};
          // const double p_dsz_def[5] = {0.9770996646685013, -0.014030111631950407, 0.0011083275145709788, 0.9356517118853516, -0.00022382292795847247}; 

          // dxyerr_scale_def = (x<=8)*(p_dxy_def[0]+p_dxy_def[1]*x+p_dxy_def[2]*pow(x,2))+(x>=8&&x<=200)*(p_dxy_def[3]+p_dxy_def[4]*x);
          // dszerr_scale_def = (x<=8)*(p_dsz_def[0]+p_dsz_def[1]*x+p_dsz_def[2]*pow(x,2))+(x>=8&&x<=200)*(p_dsz_def[3]+p_dsz_def[4]*x);

         //2017
          // const double p_dxy[5] = {1.0453960904585817, 0.041436021674833345, -0.0030425974096880935, 1.1883776026039348, -0.00013379699881263247};
          // const double p_dsz[5] = {1.1008989957407143, 0.03282237489872372, -0.003328727663590235, 1.1915963669237948, -0.00023558778443134518}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy[3]+p_dxy[4]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz[3]+p_dsz[4]*x);
        
          // //2017B
          // const double p_dxy_b[7] = {1.0454721390457333, 0.04048079999971112, -0.0023706040731047897, 1.2024041869995274, 0.000606034081486006, 1.2288316843468494, -7.350552496262e-06};
          // const double p_dsz_b[7] = {1.1271052415348382, 0.04083444981809002, -0.005074780163856769, 1.211121713287746, -0.001666029758976395, 1.1864441472534977, -0.00038567217636110724}; 

          // dxyerr_scale_b = (x<=5)*(p_dxy_b[0]+p_dxy_b[1]*x+p_dxy_b[2]*pow(x,2))+(x>5&&x<=40)*(p_dxy_b[3]+p_dxy_b[4]*x)+(x>40&&x<=200)*(p_dxy_b[5]+p_dxy_b[6]*x);
          // dszerr_scale_b = (x<=5)*(p_dsz_b[0]+p_dsz_b[1]*x+p_dsz_b[2]*pow(x,2))+(x>5&&x<=20)*(p_dsz_b[3]+p_dsz_b[4]*x)+(x>20&&x<=200)*(p_dsz_b[5]+p_dsz_b[6]*x);
        
          // //2017C
          // const double p_dxy_c[5] = {1.059641097516078, 0.05355230462527581, -0.004035569142998144, 1.2346564744807427, 3.673845265084457e-05};
          // const double p_dsz_c[5] = {1.199650922965201, 0.04880983957744797, -0.005899743231336449, 1.2958603495433494, -0.00048345549540422484};

          // dxyerr_scale_c = (x<=5)*(p_dxy_c[0]+p_dxy_c[1]*x+p_dxy_c[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy_c[3]+p_dxy_c[4]*x);
          // dszerr_scale_c = (x<=5)*(p_dsz_c[0]+p_dsz_c[1]*x+p_dsz_c[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz_c[3]+p_dsz_c[4]*x);
        
          // //2017D
          // const double p_dxy_d[5] = {1.0449405218573586, 0.04041741588818197, -0.0025603214474102624, 1.1971022964095115, -0.00028263101684195414};
          // const double p_dsz_d[5] = {1.1089086467990208, 0.03678472258881693, -0.0033503695907639366, 1.2213126797049578, -0.00010802017674114636};

          // dxyerr_scale_d = (x<=5)*(p_dxy_d[0]+p_dxy_d[1]*x+p_dxy_d[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy_d[3]+p_dxy_d[4]*x);
          // dszerr_scale_d = (x<=5)*(p_dsz_d[0]+p_dsz_d[1]*x+p_dsz_d[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz_d[3]+p_dsz_d[4]*x);
        
          // //2017E
          // const double p_dxy_e[7] = {1.024456260022345, 0.03357290572238218, -0.002853085601525066, 1.1301634498138307, -0.0009172528240628981, 1.1086034672954395, -0.0003052307678100865};
          // const double p_dsz_e[5] = {1.0539479693172455, 0.024948102307090936, -0.0026628860730077766, 1.115610334169528, -0.0002426913095787955}; 

          // dxyerr_scale_e = (x<=5)*(p_dxy_e[0]+p_dxy_e[1]*x+p_dxy_e[2]*pow(x,2))+(x>5&&x<=25)*(p_dxy_e[3]+p_dxy_e[4]*x)+(x>25&&x<=200)*(p_dxy_e[5]+p_dxy_e[6]*x);
          // dszerr_scale_e = (x<=5)*(p_dsz_e[0]+p_dsz_e[1]*x+p_dsz_e[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz_e[3]+p_dsz_e[4]*x);
        
          // //2017F
          // const double p_dxy_f[5] = {1.0521800742264282, 0.042638428622545785, -0.0033362880473435386, 1.1950279499876233, -0.0002628719466817895};
          // const double p_dsz_f[5] = {1.0719324285711365, 0.02890067353886633, -0.0027571650289382604, 1.15849047538341, -0.0003003783473219247}; 

          // dxyerr_scale_f = (x<=5)*(p_dxy_f[0]+p_dxy_f[1]*x+p_dxy_f[2]*pow(x,2))+(x>5&&x<=200)*(p_dxy_f[3]+p_dxy_f[4]*x);
          // dszerr_scale_f = (x<=5)*(p_dsz_f[0]+p_dsz_f[1]*x+p_dsz_f[2]*pow(x,2))+(x>5&&x<=200)*(p_dsz_f[3]+p_dsz_f[4]*x);
               

          //2018 
          // const double p_dxy[7] = {1.0307879244737679, 0.02831224611434404, -0.002566477993127616, 1.1197395058047317, -0.0013395031657799897, 1.0601176129915633, 3.2335356027768554e-05};
          // const double p_dsz[7] = {1.0793278836243028, 0.013400766926921178, 1.1342091516723427, -0.0015617017338048402, 1.1189296752326552, -0.00012881652276937328, 3.173199768700976e-07}; 

          // dxyerr_scale = (x<=6)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>=6&&x<=44)*(p_dxy[3]+p_dxy[4]*x)+(x>=44&&x<=200)*(p_dxy[5]+p_dxy[6]*x);
          // dszerr_scale = (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>=4&&x<=10)*(p_dsz[2]+p_dsz[3]*x)+(x>=10&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2));
        
      	}
      	else {
      	  const double x = pt;

         //2016
          const double p_dxy[5] = {1.0077751732491917, -0.0040199053132503465, 0.00018603976241413425, 0.9804330274837163, 6.622691103824047e-05};
          const double p_dsz[5] = {1.010326413875115, -0.003003972166731244, 0.0001402087968604259, 0.9901258769433297, -0.00013487635392253963}; 

          dxyerr_scale = (x<=10)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>=10&&x<=200)*(p_dxy[3]+p_dxy[4]*x);
          dszerr_scale = (x<=14)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>=14&&x<=200)*(p_dsz[3]+p_dsz[4]*x);

          //2016APVBC
          // const double p_dxy_bc[5] = {0.9996386582630118, -0.02211930775182362, 0.0007264377953517782, 0.8509561374482384, -0.00029320578886723233};
          // const double p_dsz_bc[5] = {0.9938398377528611, -0.02099697176666402, 0.0005581650363945105, 0.786296897570581, -0.00018734851924174806}; 

          // dxyerr_scale_bc = (x<=20)*(p_dxy_bc[0]+p_dxy_bc[1]*x+p_dxy_bc[2]*pow(x,2))+(x>=20&&x<=200)*(p_dxy_bc[3]+p_dxy_bc[4]*x);
          // dszerr_scale_bc = (x<=20)*(p_dsz_bc[0]+p_dsz_bc[1]*x+p_dsz_bc[2]*pow(x,2))+(x>=20&&x<=200)*(p_dsz_bc[3]+p_dsz_bc[4]*x);

          // //2016APVDEF
          // const double p_dxy_def[5] = {1.0011983597544034, -0.015067841182373422, 0.0004431641246189639, 0.8895968202933113, -0.00021494323194744713};
          // const double p_dsz_def[5] = {1.0033837066216909, -0.007209658942561467, 0.00019396722537742134, 0.9560555071185404, -0.0005950973571676767}; 

          // dxyerr_scale_def = (x<=14)*(p_dxy_def[0]+p_dxy_def[1]*x+p_dxy_def[2]*pow(x,2))+(x>=14&&x<=200)*(p_dxy_def[3]+p_dxy_def[4]*x);
          // dszerr_scale_def = (x<=12)*(p_dsz_def[0]+p_dsz_def[1]*x+p_dsz_def[2]*pow(x,2))+(x>=12&&x<=200)*(p_dsz_def[3]+p_dsz_def[4]*x);

          // 2017
          // const double p_dxy[8] = {1.0217747615840058, 0.023570590309057164, 0.002789159027117587, 0.9874674319767205, 0.05745438503821816, -0.002749291783217478, 1.298759653093006, -0.0008753297754001446};
          // const double p_dsz[8] = {1.0214058461404374, 0.015047155896088559, 0.001845956869518867, 1.0521672124861052, 0.02373261232484642, -0.000837539361598165, 1.228084151474264, -0.0001989524621785918}; 

          // dxyerr_scale = (x<=5)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy[3]+p_dxy[4]*x+p_dxy[5]*pow(x,2))+(x>12&&x<=200)*(p_dxy[6]+p_dxy[7]*x);
          // dszerr_scale = (x<=5)*(p_dsz[0]+p_dsz[1]*x+p_dsz[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz[3]+p_dsz[4]*x+p_dsz[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz[6]+p_dsz[7]*x);

          // //2017B
          // const double p_dxy_b[10] = {1.0239780292649785, 0.02520490281611497, 0.002698615774764072, 1.0010044623638974, 0.057398368065915695, -0.002938305190546185, 0.0, 0.0, 1.2900894090755863, -0.0005510384458186383};
          // const double p_dsz_b[8] = {1.0132032528242354, 0.007225698614186541, 0.0015057608149426356, 1.0358552524840738, 0.014251842128965374, -0.0005818359396350325, 1.1246478047610629, -0.00020026750523001097}; 

          // dxyerr_scale_b = (x<=5)*(p_dxy_b[0]+p_dxy_b[1]*x+p_dxy_b[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy_b[3]+p_dxy_b[4]*x+p_dxy_b[5]*pow(x,2))+(x>12&&x<=200)*(p_dxy_b[8]+p_dxy_b[9]*x);
          // dszerr_scale_b = (x<=5)*(p_dsz_b[0]+p_dsz_b[1]*x+p_dsz_b[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz_b[3]+p_dsz_b[4]*x+p_dsz_b[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz_b[6]+p_dsz_b[7]*x);
        
          // //2017C
          // const double p_dxy_c[10] = {1.0270365089480384, 0.036437408283363226, 0.0020643417672699567, 1.0398578225369, 0.059259570546125254, -0.0031268235714700526, 0.0, 0.0, 1.3296690181377513, -0.0008625899926714985};
          // const double p_dsz_c[8] = {1.0268428362785673, 0.026047828262683724, 0.0017275790789553552, 1.1117744843672137, 0.024829651511513832, -0.0009580303190045584, 1.2817959787570397, -3.371302578978346e-05}; 

          // dxyerr_scale_c = (x<=5)*(p_dxy_c[0]+p_dxy_c[1]*x+p_dxy_c[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy_c[3]+p_dxy_c[4]*x+p_dxy_c[5]*pow(x,2))+(x>12&&x<=200)*(p_dxy_c[8]+p_dxy_c[9]*x);
          // dszerr_scale_c = (x<=5)*(p_dsz_c[0]+p_dsz_c[1]*x+p_dsz_c[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz_c[3]+p_dsz_c[4]*x+p_dsz_c[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz_c[6]+p_dsz_c[7]*x);
        
          // //2017D
          // const double p_dxy_d[10] = {1.0219438794566025, 0.026915685631381372, 0.0022335028609826724, 0.9954869879310493, 0.056842566243907676, -0.0029750538436284675, 0.0, 0.0, 1.2754620746926133, -0.0003289445003313669};
          // const double p_dsz_d[8] = {1.0122876954294187, 0.007755005515062908, 0.001780973568782762, 1.028542830166449, 0.01766846023529924, -0.0006495303614798221, 1.1538833043934955, 0.00040189814315956106}; 

          // dxyerr_scale_d = (x<=5)*(p_dxy_d[0]+p_dxy_d[1]*x+p_dxy_d[2]*pow(x,2))+(x>5&&x<=10)*(p_dxy_d[3]+p_dxy_d[4]*x+p_dxy_d[5]*pow(x,2))+(x>10&&x<=200)*(p_dxy_d[8]+p_dxy_d[9]*x);
          // dszerr_scale_d = (x<=5)*(p_dsz_d[0]+p_dsz_d[1]*x+p_dsz_d[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz_d[3]+p_dsz_d[4]*x+p_dsz_d[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz_d[6]+p_dsz_d[7]*x);
        
          // //2017E
          // const double p_dxy_e[8] = {1.0129765341939894, 0.017302524056451205, 0.0026499263438049207, 0.9477673201378223, 0.055084596444820104, -0.0026104793767137806, 1.244405850968552, -0.0007201352642008863};
          // const double p_dsz_e[8] = {1.0003535275162123, 0.0017113195719508437, 0.0009308643480153405, 1.0237191007765691, 0.0028565033937254097, 0.0, 1.0587568081049843, -5.675189932928624e-05}; 

          // dxyerr_scale_e = (x<=5)*(p_dxy_e[0]+p_dxy_e[1]*x+p_dxy_e[2]*pow(x,2))+(x>5&&x<=12)*(p_dxy_e[3]+p_dxy_e[4]*x+p_dxy_e[5]*pow(x,2))+(x>12&&x<=200)*(p_dxy_e[6]+p_dxy_e[7]*x);
          // dszerr_scale_e = (x<=5)*(p_dsz_e[0]+p_dsz_e[1]*x+p_dsz_e[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz_e[3]+p_dsz_e[4]*x)+(x>15&&x<=200)*(p_dsz_e[6]+p_dsz_e[7]*x);
        
          // //2017F
          // const double p_dxy_f[8] = {1.0239578682773562, 0.020505563506426454, 0.003170821519810303, 0.9745878678436475, 0.05780680166988454, -0.002414751853242754, 1.3283592559754283, -0.001294895979264268};
          // const double p_dsz_f[8] = {1.0384487238505822, 0.022697906577648048, 0.0027238596661408442, 1.0625030826368036, 0.03950087814002015, -0.0012460176657615963, 1.383324296318175, -0.0006565063011642451}; 

          // dxyerr_scale_f = (x<=5)*(p_dxy_f[0]+p_dxy_f[1]*x+p_dxy_f[2]*pow(x,2))+(x>5&&x<=11)*(p_dxy_f[3]+p_dxy_f[4]*x+p_dxy_f[5]*pow(x,2))+(x>11&&x<=200)*(p_dxy_f[6]+p_dxy_f[7]*x);
          // dszerr_scale_f = (x<=5)*(p_dsz_f[0]+p_dsz_f[1]*x+p_dsz_f[2]*pow(x,2))+(x>5&&x<=15)*(p_dsz_f[3]+p_dsz_f[4]*x+p_dsz_f[5]*pow(x,2))+(x>15&&x<=200)*(p_dsz_f[6]+p_dsz_f[7]*x);
               
          //2018
          // const double p_dxy[7] = {1.0133058333787446, 0.022237901720880488, 1.0300940621785346, 0.025700051126257423, -0.0009389967377608525, 1.2050708579976674, -0.0007234028841973103};
          // const double p_dsz[7] = {1.012081399924215, 0.007107936726156522, 1.0136309711992073, 0.0092351886738921, -0.00038672172482552905, 1.077356753286646, -0.00018092724629019752}; 

          // dxyerr_scale = (x<=4)*(p_dxy[0]+p_dxy[1]*x)+(x>=4&&x<=15)*(p_dxy[2]+p_dxy[3]*x+p_dxy[4]*pow(x,2))+(x>=15&&x<=200)*(p_dxy[5]+p_dxy[6]*x);
          // dszerr_scale = (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>=4&&x<=15)*(p_dsz[2]+p_dsz[3]*x+p_dsz[4]*pow(x,2))+(x>=15&&x<=200)*(p_dsz[5]+p_dsz[6]*x);
        }
        
        rescaled_dxyerr *= dxyerr_scale;
        rescaled_dxydszcov *= sqrt(dxyerr_scale);
        rescaled_dszerr *= dszerr_scale;
        rescaled_dxydszcov *= sqrt(dszerr_scale);

        // rescaled_dxyerr_bc *= dxyerr_scale_bc;
        // rescaled_dxydszcov_bc *= sqrt(dxyerr_scale_bc);
        // rescaled_dszerr_bc *= dszerr_scale_bc;
        // rescaled_dxydszcov_bc *= sqrt(dszerr_scale_bc);

        // rescaled_dxyerr_def *= dxyerr_scale_def;
        // rescaled_dxydszcov_def *= sqrt(dxyerr_scale_def);
        // rescaled_dszerr_def *= dszerr_scale_def;
        // rescaled_dxydszcov_def *= sqrt(dszerr_scale_def);

        // rescaled_dxyerr_d *= dxyerr_scale_d;
        // rescaled_dxydszcov_d *= sqrt(dxyerr_scale_d);
        // rescaled_dszerr_d *= dszerr_scale_d;
        // rescaled_dxydszcov_d *= sqrt(dszerr_scale_d);

        // rescaled_dxyerr_e *= dxyerr_scale_e;
        // rescaled_dxydszcov_e *= sqrt(dxyerr_scale_e);
        // rescaled_dszerr_e *= dszerr_scale_e;
        // rescaled_dxydszcov_e *= sqrt(dszerr_scale_e);

        // rescaled_dxyerr_f *= dxyerr_scale_f;
        // rescaled_dxydszcov_f *= sqrt(dxyerr_scale_f);
        // rescaled_dszerr_f *= dszerr_scale_f;
        // rescaled_dxydszcov_f *= sqrt(dszerr_scale_f);
      }
      const double nsigmadxy = dxybs / rescaled_dxyerr;


      const bool nm1[5] = {
	      pt > 1,
        // min_r <= 1 || (min_r == 2 && losthits == 0),
        min_r <= 1,
	      npxlayers >= 2,
	      nstlayers >= 6,
	      nsigmadxy > 4
	
      };

      const bool etalt1p5 = fabs(ntt.eta(itk)) < 1.5;
      const bool etagt1p5 = !etalt1p5;
      const bool sel = nm1[0] && nm1[1] && nm1[2] && nm1[3];
      // const bool seed = sel && nm1[4];

      // const bool tk_ok[max_tk_type] = { true, sel, seed };
      const bool tk_ok[max_tk_type] = {sel};

      //const bool high_purity = npxlayers == 4 && fabs(ntt.eta(itk)) < 0.8 && fabs(ntt.dz(itk)) < 10;

      for (int i = 0; i < max_tk_type; ++i) {
	      if (!tk_ok[i] || !etarange) continue;
        ++ntracks[i];

      // JMTBAD separate plots for dxy, dxybs, dxypv, dz, dzpv
        // h_tracks_pt[i]->Fill(pt, w);
        // h_tracks_eta[i]->Fill(ntt.eta(itk), w);
        // h_tracks_phi[i]->Fill(ntt.phi(itk), w);
        // h_tracks_dxy[i]->Fill(dxybs, w);
        // //	h_tracks_absdxy[i]->Fill(fabs(dxybs), w);
        // h_tracks_dsz[i]->Fill(ntt.dsz(itk), w);
        // h_tracks_dz[i]->Fill(ntt.dz(itk), w);

        // h_tracks_dzpv[i]->Fill(ntt.dzpv(itk, nt.pvs()), w);
        // h_tracks_nhits[i]->Fill(ntt.nhits(itk), w);
        // h_tracks_npxhits[i]->Fill(ntt.npxhits(itk), w);
        // h_tracks_nsthits[i]->Fill(ntt.nsthits(itk), w);
        // h_tracks_min_r[i]->Fill(min_r, w);
        // h_tracks_npxlayers[i]->Fill(npxlayers, w);
        // h_tracks_nstlayers[i]->Fill(nstlayers, w);
        //h_tracks_absnsigmadxy[i]->Fill(nsigmadxy, w);
        //h_tracks_nsigmadxy[i]->Fill(dxybs / ntt.err_dxy(itk), w);
        //	h_tracks_nsigmadsz[i]->Fill(ntt.dsz(itk) / ntt.err_dsz(itk), w);

        //h_tracks_dxyerr[i]->Fill(ntt.err_dxy(itk), w);
        //	h_tracks_dxydszcov[i]->Fill(ntt.cov_34(itk), w);
        //	h_tracks_absdxydszcov[i]->Fill(fabs(ntt.cov_34(itk)), w);
        //h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
       // h_tracks_dszerr[i]->Fill(ntt.err_dsz(itk), w);
        //	h_tracks_lambdaerr[i]->Fill(ntt.err_lambda(itk), w);
        //h_tracks_pterr[i]->Fill(ntt.err_pt(itk), w);
        //h_tracks_phierr[i]->Fill(ntt.err_phi(itk), w);
        //h_tracks_etaerr[i]->Fill(ntt.err_eta(itk), w);
        // h_tracks_absnsigmadxy[i]->Fill(nsigmadxy, w);
        // h_tracks_nsigmadxy[i]->Fill(dxybs / rescaled_dxyerr, w);
        // h_tracks_nsigmadsz[i]->Fill(ntt.dsz(itk) / rescaled_dszerr, w);
        
        // h_tracks_dxyerr[i]->Fill(rescaled_dxyerr, w);
        // h_tracks_dxydszcov[i]->Fill(rescaled_dxydszcov, w);
        // h_tracks_absdxydszcov[i]->Fill(fabs(rescaled_dxydszcov), w);
        // h_tracks_dzerr[i]->Fill(ntt.err_dz(itk), w);
        // h_tracks_dszerr[i]->Fill(rescaled_dszerr, w);
        // h_tracks_lambdaerr[i]->Fill(ntt.err_lambda(itk), w);
        // h_tracks_pterr[i]->Fill(ntt.err_pt(itk), w);
        // h_tracks_phierr[i]->Fill(ntt.err_phi(itk), w);
        // h_tracks_etaerr[i]->Fill(ntt.err_eta(itk), w);


        // h_tracks_nstlayers_v_eta[i]->Fill(ntt.eta(itk), nstlayers, w);
        // h_tracks_dxy_v_eta[i]->Fill(ntt.eta(itk), dxybs, w);
        // h_tracks_dxy_v_phi[i]->Fill(ntt.phi(itk), dxybs, w);
        // h_tracks_dxy_v_nstlayers[i]->Fill(nstlayers, dxybs, w);
        // h_tracks_nstlayers_v_phi[i]->Fill(ntt.phi(itk), nstlayers, w);
        // h_tracks_npxlayers_v_phi[i]->Fill(ntt.phi(itk), npxlayers, w);
        // h_tracks_nhits_v_phi[i]->Fill(ntt.phi(itk), ntt.nhits(itk), w);
        // h_tracks_npxhits_v_phi[i]->Fill(ntt.phi(itk), ntt.npxhits(itk), w);
        // h_tracks_nsthits_v_phi[i]->Fill(ntt.phi(itk), ntt.nsthits(itk), w);

        // h_tracks_nsigmadxy_v_eta[i]->Fill(ntt.eta(itk), nsigmadxy, w);
        // h_tracks_nsigmadxy_v_nstlayers[i]->Fill(nstlayers, nsigmadxy, w);
        // h_tracks_nsigmadxy_v_dxy[i]->Fill(dxybs, nsigmadxy, w);
        // h_tracks_nsigmadxy_v_dxyerr[i]->Fill(ntt.err_dxy(itk), nsigmadxy, w);

        //h_tracks_dxyerr_v_pt[i]->Fill(pt, ntt.err_dxy(itk), w);
        //h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dxy(itk), w);
        //h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_dxy[i]->Fill(dxybs, ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_dzpv[i]->Fill(ntt.dzpv(itk, nt.pvs()), ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dxy(itk), w);
        // h_tracks_dxyerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dxy(itk), w);

        //h_tracks_dszerr_v_pt[i]->Fill(pt, ntt.err_dsz(itk), w);
        //h_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_dsz(itk), w);
        //h_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_dxy[i]->Fill(dxybs, ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_dsz(itk), w);
        // h_tracks_dszerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_dsz(itk), w);

        h_tracks_dxyerr_v_pt[i]->Fill(pt, rescaled_dxyerr, w);
        // h_tracks_dxyerr_v_pt_bc[i]->Fill(pt, rescaled_dxyerr_bc, w);
        // h_tracks_dxyerr_v_pt_def[i]->Fill(pt, rescaled_dxyerr_def, w);
        // h_tracks_dxyerr_v_pt_d[i]->Fill(pt, rescaled_dxyerr_d, w);
        // h_tracks_dxyerr_v_pt_e[i]->Fill(pt, rescaled_dxyerr_e, w);
        // h_tracks_dxyerr_v_pt_f[i]->Fill(pt, rescaled_dxyerr_f, w);

        // h_tracks_dxyerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dxyerr, w);
        // h_tracks_dxyerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dxyerr, w);
        // h_tracks_dxyerr_v_minr[i]->Fill(ntt.min_r(itk), rescaled_dxyerr, w);

        h_tracks_dszerr_v_pt[i]->Fill(pt, rescaled_dszerr, w);
        // h_tracks_dszerr_v_pt_bc[i]->Fill(pt, rescaled_dszerr_bc, w);
        // h_tracks_dszerr_v_pt_def[i]->Fill(pt, rescaled_dszerr_def, w);
        // h_tracks_dszerr_v_pt_d[i]->Fill(pt, rescaled_dszerr_d, w);
        // h_tracks_dszerr_v_pt_e[i]->Fill(pt, rescaled_dszerr_e, w);
        // h_tracks_dszerr_v_pt_f[i]->Fill(pt, rescaled_dszerr_f, w);

        // h_tracks_dszerr_v_eta[i]->Fill(ntt.eta(itk), rescaled_dszerr, w);
        // h_tracks_dszerr_v_phi[i]->Fill(ntt.phi(itk), rescaled_dszerr, w);
        
        // h_tracks_dxydszcov_v_pt[i]->Fill(pt, rescaled_dxydszcov, w);
        // h_tracks_dxydszcov_v_eta[i]->Fill(ntt.eta(itk), rescaled_dxydszcov, w);
        // h_tracks_dxydszcov_v_phi[i]->Fill(ntt.phi(itk), rescaled_dxydszcov, w);

        h_tracks_absdxydszcov_v_pt[i]->Fill(pt, fabs(rescaled_dxydszcov), w);
        // h_tracks_absdxydszcov_v_pt_bc[i]->Fill(pt, fabs(rescaled_dxydszcov_bc), w);
        // h_tracks_absdxydszcov_v_pt_def[i]->Fill(pt, fabs(rescaled_dxydszcov_def), w);
        // h_tracks_absdxydszcov_v_pt_d[i]->Fill(pt, fabs(rescaled_dxydszcov_d), w);
        // h_tracks_absdxydszcov_v_pt_e[i]->Fill(pt, fabs(rescaled_dxydszcov_e), w);
        // h_tracks_absdxydszcov_v_pt_f[i]->Fill(pt, fabs(rescaled_dxydszcov_f), w);

        // h_tracks_absdxydszcov_v_eta[i]->Fill(ntt.eta(itk), fabs(rescaled_dxydszcov), w);
        // h_tracks_absdxydszcov_v_phi[i]->Fill(ntt.phi(itk), fabs(rescaled_dxydszcov), w);

        // h_tracks_lambdaerr_v_pt[i]->Fill(pt, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_eta[i]->Fill(ntt.eta(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_phi[i]->Fill(ntt.phi(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_dxy[i]->Fill(dxybs, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_dz[i]->Fill(ntt.dz(itk), ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_npxlayers[i]->Fill(npxlayers, ntt.err_lambda(itk), w);
        // h_tracks_lambdaerr_v_nstlayers[i]->Fill(nstlayers, ntt.err_lambda(itk), w);

        //h_tracks_eta_v_phi[i]->Fill(ntt.phi(itk), ntt.eta(itk), w);
      }
    }
    for (int i = 0; i < max_tk_type; ++i) {
      h_ntracks[i]->Fill(ntracks[i], w);
    }
    return std::make_pair(true, w);
  };

  nr.loop(fcn);
}
