#include "utils.h"
#include <cmath>

int main(int argc, char** argv) {
  double min_lspdist3 = 0.02; //FIXME

  jmt::NtupleReader<mfv::MovedTracksNtuple> nr;
  namespace po = boost::program_options;
  nr.init_options("mfvMovedTreeMCTruth/t", "TrackMoverMCTruth_HighEta", "trackmovermctruthulv13lepmv6", "all_signal = True")
  // nr.init_options("mfvMovedTreeMCTruth/t", "TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6", "trackmovermctruthonnormdzulv30lepmumv6", "all_signal = True")
    ("min-lspdist3", po::value<double>(&min_lspdist3)->default_value(0.00), "min distance between LSP decays to use event") //FIXME 0.02
    ;

  if (!nr.parse_options(argc, argv)) return 1;
  std::cout << " min_lspdist3: " << min_lspdist3 << "\n";

  if (!nr.init()) return 1;
  auto& nt = nr.nt();
  auto& bs = nt.bs();
  auto& pvs = nt.pvs();
  auto& jets = nt.jets();
  auto& muons = nt.muons();
  auto& electrons = nt.electrons();
  // auto& pf = nt.pf();
  auto& tks = nt.tracks();
  auto& gen = nt.gentruth();
  auto& vs = nt.vertices();
  ////

  const int num_numdens = 3;
  // const bool dijet      = false;
  const bool semilep    = true; //for displaced SUSY - 1jet 1lep case 
  numdens nds[num_numdens] = {
    numdens("nocuts"),
    numdens("ntracks"),
    numdens("all")
  };

  enum { k_decay_x, k_decay_y, k_decay_z, k_decay_xy, k_lspdist2, k_lspdphi, k_lspdeta, k_lspdr, k_lspasymdecay, k_lspcostheta,  k_lspdist3, 
         k_lspdist3symmath, k_ratlspdist3, k_2sinhalftheta, k_lspdistz, k_movedist2, k_movedist3, k_lspeta, k_lsppt, k_lspgammabeta, k_lspctau, 
         k_npv, k_pvz, k_dist2dpvbs, k_pvrho, k_pvntracks, k_pvscore, k_ht, k_njets, 
         k_jetmu_asymm, k_jetele_asymm, k_jet0_eta, k_mu1_eta, k_ele1_eta, k_jetmu_dr, k_jetele_dr, k_jetmu_costheta, k_jetele_costheta, 
         k_jetmu_asymsump, k_jetele_asymsump, k_jetmu_deta, k_jetele_deta, 
         k_jetmu_dphi, k_jetele_dphi, k_jetmu_deta_dphi, k_jetele_deta_dphi, k_jetlep_deta_dphi,
         k_pt0, k_mupt1, k_elept1, k_ntks_j0, k_jet_dr_minj0_q0, k_mu_dr_minl1_l1, k_ele_dr_minl1_l1, k_boost0_boost1, 

         k_movedseedinvtx_trk_whichjet, k_miscclose_trk_whichjet, k_miscclose_trk_p, k_miscclose_trk_eta, k_miscclose_trk_dzerr, 
         k_movedseedinvtx_trk_dsz, k_miscclose_trk_dsz, k_movedseedoutvtx_trk_eta, k_movedseedinvtx_trk_eta, k_movedseedoutvtx_trk_p, 
         k_movedseedinvtx_trk_p, k_movedseedoutvtx_trk_dz, k_movedseedinvtx_trk_dz, k_movedseedoutvtx_trk_gennsigma, k_movedseedinvtx_trk_gennsigma, 
         k_movedseedoutvtx_trk_dr, k_movedseedinvtx_trk_dr, k_movedseedoutvtx_trk_dxyerr, k_movedseedinvtx_trk_dxyerr, k_movedseedoutvtx_trk_dzerr, 
         k_movedseedinvtx_trk_dzerr, k_movedseedoutvtx_trk_whichpv, k_movedseedinvtx_trk_whichpv, k_jet0_trk_pt, k_jet0_trk_p, 
         k_jet0_trk_dr_gennsigma, k_jet0_trk_dr_genmissdist, k_jet0_trk_dr_gendz, k_jet0_trk_eta_gennsigma,
         k_jet0_trk_eta_gendz, k_jet0_trk_dz, k_jet0_trk_vtxdxy, k_jet0_trk_vtxdz, 
         k_jet0_trk_nsigmavtxdz, k_jet0_trk_nsigmavtxdxy, k_jet0_trk_nsigmavtx, k_jet0_trk_dzerr, k_jet0_trk_nsigmadz, k_jet0_trk_dxyerr,
         k_jet0_trk_eta, k_jet0_sump, k_mu1_p_eta, k_ele1_p_eta, k_lep1_p_eta,
         k_mu1_p, k_ele1_p, k_jet0_sump_mu1_p, k_jet0_sump_ele1_p, k_jet0_sump_lep1_p, k_jetmudr_qrk0_dxybs, k_jeteledr_qrk0_dxybs, k_jetmudr_genmu1_dxybs, k_jeteledr_genele1_dxybs, 
         k_jetmudphi_qrk0_dxybs, k_jeteledphi_qrk0_dxybs, k_jetmudphi_genmu1_dxybs, k_jeteledphi_genele1_dxybs, 
         k_closeseedtks_qrk0_dxybs, k_closeseedtks_genmu1_dxybs, k_closeseedtks_genele1_dxybs, k_nmovedtks_jetmu_dr, k_nmovedtks_jetele_dr, k_nmovedtks0_qrk0_dxybs, 
         k_nmovedseedtks0_qrk0_dxybs, k_nmovedtks0_jet0_sump, k_nmovedseedtks0_jet0_sump, 
         k_nmovedtks_movedist3, k_nmovedseedtks_movedist3, k_mu1_p_movedist3, k_ele1_p_movedist3, k_jet0_sump_movedist3, 
         k_mu1_p_genmu1_dxybs, k_ele1_p_genele1_dxybs, k_jet0_sump_qrk0_dxybs, k_llp_sump_mu, k_llp_sump_ele,  k_llp_sump_jetmudphi, k_llp_sump_jeteledphi, 
         k_llp_sump_jetmudr, k_llp_sump_jeteledr, k_jet0_sump_jetmudr, k_jet0_sump_jeteledr, k_jet0_sump_jetlepdr, k_mu1_p_jetmudr, k_ele1_p_jeteledr, k_lep1_p_jetlepdr,
         k_mu1_pT_jetmudr, k_ele1_pT_jeteledr, k_lep1_pT_jetlepdr,
         k_2logm_jetmudr, k_2logm_jeteledr, k_2logm_costheta_mu, k_2logm_costheta_ele, k_mu1_p_jetmu_costheta, k_ele1_p_jetele_costheta, 
         k_movedist3_movedist2, k_movedist3_jetmudr, k_movedist3_jeteledr, k_movedist3_mu1_p, k_movedist3_ele1_p, k_movedist3_angle2d, 
         k_angle2d_jetmudr, k_angle2d_jeteledr, k_angle2d_mu1_p,  k_angle2d_ele1_p, k_movedist2_jetmudr, k_movedist2_jeteledr, 
         k_movedist2_mu1_p, k_movedist2_ele1_p, k_movedist3_tightcloseseedtks, 
         k_jetmu_costheta_tightcloseseedtks, k_jetele_costheta_tightcloseseedtks, 
         k_jetmu_dr_tightcloseseedtks, k_jetele_dr_tightcloseseedtks,
         k_movedist3_closeseedtks, k_movedist3_nmovedseedtks, k_movedist3_nmovedtks, 
         k_movedist3_nmovedcloseseedtks, k_movedist3_nmisccloseseedtks, k_movedist2_closeseedtks, k_movedist2_nmovedseedtks, k_movedist2_nmovedtks, 
         k_movedist2_nmovedcloseseedtks, k_movedist2_nmisccloseseedtks, 
         k_jetmu_costheta_closeseedtks, k_jetele_costheta_closeseedtks, k_jetmu_dr_closeseedtks, k_jetele_dr_closeseedtks,
         k_lspdist3_movedcloseseedtks, 
         k_lspdist3_movedist3, k_lspdist3_movedist2, k_lspdist3_qrk0_dxybs, 
         k_lspdist3_genmu1_dxybs, k_lspdist3_genele1_dxybs, 
         k_mu1_p_jetdphi, k_ele1_p_jetdphi, k_jet0_maxeta_mu1_eta, k_jet0_maxeta_ele1_eta, 
         k_genmu1_p, k_genele1_p, k_qrk0_p, k_genmu1_dxybs, k_genele1_dxybs, 
         k_qrk0_dxybs, k_mu1_dxybs, k_ele1_dxybs,k_jet0_dxybs, 
         k_qrktosump_j0, k_genmutop_mu1, k_geneletop_ele1, 
         k_qrktosump_sumpj0, k_genmutosump_sumpmu1, k_geneletosump_sumpele1, 
         k_2p0p1_1mgencos_mu, k_2p0p1_1mgencos_ele, 
         k_2sump0sump1_1mcos_mu, k_2sump0sump1_1mcos_ele,
         k_2genlogm_mu, k_2genlogm_ele, k_2logm_mu, k_2logm_ele, 
         k_asymjetmu_jetmudr, k_asymjetele_jeteledr,
         k_closeseed_trk_gendz, k_closeseed_trk_genmissdist, k_closeseed_trk_gennsigmadz, k_jet0_trk_gennsigma,
         k_jet0_trk_gennsigmamissdist, k_jet0_trk_genmissdist, k_jet0_trk_gennsigmadz, 
         k_jet0_trk_gendz, k_jet0_trk_whichpv, k_jet0_trk_dsz, 
         k_jet0_trk_nsigmadsz, k_jet0_trk_dxy, k_jet0_trk_nsigmadxy, k_nmovedtracks, k_dphi_sum_jmu_mv, k_deta_sum_jmu_mv, k_dphi_sum_qgm_mv, k_dphi_sum_jele_mv, 
         k_deta_sum_jele_mv, k_dphi_sum_qge_mv, 
         k_jetpt0_asymm_mu, k_jetpt0_asymm_ele, k_mupt1_asymm, k_elept1_asymm, k_jeteta0_asymm_mu, k_jeteta0_asymm_ele, 
         k_mueta1_asymm, k_eleeta1_asymm, k_jetmudr_asymm, k_jeteledr_asymm, 
         k_jetmudravg, k_jeteledravg, k_angle0, k_anglemu1, k_angleele1, 
         k_dphi_j0_mv, k_dphi_mu1_mv, k_dphi_ele1_mv, k_deta_j0_mv, k_deta_mu1_mv, k_deta_ele1_mv, 
         k_dphi_q0_mv, k_dphi_genmu1_mv, k_dphi_genele1_mv, k_nseedtracks, 
         k_miscseedtracks, k_misccloseseedtracks, k_closeseedtks, k_sharedcloseseedtks, k_tightcloseseedtks, k_movedseedtks, k_movedcloseseedtks, 
         k_movedvtxseedtks, k_rat_moved_to_closetks, k_rat_moved_to_vtxtks, k_rat_movedvtxtks_to_movedtks, k_rat_movedclosetks_to_movedtks, 
         k_jetmudphimax, k_jeteledphimax, 
         k_jetmudetamax, k_jeteledetamax, 
         k_qrkgenmudphimax, k_qrkgeneledphimax, 
         k_jetmudphi_mveta, k_jeteledphi_mveta, 
         k_jetmumovea3d01, k_jetelemovea3d01, 
         k_jetmueta01, k_jeteleeta01, 
         k_jetmupt01, k_jetelept01, 
         k_pt_angle0, k_pt_anglemu1, k_pt_angleele1, 
         k_eta_angle0, k_eta_anglemu1, k_eta_angleele1, 
         k_nvtx, k_vtxcat, k_vtxbs2derr, k_vtxunc, k_vtxeta, k_vtxz, k_vtxdbv, k_vtx3dbv, k_vtxntk, k_dr, 
         k_dvv, k_dvv_2vtx, k_movedist3_movedist2_2vtx, k_dvv2d, k_vtxnm1_dbv, k_vtxnm1_ntk, k_vtxnm1_bs2derr, k_vtx3tkchi2, k_vtx3tkdbv, 
         k_vtx3tkdvv, k_vtx3tkzdbv, k_vtx3tkunc, k_vtx4tkchi2, k_vtx4tkdbv, k_vtx4tkdvv, k_vtx4tkzdbv, k_vtx4tkunc, k_vtx5tkchi2, k_vtx5tkdbv, 
         k_vtx5tkdvv, k_vtx5tkzdbv, k_vtx5tkunc};

  for (numdens& nd : nds) {
    nd.book(k_decay_x,  "decay_x" , ";SV Decay X-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_y,  "decay_y" , ";SV Decay Y-pos [cm]; arb. units", 100, -4, 4);
    nd.book(k_decay_z,  "decay_z" , ";SV Decay Z-pos [cm]; arb. units", 100, -20, 20);
    nd.book(k_decay_xy, "decay_xy" , ";SV Decay X-pos [cm]; SV Decay Y-pos [cm]", 100, -10, 10, 100, -10, 10);
    nd.book(k_lspdist2, "lspdist2", ";2-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_lspdphi, "lspdphi", ";#Delta#Phi between gen verts;events/0.01 cm", 350, 0, 3.5);
    nd.book(k_lspdeta, "lspdeta", ";#Delta#Eta between gen verts;events/0.01 cm", 350, 0, 3.5);
    nd.book(k_lspdr, "lspdr", ";#Delta R between gen verts;events/0.01 cm", 350, 0, 7.0);
    nd.book(k_lspasymdecay, "lspasymdecay", "; |lsp1 decay - lsp0 decay|/lsp0 decay; ", 50, 0, 1.0);
    nd.book(k_lspcostheta, "lspcostheta", ";cos(#Theta) between gen verts;events/0.01 cm", 100, 0, 1.0);
    nd.book(k_lspdist3, "lspdist3", ";3-dist between gen verts;events/0.01 cm", 200, 0, 2.0); 
    nd.book(k_lspdist3symmath, "lspdist3symmath", ";2*movedist3d*sin(#theta/2);events/0.01 cm", 200, 0, 2);
    nd.book(k_ratlspdist3, "ratlspdist3", ";#frac{2*movedist3d*sin(#theta/2)}{truth lspdist3};events", 200, 0, 1);
    nd.book(k_2sinhalftheta, "2sinhalftheta", ";2*sin(#theta/2);events", 60, -3, 3);
    nd.book(k_lspdistz, "lspdistz", ";z-dist between gen verts;events/0.01 cm", 200, 0, 2);
    nd.book(k_movedist2, "movedist2", ";movement 2-dist;events/0.01 cm", 50, 0, 2.5);
    nd.book(k_movedist3, "movedist3", ";movement 3-dist;events/0.01 cm", 50, 0, 4.0);  
    nd.book(k_lspeta,    "movevectoreta"   , ";move vector eta;events/0.08 cm", 100, -4, 4);
    nd.book(k_lsppt,     "lsppt"    , ";Pt of LSP [GeV];events/bin", 50, 0, 1000);
    nd.book(k_lspgammabeta,     "lspgammabeta"    , ";#gamma#beta of LSP ;events/bin", 100, 0, 20);
    nd.book(k_lspctau,     "lspctau"    , ";c#tau of LSP ;events/bin", 100, 0, 2);
    nd.book(k_npv, "npv", ";# PV;events/1", 100, 0, 100);
    nd.book(k_pvz, "pvz", ";PV z (cm);events/0.24 cm", 200, -24, 24);
    nd.book(k_dist2dpvbs, "dist2dpvbs", ";dist2d(pvs,bs) (cm);events/0.24 cm", 100, -0.1, 0.1);
    nd.book(k_pvrho, "pvrho", ";PV #rho (cm);events/1 #mum", 200, 0, 0.02);
    nd.book(k_pvntracks, "pvntracks", ";PV # tracks;events/2", 200, 0, 400);
    nd.book(k_pvscore, "pvscore", ";PV #Sigma p_{T}^{2} (GeV^{2});events/200 GeV^{2}", 200, 0, 40000);
    nd.book(k_ht, "ht", ";#Sigma H_{T} (GeV);events/50 GeV", 20, 0, 1000);
    nd.book(k_njets, "njets", ";# jets;events/1", 20, 0, 20);
    
    // nd.book(k_nmuons, "nmuons", ";# passed offline-sel muons;events/1", 10, 0, 10);
    // nd.book(k_muon_pT, "muon_pT", ";muons p_{T} (GeV);events/1", 50, 0, 200);
    // nd.book(k_muon_abseta, "muon_abseta", ";muons |#eta|; arb. units", 70, 0, 3.5);
    // nd.book(k_muon_iso, "muon_iso", ";muons iso;events/1", 200, 0, 0.15);
    // nd.book(k_muon_absdxybs, "muon_absdxybs", ";muons |dxy| cm; arb. units", 80, 0, 0.2);
    // nd.book(k_muon_absdz, "muon_absdz", ";muons |dz| cm; arb. units", 80, 0, 1.0);
    // nd.book(k_muon_nsigmadxybs, "muon_nsigmadxybs", ";muons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    // nd.book(k_neles, "neles", ";# passed offline-sel electrons;events/1", 10, 0, 10);
    // nd.book(k_ele_pT, "ele_pT", ";electrons p_{T} (GeV);events/1", 50, 0, 200);
    // nd.book(k_ele_abseta, "ele_abseta", ";electrons |#eta|; arb. units", 70, 0, 3.5);
    // nd.book(k_ele_iso, "ele_iso", ";electrons iso;events/1", 200, 0, 0.15);
    // nd.book(k_ele_absdxybs, "ele_absdxybs", ";electrons |dxy| cm; arb. units", 80, 0, 0.2);
    // nd.book(k_ele_absdz, "ele_absdz", ";electrons |dz| cm; arb. units", 80, 0, 1.0);
    // nd.book(k_ele_nsigmadxybs, "ele_nsigmadxybs", ";electrons n#sigma dxybs ; arb. units", 80, 0, 6.0);
    // nd.book(k_met_pT, "met_pT", ";missing p_{T} (GeV);events/1", 50, 0, 200);
    // nd.book(k_w_pT, "w_pT", ";RECO W(Z) boson's p_{T} (GeV);events/1", 50, 0, 200);
    // nd.book(k_w_mT, "w_mT", ";RECO W boson's mass_{T} (GeV);events/1", 50, 0, 150);
    // nd.book(k_z_pT, "z_pT", ";RECO Z boson's p_{T} (GeV);events/1", 50, 0, 200);
    // nd.book(k_z_m, "z_m", ";RECO Z boson's inv. mass (GeV);events/1", 50, 0, 150);
    // nd.book(k_lnu_absphi, "lnu_absphi", ";lepton-#nu |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_ljet_absdr, "ljet_absdr", ";lepton-closest-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_ljet0_absdr, "ljet0_absdr", ";lepton-jet0 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_ljet1_absdr, "ljet1_absdr", ";lepton-jet1 |#DeltaR|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_nujet0_absphi, "nujet0_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_nujet1_absphi, "nujet1_absphi", ";MET-jet0 |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_wjet_dphi, "wjet_dphi", ";W(Z)-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
    // nd.book(k_zjet_dphi, "zjet_dphi", ";Z-jet |#DeltaPhi|; arb. units", 70, 0.0, 3.5);
   
    nd.book(k_jetmu_asymm, "jetmu_asymm", ";jet-mu pT asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_jetele_asymm, "jetele_asymm", ";jet-ele pT asymmetry A_{J}; arb. units", 25, 0, 1);
    nd.book(k_jet0_eta, "jet0_eta", ";jet0's Eta; arb. units", 60, -4, 4);
    // nd.book(k_jet1_eta, "jet1_eta", ";jet1's Eta; arb. units", 60, -3, 3);
    nd.book(k_mu1_eta, "mu1_eta", ";mu1's Eta; arb. units", 60, -4, 4);
    nd.book(k_ele1_eta, "ele1_eta", ";ele1's Eta; arb. units", 60, -4, 4);
    nd.book(k_mu1_p_eta, "mu1_p_eta", ";mu1's momentum p; mu1's Eta", 100, 0, 500, 60, -4, 4); //check ##
    nd.book(k_ele1_p_eta, "ele1_p_eta", ";ele1's momentum p; ele1's Eta", 100, 0, 500, 60, -4, 4); //check ##
    nd.book(k_lep1_p_eta, "lep1_p_eta", ";lep1's momentum p; lep1's Eta", 100, 0, 500, 60, -4, 4); //check ##

    // nd.book(k_jet_dr, "jet_dr", ";jets' #DeltaR; arb. units", 60, 0, 6);
    nd.book(k_jetmu_dr, "jetmu_dr", ";jet-mu #DeltaR; arb. units", 60, 0, 6);
    nd.book(k_jetele_dr, "jetele_dr", ";jet-ele #DeltaR; arb. units", 60, 0, 6);
    // nd.book(k_jet_costheta, "jet_costheta", ";jets' cos(#theta); arb. units", 80, -1, 1);
    nd.book(k_jetmu_costheta, "jetmu_costheta", ";jet-mu cos(#theta); arb. units", 80, -1, 1);
    nd.book(k_jetele_costheta, "jetele_costheta", ";jet-ele cos(#theta); arb. units", 80, -1, 1);
    // nd.book(k_jet_asymsump, "jet_asymsump", ";jet's quality tracks sum mom. asymm. A_{J}", 20, -1, 1);
    nd.book(k_jetmu_asymsump, "jetmu_asymsump", ";mu mom. - jet quality tracks sum mom. asymm. A_{J}", 20, -1, 1);
    nd.book(k_jetele_asymsump, "jetele_asymsump", ";ele mom. - jet quality tracks sum mom. asymm. A_{J}", 20, -1, 1);
    // nd.book(k_jet_deta, "jet_deta", ";jets' #DeltaEta; arb. units", 70, 0, 7);
    nd.book(k_jetmu_deta, "jetmu_deta", ";jet-mu #DeltaEta; arb. units", 70, 0, 7);
    nd.book(k_jetele_deta, "jetele_deta", ";jet-ele #DeltaEta; arb. units", 70, 0, 7);
    // nd.book(k_jet_dphi, "jet_dphi", ";jets' #DeltaPhi; arb. units", 70, -3.5, 3.5);
    nd.book(k_jetmu_dphi, "jetmu_dphi", ";jet-mu #DeltaPhi; arb. units", 70, -3.5, 3.5);
    nd.book(k_jetele_dphi, "jetele_dphi", ";jet-ele #DeltaPhi; arb. units", 70, -3.5, 3.5);
    nd.book(k_jetmu_deta_dphi, "jetmu_deta_dphi", ";jet-mu #DeltaEta; jet-mu #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##
    nd.book(k_jetele_deta_dphi, "jetele_deta_dphi", ";jet-ele #DeltaEta; jet-ele #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##
    nd.book(k_jetlep_deta_dphi, "jetlep_deta_dphi", ";jet-lep #DeltaEta; jet-lep #DeltaPhi", 70, -3.5, 3.5, 70, -3.5, 3.5); //check##

    // nd.book(k_jet_dind, "jet_dind", ";jets' #DeltaIndex; arb. units", 20, 0, 20);
    nd.book(k_pt0, "pt0", ";RECO jet0 pT [GeV]", 100, 0, 500);
    // nd.book(k_pt1, "pt1", ";RECO jet1 pT [GeV]", 50, 0, 150);
    nd.book(k_mupt1, "mupt1", ";RECO mu1 pT [GeV]", 100, 0, 500);
    nd.book(k_elept1, "elept1", ";RECO ele1 pT [GeV]", 100, 0, 500);
    nd.book(k_ntks_j0, "ntks_j0", ";Ntks in jet0", 25, 0, 25);
    // nd.book(k_ntks_j1, "ntks_j1", ";Ntks in jet1", 25, 0, 25);
    nd.book(k_jet_dr_minj0_q0, "jet_dr_minj0_q0", ";#DeltaR(j0,quark0)", 70, 0, 7);
    // nd.book(k_jet_dr_minj1_q1, "jet_dr_minj1_q1", ";#DeltaR(minij1,quark1)", 70, 0, 7);
    nd.book(k_mu_dr_minl1_l1, "mu_dr_minl1_l1", ";#DeltaR(mu1,genmu1)", 70, 0, 7);
    nd.book(k_ele_dr_minl1_l1, "ele_dr_minl1_l1", ";#DeltaR(ele1,genele1)", 70, 0, 7);
    // nd.book(k_ntk0_ntk1, "ntk0_ntk1", ";Ntks in jet0; Ntks in jet1; arb. units", 25, 0.0, 25, 25, 0.0, 25);
    nd.book(k_boost0_boost1, "boost0_boost1", ";#gamma#beta of quark0; #gamma#beta of quark1; arb. units", 50, 0.0, 200, 50, 0.0, 200);
    nd.book(k_jet0_trk_pt, "jet0_trk_pt", "; jet0-movedquality-track's pT; arb. units", 45, 0, 15);
    // nd.book(k_jet1_trk_pt, "jet1_trk_pt", "; jet1-movedquality-track's pT; arb. units", 45, 0, 15);
    nd.book(k_jet0_trk_p, "jet0_trk_p", "; jet0-movedquality-track's p; arb. units", 45, 0, 15);
    // nd.book(k_jet1_trk_p, "jet1_trk_p", "; jet1-movedquality-track's p; arb. units", 45, 0, 15);
    nd.book(k_jet0_sump, "jet0_sump", "; jet0-movedquality-track's sum p; arb. units", 100, 0, 500);
    // nd.book(k_jet1_sump, "jet1_sump", "; jet1-movedquality-track's sum p; arb. units", 80, 0, 80);
    nd.book(k_mu1_p, "mu1_p", "; mu1-movedquality-track's p; arb. units", 100, 0, 500);
    nd.book(k_ele1_p, "ele1_p", "; ele1-movedquality-track's p; arb. units", 100, 0, 500);
    nd.book(k_llp_sump_mu, "llp_sump_mu", "; llp-moved-misc-quality-track's sum p (mu)", 100, 0, 1000);
    nd.book(k_llp_sump_ele, "llp_sump_ele", "; llp-moved-misc-quality-track's sum p (ele)", 100, 0, 1000);

    // nd.book(k_llp_sump_jetdphi, "llp_sump_jetdphi", "; llp-moved-misc-quality-track's sum p;jets #DeltaPhi", 300, 0, 300, 70, -3.5, 3.5);
    nd.book(k_llp_sump_jetmudphi, "llp_sump_jetmudphi", "; llp-moved-misc-quality-track's sum p;jet-mu #DeltaPhi", 300, 0, 300, 70, -3.5, 3.5);
    nd.book(k_llp_sump_jeteledphi, "llp_sump_jeteledphi", "; llp-moved-misc-quality-track's sum p;jet-ele #DeltaPhi", 300, 0, 300, 70, -3.5, 3.5);
    // nd.book(k_llp_sump_jetdr, "llp_sump_jetdr", "; llp-moved-misc-quality-track's sum p;jets #DeltaR", 300, 0, 300, 60, 0, 6.0);
    nd.book(k_llp_sump_jetmudr, "llp_sump_jetmudr", "; llp-moved-misc-quality-track's sum p;jet-mu #DeltaR", 300, 0, 300, 60, 0, 6.0);
    nd.book(k_llp_sump_jeteledr, "llp_sump_jeteledr", "; llp-moved-misc-quality-track's sum p;jet-ele #DeltaR", 300, 0, 300, 60, 0, 6.0);
    // nd.book(k_jet0_sump_jetdr, "jet0_sump_jetdr", "; jet0-movedquality-track's sum p;jets #DeltaR", 80, 0, 80, 60, 0, 6.0);
    nd.book(k_jet0_sump_jetmudr, "jet0_sump_jetmudr", "; jet0-movedquality-track's sum p;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_jet0_sump_jeteledr, "jet0_sump_jeteledr", "; jet0-movedquality-track's sum p;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_jet0_sump_jetlepdr, "jet0_sump_jetlepdr", "; jet0-movedquality-track's sum p;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #

    nd.book(k_mu1_p_jetmudr, "mu1_p_jetdr", "; mu1-movedquality's p;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_ele1_p_jeteledr, "ele1_p_jetdr", "; ele1-movedquality's p;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_lep1_p_jetlepdr, "lep1_p_jetdr", "; lep1-movedquality's p;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #

    nd.book(k_mu1_pT_jetmudr, "mu1_pT_jetdr", "; mu1-pT;jet-mu #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_ele1_pT_jeteledr, "ele1_pT_jetdr", "; ele1-pT;jet-ele #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #
    nd.book(k_lep1_pT_jetlepdr, "lep1_pT_jetdr", "; lep1-pT;jet-lep #DeltaR", 100, 0, 500, 60, 0, 6.0); //check #


    // nd.book(k_2logm_jetdr, "2logm_jetdr", "; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta));jets #DeltaR", 70, 0, 7, 60, 0, 6.0); 
    nd.book(k_2logm_jetmudr, "2logm_jetmudr", "; log(2*sump_{tk0}*mup_{1}) + log(1-cos(#Delta#Theta));jet-mu #DeltaR", 70, 0, 7, 60, 0, 6.0); //check #
    nd.book(k_2logm_jeteledr, "2logm_jeteledr", "; log(2*sump_{tk0}*elep_{1}) + log(1-cos(#Delta#Theta));jet-ele #DeltaR", 70, 0, 7, 60, 0, 6.0); //check #
    // nd.book(k_2logm_costheta, "2logm_costheta", "; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta));jets' cos(#theta)", 70, 0, 7, 80, -1, 1); 
    nd.book(k_2logm_costheta_mu, "2logm_costheta_mu", "; log(2*sump_{tk0}*mup_{1}) + log(1-cos(#Delta#Theta));jet-mu cos(#theta)", 70, 0, 7, 80, -1, 1); //check #
    nd.book(k_2logm_costheta_ele, "2logm_costheta_ele", "; log(2*sump_{tk0}*elep_{1}) + log(1-cos(#Delta#Theta));jet-ele cos(#theta)", 70, 0, 7, 80, -1, 1); //check #
    // nd.book(k_jet1_sump_jet_costheta, "jet1_sump_jet_costheta", "; jet1-movedquality-track's sum p;jets' cos(#theta)", 80, 0, 80, 80, -1, 1);
    nd.book(k_mu1_p_jetmu_costheta, "mu1_p_jetmu_costheta", "; mu1-movedquality's p;jet-mu cos(#theta)", 80, 0, 80, 80, -1, 1); //check #
    nd.book(k_ele1_p_jetele_costheta, "ele1_p_jetele_costheta", "; ele1-movedquality's p;jet-ele cos(#theta)", 80, 0, 80, 80, -1, 1); //check #
    nd.book(k_movedist3_movedist2, "movedist3_movedist2", "; movement 3-dist; movement 2-dist", 50, 0, 4.0, 50, 0, 2.5); 
    // nd.book(k_movedist3_jetdr, "movedist3_jetdr", "; movement 3-dist;jets #DeltaR", 50, 0, 4.0, 60, 0, 6.0);  
    nd.book(k_movedist3_jetmudr, "movedist3_jetmudr", "; movement 3-dist;jetmu #DeltaR", 50, 0, 4.0, 60, 0, 6.0); //check#
    nd.book(k_movedist3_jeteledr, "movedist3_jeteledr", "; movement 3-dist;jetele #DeltaR", 50, 0, 4.0, 60, 0, 6.0); //check#
    // nd.book(k_movedist3_jet1_sump, "movedist3_jet1_sump", "; movement 3-dist; jet1-movedquality-track's sum p", 50, 0, 4.0, 40, 0, 80);  
    nd.book(k_movedist3_mu1_p, "movedist3_mu1_p", "; movement 3-dist; mu1-movedquality-track's p", 50, 0, 4.0, 40, 0, 80);  
    nd.book(k_movedist3_ele1_p, "movedist3_ele1_p", "; movement 3-dist; ele1-movedquality-track's p", 50, 0, 4.0, 40, 0, 80);  
    nd.book(k_movedist3_angle2d, "movedist3_angle2d", "; movement 3-dist; movedist2/movedist3", 50, 0, 4.0, 50, 0, 1.5); 
    // nd.book(k_angle2d_jetdr, "angle2d_jetdr", ";  movedist2/movedist3;jets #DeltaR", 50, 0, 1.5, 60, 0, 6.0);  
    nd.book(k_angle2d_jetmudr, "angle2d_jetmudr", ";  movedist2/movedist3;jet-mu #DeltaR", 50, 0, 1.5, 60, 0, 6.0);  
    nd.book(k_angle2d_jeteledr, "angle2d_jeteledr", ";  movedist2/movedist3;jet-ele #DeltaR", 50, 0, 1.5, 60, 0, 6.0);  
    // nd.book(k_angle2d_jet1_sump, "angle2d_jet1_sump", ";  movedist2/movedist3; jet1-movedquality-track's sum p", 50, 0, 1.5, 40, 0, 80); 
    nd.book(k_angle2d_mu1_p, "angle2d_jet1_sump", ";  movedist2/movedist3; jet1-movedquality-track's sum p", 50, 0, 1.5, 40, 0, 80); 
    nd.book(k_angle2d_ele1_p, "angle2d_jet1_sump", ";  movedist2/movedist3; jet1-movedquality-track's sum p", 50, 0, 1.5, 40, 0, 80); 
    // nd.book(k_movedist2_jetdr, "movedist2_jetdr", "; movement 2-dist;jets #DeltaR", 50, 0, 2.5, 60, 0, 6.0);  
    nd.book(k_movedist2_jetmudr, "movedist2_jetmudr", "; movement 2-dist;jet-mu #DeltaR", 50, 0, 2.5, 60, 0, 6.0);  
    nd.book(k_movedist2_jeteledr, "movedist2_jeteledr", "; movement 2-dist;jet-ele #DeltaR", 50, 0, 2.5, 60, 0, 6.0);  
    // nd.book(k_movedist2_jet1_sump, "movedist2_jet1_sump", "; movement 2-dist; jet1-movedquality-track's sum p", 50, 0, 2.5, 40, 0, 80);  
    nd.book(k_movedist2_mu1_p, "movedist2_mu1_p", "; movement 2-dist; mu1-movedquality-track's p", 50, 0, 2.5, 40, 0, 80);  
    nd.book(k_movedist2_ele1_p, "movedist2_ele1_p", "; movement 2-dist; ele1-movedquality-track's p", 50, 0, 2.5, 40, 0, 80);  
    nd.book(k_movedist3_tightcloseseedtks, "movedist3_tightcloseseedtks", ";movement 3-dist ;# seed tracks 2#sigma-close to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    // nd.book(k_jet_costheta_tightcloseseedtks, "jet_costheta_tightcloseseedtks", "; jets' cos(#theta);# seed tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jetmu_costheta_tightcloseseedtks, "jetmu_costheta_tightcloseseedtks", "; jet-mu cos(#theta);# seed tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jetele_costheta_tightcloseseedtks, "jetele_costheta_tightcloseseedtks", "; jet-ele cos(#theta);# seed tracks 2#sigma-close to artificial vtx", 80, -1, 1, 25, 0, 25);
    // nd.book(k_jet_dr_tightcloseseedtks, "jet_dr_tightcloseseedtks", "; jets' #DeltaR;# seed tracks 2#sigma-close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_jetmu_dr_tightcloseseedtks, "jetmu_dr_tightcloseseedtks", "; jet-mu #DeltaR;# seed tracks 2#sigma-close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_jetele_dr_tightcloseseedtks, "jetele_dr_tightcloseseedtks", "; jet-ele #DeltaR;# seed tracks 2#sigma-close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_movedist3_closeseedtks, "movedist3_closeseedtks", ";movement 3-dist ;# seed tracks close to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_movedist3_nmovedtks, "movedist3_nmovedtks", ";movement 3-dist ;# tracks associated to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_movedist3_nmovedcloseseedtks, "movedist3_nmovedcloseseedtks", ";movement 3-dist ;# close seed tracks associated to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_movedist3_nmisccloseseedtks, "movedist3_nmisccloseseedtks", ";movement 3-dist ;# close seed tracks not associated to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_movedist3_nmovedseedtks, "movedist3_nmovedseedtks", ";movement 3-dist ;# seed tracks associated to artificial vtx", 50, 0, 4.0, 25, 0, 25);
    nd.book(k_movedist2_closeseedtks, "movedist2_closeseedtks", ";movement 2-dist ;# seed tracks close to artificial vtx", 50, 0, 2.5, 25, 0, 25);
    nd.book(k_movedist2_nmovedtks, "movedist2_nmovedtks", ";movement 2-dist ;# tracks associated to artificial vtx", 50, 0, 2.5, 25, 0, 25);
    nd.book(k_movedist2_nmovedcloseseedtks, "movedist2_nmovedcloseseedtks", ";movement 2-dist ;# close seed tracks associated to artificial vtx", 50, 0, 2.5, 25, 0, 25);
    nd.book(k_movedist2_nmisccloseseedtks, "movedist2_nmisccloseseedtks", ";movement 2-dist ;# close seed tracks not associated to artificial vtx", 50, 0, 2.5, 25, 0, 25);
    nd.book(k_movedist2_nmovedseedtks, "movedist2_nmovedseedtks", ";movement 2-dist ;# seed tracks associated to artificial vtx", 50, 0, 2.5, 25, 0, 25);
    // nd.book(k_jet_costheta_closeseedtks, "jet_costheta_closeseedtks", "; jets' cos(#theta);# seed tracks close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jetmu_costheta_closeseedtks, "jetmu_costheta_closeseedtks", "; jet-mu cos(#theta);# seed tracks close to artificial vtx", 80, -1, 1, 25, 0, 25);
    nd.book(k_jetele_costheta_closeseedtks, "jetele_costheta_closeseedtks", "; jet-ele cos(#theta);# seed tracks close to artificial vtx", 80, -1, 1, 25, 0, 25);
    // nd.book(k_jet_dr_closeseedtks, "jet_dr_closeseedtks", "; jets' #DeltaR;# seed tracks close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_jetmu_dr_closeseedtks, "jetmu_dr_closeseedtks", "; jet-mu #DeltaR;# seed tracks close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_jetele_dr_closeseedtks, "jetele_dr_closeseedtks", "; jet-ele #DeltaR;# seed tracks close to artificial vtx", 60, 0, 6, 25, 0, 25);
    nd.book(k_lspdist3_movedcloseseedtks, "lspdist3_movedcloseseedtks", "; 3-dist between gen verts;# moved seed tracks 5#sigma to LLP", 80, 0, 2.0, 30, 0, 30);
    nd.book(k_lspdist3_movedist3, "lspdist3_movedist3", "; 3-dist between gen verts;# movement 3-dist", 20, 0, 1.0, 20, 0, 2.5);
    nd.book(k_lspdist3_movedist2, "lspdist3_movedist2", "; 3-dist between gen verts;# movement 2-dist", 20, 0, 1.0, 20, 0, 2.5);
    nd.book(k_lspdist3_qrk0_dxybs, "lspdist3_qrk0_dxybs", "; 3-dist between gen verts; quark0's dxybs", 20, 0, 1.0, 20, 0, 0.2);
    // nd.book(k_lspdist3_qrk1_dxybs, "lspdist3_qrk1_dxybs", "; 3-dist between gen verts; quark1's dxybs", 20, 0, 1.0, 20, 0, 0.2);
    nd.book(k_lspdist3_genmu1_dxybs, "lspdist3_genmu1_dxybs", "; 3-dist between gen verts; genmu1's dxybs", 20, 0, 1.0, 20, 0, 0.2);
    nd.book(k_lspdist3_genele1_dxybs, "lspdist3_genele1_dxybs", "; 3-dist between gen verts; genele1's dxybs", 20, 0, 1.0, 20, 0, 0.2);
    // nd.book(k_qrk0_phi_genqrk0_phi, "qrk0_phi_genqrk0_phi", "; matched-track quark0's phi ; GEN quark0's phi", 20, -3.5, 3.5, 20, -3.5, 3.5);
    // nd.book(k_qrk1_phi_genqrk1_phi, "qrk1_phi_genqrk1_phi", "; matched-track quark1's phi ; GEN quark1's phi", 20, -3.5, 3.5, 20, -3.5, 3.5);
    nd.book(k_mu1_p_jetdphi, "mu1_sump_jetmudphi", "; mu1-movedquality-track's p;jet-mu #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5);
    nd.book(k_ele1_p_jetdphi, "ele1_sump_jeteledphi", "; ele1-movedquality-track's p;jet-ele #DeltaPhi", 80, 0, 80, 70, -3.5, 3.5);
    // nd.book(k_jet1_ntks_jetdphi, "jet1_ntks_jetdphi", "; Ntks in jet1;jets #DeltaPhi", 25, 0, 25, 70, -3.5, 3.5);
    nd.book(k_jet0_maxeta_mu1_eta, "jet0_maxeta_mu1_eta", "; max(jet0-movedquality-track's Eta); mu1-movedquality-track's Eta", 60, -3, 3, 60, -3, 3); 
    nd.book(k_jet0_maxeta_ele1_eta, "jet0_maxeta_ele1_eta", "; max(jet0-movedquality-track's Eta); ele1-movedquality-track's Eta", 60, -3, 3, 60, -3, 3); 
    // nd.book(k_jet0_sump_jet1_sump, "jet0_sump_jet1_sump", "; jet0-movedquality-track's sum p; jet1-movedquality-track's sum p", 80, 0, 80, 80, 0, 80); 
    nd.book(k_jet0_sump_mu1_p, "jet0_sump_mu1_p", "; jet0-movedquality-track's sum p; mu1-movedquality-track's p", 100, 0, 500, 100, 0, 500); 
    nd.book(k_jet0_sump_ele1_p, "jet0_sump_ele1_p", "; jet0-movedquality-track's sum p; ele1-movedquality-track's p", 100, 0, 500, 100, 0, 500); 
    nd.book(k_jet0_sump_lep1_p, "jet0_sump_lep1_p", "; jet0-movedquality-track's sum p; ele1-movedquality-track's p", 100, 0, 500, 100, 0, 500); 

    // nd.book(k_jetdr_qrk0_dxybs, "jetdr_qrk0_dxybs", "; jets' #DeltaR; quark0's dxybs", 60, 0, 6, 20, 0, 0.2);
    nd.book(k_jetmudr_qrk0_dxybs, "jetmudr_qrk0_dxybs", "; jet-mu #DeltaR; quark0's dxybs", 60, 0, 6, 20, 0, 0.2);
    nd.book(k_jeteledr_qrk0_dxybs, "jeteledr_qrk0_dxybs", "; jet-ele #DeltaR; quark0's dxybs", 60, 0, 6, 20, 0, 0.2);
    // nd.book(k_jetdr_qrk1_dxybs, "jetdr_qrk1_dxybs", "; jets' #DeltaR; quark1's dxybs", 60, 0, 6, 20, 0, 0.2);
    nd.book(k_jetmudr_genmu1_dxybs, "jetmudr_genmu1_dxybs", "; jet-mu #DeltaR; genmu1's dxybs", 60, 0, 6, 20, 0, 0.2);
    nd.book(k_jeteledr_genele1_dxybs, "jeteledr_genele1_dxybs", "; jet-ele #DeltaR; genele1's dxybs", 60, 0, 6, 20, 0, 0.2);
    // nd.book(k_jetdphi_qrk0_dxybs, "jetdphi_qrk0_dxybs", "; jets' #DeltaPhi; quark0's dxybs", 70, 0, 7, 20, 0, 0.2);
    nd.book(k_jetmudphi_qrk0_dxybs, "jetmudphi_qrk0_dxybs", "; jet-mu #DeltaPhi; quark0's dxybs", 70, 0, 7, 20, 0, 0.2);
    nd.book(k_jeteledphi_qrk0_dxybs, "jeteledphi_qrk0_dxybs", "; jet-ele #DeltaPhi; quark0's dxybs", 70, 0, 7, 20, 0, 0.2);
    // nd.book(k_jetdphi_qrk1_dxybs, "jetdphi_qrk1_dxybs", "; jets' #DeltaPhi; quark1's dxybs", 70, 0, 7, 20, 0, 0.2);
    nd.book(k_jetmudphi_genmu1_dxybs, "jetmudphi_genmu1_dxybs", "; jet-mu #DeltaPhi; genmu1's dxybs", 70, 0, 7, 20, 0, 0.2);
    nd.book(k_jeteledphi_genele1_dxybs, "jeteledphi_genele1_dxybs", "; jet-ele #DeltaPhi; genele1's dxybs", 70, 0, 7, 20, 0, 0.2);
    nd.book(k_closeseedtks_qrk0_dxybs, "closeseedtks_qrk0_dxybs", "; # seed tracks close to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    // nd.book(k_closeseedtks_qrk1_dxybs, "closeseedtks_qrk1_dxybs", "; # seed tracks close to artificial vtx; quark1's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_closeseedtks_genmu1_dxybs, "closeseedtks_genmu1_dxybs", "; # seed tracks close to artificial vtx; genmu1's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_closeseedtks_genele1_dxybs, "closeseedtks_genele1_dxybs", "; # seed tracks close to artificial vtx; genele1's dxybs", 25, 0, 25, 20, 0, 0.2);
    // nd.book(k_nmovedtks_jet_dr, "nmovedtks_jet_dr", "; # quality tracks associated to artificial vtx; jets' #DeltaR", 25, 0, 25, 60, 0, 6.0);
    nd.book(k_nmovedtks_jetmu_dr, "nmovedtks_jetmu_dr", "; # quality tracks associated to artificial vtx; jet-mu #DeltaR", 25, 0, 25, 60, 0, 6.0);
    nd.book(k_nmovedtks_jetele_dr, "nmovedtks_jetele_dr", "; # quality tracks associated to artificial vtx; jet-ele #DeltaR", 25, 0, 25, 60, 0, 6.0);
    nd.book(k_nmovedtks0_qrk0_dxybs, "nmovedtks0_qrk0_dxybs", "; # quality tracks in jet0 associated to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    // nd.book(k_nmovedtks1_qrk1_dxybs, "nmovedtks1_qrk1_dxybs", "; # quality tracks in jet1 associated to artificial vtx; quark1's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_nmovedseedtks0_qrk0_dxybs, "nmovedseedtks0_qrk0_dxybs", "; # seed tracks in jet0 associated to artificial vtx; quark0's dxybs", 25, 0, 25, 20, 0, 0.2);
    // nd.book(k_nmovedseedtks1_qrk1_dxybs, "nmovedseedtks1_qrk1_dxybs", "; # seed tracks in jet1 associated to artificial vtx; quark1's dxybs", 25, 0, 25, 20, 0, 0.2);
    nd.book(k_nmovedtks0_jet0_sump, "nmovedtks0_jet0_sump", "; # quality tracks in jet0 associated to artificial vtx; jet0-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    // nd.book(k_nmovedtks1_jet1_sump, "nmovedtks1_jet1_sump", "; # quality tracks in jet1 associated to artificial vtx; jet1-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    nd.book(k_nmovedseedtks0_jet0_sump, "nmovedseedtks0_jet0_sump", "; # seed tracks in jet0 associated to artificial vtx; jet0-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    // nd.book(k_nmovedseedtks1_jet1_sump, "nmovedseedtks1_jet1_sump", "; # seed tracks in jet1 associated to artificial vtx; jet1-movedquality-track's sum p", 25, 0, 25, 20, 0, 80);
    nd.book(k_nmovedtks_movedist3, "nmovedtks_movedist3", "; # quality tracks associated to artificial vtx;  movement 3-dist", 25, 0, 25, 20, 0, 4.0);
    nd.book(k_nmovedseedtks_movedist3, "nmovedseedtks_movedist3", "; # seed tracks associated to artificial vtx;  movement 3-dist", 25, 0, 25, 20, 0, 4.0);
    nd.book(k_jet0_sump_movedist3, "jet0_sump_movedist3", "; jet0-movedquality-track's sum p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0);
    // nd.book(k_jet1_sump_movedist3, "jet1_sump_movedist3", "; jet1-movedquality-track's sum p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0);
    nd.book(k_mu1_p_movedist3, "mu1_sump_movedist3", "; mu1-movedquality-track's p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0);
    nd.book(k_ele1_p_movedist3, "ele1_sump_movedist3", "; ele1-movedquality-track's p;  movement 3-dist", 20, 0, 80, 20, 0, 4.0);
    nd.book(k_jet0_sump_qrk0_dxybs, "jet0_sump_qrk0_dxybs", "; jet0-movedquality-track's sum p;  quark0's dxybs", 20, 0, 80, 20, 0, 0.2);
    // nd.book(k_jet1_sump_qrk1_dxybs, "jet1_sump_qrk1_dxybs", "; jet1-movedquality-track's sum p;  quark1's dxybs", 20, 0, 80, 20, 0, 0.2);
    nd.book(k_mu1_p_genmu1_dxybs, "mu1_p_genmu1_dxybs", "; mu1-movedquality-track's p;  genmu1's dxybs", 20, 0, 80, 20, 0, 0.2);
    nd.book(k_ele1_p_genele1_dxybs, "ele1_p_genele1_dxybs", "; ele1-movedquality-track's p;  genele1's dxybs", 20, 0, 80, 20, 0, 0.2);
    nd.book(k_qrktosump_j0, "qrktosump_j0", "; #frac{jet0-movedquality-track's sum p}{quark0's p}; arb. units", 50, 0, 1);
    // nd.book(k_qrk0_matchthres, "qrk0_matchthres", "; quark0's matchthres; arb. units", 100, 0, 10);
    // nd.book(k_qrk1_matchthres, "qrk1_macththres", "; quark1's matchthres; arb. units", 100, 0, 10);
    nd.book(k_qrk0_p, "qrk0_p", "; quark0's p; arb. units", 100, 0, 100);
    // nd.book(k_qrk1_p, "qrk1_p", "; quark1's p; arb. units", 100, 0, 100);
    nd.book(k_genmu1_p, "genele1_p", "; genmu1's p; arb. units", 100, 0, 100);
    nd.book(k_genele1_p, "genmu1_p", "; genele1's p; arb. units", 100, 0, 100);
    nd.book(k_qrk0_dxybs, "qrk0_dxybs", "; quark0's dxybs; arb. units", 50, 0.0, 0.2);
    // nd.book(k_qrk1_dxybs, "qrk1_dxybs", "; quark1's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_genmu1_dxybs, "genmu1_dxybs", "; genmu1's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_genele1_dxybs, "genele1_dxybs", "; genele1's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_jet0_dxybs, "jet0_dxybs", "; jet0's dxybs; arb. units", 50, 0.0, 0.2);
    // nd.book(k_jet1_dxybs, "jet1_dxybs", "; jet1's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_mu1_dxybs, "mu1_dxybs", "; mu1's dxybs; arb. units", 50, 0.0, 0.2);
    nd.book(k_ele1_dxybs, "ele1_dxybs", "; ele1's dxybs; arb. units", 50, 0.0, 0.2);
    // nd.book(k_qrk0_mingendxy, "qrk0_mingendxy", "; quark0's matched track gennsigmadxy; arb. units", 100, 0.0, 5.0);
    // nd.book(k_qrk1_mingendxy, "qrk1_mingendxy", "; quark1's matched track gennsigmadxy; arb. units", 100, 0.0, 5.0);
    // nd.book(k_qrktosump_j1, "qrktosump_j1", "; #frac{jet1-movedquality-track's sum p}{quark1's p}; arb. units", 50, 0, 1);
    nd.book(k_genmutop_mu1, "genmutop_mu1", "; #frac{mu1-movedquality-track's p}{mu1's p}; arb. units", 50, 0, 1);
    nd.book(k_geneletop_ele1, "geneletop_ele1", "; #frac{ele1-movedquality-track's p}{ele1's p}; arb. units", 50, 0, 1);
    nd.book(k_qrktosump_sumpj0, "qrktosump_sumpj0", "; jet0-movedquality-track's sum p; #frac{jet0-movedquality-track's sum p}{quark0's p}; arb. units", 50, 0, 50, 50, 0, 1);
    // nd.book(k_qrktosump_sumpj1, "qrktosump_sumpj1", "; jet1-movedquality-track's sum p; #frac{jet1-movedquality-track's sum p}{quark1's p}; arb. units", 50, 0, 50, 50, 0, 1);
    nd.book(k_genmutosump_sumpmu1, "genmutosump_sumpmu1", "; mu1-movedquality-track's p; #frac{mu1-movedquality-track's p}{mu1's p}; arb. units", 50, 0, 50, 50, 0, 1);
    nd.book(k_geneletosump_sumpele1, "geneletosump_sumpele1", "; ele1-movedquality-track's p; #frac{ele1-movedquality-track's p}{ele1's p}; arb. units", 50, 0, 50, 50, 0, 1);
    // nd.book(k_2p0p1_1mgencos, "2p0p1_1mgencos", "; log(2*p_{quark0}*p_{quark1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2p0p1_1mgencos_mu, "2p0p1_1mgencos_mu", "; log(2*p_{quark0}*p_{genmu1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2p0p1_1mgencos_ele, "2p0p1_1mgencos_ele", "; log(2*p_{quark0}*p_{genele1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    // nd.book(k_2sump0sump1_1mcos, "2sump0sump1_1mcos", "; log(2*sump_{tk0}*sump_{tk1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2sump0sump1_1mcos_mu, "2sump0sump1_1mcos_mu", "; log(2*sump_{tk0}*p_{mu1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    nd.book(k_2sump0sump1_1mcos_ele, "2sump0sump1_1mcos_ele", "; log(2*sump_{tk0}*p_{ele1}); log(1-cos(#Delta#Theta))", 70, 0, 7, 20, -2, 0);
    // nd.book(k_1mcosto1mgencos, "1mcosto1mgencos", "; #frac{1-cos(#Delta#Theta)_{minijet}}{1-cos(#Delta#Theta)_{GEN}}", 20, 0, 1);
    // nd.book(k_2logm, "2logm", "; log(2*sump_{tk0}*sump_{tk1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_2logm_mu, "2logm_mu", "; log(2*sump_{tk0}*p_{mu1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_2logm_ele, "2logm_ele", "; log(2*sump_{tk0}*p_{ele1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    // nd.book(k_2genlogm, "2genlogm", "; log(2*p_{quark0}*p_{quark1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_2genlogm_mu, "2genlogm_mu", "; log(2*p_{quark0}*p_{genmu1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    nd.book(k_2genlogm_ele, "2genlogm_ele", "; log(2*p_{quark0}*p_{genele1}) + log(1-cos(#Delta#Theta))", 70, 0, 7);
    // nd.book(k_asymjet_jetdr, "asymjet_jetdr", ";jet's quality tracks sum mom. asymm. A_{J}; jets's movedquality-track p4 #DeltaR ", 20, -1, 1, 60, 0, 6.0);
    nd.book(k_asymjetmu_jetmudr, "asymjetmu_jetmudr", ";mu mom. - jet's quality tracks sum mom. asymm. A_{J}; jet-mu movedquality-track p4 #DeltaR ", 20, -1, 1, 60, 0, 6.0);
    nd.book(k_asymjetele_jeteledr, "asymjetele_jeteledr", ";ele mom. - jet's quality tracks sum mom. asymm. A_{J}; jet-ele movedquality-track p4 #DeltaR ", 20, -1, 1, 60, 0, 6.0);
    // nd.book(k_jet0_trk_dr, "jet0_trk_dr", "; jet0-movedquality-track's DeltaR-to-jet; arb. units", 45, 0, 0.5);
    // nd.book(k_jet1_trk_dr, "jet1_trk_dr", "; jet1-movedquality-track's DeltaR-to-jet; arb. units", 45, 0, 0.5);
    nd.book(k_jet0_trk_dr_gennsigma, "jet0_trk_dr_gennsigma", "; jet0-movedquality-track's DeltaR-to-jet; jet0-movedquality-track's n#sigma to LLP; arb. units", 45, 0, 0.5, 120, 0, 30);
    // nd.book(k_jet1_trk_dr_gennsigma, "jet1_trk_dr_gennsigma", "; jet1-movedquality-track's DeltaR-to-jet; jet1-movedquality-track's n#sigma to LLP; arb. units", 45, 0, 0.5, 120, 0, 30);
    nd.book(k_jet0_trk_dr_genmissdist, "jet0_trk_dr_genmissdist", "; jet0-movedquality-track's DeltaR-to-jet; jet0-movedquality-track's missdist to LLP; arb. units", 45, 0, 0.5, 50, -0.05, 0.05);
    // nd.book(k_jet1_trk_dr_genmissdist, "jet1_trk_dr_genmissdist", "; jet1-movedquality-track's DeltaR-to-jet; jet1-movedquality-track's missdist to LLP; arb. units", 45, 0, 0.5, 50, -0.05, 0.05);
    nd.book(k_jet0_trk_dr_gendz, "jet0_trk_dr_gendz", "; jet0-movedquality-track's DeltaR-to-jet; jet0-movedquality-track's dz to LLP; arb. units", 45, 0, 0.5, 50, -0.05, 0.05);
    // nd.book(k_jet1_trk_dr_gendz, "jet1_trk_dr_gendz", "; jet1-movedquality-track's DeltaR-to-jet; jet1-movedquality-track's dz to LLP; arb. units", 45, 0, 0.5, 50, -0.05, 0.05);
    nd.book(k_jet0_trk_eta_gennsigma, "jet0_trk_eta_gennsigma", "; jet0-movedquality-track's eta; jet0-movedquality-track's n#sigma to LLP; arb. units", 70, -3.5, 3.5, 120, 0, 30);
    // nd.book(k_jet1_trk_eta_gennsigma, "jet1_trk_eta_gennsigma", "; jet1-movedquality-track's eta; jet1-movedquality-track's n#sigma to LLP; arb. units", 70, -3.5, 3.5, 120, 0, 30);
    nd.book(k_jet0_trk_eta_gendz, "jet0_trk_eta_gendz", "; jet0-movedquality-track's eta; jet0-movedquality-track's dz to LLP; arb. units", 70, -3.5, 3.5, 50, -0.05, 0.05);
    // nd.book(k_jet1_trk_eta_gendz, "jet1_trk_eta_gendz", "; jet1-movedquality-track's eta; jet1-movedquality-track's dz to LLP; arb. units", 70, -3.5, 3.5, 50, -0.05, 0.05);
    nd.book(k_jet0_trk_dz, "jet0_trk_dz", "; jet0-movedquality-track's dz; arb. units", 50, -1.0, 1.0);
    // nd.book(k_jet1_trk_dz, "jet1_trk_dz", "; jet1-movedquality-track's dz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_vtxdxy, "jet0_trk_vtxdxy", "; jet0-movedquality-track's dxy to vtx; arb. units", 50, -1.0, 1.0);
    // nd.book(k_jet1_trk_vtxdxy, "jet1_trk_vtxdxy", "; jet1-movedquality-track's dxy to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_vtxdz, "jet0_trk_vtxdz", "; jet0-movedquality-track's dz to vtx; arb. units", 50, -1.0, 1.0);
    // nd.book(k_jet1_trk_vtxdz, "jet1_trk_vtxdz", "; jet1-movedquality-track's dz to vtx; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_nsigmavtxdz, "jet0_trk_nsigmavtxdz", "; jet0-movedquality-track's nsigmavtxdz; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_nsigmavtxdz, "jet1_trk_nsigmavtxdz", "; jet1-movedquality-track's nsigmavtxdz; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_nsigmavtxdxy, "jet0_trk_nsigmavtxdxy", "; jet0-movedquality-track's nsigmavtxdxy; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_nsigmavtxdxy, "jet1_trk_nsigmavtxdxy", "; jet1-movedquality-track's nsigmavtxdxy; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_nsigmavtx, "jet0_trk_nsigmavtx", "; jet0-movedquality-track's nsigmavtx; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_nsigmavtx, "jet1_trk_nsigmavtx", "; jet1-movedquality-track's nsigmavtx; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_dzerr, "jet0_trk_dzerr", "; jet0-movedquality-track's dz err; arb. units", 100, 0.0, 0.05);
    // nd.book(k_jet1_trk_dzerr, "jet1_trk_dzerr", "; jet1-movedquality-track's dz err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet0_trk_nsigmadz, "jet0_trk_nsigmadz", "; jet0-movedquality-track's n#sigma dzpv; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_nsigmadz, "jet1_trk_nsigmadz", "; jet1-movedquality-track's n#sigma dzpv; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_dxyerr, "jet0_trk_dxyerr", "; jet0-movedquality-track's dxy err; arb. units", 100, 0.0, 0.05);
    // nd.book(k_jet1_trk_dxyerr, "jet1_trk_dxyerr", "; jet1-movedquality-track's dxy err; arb. units", 100, 0.0, 0.05);
    nd.book(k_jet0_trk_eta, "jet0_trk_eta", "; jet0-movedquality-track's eta; arb. units", 70, -3.5, 3.5);
    // nd.book(k_jet1_trk_eta, "jet1_trk_eta", "; jet1-movedquality-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_movedseedinvtx_trk_whichjet, "movedseedinvtx_trk_whichjet", "; movedquality-invtx-track's whichjet; arb. units", 258, 0.0, 258.0);
    nd.book(k_miscclose_trk_whichjet, "miscclose_trk_whichjet", "; misc-closeseed-track's whichjet; arb. units", 258, 0.0, 258.0);
    
    nd.book(k_miscclose_trk_p, "miscclose_trk_p", "; misc-closeseed-track's p; arb. units", 45, 0, 15);
    nd.book(k_miscclose_trk_eta, "miscclose_trk_eta", "; misc-closeseed-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_miscclose_trk_dzerr, "miscclose_trk_dzerr", "; misc-closeseed-track's dzerr; arb. units", 100, 0.0, 0.05);
    nd.book(k_movedseedinvtx_trk_dsz, "movedseedinvtx_trk_dsz", "; movedquality-invtx-track's dzsin#theta; arb. units", 50, -0.5, 0.5);
    nd.book(k_miscclose_trk_dsz, "miscclose_trk_dsz", "; misc-closeseed-track's dzsin#theta; arb. units", 50, -0.5, 0.5);
    nd.book(k_movedseedoutvtx_trk_eta, "movedseedoutvtx_trk_eta", "; movedquality-outvtx-10n#sigma-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_movedseedinvtx_trk_eta, "movedseedinvtx_trk_eta", "; movedquality-invtx-track's eta; arb. units", 70, -3.5, 3.5);
    nd.book(k_movedseedoutvtx_trk_p, "movedseedoutvtx_trk_p", "; movedquality-outvtx-10n#sigma-track's p; arb. units", 45, 0, 15);
    nd.book(k_movedseedinvtx_trk_p, "movedseedinvtx_trk_p", "; movedquality-invtx-track's p; arb. units", 45, 0, 15);
    nd.book(k_movedseedoutvtx_trk_dz, "movedseedoutvtx_trk_dz", "; movedquality-outvtx-10n#sigma-track's dzpv; arb. units", 50, -1.0, 1.0);
    nd.book(k_movedseedinvtx_trk_dz, "movedseedinvtx_trk_dz", "; movedquality-invtx-track's dzpv; arb. units", 50, -1.0, 1.0);
    nd.book(k_movedseedoutvtx_trk_gennsigma, "movedseedoutvtx_trk_gennsigma", "; movedquality-outvtx-10n#sigma-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_movedseedinvtx_trk_gennsigma, "movedseedinvtx_trk_gennsigma", "; movedquality-invtx-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_movedseedoutvtx_trk_dr, "movedseedoutvtx_trk_dr", "; movedquality-outvtx-10n#sigma-track's #DeltaR to quark; arb. units", 50, 0, 0.5);
    nd.book(k_movedseedinvtx_trk_dr, "movedseedinvtx_trk_dr", "; movedquality-invtx-track's #DeltaR to quark; arb. units", 50, 0, 0.5);
    nd.book(k_movedseedoutvtx_trk_whichpv, "movedseedoutvtx_trk_whichpv", "; movedquality-outvtx-10n#sigma-track's whichpv; arb. units", 258, 0, 258);
    nd.book(k_movedseedinvtx_trk_whichpv, "movedseedinvtx_trk_whichpv", "; movedquality-invtx-track's whichpv; arb. units", 258, 0, 258);
    nd.book(k_movedseedoutvtx_trk_dzerr, "movedseedoutvtx_trk_dzerr", "; movedquality-outvtx-10n#sigma-track's dzerr; arb. units", 100, 0.0, 0.05);
    nd.book(k_movedseedinvtx_trk_dzerr, "movedseedinvtx_trk_dzerr", "; movedquality-invtx-track's dzerr; arb. units", 100, 0, 0.05);
    nd.book(k_movedseedoutvtx_trk_dxyerr, "movedseedoutvtx_trk_dxyerr", "; movedquality-outvtx-10n#sigma-track's dxyerr; arb. units", 100, 0.0, 0.05);
    nd.book(k_movedseedinvtx_trk_dxyerr, "movedseedinvtx_trk_dxyerr", "; movedquality-invtx-track's dxyerr; arb. units", 100, 0, 0.05);
    nd.book(k_closeseed_trk_genmissdist, "closeseed_trk_genmissdist", "; close-seed-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gendz, "closeseed_trk_gendz", "; close-seed-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_closeseed_trk_gennsigmadz, "closeseed_trk_gennsigmadz", "; close-seed-track's gennsigmadz; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gennsigma, "jet0_trk_gennsigma", "; jet0-movedquality-track's n#sigma to LLP; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_gennsigma, "jet1_trk_gennsigma", "; jet1-movedquality-track's n#sigma to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gennsigmamissdist, "jet0_trk_gennsigmamissdist", "; jet0-movedquality-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_gennsigmamissdist, "jet1_trk_gennsigmamissdist", "; jet1-movedquality-track's n#sigma missdist to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_genmissdist, "jet0_trk_genmissdist", "; jet0-movedquality-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    // nd.book(k_jet1_trk_genmissdist, "jet1_trk_genmissdist", "; jet1-movedquality-track's missdist to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_gennsigmadz, "jet0_trk_gennsigmadz", "; jet0-movedquality-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_gennsigmadz, "jet1_trk_gennsigmadz", "; jet1-movedquality-track's n#sigma dz to LLP; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_gendz, "jet0_trk_gendz", "; jet0-movedquality-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    // nd.book(k_jet1_trk_gendz, "jet1_trk_gendz", "; jet1-movedquality-track's dz to LLP; arb. units", 50, -0.05, 0.05);
    nd.book(k_jet0_trk_whichpv, "jet0_trk_whichpv", "; jet1-movedquality-track's which_pv; arb. units", 260, 0.0, 260);
    // nd.book(k_jet1_trk_whichpv, "jet1_trk_whichpv", "; jet1-movedquality-track's which_pv; arb. units", 260, 0.0, 260);
    nd.book(k_jet0_trk_dsz, "jet0_trk_dsz", "; jet0-movedquality-track's dsz; arb. units", 50, -1.0, 1.0);
    // nd.book(k_jet1_trk_dsz, "jet1_trk_dsz", "; jet1-movedquality-track's dsz; arb. units", 50, -1.0, 1.0);
    nd.book(k_jet0_trk_nsigmadsz, "jet0_trk_nsigmadsz", "; jet0-movedquality-track's nsigmadsz; arb. units", 80, -10, 10);
    // nd.book(k_jet1_trk_nsigmadsz, "jet1_trk_nsigmadsz", "; jet1-movedquality-track's nsigmadsz; arb. units", 80, -10, 10);
    nd.book(k_jet0_trk_dxy, "jet0_trk_dxy", "; jet0-movedquality-track's dxybs; arb. units", 50, -0.5, 0.5);
    // nd.book(k_jet1_trk_dxy, "jet1_trk_dxy", "; jet1-movedquality-track's dxybs; arb. units", 50, -0.5, 0.5);
    nd.book(k_jet0_trk_nsigmadxy, "jet0_trk_nsigmadxy", "; jet0-movedquality-track's nsigmadxybs; arb. units", 160, -20, 20);
    // nd.book(k_jet1_trk_nsigmadxy, "jet1_trk_nsigmadxy", "; jet1-movedquality-track's nsigmadxybs; arb. units", 160, -20, 20);
    nd.book(k_nmovedtracks, "nmovedtracks", ";# moved tracks;events/2", 30, 0, 30);
    nd.book(k_dphi_sum_jmu_mv, "dphi_sum_jmu_mv", ";abs #Delta #phi between jet0+mu1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_sum_jmu_mv, "deta_sum_jmu_mv", ";abs #Delta #eta between jet0+mu1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_sum_qgm_mv, "dphi_sum_qgm_mv", ";abs #Delta #phi between jet0+mu1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_sum_jele_mv, "dphi_sum_jele_mv", ";abs #Delta #phi between jet0+ele1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_sum_jele_mv, "deta_sum_jele_mv", ";abs #Delta #eta between jet0+ele1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_sum_qge_mv, "dphi_sum_qge_mv", ";abs #Delta #phi between jet0+ele1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_jetpt0_asymm_mu, "jetpt0_asymm_mu", ";jet p_{T} 0; jet mu asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_jetpt0_asymm_ele, "jetpt0_asymm_ele", ";jet p_{T} 0; jet ele asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    // nd.book(k_jetpt1_asymm, "jetpt1_asymm", ";jet p_{T} 1; jet asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_mupt1_asymm, "mupt1_asymm", ";mu p_{T} 1; jet mu asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    nd.book(k_elept1_asymm, "elept1_asymm", ";ele p_{T} 1; jet ele asymm. A_{J}", 50, 0, 1000, 25, 0, 1);
    // nd.book(k_jeteta0_asymm, "jeteta0_asymm", ";jet #eta 0; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta0_asymm_mu, "jeteta0_asymm_mu", ";jet #eta 0; jet mu asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_jeteta0_asymm_ele, "jeteta0_asymm_ele", ";jet #eta 0; jet ele asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    // nd.book(k_jeteta1_asymm, "jeteta1_asymm", ";jet #eta 1; jet asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_mueta1_asymm, "mueta1_asymm", ";mu #eta 1; jet mu asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    nd.book(k_eleeta1_asymm, "eleeta1_asymm", ";ele #eta 1; jet ele asymm. A_{J}", 100, -4, 4, 25, 0, 1);
    // nd.book(k_jetdr_asymm, "jetdr_asymm", ";jets #DeltaR; jet asymm. A_{J}", 60, 0, 6, 25, 0, 1);
    nd.book(k_jetmudr_asymm, "jetmudr_asymm", ";jet-mu #DeltaR; jet mu asymm. A_{J}", 60, 0, 6, 25, 0, 1);
    nd.book(k_jeteledr_asymm, "jeteledr_asymm", ";jet-ele #DeltaR; jet ele asymm. A_{J}", 60, 0, 6, 25, 0, 1);
    // nd.book(k_jetdravg, "jetdravg", ";avg jet #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jetmudravg, "jetmudravg", ";avg jet-mu #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_jeteledravg, "jeteledravg", ";avg jet-ele #Delta R;events/0.1", 70, 0, 7);
    nd.book(k_angle0, "jetmovea3d0", ";Angle between jet0 and SV;arb. units", 63, 0, M_PI);
    // nd.book(k_angle1, "jetmovea3d1", ";Angle between jet1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_anglemu1, "mumovea3d1", ";Angle between mu1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_angleele1, "elemovea3d1", ";Angle between ele1 and SV;arb. units", 63, 0, M_PI);
    nd.book(k_dphi_j0_mv, "dphi_j0_mv", ";abs #Delta #phi between jet0 and move vec;events/bin", 63, 0, M_PI);
    // nd.book(k_dphi_j1_mv, "dphi_j1_mv", ";abs #Delta #phi between jet1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_mu1_mv, "dphi_mu1_mv", ";abs #Delta #phi between mu1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_ele1_mv, "dphi_ele1_mv", ";abs #Delta #phi between ele1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_deta_j0_mv, "deta_j0_mv", ";abs #Delta #eta between jet0 and move vec;events/bin", 25, 0, 4);
    // nd.book(k_deta_j1_mv, "deta_j1_mv", ";abs #Delta #eta between jet1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_mu1_mv, "deta_mu1_mv", ";abs #Delta #eta between mu1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_deta_ele1_mv, "deta_ele1_mv", ";abs #Delta #eta between ele1 and move vec;events/bin", 25, 0, 4);
    nd.book(k_dphi_q0_mv, "dphi_q0_mv", ";abs #Delta #phi between qrk0 and move vec;events/bin", 63, 0, M_PI);
    // nd.book(k_dphi_q1_mv, "dphi_q1_mv", ";abs #Delta #phi between qrk1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_genmu1_mv, "dphi_genmu1_mv", ";abs #Delta #phi between genmu1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_dphi_genele1_mv, "dphi_genele1_mv", ";abs #Delta #phi between genele1 and move vec;events/bin", 63, 0, M_PI);
    nd.book(k_nseedtracks, "nseedtracks", ";# seed tracks;events", 80, 0, 80);
    nd.book(k_miscseedtracks, "miscseedtracks", ";#Sigma seed tks not from moved jets;count", 30, 0, 30);
    nd.book(k_misccloseseedtracks, "misccloseseedtracks", ";#Sigma seed tks 5#sigma to artificial vtx not from moved jets;count", 20, 0, 20);
    nd.book(k_closeseedtks,  "closeseedtks", ";# seed tracks close to artificial vtx.;count", 80, 0, 80);
    nd.book(k_sharedcloseseedtks,  "sharedcloseseedtks", ";# seed tracks close to both artificial vtx.;count", 20, 0, 20);
    nd.book(k_tightcloseseedtks,  "tightcloseseedtks", ";# seed tracks 2#sigma-close to artificial vtx.;count", 25, 0, 25);
    nd.book(k_movedseedtks,  "movedseedtks", ";# moved seed tracks;count", 30, 0, 30);
    nd.book(k_movedvtxseedtks,  "movedvtxseedtks", ";# moved seed tracks in vtx;count", 30, 0, 30);
    nd.book(k_movedcloseseedtks,  "movedcloseseedtks", ";# moved seed tracks 5#sigma to LLP;count", 30, 0, 30);
    nd.book(k_rat_moved_to_closetks, "rat_moved_to_closetks", ";#frac{# moved seed tracks 5#sigma to LLP}{# seed tracks 5#sigma to LLP};count", 50, 0, 1);
    nd.book(k_rat_moved_to_vtxtks, "rat_moved_to_vtxtks", ";#frac{# moved seed tracks in vtx}{# vtx ntrack};count", 50, 0, 1);
    nd.book(k_rat_movedvtxtks_to_movedtks, "rat_movedvtxtks_to_movedtks", ";#frac{# moved seed tracks in vtx}{# moved seed tracks};count", 50, 0, 1);
    nd.book(k_rat_movedclosetks_to_movedtks, "rat_movedclosetks_to_movedtks", ";#frac{# moved seed tracks 5#sigma to LLP}{# moved seed tracks};count", 50, 0, 1);
    // nd.book(k_jetdphimax, "jetdphimax", ";max jet #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jetmudphimax, "jetmudphimax", ";max jet-mu #Delta #phi; events", 32, -M_PI, M_PI);
    nd.book(k_jeteledphimax, "jeteledphimax", ";max jet-ele #Delta #phi; events", 32, -M_PI, M_PI);
    // nd.book(k_jetdetamax, "jetdetamax", ";max jet #Delta #eta; events", 200, -5, 5);
    nd.book(k_jetmudetamax, "jetmudetamax", ";max jet-mu #Delta #eta; events", 200, -5, 5);
    nd.book(k_jeteledetamax, "jeteledetamax", ";max jet-ele #Delta #eta; events", 200, -5, 5);
    // nd.book(k_qrkdphimax, "qrkdphimax", ";abs. max qrk #Delta #phi; events", 75, -3.5, 3.5);
    nd.book(k_qrkgenmudphimax, "qrkgenmudphimax", ";abs. max qrk genmu #Delta #phi; events", 75, -3.5, 3.5);
    nd.book(k_qrkgeneledphimax, "qrkgeneledphimax", ";abs. max qrk genele #Delta #phi; events", 75, -3.5, 3.5);
    // nd.book(k_jetdphi_mveta, "jetdphi_mveta", ";abs(max jet #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);
    nd.book(k_jetmudphi_mveta, "jetmudphi_mveta", ";abs(max jet, mu #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);
    nd.book(k_jeteledphi_mveta, "jeteledphi_mveta", ";abs(max jet, ele #Delta #phi);abs( #eta of disp. vector)", 32, 0, M_PI, 40, 0, 4);
    // nd.book(k_jetmovea3d01, "jetmovea3d", ";3D angle between jet 0 and move vector;3D angle between jet 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_jetmumovea3d01, "jetmumovea3d", ";3D angle between jet 0 and move vector;3D angle between mu 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    nd.book(k_jetelemovea3d01, "jetelemovea3d", ";3D angle between jet 0 and move vector;3D angle between ele 1 and move vector", 63, 0, M_PI, 63, 0, M_PI);
    // nd.book(k_jeteta01, "jeteta01", ";jet #eta 0 (GeV);jet #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    nd.book(k_jetmueta01, "jetmueta01", ";jet #eta 0 (GeV);mu #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    nd.book(k_jeteleeta01, "jeteleeta01", ";jet #eta 0 (GeV);ele #eta 1 (GeV)", 100, -4, 4, 100, -4, 4);
    // nd.book(k_jetpt01, "jetpt01", ";jet p_{T} 0 (GeV);jet p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_jetmupt01, "jetmupt01", ";jet p_{T} 0 (GeV);mu p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_jetelept01, "jetelept01", ";jet p_{T} 0 (GeV);ele p_{T} 1 (GeV)", 50, 0, 1000, 50, 0, 1000);
    nd.book(k_pt_angle0,     "pt_angle0"    , ";Pt of jet0 [GeV]; Angle between jet0 and SV", 50, 0, 2500, 63, 0, M_PI);
    // nd.book(k_pt_angle1,     "pt_angle1"    , ";Pt of jet1 [GeV]; Angle between jet1 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_pt_anglemu1,     "pt_anglemu1"    , ";Pt of mu1 [GeV]; Angle between mu1 and SV", 50, 0, 2500, 63, 0, M_PI);
    nd.book(k_pt_angleele1,     "pt_angleele1"    , ";Pt of ele1 [GeV]; Angle between ele1 and SV", 50, 0, 2500, 63, 0, M_PI);

    nd.book(k_eta_angle0,    "eta_angle0"  , ";Eta of SV decay vector; Angle between jet0 and SV", 60, -5, 5, 63, 0, M_PI);
    // nd.book(k_eta_angle1,    "eta_angle1"  , ";Eta of SV decay vector; Angle between jet1 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_eta_anglemu1,    "eta_anglemu1"  , ";Eta of SV decay vector; Angle between mu1 and SV", 60, -5, 5, 63, 0, M_PI);
    nd.book(k_eta_angleele1,    "eta_angleele1"  , ";Eta of SV decay vector; Angle between ele1 and SV", 60, -5, 5, 63, 0, M_PI);

    nd.book(k_nvtx, "nvtx", ";number of vertices;events/1", 8, 0, 8);
    nd.book(k_vtxcat, "vtxcat", ";no-vtx:fail vtxunc: fail dbv: fail both;events", 6, 0, 6);
    nd.book(k_vtxbs2derr, "vtxbs2derr", ";bs2derr of vertex;events", 500, 0, 0.05);
    nd.book(k_vtxunc, "vtxunc", ";dist3d(move vector, vtx) cm; arb. units", 200, 0, 0.2);
    nd.book(k_vtxeta, "vtxeta", ";eta of vertex;events", 100, -4, 4);
    nd.book(k_vtxz, "vtxz", ";z pos of vertex;events", 100, -10, 10);
    nd.book(k_vtxdbv, "vtxdbv", ";2D displacement of vertex to a beamspot;events", 50, 0, 2); //FIXME
    nd.book(k_vtx3dbv, "vtx3dbv", ";3D displacement of vertex to a beamspot;events", 50, 0, 2);
    nd.book(k_vtxntk, "vtxntk", ";ntrack of vertex;events", 20, 0, 20);
    nd.book(k_dr, "dr", "; #Delta R separation of LLPs;events", 70, 0, 7);
    nd.book(k_dvv, "dvv", "; 3D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_dvv_2vtx, "dvv_2vtx", "; 3D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_movedist3_movedist2_2vtx, "movedist3_movedist2_2vtx", "; movement 3-dist; movement 2-dist", 50, 0, 4.0, 50, 0, 2.5); 
    nd.book(k_dvv2d, "dvv2d", "; 2D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_vtxnm1_dbv, "vtxnm1_dbv", ";2D displacement of n-1-vertex to a beamspot;events", 50, 0, 2.0); 
    nd.book(k_vtxnm1_ntk, "vtxnm1_ntk", ";ntrack of n-1-vertex;events", 20, 0, 20);
    nd.book(k_vtxnm1_bs2derr, "vtxnm1_bs2derr", ";bs2derr of n-1-vertex;events", 500, 0, 0.05);
    nd.book(k_vtx3tkchi2, "vtx3tkchi2", ";norm-chi2/3tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx3tkdbv, "vtx3tkdbv", ";2D-displacement of a vtx/3tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx3tkdvv, "vtx3tkdvv", "; 3D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_vtx3tkzdbv, "vtx3tkzdbv", ";z-displacement of a vtx/3tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx3tkunc, "vtx3tkunc", ";3D-distance of a vtx to an LLP/3tk-vtx cm. ;events", 100, 0, 0.04);
    nd.book(k_vtx4tkchi2, "vtx4tkchi2", ";norm-chi2/4tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx4tkdbv, "vtx4tkdbv", ";2D-displacement of a vtx/4tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx4tkdvv, "vtx4tkdvv", "; 3D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_vtx4tkzdbv, "vtx4tkzdbv", ";z-displacement of a vtx/4tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx4tkunc, "vtx4tkunc", ";3D-distance of a vtx to an LLP/4tk-vtx cm. ;events", 100, 0, 0.04);
    nd.book(k_vtx5tkchi2, "vtx5tkchi2", ";norm-chi2/5tk-vtx;events", 20, 0, 5.0);
    nd.book(k_vtx5tkdbv, "vtx5tkdbv", ";2D-displacement of a vtx/5tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx5tkdvv, "vtx5tkdvv", "; 3D separation of LLP decay points;events", 200, 0, 0.5);
    nd.book(k_vtx5tkzdbv, "vtx5tkzdbv", ";z-displacement of a vtx/5tk-vtx cm. ;events", 200, 0, 0.2);
    nd.book(k_vtx5tkunc, "vtx5tkunc", ";3D-distance of a vtx to an LLP/5tk-vtx cm. ;events", 100, 0, 0.04);
  }

  TH1D* h_vtxntracks[num_numdens] = {0};
  TH1D* h_vtxbs2derr[num_numdens] = {0};
  //TH1D* h_vtxtkonlymass[num_numdens] = {0}; // JMTBAD interface for vertex_tracks common to Mini2 and MovedTracks ntuples
  TH1D* h_vtxs_mass[num_numdens] = {0};

  for (int i = 0; i < num_numdens; ++i) {
    h_vtxntracks[i] = new TH1D(TString::Format("h_%i_vtxntracks",      i), ";# tracks in largest vertex;events/1", 40, 0, 40);
    h_vtxbs2derr[i] = new TH1D(TString::Format("h_%i_vtxbs2derr",      i), ";#sigma(d_{BV}) of largest vertex (cm);events/2 #mum", 50, 0, 0.01);
    //h_vtxtkonlymass[i] = new TH1D(TString::Format("h_%i_vtxtkonlymass", i), ";track-only mass of largest vertex (GeV);events/1 GeV", 500, 0, 500);
    h_vtxs_mass[i] = new TH1D(TString::Format("h_%i_vtxs_mass", i), ";track+jets mass of largest vertex (GeV);vertices/50 GeV", 100, 0, 5000);
  }

  double den = 0;

  std::map<std::string, double> nums;
  std::map<std::string, double> nums_2vtx;

  auto fcn = [&]() {
    const double w = nr.weight();
    // First part of the preselection: our offline jet requirements
    // plus require the lsps to be far enough apart that they don't
    // interfere with each other in reconstruction
    if (!gen.valid() || gen.lspdist3() < min_lspdist3) //FIXME 
      NR_loop_cont(w);

    for (numdens& nd : nds)
      nd.setw(w);


    const size_t nvtx = vs.n();
    const double lspdist2 = gen.lspdist2();
    const double lspdist3 = gen.lspdist3();
    const double lspdistz = gen.lspdistz();

    const float  close_criteria = 5.0;  // How close must a seed track pass near an SV to be considered 'close?'
    const float  tight_close_criteria = 2.0;  // How close must a seed track pass near an SV to be considered 'close?'
    std::vector<int> tks_in_lspjets;

    int n_miscseedtracks = 0;
    int n_misccloseseedtracks = 0;
    double n_movedseedtks = 0;
    double n_movedseedtks0 = 0;
    double n_movedseedtks1 = 0;
    // Instantiate some jet, leptons & quark variables to be filled later
    // int nselmuons = 0, nseleles = 0;
    // TLorentzVector muon_p4;
    // TLorentzVector ele_p4;
    // TLorentzVector tmpz_p4;
    // TLorentzVector zee_p4;
    // TLorentzVector zmumu_p4;
    // bool has_Zmumuboson = false;
    // bool has_Zeeboson = false;
    // bool has_Wboson = false;
    // double z_m = -99, zmumu_m = -99, zee_m = -99;
    // double z_pT = -99, zmumu_pT = -99, zee_pT = -99;

    // double muon_pT = -99, ele_pT = -99;
    // double muon_px = -99, ele_px = -99;
    // double muon_py = -99, ele_py = -99;
    // double muon_pz = -99, ele_pz = -99;
    // double muon_q = -99, ele_q = -99;
    // double muon_abseta = -99, ele_abseta = -99;
    // double muon_iso = 99, ele_iso = 99;
    // double muon_absdxybs = -99, ele_absdxybs = -99;
    // double muon_nsigmadxybs = -99, ele_nsigmadxybs = -99;
    // double muon_absdz = -99, ele_absdz = -99;
    // double met_pT = std::hypot(pf.met_x(), pf.met_y());
    // double lnu_absphi = -99, ljet_absdr = -99, ljet0_absdr = -99,  ljet1_absdr = -99, nujet0_absphi = -99, nujet1_absphi = -99;
    // double w_mT = -99;
    // double w_pT = -99;

    // float   jet_aj = -9.9, jet_dr = -9.9, jet_deta = -9.9, jet_dphi = -9.9, jet_dind = -9.9, jet_pt_0 = -9.9, jet_pt_1 = -9.9;
    float   jet_pt_0 = -9.9;
    float   jetele_aj = -9.9, jetele_dr = -9.9, jetele_deta = -9.9, jetele_dphi = -9.9, ele_pt_1 = -9.9;
    float   jetmu_aj = -9.9, jetmu_dr = -9.9, jetmu_deta = -9.9, jetmu_dphi = -9.9, mu_pt_1 = -9.9;
    float   jet_dr_minjq0 = -9.9, ele_dr_minl1 = -9.9, mu_dr_minl1 = -9.9;
    // float   jet_eta_0 = -100.0, jet_eta_1 = -100.0;
    float   jet_eta_0 = -100.0,  ele_eta_1 = -100.0, mu_eta_1 = -100.0;
    // double  jet0_lsp_angle = -9.9, jet1_lsp_angle = -9.9;
    double  jet0_lsp_angle = -9.9, ele1_lsp_angle = -9.9, mu1_lsp_angle=-9.9;
    // double  jet_mv_dphi_0  = 0.0, jet_mv_dphi_1 = 0.0, jet_mv_dphi_sum = 0.0;
    double  jet_mv_dphi_0  = 0.0, ele_mv_dphi_1 = 0.0, mu_mv_dphi_1 = 0.0, jetele_mv_dphi_sum = 0.0, jetmu_mv_dphi_sum = 0.0;
    // double  jet_mv_deta_0  = 0.0, jet_mv_deta_1 = 0.0, jet_mv_deta_sum = 0.0;
    double  jet_mv_deta_0  = 0.0, ele_mv_deta_1 = 0.0, mu_mv_deta_1 = 0.0, jetele_mv_deta_sum = 0.0, jetmu_mv_deta_sum = 0.0;

    // double  qrk_mv_dphi_0  = 0.0, qrk_mv_dphi_1 = 0.0, qrk_mv_dphi_sum = 0.0;
    double  qrk_mv_dphi_0  = 0.0, genele_mv_dphi_1 = 0.0, genmu_mv_dphi_1 = 0.0, qrkgenele_mv_dphi_sum = 0.0, qrkgenmu_mv_dphi_sum = 0.0;

    // double  jet_dphi_max = 0.0;
    // double  jet_deta_max = 0.0;
    // double  qrk_dphi_max = 0.0;
    // int     jet_ntks_0 = -10, jet_ntks_1 = -10;
    double jetele_dphi_max = 0.0, jetmu_dphi_max = 0.0;
    double jetele_deta_max = 0.0, jetmu_deta_max = 0.0;
    double qrkgenele_dphi_max = 0.0, qrkgenmu_dphi_max = 0.0;
    int     jet_ntks_0 = -10;

    double  boost0 = -10, boost1 = -10;
    double n_closeseedtks = 0;
    double n_sharedcloseseedtks = 0;
    int n_movedcloseseedtks = 0;
    int n_tightcloseseedtks = 0;
    int n_movedvtxseedtks = 0;
    const int nseedtracks = tks.nseed(bs);
    double sump_0 = 0;
    // double sump_1 = 0;
    double p_mu1 = 0;
    double p_ele1 = 0;

    //for reco : 
    double mu1_reco_p = 0;
    double mu1_reco_pt = 0;
    double ele1_reco_p = 0;
    double ele1_reco_pt = 0;

    double miscp = 0;
    double sumpreco_0 = 0;
    // double sumpreco_1 = 0;
    // double sumpreco_mu1 = 0;
    // double sumpreco_ele1 =0;

    double maxeta_0 = 0.0;
    // double maxeta_1 = 0.0;


    //double qrk0_mingendxy = 100.0;
    //double qrk1_mingendxy = 100.0;
    double qrk0_dxybs = -9.9;
    // double qrk1_dxybs = -9.9;
    double genmu1_dxybs = -9.9;
    double genele1_dxybs = -9.9;
    double jet0_dxybs = -9.9;
    // double jet1_dxybs = -9.9;
    double ele1_dxybs = -9.9;
    double mu1_dxybs = -9.9;
    double qrkp_0 = -9.9;
    // double qrkp_1 = -9.9;
    double genmup_1 = -9.9;
    double genelep_1 = -9.9;
    //double qrk0_matchthres = -9.9;
    //double qrk1_matchthres = -9.9;
    // double qrk_costheta = -9.9;
    double qrkgenele_costheta = -9.9;
    double qrkgenmu_costheta = -9.9;
    // double jet_costheta = -9.9;
    double jetele_costheta = -9.9;
    double jetmu_costheta = -9.9;
    std::vector<int> miscclosetrk_idx; //FIXME
    std::vector<int> closeseedtrk_idx;
    std::vector<int> jet0trk_idx;
    // std::vector<int> jet1trk_idx;
    int mu1trk_idx;
    int ele1trk_idx;
    std::vector<int> movedseedinvtxtrk_idx;
    std::vector<int> movedseedoutvtxtrk_idx;
    // double  wjet_dphi = 99, zjet_dphi = 99;

    // TLorentzVector minijet_p4_0;
    // TLorentzVector minijet_p4_1;

    TLorentzVector quark_p4_0;
    TLorentzVector genele_p4_1;
    TLorentzVector genmu_p4_1;
    // std::vector<int> minijettrk_idx;

    const TVector3 lspdecay0(gen.decay(0, bs).x() - pvs.x(0), gen.decay(0, bs).y() - pvs.y(0), gen.decay(0, bs).z() - pvs.z(0));  // JMTBAD BS BS
    const TVector3 lspdecay1(gen.decay(1, bs).x() - pvs.x(0), gen.decay(1, bs).y() - pvs.y(0), gen.decay(1, bs).z() - pvs.z(0));  // JMTBAD BS BS

    const double dvv_2vtx = sqrt((lspdecay0.x() - lspdecay1.x()) * (lspdecay0.x() - lspdecay1.x()) + (lspdecay0.y() - lspdecay1.y()) * (lspdecay0.y() - lspdecay1.y()) + (lspdecay0.z() - lspdecay1.z()) * (lspdecay0.z() - lspdecay1.z()));
    double movedist3d0 = lspdecay0.Mag();
    double movedist2d0 = lspdecay0.Perp();
    double movedist3d1 = lspdecay1.Mag();
    double movedist2d1 = lspdecay1.Perp();
    
    int count_llp = 0;

    // Loop over each LSP
    for (int ilsp = 0; ilsp < 2; ++ilsp) {
      const TVector3 lspdecay(gen.decay(ilsp,bs).x() -pvs.x(0), gen.decay(ilsp,bs).y() -pvs.y(0), gen.decay(ilsp,bs).z()-pvs.z(0));  // JMTBAD BS BS
      const double movedist2 = lspdecay.Perp();
      const double movedist3 = lspdecay.Mag();
      const TLorentzVector lsp_p4 = gen.p4(ilsp);

      const double dvv = sqrt( (lspdecay0.x() - lspdecay1.x())*(lspdecay0.x() - lspdecay1.x()) + (lspdecay0.y() - lspdecay1.y())*(lspdecay0.y() - lspdecay1.y()) + (lspdecay0.z() - lspdecay1.z())*(lspdecay0.z() - lspdecay1.z()));
      const double dvv2d = sqrt( (lspdecay0.x() - lspdecay1.x())*(lspdecay0.x() - lspdecay1.x()) + (lspdecay0.y() - lspdecay1.y())*(lspdecay0.y() - lspdecay1.y()));
      const double dr = lspdecay0.DeltaR(lspdecay1); 
      const double lspdphi = fabs(lspdecay0.DeltaPhi(lspdecay1));
      const double lspdeta = fabs(lspdecay0.Eta() - lspdecay1.Eta());
      const double lspdr = lspdecay0.DeltaR(lspdecay1);
      const double lspasymdecay = fabs(lspdecay1.Mag() - lspdecay0.Mag())/lspdecay0.Mag();
      const double lspcostheta = ((gen.p4(0).X()*gen.p4(1).X()) + (gen.p4(0).Y()*gen.p4(1).Y()) + (gen.p4(0).Z()*gen.p4(1).Z()))/(gen.p4(0).P()*gen.p4(1).P());
      const double lspdist3symmath = 2*sin(lspdr/2)*movedist3;

      if ( dvv < 0.1 ) //FIXME
        continue; 

      // Second part of preselection: only look at move vectors
      // ~inside the beampipe // JMTBAD the 2.0 cm requirement isn't
      // exact
      //if (movedist2 < 0.01 || movedist2 > 2.0) // old cuts
      if (movedist2 > 2.4) //FIXME
        continue;

      // for (int j = 0, je = jets.n(); j < je; ++j) {
      //   // std::cout << jets.pt(j)<<std::endl;
      //   // std::cout << int(jets.ntracks(j))<<std::endl;
      // }
      bool lep_isele = false;
      bool lep_ismu = false;
      // if (dijet) {
      if (semilep) { 
        //assert(abs(gen.id(ilsp)) == 1000006); // stop pair production


        // don't need this -- pretty sure for semilep case
        // for (int i = 0, ie = muons.n(); i < ie; ++i) {
        //   if (muons.pt(i) > 20.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
        //     double tmp_muon_absdxybs = abs(muons.dxybs(i, bs));
        //     double tmp_muon_absdz = muons.dzpv(i, pvs); 
        //     bool muon_IP_cut = tmp_muon_absdxybs < 0.02 && tmp_muon_absdz < 0.5;
        //     if (muon_IP_cut && muons.pt(i) > 29.0 && abs(muons.eta(i)) < 2.4 && muons.isMed(i) && muons.iso(i) < 0.15) {
        //       nselmuons += 1;
        //       if (nselmuons == 1) {
        //         muon_pT = muons.pt(i);
        //         muon_px = muons.px(i);
        //         muon_py = muons.py(i);
        //         muon_pz = muons.pz(i);
        //         muon_p4.SetPxPyPzE(muon_px, muon_py, muon_pz, muon_pT);
        //         muon_q = muons.q(i);
        //         muon_abseta = abs(muons.eta(i));
        //         muon_iso = muons.iso(i);
        //         muon_absdxybs = abs(muons.dxybs(i, bs));
        //         muon_absdz = muons.dzpv(i, pvs); 
        //         muon_nsigmadxybs = muons.nsigmadxybs(i, bs);
        //         tmpz_p4 += muon_p4;

        //       }
        //       if (has_Zmumuboson == false && nselmuons > 0 && muon_q * muons.q(i) == -1) {
        //         TLorentzVector antimuon_p4;
        //         antimuon_p4.SetPxPyPzE(muons.px(i), muons.py(i), muons.pz(i), muons.p(i));
        //         tmpz_p4 += antimuon_p4;
        //         has_Zmumuboson = true;
        //       }

        //     }

        //   }
        // }

        // if (has_Zmumuboson) {
        //   zmumu_m = tmpz_p4.M();
        //   zmumu_pT = tmpz_p4.Pt();
        //   zmumu_p4 = tmpz_p4;
        // }
        // tmpz_p4.SetPxPyPzE(0.0, 0.0, 0.0, 0.0);

        // for (int i = 0, ie = electrons.n(); i < ie; ++i) {
        //   double tmp_ele_abseta = abs(electrons.eta(i));
        //   double tmp_ele_absdxybs = abs(electrons.dxybs(i, bs));
        //   double tmp_ele_absdz = electrons.dzpv(i, pvs); 
        //   bool ele_IP_cut = tmp_ele_abseta < 1.48 ? tmp_ele_absdxybs < 0.05 && tmp_ele_absdz < 0.1 : tmp_ele_absdxybs < 0.1 && tmp_ele_absdz < 0.2;
        //   if (ele_IP_cut && electrons.pt(i) > 20.0 && abs(electrons.eta(i)) < 2.4 && electrons.isTight(i) && electrons.passveto(i) && electrons.iso(i) < 0.1) {
        //     nseleles += 1;
        //     if (nseleles == 1) {
        //       ele_pT = electrons.pt(i);
        //       ele_px = electrons.px(i);
        //       ele_py = electrons.py(i);
        //       ele_pz = electrons.pz(i);
        //       ele_p4.SetPxPyPzE(ele_px, ele_py, ele_pz, ele_pT);
        //       ele_abseta = abs(electrons.eta(i));
        //       ele_q = electrons.q(i);
        //       ele_iso = electrons.iso(i);
        //       ele_absdxybs = abs(electrons.dxybs(i, bs));
        //       ele_absdz = electrons.dzpv(i, pvs); 
        //       ele_nsigmadxybs = electrons.nsigmadxybs(i, bs);
        //       tmpz_p4 += ele_p4;

        //     }

        //     if (has_Zeeboson == false && nseleles > 0 && ele_q * electrons.q(i) == -1) {
        //       TLorentzVector antiele_p4;
        //       antiele_p4.SetPxPyPzE(electrons.px(i), electrons.py(i), electrons.pz(i), electrons.p(i));
        //       tmpz_p4 += antiele_p4;
        //       has_Zeeboson = true;
        //     }
        //   }
        // }

        // TLorentzVector met_p4;
        // met_p4.SetPtEtaPhiM(met_pT, 0, pf.met_phi(), 0);
        // TLorentzVector w_p4;

        // if (met_p4.Pt() > 25) {
        //   if (nselmuons > 0) {
        //     has_Wboson = true;
        //     w_p4 = met_p4 + muon_p4;
        //     w_pT = w_p4.Pt();
        //     lnu_absphi = abs(muon_p4.DeltaPhi(met_p4));
        //     w_mT = w_p4.Mt();
        //   }
        //   else if (nseleles > 0 && nselmuons == 0) {
        //     has_Wboson = true;
        //     w_p4 = met_p4 + ele_p4;
        //     w_pT = w_p4.Pt();
        //     lnu_absphi = abs(ele_p4.DeltaPhi(met_p4));
        //     w_mT = w_p4.Mt();
        //   }
        // }
        // if (has_Zeeboson) {
        //   zee_m = tmpz_p4.M();
        //   zee_pT = tmpz_p4.Pt();
        //   zee_p4 = tmpz_p4;
        // }
        ////////////////

        //gen idx list : ilsp = 0, ilsp = 1, 2 and 4 == quarks. 3, 5 == leptons
        // Match decay daughters to the closest (by dR) reconstructed jets
        // std::vector<int> closest_jets(2,-1), quark_assoc(2,-1);
        // int s = 2+ilsp*2, swapem = gen.pt(s) < gen.pt(s+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        // for (int i = 0; i < 2; ++i) {
        //   const int iq = s + (swapem ? !i : i);
        //   //assert(gen.id(iq) == -1000006 / gen.id(ilsp)); // stop -> dbar dbar + c.c.

        //   jmt::MinValue m(0.4);
        //   for (int j = 0, je = jets.n(); j < je; ++j)
        //     m(j, gen.p4(iq).DeltaR(jets.p4(j)));

        //   closest_jets[i] = m.i();
        //   quark_assoc[i] = iq;
        // }

        //do it for jet/lep : 
        //idx 0,2 == jets; idx 1, 3 == lep (so 0,1 for vtx0, 2,3 for vtx1)
        int closest_jet = -1;
        int closest_ele = -1;
        int closest_mu = -1;

        jmt::MinValue m(0.4);
        for (int j = 0, je = jets.n(); j < je; ++j)
          m(j, gen.p4(2+ilsp*2).DeltaR(jets.p4(j)));

        closest_jet = m.i();

        jmt::MinValue em(0.1);
        for (int e = 0, ee = electrons.n(); e < ee; ++e)
          em(e, gen.p4(3+ilsp*2).DeltaR(electrons.p4(e)));
        closest_ele = em.i();

        jmt::MinValue mm(0.1);
        for (int im=0, me = muons.n(); im < me; ++im)
          mm(im, gen.p4(3+ilsp*2).DeltaR(muons.p4(im)));
        closest_mu = mm.i();

        //then between the two leptons : 
        if (em.v() < mm.v()) lep_isele = true;
        if (mm.v() < em.v()) lep_ismu = true;


        // Last hidden part of the preselection: skip events where
        // daughter doesn't match to a jet or both match to the same
        // jet // JMTBAD how many are we skipping?
        TLorentzVector jet_p4_0;
        TLorentzVector mu_p4_1;
        TLorentzVector ele_p4_1;

        TLorentzVector mu1_reco_p4;
        TLorentzVector ele1_reco_p4;

        quark_p4_0 = gen.p4(2+ilsp*2);

        // get info from the reco lepton (used for hists... pT, and p)
        if (lep_isele) {
          genele_p4_1 = gen.p4(3+ilsp*2);
          // ele_p4_1 = electrons.p4(closest_ele);
          // ele1_reco_p = electrons.p(closest_ele);
          // ele1_reco_pt = electrons.p4(closest_ele).Pt();
        }
        if (lep_ismu) {
          genmu_p4_1 = gen.p4(3+ilsp*2);
          // mu_p4_1 = muons.p4(closest_mu);
          // mu1_reco_p = muons.p(closest_mu);
          // mu1_reco_pt = muons.p4(closest_mu).Pt();
        }

        if (lep_isele) genele_p4_1 = gen.p4(3+ilsp*2);
        if (lep_ismu) genmu_p4_1 = gen.p4(3+ilsp*2);


        // //if (closest_jets[0] == -1 || closest_jets[1] == -1 || closest_jets[0] == closest_jets[1])
        // //   continue;

        // if (nselmuons < 1)
        //   continue;

        //make certain that there is a jet that matches with the genquark 
        if (closest_jet == -1)
          continue;
        
        //make certain that there is a lepton that matches with the genlepton 
        if (!lep_ismu && !lep_isele)
          continue;

        const std::vector<int> jet0_tracks = tks.tks_for_jet(closest_jet);
        // const std::vector<int> jet1_tracks = tks.tks_for_jet(closest_jets[1]);
        // int minijet_ntk_0 = 0;
        // int minijet_ntk_1 = 0;
        int jet_ntk_0 = 0;
        n_movedseedtks = 0;
        n_movedseedtks0 = 0;
        n_movedseedtks1 = 0;
        sump_0 = 0;
        p_mu1 = 0;
        p_ele1 = 0;

        miscp = 0;
        maxeta_0 = 0;
        // maxeta_1 = 0;
        // mu_eta_1 = 100;
        // ele_eta_1 = 100;
        //qrk0_mingendxy = 100;
        //qrk1_mingendxy = 100;
        //qrk0_phi = -9.9;
        //qrk1_phi = -9.9;
        //qrk0_matchthres = -9.9;
        //qrk1_matchthres = -9.9;
        // minijet_p4_0.SetPxPyPzE(0, 0, 0, 0);
        // minijet_p4_1.SetPxPyPzE(0, 0, 0, 0);
        jet_p4_0.SetPxPyPzE(0,0,0,0);
        mu_p4_1.SetPxPyPzE(0,0,0,0);
        ele_p4_1.SetPxPyPzE(0,0,0,0);
        jet0trk_idx = {};
        mu1trk_idx = -1;
        ele1trk_idx = -1;
        //for reco leptons 
        mu1_reco_p4.SetPxPyPzE(0,0,0,0);
        ele1_reco_p4.SetPxPyPzE(0,0,0,0); 
        ele1_reco_p = 0;
        mu1_reco_p = 0;
        ele1_reco_pt = 0;
        mu1_reco_pt = 0;
        // jet1trk_idx = {};

        movedseedinvtxtrk_idx = {};
        movedseedoutvtxtrk_idx = {};
        sumpreco_0 = 0;
        // sumpreco_mu1 = 0;
        // sumpreco_ele1 = 0;

        for (int j = 0; j < tks.n(); ++j) {
          const TLorentzVector jp4 = tks.p4(j);
          auto jit0 = std::find(jet0_tracks.begin(), jet0_tracks.end(), j);
          if ( tks.pass_sel(j) && jit0 != jet0_tracks.end()){ 
            sumpreco_0 += tks.p(j);
          }

          // if (tks.pass_sel(j) && nt.mtk_moved(j)){
          //   double tkmudr = tks.p4(j).DeltaR(genmu_p4_1); //check and make sure that this mtk is the one corresponding to the genmu 
          //   if (tkmudr < 0.1) sumpreco_mu1 = tks.p(j);
          // }
          // if (tks.pass_sel(j) && nt.etk_moved(j)){
          //   double tkedr = tks.p4(j).DeltaR(genele_p4_1);
          //   if (tkedr < 0.1) sumpreco_ele1 = tks.p(j);
          // }

        }  
        for (int j = 0; j < tks.n(); ++j) {
          const TLorentzVector jp4 = tks.p4(j);
          if ( tks.pass_sel(j) && jp4.DeltaR(quark_p4_0) < 0.4 ){ //FIXME 
            // auto mt = std::find(minijettrk_idx.begin(), minijettrk_idx.end(), j);
            // if (mt != minijettrk_idx.end()) continue;
            double jet0_gennsigmadz = tks.dz(j, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(j);
            double jet0_gennsigmamissdist = tks.dxy(j, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(j);  
            double jet0_gennsigma = sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)); 
            if (jet0_gennsigma > 10) continue; 
            jet_p4_0 += tks.p4(j);
            // minijet_p4_0 += tks.p4(j);
            // minijet_ntk_0 += 1;
            jet_ntk_0 += 1;
            jet0trk_idx.push_back(j);
            // minijettrk_idx.push_back(j);
            sump_0 += tks.p(j);
            if (fabs(tks.eta(j)) > fabs(maxeta_0)) maxeta_0 = tks.eta(j);
            if (tks.pass_seed(j, bs)) {
              n_movedseedtks++;
              n_movedseedtks0++;
            }
          }
          if (lep_ismu){ 
            if (tks.pass_sel(j) && nt.mtk_moved(j) && jp4.DeltaR(genmu_p4_1) < 0.1){
              double mu1_gennsigmadz = tks.dz(j, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(j);
              double mu1_gennsigmamissdist = tks.dxy(j, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(j);  
              double mu1_gennsigma = sqrt((mu1_gennsigmamissdist*mu1_gennsigmamissdist) + (mu1_gennsigmadz*mu1_gennsigmadz)); 
              if (mu1_gennsigma > 10) continue; 
              mu_p4_1 = tks.p4(j);
              mu1trk_idx = j;
              p_mu1 = tks.p(j);
              mu_eta_1 = tks.eta(j);
              if (tks.pass_seed(j, bs)) {
                n_movedseedtks++;
                n_movedseedtks1++;
              }
              //for reco mu : 
              mu1_reco_p4 = muons.p4(closest_mu);
              mu1_reco_p = mu1_reco_p4.P();
              mu1_reco_pt = muons.pt(closest_mu);
            }
          }
          if (lep_isele){ 
            if (tks.pass_sel(j) && nt.etk_moved(j) && jp4.DeltaR(genele_p4_1) < 0.1){
              double ele1_gennsigmadz = tks.dz(j, gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(j);
              double ele1_gennsigmamissdist = tks.dxy(j, gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(j);  
              double ele1_gennsigma = sqrt((ele1_gennsigmamissdist*ele1_gennsigmamissdist) + (ele1_gennsigmadz*ele1_gennsigmadz)); 
              if (ele1_gennsigma > 10) continue; 
              ele_p4_1 = tks.p4(j);
              ele1trk_idx = j;
              p_ele1 = tks.p(j);
              ele_eta_1 = tks.eta(j);
              if (tks.pass_seed(j, bs)) {
                n_movedseedtks++;
                n_movedseedtks1++;
              }
              //reco ele 
              ele1_reco_p4 = electrons.p4(closest_ele);
              ele1_reco_p = ele1_reco_p4.P();
              ele1_reco_pt = electrons.pt(closest_ele);
            }
          } 
        }
        jet_eta_0 = jet_p4_0.Eta();
        // jet_p4_0 = minijet_p4_0;
        // jet_p4_1 = minijet_p4_1;
        // jet_eta_0 = minijet_p4_0.Eta();
        // jet_eta_1 = minijet_p4_1.Eta();
        jet_ntks_0 = jet_ntk_0;
        // jet_ntks_1 = minijet_ntk_1;

        miscclosetrk_idx = {}; //FIXME
        closeseedtrk_idx = {};
        n_closeseedtks = 0;
        n_sharedcloseseedtks = 0;
        n_movedcloseseedtks = 0;
        n_tightcloseseedtks = 0;
        n_movedvtxseedtks = 0;
        n_miscseedtracks = 0;
        n_misccloseseedtracks = 0;
        // Start calculating significances of closest approach and count # of close seed tracks
        for (int it=0, ite = tks.n(); it < ite; it++) {
          if (tks.pass_seed(it, bs)) {

            n_miscseedtracks++; // Count up all seed tracks. Will subtract out the matching tracks later. 
            std::vector<double> sigs_quad;

            for (int il = 0; il < 2; il++) {
              const double temp_sigdxy = tks.dxy(it, gen.decay_x(il), gen.decay_y(il))/tks.err_dxy(it);
              const double temp_sigdz  = tks.dz(it, gen.decay_x(il), gen.decay_y(il), gen.decay_z(il))/tks.err_dz(it);
              const double sum_sq_sig = hypot(temp_sigdxy, temp_sigdz);
              sigs_quad.push_back(sum_sq_sig);
            }      

            //HERE 
            // Count how many 'close' seed tracks there are
            if ( sigs_quad[0] < close_criteria && sigs_quad[1] < close_criteria )
              n_sharedcloseseedtks++;

            // auto miniit = std::find(minijettrk_idx.begin(), minijettrk_idx.end(), it);
            auto jetit = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), it);
            if ( sigs_quad[ilsp] < close_criteria){
              n_closeseedtks++;
              closeseedtrk_idx.push_back(it);
              // if (miniit != minijettrk_idx.end()){
              //for the jet
              if (jetit != jet0trk_idx.end()) {
                n_movedcloseseedtks++;
              }
              //for the lep
              else if (mu1trk_idx == it || ele1trk_idx == it)
                n_movedcloseseedtks++;

              else{
                n_misccloseseedtracks++;
                const TLorentzVector jp4 = tks.p4(it);
                miscclosetrk_idx.push_back(it);
                miscp += tks.p(it);
              }
            }

            if ( sigs_quad[ilsp] < tight_close_criteria){
              n_tightcloseseedtks++;
            }

            // if (miniit != minijettrk_idx.end())
            if (jetit != jet0trk_idx.end())
              n_miscseedtracks--;

          }
        }

        // int j = ilsp;   
        // int slsp = 2+j*2, swapemm = gen.pt(slsp) < gen.pt(slsp+1); // toward making the jet assoc'd to the higher (lower) pT quark be "jet0" ("jet1")
        // int iqlsp0 = slsp + (swapemm ? !0 : 0);
        // int iqlsp1 = slsp + (swapemm ? !1 : 1);
        // boost0 =  gen.p4(iqlsp0).Beta()*gen.p4(iqlsp0).Gamma(); 
        // boost1 = gen.p4(iqlsp1).Beta()*gen.p4(iqlsp1).Gamma(); 

        boost0 = gen.p4(2+ilsp*2).Beta()*gen.p4(2+ilsp*2).Gamma();
        boost1 = gen.p4(3+ilsp*2).Beta()*gen.p4(3+ilsp*2).Gamma();

        // const TLorentzVector jet_tot_p4 = jet_p4_0 + jet_p4_1;
        jet0_lsp_angle = jet_p4_0.Angle(lsp_p4.Vect());	 //smearing angle
        // jet1_lsp_angle = jet_p4_1.Angle(lsp_p4.Vect());  //smearing angle
        jet_pt_0  = jet_p4_0.Pt();
        // jet_pt_1  = jet_p4_1.Pt();
        jet_dr_minjq0 = jet_p4_0.DeltaR(quark_p4_0);
        // jet_dr_minjq1 = jet_p4_1.DeltaR(quark_p4_1);
        // jet_dr        = quark_p4_0.DeltaR(quark_p4_1);
        // jet_costheta = ((jet_p4_0.X()*jet_p4_1.X()) + (jet_p4_0.Y()*jet_p4_1.Y()) + (jet_p4_0.Z()*jet_p4_1.Z()))/(jet_p4_0.P()*jet_p4_1.P()); 
        // jet_dphi =  quark_p4_0.DeltaPhi(quark_p4_1); //jet_p4_0.DeltaPhi(jet_p4_1);
        // jet_aj    = (jet_pt_0 - jet_pt_1) / (jet_pt_0 + jet_pt_1);
        // jet_deta = fabs(quark_p4_0.Eta() - quark_p4_1.Eta()); //fabs(jet_eta_0 - jet_eta_1);
        // jet_dphi_max = jet_p4_0.DeltaPhi(jet_p4_1);
        // jet_deta_max = jet_eta_0 - jet_eta_1; // JMTBAD fabs?
        // qrk_dphi_max = quark_p4_0.DeltaPhi(quark_p4_1);
        jet_mv_dphi_0  = lsp_p4.DeltaPhi(jet_p4_0);
        // jet_mv_dphi_1  = lsp_p4.DeltaPhi(jet_p4_1);
        // jet_mv_dphi_sum = lsp_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        qrk_mv_dphi_0  = lsp_p4.DeltaPhi(quark_p4_0);
        // qrk_mv_dphi_1  = lsp_p4.DeltaPhi(quark_p4_1);
        // qrk_mv_dphi_sum = lsp_p4.DeltaPhi(quark_p4_0 + quark_p4_1);
        qrkp_0 = quark_p4_0.P();
        // qrkp_1 = quark_p4_1.P();
        // qrk_costheta = ((quark_p4_0.X()*quark_p4_1.X()) + (quark_p4_0.Y()*quark_p4_1.Y()) + (quark_p4_0.Z()*quark_p4_1.Z()))/(quark_p4_0.P()*quark_p4_1.P()); 
        jet_mv_deta_0  = fabs(jet_eta_0 - lsp_p4.Eta());
        // jet_mv_deta_1  = fabs(jet_eta_1 - lsp_p4.Eta());
        // jet_mv_deta_sum = fabs((jet_p4_0 + jet_p4_1).Eta() - lsp_p4.Eta());

        TVector3 lspdecaybsp(gen.decay(ilsp,bs).x(), gen.decay(ilsp,bs).y() , gen.decay(ilsp,bs).z());  // JMTBAD BS BS
        double decay_radius = lspdecaybsp.Perp();
        qrk0_dxybs = decay_radius*sin(qrk_mv_dphi_0);
        // qrk1_dxybs = decay_radius*sin(qrk_mv_dphi_1);
        jet0_dxybs = decay_radius*sin(jet_mv_dphi_0);
        // jet1_dxybs = decay_radius*sin(jet_mv_dphi_1);

        // const TLorentzVector jetele_p4;
        // const TLorentzVector jetmu_p4;
        double genlep_eta = 10.0; //to be used later
        double jetlep_dr = -1.0; //to be used later
        if (lep_isele) { 
          const TLorentzVector jetele_p4 = jet_p4_0 + ele_p4_1;
          ele1_lsp_angle = ele_p4_1.Angle(lsp_p4.Vect());
          ele_pt_1 = ele_p4_1.Pt();
          ele_dr_minl1 = ele_p4_1.DeltaR(genele_p4_1);;
          jetele_dr = quark_p4_0.DeltaR(genele_p4_1);
          jetele_costheta = ((jet_p4_0.X()*ele_p4_1.X()) + (jet_p4_0.Y()*ele_p4_1.Y()) + (jet_p4_0.Z()*ele_p4_1.Z()))/(jet_p4_0.P()*ele_p4_1.P()); 
          jetele_dphi =  quark_p4_0.DeltaPhi(genele_p4_1); //jet_p4_0.DeltaPhi(jet_p4_1);
          jetele_aj    = (jet_pt_0 - ele_pt_1) / (jet_pt_0 + ele_pt_1);

          jetele_deta = fabs(quark_p4_0.Eta() - genele_p4_1.Eta()); //fabs(jet_eta_0 - jet_eta_1);
          jetele_dphi_max = jet_p4_0.DeltaPhi(ele_p4_1);
          jetele_deta_max = jet_eta_0 - ele_eta_1; // JMTBAD fabs?
          qrkgenele_dphi_max = quark_p4_0.DeltaPhi(genele_p4_1);
          ele_mv_dphi_1 = lsp_p4.DeltaPhi(ele_p4_1);
          jetele_mv_dphi_sum = lsp_p4.DeltaPhi(jet_p4_0 + ele_p4_1);
          genele_mv_dphi_1  = lsp_p4.DeltaPhi(genele_p4_1);
          qrkgenele_mv_dphi_sum = lsp_p4.DeltaPhi(quark_p4_0 + genele_p4_1);
          genelep_1 = genele_p4_1.P();
          qrkgenele_costheta = ((quark_p4_0.X()*genele_p4_1.X()) + (quark_p4_0.Y()*genele_p4_1.Y()) + (quark_p4_0.Z()*genele_p4_1.Z()))/(quark_p4_0.P()*genele_p4_1.P()); 
          ele_mv_deta_1  = fabs(ele_eta_1 - lsp_p4.Eta());
          jetele_mv_deta_sum = fabs((jet_p4_0 + ele_p4_1).Eta() - lsp_p4.Eta());
          genele1_dxybs = decay_radius*sin(genele_mv_dphi_1);
          ele1_dxybs = decay_radius*sin(ele_mv_dphi_1);
          genlep_eta = genele_p4_1.Eta();
          jetlep_dr = jetele_dr;

        }
        if (lep_ismu) {
          const TLorentzVector jetmu_p4 = jet_p4_0 + mu_p4_1;
          mu1_lsp_angle = mu_p4_1.Angle(lsp_p4.Vect());
          mu_pt_1 = mu_p4_1.Pt();
          mu_dr_minl1 = mu_p4_1.DeltaR(genmu_p4_1);
          jetmu_dr = quark_p4_0.DeltaR(genmu_p4_1);
          jetmu_costheta = ((jet_p4_0.X()*mu_p4_1.X()) + (jet_p4_0.Y()*mu_p4_1.Y()) + (jet_p4_0.Z()*mu_p4_1.Z()))/(jet_p4_0.P()*mu_p4_1.P()); 
          jetmu_dphi =  quark_p4_0.DeltaPhi(genmu_p4_1); //jet_p4_0.DeltaPhi(jet_p4_1);
          jetmu_aj    = (jet_pt_0 - mu_pt_1) / (jet_pt_0 + mu_pt_1); 
          jetmu_deta = fabs(quark_p4_0.Eta() - genmu_p4_1.Eta()); //fabs(jet_eta_0 - jet_eta_1);
          jetmu_dphi_max = jet_p4_0.DeltaPhi(mu_p4_1);
          jetmu_deta_max = jet_eta_0 - mu_eta_1; // JMTBAD fabs?
          qrkgenmu_dphi_max = quark_p4_0.DeltaPhi(genmu_p4_1);
          mu_mv_dphi_1 = lsp_p4.DeltaPhi(mu_p4_1);
          jetmu_mv_dphi_sum = lsp_p4.DeltaPhi(jet_p4_0 + mu_p4_1);
          genmu_mv_dphi_1  = lsp_p4.DeltaPhi(genmu_p4_1);
          qrkgenmu_mv_dphi_sum = lsp_p4.DeltaPhi(quark_p4_0 + genmu_p4_1);
          genmup_1 = genmu_p4_1.P();
          qrkgenmu_costheta = ((quark_p4_0.X()*genmu_p4_1.X()) + (quark_p4_0.Y()*genmu_p4_1.Y()) + (quark_p4_0.Z()*genmu_p4_1.Z()))/(quark_p4_0.P()*genmu_p4_1.P()); 
          mu_mv_deta_1  = fabs(mu_eta_1 - lsp_p4.Eta());
          jetmu_mv_deta_sum = fabs((jet_p4_0 + mu_p4_1).Eta() - lsp_p4.Eta());
          genmu1_dxybs = decay_radius*sin(genmu_mv_dphi_1);
          mu1_dxybs = decay_radius*sin(mu_mv_dphi_1);
          genlep_eta = genmu_p4_1.Eta();
          jetlep_dr = jetmu_dr;
        }

        // if (has_Wboson) wjet_dphi = w_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        // if (has_Zmumuboson) {
        //   zjet_dphi = zmumu_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        //   z_m = zmumu_m;
        //   z_pT = zmumu_pT;
        // }
        // else if (has_Zeeboson) {
        //   zjet_dphi = zee_p4.DeltaPhi(jet_p4_0 + jet_p4_1);
        //   z_m = zee_m;
        //   z_pT = zee_pT;
        // }
        // if (met_p4.Pt() > 25) {
        //   if (nselmuons > 0) {
        //     ljet_absdr = abs(muon_p4.DeltaR(jet_p4_0)) < abs(muon_p4.DeltaR(jet_p4_1)) ? abs(muon_p4.DeltaR(jet_p4_0)) : abs(muon_p4.DeltaR(jet_p4_1));
        //     ljet0_absdr = abs(muon_p4.DeltaR(jet_p4_0));
        //     ljet1_absdr = abs(muon_p4.DeltaR(jet_p4_1));
        //   }
        //   else if (nseleles > 0 && nselmuons == 0) {
        //     ljet_absdr = abs(ele_p4.DeltaR(jet_p4_0)) < abs(ele_p4.DeltaR(jet_p4_1)) ? abs(ele_p4.DeltaR(jet_p4_0)) : abs(ele_p4.DeltaR(jet_p4_1));		
        //     ljet0_absdr = abs(ele_p4.DeltaR(jet_p4_0));
        //     ljet1_absdr = abs(ele_p4.DeltaR(jet_p4_1));
        //   }
        //   nujet0_absphi = abs(met_p4.DeltaPhi(jet_p4_0));
        //   nujet1_absphi = abs(met_p4.DeltaPhi(jet_p4_1));

        // }

        //FIXME
        // check that there is a reco lepton 
        if (mu1_reco_p == 0 && ele1_reco_p == 0)
          continue;

        //want a jet
        if (sump_0 == 0) 
          continue;
        
        // if (fabs(quark_p4_0.Eta()) > 2.5 || fabs(quark_p4_1.Eta()) > 2.5)
        if (fabs(quark_p4_0.Eta()) > 2.5 || fabs(genlep_eta) > 2.5)
          continue;

        // if ( fabs(jet_dr) < 0.4 )
        if (fabs(jetlep_dr) < 0.4)
          continue;


        //High-Eta
        // if (fabs(quark_p4_0.Eta()) > 1.5 || fabs(quark_p4_1.Eta()) > 1.5)
        if (fabs(quark_p4_0.Eta()) < 1.5 || fabs(genlep_eta) < 1.5)
          continue;


        //std::cout << " run: " << nr.nt().base().run() << std::endl << " lumi: " << nr.nt().base().lumi() << " event: " << nr.nt().base().event() << std::endl;
        //std::cout << " jet0: " << closest_jets[0] << " jet1: " << closest_jets[1] << std::endl;

        //std::cout << " quark0" << " eta " << quark_p4_0.Eta() << " p " << quark_p4_0.P() << " ntk0 " << jet_ntks_0 << std::endl;
        //std::cout << " quark1" << " eta " << quark_p4_1.Eta() << " p " << quark_p4_1.P() << " ntk1 " << jet_ntks_1 << std::endl;

      }


      int n_pass_nocuts = 0;
      int n_pass_ntracks = 0;
      int n_pass_all = 0;
      double  dist2move = -9.9;
      jmt::MinValue dist2min(100);
      std::vector<int> first_vtx_to_pass(num_numdens, -1);
      double vtx_cat = 0.0, vtx_bs2derr = -9.9, vtx_eta = -9.9, vtx_z = -999.9, vtx_dbv = -999.9, vtx_3dbv = -999.9, vtx_ntk = -9, vtx_chi2 = -9.9; // JMTBAD ??? these end up with what???
      auto set_it_if_first = [](int& to_set, int to_set_to) { if (to_set == -1) to_set = to_set_to; };
      for (size_t i = 0; i < nvtx; ++i) {
        dist2move = (gen.decay(ilsp, bs) - vs.pos(i)).Mag();
        dist2min(i, dist2move);
        if (dist2move > 0.0400) //FIXME
          continue;

        vtx_bs2derr = vs.bs2derr(i); // JMTBAD ???
        vtx_eta     = vs.eta(i);
        vtx_z       = vs.z(i);
        vtx_dbv     = vs.pos(i).Perp();
        vtx_3dbv    = vs.pos(i).Mag();
        vtx_ntk     = vs.ntracks(i);
        vtx_chi2    = vs.chi2(i)/vs.ndof(i);
        const bool pass_beams = vtx_dbv >= 0.0100 && vtx_dbv < 2.0;
        const bool pass_ntracks = vs.ntracks(i) >= 4 && pass_beams;
        const bool pass_bs2derr = vs.bs2derr(i) < 0.0050 && pass_beams; // JMTBAD rescale_bs2derr // FIXME

        if (1) { set_it_if_first(first_vtx_to_pass[0], i); ++n_pass_nocuts; }
        if (pass_ntracks) { set_it_if_first(first_vtx_to_pass[1], i); ++n_pass_ntracks; }
        if (pass_ntracks && pass_bs2derr) { set_it_if_first(first_vtx_to_pass[2], i); ++n_pass_all; }

      }
      dist2move = dist2min.v();
      double mindist2move_iv = dist2min.i();
      if (mindist2move_iv != -1){
        vtx_bs2derr = vs.bs2derr(mindist2move_iv); // JMTBAD ???
        vtx_eta     = vs.eta(mindist2move_iv);
        vtx_z       = vs.z(mindist2move_iv);
        vtx_dbv     = vs.pos(mindist2move_iv).Perp();
        vtx_3dbv    = vs.pos(mindist2move_iv).Mag();
        vtx_ntk     = vs.ntracks(mindist2move_iv);
        vtx_chi2    = vs.chi2(mindist2move_iv)/vs.ndof(mindist2move_iv);

        if (vtx_dbv > 0.0100 && dist2move < 0.0200) vtx_cat = 1.0;
        if (vtx_dbv < 0.0100 && dist2move > 0.0200) vtx_cat = 2.0;
        if (vtx_dbv < 0.0100 && dist2move > 0.0200) vtx_cat = 3.0;
        const std::vector<int> its = tks.tks_for_sv(mindist2move_iv);
        for (int it : its){
          auto it0 = std::find(jet0trk_idx.begin(), jet0trk_idx.end(), it);
          // auto it1 = std::find(jet1trk_idx.begin(), jet1trk_idx.end(), it);
          // if (it0 != jet0trk_idx.end() || it1 != jet1trk_idx.end()){
          if (it0 != jet0trk_idx.end() || it == mu1trk_idx || it == ele1trk_idx) { 
            n_movedvtxseedtks++;
            movedseedinvtxtrk_idx.push_back(it);
          } 
        }

        for (int ttk = 0; ttk < tks.n(); ++ttk){
          const double vtxdz = tks.dz(ttk, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
          const double vtxdxy = tks.dxy(ttk, vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
          if (sqrt((vtxdxy/tks.err_dxy(ttk)*(vtxdxy/tks.err_dxy(ttk))) + (vtxdz/tks.err_dz(ttk)*(vtxdz/tks.err_dz(ttk)))) > 10)
            movedseedoutvtxtrk_idx.push_back(ttk);
        }
      }

      if (dist2move > 0.0400 && dist2move < 100) //FIXME
        continue;

      den += w;
      count_llp += 1;

      for (numdens& nd : nds) {
        nd.den(k_decay_x, lspdecay.x());
        nd.den(k_decay_y, lspdecay.y());
        nd.den(k_decay_z, lspdecay.z());
        nd.den(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.den(k_lspdphi, lspdphi);
        nd.den(k_lspdeta, lspdeta);
        nd.den(k_lspdr, lspdr);
        nd.den(k_lspasymdecay, lspasymdecay);
        nd.den(k_lspcostheta, lspcostheta);
        nd.den(k_lspdist2, lspdist2);
        nd.den(k_lspdist3, lspdist3);
        nd.den(k_lspdist3symmath, lspdist3symmath);
        nd.den(k_ratlspdist3, lspdist3symmath/lspdist3);
        nd.den(k_2sinhalftheta, 2*sin(lspdr/2));
        nd.den(k_lspdistz, lspdistz);
        nd.den(k_movedist2, movedist2);
        nd.den(k_movedist3, movedist3);
        nd.den(k_lspeta, lsp_p4.Eta());
        nd.den(k_lsppt, lsp_p4.Pt());
        nd.den(k_lspgammabeta, lsp_p4.Beta()*lsp_p4.Gamma());
        nd.den(k_lspctau, movedist3/(lsp_p4.Beta()*lsp_p4.Gamma()));
        nd.den(k_npv, pvs.n());
        nd.den(k_pvz, pvs.z(0));
        nd.den(k_dist2dpvbs, sqrt((pvs.x(0)-bs.x(pvs.z(0)))*(pvs.x(0)-bs.x(pvs.z(0))) + (pvs.y(0)-bs.y(pvs.z(0)))*(pvs.y(0)-bs.y(pvs.z(0)))));
        nd.den(k_pvrho, pvs.rho(0));
        nd.den(k_pvntracks, pvs.ntracks(0));
        nd.den(k_pvscore, pvs.score(0));
        nd.den(k_ht, jets.ht());
        nd.den(k_njets, jets.n());
        // nd.den(k_nmuons, nselmuons);
        // nd.den(k_muon_pT, muon_pT);
        // nd.den(k_muon_abseta, muon_abseta);
        // nd.den(k_muon_iso, muon_iso);
        // nd.den(k_muon_absdxybs, muon_absdxybs);
        // nd.den(k_muon_absdz, muon_absdz);
        // nd.den(k_muon_nsigmadxybs, muon_nsigmadxybs);
        // nd.den(k_neles, nseleles);
        // nd.den(k_ele_pT, ele_pT);
        // nd.den(k_ele_abseta, ele_abseta);
        // nd.den(k_ele_iso, ele_iso);
        // nd.den(k_ele_absdxybs, ele_absdxybs);
        // nd.den(k_met_pT, met_pT);
        // nd.den(k_w_pT, w_pT);
        // nd.den(k_w_mT, w_mT);
        // nd.den(k_z_pT, z_pT);
        // nd.den(k_z_m, z_m); 
        // nd.den(k_lnu_absphi, lnu_absphi);
        // nd.den(k_ljet_absdr, ljet_absdr);
        // nd.den(k_ljet0_absdr, ljet0_absdr);
        // nd.den(k_ljet1_absdr, ljet1_absdr);
        // nd.den(k_nujet0_absphi, nujet0_absphi);
        // nd.den(k_nujet1_absphi, nujet1_absphi);
        // nd.den(k_wjet_dphi, fabs(wjet_dphi));
        // nd.den(k_zjet_dphi, fabs(zjet_dphi));

        // std::cout << "here 1 " << std::endl;

        nd.den(k_jet0_eta, jet_eta_0);
        // nd.den(k_jet_dind, jet_dind);
        nd.den(k_pt0, jet_pt_0);
        nd.den(k_ntks_j0, jet_ntks_0);
        // nd.den(k_ntks_j1, jet_ntks_1);
        nd.den(k_jet_dr_minj0_q0, jet_dr_minjq0);
        // nd.den(k_ntk0_ntk1, jet_ntks_0, jet_ntks_1);
        nd.den(k_boost0_boost1, boost0, boost1);
        for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
          nd.den(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.den(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.den(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(closeseedtrk_idx[j]));
        }
        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet0trk_idx[j]);
          // nd.den(k_jet0_trk_dr, jp4.DeltaR(minijet_p4_0));
          // nd.den(k_jet0_trk_dr, jp4.DeltaR(jet_p4_0));

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
          nd.den(k_jet0_trk_nsigmadz, tks.dzpv(jet0trk_idx[j], pvs)/tks.err_dz(jet0trk_idx[j]));
          const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet0trk_idx[j]);
          const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet0trk_idx[j]);  
          nd.den(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
          nd.den(k_jet0_trk_dr_gennsigma, jp4.DeltaR(quark_p4_0), sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
          nd.den(k_jet0_trk_dr_genmissdist, jp4.DeltaR(quark_p4_0), tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));            nd.den(k_jet0_trk_dr_gendz, jp4.DeltaR(quark_p4_0), tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
          nd.den(k_jet0_trk_eta_gennsigma, tks.eta(jet0trk_idx[j]), sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
          nd.den(k_jet0_trk_eta_gendz, tks.eta(jet0trk_idx[j]), tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
          nd.den(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
          nd.den(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.den(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
          nd.den(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.den(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
          nd.den(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.den(k_jet0_trk_nsigmadsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0))/tks.err_dz(jet0trk_idx[j]));
          nd.den(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
          nd.den(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
          nd.den(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
          for (size_t ind = 0; ind < miscclosetrk_idx.size(); ++ind){
            nd.den(k_miscclose_trk_whichjet, tks.which_jet(miscclosetrk_idx[ind]));
            nd.den(k_miscclose_trk_dsz, tks.dsz(miscclosetrk_idx[ind], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
            nd.den(k_miscclose_trk_p, tks.p(miscclosetrk_idx[ind]));
            nd.den(k_miscclose_trk_eta, tks.eta(miscclosetrk_idx[ind]));
            nd.den(k_miscclose_trk_dzerr, tks.err_dz(miscclosetrk_idx[ind]));
          }
          auto itin = std::find(movedseedinvtxtrk_idx.begin(),  movedseedinvtxtrk_idx.end(), jet0trk_idx[j]);
          if (itin != movedseedinvtxtrk_idx.end()){
            nd.den(k_movedseedinvtx_trk_whichjet, tks.which_jet(jet0trk_idx[j]));
            nd.den(k_movedseedinvtx_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
            nd.den(k_movedseedinvtx_trk_dr, jp4.DeltaR(quark_p4_0));
            nd.den(k_movedseedinvtx_trk_p, tks.p(jet0trk_idx[j]));
            nd.den(k_movedseedinvtx_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
            nd.den(k_movedseedinvtx_trk_eta, tks.eta(jet0trk_idx[j]));
            nd.den(k_movedseedinvtx_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
            nd.den(k_movedseedinvtx_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
            nd.den(k_movedseedinvtx_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
            nd.den(k_movedseedinvtx_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
          }
          auto itout = std::find(movedseedoutvtxtrk_idx.begin(),  movedseedoutvtxtrk_idx.end(), jet0trk_idx[j]);
          if (itout != movedseedoutvtxtrk_idx.end()){
            nd.den(k_movedseedoutvtx_trk_dr, jp4.DeltaR(quark_p4_0));
            nd.den(k_movedseedoutvtx_trk_p, tks.p(jet0trk_idx[j]));
            nd.den(k_movedseedoutvtx_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
            nd.den(k_movedseedoutvtx_trk_eta, tks.eta(jet0trk_idx[j]));
            nd.den(k_movedseedoutvtx_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
            nd.den(k_movedseedoutvtx_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
            nd.den(k_movedseedoutvtx_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
            nd.den(k_movedseedoutvtx_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
          }
        }
        // std::cout << "here 2 " << std::endl;
        // std::cout << "is lep a muon or electron? " << lep_ismu << " " << lep_isele << std::endl;
        if (lep_ismu) { 
          nd.den(k_jetmu_asymm, jetmu_aj);
          nd.den(k_mu1_eta, mu_eta_1);
          nd.den(k_mu1_p_eta, mu1_reco_p, mu_eta_1);
          nd.den(k_lep1_p_eta, mu1_reco_p, mu_eta_1);
          nd.den(k_jetmu_dr, jetmu_dr);
          nd.den(k_jetmu_costheta, jetmu_costheta);
          nd.den(k_jetmu_deta, jetmu_deta);
          nd.den(k_jetmu_dphi, jetmu_dphi);
          nd.den(k_jetmu_deta_dphi, jetmu_deta, jetmu_dphi);
          nd.den(k_jetlep_deta_dphi, jetmu_deta, jetmu_dphi);
          nd.den(k_mupt1, mu1_reco_pt);
          nd.den(k_mu_dr_minl1_l1, mu_dr_minl1);
          nd.den(k_llp_sump_jetmudphi, sump_0+p_mu1+miscp, jetmu_dphi);
          nd.den(k_llp_sump_jetmudr, sump_0+p_mu1+miscp, jetmu_dr);
          nd.den(k_jet0_sump_jetmudr, sump_0, jetmu_dr);
          nd.den(k_jet0_sump_jetlepdr, sump_0, jetmu_dr);
          nd.den(k_mu1_p_jetmudr, mu1_reco_p, jetmu_dr);
          nd.den(k_lep1_p_jetlepdr, mu1_reco_p, jetmu_dr);
          nd.den(k_mu1_pT_jetmudr, mu1_reco_pt, jetmu_dr);
          nd.den(k_lep1_pT_jetlepdr, mu1_reco_pt, jetmu_dr);

          nd.den(k_movedist3_jetmudr, movedist3, jetmu_dr);
          nd.den(k_movedist3_mu1_p, movedist3, p_mu1);
          nd.den(k_angle2d_jetmudr, movedist2/movedist3, jetmu_dr);
          nd.den(k_angle2d_mu1_p, movedist2/movedist3, p_mu1);
          nd.den(k_movedist2_jetmudr, movedist2, jetmu_dr);
          nd.den(k_movedist2_mu1_p, movedist2, p_mu1);
          nd.den(k_jetmu_costheta_tightcloseseedtks, jetmu_costheta, n_tightcloseseedtks);
          nd.den(k_jetmu_dr_tightcloseseedtks, jetmu_dr, n_tightcloseseedtks);
          nd.den(k_jetmu_costheta_closeseedtks, jetmu_costheta, n_closeseedtks);
          nd.den(k_jetmu_dr_closeseedtks, jetmu_dr, n_closeseedtks);
          nd.den(k_lspdist3_genmu1_dxybs, lspdist3, genmu1_dxybs); 
          nd.den(k_mu1_p, mu1_reco_p);
          nd.den(k_2logm_jetmudr, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta), jetmu_dr);
          nd.den(k_2logm_costheta_mu, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta), jetmu_costheta);
          nd.den(k_mu1_p_jetmu_costheta, p_mu1, jetmu_costheta);
          nd.den(k_mu1_p_jetdphi, p_mu1, jetmu_dphi);
          nd.den(k_asymjetmu_jetmudr, (sump_0 - p_mu1)/(sump_0 + p_mu1), jetmu_dr);
          nd.den(k_jetmu_asymsump, (sump_0 - p_mu1)/(sump_0 + p_mu1));
          nd.den(k_jet0_maxeta_mu1_eta, maxeta_0, mu_eta_1);
          nd.den(k_jet0_sump_mu1_p, sump_0, mu1_reco_p);
          nd.den(k_jet0_sump_lep1_p, sump_0, mu1_reco_p);
          nd.den(k_jetmudr_qrk0_dxybs, jetmu_dr, qrk0_dxybs);
          nd.den(k_jetmudr_genmu1_dxybs, jetmu_dr, genmu1_dxybs);
          nd.den(k_jetmudphi_qrk0_dxybs, jetmu_dphi, qrk0_dxybs);
          nd.den(k_jetmudphi_genmu1_dxybs, jetmu_dphi, genmu1_dxybs);
          nd.den(k_closeseedtks_genmu1_dxybs, n_closeseedtks, genmu1_dxybs); 
          nd.den(k_nmovedtks_jetmu_dr, jet_ntks_0, jetmu_dr); //include lepton track? 
          nd.den(k_mu1_p_movedist3, p_mu1, movedist3); 
          nd.den(k_mu1_p_genmu1_dxybs, p_mu1, genmu1_dxybs); 
          nd.den(k_genmu1_p, genmup_1);
          nd.den(k_genmu1_dxybs, genmu1_dxybs);
          nd.den(k_mu1_dxybs, mu1_dxybs);
          nd.den(k_genmutop_mu1, p_mu1/genmup_1);
          nd.den(k_genmutosump_sumpmu1, p_mu1, p_mu1/genmup_1);
          nd.den(k_2p0p1_1mgencos_mu, log10(2*qrkp_0*genmup_1), log10(1-qrkgenmu_costheta));
          nd.den(k_2sump0sump1_1mcos_mu, log10(2*sump_0*p_mu1), log10(1-jetmu_costheta));
          // nd.den(k_1mcosto1mgencos_mu, (1-jetmu_costheta)/(1-qrkgenmu_costheta));
          nd.den(k_2logm_mu, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta));
          nd.den(k_2genlogm_mu, log10(2*qrkp_0*genmup_1) + log10(1-qrkgenmu_costheta));
          nd.den(k_dphi_sum_jmu_mv, jetmu_mv_dphi_sum);
          nd.den(k_deta_sum_jmu_mv, jetmu_mv_deta_sum);
          nd.den(k_dphi_sum_qgm_mv, fabs(qrkgenmu_mv_dphi_sum));
          nd.den(k_jetpt0_asymm_mu, jet_pt_0, jetmu_aj);
          nd.den(k_mupt1_asymm, mu_pt_1, jetmu_aj);
          nd.den(k_jeteta0_asymm_mu, jet_eta_0, jetmu_aj);
          nd.den(k_mueta1_asymm, mu_eta_1, jetmu_aj);
          nd.den(k_jetmudr_asymm, jetmu_dr, jetmu_aj);
          nd.den(k_anglemu1, mu1_lsp_angle);
          nd.den(k_jetmudravg, jetmu_dr);
          nd.den(k_dphi_mu1_mv, fabs(mu_mv_dphi_1));
          nd.den(k_deta_mu1_mv, mu_mv_deta_1);
          nd.den(k_dphi_genmu1_mv, fabs(genmu_mv_dphi_1));
          nd.den(k_jetmudphimax, jetmu_dphi_max);
          nd.den(k_jetmudetamax, jetmu_deta_max);
          nd.den(k_qrkgenmudphimax, qrkgenmu_dphi_max);
          nd.den(k_jetmudphi_mveta, fabs(jetmu_dphi_max), fabs(lsp_p4.Eta()));
          nd.den(k_jetmumovea3d01, jet0_lsp_angle, mu1_lsp_angle);
          nd.den(k_jetmueta01,  jet_eta_0, mu_eta_1);
          nd.den(k_jetmupt01, jet_pt_0, mu_pt_1);
          nd.den(k_pt_anglemu1, mu_pt_1, mu1_lsp_angle);
          nd.den(k_eta_anglemu1, lsp_p4.Eta(), mu1_lsp_angle);
          nd.den(k_llp_sump_mu, sump_0+p_mu1+miscp);
        }
        if (lep_isele) {
          nd.den(k_jetele_asymm, jetele_aj);
          nd.den(k_ele1_eta, ele_eta_1);
          nd.den(k_ele1_p_eta, ele1_reco_p, ele_eta_1); 
          nd.den(k_lep1_p_eta, ele1_reco_p, ele_eta_1); 
          nd.den(k_jetele_dr, jetele_dr);
          nd.den(k_jetele_costheta, jetele_costheta);
          nd.den(k_jetele_deta, jetele_deta);
          nd.den(k_jetele_dphi, jetele_dphi);
          nd.den(k_jetele_deta_dphi, jetele_deta, jetele_dphi);
          nd.den(k_jetlep_deta_dphi, jetele_deta, jetele_dphi);
          nd.den(k_elept1, ele1_reco_pt);
          nd.den(k_ele_dr_minl1_l1, ele_dr_minl1);
          nd.den(k_llp_sump_jeteledphi, sump_0+p_ele1+miscp, jetele_dphi);
          nd.den(k_llp_sump_jeteledr, sump_0+p_ele1+miscp, jetele_dr);
          nd.den(k_jet0_sump_jeteledr, sump_0, jetele_dr);
          nd.den(k_jet0_sump_jetlepdr, sump_0, jetele_dr);
          nd.den(k_ele1_p_jeteledr, ele1_reco_p, jetele_dr);
          nd.den(k_lep1_p_jetlepdr, ele1_reco_p, jetele_dr);
          nd.den(k_ele1_pT_jeteledr, ele1_reco_pt, jetele_dr);
          nd.den(k_lep1_pT_jetlepdr, ele1_reco_pt, jetele_dr);
          nd.den(k_movedist3_jeteledr, movedist3, jetele_dr);
          nd.den(k_movedist3_ele1_p, movedist3, p_ele1);
          nd.den(k_angle2d_jeteledr, movedist2/movedist3, jetele_dr);
          nd.den(k_angle2d_ele1_p, movedist2/movedist3, p_ele1);
          nd.den(k_movedist2_jeteledr, movedist2, jetele_dr);
          nd.den(k_movedist2_ele1_p, movedist2, p_ele1);
          nd.den(k_jetele_costheta_tightcloseseedtks, jetele_costheta, n_tightcloseseedtks);
          nd.den(k_jetele_dr_tightcloseseedtks, jetele_dr, n_tightcloseseedtks);
          nd.den(k_jetele_costheta_closeseedtks, jetele_costheta, n_closeseedtks);
          nd.den(k_jetele_dr_closeseedtks, jetele_dr, n_closeseedtks);
          nd.den(k_lspdist3_genele1_dxybs, lspdist3, genele1_dxybs); 
          nd.den(k_ele1_p, ele1_reco_p);
          nd.den(k_2logm_jeteledr, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta), jetele_dr);
          nd.den(k_2logm_costheta_ele, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta), jetele_costheta);
          nd.den(k_ele1_p_jetele_costheta, p_ele1, jetele_costheta);
          nd.den(k_ele1_p_jetdphi, p_ele1, jetele_dphi);
          nd.den(k_asymjetele_jeteledr, (sump_0 - p_ele1)/(sump_0 + p_ele1), jetele_dr);
          nd.den(k_jetele_asymsump, (sump_0 - p_ele1)/(sump_0 + p_ele1));
          nd.den(k_jet0_maxeta_ele1_eta, maxeta_0, ele_eta_1);
          nd.den(k_jet0_sump_ele1_p, sump_0, ele1_reco_p);
          nd.den(k_jet0_sump_lep1_p, sump_0, ele1_reco_p);
          nd.den(k_jeteledr_qrk0_dxybs, jetele_dr, qrk0_dxybs);
          nd.den(k_jeteledr_genele1_dxybs, jetele_dr, genele1_dxybs);
          nd.den(k_jeteledphi_qrk0_dxybs, jetele_dphi, qrk0_dxybs);
          nd.den(k_jeteledphi_genele1_dxybs, jetele_dphi, genele1_dxybs);
          nd.den(k_closeseedtks_genele1_dxybs, n_closeseedtks, genele1_dxybs); 
          nd.den(k_nmovedtks_jetele_dr, jet_ntks_0, jetele_dr); //include lepton track?
          nd.den(k_ele1_p_movedist3, p_ele1, movedist3); 
          nd.den(k_ele1_p_genele1_dxybs, p_ele1, genele1_dxybs); 
          nd.den(k_genele1_p, genelep_1);
          nd.den(k_genele1_dxybs, genele1_dxybs);
          nd.den(k_ele1_dxybs, ele1_dxybs);
          nd.den(k_geneletop_ele1, p_ele1/genelep_1);
          nd.den(k_geneletosump_sumpele1, p_ele1, p_ele1/genelep_1);
          nd.den(k_2p0p1_1mgencos_ele, log10(2*qrkp_0*genelep_1), log10(1-qrkgenele_costheta));
          nd.den(k_2sump0sump1_1mcos_ele, log10(2*sump_0*p_ele1), log10(1-jetele_costheta));
          // nd.den(k_1mcosto1mgencos_ele, (1-jetele_costheta)/(1-qrkgenele_costheta));
          nd.den(k_2logm_ele, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta));
          nd.den(k_2genlogm_ele, log10(2*qrkp_0*genelep_1) + log10(1-qrkgenele_costheta));
          nd.den(k_dphi_sum_jele_mv, jetele_mv_dphi_sum);
          nd.den(k_deta_sum_jele_mv, jetele_mv_deta_sum);
          nd.den(k_dphi_sum_qge_mv, fabs(qrkgenele_mv_dphi_sum));
          nd.den(k_jetpt0_asymm_ele, jet_pt_0, jetele_aj);
          nd.den(k_elept1_asymm, ele_pt_1, jetele_aj);
          nd.den(k_jeteta0_asymm_ele, jet_eta_0, jetele_aj);
          nd.den(k_eleeta1_asymm, ele_eta_1, jetele_aj);
          nd.den(k_jeteledr_asymm, jetele_dr, jetele_aj);
          nd.den(k_angleele1, ele1_lsp_angle);
          nd.den(k_jeteledravg, jetele_dr);
          nd.den(k_dphi_ele1_mv, fabs(ele_mv_dphi_1));
          nd.den(k_deta_ele1_mv, ele_mv_deta_1);
          nd.den(k_dphi_genele1_mv, fabs(genele_mv_dphi_1));
          nd.den(k_jeteledphimax, jetele_dphi_max);
          nd.den(k_jeteledetamax, jetele_deta_max);
          nd.den(k_qrkgeneledphimax, qrkgenele_dphi_max);
          nd.den(k_jeteledphi_mveta, fabs(jetele_dphi_max), fabs(lsp_p4.Eta()));
          nd.den(k_jetelemovea3d01, jet0_lsp_angle, ele1_lsp_angle);
          nd.den(k_jeteleeta01,  jet_eta_0, ele_eta_1);
          nd.den(k_jetelept01, jet_pt_0, ele_pt_1);
          nd.den(k_pt_angleele1, ele_pt_1, ele1_lsp_angle);
          nd.den(k_eta_angleele1, lsp_p4.Eta(), ele1_lsp_angle);
          nd.den(k_llp_sump_ele, sump_0+p_ele1+miscp);
        }
        nd.den(k_jet0_sump, sump_0);
        // nd.den(k_llp_sump_jetdr, sump_0+sump_1+miscp, jet_dr);
        // nd.den(k_llp_sump, sump_0+sump_1+miscp);

        // nd.den(k_jet0_sump_jetdr, sump_0, jet_dr);
        nd.den(k_movedist3_movedist2, movedist3, movedist2);
        // nd.den(k_movedist3_jetdr, movedist3, jet_dr);
        // nd.den(k_movedist3_jet1_sump, movedist3, sump_1);
        nd.den(k_movedist3_angle2d, movedist3, movedist2/movedist3);
        // nd.den(k_angle2d_jetdr, movedist2/movedist3, jet_dr);
        // nd.den(k_angle2d_jet1_sump, movedist2/movedist3, sump_1);
        // nd.den(k_movedist2_jetdr, movedist2, jet_dr);
        // nd.den(k_movedist2_jet1_sump, movedist2, sump_1);
        nd.den(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
        // nd.den(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
        // nd.den(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
        nd.den(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
        // nd.den(k_movedist3_nmovedtks, movedist3, jet_ntks_0 + jet_ntks_1);
        nd.den(k_movedist3_nmovedcloseseedtks, movedist3, n_movedcloseseedtks);
        nd.den(k_movedist3_nmisccloseseedtks, movedist3, n_misccloseseedtracks);
        nd.den(k_movedist3_nmovedseedtks, movedist3, n_movedseedtks);
        nd.den(k_movedist2_closeseedtks, movedist2, n_closeseedtks);
        // nd.den(k_movedist2_nmovedtks, movedist2, jet_ntks_0 + jet_ntks_1);
        nd.den(k_movedist2_nmovedcloseseedtks, movedist2, n_movedcloseseedtks);
        nd.den(k_movedist2_nmisccloseseedtks, movedist2, n_misccloseseedtracks);
        nd.den(k_movedist2_nmovedseedtks, movedist2, n_movedseedtks);
        // nd.den(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
        // nd.den(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
        nd.den(k_lspdist3_movedcloseseedtks, lspdist3, n_movedcloseseedtks); 
        nd.den(k_lspdist3_movedist3, lspdist3, movedist3); 
        nd.den(k_lspdist3_movedist2, lspdist3, movedist2); 
        nd.den(k_lspdist3_qrk0_dxybs, lspdist3, qrk0_dxybs); 
        // std::cout << "here 4 " << std::endl;

        // nd.den(k_lspdist3_qrk1_dxybs, lspdist3, qrk1_dxybs); 

        //nd.den(k_qrk0_phi_genqrk0_phi, qrk0_phi, quark_p4_0.Phi()); 
        //nd.den(k_qrk1_phi_genqrk1_phi, qrk1_phi, quark_p4_1.Phi()); 
       
        // for (size_t j = 0; j < jet1trk_idx.size(); ++j){
        //   const TLorentzVector jp4 = tks.p4(jet1trk_idx[j]);
        //   nd.den(k_jet1_trk_dr, jp4.DeltaR(minijet_p4_1));
        //   nd.den(k_jet1_trk_pt, tks.pt(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_p, tks.p(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_eta, tks.eta(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //   if (mindist2move_iv != -1) {
        //     const double jet1_vtxdz = tks.dz(jet1trk_idx[j],vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
        //     const double jet1_vtxdxy = tks.dxy(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
        //     nd.den(k_jet1_trk_vtxdxy, jet1_vtxdxy);
        //     nd.den(k_jet1_trk_vtxdz, jet1_vtxdz);
        //     nd.den(k_jet1_trk_nsigmavtxdz, jet1_vtxdz/tks.err_dz(jet1trk_idx[j]));
        //     nd.den(k_jet1_trk_nsigmavtxdxy, jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]));
        //     nd.den(k_jet1_trk_nsigmavtx, sqrt((jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]))*(jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j])) + (jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))*(jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))));
        //   }
        //   nd.den(k_jet1_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_nsigmadz, tks.dzpv(jet1trk_idx[j], pvs)/tks.err_dz(jet1trk_idx[j]));
        //   const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet1trk_idx[j]);
        //   const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet1trk_idx[j]);  
        //   nd.den(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
        //   nd.den(k_jet1_trk_dr_gennsigma, jp4.DeltaR(quark_p4_1), sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //   nd.den(k_jet1_trk_dr_genmissdist, jp4.DeltaR(quark_p4_1), tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));            nd.den(k_jet1_trk_dr_gendz, jp4.DeltaR(quark_p4_1), tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
        //   nd.den(k_jet1_trk_eta_gennsigma, tks.eta(jet1trk_idx[j]), sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //   nd.den(k_jet1_trk_eta_gendz, tks.eta(jet1trk_idx[j]), tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
        //   nd.den(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
        //   nd.den(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
        //   nd.den(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
        //   nd.den(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
        //   nd.den(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        //   nd.den(k_jet1_trk_nsigmadsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0))/tks.err_dz(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
        //   nd.den(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
        //   nd.den(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //   auto itin = std::find(movedseedinvtxtrk_idx.begin(),  movedseedinvtxtrk_idx.end(), jet1trk_idx[j]);
        //   if (itin != movedseedinvtxtrk_idx.end()){
        //     nd.den(k_movedseedinvtx_trk_whichjet, tks.which_jet(jet1trk_idx[j]));
        //     nd.den(k_movedseedinvtx_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        //     nd.den(k_movedseedinvtx_trk_dr, jp4.DeltaR(quark_p4_1));
        //     nd.den(k_movedseedinvtx_trk_p, tks.p(jet1trk_idx[j]));
        //     nd.den(k_movedseedinvtx_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //     nd.den(k_movedseedinvtx_trk_eta, tks.eta(jet1trk_idx[j]));
        //     nd.den(k_movedseedinvtx_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //     nd.den(k_movedseedinvtx_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //     nd.den(k_movedseedinvtx_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //     nd.den(k_movedseedinvtx_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   }
        //   auto itout = std::find(movedseedoutvtxtrk_idx.begin(),  movedseedoutvtxtrk_idx.end(), jet1trk_idx[j]);
        //   if (itout != movedseedoutvtxtrk_idx.end()){
        //     nd.den(k_movedseedoutvtx_trk_dr, jp4.DeltaR(quark_p4_1));
        //     nd.den(k_movedseedoutvtx_trk_p, tks.p(jet1trk_idx[j]));
        //     nd.den(k_movedseedoutvtx_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //     nd.den(k_movedseedoutvtx_trk_eta, tks.eta(jet1trk_idx[j]));
        //     nd.den(k_movedseedoutvtx_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //     nd.den(k_movedseedoutvtx_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //     nd.den(k_movedseedoutvtx_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //     nd.den(k_movedseedoutvtx_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   }
        // }

        // nd.den(k_jet1_sump, sump_1);
        // nd.den(k_jet1_sump_jetdr, sump_1, jet_dr);
        // nd.den(k_2logm_jetdr, log10(2*sump_0*sump_1) + log10(1-jet_costheta), jet_dr);
        // nd.den(k_2logm_costheta, log10(2*sump_0*sump_1) + log10(1-jet_costheta), jet_costheta);
        // nd.den(k_jet1_sump_jet_costheta, sump_1, jet_costheta);
        // nd.den(k_jet1_sump_jetdphi, sump_1, jet_dphi);
        // nd.den(k_jet1_ntks_jetdphi, jet_ntks_1, jet_dphi);
        // nd.den(k_asymjet_jetdr, (sump_0 - sump_1)/(sump_0 + sump_1), jet_dr);
        // nd.den(k_jet_asymsump, (sump_0 - sump_1)/(sump_0 + sump_1));
        // nd.den(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
        // nd.den(k_jet0_sump_jet1_sump, sump_0, sump_1);
        // nd.den(k_jetdr_qrk0_dxybs, jet_dr, qrk0_dxybs);
        // nd.den(k_jetdr_qrk1_dxybs, jet_dr, qrk1_dxybs);
        // nd.den(k_jetdphi_qrk0_dxybs, jet_dphi, qrk0_dxybs);
        // nd.den(k_jetdphi_qrk1_dxybs, jet_dphi, qrk1_dxybs);
        nd.den(k_closeseedtks_qrk0_dxybs, n_closeseedtks, qrk0_dxybs); 
        // nd.den(k_closeseedtks_qrk1_dxybs, n_closeseedtks, qrk1_dxybs); 
        // nd.den(k_nmovedtks_jet_dr, jet_ntks_0 + jet_ntks_1, jet_dr); 
        nd.den(k_nmovedtks0_qrk0_dxybs, jet_ntks_0, qrk0_dxybs); 
        // nd.den(k_nmovedtks1_qrk1_dxybs, jet_ntks_1, qrk1_dxybs); 
        nd.den(k_nmovedseedtks0_qrk0_dxybs, n_movedseedtks0, qrk0_dxybs); 
        // nd.den(k_nmovedseedtks1_qrk1_dxybs, n_movedseedtks1, qrk1_dxybs); 
        nd.den(k_nmovedtks0_jet0_sump, jet_ntks_0, sump_0); 
        // nd.den(k_nmovedtks1_jet1_sump, jet_ntks_1, sump_1); 
        nd.den(k_nmovedseedtks0_jet0_sump, n_movedseedtks0, sump_0); 
        // nd.den(k_nmovedseedtks1_jet1_sump, n_movedseedtks1, sump_1); 
        // nd.den(k_nmovedtks_movedist3, jet_ntks_0 + jet_ntks_1, movedist3); 
        nd.den(k_nmovedtks_movedist3, jet_ntks_0, movedist3); 
        nd.den(k_nmovedseedtks_movedist3, n_movedseedtks, movedist3); 
        // nd.den(k_jet1_sump_movedist3, sump_1, movedist3); 
        nd.den(k_jet0_sump_movedist3, sump_0, movedist3); 
        // nd.den(k_jet1_sump_qrk1_dxybs, sump_1, qrk1_dxybs); 
        nd.den(k_jet0_sump_qrk0_dxybs, sump_0, qrk0_dxybs); 
        //nd.den(k_qrk0_matchthres, qrk0_matchthres);
        //nd.den(k_qrk1_matchthres, qrk1_matchthres);
        nd.den(k_qrk0_p, qrkp_0);
        // nd.den(k_qrk1_p, qrkp_1);
        nd.den(k_qrk0_dxybs, qrk0_dxybs);
        // nd.den(k_qrk1_dxybs, qrk1_dxybs);
        nd.den(k_jet0_dxybs, jet0_dxybs);
        // nd.den(k_jet1_dxybs, jet1_dxybs);
        //nd.den(k_qrk0_mingendxy, qrk0_mingendxy);
        //nd.den(k_qrk1_mingendxy, qrk1_mingendxy);
        nd.den(k_qrktosump_j0, sump_0/qrkp_0);
        // nd.den(k_qrktosump_j1, sump_1/qrkp_1);
        nd.den(k_qrktosump_sumpj0, sump_0, sump_0/qrkp_0);
        // nd.den(k_qrktosump_sumpj1, sump_1, sump_1/qrkp_1);
        // nd.den(k_2p0p1_1mgencos, log10(2*qrkp_0*qrkp_1), log10(1-qrk_costheta));
        // nd.den(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
        // nd.den(k_1mcosto1mgencos, (1-jet_costheta)/(1-qrk_costheta));
        // nd.den(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
        // nd.den(k_2genlogm, log10(2*qrkp_0*qrkp_1) + log10(1-qrk_costheta));
        // nd.den(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
        // nd.den(k_dphi_sum_j_mv, jet_mv_dphi_sum);
        // nd.den(k_deta_sum_j_mv, jet_mv_deta_sum);
        // nd.den(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        // nd.den(k_jetpt0_asymm, jet_pt_0, jet_aj);
        // nd.den(k_jetpt1_asymm, jet_pt_1, jet_aj);
        // nd.den(k_jeteta0_asymm, jet_eta_0, jet_aj);
        // nd.den(k_jeteta1_asymm, jet_eta_1, jet_aj);
        // nd.den(k_jetdr_asymm, jet_dr, jet_aj);
        nd.den(k_angle0, jet0_lsp_angle);
        // nd.den(k_angle1, jet1_lsp_angle);
        // nd.den(k_jetdravg, jet_dr);
        nd.den(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        // nd.den(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.den(k_deta_j0_mv, jet_mv_deta_0);
        // nd.den(k_deta_j1_mv, jet_mv_deta_1);
        nd.den(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        // nd.den(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        // std::cout << "here 5 " << std::endl;

        nd.den(k_nseedtracks, nseedtracks);
        nd.den(k_miscseedtracks, n_miscseedtracks); 
        nd.den(k_misccloseseedtracks, n_misccloseseedtracks); 
        nd.den(k_closeseedtks, n_closeseedtks);
        nd.den(k_sharedcloseseedtks, n_sharedcloseseedtks);
        nd.den(k_tightcloseseedtks, n_tightcloseseedtks);
        nd.den(k_movedseedtks, n_movedseedtks);
        nd.den(k_movedvtxseedtks, n_movedvtxseedtks);
        nd.den(k_movedcloseseedtks, n_movedcloseseedtks);
        nd.den(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
        nd.den(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
        nd.den(k_rat_movedvtxtks_to_movedtks, n_movedvtxseedtks/n_movedseedtks); 
        nd.den(k_rat_movedclosetks_to_movedtks, n_movedcloseseedtks/n_movedseedtks); 
        // nd.den(k_jetdphimax, jet_dphi_max);
        // nd.den(k_jetdetamax, jet_deta_max);
        // nd.den(k_qrkdphimax, qrk_dphi_max);
        // nd.den(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        // nd.den(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        // nd.den(k_jeteta01,  jet_eta_0, jet_eta_1);
        // nd.den(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.den(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        // nd.den(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.den(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        // nd.den(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
        // std::cout << "here 5 " << std::endl;

        nd.den(k_nvtx, nvtx);
        nd.den(k_vtxcat, vtx_cat);
        nd.den(k_vtxbs2derr, vtx_bs2derr);
        nd.den(k_vtxunc, dist2move);
        nd.den(k_vtxeta, vtx_eta);
        nd.den(k_vtxz, vtx_z);
        nd.den(k_vtxdbv, vtx_dbv);
        nd.den(k_vtx3dbv, vtx_3dbv);
        nd.den(k_vtxntk, vtx_ntk);
        nd.den(k_dr, dr);
        nd.den(k_dvv, dvv);
        nd.den(k_dvv2d, dvv2d);
        if (vtx_ntk >= 4 && vtx_bs2derr < 0.0050) nd.den(k_vtxnm1_dbv, vtx_dbv);
        if (vtx_ntk >= 4 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.den(k_vtxnm1_bs2derr, vtx_bs2derr);
        if (vtx_bs2derr < 0.0050 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.den(k_vtxnm1_ntk, vtx_ntk);
        if (vtx_ntk == 3) nd.den(k_vtx3tkchi2, vtx_chi2);
        if (vtx_ntk == 4) nd.den(k_vtx4tkchi2, vtx_chi2);
        if (vtx_ntk == 5) nd.den(k_vtx5tkchi2, vtx_chi2);
        // if (vtx_ntk == 6) nd.den(k_vtx6tkchi2, vtx_chi2);
        if (vtx_ntk == 3) nd.den(k_vtx3tkdbv, vtx_dbv);
        if (vtx_ntk == 4) nd.den(k_vtx4tkdbv, vtx_dbv);
        if (vtx_ntk == 5) nd.den(k_vtx5tkdbv, vtx_dbv);
        // if (vtx_ntk == 6) nd.den(k_vtx6tkdbv, vtx_dbv);
        if (vtx_ntk == 3) nd.den(k_vtx3tkdvv, dvv);
        if (vtx_ntk == 4) nd.den(k_vtx4tkdvv, dvv);
        if (vtx_ntk == 5) nd.den(k_vtx5tkdvv, dvv);
        // if (vtx_ntk == 6) nd.den(k_vtx6tkdvv, dvv);
        if (vtx_ntk == 3) nd.den(k_vtx3tkzdbv, vtx_z);
        if (vtx_ntk == 4) nd.den(k_vtx4tkzdbv, vtx_z);
        if (vtx_ntk == 5) nd.den(k_vtx5tkzdbv, vtx_z);
        // if (vtx_ntk == 6) nd.den(k_vtx6tkzdbv, vtx_z);
        if (vtx_ntk == 3) nd.den(k_vtx3tkunc, dist2move);
        if (vtx_ntk == 4) nd.den(k_vtx4tkunc, dist2move);
        if (vtx_ntk == 5) nd.den(k_vtx5tkunc, dist2move);
        // if (vtx_ntk == 6) nd.den(k_vtx6tkunc, dist2move);
        // std::cout << "here 6 " << std::endl;

      }

      for (int in = 0; in < num_numdens; ++in) {
        int iv = first_vtx_to_pass[in];
        if (iv != -1) {
          h_vtxntracks   [in]->Fill(vs.ntracks(iv));
          h_vtxbs2derr   [in]->Fill(vs.bs2derr(iv));
          //h_vtxtkonlymass[in]->Fill(vs.tkonlymass(iv));
          h_vtxs_mass    [in]->Fill(vs.mass(iv));
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

      for (int in = 0; in < num_numdens; ++in) {
        if (!npasses[in])
          continue;
        numdens& nd = nds[in];
        nd.num(k_decay_x, lspdecay.x());
        nd.num(k_decay_y, lspdecay.y());
        nd.num(k_decay_z, lspdecay.z());
        nd.num(k_decay_xy, lspdecay.x(), lspdecay.y());
        nd.num(k_lspdphi, lspdphi);
        nd.num(k_lspdeta, lspdeta);
        nd.num(k_lspdr, lspdr);
        nd.num(k_lspasymdecay, lspasymdecay);
        nd.num(k_lspcostheta, lspcostheta);
        nd.num(k_lspdist2, lspdist2);
        nd.num(k_lspdist3, lspdist3);
        nd.num(k_lspdist3symmath, lspdist3symmath);
        nd.num(k_ratlspdist3, lspdist3symmath/lspdist3);
        nd.num(k_2sinhalftheta, 2*sin(lspdr/2));
        nd.num(k_lspdistz, lspdistz);
        nd.num(k_movedist2, movedist2);
        nd.num(k_movedist3, movedist3);
        nd.num(k_lspeta, lsp_p4.Eta());
        nd.num(k_lsppt, lsp_p4.Pt());
        nd.num(k_lspgammabeta, lsp_p4.Beta()*lsp_p4.Gamma());
        nd.num(k_lspctau, movedist3/(lsp_p4.Beta()*lsp_p4.Gamma()));
        nd.num(k_npv, pvs.n());
        nd.num(k_pvz, pvs.z(0) + bs.z());
        nd.num(k_dist2dpvbs, sqrt((pvs.x(0)-bs.x(pvs.z(0)))*(pvs.x(0)-bs.x(pvs.z(0))) + (pvs.y(0)-bs.y(pvs.z(0)))*(pvs.y(0)-bs.y(pvs.z(0)))));
        nd.num(k_pvrho, pvs.rho(0));
        nd.num(k_pvntracks, pvs.ntracks(0));
        nd.num(k_pvscore, pvs.score(0));
        nd.num(k_ht, jets.ht());
        nd.num(k_njets, jets.n());
        // nd.num(k_nmuons, nselmuons);
        // nd.num(k_muon_pT, muon_pT);
        // nd.num(k_muon_abseta, muon_abseta);
        // nd.num(k_muon_iso, muon_iso);
        // nd.num(k_muon_absdxybs, muon_absdxybs);
        // nd.num(k_muon_absdz, muon_absdz);
        // nd.num(k_muon_nsigmadxybs, muon_nsigmadxybs);
        // nd.num(k_neles, nseleles);
        // nd.num(k_ele_pT, ele_pT);
        // nd.num(k_ele_abseta, ele_abseta);
        // nd.num(k_ele_iso, ele_iso);
        // nd.num(k_ele_absdxybs, ele_absdxybs);
        // nd.num(k_ele_absdz, ele_absdz);
        // nd.num(k_ele_nsigmadxybs, ele_nsigmadxybs);
        // nd.num(k_met_pT, met_pT);
        // nd.num(k_w_pT, w_pT);
        // nd.num(k_w_mT, w_mT);
        // nd.num(k_z_pT, z_pT);
        // nd.num(k_z_m, z_m);
        // nd.num(k_lnu_absphi, lnu_absphi);
        // nd.num(k_ljet_absdr, ljet_absdr);
        // nd.num(k_ljet0_absdr, ljet0_absdr);
        // nd.num(k_ljet1_absdr, ljet1_absdr);
        // nd.num(k_nujet0_absphi, nujet0_absphi);
        // nd.num(k_nujet1_absphi, nujet1_absphi);
        // nd.num(k_wjet_dphi, fabs(wjet_dphi));
        // nd.num(k_zjet_dphi, fabs(zjet_dphi));

        // nd.num(k_jet_asymm, jet_aj);
        nd.num(k_jet0_eta, jet_eta_0);
        // nd.num(k_jet1_eta, jet_eta_1);
        // nd.num(k_jet_dr, jet_dr);
        // nd.num(k_jet_costheta, jet_costheta);
        // nd.num(k_jet_deta, jet_deta);
        // nd.num(k_jet_dphi, jet_dphi);
        // nd.num(k_jet_dind, jet_dind);
        nd.num(k_pt0, jet_pt_0);
        // nd.num(k_pt1, jet_pt_1);
        nd.num(k_ntks_j0, jet_ntks_0);
        // nd.num(k_ntks_j1, jet_ntks_1);
        nd.num(k_jet_dr_minj0_q0, jet_dr_minjq0);
        // nd.num(k_jet_dr_minj1_q1, jet_dr_minjq1);
        // nd.num(k_ntk0_ntk1, jet_ntks_0, jet_ntks_1);
        nd.num(k_boost0_boost1, boost0, boost1);
        for (size_t j = 0; j < closeseedtrk_idx.size(); ++j){
          nd.num(k_closeseed_trk_genmissdist, tks.dxy(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.num(k_closeseed_trk_gendz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.num(k_closeseed_trk_gennsigmadz, tks.dz(closeseedtrk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(closeseedtrk_idx[j]));
        }
        for (size_t j = 0; j < jet0trk_idx.size(); ++j){
          const TLorentzVector jp4 = tks.p4(jet0trk_idx[j]);
          // nd.num(k_jet0_trk_dr, jp4.DeltaR(jet_p4_0));
          nd.num(k_jet0_trk_pt, tks.pt(jet0trk_idx[j]));
          nd.num(k_jet0_trk_eta, tks.eta(jet0trk_idx[j]));
          nd.num(k_jet0_trk_p, tks.p(jet0trk_idx[j]));
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
          nd.num(k_jet0_trk_nsigmadz, tks.dzpv(jet0trk_idx[j], pvs)/tks.err_dz(jet0trk_idx[j]));
          const double jet0_gennsigmadz = tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet0trk_idx[j]);
          const double jet0_gennsigmamissdist = tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet0trk_idx[j]);  
          nd.num(k_jet0_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));
          nd.num(k_jet0_trk_dr_gennsigma, jp4.DeltaR(quark_p4_0), sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
          nd.num(k_jet0_trk_dr_genmissdist, jp4.DeltaR(quark_p4_0), tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));            
          nd.num(k_jet0_trk_dr_gendz, jp4.DeltaR(quark_p4_0), tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
          nd.num(k_jet0_trk_eta_gennsigma, tks.eta(jet0trk_idx[j]), sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
          nd.num(k_jet0_trk_eta_gendz, tks.eta(jet0trk_idx[j]), tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
          nd.num(k_jet0_trk_gennsigmamissdist, jet0_gennsigmamissdist);
          nd.num(k_jet0_trk_genmissdist, tks.dxy(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
          nd.num(k_jet0_trk_gennsigmadz, jet0_gennsigmadz);
          nd.num(k_jet0_trk_gendz, tks.dz(jet0trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
          nd.num(k_jet0_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
          nd.num(k_jet0_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
          nd.num(k_jet0_trk_nsigmadsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0))/tks.err_dz(jet0trk_idx[j]));
          nd.num(k_jet0_trk_dxy, tks.dxybs(jet0trk_idx[j], bs));
          nd.num(k_jet0_trk_nsigmadxy, tks.dxybs(jet0trk_idx[j], bs)/tks.err_dxy(jet0trk_idx[j]));
          nd.num(k_jet0_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
          for (size_t ind = 0; ind < miscclosetrk_idx.size(); ++ind){
            nd.num(k_miscclose_trk_whichjet, tks.which_jet(miscclosetrk_idx[ind]));
            nd.num(k_miscclose_trk_dsz, tks.dsz(miscclosetrk_idx[ind], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
            nd.num(k_miscclose_trk_p, tks.p(miscclosetrk_idx[ind]));
            nd.num(k_miscclose_trk_eta, tks.eta(miscclosetrk_idx[ind]));
            nd.num(k_miscclose_trk_dzerr, tks.err_dz(miscclosetrk_idx[ind]));
          }
          auto itin = std::find(movedseedinvtxtrk_idx.begin(),  movedseedinvtxtrk_idx.end(), jet0trk_idx[j]);
          if (itin != movedseedinvtxtrk_idx.end()){
            nd.num(k_movedseedinvtx_trk_whichjet, tks.which_jet(jet0trk_idx[j]));
            nd.num(k_movedseedinvtx_trk_dsz, tks.dsz(jet0trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
            nd.num(k_movedseedinvtx_trk_dr, jp4.DeltaR(quark_p4_0));
            nd.num(k_movedseedinvtx_trk_p, tks.p(jet0trk_idx[j]));
            nd.num(k_movedseedinvtx_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
            nd.num(k_movedseedinvtx_trk_eta, tks.eta(jet0trk_idx[j]));
            nd.num(k_movedseedinvtx_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
            nd.num(k_movedseedinvtx_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
            nd.num(k_movedseedinvtx_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
            nd.num(k_movedseedinvtx_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
          }
          auto itout = std::find(movedseedoutvtxtrk_idx.begin(),  movedseedoutvtxtrk_idx.end(), jet0trk_idx[j]);
          if (itout != movedseedoutvtxtrk_idx.end()){
            nd.num(k_movedseedoutvtx_trk_dr, jp4.DeltaR(quark_p4_0));
            nd.num(k_movedseedoutvtx_trk_p, tks.p(jet0trk_idx[j]));
            nd.num(k_movedseedoutvtx_trk_dz, tks.dzpv(jet0trk_idx[j], pvs));
            nd.num(k_movedseedoutvtx_trk_eta, tks.eta(jet0trk_idx[j]));
            nd.num(k_movedseedoutvtx_trk_whichpv, tks.which_pv(jet0trk_idx[j]));
            nd.num(k_movedseedoutvtx_trk_gennsigma, sqrt((jet0_gennsigmamissdist*jet0_gennsigmamissdist) + (jet0_gennsigmadz*jet0_gennsigmadz)));   
            nd.num(k_movedseedoutvtx_trk_dxyerr, tks.err_dxy(jet0trk_idx[j]));
            nd.num(k_movedseedoutvtx_trk_dzerr, tks.err_dz(jet0trk_idx[j]));
          }
        }
        if (lep_ismu) { 
          nd.num(k_jetmu_asymm, jetmu_aj);
          nd.num(k_mu1_eta, mu_eta_1);
          nd.num(k_mu1_p_eta, mu1_reco_p, mu_eta_1);
          nd.num(k_lep1_p_eta, mu1_reco_p, mu_eta_1);
          nd.num(k_jetmu_dr, jetmu_dr);
          nd.num(k_jetmu_costheta, jetmu_costheta);
          nd.num(k_jetmu_deta, jetmu_deta);
          nd.num(k_jetmu_dphi, jetmu_dphi);
          nd.num(k_jetmu_deta_dphi, jetmu_deta, jetmu_dphi);
          nd.num(k_jetlep_deta_dphi, jetmu_deta, jetmu_dphi);
          nd.num(k_mupt1, mu1_reco_pt);
          nd.num(k_mu_dr_minl1_l1, mu_dr_minl1);
          nd.num(k_llp_sump_jetmudphi, sump_0+p_mu1+miscp, jetmu_dphi);
          nd.num(k_llp_sump_jetmudr, sump_0+p_mu1+miscp, jetmu_dr);
          nd.num(k_jet0_sump_jetmudr, sump_0, jetmu_dr);
          nd.num(k_jet0_sump_jetlepdr, sump_0, jetmu_dr);
          nd.num(k_mu1_p_jetmudr, mu1_reco_p, jetmu_dr);
          nd.num(k_lep1_p_jetlepdr, mu1_reco_p, jetmu_dr);
          nd.num(k_mu1_pT_jetmudr, mu1_reco_pt, jetmu_dr);
          nd.num(k_lep1_pT_jetlepdr, mu1_reco_pt, jetmu_dr);

          nd.num(k_movedist3_jetmudr, movedist3, jetmu_dr);
          nd.num(k_movedist3_mu1_p, movedist3, p_mu1);
          nd.num(k_angle2d_jetmudr, movedist2/movedist3, jetmu_dr);
          nd.num(k_angle2d_mu1_p, movedist2/movedist3, p_mu1);
          nd.num(k_movedist2_jetmudr, movedist2, jetmu_dr);
          nd.num(k_movedist2_mu1_p, movedist2, p_mu1);
          nd.num(k_jetmu_costheta_tightcloseseedtks, jetmu_costheta, n_tightcloseseedtks);
          nd.num(k_jetmu_dr_tightcloseseedtks, jetmu_dr, n_tightcloseseedtks);
          nd.num(k_jetmu_costheta_closeseedtks, jetmu_costheta, n_closeseedtks);
          nd.num(k_jetmu_dr_closeseedtks, jetmu_dr, n_closeseedtks);
          nd.num(k_lspdist3_genmu1_dxybs, lspdist3, genmu1_dxybs); 
          nd.num(k_mu1_p, mu1_reco_p);
          nd.num(k_2logm_jetmudr, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta), jetmu_dr);
          nd.num(k_2logm_costheta_mu, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta), jetmu_costheta);
          nd.num(k_mu1_p_jetmu_costheta, p_mu1, jetmu_costheta);
          nd.num(k_mu1_p_jetdphi, p_mu1, jetmu_dphi);
          nd.num(k_asymjetmu_jetmudr, (sump_0 - p_mu1)/(sump_0 + p_mu1), jetmu_dr);
          nd.num(k_jetmu_asymsump, (sump_0 - p_mu1)/(sump_0 + p_mu1));
          nd.num(k_jet0_maxeta_mu1_eta, maxeta_0, mu_eta_1);
          nd.num(k_jet0_sump_mu1_p, sump_0, mu1_reco_p);
          nd.num(k_jet0_sump_lep1_p, sump_0, mu1_reco_p);
          nd.num(k_jetmudr_qrk0_dxybs, jetmu_dr, qrk0_dxybs);
          nd.num(k_jetmudr_genmu1_dxybs, jetmu_dr, genmu1_dxybs);
          nd.num(k_jetmudphi_qrk0_dxybs, jetmu_dphi, qrk0_dxybs);
          nd.num(k_jetmudphi_genmu1_dxybs, jetmu_dphi, genmu1_dxybs);
          nd.num(k_closeseedtks_genmu1_dxybs, n_closeseedtks, genmu1_dxybs);
          nd.num(k_nmovedtks_jetmu_dr, jet_ntks_0, jetmu_dr); //include lepton track? 
          nd.num(k_mu1_p_movedist3, p_mu1, movedist3); 
          nd.num(k_mu1_p_genmu1_dxybs, p_mu1, genmu1_dxybs); 
          nd.num(k_genmu1_p, genmup_1);
          nd.num(k_genmu1_dxybs, genmu1_dxybs);
          nd.num(k_mu1_dxybs, mu1_dxybs);
          nd.num(k_genmutop_mu1, p_mu1/genmup_1);
          nd.num(k_genmutosump_sumpmu1, p_mu1, p_mu1/genmup_1);
          nd.num(k_2p0p1_1mgencos_mu, log10(2*qrkp_0*genmup_1), log10(1-qrkgenmu_costheta));
          nd.num(k_2sump0sump1_1mcos_mu, log10(2*sump_0*p_mu1), log10(1-jetmu_costheta));
          // nd.num(k_1mcosto1mgencos_mu, (1-jetmu_costheta)/(1-qrkgenmu_costheta));
          nd.num(k_2logm_mu, log10(2*sump_0*p_mu1) + log10(1-jetmu_costheta));
          nd.num(k_2genlogm_mu, log10(2*qrkp_0*genmup_1) + log10(1-qrkgenmu_costheta));
          nd.num(k_dphi_sum_jmu_mv, jetmu_mv_dphi_sum);
          nd.num(k_deta_sum_jmu_mv, jetmu_mv_deta_sum);
          nd.num(k_dphi_sum_qgm_mv, fabs(qrkgenmu_mv_dphi_sum));
          nd.num(k_jetpt0_asymm_mu, jet_pt_0, jetmu_aj);
          nd.num(k_mupt1_asymm, mu_pt_1, jetmu_aj);
          nd.num(k_jeteta0_asymm_mu, jet_eta_0, jetmu_aj);
          nd.num(k_mueta1_asymm, mu_eta_1, jetmu_aj);
          nd.num(k_jetmudr_asymm, jetmu_dr, jetmu_aj);
          nd.num(k_anglemu1, mu1_lsp_angle);
          nd.num(k_jetmudravg, jetmu_dr);
          nd.num(k_dphi_mu1_mv, fabs(mu_mv_dphi_1));
          nd.num(k_deta_mu1_mv, mu_mv_deta_1);
          nd.num(k_dphi_genmu1_mv, fabs(genmu_mv_dphi_1));
          nd.num(k_jetmudphimax, jetmu_dphi_max);
          nd.num(k_jetmudetamax, jetmu_deta_max);
          nd.num(k_qrkgenmudphimax, qrkgenmu_dphi_max);
          nd.num(k_jetmudphi_mveta, fabs(jetmu_dphi_max), fabs(lsp_p4.Eta()));
          nd.num(k_jetmumovea3d01, jet0_lsp_angle, mu1_lsp_angle);
          nd.num(k_jetmueta01,  jet_eta_0, mu_eta_1);
          nd.num(k_jetmupt01, jet_pt_0, mu_pt_1);
          nd.num(k_pt_anglemu1, mu_pt_1, mu1_lsp_angle);
          nd.num(k_eta_anglemu1, lsp_p4.Eta(), mu1_lsp_angle);
        }
        if (lep_isele) {
          nd.num(k_jetele_asymm, jetele_aj);
          nd.num(k_ele1_eta, ele_eta_1);
          nd.den(k_ele1_p_eta, ele1_reco_p, ele_eta_1); 
          nd.den(k_lep1_p_eta, ele1_reco_p, ele_eta_1); 
          nd.num(k_jetele_dr, jetele_dr);
          nd.num(k_jetele_costheta, jetele_costheta);
          nd.num(k_jetele_deta, jetele_deta);
          nd.num(k_jetele_dphi, jetele_dphi);
          nd.num(k_jetele_deta_dphi, jetele_deta, jetele_dphi);
          nd.num(k_jetlep_deta_dphi, jetele_deta, jetele_dphi);
          nd.num(k_elept1, ele1_reco_pt);
          nd.num(k_ele_dr_minl1_l1, ele_dr_minl1);
          nd.num(k_llp_sump_jeteledphi, sump_0+p_ele1+miscp, jetele_dphi);
          nd.num(k_llp_sump_jeteledr, sump_0+p_ele1+miscp, jetele_dr);
          nd.num(k_jet0_sump_jeteledr, sump_0, jetele_dr);
          nd.num(k_jet0_sump_jetlepdr, sump_0, jetele_dr);
          nd.num(k_ele1_p_jeteledr, ele1_reco_p, jetele_dr);
          nd.num(k_lep1_p_jetlepdr, ele1_reco_p, jetele_dr);
          nd.num(k_ele1_pT_jeteledr, ele1_reco_pt, jetele_dr);
          nd.num(k_lep1_pT_jetlepdr, ele1_reco_pt, jetele_dr);
          nd.num(k_movedist3_jeteledr, movedist3, jetele_dr);
          nd.num(k_movedist3_ele1_p, movedist3, p_ele1);
          nd.num(k_angle2d_jeteledr, movedist2/movedist3, jetele_dr);
          nd.num(k_angle2d_ele1_p, movedist2/movedist3, p_ele1);
          nd.num(k_movedist2_jeteledr, movedist2, jetele_dr);
          nd.num(k_movedist2_ele1_p, movedist2, p_ele1);
          nd.num(k_jetele_costheta_tightcloseseedtks, jetele_costheta, n_tightcloseseedtks);
          nd.num(k_jetele_dr_tightcloseseedtks, jetele_dr, n_tightcloseseedtks);
          nd.num(k_jetele_costheta_closeseedtks, jetele_costheta, n_closeseedtks);
          nd.num(k_jetele_dr_closeseedtks, jetele_dr, n_closeseedtks);
          nd.num(k_lspdist3_genele1_dxybs, lspdist3, genele1_dxybs); 
          nd.num(k_ele1_p, ele1_reco_p);
          nd.num(k_2logm_jeteledr, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta), jetele_dr);
          nd.num(k_2logm_costheta_ele, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta), jetele_costheta);
          nd.num(k_ele1_p_jetele_costheta, p_ele1, jetele_costheta);
          nd.num(k_ele1_p_jetdphi, p_ele1, jetele_dphi);
          nd.num(k_asymjetele_jeteledr, (sump_0 - p_ele1)/(sump_0 + p_ele1), jetele_dr);
          nd.num(k_jetele_asymsump, (sump_0 - p_ele1)/(sump_0 + p_ele1));
          nd.num(k_jet0_maxeta_ele1_eta, maxeta_0, ele_eta_1);
          nd.num(k_jet0_sump_ele1_p, sump_0, ele1_reco_p);
          nd.num(k_jet0_sump_lep1_p, sump_0, ele1_reco_p);
          nd.num(k_jeteledr_qrk0_dxybs, jetele_dr, qrk0_dxybs);
          nd.num(k_jeteledr_genele1_dxybs, jetele_dr, genele1_dxybs);
          nd.num(k_jeteledphi_qrk0_dxybs, jetele_dphi, qrk0_dxybs);
          nd.num(k_jeteledphi_genele1_dxybs, jetele_dphi, genele1_dxybs);
          nd.num(k_closeseedtks_genele1_dxybs, n_closeseedtks, genele1_dxybs); 
          nd.num(k_nmovedtks_jetele_dr, jet_ntks_0, jetele_dr); //include lepton track?
          nd.num(k_ele1_p_movedist3, p_ele1, movedist3); 
          nd.num(k_ele1_p_genele1_dxybs, p_ele1, genele1_dxybs); 
          nd.num(k_genele1_p, genelep_1);
          nd.num(k_genele1_dxybs, genele1_dxybs);
          nd.num(k_ele1_dxybs, ele1_dxybs);
          nd.num(k_geneletop_ele1, p_ele1/genelep_1);
          nd.num(k_geneletosump_sumpele1, p_ele1, p_ele1/genelep_1);
          nd.num(k_2p0p1_1mgencos_ele, log10(2*qrkp_0*genelep_1), log10(1-qrkgenele_costheta));
          nd.num(k_2sump0sump1_1mcos_ele, log10(2*sump_0*p_ele1), log10(1-jetele_costheta));
          // nd.num(k_1mcosto1mgencos_ele, (1-jetele_costheta)/(1-qrkgenele_costheta));
          nd.num(k_2logm_ele, log10(2*sump_0*p_ele1) + log10(1-jetele_costheta));
          nd.num(k_2genlogm_ele, log10(2*qrkp_0*genelep_1) + log10(1-qrkgenele_costheta));
          nd.num(k_dphi_sum_jele_mv, jetele_mv_dphi_sum);
          nd.num(k_deta_sum_jele_mv, jetele_mv_deta_sum);
          nd.num(k_dphi_sum_qge_mv, fabs(qrkgenele_mv_dphi_sum));
          nd.num(k_jetpt0_asymm_ele, jet_pt_0, jetele_aj);
          nd.num(k_elept1_asymm, ele_pt_1, jetele_aj);
          nd.num(k_jeteta0_asymm_ele, jet_eta_0, jetele_aj);
          nd.num(k_eleeta1_asymm, ele_eta_1, jetele_aj);
          nd.num(k_jeteledr_asymm, jetele_dr, jetele_aj);
          nd.num(k_angleele1, ele1_lsp_angle);
          nd.num(k_jeteledravg, jetele_dr);
          nd.num(k_dphi_ele1_mv, fabs(ele_mv_dphi_1));
          nd.num(k_deta_ele1_mv, ele_mv_deta_1);
          nd.num(k_dphi_genele1_mv, fabs(genele_mv_dphi_1));
          nd.num(k_jeteledphimax, jetele_dphi_max);
          nd.num(k_jeteledetamax, jetele_deta_max);
          nd.num(k_qrkgeneledphimax, qrkgenele_dphi_max);
          nd.num(k_jeteledphi_mveta, fabs(jetele_dphi_max), fabs(lsp_p4.Eta()));
          nd.num(k_jetelemovea3d01, jet0_lsp_angle, ele1_lsp_angle);
          nd.num(k_jeteleeta01,  jet_eta_0, ele_eta_1);
          nd.num(k_jetelept01, jet_pt_0, ele_pt_1);
          nd.num(k_pt_angleele1, ele_pt_1, ele1_lsp_angle);
          nd.num(k_eta_angleele1, lsp_p4.Eta(), ele1_lsp_angle);
        }

        nd.num(k_jet0_sump, sump_0);
        // nd.num(k_llp_sump_jetdphi, sump_0+sump_1+miscp, jet_dphi);
        // nd.num(k_llp_sump_jetdr, sump_0+sump_1+miscp, jet_dr);
        // nd.num(k_llp_sump, sump_0+sump_1+miscp);
        nd.num(k_llp_sump_mu, sump_0+p_mu1+miscp);
        nd.num(k_llp_sump_ele, sump_0+p_ele1+miscp);

        // nd.num(k_jet0_sump_jetdr, sump_0, jet_dr);
        nd.num(k_movedist3_movedist2, movedist3, movedist2);
        // nd.num(k_movedist3_jetdr, movedist3, jet_dr);
        // nd.num(k_movedist3_jet1_sump, movedist3, sump_1);
        nd.num(k_movedist3_angle2d, movedist3, movedist2/movedist3);
        // nd.num(k_angle2d_jetdr, movedist2/movedist3, jet_dr);
        // nd.num(k_angle2d_jet1_sump, movedist2/movedist3, sump_1);
        // nd.num(k_movedist2_jetdr, movedist2, jet_dr);
        // nd.num(k_movedist2_jet1_sump, movedist2, sump_1);
        nd.num(k_movedist3_tightcloseseedtks, movedist3, n_tightcloseseedtks);
        // nd.num(k_jet_costheta_tightcloseseedtks, jet_costheta, n_tightcloseseedtks);
        // nd.num(k_jet_dr_tightcloseseedtks, jet_dr, n_tightcloseseedtks);
        nd.num(k_movedist3_closeseedtks, movedist3, n_closeseedtks);
        // nd.num(k_movedist3_nmovedtks, movedist3, jet_ntks_0 + jet_ntks_1);
        nd.num(k_movedist3_nmovedcloseseedtks, movedist3, n_movedcloseseedtks);
        nd.num(k_movedist3_nmisccloseseedtks, movedist3, n_misccloseseedtracks);
        nd.num(k_movedist3_nmovedseedtks, movedist3, n_movedseedtks);
        nd.num(k_movedist2_closeseedtks, movedist2, n_closeseedtks);
        // nd.num(k_movedist2_nmovedtks, movedist2, jet_ntks_0 + jet_ntks_1);
        nd.num(k_movedist2_nmovedcloseseedtks, movedist2, n_movedcloseseedtks);
        nd.num(k_movedist2_nmisccloseseedtks, movedist2, n_misccloseseedtracks);
        nd.num(k_movedist2_nmovedseedtks, movedist2, n_movedseedtks);
        //nd.num(k_jet_costheta_closeseedtks, jet_costheta, n_closeseedtks);
        //nd.num(k_jet_dr_closeseedtks, jet_dr, n_closeseedtks);
        nd.num(k_lspdist3_movedcloseseedtks, lspdist3, n_movedcloseseedtks); 
        nd.num(k_lspdist3_movedist3, lspdist3, movedist3); 
        nd.num(k_lspdist3_movedist2, lspdist3, movedist2); 
        nd.num(k_lspdist3_qrk0_dxybs, lspdist3, qrk0_dxybs); 
        // nd.num(k_lspdist3_qrk1_dxybs, lspdist3, qrk1_dxybs); 

        //nd.num(k_qrk0_phi_genqrk0_phi, qrk0_phi, quark_p4_0.Phi()); 
        //nd.num(k_qrk1_phi_genqrk1_phi, qrk1_phi, quark_p4_1.Phi()); 
        
        // for (size_t j = 0; j < jet1trk_idx.size(); ++j){
        //   const TLorentzVector jp4 = tks.p4(jet1trk_idx[j]);
        //   nd.num(k_jet1_trk_dr, jp4.DeltaR(minijet_p4_1));
        //   nd.num(k_jet1_trk_pt, tks.pt(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_eta, tks.eta(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_p, tks.p(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //   if (mindist2move_iv != -1) {
        //     const double jet1_vtxdz = tks.dz(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)),vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)),vs.z(mindist2move_iv)); 
        //     const double jet1_vtxdxy = tks.dxy(jet1trk_idx[j], vs.x(mindist2move_iv) + bs.x(vs.z(mindist2move_iv)), vs.y(mindist2move_iv) + bs.y(vs.z(mindist2move_iv)));
        //     nd.num(k_jet1_trk_vtxdxy, jet1_vtxdxy);
        //     nd.num(k_jet1_trk_vtxdz, jet1_vtxdz);
        //     nd.num(k_jet1_trk_nsigmavtxdz, jet1_vtxdz/tks.err_dz(jet1trk_idx[j]));
        //     nd.num(k_jet1_trk_nsigmavtxdxy, jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]));
        //     nd.num(k_jet1_trk_nsigmavtx, sqrt((jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j]))*(jet1_vtxdxy/tks.err_dxy(jet1trk_idx[j])) + (jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))*(jet1_vtxdz/tks.err_dz(jet1trk_idx[j]))));
        //   }
        //   nd.num(k_jet1_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_nsigmadz, tks.dzpv(jet1trk_idx[j], pvs)/tks.err_dz(jet1trk_idx[j]));
        //   const double jet1_gennsigmadz = tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp))/tks.err_dz(jet1trk_idx[j]);
        //   const double jet1_gennsigmamissdist = tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp))/tks.err_dxy(jet1trk_idx[j]);  
        //   nd.num(k_jet1_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));
        //   nd.num(k_jet1_trk_dr_gennsigma, jp4.DeltaR(quark_p4_1), sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //   nd.num(k_jet1_trk_dr_genmissdist, jp4.DeltaR(quark_p4_1), tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));            nd.num(k_jet1_trk_dr_gendz, jp4.DeltaR(quark_p4_1), tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
        //   nd.num(k_jet1_trk_eta_gennsigma, tks.eta(jet1trk_idx[j]), sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //   nd.num(k_jet1_trk_eta_gendz, tks.eta(jet1trk_idx[j]), tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));   
        //   nd.num(k_jet1_trk_gennsigmamissdist, jet1_gennsigmamissdist);
        //   nd.num(k_jet1_trk_genmissdist, tks.dxy(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp)));
        //   nd.num(k_jet1_trk_gennsigmadz, jet1_gennsigmadz);
        //   nd.num(k_jet1_trk_gendz, tks.dz(jet1trk_idx[j], gen.decay_x(ilsp), gen.decay_y(ilsp), gen.decay_z(ilsp)));
        //   nd.num(k_jet1_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        //   nd.num(k_jet1_trk_nsigmadsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0))/tks.err_dz(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_dxy, tks.dxybs(jet1trk_idx[j], bs));
        //   nd.num(k_jet1_trk_nsigmadxy, tks.dxybs(jet1trk_idx[j], bs)/tks.err_dxy(jet1trk_idx[j]));
        //   nd.num(k_jet1_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //   auto itin = std::find(movedseedinvtxtrk_idx.begin(),  movedseedinvtxtrk_idx.end(), jet1trk_idx[j]);
        //   if (itin != movedseedinvtxtrk_idx.end()){
        //     nd.num(k_movedseedinvtx_trk_whichjet, tks.which_jet(jet1trk_idx[j]));
        //     nd.num(k_movedseedinvtx_trk_dsz, tks.dsz(jet1trk_idx[j], pvs.x(0) + bs.x(pvs.z(0)), pvs.y(0) + bs.y(pvs.z(0)), pvs.z(0)));
        //     nd.num(k_movedseedinvtx_trk_dr, jp4.DeltaR(quark_p4_1));
        //     nd.num(k_movedseedinvtx_trk_p, tks.p(jet1trk_idx[j]));
        //     nd.num(k_movedseedinvtx_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //     nd.num(k_movedseedinvtx_trk_eta, tks.eta(jet1trk_idx[j]));
        //     nd.num(k_movedseedinvtx_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //     nd.num(k_movedseedinvtx_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //     nd.num(k_movedseedinvtx_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //     nd.num(k_movedseedinvtx_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   }
        //   auto itout = std::find(movedseedoutvtxtrk_idx.begin(),  movedseedoutvtxtrk_idx.end(), jet1trk_idx[j]);
        //   if (itout != movedseedoutvtxtrk_idx.end()){
        //     nd.num(k_movedseedoutvtx_trk_dr, jp4.DeltaR(quark_p4_1));
        //     nd.num(k_movedseedoutvtx_trk_p, tks.p(jet1trk_idx[j]));
        //     nd.num(k_movedseedoutvtx_trk_dz, tks.dzpv(jet1trk_idx[j], pvs));
        //     nd.num(k_movedseedoutvtx_trk_eta, tks.eta(jet1trk_idx[j]));
        //     nd.num(k_movedseedoutvtx_trk_whichpv, tks.which_pv(jet1trk_idx[j]));
        //     nd.num(k_movedseedoutvtx_trk_gennsigma, sqrt((jet1_gennsigmamissdist*jet1_gennsigmamissdist) + (jet1_gennsigmadz*jet1_gennsigmadz)));   
        //     nd.num(k_movedseedoutvtx_trk_dxyerr, tks.err_dxy(jet1trk_idx[j]));
        //     nd.num(k_movedseedoutvtx_trk_dzerr, tks.err_dz(jet1trk_idx[j]));
        //   }
        // }

        // nd.num(k_jet1_sump, sump_1);
        // nd.num(k_jet1_sump_jetdr, sump_1, jet_dr);
        // nd.num(k_2logm_jetdr, log10(2*sump_0*sump_1) + log10(1-jet_costheta), jet_dr);
        // nd.num(k_2logm_costheta, log10(2*sump_0*sump_1) + log10(1-jet_costheta), jet_costheta);
        // nd.num(k_jet1_sump_jet_costheta, sump_1, jet_costheta);
        // nd.num(k_jet1_sump_jetdphi, sump_1, jet_dphi);
        // nd.num(k_jet1_ntks_jetdphi, jet_ntks_1, jet_dphi);
        // nd.num(k_asymjet_jetdr, (sump_0 - sump_1)/(sump_0 + sump_1), jet_dr);
        // nd.num(k_jet_asymsump, (sump_0 - sump_1)/(sump_0 + sump_1));
        // nd.num(k_jet0_maxeta_jet1_maxeta, maxeta_0, maxeta_1);
        // nd.num(k_jet0_sump_jet1_sump, sump_0, sump_1);
        // nd.num(k_jetdr_qrk0_dxybs, jet_dr, qrk0_dxybs);
        // nd.num(k_jetdr_qrk1_dxybs, jet_dr, qrk1_dxybs);
        // nd.num(k_jetdphi_qrk0_dxybs, jet_dphi, qrk0_dxybs);
        // nd.num(k_jetdphi_qrk1_dxybs, jet_dphi, qrk1_dxybs);
        nd.num(k_closeseedtks_qrk0_dxybs, n_closeseedtks, qrk0_dxybs); 
        // nd.num(k_closeseedtks_qrk1_dxybs, n_closeseedtks, qrk1_dxybs); 
        // nd.num(k_nmovedtks_jet_dr, jet_ntks_0 + jet_ntks_1, jet_dr); 
        nd.num(k_nmovedtks0_qrk0_dxybs, jet_ntks_0, qrk0_dxybs); 
        // nd.num(k_nmovedtks1_qrk1_dxybs, jet_ntks_1, qrk1_dxybs); 
        nd.num(k_nmovedseedtks0_qrk0_dxybs, n_movedseedtks0, qrk0_dxybs); 
        // nd.num(k_nmovedseedtks1_qrk1_dxybs, n_movedseedtks1, qrk1_dxybs); 
        nd.num(k_nmovedtks0_jet0_sump, jet_ntks_0, sump_0); 
        // nd.num(k_nmovedtks1_jet1_sump, jet_ntks_1, sump_1); 
        nd.num(k_nmovedseedtks0_jet0_sump, n_movedseedtks0, sump_0); 
        // nd.num(k_nmovedseedtks1_jet1_sump, n_movedseedtks1, sump_1); 
        // nd.num(k_nmovedtks_movedist3, jet_ntks_0 + jet_ntks_1, movedist3); 
        nd.num(k_nmovedseedtks_movedist3, n_movedseedtks, movedist3); 
        // nd.num(k_jet1_sump_movedist3, sump_1, movedist3); 
        nd.num(k_jet0_sump_movedist3, sump_0, movedist3); 
        // nd.num(k_jet1_sump_qrk1_dxybs, sump_1, qrk1_dxybs); 
        nd.num(k_jet0_sump_qrk0_dxybs, sump_0, qrk0_dxybs); 
        //nd.num(k_qrk0_matchthres, qrk0_matchthres);
        //nd.num(k_qrk1_matchthres, qrk1_matchthres);
        nd.num(k_qrk0_p, qrkp_0);
        // nd.num(k_qrk1_p, qrkp_1);
        nd.num(k_qrk0_dxybs, qrk0_dxybs);
        // nd.num(k_qrk1_dxybs, qrk1_dxybs);
        nd.num(k_jet0_dxybs, jet0_dxybs);
        // nd.num(k_jet1_dxybs, jet1_dxybs);
        //nd.num(k_qrk0_mingendxy, qrk0_mingendxy);
        //nd.num(k_qrk1_mingendxy, qrk1_mingendxy);
        nd.num(k_qrktosump_j0, sump_0/qrkp_0);
        // nd.num(k_qrktosump_j1, sump_1/qrkp_1);
        nd.num(k_qrktosump_sumpj0, sump_0, sump_0/qrkp_0);
        // nd.num(k_qrktosump_sumpj1, sump_1, sump_1/qrkp_1);
        // nd.num(k_2p0p1_1mgencos, log10(2*qrkp_0*qrkp_1), log10(1-qrk_costheta));
        // nd.num(k_2sump0sump1_1mcos, log10(2*sump_0*sump_1), log10(1-jet_costheta));
        // nd.num(k_1mcosto1mgencos, (1-jet_costheta)/(1-qrk_costheta));
        // nd.num(k_2logm, log10(2*sump_0*sump_1) + log10(1-jet_costheta));
        // nd.num(k_2genlogm, log10(2*qrkp_0*qrkp_1) + log10(1-qrk_costheta));
        // nd.num(k_nmovedtracks, jet_ntks_0 + jet_ntks_1);
        // nd.num(k_dphi_sum_j_mv, fabs(jet_mv_dphi_sum));
        // nd.num(k_deta_sum_j_mv, jet_mv_deta_sum);
        // nd.num(k_dphi_sum_q_mv, fabs(qrk_mv_dphi_sum));
        // nd.num(k_jetpt0_asymm, jet_pt_0, jet_aj);
        // nd.num(k_jetpt1_asymm, jet_pt_1, jet_aj);
        // nd.num(k_jeteta0_asymm, jet_eta_0, jet_aj);
        // nd.num(k_jeteta1_asymm, jet_eta_1, jet_aj);
        // nd.num(k_jetdr_asymm, jet_dr, jet_aj);
        // nd.num(k_jetdravg, jet_dr);
        nd.num(k_angle0, jet0_lsp_angle);
        // nd.num(k_angle1, jet1_lsp_angle);
        nd.num(k_dphi_j0_mv, fabs(jet_mv_dphi_0));
        // nd.num(k_dphi_j1_mv, fabs(jet_mv_dphi_1));
        nd.num(k_deta_j0_mv, jet_mv_deta_0);
        // nd.num(k_deta_j1_mv, jet_mv_deta_1);
        nd.num(k_dphi_q0_mv, fabs(qrk_mv_dphi_0));
        // nd.num(k_dphi_q1_mv, fabs(qrk_mv_dphi_1));
        nd.num(k_nseedtracks, nseedtracks);
        nd.num(k_miscseedtracks, n_miscseedtracks); 
        nd.num(k_misccloseseedtracks, n_misccloseseedtracks); 
        nd.num(k_closeseedtks, n_closeseedtks);
        nd.num(k_sharedcloseseedtks, n_sharedcloseseedtks);
        nd.num(k_tightcloseseedtks, n_tightcloseseedtks);
        nd.num(k_movedseedtks, n_movedseedtks);
        nd.num(k_movedvtxseedtks, n_movedvtxseedtks);
        nd.num(k_movedcloseseedtks, n_movedcloseseedtks);
        nd.num(k_rat_moved_to_closetks, n_movedcloseseedtks/n_closeseedtks); 
        nd.num(k_rat_moved_to_vtxtks, n_movedvtxseedtks/vtx_ntk); 
        nd.num(k_rat_movedvtxtks_to_movedtks, n_movedvtxseedtks/n_movedseedtks); 
        nd.num(k_rat_movedclosetks_to_movedtks, n_movedcloseseedtks/n_movedseedtks); 
        // nd.num(k_jetdphimax, jet_dphi_max);
        // nd.num(k_jetdetamax, jet_deta_max);
        // nd.num(k_qrkdphimax, qrk_dphi_max);
        // nd.num(k_jetdphi_mveta, fabs(jet_dphi_max), fabs(lsp_p4.Eta()));
        // nd.num(k_jetmovea3d01, jet0_lsp_angle, jet1_lsp_angle);
        // nd.num(k_jeteta01,  jet_eta_0, jet_eta_1);
        // nd.num(k_jetpt01, jet_pt_0, jet_pt_1);
        nd.num(k_pt_angle0, jet_pt_0, jet0_lsp_angle);
        // nd.num(k_pt_angle1, jet_pt_1, jet1_lsp_angle);
        nd.num(k_eta_angle0, lsp_p4.Eta(), jet0_lsp_angle);
        // nd.num(k_eta_angle1, lsp_p4.Eta(), jet1_lsp_angle);
        nd.num(k_nvtx, npasses[in]);
        nd.num(k_vtxcat, vtx_cat);
        nd.num(k_vtxbs2derr, vtx_bs2derr);
        nd.num(k_vtxunc, dist2move);
        nd.num(k_vtxeta, vtx_eta);
        nd.num(k_vtxz, vtx_z);
        nd.num(k_vtxdbv, vtx_dbv);
        nd.num(k_vtx3dbv, vtx_3dbv);
        nd.num(k_vtxntk, vtx_ntk);
        nd.num(k_dr, dr);
        nd.num(k_dvv, dvv);
        nd.num(k_dvv2d, dvv2d);
        if (vtx_ntk >= 4 && vtx_bs2derr < 0.0050) nd.num(k_vtxnm1_dbv, vtx_dbv);
        if (vtx_ntk >= 4 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.num(k_vtxnm1_bs2derr, vtx_bs2derr);
        if (vtx_bs2derr < 0.0050 && vtx_dbv > 0.0100 && vtx_dbv < 2.0) nd.num(k_vtxnm1_ntk, vtx_ntk);
        if (vtx_ntk == 3) nd.num(k_vtx3tkchi2, vtx_chi2);
        if (vtx_ntk == 4) nd.num(k_vtx4tkchi2, vtx_chi2);
        if (vtx_ntk == 5) nd.num(k_vtx5tkchi2, vtx_chi2);
        if (vtx_ntk == 3) nd.num(k_vtx3tkdbv, vtx_dbv);
        if (vtx_ntk == 4) nd.num(k_vtx4tkdbv, vtx_dbv);
        if (vtx_ntk == 5) nd.num(k_vtx5tkdbv, vtx_dbv);
        if (vtx_ntk == 3) nd.num(k_vtx3tkdvv, dvv);
        if (vtx_ntk == 4) nd.num(k_vtx4tkdvv, dvv);
        if (vtx_ntk == 5) nd.num(k_vtx5tkdvv, dvv);
        if (vtx_ntk == 3) nd.num(k_vtx3tkzdbv, vtx_z);
        if (vtx_ntk == 4) nd.num(k_vtx4tkzdbv, vtx_z);
        if (vtx_ntk == 5) nd.num(k_vtx5tkzdbv, vtx_z);
        if (vtx_ntk == 3) nd.num(k_vtx3tkunc, dist2move);
        if (vtx_ntk == 4) nd.num(k_vtx4tkunc, dist2move);
        if (vtx_ntk == 5) nd.num(k_vtx5tkunc, dist2move);
      }
    }

    // Loop over each event 

    den = 0;
    den += w;

    for (int in = 0; in < num_numdens; ++in) {
      numdens& nd = nds[in];
      if (count_llp != 2) //FIXME
        continue;
      nd.den(k_dvv_2vtx, dvv_2vtx);
      nd.den(k_movedist3_movedist2_2vtx, movedist3d0, movedist2d0);
      nd.den(k_movedist3_movedist2_2vtx, movedist3d1, movedist2d1);
    }

    double sumdbv = -9.9;
    int n_pass_nocuts_2vtx = 0;
    int n_pass_ntracks_2vtx = 0;
    int n_pass_all_2vtx = 0;
    double  dist2move_0 = -9.9;
    double  dist2move_1 = -9.9;
    double vtx0_bs2derr = -9.9, vtx0_dbv = -999.9, vtx0_ntk = -9; // JMTBAD ??? these end up with what???
    double vtx1_bs2derr = -9.9, vtx1_dbv = -999.9, vtx1_ntk = -9; // JMTBAD ??? these end up with what???
    jmt::MinValue dist2min_0(100);
    jmt::MinValue dist2min_1(100);
    for (size_t i = 0; i < nvtx; ++i) {
      dist2move_0 = (gen.decay(0, bs) - vs.pos(i)).Mag();
      dist2min_0(i, dist2move_0);
      if (dist2move_0 > 0.0400) //FIXME
        continue;
      for (size_t j = 0; j < nvtx; ++j) {
        dist2move_1 = (gen.decay(1, bs) - vs.pos(j)).Mag();
        dist2min_1(j, dist2move_1);
        if (dist2move_1 > 0.0400 || i==j) //FIXME
          continue;

        vtx0_bs2derr = vs.bs2derr(i); // JMTBAD ???
        vtx0_dbv = vs.pos(i).Perp();
        vtx0_ntk = vs.ntracks(i);

        vtx1_bs2derr = vs.bs2derr(j); // JMTBAD ???
        vtx1_dbv = vs.pos(j).Perp();
        vtx1_ntk = vs.ntracks(j);

        sumdbv = vtx0_dbv + vtx1_dbv;
        const bool pass_beams = vtx0_dbv >= 0.0100 && vtx0_dbv < 2.0 && vtx1_dbv >= 0.0100 && vtx1_dbv < 2.0;
        const bool pass_ntracks = vtx0_ntk >= 4 && vtx1_ntk >= 4 && pass_beams;
        const bool pass_bs2derr = vtx0_bs2derr < 0.0050 && vtx1_bs2derr < 0.0050 && pass_beams; // JMTBAD rescale_bs2derr // FIXME
        

        if (1) {++n_pass_nocuts_2vtx;}
        if (pass_ntracks) {++n_pass_ntracks_2vtx;}
        if (pass_ntracks && pass_bs2derr) {++n_pass_all_2vtx;}


      }
    }

    if (n_pass_nocuts_2vtx)  nums_2vtx["nocuts"] += w;
    if (n_pass_ntracks_2vtx) nums_2vtx["ntracks"] += w;
    if (n_pass_all_2vtx)     nums_2vtx["all"] += w;

    const int npasses_2vtx[num_numdens] = {
      n_pass_nocuts_2vtx,
      n_pass_ntracks_2vtx,
      n_pass_all_2vtx
    };

    for (int in = 0; in < num_numdens; ++in) {
      if (count_llp != 2) //FIXME
        continue;
      if (!npasses_2vtx[in])
        continue;
      if (sumdbv < 0.05)
        continue;
      numdens& nd = nds[in];
      nd.num(k_dvv_2vtx, dvv_2vtx);
      nd.num(k_movedist3_movedist2_2vtx, movedist3d0, movedist2d0);
      nd.num(k_movedist3_movedist2_2vtx, movedist3d1, movedist2d1);
    }

    NR_loop_cont(w);
  };

  nr.loop(fcn);

  printf("%12.1f", den);
  for (const std::string& c : {"nocuts", "ntracks", "all"}) {
    const jmt::interval i = jmt::clopper_pearson_binom(nums[c], den);
    printf("    %6.4f +- %6.4f", i.value, i.error());
  }
  printf("\n");
}
