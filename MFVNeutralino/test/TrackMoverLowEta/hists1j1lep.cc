#include "BTagSFHelper.h"
#include "utils.h"
#include <string>
#include <iostream>
#include "TRandom3.h"

//this to be used when moving only 1 jet (and 1 lepton) to a SV instead of 2 jets 
double ntks_weight(int i) {
  const int N = 60;
  if (i < 0 || i >= N) return 0;
  // from h_2_vtxntracks so only apply there?
  const double ws[N] = { 0., 0., 0., 0., 0., 0., 1.674196, 1.550810, 1.459271, 1.284317, 1.187709, 1.231090, 1.242313, 1.145012, 1.182134, 1.114840, 1.093479, 0.964026, 1.039401, 0.940219, 0.907171, 0.976593, 0.918716, 0.904142, 0.867394, 0.777177, 0.814517, 0.799371, 0.829022, 0.834422, 0.609130, 0.599720, 0.726436, 0.570779, 0.677044, 0.590878, 0.540080, 0.490107, 0.561173, 0.464503, 0.537223, 0.414802, 0.426949, 0.173858, 0.267836, 0.725926, 0.237331, 0.201321, 0.121923, 0.311854, 0.193843, 0.995309, 0., 0., 0., 0.559031, 0.810189, 0., 0., 0. };
  return ws[i];
}

int main(int argc, char** argv) {
  bool btagsf_weights = false;
  bool ntks_weights = false;
  bool jet_decay_weights = false;
  bool jetlep_kin_weights = false;
  std::string w_fn_2d_move = "reweight2Dmove.root";
  std::string w_fn_2d_kin = "reweight2Dkin.root";
  // std::string w_fn_2d_ang = "reweight2Dang.root";
  std::string w_fn_1d_kin = "reweight1Dkin.root";
  std::string tm = "sim";
  
  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;

  namespace po = boost::program_options;
  nr.init_options("mfvMovedTree101/t", "TrackMoverHistsV27m", "nr_trackmoverv27mv1")
    ("btagsf",        po::value<bool>  (&btagsf_weights)->default_value(false),   "whether to use b-tag SF weights")
    ("ntks-weights",  po::value<bool>  (&ntks_weights)  ->default_value(false),   "whether to use ntracks weights")
    ("jet-decayweights",po::value<bool>  (&jet_decay_weights)->default_value(true),   "whether to use jet decay weights")
    ("w_fn_2d_move",       po::value<std::string>  (&w_fn_2d_move)          ->default_value("reweight2Dmove.root"),  "file name of weights")
    ("w_fn_2d_kin",       po::value<std::string>  (&w_fn_2d_kin)          ->default_value("reweight2Dkin.root"),  "file name of weights")
    // ("w_fn_2d_ang",       po::value<std::string>  (&w_fn_2d_ang)          ->default_value("reweight2Dang.root"),  "file name of weights")
    ("jetlep-kinweights",       po::value<bool> (&jetlep_kin_weights)->default_value(true),  "whether to use jetlep kin weights")
    ("w_fn_1d_kin",       po::value<std::string>  (&w_fn_1d_kin)          ->default_value("reweight1Dkin.root"),  "file name of weights")

    ("tm",       po::value<std::string>  (&tm)          ->default_value("sim"),  "simulation or data")
    ;

  if (!nr.parse_options(argc, argv)) return 1;

  char* w_fn_2d_move_ar = new char [w_fn_2d_move.size()+1];
  strcpy(w_fn_2d_move_ar, w_fn_2d_move.c_str());

  char* w_fn_2d_kin_ar = new char [w_fn_2d_kin.size()+1];
  strcpy(w_fn_2d_kin_ar, w_fn_2d_kin.c_str());

  // char* w_fn_2d_ang_ar = new char [w_fn_2d_ang.size()+1];
  // strcpy(w_fn_2d_ang_ar, w_fn_2d_ang.c_str());

  char* w_fn_1d_kin_ar = new char [w_fn_1d_kin.size()+1];
  strcpy(w_fn_1d_kin_ar, w_fn_1d_kin.c_str());

  char* tm_ar = new char [tm.size()+1];
  strcpy(tm_ar, tm.c_str());
  
  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();	
  auto& muons = nt.muons();
  auto& electrons = nt.electrons();
  auto& pf = nt.pf();
  auto& tks = nt.tracks();
  auto& vs = nt.vertices();

  ////


  std::unique_ptr<BTagSFHelper> btagsfhelper;
  if (btagsf_weights) btagsfhelper.reset(new BTagSFHelper);

  const std::vector<std::string> jet_2d_kin_weights_hists = {
    // "nocuts_llp_sump_jetdr_den",  //FIXME
    // "nocuts_jet0_sump_jetlepdr_den",
    "nocuts_lep1_pT_jetdr_den", 
    // "nocuts_mu1_p_eta_den",
    // "nocuts_ele1_p_eta_den",
    // "nocuts_jet0_sump_lep1_p_den",
    //"nocuts_jet0_sump_qrk0_dxybs_den",
    //"nocuts_jetdr_qrk1_dxybs_den",
    //"nocuts_nmovedseedtks0_jet0_sump_den",
    //"nocuts_nmovedseedtks1_jet1_sump_den",
  };

  const std::vector<std::string> jetlep_1d_kin_weights_hists = {
    // "nocuts_jetmu_dr_den",
    // "nocuts_jetele_dr_den",
    // "nocuts_mu1_p_den",
    // "nocuts_ele1_p_den",
    // "nocuts_jet0_sump_den",
    // "nocuts_elept1_den",
    // "nocuts_mupt1_den",
    "nocuts_pt0_den",
  };
  const std::vector<std::string> jet_2d_move_weights_hists = {
    "nocuts_movedist3_movedist2_den",
  };
  // const std::vector<std::string> jet_2d_ang_weights_hists = {
  //   "nocuts_jetlep_deta_dphi_den",
  // };
  const std::vector<std::string> extra_weights_hists = {
    //"nocuts_npv_den",
    //"nocuts_pvz_den",
    //"nocuts_pvx_den",
    //"nocuts_pvy_den",
    //"nocuts_ntracks_den",
    //"nocuts_npv_den_redo"
    //"nocuts_ht_den",
    //"nocuts_pvntracks_den",
    // "nocuts_jetmu_dr_den",
    // "nocuts_jetele_dr_den",
    // "nocuts_mu1_p_den",
    // "nocuts_ele1_p_den",
    // "nocuts_jet0_sump_den"
  };
  TFile* extra_weights = extra_weights_hists.size() > 0 ? TFile::Open("reweight.root") : 0;

  const bool use_extra_weights = extra_weights != 0 && extra_weights->IsOpen();
  if (use_extra_weights) printf("using extra weights from reweight.root (1D) \n");
  if (jet_decay_weights) std::cout << "using extra weights from " << w_fn_2d_move << " and " << w_fn_2d_kin << std::endl;
  // if (jet_decay_weights) std::cout << "using extra weights from " << w_fn_2d_move << std::endl;
  if (jetlep_kin_weights) std::cout << "using 1D weights " << std::endl;
  TH1D* h_btagsfweight = new TH1D("h_btagsfweight", ";weight;events/0.01", 200, 0, 2);

  const int num_numdens = 3;
  numdens nds[num_numdens] = { // JMTBAD why multiple dens here?
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };
  enum { k_movedist2, k_movedist3, k_movevectoreta, k_npv, k_pvx, k_pvy, k_pvz, k_pvrho, k_pvntracks, k_pvscore, 
         k_ht, k_njets, k_nmuons, k_muon_pT, k_muon_abseta, k_muon_iso, k_muon_zoom_iso, k_muon_absdxybs, k_muon_absdz, 
         k_muon_nsigmadxybs, k_neles, k_ele_pT, k_ele_abseta, k_ele_iso, k_ele_zoom_iso, k_ele_absdxybs, k_ele_absdz, 
         k_ele_nsigmadxybs, k_met_pT, k_w_pT, k_w_mT, k_z_pT, k_z_m, k_lnu_absphi, k_ljet_absdr, k_ljet0_absdr, 
         k_ljet1_absdr, k_nujet0_absphi, k_nujet1_absphi, k_wjet_dphi, k_zjet_dphi, k_w_ntk_j0, k_z_ntk_j0, k_jetmu_asymm, 
         k_jetele_asymm, k_jet0_eta, k_mu1_eta, k_ele1_eta, k_jetmu_dr, k_jetele_dr, k_jetmu_costheta, k_jetmu_deta,
         k_jetmu_dphi, k_jetmu_deta_dphi, k_jetele_costheta, k_jetele_deta, k_jetele_dphi, k_jetele_deta_dphi, k_jetlep_deta_dphi,
         k_pt0, k_mupt1, k_elept1, k_ntks_j0,
         k_jet0_trk_pt, k_mu1_trk_pt, k_ele1_trk_pt, k_jet0_trk_p, k_mu1_p, k_ele1_p, k_jet0_sump, k_mu1_p_eta, k_ele1_p_eta, k_lep1_p_eta,
         k_jet0_maxeta_mu1_eta, k_jet0_sump_mu1_p, k_jet0_maxeta_ele1_eta, k_jet0_sump_ele1_p, k_jet0_sump_lep1_p,
         k_closeseedtks_qrk0_dxybs, k_closeseedtks_mu1_dxybs, k_closeseedtks_ele1_dxybs, k_jetmudr_qrk0_dxybs, k_jeteledr_qrk0_dxybs,
         k_jetdr_mu1_dxybs, k_jetdr_ele1_dxybs, k_jetmudphi_qrk0_dxybs, k_jeteledphi_qrk0_dxybs, k_jetdphi_mu1_dxybs, 
         k_jetdphi_ele1_dxybs, k_nmovedtks_jetmu_dr, k_nmovedtks_jetele_dr, k_nmovedtks0_qrk0_dxybs, k_nmovedseedtks0_qrk0_dxybs, k_nmovedtks0_jet0_sump, 
         k_nmovedseedtks0_jet0_sump, k_nmovedtks_movedist3, k_nmovedseedtks_movedist3, k_llp_sump_mu, k_llp_sump_ele, k_llp_sump_jetmudphi, 
         k_llp_sump_jetmudr, k_llp_sump_jeteledphi, k_llp_sump_jeteledr, k_jet0_sump_movedist3, k_mu1_p_movedist3, k_ele1_p_movedist3, k_jet0_sump_qrk0_dxybs, 
         k_mu1_p_mu1_dxybs, k_ele1_p_ele1_dxybs, k_jet0_sump_jetmudr, k_jet0_sump_jeteledr, k_jet0_sump_jetlepdr, k_mu1_p_jetmudr, k_ele1_p_jeteledr, k_lep1_p_jetlepdr,
         k_mu1_pT_jetmudr, k_ele1_pT_jeteledr, k_lep1_pT_jetlepdr,
         k_2logm_jetmudr, k_2logm_mucostheta, k_2logm_jeteledr, k_2logm_elecostheta, k_mu1_p_jetmu_costheta, k_ele1_p_jetele_costheta,
         k_closeseed_trk_genmissdist, k_closeseed_trk_gendz, k_closeseed_trk_gennsigmadz, k_movedist3_movedist2, 
         k_movedist3_jetmudr, k_movedist3_jeteledr, k_movedist3_tightcloseseedtks, k_jetmu_costheta_tightcloseseedtks, k_jetele_costheta_tightcloseseedtks, 
         k_jetmu_dr_tightcloseseedtks, k_jetele_dr_tightcloseseedtks, k_movedist3_closeseedtks, k_jetmu_costheta_closeseedtks,
         k_jetele_costheta_closeseedtks, k_jetmu_dr_closeseedtks, k_jetele_dr_closeseedtks, k_mu1_p_jetdphi, k_ele1_p_jetdphi,
         k_qrk0_dxybs, k_jet0_dxybs, k_mu1_dxybs, k_ele1_dxybs, k_2sump0pmu1_1mcos, k_2sump0pele1_1mcos,
         k_2logm_mu, k_2logm_ele, 

         k_mu1jet0_trk_dx, k_mu1jet0_trk_dy, k_mu1jet0_trk_dz, k_ele1jet0_trk_dx, k_ele1jet0_trk_dy, k_ele1jet0_trk_dz, 
         k_mu1jet0_trk_dist2d, k_ele1jet0_trk_dist2d, 

         k_jet0_trk_dz, k_mu1_trk_dz, k_ele1_trk_dz,
         k_jet0_trk_vtxdxy, k_mu1_trk_vtxdxy, k_ele1_trk_vtxdxy, k_jet0_trk_vtxdz, k_mu1_trk_vtxdz, k_ele1_trk_vtxdz, 
         k_jet0_trk_nsigmavtxdz, k_mu1_trk_nsigmavtxdz, k_ele1_trk_nsigmavtxdz, k_jet0_trk_nsigmavtxdxy, k_mu1_trk_nsigmavtxdxy,  
         k_ele1_trk_nsigmavtxdxy, k_jet0_trk_nsigmavtx, k_mu1_trk_nsigmavtx, k_ele1_trk_nsigmavtx, k_jet0_trk_dzerr, k_mu1_trk_dzerr, 
         k_ele1_trk_dzerr, k_jet0_trk_dxyerr, k_mu1_trk_dxyerr, k_ele1_trk_dxyerr, k_jet0_trk_eta, k_mu1_trk_eta, k_ele1_trk_eta,
         k_jet0_trk_gennsigma, k_mu1_trk_gennsigma, k_ele1_trk_gennsigma, k_jet0_trk_gennsigmamissdist, k_mu1_trk_gennsigmamissdist,
         k_ele1_trk_gennsigmamissdist, k_jet0_trk_genmissdist, k_mu1_trk_genmissdist, k_ele1_trk_genmissdist,
         k_jet0_trk_gendz, k_mu1_trk_gendz, k_ele1_trk_gendz, k_jet0_trk_gennsigmadz, k_mu1_trk_gennsigmadz, k_ele1_trk_gennsigmadz,
         k_jet0_trk_whichpv, k_mu1_trk_whichpv, k_ele1_trk_whichpv, k_jet0_trk_dsz, k_mu1_trk_dsz, k_ele1_trk_dsz, k_jet0_trk_dxy, k_mu1_trk_dxy, 
         k_ele1_trk_dxy, k_jet0_trk_nsigmadxy, k_mu1_trk_nsigmadxy, k_ele1_trk_nsigmadxy, k_nmovedtracks, k_dphi_sum_jmu_mv, 
         k_deta_sum_jmu_mv, k_dphi_sum_jele_mv, k_deta_sum_jele_mv, k_jetpt0_jmasymm, k_jetpt0_jeasymm, k_mupt1_asymm, k_elept1_asymm, 
         k_jeteta0_jmasymm, k_jeteta0_jeasymm, k_mueta1_asymm, k_eleeta1_asymm, k_jetmudr_asymm, k_jeteledr_asymm, k_nalltracks, 
         k_nseedtracks, k_seedtracks_jetmudr, k_seedtracks_jeteledr,
         k_seedtracks_2logm_mu, k_seedtracks_2logm_ele, k_npreseljets, k_npreselbjets, k_npreselmu, k_npreselele, k_jetmui01, 
         k_jetmup01, k_jetmupt01, k_jetmueta01, k_jetmuphi01, k_jetelei01, k_jetelep01, k_jetelept01, k_jeteleeta01, k_jetelephi01,
          
         k_jetsume, k_jetdrmax, k_jetdravg, k_jetdetamax, k_jetdetaavg, k_jetdphimax, k_jetdphiavg,
         k_jet0_tkdrmax, k_jet0_tkdravg, k_jet_dphi_deta_avg, k_jdphi_nmovedtks, k_jdeta_nmovedtks, k_jdr_nmovedtks, 
         k_jtheta0_nmovedtks, k_jetmumovea3d01, k_jetelemovea3d01, k_jetmovea3d_v_jetp, k_mumovea3d_v_mup, k_elemovea3d_v_elep,
         k_jetmovea3d0_v_movevectoreta, k_mumovea3d1_v_movevectoreta, k_elemovea3d1_v_movevectoreta, k_jeta3dmax, k_angle0, k_muangle1, 
         k_eleangle1, k_dphi_j0_mv, k_dphi_mu1_mv, k_dphi_ele1_mv, k_deta_j0_mv, k_deta_mu1_mv, k_deta_ele1_mv, k_dphi_j0_mv_jdeta, k_jetsumntracks,
         k_jetsumseedtracks, k_miscseedtracks, k_misccloseseedtracks, k_closeseedtks, k_tightcloseseedtks, k_movedseedtks, 
         k_movedseedtks_jetmudr, k_movedseedtks_jeteledr, k_movedvtxseedtks, k_movedcloseseedtks, k_rat_moved_to_closetks, k_rat_moved_to_vtxtks, 
         k_jetntracks_v_jetp, k_nvtx, k_vtxbs2derr, k_vtxbs2derr_avgtkdr, k_vtxbs2derr_jdeta, k_vtxbs2derr_dphi_j0_mv, 
         k_vtxbs2derr_jdr, k_vtxunc, k_vtxunc2d, k_vtxeta, k_vtxz, k_vtxdbv, k_vtx3dbv, k_vtxntk, k_vtxnm1_dbv, k_vtxnm1_ntk, 
         k_vtxnm1_bs2derr, k_vtx4tkchi2, k_vtx4tkdbv, k_vtx4tkzdbv, k_vtx4tkunc, k_vtx5tkchi2, k_vtx5tkdbv, k_vtx5tkzdbv, 
         k_vtx5tkunc, k_vtx6tkchi2, k_vtx6tkdbv, k_vtx6tkzdbv, k_vtx6tkunc};

  for (numdens& nd : nds) {
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 50, 0, 2.5);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 50, 0, 4.0); 
    nd.book(k_movevectoreta, "movevectoreta", ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvx, "pvx", ";PV x (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvy, "pvy", ";PV y (cm);events/1.5 #mum", 200, -0.015, 0.015);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";H_{T} (GeV);events/50 GeV", 20, 0, 1000);
    nd.book(k_njets, "njets", ";# jets;events/1", 20, 0, 20);
    nd.book(k_nmuons, "nmuons", ";# passed offline-sel muons;events/1", 10, 0, 10);
    nd.book(k_muon_pT, "muon_pT", ";muons p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_muon_abseta, "muon_abseta", ";muons |#eta|; arb. units", 70, 0, 3.5);
    nd.book(k_muon_iso, "muon_iso", ";muons iso;events/1", 200, 0, 0.15);
    nd.book(k_muon_zoom_iso, "muon_zoom_iso", ";muons zoomed iso;events/1", 200, 0, 0.15);
    nd.book(k_muon_absdxybs, "muon_absdxybs", ";muons |dxybs| cm; arb. units", 80, 0, 0.2);
    nd.book(k_muon_absdz, "muon_absdz", ";muons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_muon_nsigmadxybs, "muon_nsigmadxybs", ";muons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_neles, "neles", ";# passed offline-sel electrons;events/1", 10, 0, 10);
    nd.book(k_ele_pT, "ele_pT", ";electrons p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_ele_abseta, "ele_abseta", ";electrons |#eta|; arb. units", 70, 0, 3.5);
    nd.book(k_ele_iso, "ele_iso", ";electrons iso;events/1", 200, 0, 0.15);
    nd.book(k_ele_zoom_iso, "ele_zoom_iso", ";electrons zoomed iso;events/1", 200, 0, 0.15);
    nd.book(k_ele_absdxybs, "ele_absdxybs", ";electrons |dxybs| cm; arb. units", 80, 0, 0.2);
    nd.book(k_ele_absdz, "ele_absdz", ";electrons |dz| cm; arb. units", 80, 0, 1.0);
    nd.book(k_ele_nsigmadxybs, "ele_nsigmadxybs", ";electrons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    nd.book(k_met_pT, "met_pT", ";missing p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_pT, "w_pT", ";RECO W boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_w_mT, "w_mT", ";RECO W boson's mass_{T} (GeV);events/1", 50, 0, 150);
    nd.book(k_z_pT, "z_pT", ";RECO Z boson's p_{T} (GeV);events/1", 50, 0, 200);
    nd.book(k_z_m, "z_m", ";RECO Z boson's inv. mass (GeV);events/1", 50, 0, 150);
    nd.book(k_lnu_absphi, "lnu_absphi", ";lepton-#nu |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet_absdr, "ljet_absdr", ";lepton-closest-jet |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet0_absdr, "ljet0_absdr", ";lepton-jet0 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_ljet1_absdr, "ljet1_absdr", ";lepton-jet1 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet0_absphi, "nujet0_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_nujet1_absphi, "nujet1_absphi", ";MET-jet1 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_wjet_dphi, "wjet_dphi", ";W-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_zjet_dphi, "zjet_dphi", ";Z-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    nd.book(k_w_ntk_j0, "w_ntk_j0", ";Ntks in jet0 in single-muon events; arb. units", 25, 0.0, 25);
    nd.book(k_z_ntk_j0, "z_ntk_j0", ";Ntks in jet0 in di-muon events; arb. units", 25, 0.0, 25);

    nd.book(k_jetmu_asymm, "jetmu_asymm", ";jet-mu pT asymmetry A_{J}; arb. units", 50, -1, 1); //check ##
    nd.book(k_jetele_asymm, "jetele_asymm", ";jet-ele pT asymmetry A_{J}; arb. units", 50, -1, 1); //check ##
    nd.book(k_jet0_eta, "jet0_eta", ";jet0's Eta; arb. units", 60, -4, 4);
    nd.book(k_mu1_eta, "mu1_eta", ";mu1's Eta; arb. units", 60, -4, 4); //check ##
    nd.book(k_ele1_eta, "ele1_eta", ";ele1's Eta; arb. units", 60, -4, 4); //check ##
    nd.book(k_mu1_p_eta, "mu1_p_eta", ";mu1's momentum p; mu1's Eta", 100, 0, 500, 60, -4, 4); //check ##
    nd.book(k_ele1_p_eta, "ele1_p_eta", ";ele1's momentum p; ele1's Eta", 100, 0, 500, 60, -4, 4); //check ##
    nd.book(k_lep1_p_eta, "lep1_p_eta", ";lep1's momentum p; lep1's Eta", 100, 0, 500, 60, -4, 4); //check ##

    nd.book(k_jetmu_dr, "jetmu_dr", ";jet-mu #DeltaR; arb. units", 60, 0, 6); //check ##
    nd.book(k_jetele_dr, "jetele_dr", ";jet-ele #DeltaR; arb. units", 60, 0, 6); //check##
    nd.book(k_jetmu_costheta, "jetmu_costheta", ";jet-mu cos(#theta); arb. units", 80, -1, 1); //check##
    nd.book(k_jetmu_deta, "jetmu_deta", ";jet-mu #DeltaEta; arb. units", 70, 0, 7); //check##
    nd.book(k_jetmu_dphi, "jetmu_dphi", ";jet-mu #DeltaPhi; arb. units", 70, -3.5, 3.5); //check##
    nd.book(k_jetmu_deta_dphi, "jetmu_deta_dphi", ";jet-mu #DeltaEta; jet-mu #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##

    nd.book(k_jetele_costheta, "jetele_costheta", ";jet-ele cos(#theta); arb. units", 80, -1, 1); //check##
    nd.book(k_jetele_deta, "jetele_deta", ";jet-ele #DeltaEta; arb. units", 70, 0, 7); //check##
    nd.book(k_jetele_dphi, "jetele_dphi", ";jet-ele #DeltaPhi; arb. units", 70, -3.5, 3.5); //check##
    nd.book(k_jetele_deta_dphi, "jetele_deta_dphi", ";jet-ele #DeltaEta; jet-ele #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##
    nd.book(k_jetlep_deta_dphi, "jetlep_deta_dphi", ";jet-lep #DeltaEta; jet-lep #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##

    nd.book(k_pt0, "pt0", ";RECO jet0 pT [GeV]", 100, 0, 500);
    nd.book(k_mupt1, "mupt1", ";RECO mu1 pT [GeV]", 100, 0, 500);//check ##
    nd.book(k_elept1, "elept1", ";RECO ele1 pT [GeV]", 100, 0, 500); //check##
    nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 25, 0, 25);
    nd.book(k_jet0_trk_pt, "jet0_trk_pt", "; jet0-movedquality-track's pT; arb. units", 45, 0, 15);
    nd.book(k_mu1_trk_pt, "mu1_pt", "; mu1-movedquality-'s pT; arb. units", 50, 0, 100); //check #
    nd.book(k_ele1_trk_pt, "ele1_pt", "; ele1-movedquality-'s pT; arb. units", 50, 0, 100); //check #
    nd.book(k_jet0_trk_p, "jet0_trk_p", "; jet0-movedquality-track's p; arb. units", 45, 0, 15);
    nd.book(k_mu1_p, "mu1_p", "; mu1-movedquality-'s p; arb. units", 100, 0, 500); //check #
    nd.book(k_ele1_p, "ele1_p", "; ele1-movedquality-'s p; arb. units", 100, 0, 500); //check#
    nd.book(k_jet0_sump, "jet0_sump", "; jet0-movedquality-track's sum p; arb. units", 100, 0, 500);
    nd.book(k_jet0_maxeta_mu1_eta, "jet0_maxeta_mu1_eta", "; max(jet0-movedquality-track's Eta); mu1-movedquality's Eta)", 60, -3, 3, 60, -3, 3);  //check#
    nd.book(k_jet0_maxeta_ele1_eta, "jet0_maxeta_ele1_eta", "; max(jet0-movedquality-track's Eta); ele1-movedquality's Eta", 60, -3, 3, 60, -3, 3); //check #
    nd.book(k_jet0_sump_mu1_p, "jet0_sump_mu1_p", "; jet0-movedquality-track's sum p; mu1-movedquality's p", 100, 0, 500, 100, 0, 500); //check#
    nd.book(k_jet0_sump_ele1_p, "jet0_sump_ele1_p", "; jet0-movedquality-track's sum p; ele1-movedquality's sum p", 100, 0, 500, 100, 0, 500); //check#
    nd.book(k_jet0_sump_lep1_p, "jet0_sump_lep1_p", "; jet0-movedquality-track's sum p; lep1-movedquality's p", 100, 0, 500, 100, 0, 500); //check#

    nd.book(k_closeseedtks_qrk0_dxybs, "closeseedtks_qrk0_dxybs", "; # seed tracks close to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_closeseedtks_mu1_dxybs, "closeseedtks_mu1_dxybs", "; # seed tracks close to artificial vtx; mu1's dxybs", 25, 0, 25, 20, 0, 0.2); //check #
    nd.book(k_closeseedtks_ele1_dxybs, "closeseedtks_ele1_dxybs", "; # seed tracks close to artificial vtx; ele1's dxybs", 25, 0, 25, 20, 0, 0.2); //check#
    nd.book(k_jetmudr_qrk0_dxybs, "jetmudr_qrk0_dxybs", "; jet-mu #DeltaR; quark0's dxybs", 60, 0, 6, 20, 0, 0.2); //check #
    nd.book(k_jeteledr_qrk0_dxybs, "jeteledr_qrk0_dxybs", "; jet-ele #DeltaR; quark0's dxybs", 60, 0, 6, 20, 0, 0.2); //check #
    nd.book(k_jetdr_mu1_dxybs, "jetdr_mu1_dxybs", "; jet-mu #DeltaR; mu1's dxybs", 60, 0, 6, 20, 0, 0.2); //check #
    nd.book(k_jetdr_ele1_dxybs, "jetdr_ele1_dxybs", "; jet-ele #DeltaR; ele1's dxybs", 60, 0, 6, 20, 0, 0.2); //check #
    nd.book(k_jetmudphi_qrk0_dxybs, "jetmudphi_qrk0_dxybs", "; jet-mu #DeltaPhi; quark0's dxybs", 70, 0, 7, 20, 0, 0.2); //check  #
    nd.book(k_jeteledphi_qrk0_dxybs, "jeteledphi_qrk0_dxybs", "; je-ele #DeltaPhi; quark0's dxybs", 70, 0, 7, 20, 0, 0.2); //check  #
    nd.book(k_jetdphi_mu1_dxybs, "jetdphi_mu1_dxybs", "; jet-mu #DeltaPhi; mu1's dxybs", 70, 0, 7, 20, 0, 0.2); //check #
    nd.book(k_jetdphi_ele1_dxybs, "jetdphi_ele1_dxybs", "; jet-ele #DeltaPhi; ele1's dxybs", 70, 0, 7, 20, 0, 0.2); //check #
    nd.book(k_nmovedtks_jetmu_dr, "nmovedtks_jetmu_dr", "; # quality tracks associated to artificial vtx; jet-mu #DeltaR", 25, 0, 25, 60, 0, 6.0);//check#
    nd.book(k_nmovedtks_jetele_dr, "nmovedtks_jetele_dr", "; # quality tracks associated to artificial vtx; jet-ele #DeltaR", 25, 0, 25, 60, 0, 6.0);//check#
    nd.book(k_nmovedtks0_qrk0_dxybs, "nmovedtks0_qrk0_dxybs", "; # quality tracks in jet0 associated to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_nmovedseedtks0_qrk0_dxybs, "nmovedseedtks0_qrk0_dxybs", "; # seed tracks in jet0 associated to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_nmovedtks0_jet0_sump, "nmovedtks0_jet0_sump", "; # quality tracks in jet0 associated to artificial vtx; jet0-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    nd.book(k_nmovedseedtks0_jet0_sump, "nmovedseedtks0_jet0_sump", "; # seed tracks in jet0 associated to artificial vtx; jet0-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    nd.book(k_nmovedtks_movedist3, "nmovedtks_movedist3", "; # quality tracks associated to artificial vtx;  movement 3-dist", 25, 0, 25, 20, 0, 4.0);
    nd.book(k_nmovedseedtks_movedist3, "nmovedseedtks_movedist3", "; # seed tracks associated to artificial vtx;  movement 3-dist", 25, 0, 25, 20, 0, 4.0);
    nd.book(k_llp_sump_mu, "llp_sump_mu", "; llp-moved-misc-quality-track's sum p (mu)", 100, 0, 1000);
    nd.book(k_llp_sump_ele, "llp_sump_ele", "; llp-moved-misc-quality-track's sum p (ele)", 100, 0, 1000);

    nd.book(k_llp_sump_jetmudphi, "llp_sump_jetmudphi", "; llp-moved-misc-quality-track's sum p;jet-mu #DeltaPhi", 300, 0, 300, 70, -3.5, 3.5); //check #
    nd.book(k_llp_sump_jetmudr, "llp_sump_jetmudr", "; llp-movedquality-track's sum p;jet-mu #DeltaR", 300, 0, 300, 60, 0, 6.0);  //check #
    nd.book(k_llp_sump_jeteledphi, "llp_sump_jeteledphi", "; llp-moved-misc-quality-track's sum p;jet-ele #DeltaPhi", 300, 0, 300, 70, -3.5, 3.5); //check#
    nd.book(k_llp_sump_jeteledr, "llp_sump_jeteledr", "; llp-movedquality-track's sum p;jet-ele #DeltaR", 300, 0, 300, 60, 0, 6.0); //check#
    nd.book(k_jet0_sump_movedist3, "jet0_sump_movedist3", "; jet0-movedquality-track's sum p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0);
    nd.book(k_mu1_p_movedist3, "mu1_p_movedist3", "; mu1-movedquality's p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0); //check #
    nd.book(k_ele1_p_movedist3, "ele1_p_movedist3", "; ele1-movedquality's sum p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0); //check #
    nd.book(k_jet0_sump_qrk0_dxybs, "jet0_sump_qrk0_dxybs", "; jet0-movedquality-track's sum p;  quark0's dxybs", 20, 0, 80, 20, 0, 0.2);
    nd.book(k_mu1_p_mu1_dxybs, "mu1_p_mu1_dxybs", "; mu1-movedquality's p;  mu1's dxybs", 20, 0, 80, 20, 0, 0.2); //check #
    nd.book(k_ele1_p_ele1_dxybs, "ele1_p_ele1_dxybs", "; ele1-movedquality's p;  ele1's dxybs", 20, 0, 80, 20, 0, 0.2); //check #
    nd.book(k_jet0_sump_jetmudr, "jet0_sump_jetmudr", "; jet0-movedquality-track's sum p;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_jet0_sump_jeteledr, "jet0_sump_jeteledr", "; jet0-movedquality-track's sum p;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_jet0_sump_jetlepdr, "jet0_sump_jetlepdr", "; jet0-movedquality-track's sum p;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_mu1_p_jetmudr, "mu1_p_jetdr", "; mu1-movedquality's p;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_ele1_p_jeteledr, "ele1_p_jetdr", "; ele1-movedquality's p;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_lep1_p_jetlepdr, "lep1_p_jetdr", "; lep1-movedquality's p;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_mu1_pT_jetmudr, "mu1_pT_jetdr", "; mu1-pT;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_ele1_pT_jeteledr, "ele1_pT_jetdr", "; ele1-pT;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_lep1_pT_jetlepdr, "lep1_pT_jetdr", "; lep1-pT;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_2logm_jetmudr, "2logm_jetmudr", "; log(2*sump_{tk0}*mup_{1}) + log(1-cos(#Delta#Theta));jet-mu #DeltaR", 70, 0, 7, 60, 0, 6.0); //check #
    nd.book(k_2logm_mucostheta, "2logm_mucostheta", "; log(2*sump_{tk0}*mup_{1}) + log(1-cos(#Delta#Theta));jet-mu cos(#theta)", 70, 0, 7, 80, -1, 1); //check #
    nd.book(k_2logm_jeteledr, "2logm_jeteledr", "; log(2*sump_{tk0}*elep_{1}) + log(1-cos(#Delta#Theta));jet-ele #DeltaR", 70, 0, 7, 60, 0, 6.0); //check #
    nd.book(k_2logm_elecostheta, "2logm_elecostheta", "; log(2*sump_{tk0}*elep_{1}) + log(1-cos(#Delta#Theta));jet-ele cos(#theta)", 70, 0, 7, 80, -1, 1); //check #
    nd.book(k_mu1_p_jetmu_costheta, "mu1_p_jetmu_costheta", "; mu1-movedquality's p;jet-mu cos(#theta)", 80, 0, 80, 80, -1, 1); //check #
    nd.book(k_ele1_p_jetele_costheta, "ele1_p_jetele_costheta", "; ele1-movedquality's p;jet-ele cos(#theta)", 80, 0, 80, 80, -1, 1); //check #

    nd.book(k_closeseed_trk_genmissdist, "closeseed_trk_genmissdist", "; close-seed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gendz, "closeseed_trk_gendz", "; close-seed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gennsigmadz, "closeseed_trk_gennsigmadz", "; close-seed-track's gennsigmadz; arb. units", 80, -10, 10);
    nd.book(k_movedist3_movedist2, "movedist3_movedist2", "; movement 3-dist; movement 2-dist", 50, 0, 4.0, 50, 0, 2.5); 
    nd.book(k_movedist3_jetmudr, "movedist3_jetmudr", "; movement 3-dist;jetmu #DeltaR", 50, 0, 4.0, 60, 0, 6.0); //check#
    nd.book(k_movedist3_jeteledr, "movedist3_jeteledr", "; movement 3-dist;jetele #DeltaR", 50, 0, 4.0, 60, 0, 6.0); //check#
    nd.book(k_movedist3_tightcloseseedtks, "movedist3_tightcloseseedtks", ";movement 3-dist ;# seed tracks 2#sigma-close to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_jetmu_costheta_tightcloseseedtks, "jetmu_costheta_tightcloseseedtks", "; jet-mu cos(#theta);# seed tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25); //check #
    nd.book(k_jetele_costheta_tightcloseseedtks, "jetele_costheta_tightcloseseedtks", "; jet-ele cos(#theta);# seed tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25); //check #
    
    nd.book(k_jetmu_dr_tightcloseseedtks, "jetmu_dr_tightcloseseedtks", "; jet-mu #DeltaR;# seed tracks 2#sigma-close to artificial vtx", 60, 0, 6, 25, 0, 25); //check #
    nd.book(k_jetele_dr_tightcloseseedtks, "jetele_dr_tightcloseseedtks", "; jet-ele #DeltaR;# seed tracks 2#sigma-close to artificial vtx", 60, 0, 6, 25, 0, 25); //check #

    nd.book(k_movedist3_closeseedtks, "movedist3_closeseedtks", ";movement 3-dist ;# seed tracks close to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_jetmu_costheta_closeseedtks, "jetmu_costheta_closeseedtks", "; jet-mu cos(#theta);# seed tracks close to artificial vtx", 80, -1, 1, 25, 0, 25); //check #
    nd.book(k_jetele_costheta_closeseedtks, "jetele_costheta_closeseedtks", "; jet-ele cos(#theta);# seed tracks close to artificial vtx", 80, -1, 1, 25, 0, 25); //check #
    nd.book(k_jetmu_dr_closeseedtks, "jetmu_dr_closeseedtks", "; jet-mu #DeltaR;# seed tracks close to artificial vtx", 60, 0, 6, 25, 0, 25); //check #
    nd.book(k_jetele_dr_closeseedtks, "jetele_dr_closeseedtks", "; jet-ele #DeltaR;# seed tracks close to artificial vtx", 60, 0, 6, 25, 0, 25); //check #
    nd.book(k_mu1_p_jetdphi, "mu1_p_jetdphi", "; mu1-movedquality's sum p;jets #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5); //check #
    nd.book(k_ele1_p_jetdphi, "ele1_p_jetdphi", "; ele1-movedquality's sum p;jets #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5); //check #

    nd.book(k_qrk0_dxybs, "qrk0_dxybs", "; quark0's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_jet0_dxybs, "jet0_dxybs", "; jet0's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_mu1_dxybs, "mu1_dxybs", "; mu1's dxybs; arb. units", 50, 0.0, 0.2); //check # 
    nd.book(k_ele1_dxybs, "ele1_dxybs", "; ele1's dxybs; arb. units", 50, 0.0, 0.2); //check #
    nd.book(k_2sump0pmu1_1mcos, "2sump0pmu1_1mcos", "; log(2*sump_{tk0}*p_{mutk1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0); //check # 
    nd.book(k_2sump0pele1_1mcos, "2sump0pele1_1mcos", "; log(2*sump_{tk0}*p_{eletk1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0); //check # 

    nd.book(k_2logm_mu, "2logm_mu", "; log(2*sump_{tk0}*p_{mutk1}) + log(1-cos(#Delta#Theta))", 70, 0, 7); //check #
    nd.book(k_2logm_ele, "2logm_ele", "; log(2*sump_{tk0}*p_{eletk1}) + log(1-cos(#Delta#Theta))", 70, 0, 7); //check #

    nd.book(k_mu1jet0_trk_dx, "mu1jet0_trk_dx", "; jet0 x pos - mu1 x pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1jet0_trk_dy, "mu1jet0_trk_dy", "; jet0 y pos - mu1 y pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1jet0_trk_dz, "mu1jet0_trk_dz", "; jet0 z pos - mu1 z pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_ele1jet0_trk_dx, "ele1jet0_trk_dx", "; jet0 x pos - ele1 x pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_ele1jet0_trk_dy, "ele1jet0_trk_dy", "; jet0 y pos - ele1 y pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_ele1jet0_trk_dz, "ele1jet0_trk_dz", "; jet0 z pos - ele1 z pos; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1jet0_trk_dist2d, "mu1jet0_trk_dist2d", "; 2d distance between jet0 and mu1; arb. units", 50, 0.0, 5.0);
    nd.book(k_ele1jet0_trk_dist2d, "ele1jet0_trk_dist2d", "; 2d distance between jet0 and ele1; arb. units", 50, 0.0, 5.0);

    nd.book(k_jet0_trk_dz, "jet0_trk_dz", "; jet0-movedquality-track's dzpv; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1_trk_dz, "mu1_trk_dz", "; mu1-movedquality's dzpv; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_ele1_trk_dz, "ele1_trk_dz", "; ele1-movedquality's dzpv; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_jet0_trk_vtxdxy, "jet0_trk_vtxdxy", "; jet0-movedquality-track's dxy to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1_trk_vtxdxy, "mu1_trk_vtxdxy", "; mu1-movedquality's dxy to vtx; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_ele1_trk_vtxdxy, "ele1_trk_vtxdxy", "; ele1-movedquality's dxy to vtx; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_jet0_trk_vtxdz, "jet0_trk_vtxdz", "; jet0-movedquality-track's dz to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1_trk_vtxdz, "mu1_trk_vtxdz", "; mu1-movedquality's dz to vtx; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_ele1_trk_vtxdz, "ele1_trk_vtxdz", "; ele1-movedquality's dz to vtx; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_jet0_trk_nsigmavtxdz, "jet0_trk_nsigmavtxdz", "; jet0-movedquality-track's nsigmavtxdz; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_nsigmavtxdz, "mu1_trk_nsigmavtxdz", "; mu1-movedquality's nsigmavtxdz; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_nsigmavtxdz, "ele1_trk_nsigmavtxdz", "; ele1-movedquality's nsigmavtxdz; arb. units", 80, -10, 10); //check #
    nd.book(k_jet0_trk_nsigmavtxdxy, "jet0_trk_nsigmavtxdxy", "; jet0-movedquality-track's nsigmavtxdxy; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_nsigmavtxdxy, "mu1_trk_nsigmavtxdxy", "; mu1-movedquality-track's nsigmavtxdxy; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_nsigmavtxdxy, "ele1_trk_nsigmavtxdxy", "; ele1-movedquality-track's nsigmavtxdxy; arb. units", 80, -10, 10); //check #

    nd.book(k_jet0_trk_nsigmavtx, "jet0_trk_nsigmavtx", "; jet0-movedquality-track's nsigmavtx; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_nsigmavtx, "mu1_trk_nsigmavtx", "; mu1-movedquality-track's nsigmavtx; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_nsigmavtx, "ele1_trk_nsigmavtx", "; ele1-movedquality-track's nsigmavtx; arb. units", 80, -10, 10); //check #
    nd.book(k_jet0_trk_dzerr, "jet0_trk_dzerr", "; jet0-movedquality-track's dz err; arb. units", 100, 0.0, 0.05);
    nd.book(k_mu1_trk_dzerr, "mu1_trk_dzerr", "; mu1-movedquality-track's dz err; arb. units", 100, 0.0, 0.05); //check #
    nd.book(k_ele1_trk_dzerr, "ele1_trk_dzerr", "; ele1-movedquality-track's dz err; arb. units", 100, 0.0, 0.05); //check #
    nd.book(k_jet0_trk_dxyerr, "jet0_trk_dxyerr", "; jet0-movedquality-track's dxy err; arb. units", 100, 0.0, 0.05);
    nd.book(k_mu1_trk_dxyerr, "mu1_trk_dxyerr", "; mu1-movedquality-track's dxy err; arb. units", 100, 0.0, 0.05); //check #
    nd.book(k_ele1_trk_dxyerr, "ele1_trk_dxyerr", "; ele1-movedquality-track's dxy err; arb. units", 100, 0.0, 0.05); //check #
    nd.book(k_jet0_trk_eta, "jet0_trk_eta", "; jet0-movedquality-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_mu1_trk_eta, "mu1_trk_eta", "; mu1-movedquality-track's eta; arb. units", 70, -3.5, 3.5); //check #
    nd.book(k_ele1_trk_eta, "ele1_trk_eta", "; ele1-movedquality-track's eta; arb. units", 70, -3.5, 3.5); //check #
    nd.book(k_jet0_trk_gennsigma, "jet0_trk_gennsigma", "; jet0-movedquality-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_gennsigma, "mu1_trk_gennsigma", "; mu1-movedquality's n#sigma to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_gennsigma, "ele1_trk_gennsigma", "; ele1-movedquality's n#sigma to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_jet0_trk_gennsigmamissdist, "jet0_trk_gennsigmamissdist", "; jet0-movedquality-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_gennsigmamissdist, "mu1_trk_gennsigmamissdist", "; mu1-movedquality's n#sigma missdist to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_gennsigmamissdist, "ele1_trk_gennsigmamissdist", "; ele1-movedquality's n#sigma missdist to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_jet0_trk_genmissdist, "jet0_trk_genmissdist", "; jet0-movedquality-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_mu1_trk_genmissdist, "mu1_trk_genmissdist", "; mu1-movedquality's missdist to LLP; arb. units", 50, -0.05, 0.05); //check #
    nd.book(k_ele1_trk_genmissdist, "ele1_trk_genmissdist", "; ele1-movedquality's missdist to LLP; arb. units", 50, -0.05, 0.05); //check  #
    nd.book(k_jet0_trk_gendz, "jet0_trk_gendz", "; jet0-movedquality-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_mu1_trk_gendz, "mu1_trk_gendz", "; mu1-movedquality's dz to LLP; arb. units", 50, -0.05, 0.05); //check #
    nd.book(k_ele1_trk_gendz, "ele1_trk_gendz", "; ele1-movedquality's dz to LLP; arb. units", 50, -0.05, 0.05); //check #
    nd.book(k_jet0_trk_gennsigmadz, "jet0_trk_gennsigmadz", "; jet0-movedquality-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_mu1_trk_gennsigmadz, "mu1_trk_gennsigmadz", "; mu1-movedquality-track's n#sigma dz to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_ele1_trk_gennsigmadz, "ele1_trk_gennsigmadz", "; ele1-movedquality-track's n#sigma dz to LLP; arb. units", 80, -10, 10); //check #
    nd.book(k_jet0_trk_whichpv, "jet0_trk_whichpv", "; jet0-movedquality-track's which_pv; arb. units", 40, 0.0, 40);
    nd.book(k_mu1_trk_whichpv, "mu1_trk_whichpv", "; mu1-movedquality-track's which_pv; arb. units", 40, 0.0, 40); //check #
    nd.book(k_ele1_trk_whichpv, "ele1_trk_whichpv", "; ele1-movedquality-track's which_pv; arb. units", 40, 0.0, 40); //check #
    nd.book(k_jet0_trk_dsz, "jet0_trk_dsz", "; jet0-movedquality-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_mu1_trk_dsz, "mu1_trk_dsz", "; mu1-movedquality-track's dsz; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_ele1_trk_dsz, "ele1_trk_dsz", "; ele1-movedquality-track's dsz; arb. units", 50, -1.0, 1.0); //check #
    nd.book(k_jet0_trk_dxy, "jet0_trk_dxy", "; jet0-movedquality-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_mu1_trk_dxy, "mu1_trk_dxy", "; mu1-movedquality-track's dxybs; arb. units", 50, -0.5, 0.5); //check #
    nd.book(k_ele1_trk_dxy, "ele1_trk_dxy", "; ele1-movedquality-track's dxybs; arb. units", 50, -0.5, 0.5); //check #
    nd.book(k_jet0_trk_nsigmadxy, "jet0_trk_nsigmadxy", "; jet0-movedquality-track's nsigmadxybs; arb. units", 160, -20, 20);
    nd.book(k_mu1_trk_nsigmadxy, "mu1_trk_nsigmadxy", "; mu1-movedquality-track's nsigmadxybs; arb. units", 160, -20, 20); //check #
    nd.book(k_ele1_trk_nsigmadxy, "ele1_trk_nsigmadxy", "; ele1-movedquality-track's nsigmadxybs; arb. units", 160, -20, 20); //check #
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 30, 0, 30);
    nd.book(k_dphi_sum_jmu_mv, "dphi_sum_jmu_mv", ";#Delta #phi between jet0+mu1 and move vec;events/bin", 70, -3.5, 3.5); //check # 
    nd.book(k_deta_sum_jmu_mv, "deta_sum_jmu_mv", ";abs #Delta #eta between jet0+mu1 and move vec;events/bin", 25, 0, 4); //check #
    nd.book(k_dphi_sum_jele_mv, "dphi_sum_jele_mv", ";#Delta #phi between jet0+ele1 and move vec;events/bin", 70, -3.5, 3.5); //check #
    nd.book(k_deta_sum_jele_mv, "deta_sum_jele_mv", ";abs #Delta #eta between jet0+ele1 and move vec;events/bin", 25, 0, 4); //check #

    nd.book(k_jetpt0_jmasymm, "jetpt0_jmasymm", ";jet p_{T} 0; jetmu asymm. A_{J}", 50, 0, 1000, 50, -1, 1); //check #
    nd.book(k_jetpt0_jeasymm, "jetpt0_jeasymm", ";jet p_{T} 0; jetele asymm. A_{J}", 50, 0, 1000, 50, -1, 1); //check #
    nd.book(k_mupt1_asymm, "mupt1_asymm", ";mu p_{T} 1; jetmu asymm. A_{J}", 50, 0, 1000, 50, -1, 1); //check #
    nd.book(k_elept1_asymm, "elept1_asymm", ";ele p_{T} 1; jetele asymm. A_{J}", 50, 0, 1000, 50, -1, 1); //check #
    nd.book(k_jeteta0_jmasymm, "jeteta0_jmasymm", ";jet #eta 0; jetmu asymm. A_{J}", 100, -4, 4, 50, -1, 1); //check #
    nd.book(k_jeteta0_jeasymm, "jeteta0_jeasymm", ";jet #eta 0; jetmu asymm. A_{J}", 100, -4, 4, 50, -1, 1); //check #
    nd.book(k_mueta1_asymm, "mueta1_asymm", ";mu #eta 1; jetmu asymm. A_{J}", 100, -4, 4, 50, -1, 1); //check #
    nd.book(k_eleeta1_asymm, "eleeta1_asymm", ";ele #eta 1; jetele asymm. A_{J}", 100, -4, 4, 50, -1, 1); //check #
    nd.book(k_jetmudr_asymm, "jetmudr_asymm", ";jetmu #DeltaR; jetmu asymm. A_{J}", 60, 0, 6, 50, -1, 1); //check #
    nd.book(k_jeteledr_asymm, "jeteledr_asymm", ";jetele #DeltaR; jetele asymm. A_{J}", 60, 0, 6, 50, -1, 1); //check #

    nd.book(k_nalltracks, "nalltracks", ";# all tracks;events/10", 200, 0, 2000);
    nd.book(k_nseedtracks, "nseedtracks", ";# seed tracks;events", 80, 0, 80);
    nd.book(k_seedtracks_jetmudr, "seedtracks_jetmudr", "; # seed tracks; jetmu #DeltaR", 20, 0, 20, 60, 0, 6); //check#
    nd.book(k_seedtracks_jeteledr, "seedtracks_jeteledr", "; # seed tracks; jetele #DeltaR", 20, 0, 20, 60, 0, 6); //check#
    nd.book(k_seedtracks_2logm_mu, "seedtracks_2logm_mu", "; # seed tracks; log(2*sump_{tk0}*p_{mutk1}) + log(1-cos(#Delta#Theta))", 20, 0, 20, 70, 0, 7); //check #
    nd.book(k_seedtracks_2logm_ele, "seedtracks_2logm_ele", "; # seed tracks; log(2*sump_{tk0}*p_{eletk1}) + log(1-cos(#Delta#Theta))", 20, 0, 20, 70, 0, 7); //check #

    nd.book(k_npreseljets, "npreseljets", ";# preselected jets;events/1", 20, 0, 20);
    nd.book(k_npreselbjets, "npreselbjets", ";# preselected b jets;events/1", 20, 0, 20);
    nd.book(k_npreselmu, "npreselmu", ";# preselected muons;events/1", 20, 0, 20);
    nd.book(k_npreselele, "npreselele", ";# preselected electrons;events/1", 20, 0, 20);

    nd.book(k_jetmui01, "jetmui01", ";jet i 0 (GeV);mu i 1 (GeV);events", 15, 0, 15, 15, 0, 15); //check #
    nd.book(k_jetmup01, "jetmup01", ";jet 0 momentum (GeV);mu 1 momentum (GeV)", 200, 0, 2000, 200, 0, 2000); //check #
    nd.book(k_jetmupt01, "jetmupt01", ";jet p_{T} 0 (GeV);mu p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000); //check #
    nd.book(k_jetmueta01, "jetmueta01", ";jet #eta 0 (GeV);mu #eta 1 (GeV)", 100, -4, 4, 100, -4, 4); //check # 
    nd.book(k_jetmuphi01, "jetmuphi01", ";jet #phi 0 (GeV);mu #phi 1 (GeV)", 126, -M_PI, M_PI, 126, -M_PI, M_PI); //check #
    nd.book(k_jetelei01, "jetelei01", ";jet i 0 (GeV);ele i 1 (GeV);events", 15, 0, 15, 15, 0, 15); //check #
    nd.book(k_jetelep01, "jetelep01", ";jet 0 momentum (GeV);ele 1 momentum (GeV)", 200, 0, 2000, 200, 0, 2000); //check #
    nd.book(k_jetelept01, "jetelept01", ";jet p_{T} 0 (GeV);ele p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000); //check #
    nd.book(k_jeteleeta01, "jeteleeta01", ";jet #eta 0 (GeV);ele #eta 1 (GeV)", 100, -4, 4, 100, -4, 4); //check #
    nd.book(k_jetelephi01, "jetelephi01", ";jet #phi 0 (GeV);ele #phi 1 (GeV)", 126, -M_PI, M_PI, 126, -M_PI, M_PI); //check #
    nd.book(k_jetsume, "jetsume", ";#Sigma jet energy (GeV);events/5 GeV", 200, 0, 1000);
    //should probably FIX ???
    nd.book(k_jetdrmax, "jetdrmax", ";max jet-lep #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdravg, "jetdravg", ";avg jet-lep #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetdetamax, "jetdetamax", ";max jet-lep #Delta #eta; events", 200, -5, 5);
    nd.book(k_jetdetaavg, "jetdetaavg", ";avg jet-lep #Delta #eta; events", 200, -5, 5);
    nd.book(k_jetdphimax, "jetdphimax", ";max jet-lep #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jetdphiavg, "jetdphiavg", ";avg jet-lep #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jet0_tkdrmax, "jet0_tkdrmax", ";max track #Delta R in jet0; events", 63, 0, M_PI);
    nd.book(k_jet0_tkdravg, "jet0_tkdravg", ";avg track #Delta R in jet0; events", 63, 0, M_PI);
    nd.book(k_jet_dphi_deta_avg, "jet_dphi_deta_avg", ";avg jet #Delta #phi; avg jet #Delta #eta", 31, -M_PI, M_PI, 50, -4, 4); 
    nd.book(k_jdphi_nmovedtks, "jdphi_nmovedtracks", ";abs. avg. jet #Delta #phi; no. moved tracks", 31, 0, M_PI, 60, 0, 120);
    nd.book(k_jdeta_nmovedtks, "jdeta_nmovedtracks", ";abs. avg. jet #Delta #eta; no. moved tracks", 25, 0, 4, 60, 0, 120);
    nd.book(k_jdr_nmovedtks, "jdr_nmovedtracks", ";avg. jet #Delta R; no. moved tracks", 30, 0, 6, 60, 0, 120);
    //
    nd.book(k_jtheta0_nmovedtks, "jtheta0_nmovedtracks", ";3D angle btwn moved jet and move vector; no. moved tracks", 31, 0, M_PI, 60, 0, 120);
    nd.book(k_jetmumovea3d01, "jetmumovea3d", ";3D angle between jet 0 and move vector;3D angle between mu 1 and move vector", 63, 0, M_PI, 63, 0, M_PI); //check #
    nd.book(k_jetelemovea3d01, "jetelemovea3d", ";3D angle between jet 0 and move vector;3D angle between ele 1 and move vector", 63, 0, M_PI, 63, 0, M_PI); //check #
    nd.book(k_jetmovea3d_v_jetp, "jetmovea3d_v_jetp", ";jet momentum p (GeV);3D angle between moved jet and move vector", 200, 0, 2000, 63, 0, M_PI);
    nd.book(k_mumovea3d_v_mup, "mumovea3d_v_mup", ";mu momentum p (GeV);3D angle between moved mu and move vector", 200, 0, 2000, 63, 0, M_PI); //check#
    nd.book(k_elemovea3d_v_elep, "elemovea3d_v_elep", ";ele momentum p (GeV);3D angle between moved ele and move vector", 200, 0, 2000, 63, 0, M_PI); //check#

    nd.book(k_jetmovea3d0_v_movevectoreta, "jetmovea3d0_v_movevectoreta", ";move vector eta;3D angle between moved jet and move vector", 100, -4, 4, 63, 0, M_PI);
    nd.book(k_mumovea3d1_v_movevectoreta, "mumovea3d1_v_movevectoreta", ";move vector eta;3D angle between moved mu and move vector", 100, -4, 4, 63, 0, M_PI); //check #
    nd.book(k_elemovea3d1_v_movevectoreta, "elemovea3d1_v_movevectoreta", ";move vector eta;3D angle between moved ele and move vector", 100, -4, 4, 63, 0, M_PI); //check #
    nd.book(k_jeta3dmax, "jeta3dmax", ";max 3D angle between moved jet-lep;events/0.05", 63, 0, M_PI);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_muangle1, "mumovea3d1", ";Angle between mu1 and SV;arb. units", 63, 0, M_PI); //check #
    nd.book(k_eleangle1, "elemovea3d1", ";Angle between ele1 and SV;arb. units", 63, 0, M_PI); //check #
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_mu1_mv, "dphi_mu1_mv", ";abs #Delta #phi between mu1 and move vec;events/bin", 63, 0, M_PI); //check #
    nd.book(k_dphi_ele1_mv, "dphi_ele1_mv", ";abs #Delta #phi between ele1 and move vec;events/bin", 63, 0, M_PI); //check #
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_mu1_mv, "deta_mu1_mv", ";abs #Delta #eta between mu1 and move vec;events/bin", 25, 0, 4);//check #
    nd.book(k_deta_ele1_mv, "deta_ele1_mv", ";abs #Delta #eta between ele1 and move vec;events/bin", 25, 0, 4); //check  #
    nd.book(k_dphi_j0_mv_jdeta, "dphi_j0_mv_jdeta", ";abs #Delta #phi btwn jet0 and move vec; abs #Delta #eta btwn jets", 63, 0, M_PI, 50, 0, 5);
    nd.book(k_jetsumntracks, "jetsumntracks", ";#Sigma jet # tracks;events/5", 200, 0, 1000);
    nd.book(k_jetsumseedtracks, "jetsumseedtracks", ";#Sigma jet # seed tracks;events/5", 200, 0, 1000);    
    nd.book(k_miscseedtracks, "miscseedtracks", ";#Sigma seed tks not from moved jets;count", 30, 0, 30);
    nd.book(k_misccloseseedtracks, "misccloseseedtracks", ";#Sigma seed tks 5#sigma to artificial vtx not from moved jets;count", 20, 0, 20);
    nd.book(k_closeseedtks,  "closeseedtks", ";# seed tracks close to artificial vtx.;count", 80, 0, 80);
    nd.book(k_tightcloseseedtks,  "tightcloseseedtks", ";# seed tracks 2#sigma-close to artificial vtx.;count", 25, 0, 25);
    nd.book(k_movedseedtks,  "movedseedtks", ";# moved seed tracks;count", 30, 0, 30);
    nd.book(k_movedseedtks_jetmudr, "movedseedtks_jetmudr", ";# moved seed tracks; jet-mu #DeltaR", 30, 0, 30, 60, 0, 6); //check#
    nd.book(k_movedseedtks_jeteledr, "movedseedtks_jeteledr", ";# moved seed tracks; jet-ele #DeltaR", 30, 0, 30, 60, 0, 6); //check#

    nd.book(k_movedvtxseedtks,  "movedvtxseedtks", ";# moved seed tracks in vtx;count", 30, 0, 30);
    nd.book(k_movedcloseseedtks,  "movedcloseseedtks", ";# moved seed tracks 5#sigma to LLP;count", 30, 0, 30);
    nd.book(k_rat_moved_to_closetks, "rat_moved_to_closetks", ";#frac{# moved seed tracks 5#sigma to LLP}{# seed tracks 5#sigma to LLP};count", 50, 0, 1);
    nd.book(k_rat_moved_to_vtxtks, "rat_moved_to_vtxtks", ";#frac{# moved seed tracks in vtx}{# vtx ntrack};count", 50, 0, 1);
    nd.book(k_jetntracks_v_jetp, "jetntracks_v_jetp01", ";jet momentum (GeV);jet # tracks", 200, 0, 2000, 50, 0, 50);
    nd.book(k_nvtx, "nvtx", ";number of vertices;events/1", 8, 0, 8);
    nd.book(k_vtxbs2derr, "vtxbs2derr", ";bs2derr of vertex;events", 500, 0, 0.05);
    nd.book(k_vtxbs2derr_avgtkdr, "vtxbs2derr_avgtkdr", ";bs2derr of vertex; avg tk #Delta R", 100, 0, 0.025, 31, 0, M_PI);
    nd.book(k_vtxbs2derr_jdeta, "vtxbs2derr_jdeta", ";bs2derr of vertex; jet #Delta #eta", 100, 0, 0.025, 25, 0, 4);
    nd.book(k_vtxbs2derr_dphi_j0_mv, "vtxbs2derr_dphi_j0_mv", ";bs2derr of vertex;  #Delta #phi btwn j0 and MV", 100, 0, 0.025, 63, 0, M_PI);
    nd.book(k_vtxbs2derr_jdr, "vtxbs2derr_jdr", ";bs2derr of vertex; jet #Delta R", 100, 0, 0.025, 30, 0, 6);
    nd.book(k_vtxunc, "vtxunc", ";dist3d(move vector, vtx) cm; arb. units", 200, 0, 0.2);
    nd.book(k_vtxunc2d, "vtxunc2d", ";dist2d(move vector, vtx) cm; arb. units", 200, 0, 0.2);
    nd.book(k_vtxeta, "vtxeta", ";eta of vertex;events", 100, -4, 4);
    nd.book(k_vtxz, "vtxz", ";z pos of vertex;events", 100, -10, 10);
    nd.book(k_vtxdbv, "vtxdbv", ";2D displacement of vertex to a beamspot;events", 50, 0, 2.0); 
    nd.book(k_vtx3dbv, "vtx3dbv", ";3D displacement of vertex to a beamspot;events", 50, 0, 2.0); 
    nd.book(k_vtxntk, "vtxntk", ";ntrack of vertex;events", 20, 0, 20);
    nd.book(k_vtxnm1_dbv, "vtxnm1_dbv", ";2D displacement of n-1-vertex to a beamspot;events", 50, 0, 2.0); 
    nd.book(k_vtxnm1_ntk, "vtxnm1_ntk", ";ntrack of n-1-vertex;events", 20, 0, 20);
    nd.book(k_vtxnm1_bs2derr, "vtxnm1_bs2derr", ";bs2derr of n-1-vertex;events", 500, 0, 0.05);
    nd.book(k_vtx4tkchi2, "vtx4tkchi2", ";norm-chi2/4tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx4tkdbv, "vtx4tkdbv", ";2D-displacement of a vtx/4tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx4tkzdbv, "vtx4tkzdbv", ";z-displacement of a vtx/4tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx4tkunc, "vtx4tkunc", ";3D-distance of a vtx to an LLP/4tk-vtx cm. ;events", 100, 0, 0.04);
    nd.book(k_vtx5tkchi2, "vtx5tkchi2", ";norm-chi2/5tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx5tkdbv, "vtx5tkdbv", ";2D-displacement of a vtx/5tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx5tkzdbv, "vtx5tkzdbv", ";z-displacement of a vtx/5tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx5tkunc, "vtx5tkunc", ";3D-distance of a vtx to an LLP/5tk-vtx cm. ;events", 100, 0, 0.04);
    nd.book(k_vtx6tkchi2, "vtx6tkchi2", ";norm-chi2/6tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx6tkdbv, "vtx6tkdbv", ";2D-displacement of a vtx/6tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx6tkzdbv, "vtx6tkzdbv", ";z-displacement of a vtx/6tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx6tkunc, "vtx6tkunc", ";3D-distance of a vtx to an LLP/6tk-vtx cm. ;events", 100, 0, 0.04);
  }

  // JMTBAD some (all?) of these should be numdens
  TH1D* h_vtxdbv[num_numdens] = {0};
  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //  TH1D* h_vtxtkonlymass[num_numdens] = {0};  // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxmass[num_numdens] = {0};
  TH1D* h_vtxanglemax[num_numdens] = {0};
  TH1D* h_vtxphi[num_numdens] = {0};
  TH1D* h_vtxeta[num_numdens] = {0};
  TH1D* h_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxntracks[num_numdens] = {0};
  //  TH2D* h_vtxbs2derr_v_vtxtkonlymass[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxanglemax[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxphi[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxeta[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxpt[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_vtxdbv[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_etamovevec[num_numdens] = {0};
  TH2D* h_vtxbs2derr_v_maxtkerrdxy[num_numdens] = {0};

  TH1D* h_tks_pt[num_numdens] = {0};
  TH1D* h_tks_eta[num_numdens] = {0};
  TH1D* h_tks_phi[num_numdens] = {0};
  TH1D* h_tks_dxy[num_numdens] = {0};
  TH1D* h_tks_dz[num_numdens] = {0};
  TH1D* h_tks_err_pt[num_numdens] = {0};
  TH1D* h_tks_err_eta[num_numdens] = {0};
  TH1D* h_tks_err_phi[num_numdens] = {0};
  TH1D* h_tks_err_dxy[num_numdens] = {0};
  TH1D* h_tks_err_dz[num_numdens] = {0};
  TH1D* h_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_tks_npxlayers[num_numdens] = {0};
  TH1D* h_tks_nstlayers[num_numdens] = {0};

  TH1D* h_vtx_tks_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nstlayers[num_numdens] = {0};

  TH1D* h_vtx_tks_nomove_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_pt[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_eta[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_phi[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_err_dz[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nsigmadxy[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_npxlayers[num_numdens] = {0};
  TH1D* h_vtx_tks_nomove_nstlayers[num_numdens] = {0};

  TH1D* h_moved_tks_pt[num_numdens] = {0};
  TH1D* h_moved_tks_eta[num_numdens] = {0};
  TH1D* h_moved_tks_phi[num_numdens] = {0};
  TH1D* h_moved_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_dz[num_numdens] = {0};
  TH1D* h_moved_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_tks_nstlayers[num_numdens] = {0};

  TH1D* h_moved_nosel_tks_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_pt[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_eta[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_phi[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_err_dz[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nsigmadxy[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_npxlayers[num_numdens] = {0};
  TH1D* h_moved_nosel_tks_nstlayers[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxdbv[i] = new TH1D(TString::Format("h_%i_vtxdbv", i), ";d_{BV} of largest vertex (cm);events/50 #mum", 400, 0, 2);
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks", i), ";# tracks in largest vertex;events/1", 60, 0, 60);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr", i), ";#sigma(d_{BV}) of largest vertex (cm);events/1 #mum", 500, 0, 0.05);
    //    h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 50, 0, 500);
    h_vtxmass[i] = new TH1D(TString::Format("h_%i_vtxmass", i), ";track+jets mass of largest vertex (GeV);events/1 GeV", 100, 0, 5000);
    h_vtxanglemax[i] = new TH1D(TString::Format("h_%i_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;events/0.03", 100, 0, M_PI);
    h_vtxphi[i] = new TH1D(TString::Format("h_%i_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;events/0.06", 100, -M_PI, M_PI);
    h_vtxeta[i] = new TH1D(TString::Format("h_%i_vtxeta", i), ";tracks-plus-jets-by-ntracks #eta of largest vertex; events/0.03", 100, -4, 4);
    h_vtxpt[i] = new TH1D(TString::Format("h_%i_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);events/1", 500, 0, 500);

    h_vtxbs2derr_v_vtxntracks[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxntracks", i), ";# tracks in largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 60, 0, 60, 500, 0, 0.05);
    //    h_vtxbs2derr_v_vtxtkonlymass[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxanglemax[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxanglemax", i), ";biggest angle between pairs of tracks in vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxphi[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxphi", i), ";tracks-plus-jets-by-ntracks #phi of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, -M_PI, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxeta[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxeta", i), ";tracks-plus-jets-by-ntracks #theta of largest vertex;#sigma(d_{BV}) of largest vertex (cm)", 100, 0, M_PI, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxpt[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxpt", i), ";tracks-plus-jets-by-ntracks p_{T} of largest vertex (GeV);#sigma(d_{BV}) of largest vertex (cm)", 500, 0, 500, 500, 0, 0.05);
    h_vtxbs2derr_v_vtxdbv[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_vtxdbv", i), ";d_{BV} of largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 400, 0, 2, 500, 0, 0.05);
    h_vtxbs2derr_v_etamovevec[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_etamovevec", i), ";eta of move vector;#sigma(d_{BV}) of largest vertex (cm)", 100, -4, 4, 500, 0, 0.05);
    h_vtxbs2derr_v_maxtkerrdxy[i] = new TH2D(TString::Format("h_%i_vtxbs2derr_v_maxtkerrdxy", i), ";largest track #sigma(dxy) in largest vertex (cm);#sigma(d_{BV}) of largest vertex (cm)", 100, 0, 0.1, 500, 0, 0.05);

    h_tks_pt[i] = new TH1D(TString::Format("h_%i_tks_pt", i), ";moved and selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_tks_eta[i] = new TH1D(TString::Format("h_%i_tks_eta", i), ";moved and selected track #eta;tracks/0.16", 50, -4, 4);
    h_tks_phi[i] = new TH1D(TString::Format("h_%i_tks_phi", i), ";moved and selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_tks_dxy[i] = new TH1D(TString::Format("h_%i_tks_dxy", i), ";moved and selected track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_tks_dz[i] = new TH1D(TString::Format("h_%i_tks_dz", i), ";moved and selected track dz;tracks/100 #mum", 200, -1, 1);
    h_tks_err_pt[i] = new TH1D(TString::Format("h_%i_tks_err_pt", i), ";moved and selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_tks_err_eta[i] = new TH1D(TString::Format("h_%i_tks_err_eta", i), ";moved and selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_phi[i] = new TH1D(TString::Format("h_%i_tks_err_phi", i), ";moved and selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_tks_err_dxy", i), ";moved and selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_err_dz[i] = new TH1D(TString::Format("h_%i_tks_err_dz", i), ";moved and selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_tks_nsigmadxy", i), ";moved and selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_tks_npxlayers", i), ";moved and selected track npxlayers;tracks/1", 20, 0, 20);
    h_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_tks_nstlayers", i), ";moved and selected track nstlayers;tracks/1", 20, 0, 20);

    h_vtx_tks_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_pt", i), ";track p_{T} in largest vertex (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_eta", i), ";track #eta in largest vertex;tracks/0.16", 50, -4, 4);
    h_vtx_tks_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_phi", i), ";track #phi in largest vertex;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_dxy", i), ";track dxy in largest vertex;tracks/40 #mum", 200, -0.8, 0.8);
    h_vtx_tks_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_dz", i), ";track dz in largest vertex;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_pt", i), ";track #sigma(p_{T}) in largest vertex;tracks/0.01", 200, 0, 2);
    h_vtx_tks_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_eta", i), ";track #sigma(#eta) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_phi", i), ";track #sigma(#phi) in largest vertex;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_err_dz", i), ";track #sigma(dz) (cm) in largest vertex;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex;tracks/0.1", 200, 0, 20);
    h_vtx_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_npxlayers", i), ";track npxlayers in largest vertex;tracks/1", 20, 0, 20);
    h_vtx_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nstlayers", i), ";track nstlayers in largest vertex;tracks/1", 20, 0, 20);

    h_vtx_tks_nomove_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_pt", i), ";track p_{T} in largest vertex but not moved (GeV);tracks/1 GeV", 200, 0, 200);
    h_vtx_tks_nomove_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_eta", i), ";track #eta in largest vertex but not moved;tracks/0.16", 50, -4, 4);
    h_vtx_tks_nomove_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_phi", i), ";track #phi in largest vertex but not moved;tracks/0.13", 50, -M_PI, M_PI);
    h_vtx_tks_nomove_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dxy", i), ";track dxy in largest vertex but not moved;tracks/40 #mum", 200, -0.4, 0.4);
    h_vtx_tks_nomove_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_dz", i), ";track dz in largest vertex but not moved;tracks/100 #mum", 200, -1, 1);
    h_vtx_tks_nomove_err_pt[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_pt", i), ";track #sigma(p_{T}) in largest vertex but not moved;tracks/0.01", 200, 0, 2);
    h_vtx_tks_nomove_err_eta[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_eta", i), ";track #sigma(#eta) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_phi[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_phi", i), ";track #sigma(#phi) in largest vertex but not moved;tracks/0.0001", 200, 0, 0.02);
    h_vtx_tks_nomove_err_dxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dxy", i), ";track #sigma(dxy) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_err_dz[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_err_dz", i), ";track #sigma(dz) (cm) in largest vertex but not moved;tracks/0.001 cm", 100, 0, 0.1);
    h_vtx_tks_nomove_nsigmadxy[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nsigmadxy", i), ";track n#sigma(dxy) in largest vertex but not moved;tracks/0.1", 200, 0, 20);
    h_vtx_tks_nomove_npxlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_npxlayers", i), ";track npxlayers in largest vertex but not moved;tracks/1", 20, 0, 20);
    h_vtx_tks_nomove_nstlayers[i] = new TH1D(TString::Format("h_%i_vtx_tks_nomove_nstlayers", i), ";track nstlayers in largest vertex but not moved;tracks/1", 20, 0, 20);

    h_moved_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_pt", i), ";moved track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_eta", i), ";moved track #eta;tracks/0.16", 50, -4, 4);
    h_moved_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_phi", i), ";moved track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_dxy", i), ";moved track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_moved_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_dz", i), ";moved track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_tks_err_pt", i), ";moved track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_tks_err_eta", i), ";moved track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_tks_err_phi", i), ";moved track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dxy", i), ";moved track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_tks_err_dz", i), ";moved track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_tks_nsigmadxy", i), ";moved track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_npxlayers", i), ";moved track npxlayers;tracks/1", 20, 0, 20);
    h_moved_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_tks_nstlayers", i), ";moved track nstlayers;tracks/1", 20, 0, 20);

    h_moved_nosel_tks_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_pt", i), ";moved but not selected track p_{T} (GeV);tracks/1 GeV", 200, 0, 200);
    h_moved_nosel_tks_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_eta", i), ";moved but not selected track #eta;tracks/0.16", 50, -4, 4);
    h_moved_nosel_tks_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_phi", i), ";moved but not selected track #phi;tracks/0.13", 50, -M_PI, M_PI);
    h_moved_nosel_tks_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dxy", i), ";moved but not selected track dxy;tracks/40 #mum", 200, -0.8, 0.8);
    h_moved_nosel_tks_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_dz", i), ";moved but not selected track dz;tracks/100 #mum", 200, -1, 1);
    h_moved_nosel_tks_err_pt[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_pt", i), ";moved but not selected track #sigma(p_{T});tracks/0.01", 200, 0, 2);
    h_moved_nosel_tks_err_eta[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_eta", i), ";moved but not selected track #sigma(#eta);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_phi[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_phi", i), ";moved but not selected track #sigma(#phi);tracks/0.0001", 200, 0, 0.02);
    h_moved_nosel_tks_err_dxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dxy", i), ";moved but not selected track #sigma(dxy) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_err_dz[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_err_dz", i), ";moved but not selected track #sigma(dz) (cm);tracks/0.001 cm", 100, 0, 0.1);
    h_moved_nosel_tks_nsigmadxy[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nsigmadxy", i), ";moved but not selected track n#sigma(dxy);tracks/0.1", 200, 0, 20);
    h_moved_nosel_tks_npxlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_npxlayers", i), ";moved but not selected track npxlayers;tracks/1", 20, 0, 20);
    h_moved_nosel_tks_nstlayers[i] = new TH1D(TString::Format("h_%i_moved_nosel_tks_nstlayers", i), ";moved but not selected track nstlayers;tracks/1", 20, 0, 20);
  }


  std::map<std::string, double> nums;
  unsigned long long nden = 0, nnegden = 0;
  double den = 0, negden = 0;
  
  //jmt::ConfigFromEnv env("sm", true);
  //const int inst = env.get_int("inst", 0);
  //const int seed = env.get_int("seed", 12919135 + inst);
  //gRandom->SetSeed(0);

  auto fcn = [&]() {
    double w = nr.weight();

    if (nr.use_weights()) {
      if (nr.is_mc() && btagsf_weights) {
        assert(0); // JMTBAD update for 2017+8, probably just the discriminator
        double p_mc = 1, p_data = 1;

        for (size_t i = 0, ie = jets.n(); i < ie; ++i) {
          const double pt = jets.pt(i);
          const double eta = jets.eta(i);
          const bool is_tagged = jets.bdisc(i) > 0.935;
          const int hf = jets.genflavor(i);

          const double sf = btagsfhelper->scale_factor(BTagSFHelper::BH, BTagSFHelper::tight, hf, eta, pt).v;
          const double e = btagsfhelper->efficiency(hf, eta, pt).v;
          assert(e > 0 && e <= 1);

          if (is_tagged) {
            p_mc   *= e;
            p_data *= e*sf;
          }
          else {
            p_mc   *= 1-e;
            p_data *= 1-e*sf;
          }
        }

        const double btagsfw = p_data / p_mc;
        h_btagsfweight->Fill(btagsfw);
        w *= btagsfw;
      }

      if (nr.is_mc() && use_extra_weights) {
        for (const auto& name : extra_weights_hists) {
          TH1D* hw = (TH1D*)extra_weights->Get(name.c_str());
          assert(hw);
          const double v =
            name == "nocuts_npv_den" ? pvs.n() :
            name == "nocuts_pvz_den" ? pvs.z(0) :
            name == "nocuts_pvx_den" ? pvs.x(0) :
            name == "nocuts_pvy_den" ? pvs.y(0) :
            name == "nocuts_nalltracks_den" ? nt.tm().nalltracks() :
            name == "nocuts_npv_den_redo" ? pvs.n() :
            name == "nocuts_ht_den" ? jets.ht() :
            name == "nocuts_pvndof_den" ? pvs.ndof(0) :
            -1e99;
          assert(v > -1e98);
          const int bin = hw->FindBin(v);
          if (bin >= 1 && bin <= hw->GetNbinsX())  
            w *= hw->GetBinContent(bin);
        }
      }
    }

    const TVector3& move_vector = nt.move_vector();
    const double movedist2 = move_vector.Perp();
    const double movedist3 = move_vector.Mag();
    const double movevectoreta = move_vector.Eta();
    const int nseedtracks = tks.nseed(bs);
    int n_movedseedtks = 0;
    int n_movedseedtks0 = 0;
    int n_movedmuseedtks = 0;
    int n_movedeleseedtks = 0;
    int n_movedtks = 0;
    double n_misccloseseedtks = 0;
    double n_closeseedtks = 0;
    int n_tightcloseseedtks = 0;
    int n_movedcloseseedtks = 0;
    int n_movedvtxseedtks = 0;
    const float  close_criteria = 5.0;  // How close must a seed track pass near an SV to be considered 'close?'
    const float  tight_close_criteria = 2.0;  // How close must a seed track pass near an SV to be considered 'close?'
    // First part of the preselection: our offline jet requirements
    // (mostly applied in ntupling step) plus only look at move
    // vectors ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't exact
    //if (movedist2 < 0.01 || movedist2 > 2.0) //old cuts 
    if (movedist2 > 2.4) //FIXME
      NR_loop_cont(w);

    int nselmuons = 0;
    double muon_pT = -99;
    double muon_p = -99;
    double muon_q = -99;
    double muon_px = -99;
    double muon_py = -99;
    double muon_pz = -99;
    double muon_abseta = -99;	 
    double muon_iso = 99;
    double muon_absdxybs = -99;
    double muon_absdz = -99;
    double muon_nsigmadxybs = -99;
    TLorentzVector muon_p4;
    TLorentzVector tmpz_p4;
    TLorentzVector zmumu_p4;
    TLorentzVector zee_p4;
    bool has_Zmumuboson = false;
    bool has_Zeeboson = false;
    // bool has_Wboson = false;


    for (int i = 0, ie = muons.n(); i < ie; ++i) {
      double tmp_muon_absdxybs = abs(muons.dxybs(i, bs));
      double tmp_muon_absdz = muons.dzpv(i, pvs);
      bool muon_IP_cut = tmp_muon_absdxybs < 0.02 && tmp_muon_absdz < 0.5;
      if (muon_IP_cut && muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
        nselmuons += 1;
        if (nselmuons == 1) {
          muon_pT = muons.pt(i);
          muon_p = muons.p(i);
          muon_px = muons.px(i);
          muon_py = muons.py(i);
          muon_pz = muons.pz(i);
          muon_p4.SetPxPyPzE(muon_px, muon_py, muon_pz, muon_p);
          muon_q = muons.q(i);
          muon_abseta = abs(muons.eta(i));
          muon_absdxybs = abs(muons.dxybs(i, bs));
          muon_absdz =  muons.dzpv(i, pvs);
          muon_iso = muons.iso(i);
          muon_nsigmadxybs = muons.nsigmadxybs(i, bs);
          tmpz_p4 += muon_p4;

        }
        if (has_Zmumuboson == false && nselmuons > 0 && muon_q * muons.q(i) == -1) {
          TLorentzVector antimuon_p4;
          antimuon_p4.SetPxPyPzE(muons.px(i), muons.py(i), muons.pz(i), muons.p(i));
          tmpz_p4 += antimuon_p4;
          has_Zmumuboson = true; 
        }
      }
    }

    double z_m = -99; //, zmumu_m = -99; 
    double z_pT = -99; //, zmumu_pT = -99;
    if (has_Zmumuboson) {
      //zmumu_m = tmpz_p4.M();
      //zmumu_pT = tmpz_p4.Pt();
      zmumu_p4 = tmpz_p4;
    }

    int nseleles = 0;
    double ele_pT = -99;
    double ele_p = -99;
    double ele_q = -99;
    double ele_px = -99;
    double ele_py = -99;
    double ele_pz = -99;
    double ele_abseta = -99;
    double ele_iso = 99;
    double ele_absdxybs = -99;
    double ele_absdz = -99;
    double ele_nsigmadxybs = -99;
    TLorentzVector ele_p4;
    tmpz_p4.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);

    for (int i = 0, ie = electrons.n(); i < ie; ++i) {
      double tmp_ele_abseta = abs(electrons.eta(i));
      double tmp_ele_absdxybs = abs(electrons.dxybs(i, bs));
      double tmp_ele_absdz = electrons.dzpv(i, pvs);  
      bool ele_IP_cut = tmp_ele_abseta < 1.48 ? tmp_ele_absdxybs < 0.05 && tmp_ele_absdz < 0.1 : tmp_ele_absdxybs < 0.1 && tmp_ele_absdz < 0.2;
      if (ele_IP_cut && electrons.pt(i) > 20.0 && abs(electrons.eta(i)) < 2.4 && electrons.isTight(i) && electrons.passveto(i) && electrons.iso(i) < 0.1) {
        nseleles += 1;
        if (nseleles == 1) {
          ele_pT = electrons.pt(i);
          ele_p = electrons.p(i);
          ele_px = electrons.px(i);
          ele_py = electrons.py(i);
          ele_pz = electrons.pz(i);
          ele_abseta = abs(electrons.eta(i));
          ele_absdxybs = abs(electrons.dxybs(i, bs));
          ele_absdz = electrons.dzpv(i, pvs);
          ele_p4.SetPxPyPzE(ele_px, ele_py, ele_pz, ele_p);
          ele_q = electrons.q(i);
          ele_iso = electrons.iso(i);
          ele_nsigmadxybs = electrons.nsigmadxybs(i, bs);
          tmpz_p4 += ele_p4;

        }

        if ( has_Zeeboson == false && nseleles > 0 && ele_q * electrons.q(i) == -1) {
          TLorentzVector antiele_p4;
          antiele_p4.SetPxPyPzE(electrons.px(i), electrons.py(i), electrons.pz(i), electrons.p(i));
          tmpz_p4 += antiele_p4;
          has_Zeeboson = true;
        }
      }
    }

    double met_pT = std::hypot(pf.met_x(), pf.met_y());
    TLorentzVector met_p4;
    met_p4.SetPtEtaPhiM(met_pT, 0, pf.met_phi(), 0);
    double lnu_absphi = -99, ljet_absdr = -99, ljet0_absdr = -99, nujet0_absphi = -99; // ljet1_absdr = -99,  nujet1_absphi = -99;
    double w_mT = -99; //, zee_m = -99;
    double w_pT = -99; //, zee_pT = -99;
    TLorentzVector w_p4;

    if (met_p4.Pt() > 25) {
      if (nselmuons && !has_Zmumuboson) {
        // has_Wboson = true;
        w_p4 = met_p4 + muon_p4;
        w_pT = w_p4.Pt();
        lnu_absphi = abs(muon_p4.DeltaPhi(met_p4));
        w_mT = sqrt(2 * muon_pT * met_pT * (1 - cos(muon_p4.DeltaPhi(met_p4))));
      }
      else if (nseleles > 0 && nselmuons == 0 && !has_Zeeboson) {
        // has_Wboson = true;
        w_p4 = met_p4 + ele_p4;
        w_pT = w_p4.Pt();
        lnu_absphi = abs(ele_p4.DeltaPhi(met_p4));
        w_mT = sqrt(2 * muon_pT * met_pT * (1 - cos(muon_p4.DeltaPhi(met_p4))));
      }
    }
    if (has_Zeeboson) {
      // zee_m = tmpz_p4.M();
      // zee_pT = tmpz_p4.Pt();
      zee_p4 = tmpz_p4;
    }

    //now we are looking at the moved jets (and leptons) specifically 
    auto nps = [&](const int k) { return tks.pass_seed(k, bs); };
    int nmovedjets = 0, jet_sumntracks = 0;
    //for jet+lep studies; these movedele and movedmu have passed hlt (not yet pt...) 
    int nmovedele = 0;
    int nmovedmu = 0;

    //FIXME : these should be with regards to jet_mu, jet_ele pairs -- should it be split by lep? or combined? 
    // not yet changing name to be easier 
    int jet_sumseedtracks = 0;
    double jet_sume = 0;
    double jetlep_dravg = 0, jetlep_detaavg = 0, jetlep_dphiavg = 0;
    double jetlep_drmax = 0, jetlep_detamax = 0, jetlep_dphimax = 0;

    double jetlep_a3dmax = 0;
    // int jet_0 = -1; // keep track of the pair of jets with largest 3D angle // JMTBAD should this be largest phi?
    int jetmu_i[2] = {-1,-1}; // keep track of the pair of jets with largest 3D angle // JMTBAD should this be largest phi? ALSO FIXME - 0th is jet, 1st is lep
    int jetele_i[2] = {-1,-1}; // keep track of the pair of jets with largest 3D angle // JMTBAD should this be largest phi? ALSO FIXME - 0th is jet, 1st is lep
    bool lep_ismu = false; //keep track of which lep is chosen w/ the jet to form the largest 3D angle -- only one can be true 
    bool lep_isele = false; //keep track of which lep is chosen w/ the jet to form the largest 3D angle -- only one can be true

    // 
    for (int i = 0, ie = jets.n(); i < ie; ++i) {
      if (!nt.jet_moved(i)) continue;
      const auto i_p4 = jets.p4(i);
      ++nmovedjets;
      jet_sume += jets.energy(i);
      jet_sumntracks += jets.ntracks(i);
      const std::vector<int> jet_tk_list = tks.tks_for_jet(i);
      jet_sumseedtracks += std::count_if(jet_tk_list.begin(), jet_tk_list.end(), nps);
      // jet_0 = i;
      for (int j=0, ee = electrons.n(); j < ee; ++j) { 
        if (!nt.electron_moved(j)) continue;
        ++nmovedele;
        const auto e_p4 = electrons.p4(j);
        // std::cout << "moved electron pt : " << e_p4.Pt() << std::endl;
        const double dr = i_p4.DeltaR(e_p4);
        const double deta = i_p4.Eta() - e_p4.Eta();
        const double dphi = i_p4.DeltaPhi(e_p4);
        jetlep_dravg += dr;
        jetlep_detaavg += deta;
        jetlep_dphiavg += dphi;
        if (dr > jetlep_drmax)
          jetlep_drmax = dr;
        if (fabs(deta) > fabs(jetlep_detamax))
          jetlep_drmax = dr;
        if (fabs(dphi) > fabs(jetlep_dphimax))
          jetlep_dphimax = dphi;

        const double a3d = i_p4.Angle(e_p4.Vect());
        if (a3d > jetlep_a3dmax){
          jetlep_a3dmax = a3d;
          jetele_i[0] = i;
          jetele_i[1] = j;
          // std::cout << "found an electron - jet pair" << std::endl;
          lep_isele = true;
          if (lep_ismu) lep_ismu = false; //flip to false since found a better pair w/ electron
        }
      }
      for (int j=0, mm = muons.n(); j < mm; ++j) { 
        if (!nt.muon_moved(j)) continue;
        ++nmovedmu;
        const auto m_p4 = muons.p4(j);
        // std::cout << "moved muon pt : " << m_p4.Pt() << std::endl;

        const double dr = i_p4.DeltaR(m_p4);
        const double deta = i_p4.Eta() - m_p4.Eta();
        const double dphi = i_p4.DeltaPhi(m_p4);
        jetlep_dravg += dr;
        jetlep_detaavg += deta;
        jetlep_dphiavg += dphi;
        if (dr > jetlep_drmax)
          jetlep_drmax = dr;
        if (fabs(deta) > fabs(jetlep_detamax))
          jetlep_drmax = dr;
        if (fabs(dphi) > fabs(jetlep_dphimax))
          jetlep_dphimax = dphi;

        const double a3d = i_p4.Angle(m_p4.Vect());
        if (a3d > jetlep_a3dmax){
          jetlep_a3dmax = a3d;
          jetmu_i[0] = i;
          jetmu_i[1] = j;
          // std::cout << "found a muon - jet pair" << std::endl;
          lep_ismu = true;
          if (lep_isele) lep_isele = false; //flip to false since found a better pair w/ muon
        }
      }
    }


    int nmovedjetlep = nmovedjets + nmovedele + nmovedmu;
    const int nmovedpairs = nmovedjetlep*(nmovedjetlep-1)/2; 
    jetlep_detaavg /= nmovedpairs;
    jetlep_dphiavg /= nmovedpairs;
    jetlep_dravg /= nmovedpairs;

    int jet0_ntracks = 0;
    // int jet0_nseedtracks = 0;
    TLorentzVector jet0_p4;
    double jet0_max_trackpair_dr = 0;
    double jet0_avg_trackpair_dr = 0;
    double jet0_pt = 0;
    double jet0_eta = 0;
    double jet0_phi = 0;
    double jet0_p = 0;
    double jet0_mv_deta = 0;
    double jet0_mv_dphi = 0;
    double jet0_mv_a3d = 0;

    TLorentzVector mu1_p4;
    double mu1_pt = 0;
    double mu1_eta = 0;
    double mu1_phi = 0;
    double mu1_p = 0;
    double mu1_mv_deta = 0;
    double mu1_mv_dphi = 0;
    double mu1_mv_a3d = 0;

    TLorentzVector ele1_p4;
    double ele1_pt = 0;
    double ele1_eta = 0;
    double ele1_phi = 0;
    double ele1_p = 0;
    double ele1_mv_deta = 0;
    double ele1_mv_dphi = 0;
    double ele1_mv_a3d = 0;


    int ll = -1;
    int jj = -1; 
    if (lep_isele > 0) { 
      ll = jetele_i[1]; //the lep
      jj = jetele_i[0];
    }
    if (lep_ismu > 0) {
      ll = jetmu_i[1]; //the lep
      jj = jetmu_i[0];
    }
    // std::cout << "is the lepton an ele ? or mu ? " << lep_isele << " " << lep_ismu << std::endl;
    // std::cout << "ll : " << ll << " and jj : " << jj << std::endl;
    // std::cout << "size of jets : " << jets.n() << std::endl;
    // std::cout << "size of muon : " << muons.n() << std::endl;
    // std::cout << "size of ele : " << electrons.n() << std::endl;


    //there is a new requirement that the jet is moved only if it is within 1mm of the lepton in dz. therefore, now need an if statement to protect cases when no jet is moved. 
    std::vector<int> jet0_tracks;

    if (jj != -1) { 
      jet0_tracks = tks.tks_for_jet(jj);
      jet0_ntracks = jets.ntracks(jj);
      // jet0_nseedtracks = std::count_if(jet0_tracks.begin(), jet0_tracks.end(), nps);
      jet0_pt = jets.pt(jj);
      jet0_eta = jets.eta(jj);
      jet0_phi = jets.phi(jj);
      auto p4 = jet0_p4 = jets.p4(jj);
      jet0_p = jet0_p4.P();
      // if (jet0_pt != jet0_p4.Pt()) std::cout << "Difference seen in jet pT : " << jet0_pt << " " << jet0_p4.Pt() << std::endl;
      jet0_mv_deta = fabs(move_vector.Eta() - p4.Eta());
      jet0_mv_dphi = move_vector.DeltaPhi(p4.Vect());
      jet0_mv_a3d = move_vector.Angle(p4.Vect());
      const int ntk = jet0_tracks.size();
      for (int j = 0; j < ntk; ++j)
        for (int k = j+1; k < ntk; ++k) {
          const double dr = tks.p3(jet0_tracks[j]).DeltaR(tks.p3(jet0_tracks[k]));
          jet0_avg_trackpair_dr += dr;
          if (dr > jet0_max_trackpair_dr)
            jet0_max_trackpair_dr = dr;
        }
      jet0_avg_trackpair_dr /= ntk*(ntk-1)/2;
    }

    if (lep_ismu > 0) {
      // mu1_p4 = muons.p4(ll);
      mu1_pt = muons.pt(ll);
      mu1_eta = muons.eta(ll);
      mu1_phi = muons.phi(ll);
      auto mp4 = mu1_p4 = muons.p4(ll);
      mu1_p = mu1_p4.P();
      mu1_mv_deta = fabs(move_vector.Eta() - mp4.Eta());
      mu1_mv_dphi = move_vector.DeltaPhi(mp4.Vect());
      mu1_mv_a3d = move_vector.Angle(mp4.Vect());
    }
    if (lep_isele > 0) { 
      // ele1_p4 = electrons.p4(ll);
      ele1_pt = electrons.pt(ll);
      ele1_eta = electrons.eta(ll);
      ele1_phi = electrons.phi(ll);
      auto ep4 = ele1_p4 = electrons.p4(ll);
      ele1_p = ele1_p4.P();
      ele1_mv_deta = fabs(move_vector.Eta() - ep4.Eta());
      ele1_mv_dphi = move_vector.DeltaPhi(ep4.Vect());
      ele1_mv_a3d = move_vector.Angle(ep4.Vect());
    }

    // const std::vector<int> jet0_tracks = tks.tks_for_jet(jj);
    std::vector<int> closeseedtrk_idx;
    std::vector<int> jet0trk_idx;
    int jet_ntk_0 = 0;
    double sump_0 = 0;
    double miscp = 0;
    double maxeta_0 = 0.0;
    double maxeta_1 = 0.0;

    int mu1trk_idx = -1; 
    int ele1trk_idx = -1;
    double mup_1 = 0;
    double elep_1 = 0;

    for (int j = 0; j < tks.n(); ++j) {
      if (nt.tk_moved(j) || nt.mtk_moved(j) || nt.etk_moved(j))
        // printf("track %i: pt: %10.3f eta: %10.3f phi: %10.3f pass sel? : %d tk_moved? : %d  mu track moved? : %d  ele track moved? : %d \n", j, tks.pt(j), tks.eta(j), tks.phi(j), tks.pass_sel(j), nt.tk_moved(j), nt.mtk_moved(j), nt.etk_moved(j) );

      const TLorentzVector jp4 = tks.p4(j);
      auto it0 = std::find(jet0_tracks.begin(), jet0_tracks.end(), j);
      if (it0 != jet0_tracks.end() && tks.pass_sel(j) && nt.tk_moved(j)){
        jet0_p4 += tks.p4(j);
        jet_ntk_0 += 1;
        jet0trk_idx.push_back(j);
        sump_0+=tks.p(j);
        n_movedtks++;
        if (fabs(tks.eta(j)) > fabs(maxeta_0)) maxeta_0 = tks.eta(j);
        if (tks.pass_seed(j, bs)){
          n_movedseedtks++;
          n_movedseedtks0++;
        }
      }
      if (tks.pass_sel(j) && nt.mtk_moved(j)){
        //make certain its the same as the moved muon (above) --do the check when needed
        // double dr = tks.p4(j).DeltaR(mu1_p4); 
        // std::cout << "moved muon : " << mu1_p4.Phi() << " " << mu1_p4.Eta() << std::endl;
        // std::cout << "moved track : " << tks.phi(j) << " " << tks.eta(j) << std::endl;

        // if (dr > 0.1) std::cout << "MISMATCH MOVED TRACK - MUON " << dr << std::endl;
        mu1trk_idx = j;
        mup_1 = tks.p(j);
        if (fabs(tks.eta(j)) > fabs(maxeta_1)) maxeta_1 = tks.eta(j);
        if (tks.pass_seed(j, bs)) {
          n_movedseedtks++;
          n_movedmuseedtks++;

        }
      }
      if (tks.pass_sel(j) && nt.etk_moved(j)){
        //make certain its the same as the moved electron (above) 
        // double dr = reco::deltaR(ep4.Phi(), tks.phi(j), ep4.Eta(), tks.eta(j));
        // double dr = tks.p4(j).DeltaR(ele1_p4); 

        // if (dr > 0.1) std::cout << "MISMATCH MOVED TRACK - ELECTRON " << dr << std::endl;
        ele1trk_idx = j;
        elep_1 = tks.p(j);
        if (fabs(tks.eta(j)) > fabs(maxeta_1)) maxeta_1 = tks.eta(j);
        if (tks.pass_seed(j, bs)) {
          n_movedseedtks++;
          n_movedeleseedtks++;

        }
      }
    }
    // std::cout << "nmoved ele(mu) seedtracks " << n_movedeleseedtks << " , " << n_movedmuseedtks << std::endl;
    // std::cout << "nmoved ele(mu)  " << nmovedele << " , " << nmovedmu << std::endl;

    //start 
    TVector3 lspdecaybsp(nt.tm().move_x(), nt.tm().move_y() , nt.tm().move_z());  // JMTBAD BS BS
    double decay_radius = lspdecaybsp.Perp();
    double qrk0_dxybs = decay_radius*sin(jet0_mv_dphi);
    double mu1_dxybs = decay_radius*sin(mu1_mv_dphi);
    double ele1_dxybs = decay_radius*sin(ele1_mv_dphi);
    double jet0_dxybs = decay_radius*sin(jet0_mv_dphi);
    // double jet1_dxybs = decay_radius*sin(jet0_mv_dphi[1]);
    
    for (int j = 0; j < tks.n(); ++j){
        //if (tks.pass_seed(j, bs) && nt.tk_moved(j)) n_movedseedtks++;
        if (tks.pass_seed(j,bs)){
            const double temp_sigdxy = tks.dxy(j, nt.tm().move_x() + bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()))/tks.err_dxy(j);
            const double temp_sigdz  = tks.dz(j, nt.tm().move_x() + bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(j);
            const double sum_sq_sig = hypot(temp_sigdxy, temp_sigdz);
            const double sigs_quad = sum_sq_sig;
        
            // Count how many 'close' seed tracks there are
            if ( sigs_quad < close_criteria){
              n_closeseedtks++;
              closeseedtrk_idx.push_back(j);
              auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), j);
              if (it0 != jet0trk_idx.end()){
                n_movedcloseseedtks++;
              }
              else if (j == mu1trk_idx || j == ele1trk_idx){
                n_movedcloseseedtks++;
              }
              else{
                n_misccloseseedtks++;
                miscp += tks.p(j);
              }
            }
            if ( sigs_quad < tight_close_criteria){
              n_tightcloseseedtks++;
            }
        }
    }

    //for (size_t j = 0; j < jet1trk_idx.size(); ++j)
    //    if (tks.pass_seed(jet1trk_idx[j], bs) && nt.tk_moved(jet1trk_idx[j])) n_movedseedtks++;
    double jetele_asymm = -999.0;
    double jetele_dr = -999.0;
    double jetele_costheta = -999.0;
    double jetele_dphi = -999.0;
    double jetele_deta = -999.0;
    double jetele_mv_dphi_sum = -999.0;
    double jetele_mv_deta_sum = -999.0;

    double jetmu_asymm = -999.0;
    double jetmu_dr = -999.0;
    double jetmu_costheta = -999.0;
    double jetmu_dphi = -999.0;
    double jetmu_deta = -999.0;
    double jetmu_mv_dphi_sum = -999.0;
    double jetmu_mv_deta_sum = -999.0;
    //duplicate for jet-lep case : 
    if (lep_isele > 0) { 
      jetele_asymm = (jet0_p4.Pt() - ele1_p4.Pt()) / (jet0_p4.Pt() + ele1_p4.Pt());
      jetele_dr = jet0_p4.DeltaR(ele1_p4); 
      jetele_costheta = ((jet0_p4.X()*ele1_p4.X()) + (jet0_p4.Y()*ele1_p4.Y()) + (jet0_p4.Z()*ele1_p4.Z()))/(jet0_p4.P()*ele1_p4.P()); 
      jetele_dphi = jet0_p4.DeltaPhi(ele1_p4); 
      jetele_deta = fabs(jet0_p4.Eta() - ele1_p4.Eta()); 
      // const double jetele_dind = fabs(jetele_i[1] - jetele_i[0]);
      jetele_mv_dphi_sum = move_vector.DeltaPhi((jet0_p4 + ele1_p4).Vect());
      jetele_mv_deta_sum = fabs((jet0_p4 + ele1_p4).Eta() - move_vector.Eta());
    }
    if (lep_ismu > 0) { 
      jetmu_asymm = (jet0_p4.Pt() - mu1_p4.Pt()) / (jet0_p4.Pt() + mu1_p4.Pt());

      jetmu_dr = jet0_p4.DeltaR(mu1_p4); 
      jetmu_costheta = ((jet0_p4.X()*mu1_p4.X()) + (jet0_p4.Y()*mu1_p4.Y()) + (jet0_p4.Z()*mu1_p4.Z()))/(jet0_p4.P()*mu1_p4.P()); 
      jetmu_dphi = jet0_p4.DeltaPhi(mu1_p4); 
      jetmu_deta = fabs(jet0_p4.Eta() - mu1_p4.Eta()); 
      // const double jetmu_dind = fabs(jetmu_i[1] - jetmu_i[0]);
      jetmu_mv_dphi_sum = move_vector.DeltaPhi((jet0_p4 + mu1_p4).Vect());
      jetmu_mv_deta_sum = fabs((jet0_p4 + mu1_p4).Eta() - move_vector.Eta());
    }


    // double wjet_dphi = w_p4.DeltaPhi(jet0_p4[0] + jet0_p4[1]);
    // if (!has_Wboson) wjet_dphi = 99;
    // double zjet_dphi = 99;
    // if (has_Zmumuboson){
    //   zjet_dphi = zmumu_p4.DeltaPhi(jet0_p4[0] + jet0_p4[1]);
    //   z_m = zmumu_m;
    //   z_pT = zmumu_pT;
    // }
    // else if (has_Zeeboson){
    //   zjet_dphi = zee_p4.DeltaPhi(jet0_p4[0] + jet0_p4[1]);
    //   z_m = zee_m;
    //   z_pT = zee_pT;
    // }
    // if (met_p4.Pt() > 25){
    //   if (nselmuons > 0) {
    //     ljet_absdr = abs(muon_p4.DeltaR(jet0_p4[0])) < abs(muon_p4.DeltaR(jet0_p4[1])) ? abs(muon_p4.DeltaR(jet0_p4[0])) : abs(muon_p4.DeltaR(jet0_p4[1]));
    //     ljet0_absdr = abs(muon_p4.DeltaR(jet0_p4[0]));
    //     ljet1_absdr = abs(muon_p4.DeltaR(jet0_p4[1]));
    //   }
    //   else if ( nseleles > 0 && nselmuons == 0) {
    //     ljet_absdr = abs(ele_p4.DeltaR(jet0_p4[0])) < abs(ele_p4.DeltaR(jet0_p4[1])) ? abs(ele_p4.DeltaR(jet0_p4[0])) : abs(ele_p4.DeltaR(jet0_p4[1]));
    //     ljet0_absdr = abs(ele_p4.DeltaR(jet0_p4[0]));
    //     ljet1_absdr = abs(ele_p4.DeltaR(jet0_p4[1]));
    //   }
    //   nujet0_absphi = abs(met_p4.DeltaPhi(jet0_p4[0]));
    //   nujet1_absphi = abs(met_p4.DeltaPhi(jet0_p4[1]));
    // }



    // const double jet_nseedtracks_max = std::max(jet_nseedtracks[0], jet_nseedtracks[1]);
    // const double jet_nseedtracks_min = std::min(jet_nseedtracks[0], jet_nseedtracks[1]);

    //presel cuts
    //if (jet_ntk_0 < 1 || jet_ntk_1 < 1) // || jet_ntk_0 + jet_ntk_1 < 5)
    //    NR_loop_cont(w);
  
    //wrong 
    // if (nr.is_mc() && use_extra_weights) {
    //   for (const auto& name : extra_weights_hists) {
    //     TH1D* hw = (TH1D*)extra_weights->Get(name.c_str());
    //     std::cout << name << std::endl;
    //     assert(hw);
    //     // const double v =
    //     //   name == "nocuts_npv_den" ? pvs.n() :
    //     //   name == "nocuts_pvz_den" ? pvs.z(0) :
    //     //   name == "nocuts_pvx_den" ? pvs.x(0) :
    //     //   name == "nocuts_pvy_den" ? pvs.y(0) :
    //     //   name == "nocuts_nalltracks_den" ? nt.tm().nalltracks() :
    //     //   name == "nocuts_npv_den_redo" ? pvs.n() :
    //     //   name == "nocuts_ht_den" ? jets.ht() :
    //     //   name == "nocuts_pvndof_den" ? pvs.ndof(0) :
    //     //   -1e99;
    //     // assert(v > -1e98);
    //     double v = -1e99;
    //     if (name == "nocuts_jet0_sump_den") v= sump_0;
    //     if (name == "nocuts_jetele_dr_den" && lep_isele) v = jetele_dr;
    //     if (name == "nocuts_jetmu_dr_den" && lep_ismu) v = jetmu_dr;
    //     if (name == "nocuts_ele1_p_den" && lep_isele) v = ele1_p;
    //     if (name == "nocuts_mu1_p_den" && lep_ismu) v = mu1_p;
    //     if (v == -1e99) continue; //do not weigh the electron p, dr when there is a muon and vise versa 
    //     assert(v > -1e98);
    //     const int bin = hw->FindBin(v);
    //     if (bin >= 1 && bin <= hw->GetNbinsX())  
    //       w *= hw->GetBinContent(bin);
    //   }
    // }

    if (jetlep_kin_weights){
      TFile* jetlep_weights_1d_kin = TFile::Open(w_fn_1d_kin_ar);

      for (const auto& name : jetlep_1d_kin_weights_hists) {
        double v = -1e99;
        // std::cout << name << " and what lepton? " << lep_ismu << std::endl;
        // if (name == "nocuts_jetmu_dr_den" && lep_ismu)
        //   v = jetmu_dr;
        // else if (name == "nocuts_jetele_dr_den" && lep_isele)
        //   v = jetele_dr;
        // else if (name == "nocuts_mu1_p_den" && lep_ismu)
        //   v = mu1_p;
        // else if (name == "nocuts_ele1_p_den" && lep_isele)
        //   v = ele1_p;
        // if (name == "nocuts_jet0_sump_den")
        //   v = sump_0;

        // if (name == "nocuts_mupt1_den" && lep_ismu)
        //   v = mu1_pt;
        // else if (name == "nocuts_elept1_den" && lep_isele)
        //   v = ele1_pt;
        if (name == "nocuts_pt0_den")
          v = jet0_pt;

        if (v == -1e99) {
          // std::cout << "there's a mismatch so let's continue "<< std::endl;
          continue; //if the lepton was an electron, skip the weights from mu hists and vise versa 
        }
        assert(v > -1e98);
        TH1D* hw = (TH1D*)jetlep_weights_1d_kin->Get(name.c_str());
        assert(hw);
        const int bin = hw->FindBin(v);
        if (bin >= 1 && bin <= hw->GetNbinsX())
          w *= hw->GetBinContent(bin);
        
      }
      jetlep_weights_1d_kin->Close();
    }

    if (jet_decay_weights) {
      TFile* jet_weights_2d_move = TFile::Open(w_fn_2d_move_ar);
      TFile* jet_weights_2d_kin = TFile::Open(w_fn_2d_kin_ar);
      // TFile* jet_weights_2d_ang = TFile::Open(w_fn_2d_ang_ar);

      for (const auto& name : jet_2d_move_weights_hists) {
         double vx = -1e99;
         double vy = -1e99;
         if (name == "nocuts_movedist3_movedist2_den"){
         vx = movedist3;
         vy = movedist2;
         }
         TH2D* hw = (TH2D*)jet_weights_2d_move->Get(name.c_str());
         assert(hw);
         int bin = hw->FindBin(vx, vy);
         if (bin >= 1 && bin <= hw->GetNcells()){
         w *= hw->GetBinContent(bin);
         }
      }
      for (const auto& name : jet_2d_kin_weights_hists) {
         double vx = -1e99;
         double vy = -1e99;
         
        //  if (name == "nocuts_llp_sump_jetdr_den"){
        // //  vx = sump_0 + sump_1 + miscp;  //FIXME
        //  vx = sump_0 + miscp;
        // //  vy = jet_dr;
        //  }

        //trial 1
        //  if (name == "nocuts_jet0_sump_jetlepdr_den"){
        //   vx = sump_0;
        //   if (lep_isele) vy = jetele_dr;
        //   if (lep_ismu)  vy = jetmu_dr;
        //  }
         if (name == "nocuts_lep1_pT_jetdr_den"){
          if (lep_isele) {
            vx = ele1_pt;
            vy = jetele_dr;
          }
          if (lep_ismu)  {
            vx = mu1_pt;
            vy = jetmu_dr;
          }
         }
        
        //  if (name == "nocuts_jet0_sump_lep1_p_den"){
        //   vx = sump_0;
        //   if (lep_isele) vy = ele1_p;
        //   if (lep_ismu)  vy = mu1_p;
        //  }

        // if (name == "nocuts_mu1_p_eta_den" && lep_ismu){
        //   vx = mu1_p;
        //   vy = mu1_eta;
        // }
        // if (name == "nocuts_ele1_p_eta_den" && lep_isele){
        //   vx = ele1_p;
        //   vy = ele1_eta;
        // }

         TH2D* hw2 = (TH2D*)jet_weights_2d_kin->Get(name.c_str());
         assert(hw2);
         int bin = hw2->FindBin(vx, vy);
         if (bin >= 1 && bin <= hw2->GetNcells()){
         w *= hw2->GetBinContent(bin);
         }
      }

    //   for (const auto& name : jet_2d_ang_weights_hists) {
    //     double vx = -1e99;
    //     double vy = -1e99;

    //     if (name == "nocuts_jetlep_deta_dphi_den"){
    //      if (lep_isele) {
    //       vx = jetele_deta;
    //       vy = jetele_dphi;
    //      }
    //      if (lep_ismu) {
    //       vx = jetmu_deta;
    //       vy = jetmu_dphi;
    //      }
    //     }
        
    //     TH2D* hw2 = (TH2D*)jet_weights_2d_ang->Get(name.c_str());
    //     assert(hw2);
    //     int bin = hw2->FindBin(vx, vy);
    //     if (bin >= 1 && bin <= hw2->GetNcells()){
    //     w *= hw2->GetBinContent(bin);
    //     }
    //  }
      jet_weights_2d_move->Close();
      jet_weights_2d_kin->Close();
      // jet_weights_2d_ang->Close();
    }
  
    const int nvtx = vs.n();
    std::vector<double> vtxs_anglemax(nvtx, 0);
    /*
    for (int i = 0; i < nvtx; ++i) {
      const std::vector<int> tracks = tks.tks_for_sv(i);
      const int ntracks = int(tracks.size());
      assert(vs.ntracks(i) == ntracks);

      for (int j = 0; j < ntracks; ++j) {
        const TVector3 jp = tks.p3(tracks[j]);
        for (int k = j+1; k < ntracks; ++k) {
          const TVector3 kp = tks.p3(tracks[k]);
          const double angle = jp.Angle(kp); // JMTBAD probably should tighten cuts on tracks used for this
          if (angle > vtxs_anglemax[i])
            vtxs_anglemax[i] = angle;
        }
      }
    }
    */

  //  if (lep_ismu) { 
  //   std::cout << "jetmu aj check (jet pt, mu pt, aj):  ( " << jet0_p4.Pt() << " " << mu1_p4.Pt() << " " << jetmu_asymm << " )" << std::endl;
  //   std::cout << "w : " << w << std::endl;
  //  }

    //TODO : DO I NEED THESE ?!?
    // std::cout << "cuts ... " << nmovedmu << " " << nmovedele << " " << jetele_dr << " " << jetmu_dr << " " << jet0_eta << " " << mu1_eta << " " << ele1_eta << " " << std::endl;
    // std::cout << " movedlepton track idx : " << mu1trk_idx << " " << ele1trk_idx << std::endl;

    // if ( (nselmuons < 1) && (nseleles < 1))
    //    NR_loop_cont(w);
    // not this... I need to have a moved muon or moved electron
    if ((nmovedele < 1) && (nmovedmu < 1))
      NR_loop_cont(w);
    
    //also need a moved muon / electron track -> this is in case there is a moved ele/mu but the corresponding track did not pass the track cuts
    if ((mu1trk_idx == -1) && (ele1trk_idx == -1))
      NR_loop_cont(w);

    //finally make certain that they are the same object : 


    //default is -999 so one will always be true
    if ( (fabs(jetele_dr) < 0.4) || (fabs(jetmu_dr) < 0.4) )
       NR_loop_cont(w); 
    

    //default is 0 so leaving it with or 
    if ((fabs(jet0_eta) > 1.5) || (fabs(mu1_eta) > 1.5) || (fabs(ele1_eta) > 1.5))
       NR_loop_cont(w);
    

    int n_pass_nocuts = 0;
    int n_pass_ntracks = 0;
    int n_pass_all = 0;
    double dist2move = -9.9;
    double dist2move2d = -9.9;
    jmt::MinValue dist2min(100);
    jmt::MinValue dist2min2d(100);
    double vtx_bs2derr = -9.9, vtx_eta = -9.9, vtx_z = -999.9, vtx_dbv = -999.9, vtx_chi2 = -999.9, vtx_3dbv = -999.9, vtx_ntk = -9; // JMTBAD ??? these end up with what???
    std::vector<int> first_vtx_to_pass(num_numdens, -1);
    auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };

    for (int ivtx = 0; ivtx < nvtx; ++ivtx) {
      dist2move = (vs.pos(ivtx) - nt.tm().move_pos()).Mag();
      dist2move2d = (vs.pos(ivtx) - nt.tm().move_pos()).Perp();
      dist2min(ivtx, dist2move);
      dist2min2d(ivtx, dist2move2d);
      if (dist2move > 0.0400) //FIXME 
        continue;

      vtx_bs2derr = vs.bs2derr(ivtx); // JMTBAD ???
      vtx_eta     = vs.eta(ivtx);
      vtx_z       = vs.z(ivtx);
      vtx_dbv     = vs.pos(ivtx).Perp();
      vtx_3dbv    = vs.pos(ivtx).Mag();
      vtx_ntk     = vs.ntracks(ivtx);
      vtx_chi2    = vs.chi2(ivtx)/vs.ndof(ivtx);
      // std::cout << "vtx i : bs2derr, ntracks, dbv " << ivtx << " " << vtx_bs2derr << " " << vtx_ntk << " " << vtx_dbv << std::endl;
      
      const bool pass_beams = vtx_dbv >= 0.0100 && vtx_dbv < 2.0;
      const bool pass_ntracks = vs.ntracks(ivtx) >= 4 && pass_beams; //CHANGE TO 4 FOR DISPLACED LEPTON ... 
      const bool pass_bs2derr = vs.bs2derr(ivtx) < 0.0050 && pass_beams; // JMTBAD use rescale_bs2derr and in plots below //FIXME 

      if (1)                            { set_it_if_first(first_vtx_to_pass[0], ivtx); ++n_pass_nocuts;  }
      if (pass_ntracks )                 { set_it_if_first(first_vtx_to_pass[1], ivtx); ++n_pass_ntracks; }
      if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], ivtx); ++n_pass_all;     }

      if (pass_ntracks && pass_bs2derr && nr.is_mc() && nr.use_weights() && ntks_weights)
        w *= ntks_weight(vs.ntracks(ivtx));
    }

    dist2move = dist2min.v();
    dist2move2d = dist2min2d.v();
    double mindist2move_iv = dist2min.i();
    if (mindist2move_iv != -1){
      vtx_bs2derr = vs.bs2derr(mindist2move_iv); // JMTBAD ???
      vtx_eta     = vs.eta(mindist2move_iv);
      vtx_z       = vs.z(mindist2move_iv);
      vtx_dbv     = vs.pos(mindist2move_iv).Perp();
      vtx_3dbv    = vs.pos(mindist2move_iv).Mag();
      vtx_ntk     = vs.ntracks(mindist2move_iv);
      vtx_chi2     = vs.chi2(mindist2move_iv)/vs.ndof(mindist2move_iv);
      const std::vector<int> its = tks.tks_for_sv(mindist2move_iv);
      for (int it : its){
        auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), it);
        // auto it1 = std::find(jet1trk_idx.begin(), jet1trk_idx.end(), it);
        if (it0 != jet0trk_idx.end()) n_movedvtxseedtks++;
        // if (it0 != jet0trk_idx.end() || it1 != jet1trk_idx.end()) n_movedvtxseedtks++;

      }
    }
    

    if (dist2move > 0.0400 && dist2move < 100) //FIXME 
      NR_loop_cont(w);

    // w now final and can count event toward denominator
    for (numdens& nd : nds)
      nd.setw(w);
    ++nden;
    den += w;
    if (w < 0) { ++nnegden; negden += w; }
    for (numdens& nd : nds) {
      nd.den(k_movedist2, movedist2);
      nd.den(k_movedist3, movedist3);
      nd.den(k_movevectoreta, movevectoreta);
      nd.den(k_npv, pvs.n());
      nd.den(k_pvx, pvs.x(0));
      nd.den(k_pvy, pvs.y(0));
      nd.den(k_pvz, pvs.z(0));
      nd.den(k_pvrho, pvs.rho(0));
      nd.den(k_pvntracks, pvs.ntracks(0));
      nd.den(k_pvscore, pvs.score(0));
      nd.den(k_ht, jets.ht());
      nd.den(k_njets, jets.n());
      nd.den(k_nmuons, nselmuons);
      nd.den(k_muon_pT, muon_pT);
      nd.den(k_muon_abseta, muon_abseta);
      nd.den(k_muon_iso, muon_iso);
      if (muon_iso != 0.0) nd.den(k_muon_zoom_iso, muon_iso);
      nd.den(k_muon_absdxybs, muon_absdxybs);
      nd.den(k_muon_absdz, muon_absdz);
      nd.den(k_muon_nsigmadxybs, muon_nsigmadxybs);
      nd.den(k_neles, nseleles);
      nd.den(k_ele_pT, ele_pT);
      nd.den(k_ele_abseta, ele_abseta);
      nd.den(k_ele_iso, ele_iso);
      if (ele_iso != 0.0) nd.den(k_ele_zoom_iso, ele_iso);
      nd.den(k_ele_absdxybs, ele_absdxybs);
      nd.den(k_ele_absdz, ele_absdz);
      nd.den(k_ele_nsigmadxybs, ele_nsigmadxybs);
      nd.den(k_met_pT, met_pT);
      nd.den(k_w_pT, w_pT);
      nd.den(k_w_mT, w_mT);
      nd.den(k_z_pT, z_pT);
      nd.den(k_z_m, z_m);
      nd.den(k_lnu_absphi, lnu_absphi);
      nd.den(k_ljet_absdr, ljet_absdr);
      nd.den(k_ljet0_absdr, ljet0_absdr);
      // nd.den(k_ljet1_absdr, ljet1_absdr);
      nd.den(k_nujet0_absphi, nujet0_absphi);
      // nd.den(k_nujet1_absphi, nujet1_absphi);
      // nd.den(k_wjet_dphi, fabs(wjet_dphi));
      // nd.den(k_zjet_dphi, fabs(zjet_dphi));

      nd.den(k_jet0_eta, jet0_eta);
      nd.den(k_pt0, jet0_pt);
      nd.den(k_ntks_j0, jet_ntk_0);
      nd.den(k_jet0_sump, sump_0);

      for (size_t j = 0; j < jet0trk_idx.size(); ++j){
        nd.den(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
        nd.den(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
        nd.den(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet0_vtxdz = tks.dz(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet0_vtxdxy = tks.dxy(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.den(k_jet0_trk_vtxdxy, jet0_vtxdxy);
          nd.den(k_jet0_trk_vtxdz, jet0_vtxdz);
          nd.den(k_jet0_trk_nsigmavtxdz, jet0_vtxdz/tks.err_dz(jet0trk_idx[j]));
          nd.den(k_jet0_trk_nsigmavtxdxy, jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]));
          nd.den(k_jet0_trk_nsigmavtx, sqrt((jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]))*(jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j])) + (jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))*(jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))));
        }
        nd.den(k_jet0_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
        const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet0trk_idx[j]);
        const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet0trk_idx[j]);  
        nd.den(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
        nd.den(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
        nd.den(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
        nd.den(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.den(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
        nd.den(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
        nd.den(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
      }

      if (lep_ismu > 0) {
        nd.den(k_jetmu_asymm, jetmu_asymm);
        nd.den(k_mu1_eta, mu1_eta); 
        nd.den(k_mu1_p_eta, mu1_p, mu1_eta);
        nd.den(k_lep1_p_eta, mu1_p, mu1_eta);
        nd.den(k_jetmu_dr, jetmu_dr); 
        nd.den(k_jetmu_costheta, jetmu_costheta); 
        nd.den(k_jetmu_deta, jetmu_deta); 
        nd.den(k_jetmu_dphi, jetmu_dphi); 
        nd.den(k_jetmu_deta_dphi, jetmu_deta, jetmu_dphi);
        nd.den(k_jetlep_deta_dphi, jetmu_deta, jetmu_dphi);
        nd.den(k_mupt1, mu1_pt); 

        nd.den(k_mu1_trk_pt, tks.pt(mu1trk_idx));
        // nd.den(k_mu1_p, tks.p(mu1trk_idx));
        nd.den(k_mu1_p, mu1_p);

        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          nd.den(k_mu1jet0_trk_dx, (tks.vx(mu1trk_idx) - tks.vx(jet0trk_idx[j])));
          nd.den(k_mu1jet0_trk_dy, (tks.vy(mu1trk_idx) - tks.vy(jet0trk_idx[j])));
          nd.den(k_mu1jet0_trk_dz, (tks.vz(mu1trk_idx) - tks.vz(jet0trk_idx[j])));
          nd.den(k_mu1jet0_trk_dist2d, (std::sqrt( pow(2.0, (tks.vx(mu1trk_idx) - tks.vx(jet0trk_idx[j])) ) + pow(2.0, (tks.vy(mu1trk_idx) - tks.vy(jet0trk_idx[j]))))));
        }

        nd.den(k_mu1_trk_eta, tks.eta(mu1trk_idx));
        nd.den(k_mu1_trk_dz, tks.dzpv(mu1trk_idx, pvs));
        if (mindist2move_iv != -1) {
          const double mu1_vtxdz = tks.dz(mu1trk_idx,vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double mu1_vtxdxy = tks.dxy(mu1trk_idx, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.den(k_mu1_trk_vtxdxy, mu1_vtxdxy);
          nd.den(k_mu1_trk_vtxdz, mu1_vtxdz);
          nd.den(k_mu1_trk_nsigmavtxdz, mu1_vtxdz/tks.err_dz(mu1trk_idx));
          nd.den(k_mu1_trk_nsigmavtxdxy, mu1_vtxdxy/tks.err_dxy(mu1trk_idx));
          nd.den(k_mu1_trk_nsigmavtx, sqrt((mu1_vtxdxy/tks.err_dxy(mu1trk_idx))*(mu1_vtxdxy/tks.err_dxy(mu1trk_idx)) + (mu1_vtxdz/tks.err_dz(mu1trk_idx))*(mu1_vtxdz/tks.err_dz(mu1trk_idx))));
        }
        nd.den(k_mu1_trk_dzerr, tks.err_dz(mu1trk_idx));
        const double mu1_gennsigmadz = tks.dz(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(mu1trk_idx);
        const double mu1_gennsigmamissdist = tks.dxy(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(mu1trk_idx);  
        nd.den(k_mu1_trk_gennsigma, sqrt((mu1_gennsigmamissdist*mu1_gennsigmamissdist) + (mu1_gennsigmadz*mu1_gennsigmadz)));
        nd.den(k_mu1_trk_gennsigmamissdist, mu1_gennsigmamissdist);
        nd.den(k_mu1_trk_genmissdist, tks.dxy(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_mu1_trk_gennsigmadz, mu1_gennsigmadz);
        nd.den(k_mu1_trk_gendz, tks.dz(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_mu1_trk_whichpv, tks.which_pv(mu1trk_idx));
        nd.den(k_mu1_trk_dsz, tks.dsz(mu1trk_idx, pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.den(k_mu1_trk_dxy, tks.dxybs(mu1trk_idx, bs));
        nd.den(k_mu1_trk_nsigmadxy, tks.dxybs(mu1trk_idx, bs)/tks.err_dxy(mu1trk_idx));
        nd.den(k_mu1_trk_dxyerr, tks.err_dxy(mu1trk_idx));
        
        nd.den(k_jet0_maxeta_mu1_eta, maxeta_0, mu1_eta);
        nd.den(k_jet0_sump_mu1_p, sump_0, mu1_p);
        nd.den(k_jet0_sump_lep1_p, sump_0, mu1_p);
        nd.den(k_jet0_sump_jetmudr, sump_0, jetmu_dr);
        nd.den(k_jet0_sump_jetlepdr, sump_0, jetmu_dr);
        nd.den(k_mu1_p_jetmudr, mu1_p, jetmu_dr);
        nd.den(k_lep1_p_jetlepdr, mu1_p, jetmu_dr);
        nd.den(k_mu1_pT_jetmudr, mu1_pt, jetmu_dr);
        nd.den(k_lep1_pT_jetlepdr, mu1_pt, jetmu_dr);

        nd.den(k_llp_sump_mu, sump_0+mup_1+miscp);
        nd.den(k_llp_sump_jetmudphi, sump_0+mup_1+miscp, jetmu_dphi);
        nd.den(k_llp_sump_jetmudr, sump_0+mup_1+miscp, jetmu_dr);
        nd.den(k_2logm_jetmudr, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta), jetmu_dr);
        nd.den(k_2logm_mucostheta, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta), jetmu_costheta);
        nd.den(k_mu1_p_jetmu_costheta, mup_1, jetmu_costheta);
        nd.den(k_jetmu_costheta_tightcloseseedtks, jetmu_costheta, n_tightcloseseedtks);
        nd.den(k_jetmu_dr_tightcloseseedtks, jetmu_dr, n_tightcloseseedtks);
        nd.den(k_jetmu_costheta_closeseedtks, jetmu_costheta, n_closeseedtks);
        nd.den(k_jetmu_dr_closeseedtks, jetmu_dr, n_closeseedtks);
        nd.den(k_mu1_p_jetdphi, mup_1, jetmu_dphi);
        nd.den(k_mu1_dxybs, mu1_dxybs);
        nd.den(k_2sump0pmu1_1mcos, log10(2*sump_0*mup_1), log10(1-jetmu_costheta));
        nd.den(k_2logm_mu, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta));
        nd.den(k_dphi_sum_jmu_mv, jetmu_mv_dphi_sum);
        nd.den(k_deta_sum_jmu_mv, jetmu_mv_deta_sum);
        nd.den(k_seedtracks_jetmudr, nseedtracks, jetmu_dr);
        nd.den(k_seedtracks_2logm_mu, nseedtracks, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta));

        nd.den(k_jetmui01, jetmu_i[0], jetmu_i[1]);
        nd.den(k_jetmup01, jet0_p, mu1_p);
        nd.den(k_jetmupt01, jet0_pt, mu1_pt);
        nd.den(k_jetmueta01, jet0_eta, mu1_eta);
        nd.den(k_jetmuphi01, jet0_phi, mu1_phi);
        nd.den(k_jetmumovea3d01, jet0_mv_a3d, mu1_mv_a3d);
        nd.den(k_mumovea3d1_v_movevectoreta, movevectoreta, mu1_mv_a3d);
        nd.den(k_muangle1, mu1_mv_a3d);
        nd.den(k_dphi_mu1_mv, fabs(mu1_mv_dphi));
        nd.den(k_deta_mu1_mv, fabs(mu1_mv_deta));

        nd.den(k_closeseedtks_mu1_dxybs, n_closeseedtks, mu1_dxybs); 
        nd.den(k_jetdr_mu1_dxybs, jetmu_dr, mu1_dxybs);
        nd.den(k_jetmudr_qrk0_dxybs, jetmu_dr, qrk0_dxybs);
        nd.den(k_jetmudphi_qrk0_dxybs, jetmu_dphi, qrk0_dxybs);
        nd.den(k_jetdphi_mu1_dxybs, jetmu_dphi, mu1_dxybs);
        nd.den(k_movedist3_jetmudr, movedist3, jetmu_dr);
        nd.den(k_mu1_p_movedist3, mu1_p, movedist3); 
        nd.den(k_mu1_p_mu1_dxybs, mu1_p, mu1_dxybs); 
        nd.den(k_mu1_dxybs, mu1_dxybs);
        nd.den(k_jetpt0_jmasymm, jet0_p4.Pt(), jetmu_asymm);
        nd.den(k_mupt1_asymm, mu1_p4.Pt(), jetmu_asymm);
        nd.den(k_jeteta0_jmasymm, jet0_p4.Eta(), jetmu_asymm);
        nd.den(k_mueta1_asymm, mu1_p4.Eta(), jetmu_asymm);
        nd.den(k_jetmudr_asymm, jetmu_dr, jetmu_asymm);
        nd.den(k_movedseedtks_jetmudr, n_movedseedtks, jetmu_dr);
        nd.den(k_mumovea3d_v_mup, mu1_p, mu1_mv_a3d);
      }

      if (lep_isele > 0) {
        nd.den(k_jetele_asymm, jetele_asymm);
        nd.den(k_ele1_eta, ele1_eta); 
        nd.den(k_ele1_p_eta, ele1_p, ele1_eta); 
        nd.den(k_lep1_p_eta, ele1_p, ele1_eta); 
        nd.den(k_jetele_dr, jetele_dr); 
        nd.den(k_jetele_costheta, jetele_costheta); 
        nd.den(k_jetele_deta, jetele_deta); 
        nd.den(k_jetele_dphi, jetele_dphi); 
        nd.den(k_jetele_deta_dphi, jetele_deta, jetele_dphi);
        nd.den(k_jetlep_deta_dphi, jetele_deta, jetele_dphi);
        nd.den(k_elept1, ele1_pt); 

        nd.den(k_ele1_trk_pt, tks.pt(ele1trk_idx));
        // nd.den(k_ele1_p, tks.p(ele1trk_idx));
        nd.den(k_ele1_p, ele1_p);

        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          nd.den(k_ele1jet0_trk_dx, (tks.vx(ele1trk_idx) - tks.vx(jet0trk_idx[j])));
          nd.den(k_ele1jet0_trk_dy, (tks.vy(ele1trk_idx) - tks.vy(jet0trk_idx[j])));
          nd.den(k_ele1jet0_trk_dz, (tks.vz(ele1trk_idx) - tks.vz(jet0trk_idx[j])));
          nd.den(k_ele1jet0_trk_dist2d, (std::sqrt( pow(2.0, (tks.vx(ele1trk_idx) - tks.vx(jet0trk_idx[j])) ) + pow(2.0, (tks.vy(ele1trk_idx) - tks.vy(jet0trk_idx[j]))))));
        }

        nd.den(k_ele1_trk_eta, tks.eta(ele1trk_idx));
        nd.den(k_ele1_trk_dz, tks.dzpv(ele1trk_idx, pvs));
        if (mindist2move_iv != -1) {
          const double ele1_vtxdz = tks.dz(ele1trk_idx,vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double ele1_vtxdxy = tks.dxy(ele1trk_idx, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.den(k_ele1_trk_vtxdxy, ele1_vtxdxy);
          nd.den(k_ele1_trk_vtxdz, ele1_vtxdz);
          nd.den(k_ele1_trk_nsigmavtxdz, ele1_vtxdz/tks.err_dz(ele1trk_idx));
          nd.den(k_ele1_trk_nsigmavtxdxy, ele1_vtxdxy/tks.err_dxy(ele1trk_idx));
          nd.den(k_ele1_trk_nsigmavtx, sqrt((ele1_vtxdxy/tks.err_dxy(ele1trk_idx))*(ele1_vtxdxy/tks.err_dxy(ele1trk_idx)) + (ele1_vtxdz/tks.err_dz(ele1trk_idx))*(ele1_vtxdz/tks.err_dz(ele1trk_idx))));
        }
        nd.den(k_ele1_trk_dzerr, tks.err_dz(ele1trk_idx));
        const double ele1_gennsigmadz = tks.dz(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(ele1trk_idx);
        const double ele1_gennsigmamissdist = tks.dxy(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(ele1trk_idx);  
        nd.den(k_ele1_trk_gennsigma, sqrt((ele1_gennsigmamissdist*ele1_gennsigmamissdist) + (ele1_gennsigmadz*ele1_gennsigmadz)));
        nd.den(k_ele1_trk_gennsigmamissdist, ele1_gennsigmamissdist);
        nd.den(k_ele1_trk_genmissdist, tks.dxy(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_ele1_trk_gennsigmadz, ele1_gennsigmadz);
        nd.den(k_ele1_trk_gendz, tks.dz(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_ele1_trk_whichpv, tks.which_pv(ele1trk_idx));
        nd.den(k_ele1_trk_dsz, tks.dsz(ele1trk_idx, pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.den(k_ele1_trk_dxy, tks.dxybs(ele1trk_idx, bs));
        nd.den(k_ele1_trk_nsigmadxy, tks.dxybs(ele1trk_idx, bs)/tks.err_dxy(ele1trk_idx));
        nd.den(k_ele1_trk_dxyerr, tks.err_dxy(ele1trk_idx));
        
        nd.den(k_jet0_maxeta_ele1_eta, maxeta_0, ele1_eta);
        nd.den(k_jet0_sump_ele1_p, sump_0, ele1_p);
        nd.den(k_jet0_sump_lep1_p, sump_0, ele1_p);

        nd.den(k_llp_sump_ele, sump_0+elep_1+miscp);
        nd.den(k_llp_sump_jeteledphi, sump_0+elep_1+miscp, jetele_dphi);
        nd.den(k_llp_sump_jeteledr, sump_0+elep_1+miscp, jetele_dr);
        nd.den(k_llp_sump_jeteledr, sump_0+elep_1+miscp, jetele_dr);
        nd.den(k_jet0_sump_jeteledr, sump_0, jetele_dr);
        nd.den(k_jet0_sump_jetlepdr, sump_0, jetele_dr);
        nd.den(k_ele1_p_jeteledr, ele1_p, jetele_dr);
        nd.den(k_lep1_p_jetlepdr, ele1_p, jetele_dr);
        nd.den(k_ele1_pT_jeteledr, ele1_pt, jetele_dr);
        nd.den(k_lep1_pT_jetlepdr, ele1_pt, jetele_dr);

        nd.den(k_2logm_jeteledr, log10(2*sump_0*elep_1) + log10(1-jetele_costheta), jetele_dr);
        nd.den(k_2logm_elecostheta, log10(2*sump_0*elep_1) + log10(1-jetele_costheta), jetele_costheta);
        nd.den(k_ele1_p_jetele_costheta, elep_1, jetele_costheta);
        nd.den(k_jetele_costheta_tightcloseseedtks, jetele_costheta, n_tightcloseseedtks);
        nd.den(k_jetele_dr_tightcloseseedtks, jetele_dr, n_tightcloseseedtks);
        nd.den(k_jetele_costheta_closeseedtks, jetele_costheta, n_closeseedtks);
        nd.den(k_jetele_dr_closeseedtks, jetele_dr, n_closeseedtks);
        nd.den(k_ele1_p_jetdphi, elep_1, jetele_dphi);
        nd.den(k_ele1_dxybs, ele1_dxybs);
        nd.den(k_2sump0pele1_1mcos, log10(2*sump_0*elep_1), log10(1-jetele_costheta));
        nd.den(k_2logm_ele, log10(2*sump_0*elep_1) + log10(1-jetele_costheta));
        nd.den(k_dphi_sum_jele_mv, jetele_mv_dphi_sum);
        nd.den(k_deta_sum_jele_mv, jetele_mv_deta_sum);
        nd.den(k_seedtracks_jeteledr, nseedtracks, jetele_dr);
        nd.den(k_seedtracks_2logm_ele, nseedtracks, log10(2*sump_0*elep_1) + log10(1-jetele_costheta));

        nd.den(k_closeseedtks_ele1_dxybs, n_closeseedtks, ele1_dxybs); 
        nd.den(k_jetdr_ele1_dxybs, jetele_dr, ele1_dxybs);
        nd.den(k_jeteledr_qrk0_dxybs, jetele_dr, qrk0_dxybs);
        nd.den(k_jeteledphi_qrk0_dxybs, jetele_dphi, qrk0_dxybs);
        nd.den(k_jetdphi_ele1_dxybs, jetele_dphi, ele1_dxybs);
        nd.den(k_movedist3_jeteledr, movedist3, jetele_dr);
        nd.den(k_ele1_p_movedist3, ele1_p, movedist3); 
        nd.den(k_ele1_p_ele1_dxybs, ele1_p, ele1_dxybs); 
        nd.den(k_ele1_dxybs, ele1_dxybs);
        nd.den(k_jetpt0_jeasymm, jet0_p4.Pt(), jetele_asymm);
        nd.den(k_elept1_asymm, ele1_p4.Pt(), jetele_asymm);
        nd.den(k_jeteta0_jeasymm, jet0_p4.Eta(), jetele_asymm);
        nd.den(k_eleeta1_asymm, ele1_p4.Eta(), jetele_asymm);
        nd.den(k_jeteledr_asymm, jetele_dr, jetele_asymm);
        nd.den(k_movedseedtks_jeteledr, n_movedseedtks, jetele_dr);
        nd.den(k_elemovea3d_v_elep, ele1_p, ele1_mv_a3d);

        nd.den(k_jetelei01, jetele_i[0], jetele_i[1]);
        nd.den(k_jetelep01, jet0_p, ele1_p);
        nd.den(k_jetelept01, jet0_pt, ele1_pt);
        nd.den(k_jeteleeta01, jet0_eta, ele1_eta);
        nd.den(k_jetelephi01, jet0_phi, ele1_phi);
        nd.den(k_jetelemovea3d01, jet0_mv_a3d, ele1_mv_a3d);
        nd.den(k_elemovea3d1_v_movevectoreta, movevectoreta, ele1_mv_a3d);
        nd.den(k_eleangle1, ele1_mv_a3d);
        nd.den(k_dphi_ele1_mv, fabs(ele1_mv_dphi));
        nd.den(k_deta_ele1_mv, fabs(ele1_mv_deta));

      }


      for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
        nd.den(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.den(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.den(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(closeseedtrk_idx[j]));
      }


      nd.den(k_movedist3_movedist2, movedist3, movedist2);
      nd.den(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
      nd.den(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
      nd.den(k_closeseedtks_qrk0_dxybs, n_closeseedtks, qrk0_dxybs); 
      nd.den(k_nmovedtks_movedist3, jet_ntk_0 + 1, movedist3); //1 for the lepton...should fix? 


      // nd.den(k_nmovedtks_jet_dr, jet_ntk_0 + jet_ntk_1, jet_dr);  //not using but keeping for a bit 
      nd.den(k_nmovedtks0_qrk0_dxybs, jet_ntk_0, qrk0_dxybs); 
      nd.den(k_nmovedseedtks0_qrk0_dxybs, n_movedseedtks0, qrk0_dxybs); 
      nd.den(k_nmovedtks0_jet0_sump, jet_ntk_0, sump_0); 
      nd.den(k_nmovedseedtks0_jet0_sump, n_movedseedtks0, sump_0); 
      nd.den(k_nmovedseedtks_movedist3, n_movedseedtks, movedist3); 
      nd.den(k_jet0_sump_movedist3, sump_0, movedist3); 
      nd.den(k_jet0_sump_qrk0_dxybs, sump_0, qrk0_dxybs); 
      nd.den(k_qrk0_dxybs, qrk0_dxybs);
      nd.den(k_jet0_dxybs, jet0_dxybs);
      nd.den(k_nmovedtracks, n_movedtks); 

      nd.den(k_nalltracks, nt.tm().nalltracks());
      nd.den(k_nseedtracks, nseedtracks);
      nd.den(k_npreseljets, nt.tm().npreseljets());
      nd.den(k_npreselbjets, nt.tm().npreselbjets());
      nd.den(k_npreselmu, nt.tm().npreselmu());
      nd.den(k_npreselele, nt.tm().npreselele());

      nd.den(k_jetsume, jet_sume);
      //should probably FIX ????
      nd.den(k_jetdrmax, jetlep_drmax);
      nd.den(k_jetdravg, jetlep_dravg);
      nd.den(k_jetdetamax, jetlep_detamax);
      nd.den(k_jetdetaavg, jetlep_detaavg);
      nd.den(k_jetdphimax, jetlep_dphimax);
      nd.den(k_jetdphiavg, jetlep_dphiavg);
      nd.den(k_jet0_tkdrmax, jet0_max_trackpair_dr);
      nd.den(k_jet0_tkdravg, jet0_avg_trackpair_dr);
      nd.den(k_jet_dphi_deta_avg, jetlep_dphiavg, jetlep_detaavg);
      nd.den(k_jdphi_nmovedtks, fabs(jetlep_dphiavg), nt.tm().nmovedtracks());
      nd.den(k_jdeta_nmovedtks, fabs(jetlep_detaavg), nt.tm().nmovedtracks());
      nd.den(k_jdr_nmovedtks, jetlep_dravg,        nt.tm().nmovedtracks());
      nd.den(k_jtheta0_nmovedtks, jet0_mv_a3d,  nt.tm().nmovedtracks());
      //

      nd.den(k_jetmovea3d_v_jetp, jet0_p, jet0_mv_a3d);
      nd.den(k_jetmovea3d0_v_movevectoreta, movevectoreta, jet0_mv_a3d);
      nd.den(k_jeta3dmax, jetlep_a3dmax);
      nd.den(k_angle0, jet0_mv_a3d);
      nd.den(k_dphi_j0_mv, fabs(jet0_mv_dphi));
      nd.den(k_deta_j0_mv, fabs(jet0_mv_deta));
      nd.den(k_dphi_j0_mv_jdeta, fabs(jet0_mv_dphi), fabs(jetlep_detaavg));
      nd.den(k_jetsumntracks, jet_sumntracks);
      nd.den(k_jetsumseedtracks, jet_sumseedtracks);
      nd.den(k_miscseedtracks, nseedtracks - jet_sumseedtracks); 
      nd.den(k_misccloseseedtracks, n_misccloseseedtks); 
      nd.den(k_closeseedtks, n_closeseedtks);
      nd.den(k_tightcloseseedtks, n_tightcloseseedtks);
      nd.den(k_movedseedtks, n_movedseedtks);
      nd.den(k_movedvtxseedtks, n_movedvtxseedtks);
      nd.den(k_movedcloseseedtks, n_movedcloseseedtks);
      nd.den(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
      nd.den(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
      nd.den(k_jetntracks_v_jetp, jet0_p, jet0_ntracks);

      nd.den(k_nvtx, nvtx);
      nd.den(k_vtxbs2derr, vtx_bs2derr);
      nd.den(k_vtxbs2derr_avgtkdr, vtx_bs2derr, jet0_avg_trackpair_dr);
      nd.den(k_vtxbs2derr_jdeta, vtx_bs2derr, jetlep_detaavg);
      nd.den(k_vtxbs2derr_dphi_j0_mv, vtx_bs2derr, jet0_mv_dphi);
      nd.den(k_vtxbs2derr_jdr, vtx_bs2derr, jetlep_dravg);
      nd.den(k_vtxunc, dist2move);
      nd.den(k_vtxunc2d, dist2move2d);
      nd.den(k_vtxeta, vtx_eta);
      nd.den(k_vtxz, vtx_z);
      nd.den(k_vtxdbv, vtx_dbv);
      nd.den(k_vtx3dbv, vtx_3dbv);
      nd.den(k_vtxntk, vtx_ntk);
      if (vtx_ntk >= 5 && vtx_bs2derr < 0.0050) nd.den(k_vtxnm1_dbv, vtx_dbv);
      if (vtx_ntk >= 5 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.den(k_vtxnm1_bs2derr, vtx_bs2derr);
      if (vtx_bs2derr < 0.0050 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.den(k_vtxnm1_ntk, vtx_ntk);
      if (vtx_ntk == 4) nd.den(k_vtx4tkchi2, vtx_chi2);
      if (vtx_ntk == 5) nd.den(k_vtx5tkchi2, vtx_chi2);
      if (vtx_ntk == 6) nd.den(k_vtx6tkchi2, vtx_chi2);
      if (vtx_ntk == 4) nd.den(k_vtx4tkdbv, vtx_dbv);
      if (vtx_ntk == 5) nd.den(k_vtx5tkdbv, vtx_dbv);
      if (vtx_ntk == 6) nd.den(k_vtx6tkdbv, vtx_dbv);
      if (vtx_ntk == 4) nd.den(k_vtx4tkzdbv, vtx_z);
      if (vtx_ntk == 5) nd.den(k_vtx5tkzdbv, vtx_z);
      if (vtx_ntk == 6) nd.den(k_vtx6tkzdbv, vtx_z);
      if (vtx_ntk == 4) nd.den(k_vtx4tkunc, dist2move);
      if (vtx_ntk == 5) nd.den(k_vtx5tkunc, dist2move);
      if (vtx_ntk == 6) nd.den(k_vtx6tkunc, dist2move);
    }


    for (int in = 0; in < num_numdens; ++in) {
      int iv = first_vtx_to_pass[in];
      if (iv == -1)
        continue;
      const std::vector<int> its = tks.tks_for_sv(iv);
      jmt::MaxValue max_tk_err_dxy;
      for (int it : its) max_tk_err_dxy(tks.err_dxy(it));

      h_vtxdbv[in]->Fill(vs.rho(iv), w);
      h_vtxntracks[in]->Fill(vs.ntracks(iv), w);
      h_vtxbs2derr[in]->Fill(vs.bs2derr(iv), w);
      h_vtxanglemax[in]->Fill(vtxs_anglemax[iv], w);
      //      h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv), w);
      h_vtxmass[in]->Fill(vs.mass(iv), w);
      h_vtxphi[in]->Fill(vs.phi(iv), w);
      h_vtxeta[in]->Fill(vs.eta(iv), w);
      h_vtxpt[in]->Fill(vs.pt(iv), w);
      h_vtxbs2derr_v_vtxntracks[in]->Fill(vs.ntracks(iv), vs.bs2derr(iv), w);
      //      h_vtxbs2derr_v_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxanglemax[in]->Fill(vtxs_anglemax[iv], vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxphi[in]->Fill(vs.phi(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxeta[in]->Fill(vs.eta(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxpt[in]->Fill(vs.pt(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_vtxdbv[in]->Fill(vs.rho(iv), vs.bs2derr(iv), w);
      h_vtxbs2derr_v_etamovevec[in]->Fill(move_vector.Eta(), vs.bs2derr(iv), w);

      h_vtxbs2derr_v_maxtkerrdxy[in]->Fill(max_tk_err_dxy, vs.bs2derr(iv), w);

      for (const int it : its) {
        h_vtx_tks_pt[in]->Fill(tks.pt(it), w);
        h_vtx_tks_eta[in]->Fill(tks.eta(it), w);
        h_vtx_tks_phi[in]->Fill(tks.phi(it), w);
        h_vtx_tks_dxy[in]->Fill(tks.dxybs(it, bs), w);
        h_vtx_tks_dz[in]->Fill(tks.dzpv(it, pvs), w);
        h_vtx_tks_err_pt[in]->Fill(tks.err_pt(it), w);
        h_vtx_tks_err_eta[in]->Fill(tks.err_eta(it), w);
        h_vtx_tks_err_phi[in]->Fill(tks.err_phi(it), w);
        h_vtx_tks_err_dxy[in]->Fill(tks.err_dxy(it), w); // JMTBAD this stored value is not the rescaled one
        h_vtx_tks_err_dz[in]->Fill(tks.err_dz(it), w);
        h_vtx_tks_nsigmadxy[in]->Fill(tks.nsigmadxybs(it, bs), w);
        h_vtx_tks_npxlayers[in]->Fill(tks.npxlayers(it), w);
        h_vtx_tks_nstlayers[in]->Fill(tks.nstlayers(it), w);

        if (!nt.tk_moved(it)) {
          h_vtx_tks_nomove_pt[in]->Fill(tks.pt(it), w);
          h_vtx_tks_nomove_eta[in]->Fill(tks.eta(it), w);
          h_vtx_tks_nomove_phi[in]->Fill(tks.phi(it), w);
          h_vtx_tks_nomove_dxy[in]->Fill(tks.dxybs(it, bs), w);
          h_vtx_tks_nomove_dz[in]->Fill(tks.dzpv(it, pvs), w);
          h_vtx_tks_nomove_err_pt[in]->Fill(tks.err_pt(it), w);
          h_vtx_tks_nomove_err_eta[in]->Fill(tks.err_eta(it), w);
          h_vtx_tks_nomove_err_phi[in]->Fill(tks.err_phi(it), w);
          h_vtx_tks_nomove_err_dxy[in]->Fill(tks.err_dxy(it), w);
          h_vtx_tks_nomove_err_dz[in]->Fill(tks.err_dz(it), w);
          h_vtx_tks_nomove_nsigmadxy[in]->Fill(tks.nsigmadxybs(it, bs), w);
          h_vtx_tks_nomove_npxlayers[in]->Fill(tks.npxlayers(it), w);
          h_vtx_tks_nomove_nstlayers[in]->Fill(tks.nstlayers(it), w);
        }
      }
    }

    if (n_pass_nocuts)  nums["nocuts"]  += w;
    if (n_pass_ntracks) nums["ntracks"] += w;
    if (n_pass_all)     nums["all"]     += w;

    const int npasses[num_numdens] = {
      n_pass_nocuts,
      n_pass_ntracks,
      n_pass_all
    };
    for (int i = 0; i < num_numdens; ++i) {
      if (!npasses[i]) continue;
      numdens& nd = nds[i];
      nd.num(k_movedist2, movedist2);
      nd.num(k_movedist3, movedist3);
      nd.num(k_movevectoreta, movevectoreta);
      nd.num(k_npv, pvs.n());
      nd.num(k_pvx, pvs.x(0));
      nd.num(k_pvy, pvs.y(0));
      nd.num(k_pvz, pvs.z(0));
      nd.num(k_pvrho, pvs.rho(0));
      nd.num(k_pvntracks, pvs.ntracks(0));
      nd.num(k_pvscore, pvs.score(0));
      nd.num(k_ht, jets.ht());
      nd.num(k_njets, jets.n());
      nd.num(k_nmuons, nselmuons);
      nd.num(k_muon_pT, muon_pT);
      nd.num(k_muon_abseta, muon_abseta);
      nd.num(k_muon_iso, muon_iso);
      if (muon_iso != 0.0) nd.num(k_muon_zoom_iso, muon_iso);
      nd.num(k_muon_absdxybs, muon_absdxybs);
      nd.num(k_muon_absdz, muon_absdz);
      nd.num(k_muon_nsigmadxybs, muon_nsigmadxybs);
      nd.num(k_neles, nseleles);
      nd.num(k_ele_pT, ele_pT);
      nd.num(k_ele_abseta, ele_abseta);
      nd.num(k_ele_iso, ele_iso);
      if (ele_iso != 0.0) nd.num(k_ele_zoom_iso, ele_iso);
      nd.num(k_ele_absdxybs, ele_absdxybs);
      nd.num(k_ele_absdz, ele_absdz);
      nd.num(k_ele_nsigmadxybs, ele_nsigmadxybs);
      nd.num(k_met_pT, met_pT);
      nd.num(k_w_pT, w_pT);
      nd.num(k_w_mT, w_mT);
      nd.num(k_z_pT, z_pT);
      nd.num(k_z_m, z_m);
      nd.num(k_lnu_absphi, lnu_absphi);
      nd.num(k_ljet_absdr, ljet_absdr);
      nd.num(k_ljet0_absdr, ljet0_absdr);
      // nd.num(k_ljet1_absdr, ljet1_absdr);
      nd.num(k_nujet0_absphi, nujet0_absphi);
      // nd.num(k_nujet1_absphi, nujet1_absphi);
      // nd.num(k_wjet_dphi, fabs(wjet_dphi));
      // nd.num(k_zjet_dphi, fabs(zjet_dphi));

      nd.num(k_jet0_eta, jet0_eta);
      nd.num(k_pt0, jet0_pt);
      nd.num(k_ntks_j0, jet_ntk_0);
      nd.num(k_jet0_sump, sump_0);


      for (size_t j = 0; j < jet0trk_idx.size(); ++j){
        nd.num(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
        nd.num(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
        nd.num(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
        if (mindist2move_iv != -1) {
          const double jet0_vtxdz = tks.dz(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double jet0_vtxdxy = tks.dxy(jet0trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.num(k_jet0_trk_vtxdxy, jet0_vtxdxy);
          nd.num(k_jet0_trk_vtxdz, jet0_vtxdz);
          nd.num(k_jet0_trk_nsigmavtxdz, jet0_vtxdz/tks.err_dz(jet0trk_idx[j]));
          nd.num(k_jet0_trk_nsigmavtxdxy, jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]));
          nd.num(k_jet0_trk_nsigmavtx, sqrt((jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j]))*(jet0_vtxdxy/tks.err_dxy(jet0trk_idx[j])) + (jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))*(jet0_vtxdz/tks.err_dz(jet0trk_idx[j]))));
        }
        nd.num(k_jet0_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
        const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(jet0trk_idx[j]);
        const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(jet0trk_idx[j]);  
        nd.num(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
        nd.num(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
        nd.num(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
        nd.num(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.num(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
        nd.num(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
        nd.num(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
      }

      if (lep_ismu > 0) {
        nd.num(k_jetmu_asymm, jetmu_asymm);
        nd.num(k_mu1_eta, mu1_eta);
        nd.num(k_mu1_p_eta, mu1_p, mu1_eta);
        nd.num(k_lep1_p_eta, mu1_p, mu1_eta);
        nd.num(k_jetmu_dr, jetmu_dr);
        nd.num(k_jetmu_costheta, jetmu_costheta);
        nd.num(k_jetmu_deta, jetmu_deta);
        nd.num(k_jetmu_dphi, jetmu_dphi);
        nd.num(k_jetmu_deta_dphi, jetmu_deta, jetmu_dphi);
        nd.num(k_jetlep_deta_dphi, jetmu_deta, jetmu_dphi);
        nd.num(k_mupt1, mu1_pt);

        nd.num(k_mu1_trk_pt, tks.pt(mu1trk_idx));
        // nd.num(k_mu1_p, tks.p(mu1trk_idx));
        nd.num(k_mu1_p, mu1_p);

        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          nd.num(k_mu1jet0_trk_dx, (tks.vx(mu1trk_idx) - tks.vx(jet0trk_idx[j])));
          nd.num(k_mu1jet0_trk_dy, (tks.vy(mu1trk_idx) - tks.vy(jet0trk_idx[j])));
          nd.num(k_mu1jet0_trk_dz, (tks.vz(mu1trk_idx) - tks.vz(jet0trk_idx[j])));
          nd.num(k_mu1jet0_trk_dist2d, (std::sqrt( pow(2.0, (tks.vx(mu1trk_idx) - tks.vx(jet0trk_idx[j])) ) + pow(2.0, (tks.vy(mu1trk_idx) - tks.vy(jet0trk_idx[j]))))));
        }
        nd.num(k_mu1_trk_eta, tks.eta(mu1trk_idx));
        nd.num(k_mu1_trk_dz, tks.dzpv(mu1trk_idx, pvs));
        if (mindist2move_iv != -1) {
          const double mu1_vtxdz = tks.dz(mu1trk_idx,vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double mu1_vtxdxy = tks.dxy(mu1trk_idx, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.num(k_mu1_trk_vtxdxy, mu1_vtxdxy);
          nd.num(k_mu1_trk_vtxdz, mu1_vtxdz);
          nd.num(k_mu1_trk_nsigmavtxdz, mu1_vtxdz/tks.err_dz(mu1trk_idx));
          nd.num(k_mu1_trk_nsigmavtxdxy, mu1_vtxdxy/tks.err_dxy(mu1trk_idx));
          nd.num(k_mu1_trk_nsigmavtx, sqrt((mu1_vtxdxy/tks.err_dxy(mu1trk_idx))*(mu1_vtxdxy/tks.err_dxy(mu1trk_idx)) + (mu1_vtxdz/tks.err_dz(mu1trk_idx))*(mu1_vtxdz/tks.err_dz(mu1trk_idx))));
        }
        nd.num(k_mu1_trk_dzerr, tks.err_dz(mu1trk_idx));
        const double mu1_gennsigmadz = tks.dz(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(mu1trk_idx);
        const double mu1_gennsigmamissdist = tks.dxy(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(mu1trk_idx);  
        nd.num(k_mu1_trk_gennsigma, sqrt((mu1_gennsigmamissdist*mu1_gennsigmamissdist) + (mu1_gennsigmadz*mu1_gennsigmadz)));
        nd.num(k_mu1_trk_gennsigmamissdist, mu1_gennsigmamissdist);
        nd.num(k_mu1_trk_genmissdist, tks.dxy(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_mu1_trk_gennsigmadz, mu1_gennsigmadz);
        nd.num(k_mu1_trk_gendz, tks.dz(mu1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_mu1_trk_whichpv, tks.which_pv(mu1trk_idx));
        nd.num(k_mu1_trk_dsz, tks.dsz(mu1trk_idx, pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.num(k_mu1_trk_dxy, tks.dxybs(mu1trk_idx, bs));
        nd.num(k_mu1_trk_nsigmadxy, tks.dxybs(mu1trk_idx, bs)/tks.err_dxy(mu1trk_idx));
        nd.num(k_mu1_trk_dxyerr, tks.err_dxy(mu1trk_idx));

        nd.num(k_jet0_maxeta_mu1_eta, maxeta_0, mu1_eta);
        nd.num(k_jet0_sump_mu1_p, sump_0, mu1_p);
        nd.num(k_jet0_sump_lep1_p, sump_0, mu1_p);
        nd.num(k_jet0_sump_jetmudr, sump_0, jetmu_dr);
        nd.num(k_jet0_sump_jetlepdr, sump_0, jetmu_dr);

        nd.num(k_mu1_p_jetmudr, mu1_p, jetmu_dr);
        nd.num(k_lep1_p_jetlepdr, mu1_p, jetmu_dr);
        nd.num(k_mu1_pT_jetmudr, mu1_pt, jetmu_dr);
        nd.num(k_lep1_pT_jetlepdr, mu1_pt, jetmu_dr);

        nd.num(k_llp_sump_mu, sump_0+mup_1+miscp);
        nd.num(k_llp_sump_jetmudphi, sump_0+mup_1+miscp, jetmu_dphi);
        nd.num(k_llp_sump_jetmudr, sump_0+mup_1+miscp, jetmu_dr);
        nd.num(k_2logm_jetmudr, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta), jetmu_dr);
        nd.num(k_2logm_mucostheta, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta), jetmu_costheta);
        nd.num(k_mu1_p_jetmu_costheta, mup_1, jetmu_costheta);
        nd.num(k_jetmu_costheta_tightcloseseedtks, jetmu_costheta, n_tightcloseseedtks);
        nd.num(k_jetmu_dr_tightcloseseedtks, jetmu_dr, n_tightcloseseedtks);
        nd.num(k_jetmu_costheta_closeseedtks, jetmu_costheta, n_closeseedtks);
        nd.num(k_jetmu_dr_closeseedtks, jetmu_dr, n_closeseedtks);
        nd.num(k_mu1_p_jetdphi, mup_1, jetmu_dphi);
        nd.num(k_mu1_dxybs, mu1_dxybs);
        nd.num(k_2sump0pmu1_1mcos, log10(2*sump_0*mup_1), log10(1-jetmu_costheta));
        nd.num(k_2logm_mu, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta));
        nd.num(k_dphi_sum_jmu_mv, jetmu_mv_dphi_sum);
        nd.num(k_deta_sum_jmu_mv, jetmu_mv_deta_sum);
        nd.num(k_seedtracks_jetmudr, nseedtracks, jetmu_dr);
        nd.num(k_seedtracks_2logm_mu, nseedtracks, log10(2*sump_0*mup_1) + log10(1-jetmu_costheta));

        nd.num(k_jetmui01, jetmu_i[0], jetmu_i[1]);
        nd.num(k_jetmup01, jet0_p, mu1_p);
        nd.num(k_jetmupt01, jet0_pt, mu1_pt);
        nd.num(k_jetmueta01, jet0_eta, mu1_eta);
        nd.num(k_jetmuphi01, jet0_phi, mu1_phi);
        nd.num(k_jetmumovea3d01, jet0_mv_a3d, mu1_mv_a3d);
        nd.num(k_mumovea3d1_v_movevectoreta, movevectoreta, mu1_mv_a3d);
        nd.num(k_muangle1, mu1_mv_a3d);
        nd.num(k_dphi_mu1_mv, fabs(mu1_mv_dphi));
        nd.num(k_deta_mu1_mv, fabs(mu1_mv_deta));

        nd.num(k_closeseedtks_mu1_dxybs, n_closeseedtks, mu1_dxybs); 
        nd.num(k_jetdr_mu1_dxybs, jetmu_dr, mu1_dxybs);
        nd.num(k_jetmudr_qrk0_dxybs, jetmu_dr, qrk0_dxybs);
        nd.num(k_jetmudphi_qrk0_dxybs, jetmu_dphi, qrk0_dxybs);
        nd.num(k_jetdphi_mu1_dxybs, jetmu_dphi, mu1_dxybs);
        nd.num(k_movedist3_jetmudr, movedist3, jetmu_dr);
        nd.num(k_mu1_p_movedist3, mu1_p, movedist3); 
        nd.num(k_mu1_p_mu1_dxybs, mu1_p, mu1_dxybs); 
        nd.num(k_mu1_dxybs, mu1_dxybs);
        nd.num(k_jetpt0_jmasymm, jet0_p4.Pt(), jetmu_asymm);
        nd.num(k_mupt1_asymm, mu1_p4.Pt(), jetmu_asymm);
        nd.num(k_jeteta0_jmasymm, jet0_p4.Eta(), jetmu_asymm);
        nd.num(k_mueta1_asymm, mu1_p4.Eta(), jetmu_asymm);
        nd.num(k_jetmudr_asymm, jetmu_dr, jetmu_asymm);
        nd.num(k_movedseedtks_jetmudr, n_movedseedtks, jetmu_dr);
        nd.num(k_mumovea3d_v_mup, mu1_p, mu1_mv_a3d);
      }
      if (lep_isele > 0) {
        nd.num(k_jetele_asymm, jetele_asymm);
        nd.num(k_ele1_eta, ele1_eta);
        nd.num(k_ele1_p_eta, ele1_p, ele1_eta);
        nd.num(k_lep1_p_eta, ele1_p, ele1_eta);
        nd.num(k_jetele_dr, jetele_dr);
        nd.num(k_jetele_costheta, jetele_costheta);
        nd.num(k_jetele_deta, jetele_deta);
        nd.num(k_jetele_dphi, jetele_dphi);
        nd.den(k_jetele_deta_dphi, jetele_deta, jetele_dphi);
        nd.den(k_jetlep_deta_dphi, jetele_deta, jetele_dphi);

        nd.num(k_elept1, ele1_pt);
        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          nd.num(k_ele1jet0_trk_dx, (tks.vx(ele1trk_idx) - tks.vx(jet0trk_idx[j])));
          nd.num(k_ele1jet0_trk_dy, (tks.vy(ele1trk_idx) - tks.vy(jet0trk_idx[j])));
          nd.num(k_ele1jet0_trk_dz, (tks.vz(ele1trk_idx) - tks.vz(jet0trk_idx[j])));
          nd.num(k_ele1jet0_trk_dist2d, (std::sqrt( pow(2.0, (tks.vx(ele1trk_idx) - tks.vx(jet0trk_idx[j])) ) + pow(2.0, (tks.vy(ele1trk_idx) - tks.vy(jet0trk_idx[j]))))));
        }
        nd.num(k_ele1_trk_pt, tks.pt(ele1trk_idx));
        // nd.num(k_ele1_p, tks.p(ele1trk_idx));
        nd.num(k_ele1_p, ele1_p);

        nd.num(k_ele1_trk_eta, tks.eta(ele1trk_idx));
        nd.num(k_ele1_trk_dz, tks.dzpv(ele1trk_idx, pvs));
        if (mindist2move_iv != -1) {
          const double ele1_vtxdz = tks.dz(ele1trk_idx,vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double ele1_vtxdxy = tks.dxy(ele1trk_idx, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          nd.num(k_ele1_trk_vtxdxy, ele1_vtxdxy);
          nd.num(k_ele1_trk_vtxdz, ele1_vtxdz);
          nd.num(k_ele1_trk_nsigmavtxdz, ele1_vtxdz/tks.err_dz(ele1trk_idx));
          nd.num(k_ele1_trk_nsigmavtxdxy, ele1_vtxdxy/tks.err_dxy(ele1trk_idx));
          nd.num(k_ele1_trk_nsigmavtx, sqrt((ele1_vtxdxy/tks.err_dxy(ele1trk_idx))*(ele1_vtxdxy/tks.err_dxy(ele1trk_idx)) + (ele1_vtxdz/tks.err_dz(ele1trk_idx))*(ele1_vtxdz/tks.err_dz(ele1trk_idx))));
        }
        nd.num(k_ele1_trk_dzerr, tks.err_dz(ele1trk_idx));
        const double ele1_gennsigmadz = tks.dz(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(ele1trk_idx);
        const double ele1_gennsigmamissdist = tks.dxy(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z()))/tks.err_dxy(ele1trk_idx);  
        nd.num(k_ele1_trk_gennsigma, sqrt((ele1_gennsigmamissdist*ele1_gennsigmamissdist) + (ele1_gennsigmadz*ele1_gennsigmadz)));
        nd.num(k_ele1_trk_gennsigmamissdist, ele1_gennsigmamissdist);
        nd.num(k_ele1_trk_genmissdist, tks.dxy(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_ele1_trk_gennsigmadz, ele1_gennsigmadz);
        nd.num(k_ele1_trk_gendz, tks.dz(ele1trk_idx, nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_ele1_trk_whichpv, tks.which_pv(ele1trk_idx));
        nd.num(k_ele1_trk_dsz, tks.dsz(ele1trk_idx, pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        nd.num(k_ele1_trk_dxy, tks.dxybs(ele1trk_idx, bs));
        nd.num(k_ele1_trk_nsigmadxy, tks.dxybs(ele1trk_idx, bs)/tks.err_dxy(ele1trk_idx));
        nd.num(k_ele1_trk_dxyerr, tks.err_dxy(ele1trk_idx));
        
        nd.num(k_jet0_maxeta_ele1_eta, maxeta_0, ele1_eta);
        nd.num(k_jet0_sump_jeteledr, sump_0, jetele_dr);
        nd.num(k_jet0_sump_jetlepdr, sump_0, jetele_dr);
        nd.num(k_jet0_sump_ele1_p, sump_0, ele1_p);
        nd.num(k_jet0_sump_lep1_p, sump_0, ele1_p);
        nd.num(k_ele1_p_jeteledr, ele1_p, jetele_dr);
        nd.num(k_lep1_p_jetlepdr, ele1_p, jetele_dr);
        nd.num(k_ele1_pT_jeteledr, ele1_pt, jetele_dr);
        nd.num(k_lep1_pT_jetlepdr, ele1_pt, jetele_dr);
        nd.num(k_llp_sump_ele, sump_0+elep_1+miscp);
        nd.num(k_llp_sump_jeteledphi, sump_0+elep_1+miscp, jetele_dphi);
        nd.num(k_llp_sump_jeteledr, sump_0+elep_1+miscp, jetele_dr);
        nd.num(k_2logm_jeteledr, log10(2*sump_0*elep_1) + log10(1-jetele_costheta), jetele_dr);
        nd.num(k_2logm_elecostheta, log10(2*sump_0*elep_1) + log10(1-jetele_costheta), jetele_costheta);
        nd.num(k_ele1_p_jetele_costheta, elep_1, jetele_costheta);
        nd.num(k_jetele_costheta_tightcloseseedtks, jetele_costheta, n_tightcloseseedtks);
        nd.num(k_jetele_dr_tightcloseseedtks, jetele_dr, n_tightcloseseedtks);
        nd.num(k_jetele_costheta_closeseedtks, jetele_costheta, n_closeseedtks);
        nd.num(k_jetele_dr_closeseedtks, jetele_dr, n_closeseedtks);
        nd.num(k_ele1_p_jetdphi, elep_1, jetele_dphi);
        nd.num(k_ele1_dxybs, ele1_dxybs);
        nd.num(k_2sump0pele1_1mcos, log10(2*sump_0*elep_1), log10(1-jetele_costheta));
        nd.num(k_2logm_ele, log10(2*sump_0*elep_1) + log10(1-jetele_costheta));
        nd.num(k_dphi_sum_jele_mv, jetele_mv_dphi_sum);
        nd.num(k_deta_sum_jele_mv, jetele_mv_deta_sum);
        nd.num(k_seedtracks_jeteledr, nseedtracks, jetele_dr);
        nd.num(k_seedtracks_2logm_ele, nseedtracks, log10(2*sump_0*elep_1) + log10(1-jetele_costheta));

        nd.num(k_closeseedtks_ele1_dxybs, n_closeseedtks, ele1_dxybs); 
        nd.num(k_jetdr_ele1_dxybs, jetele_dr, ele1_dxybs);
        nd.num(k_jeteledr_qrk0_dxybs, jetele_dr, qrk0_dxybs);
        nd.num(k_jeteledphi_qrk0_dxybs, jetele_dphi, qrk0_dxybs);
        nd.num(k_jetdphi_ele1_dxybs, jetele_dphi, ele1_dxybs);
        nd.num(k_movedist3_jeteledr, movedist3, jetele_dr);
        nd.num(k_ele1_p_movedist3, ele1_p, movedist3); 
        nd.num(k_ele1_p_ele1_dxybs, ele1_p, ele1_dxybs); 
        nd.num(k_ele1_dxybs, ele1_dxybs);
        nd.num(k_jetpt0_jeasymm, jet0_p4.Pt(), jetele_asymm);
        nd.num(k_elept1_asymm, ele1_p4.Pt(), jetele_asymm);
        nd.num(k_jeteta0_jeasymm, jet0_p4.Eta(), jetele_asymm);
        nd.num(k_eleeta1_asymm, ele1_p4.Eta(), jetele_asymm);
        nd.num(k_jeteledr_asymm, jetele_dr, jetele_asymm);
        nd.num(k_movedseedtks_jeteledr, n_movedseedtks, jetele_dr);
        nd.num(k_elemovea3d_v_elep, ele1_p, ele1_mv_a3d);

        nd.num(k_jetelei01, jetele_i[0], jetele_i[1]);
        nd.num(k_jetelep01, jet0_p, ele1_p);
        nd.num(k_jetelept01, jet0_pt, ele1_pt);
        nd.num(k_jeteleeta01, jet0_eta, ele1_eta);
        nd.num(k_jetelephi01, jet0_phi, ele1_phi);
        nd.num(k_jetelemovea3d01, jet0_mv_a3d, ele1_mv_a3d);
        nd.num(k_elemovea3d1_v_movevectoreta, movevectoreta, ele1_mv_a3d);
        nd.num(k_eleangle1, ele1_mv_a3d);
        nd.num(k_dphi_ele1_mv, fabs(ele1_mv_dphi));
        nd.num(k_deta_ele1_mv, fabs(ele1_mv_deta));

      }

      for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
        nd.num(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y()+ bs.y(nt.tm().move_z())));
        nd.num(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z()));
        nd.num(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], nt.tm().move_x()+ bs.x(nt.tm().move_z()), nt.tm().move_y() + bs.y(nt.tm().move_z()), nt.tm().move_z())/tks.err_dz(closeseedtrk_idx[j]));
      }

      nd.num(k_movedist3_movedist2, movedist3, movedist2);
      nd.num(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
      nd.num(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
      nd.num(k_closeseedtks_qrk0_dxybs, n_closeseedtks, qrk0_dxybs); 
      nd.num(k_nmovedtks_movedist3, jet_ntk_0 + 1, movedist3); //1 for the lepton...should fix? 


      // nd.num(k_nmovedtks_jet_dr, jet_ntk_0 + jet_ntk_1, jet_dr);  //not using but keeping for a bit 
      nd.num(k_nmovedtks0_qrk0_dxybs, jet_ntk_0, qrk0_dxybs); 
      nd.num(k_nmovedseedtks0_qrk0_dxybs, n_movedseedtks0, qrk0_dxybs); 
      nd.num(k_nmovedtks0_jet0_sump, jet_ntk_0, sump_0); 
      nd.num(k_nmovedseedtks0_jet0_sump, n_movedseedtks0, sump_0); 
      nd.num(k_nmovedseedtks_movedist3, n_movedseedtks, movedist3); 
      nd.num(k_jet0_sump_movedist3, sump_0, movedist3); 
      nd.num(k_jet0_sump_qrk0_dxybs, sump_0, qrk0_dxybs); 
      nd.num(k_qrk0_dxybs, qrk0_dxybs);
      nd.num(k_jet0_dxybs, jet0_dxybs);
      nd.num(k_nmovedtracks, n_movedtks); 

      nd.num(k_nalltracks, nt.tm().nalltracks());
      nd.num(k_nseedtracks, nseedtracks);
      nd.num(k_npreseljets, nt.tm().npreseljets());
      nd.num(k_npreselbjets, nt.tm().npreselbjets());
      nd.num(k_npreselmu, nt.tm().npreselmu());
      nd.num(k_npreselele, nt.tm().npreselele());

      nd.num(k_jetsume, jet_sume);
      nd.num(k_jetdrmax, jetlep_drmax);
      nd.num(k_jetdravg, jetlep_dravg);
      nd.num(k_jetdetamax, jetlep_detamax);
      nd.num(k_jetdetaavg, jetlep_detaavg);
      nd.num(k_jetdphimax, jetlep_dphimax);
      nd.num(k_jetdphiavg, jetlep_dphiavg);
      nd.num(k_jet0_tkdrmax, jet0_max_trackpair_dr);
      nd.num(k_jet0_tkdravg, jet0_avg_trackpair_dr);
      nd.num(k_jet_dphi_deta_avg, jetlep_dphiavg, jetlep_detaavg);
      nd.num(k_jdphi_nmovedtks, fabs(jetlep_dphiavg), nt.tm().nmovedtracks());
      nd.num(k_jdeta_nmovedtks, fabs(jetlep_detaavg), nt.tm().nmovedtracks());
      nd.num(k_jdr_nmovedtks, jetlep_dravg,        nt.tm().nmovedtracks());
      nd.num(k_jtheta0_nmovedtks, jet0_mv_a3d,  nt.tm().nmovedtracks());

      nd.num(k_jetmovea3d_v_jetp, jet0_p, jet0_mv_a3d);
      nd.num(k_jetmovea3d0_v_movevectoreta, movevectoreta, jet0_mv_a3d);
      nd.num(k_jeta3dmax, jetlep_a3dmax);
      nd.num(k_angle0, jet0_mv_a3d);
      nd.num(k_dphi_j0_mv, fabs(jet0_mv_dphi));
      nd.num(k_deta_j0_mv, fabs(jet0_mv_deta));
      nd.num(k_dphi_j0_mv_jdeta, fabs(jet0_mv_dphi), fabs(jetlep_detaavg));
      nd.num(k_jetsumntracks, jet_sumntracks);
      nd.num(k_jetsumseedtracks, jet_sumseedtracks);
      nd.num(k_miscseedtracks, nseedtracks - jet_sumseedtracks); 
      nd.num(k_misccloseseedtracks, n_misccloseseedtks); 
      nd.num(k_closeseedtks, n_closeseedtks);
      nd.num(k_tightcloseseedtks, n_tightcloseseedtks);
      nd.num(k_movedseedtks, n_movedseedtks);
      nd.num(k_movedvtxseedtks, n_movedvtxseedtks);
      nd.num(k_movedcloseseedtks, n_movedcloseseedtks);
      nd.num(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
      nd.num(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
      nd.num(k_jetntracks_v_jetp, jet0_p, jet0_ntracks);

      nd.num(k_nvtx, npasses[i]);
      nd.num(k_vtxbs2derr, vtx_bs2derr);
      nd.num(k_vtxbs2derr_avgtkdr, vtx_bs2derr, jet0_avg_trackpair_dr);
      nd.num(k_vtxbs2derr_jdeta, vtx_bs2derr, jetlep_detaavg);
      nd.num(k_vtxbs2derr_dphi_j0_mv, vtx_bs2derr, jet0_mv_dphi);
      nd.num(k_vtxbs2derr_jdr, vtx_bs2derr, jetlep_dravg);
      if (vtx_bs2derr < 0.0050) {
         nd.num(k_vtxunc, dist2move);
         nd.num(k_vtxunc2d, dist2move2d);
         nd.num(k_vtxeta, vtx_eta);
         nd.num(k_vtxz, vtx_z);
         nd.num(k_vtxdbv, vtx_dbv);
         nd.num(k_vtx3dbv, vtx_3dbv);
         nd.num(k_vtxntk, vtx_ntk);
      }
      if (vtx_ntk >= 4 && vtx_bs2derr < 0.0050) nd.num(k_vtxnm1_dbv, vtx_dbv);
      if (vtx_ntk >= 4 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.num(k_vtxnm1_bs2derr, vtx_bs2derr);
      if (vtx_bs2derr < 0.0050 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.num(k_vtxnm1_ntk, vtx_ntk);
      if (vtx_ntk == 4) nd.num(k_vtx4tkchi2, vtx_chi2);
      if (vtx_ntk == 5) nd.num(k_vtx5tkchi2, vtx_chi2);
      if (vtx_ntk == 6) nd.num(k_vtx6tkchi2, vtx_chi2);
      if (vtx_ntk == 4) nd.num(k_vtx4tkdbv, vtx_dbv);
      if (vtx_ntk == 5) nd.num(k_vtx5tkdbv, vtx_dbv);
      if (vtx_ntk == 6) nd.num(k_vtx6tkdbv, vtx_dbv);
      if (vtx_ntk == 4) nd.num(k_vtx4tkzdbv, vtx_z);
      if (vtx_ntk == 5) nd.num(k_vtx5tkzdbv, vtx_z);
      if (vtx_ntk == 6) nd.num(k_vtx6tkzdbv, vtx_z);
      if (vtx_ntk == 4) nd.num(k_vtx4tkunc, dist2move);
      if (vtx_ntk == 5) nd.num(k_vtx5tkunc, dist2move);
      if (vtx_ntk == 6) nd.num(k_vtx6tkunc, dist2move);

      
      for (size_t it = 0, ite = tks.n(); it < ite; ++it) {
        h_tks_pt[i]->Fill(tks.pt(it), w);
        h_tks_eta[i]->Fill(tks.eta(it), w);
        h_tks_phi[i]->Fill(tks.phi(it), w);
        h_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
        h_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
        h_tks_err_pt[i]->Fill(tks.err_pt(it), w);
        h_tks_err_eta[i]->Fill(tks.err_eta(it), w);
        h_tks_err_phi[i]->Fill(tks.err_phi(it), w);
        h_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
        h_tks_err_dz[i]->Fill(tks.err_dz(it), w);
        h_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
        h_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
        h_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);

         if (nt.tk_moved(it)) {
          h_moved_tks_pt[i]->Fill(tks.pt(it), w);
          h_moved_tks_eta[i]->Fill(tks.eta(it), w);
          h_moved_tks_phi[i]->Fill(tks.phi(it), w);
          h_moved_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
          h_moved_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
          h_moved_tks_err_pt[i]->Fill(tks.err_pt(it), w);
          h_moved_tks_err_eta[i]->Fill(tks.err_eta(it), w);
          h_moved_tks_err_phi[i]->Fill(tks.err_phi(it), w);
          h_moved_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
          h_moved_tks_err_dz[i]->Fill(tks.err_dz(it), w);
          h_moved_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
          h_moved_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
          h_moved_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);

          if (!tks.pass_seed(it, bs)) {
            h_moved_nosel_tks_pt[i]->Fill(tks.pt(it), w);
            h_moved_nosel_tks_eta[i]->Fill(tks.eta(it), w);
            h_moved_nosel_tks_phi[i]->Fill(tks.phi(it), w);
            h_moved_nosel_tks_dxy[i]->Fill(tks.dxybs(it, bs), w);
            h_moved_nosel_tks_dz[i]->Fill(tks.dzpv(it, pvs), w);
            h_moved_nosel_tks_err_pt[i]->Fill(tks.err_pt(it), w);
            h_moved_nosel_tks_err_eta[i]->Fill(tks.err_eta(it), w);
            h_moved_nosel_tks_err_phi[i]->Fill(tks.err_phi(it), w);
            h_moved_nosel_tks_err_dxy[i]->Fill(tks.err_dxy(it), w);
            h_moved_nosel_tks_err_dz[i]->Fill(tks.err_dz(it), w);
            h_moved_nosel_tks_nsigmadxy[i]->Fill(tks.nsigmadxybs(it, bs), w);
            h_moved_nosel_tks_npxlayers[i]->Fill(tks.npxlayers(it), w);
            h_moved_nosel_tks_nstlayers[i]->Fill(tks.nstlayers(it), w);
          }
        }
      }
    }
    NR_loop_cont(w);
  };

  nr.loop(fcn);

  printf("%llu/%llu = %.1f/%.1f denominator events with negative weights\n", nnegden, nden, negden, den);
  printf("%20s  %12s  %12s  %10s [%10s, %10s] +%10s -%10s\n", "name", "num", "den", "eff", "lo", "hi", "+", "-");
  for (const auto& p : nums) {
    const jmt::interval i = jmt::clopper_pearson_binom(p.second, den);
    printf("%20s  %12.1f  %12.1f  %10.4f [%10.4f, %10.4f] +%10.4f -%10.4f\n", p.first.c_str(), p.second, den, i.value, i.lower, i.upper, i.upper - i.value, i.value - i.lower);
  }
}
