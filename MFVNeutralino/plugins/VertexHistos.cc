#include "TH2.h"
#include "TH3.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/PairwiseHistos.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/Year.h"
// #include "DataFormats/HepMCCandidate/interface/GenParticle.h"


class MFVVertexHistos : public edm::EDAnalyzer {
 public:
  explicit MFVVertexHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<double> weight_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  // const edm::EDGetTokenT<reco::GenParticleCollection> gen_particles_token; //GEN COMMENTED OUT
  bool satisfiesLepTriggerPT(edm::Handle<MFVEvent>, edm::Handle<MFVVertexAuxCollection>, int, int, size_t, const edm::EventSetup&);

  bool jet_hlt_match(edm::Handle<MFVEvent> mevent, int i, float min_jet_pt=20.) const {
    // an offline jet with a successful HLT match will have a nonzero jet_hlt_pt;
    // all others have the default value of 0
    return mevent->jet_hlt_pt.at(i) > min_jet_pt;
  }

  const int max_ntrackplots;
  const bool do_scatterplots;

  enum sv_index { sv_all, sv_num_indices };
  static const char* sv_index_names[sv_num_indices];

  void fill(TH1F** hs,          const int, const double val,                    const double weight) const { hs[sv_all]->Fill(val, weight); }
  void fill(TH2F** hs,          const int, const double val, const double val2, const double weight) const { hs[sv_all]->Fill(val, val2, weight); }
  void fill(PairwiseHistos* hs, const int, const PairwiseHistos::ValueMap& val, const double weight) const { hs[sv_all].Fill(val, -1, weight); }

  PairwiseHistos h_sv[sv_num_indices];

  TH1F* h_sv_jets_deltaphi[4][sv_num_indices];

  TH2F* h_sv_bs2derr_bsbs2ddist[sv_num_indices];
  TH2F* h_pvrho_bsbs2ddist[sv_num_indices];
  TH2F* h_sv_elept_eleID[sv_num_indices];
  TH2F* h_sv_mupt_muID[sv_num_indices];
  TH2F* h_sv_elept_eleiso[sv_num_indices];
  TH2F* h_sv_mupt_muiso[sv_num_indices];
  TH1F* h_w;
  TH1F* h_nsv;
  TH1F* h_nsv_cc;

  TH1F* h_nsv_wlep;  // assoc. lep in sv
  TH1F* h_nsv_wlep_4tk; 
  TH1F* h_nsv_wlep_Min5tk;
  /////////////////////////////////////////////////////////////////////////////////////

//GEN COMMENTED OUT 
//  TH1F* h_ngenmatched_sv_[4];
//   TH1F* h_sv_gensv_mag_[4]; //2d distance of sv to gensv

//   //gen leptons; 
//   TH1F* h_ngendau_[4]; // gen leptons --> can infer what the genvertices will be 
//   TH1F* h_ngenmatched_[2]; //only concerned with genmatching ele and mu 
//   TH1F* h_closestdR_gen_[2];
//   TH1F* h_lepdau_novtx_[2]; //no vertex matched; is the reco ele/mu gen-matched? 
//   TH1F* h_lepdau_wvtx_[2];   //vertex matched; is the reco ele/mu gen-matched? 
//   TH1F* h_lepdau_invtx_[2];   // gen daughter is one of the tracks in the vertex (matching via lepton association) 
//   //below is filled ONLY if lepton and SV have been genmatched 
//   //these are the matched leptons in the vertex; 
//   TH1F* h_lepdau_inSV_pt_[2];
//   TH1F* h_lepdau_inSV_dxy_[2];
//   TH1F* h_lepdau_inSV_dxyerr_[2];
//   TH1F* h_lepdau_inSV_nsigmadxy_[2];
//   TH1F* h_lepdau_inSV_missdist_[2];
//   TH1F* h_lepdau_inSV_missdisterr_[2];
//   TH1F* h_lepdau_inSV_missdistsig_[2];
//   TH1F* h_lepdau_inSV_iso_[2];
//   //then similarly for those matched leptons but not in vertex; 
//   // TODO : calculate the missdist to the closest SV 
//   TH1F* h_lepdau_outSV_pt_[2];
//   TH1F* h_lepdau_outSV_dxy_[2];
//   TH1F* h_lepdau_outSV_dxyerr_[2];
//   TH1F* h_lepdau_outSV_nsigmadxy_[2];
//   TH1F* h_lepdau_outSV_missdist_[2];
//   TH1F* h_lepdau_outSV_missdisterr_[2];
//   TH1F* h_lepdau_outSV_missdistsig_[2];
//   TH1F* h_lepdau_outSV_iso_[2];

  /////////////////////////////////////////////////////////////////////////////////////
  //GEN COMMENTED OUT 
  // TH1F* h_sv_gen2ddist_signed; 
  // TH2F* h_sv_ntk_genbs2ddist;
  TH2F* h_sv_ntk_bs2ddist;
  // TH2F* h_sv_ntk_gen2ddist;
  TH2F* h_sv_ntk_njet;

  TH1F* h_sv_ntkfromjets;
  TH3F* h_sv_nallbtags;
  TH3F* h_sv_nallbtks;
  TH1F* h_sv_nbtags[3];
  TH1F* h_sv_nbtks[3];
  TH1F* h_sv_nlep_nbtks[3]; //combining to look at tracks from : lepton & bjets -> I think this is double counting

  TH1F* h_svmu_nbtags[3];
  TH1F* h_svmu_nbtks[3];
  TH1F* h_svmu_nbtks_notlep[3]; //tracks from bjets and not from leptons 
  TH1F* h_svele_nbtags[3];
  TH1F* h_svele_nbtks[3];
  TH1F* h_svele_nbtks_notlep[3]; //tracks from bjets and not from leptons 

  TH1F* h_svwele_tightsel_passtriggers; //which triggers fire in events w/ SVwele and the ele passes tightsel
  TH1F* h_svwmu_tightsel_passtriggers; //which triggers fire in events w/ SVwmu and the mu passes tightsel


  // TH1F* h_sv_nleptks_nbtks[3]; // combining : tracks from bjets (not from lep) and tracks from leptons (not from bjets) 
  // TH1F* h_sv_nlepbtks[3]; //combining : tracks from bjets (not from lep) and tracks from leptons coming from the bjet 

  // TH1F* h_sv_neletks_nbtks[3]; // combining : tracks from bjets (not from lep) and tracks from leptons (not from bjets) 
  // TH1F* h_sv_nelebtks[3]; //combining : tracks from bjets (not from lep) and tracks from leptons coming from the bjet 
  // TH1F* h_sv_nmutks_nbtks[3]; // combining : tracks from bjets (not from lep) and tracks from leptons (not from bjets) 
  // TH1F* h_sv_nmubtks[3]; //combining : tracks from bjets (not from lep) and tracks from leptons coming from the bjet 

  TH1F* h_sv_nbtks_notlep[3]; //tracks from bjets and not from leptons 
  // TH1F* h_sv_nlep_fromb[3]; //tracks coming from leptons from bjets
  // TH1F* h_sv_nele_fromb[3]; //tracks coming from ele from bjets
  // TH1F* h_sv_nmu_fromb[3]; //tracks coming from mu from bjets 

  // //now concerning counting/pt leptons from/not from b 
  // TH1F* h_sv_nlep_notb[3];
  // TH1F* h_sv_nele_notb[3];
  // TH1F* h_sv_nmu_notb[3];

  //above should have sv contain a b though so make case when do not have b 
  // TH1F* h_sv_nlep_notbnob[3];
  // TH1F* h_sv_nele_notbnob[3];
  // TH1F* h_sv_nmu_notbnob[3];

  TH1F* h_sv_mindeltaphi_svbjet[3];
  TH1F* h_sv_mindeltar_sv_bjet[3];
  TH1F* h_sv_mindeltaphi_lepbjet[3];
  TH1F* h_sv_mindeltar_lep_bjet[3];
  TH1F* h_sv_mindr_ptratio_lep_bjet[3];

  TH1F* h_sv_maxdeltaphi_lepbjet[3];
  TH1F* h_sv_maxdeltar_lep_bjet[3];
  TH1F* h_sv_maxdr_ptratio_lep_bjet[3];


  TH2F* h_sv_ntk0_ntk1;
  TH2F* h_sv_nsv_nmatchjet;
  TH2F* h_sv_xy;
  TH2F* h_sv_xy_alt;
  TH2F* h_sv_yz;
  TH2F* h_sv_xz;
  TH2F* h_sv_rz;
  TH1F* h_svdist2d;
  TH1F* h_svdist3d;
  TH1F* h_sumdbv;
  TH2F* h_sumdbv_trigcomb;
  TH2F* h_caloht_trigcomb;
  TH3F* h_dbv0dbv1_trgbit;
  TH2F* h_sv0pvdz_v_sv1pvdz;
  TH2F* h_sv0pvdzsig_v_sv1pvdzsig;
  TH1F* h_absdeltaphi01;
  TH2F* h_pvmosttracksshared;
  TH1F* h_fractrackssharedwpv01;
  TH1F* h_fractrackssharedwpvs01;
  TH1F* h_sv_shared_jets;
  TH1F* h_svdist2d_shared_jets;
  TH1F* h_svdist2d_no_shared_jets;
  TH1F* h_absdeltaphi01_shared_jets;
  TH1F* h_absdeltaphi01_no_shared_jets;

  TH1F* h_sv0_first_large_nsigmadxy_bsp;
  TH1F* h_sv0_second_large_nsigmadxy_bsp;
  TH1F* h_sv0_third_large_nsigmadxy_bsp;
  TH1F* h_sv0_first_large_dxy_bsp;
  TH1F* h_sv0_second_large_dxy_bsp;
  TH1F* h_sv0_third_large_dxy_bsp;
  TH1F* h_sv0_med_nsigmadxy_bsp;
  TH1F* h_sv0_med_dxy_bsp;
  TH1F* h_sv1_first_large_nsigmadxy_bsp;
  TH1F* h_sv1_second_large_nsigmadxy_bsp;
  TH1F* h_sv1_third_large_nsigmadxy_bsp;
  TH1F* h_sv1_first_large_dxy_bsp;
  TH1F* h_sv1_second_large_dxy_bsp;
  TH1F* h_sv1_third_large_dxy_bsp;
  TH1F* h_sv1_med_nsigmadxy_bsp;
  TH1F* h_sv1_med_dxy_bsp;

  TH1F* h_sv_test_costh[sv_num_indices];
  TH1F* h_sv_tracks_sumpt[sv_num_indices];
  TH1F* h_sv_track_weight[sv_num_indices];
  TH1F* h_sv_track_q[sv_num_indices];
  TH1F* h_sv_track_pt[sv_num_indices];
  TH1F* h_sv_track_eta[sv_num_indices];
  TH1F* h_sv_track_phi[sv_num_indices];
  TH1F* h_sv_track_dxy[sv_num_indices];
  TH1F* h_sv_track_dz[sv_num_indices];
  TH1F* h_sv_track_pt_err[sv_num_indices];
  TH1F* h_sv_track_eta_err[sv_num_indices];
  TH1F* h_sv_track_phi_err[sv_num_indices];
  TH1F* h_sv_track_dxy_err[sv_num_indices];
  TH1F* h_sv_track_dz_err[sv_num_indices];
  TH1F* h_sv_track_nsigmadxy[sv_num_indices];
  TH1F* h_sv_track_chi2dof[sv_num_indices];
  TH1F* h_sv_track_npxhits[sv_num_indices];
  TH1F* h_sv_track_nsthits[sv_num_indices];
  TH1F* h_sv_track_nhitsbehind[sv_num_indices];
  TH1F* h_sv_track_nhitslost[sv_num_indices];
  TH1F* h_sv_track_nhits[sv_num_indices];
  TH1F* h_sv_track_injet[sv_num_indices];
  TH1F* h_sv_track_inpv[sv_num_indices];

  TH1F* h_sv_sellep;
  TH1F* h_sv_selmu;
  TH1F* h_sv_selele;

  //comparing the track associated to pf candidate and the pf candidate
  TH2F* h_leading_mutrackpT_vs_mupT_inSV; //muon passes ID, iso 
  TH2F* h_leading_eletrackpT_vs_elepT_inSV; //ele passes ID, iso
  TH2F* h_leading_mutracknsigmadxy_vs_munsigmadxy_inSV; //muon passes ID, iso 
  TH2F* h_leading_eletracknsigmadxy_vs_elensigmadxy_inSV; //ele passes ID, iso

  // all_lep nocuts, hltmatch jetlepveto
  TH1F* h_svwlep_nsv_min4tk_[2];
  TH1F* h_svwlep_nsv_4tk_[2];
  TH1F* h_svwlep_nsv_min5tk_[2];

  TH1F* h_svwlep_rescale_bs2derr_[2];
  TH1F* h_svwlep_rescale_pertkbs2derr_[2];
  TH1F* h_svwlep_bsbs2ddist_[2];
  TH1F* h_svwlep_ntracks_[2];
  TH1F* h_svwlep_trackpairdravg_[2];
  TH1F* h_svwlep_costh_[2];
  TH1F* h_svwlep_tracktripmassmax_[2];
  TH1F* h_svwlep_leadinglepptinSV_[2];
  TH1F* h_svwlep_leadinglepdxyinSV_[2];
  TH1F* h_svwlep_leadinglepdxyerrinSV_[2];
  TH1F* h_svwlep_leadingleprescaleddxyerrinSV_[2];
  TH1F* h_svwlep_leadinglepnsigmadxyinSV_[2];
  TH1F* h_svwlep_leadingleprescalednsigmadxyinSV_[2];
  TH1F* h_svwlep_leadinglepIDinSV_[2];
  TH1F* h_svwlep_leadinglepisoinSV_[2];
  TH1F* h_svwlep_leadinglepetainSV_[2];
  // TH1F* h_svwlep_avgptmlep_[2];
  TH1F* h_svwlep_avgptnoleptkpt_[2];
  TH1F* h_svwlep_trackpairdravgmmax_[2];
  TH1F* h_svwlep_trackptgt3_[2];
  TH1F* h_svwlep_trackptgt10_[2];
  TH1F* h_svwlepjet_pairdr_[2];
  TH1F* h_svwlep_jet_pairdr_[2];
  TH1F* h_svwlepjet_pt_[2];
  TH1F* h_svwlepjet_ptratio_[2];
  TH2F* h_svwlep_leadinglepeta_vs_phi_inSV_[2];

  // svwele (same as above) leading lep is ele 
  TH1F* h_svwele_nsv_min4tk_[2];
  TH1F* h_svwele_nsv_4tk_[2];
  TH1F* h_svwele_nsv_min5tk_[2];
  TH1F* h_svwele_rescale_bs2derr_[2];
  TH1F* h_svwele_rescale_pertkbs2derr_[2];
  TH1F* h_svwele_bsbs2ddist_[2];
  TH1F* h_svwele_ntracks_[2];
  TH1F* h_svwele_trackpairdravg_[2];
  TH1F* h_svwele_costh_[2];
  TH1F* h_svwele_tracktripmassmax_[2];
  TH1F* h_svwele_leadinglepptinSV_[2];
  TH1F* h_svwele_leadinglepdxyinSV_[2];
  TH1F* h_svwele_leadinglepdxyerrinSV_[2];
  TH1F* h_svwele_leadingleprescaleddxyerrinSV_[2];
  TH1F* h_svwele_leadinglepnsigmadxyinSV_[2];
  TH1F* h_svwele_leadingleprescalednsigmadxyinSV_[2];
  TH1F* h_svwele_leadinglepIDinSV_[2];
  TH1F* h_svwele_leadinglepisoinSV_[2];
  TH1F* h_svwele_leadinglepetainSV_[2];
  TH1F* h_svwele_avgptnoleptkpt_[2];
  TH1F* h_svwele_trackpairdravgmmax_[2];
  TH1F* h_svwele_trackptgt3_[2];
  TH1F* h_svwele_trackptgt10_[2];
  TH1F* h_svwelejet_pairdr_[2];
  TH1F* h_svwele_jet_pairdr_[2];
  TH1F* h_svwelejet_pt_[2];
  TH1F* h_svwelejet_ptratio_[2];
  TH1F* h_svwele_leadinglephltdRinSV_[2];
  TH2F* h_svwele_leadinglepeta_vs_phi_inSV_[2];
  TH1F* h_svwelewHEM_leadinglepetainSV_[2];
  TH1F* h_svwelewHEM_leadinglepphiinSV_[2];
  TH2F* h_svwelewHEM_leadinglepeta_vs_phi_inSV_[2];

  //svwmu - leading lep is mu
  TH1F* h_svwmu_nsv_min4tk_[2];
  TH1F* h_svwmu_nsv_4tk_[2];
  TH1F* h_svwmu_nsv_min5tk_[2];
  TH1F* h_svwmu_rescale_bs2derr_[2];
  TH1F* h_svwmu_rescale_pertkbs2derr_[2];
  TH1F* h_svwmu_bsbs2ddist_[2];
  TH1F* h_svwmu_ntracks_[2];
  TH1F* h_svwmu_trackpairdravg_[2];
  TH1F* h_svwmu_costh_[2];
  TH1F* h_svwmu_tracktripmassmax_[2];
  TH1F* h_svwmu_leadinglepptinSV_[2];
  TH1F* h_svwmu_leadinglepdxyinSV_[2];
  TH1F* h_svwmu_leadinglepdxyerrinSV_[2];
  TH1F* h_svwmu_leadingleprescaleddxyerrinSV_[2];
  TH1F* h_svwmu_leadinglepnsigmadxyinSV_[2];
  TH1F* h_svwmu_leadingleprescalednsigmadxyinSV_[2];
  TH1F* h_svwmu_leadinglepIDinSV_[2];
  TH1F* h_svwmu_leadinglepisoinSV_[2];
  TH1F* h_svwmu_leadinglepetainSV_[2];
  TH1F* h_svwmu_avgptnoleptkpt_[2];
  TH1F* h_svwmu_trackpairdravgmmax_[2];
  TH1F* h_svwmu_trackptgt3_[2];
  TH1F* h_svwmu_trackptgt10_[2];
  TH1F* h_svwmujet_pairdr_[2];
  TH1F* h_svwmu_jet_pairdr_[2];
  TH1F* h_svwmujet_pt_[2];
  TH1F* h_svwmujet_ptratio_[2];
  TH1F* h_svwmu_leadinglephltdRinSV_[2];
  TH2F* h_svwmu_leadinglepeta_vs_phi_inSV_[2];

  // the nm1 plots                                                                                                                                                                     
  //w hltmatching; w/ jetlepveto                                                                                                                                                       
  TH1F* h_svwlep_leadinglepIDinSV_nm1;
  TH1F* h_svwlep_leadinglepetainSV_nm1;
  TH1F* h_svwlep_leadinglepptinSV_nm1;
  TH1F* h_svwlep_leadinglepisoinSV_nm1;
  TH1F* h_svwlep_leadinglepishltmatchedinSV_nm1;

  TH1F* h_svwmu_leadinglepIDinSV_nm1;
  TH1F* h_svwmu_leadinglepetainSV_nm1;
  TH1F* h_svwmu_leadinglepptinSV_nm1;
  TH1F* h_svwmu_leadinglepisoinSV_nm1;
  TH1F* h_svwmu_leadinglepishltmatchedinSV_nm1;

  TH1F* h_svwele_leadinglepIDinSV_nm1;
  TH1F* h_svwele_leadinglepetainSV_nm1;
  TH1F* h_svwele_leadinglepptinSV_nm1;
  TH1F* h_svwele_leadinglepisoinSV_nm1;
  TH1F* h_svwele_leadinglepishltmatchedinSV_nm1;

  //nm1 but no hlt matching; w/ jetlepveto                                                                                                                                             
  TH1F* h_svwlep_leadinglepIDinSV_nm1h;
  TH1F* h_svwlep_leadinglepetainSV_nm1h;
  TH1F* h_svwlep_leadinglepptinSV_nm1h;
  TH1F* h_svwlep_leadinglepisoinSV_nm1h;

  TH1F* h_svwmu_leadinglepIDinSV_nm1h;
  TH1F* h_svwmu_leadinglepetainSV_nm1h;
  TH1F* h_svwmu_leadinglepptinSV_nm1h;
  TH1F* h_svwmu_leadinglepisoinSV_nm1h;

  TH1F* h_svwele_leadinglepIDinSV_nm1h;
  TH1F* h_svwele_leadinglepetainSV_nm1h;
  TH1F* h_svwele_leadinglepptinSV_nm1h;
  TH1F* h_svwele_leadinglepisoinSV_nm1h;

  TH1F* h_svwlep_minjetlepdr;
  TH1F* h_svwmu_minjetlepdr;
  TH1F* h_svwele_minjetlepdr;

};

const char* MFVVertexHistos::sv_index_names[MFVVertexHistos::sv_num_indices] = { "all" };

MFVVertexHistos::MFVVertexHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    // gen_particles_token(consumes<reco::GenParticleCollection>(cfg.getParameter<edm::InputTag>("gen_particles_src"))), //GEN COMMENTED OUT
    max_ntrackplots(cfg.getParameter<int>("max_ntrackplots")),
    do_scatterplots(cfg.getParameter<bool>("do_scatterplots"))
{
  edm::Service<TFileService> fs;

  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices;arb. units", 15, 0, 15);
  h_nsv_cc = fs->make<TH1F>("h_nsv_cc", ";# of secondary vertices;arb. units", 15, 0, 15);

  h_nsv_wlep = fs->make<TH1F>("h_nsv_wlep", ";# of secondary vertices with at least 1 assoc. lep;arb. units", 10, 0, 10);

  h_sv_sellep = fs->make<TH1F>("h_sv_sellep", ";# of leptons passing ID and iso associated to a SV;arb. units", 10, 0, 10);
  h_sv_selmu = fs->make<TH1F>("h_sv_selmu", ";# of muons passing ID and iso associated to a SV;arb. units", 10, 0, 10);
  h_sv_selele = fs->make<TH1F>("h_sv_selele", ";# of electrons passing ID and iso associated to a SV;arb. units", 10, 0, 10);
  // h_sv_electron_nm1iso = fs->make<TH1F>("h_sv_electron_nm1iso", "; associated electron iso; arb. units", 60, 0, 2.0);
  // h_sv_muon_nm1iso = fs->make<TH1F>("h_sv_muon_nm1iso", "; associated muon iso; arb. units", 60, 0, 2.0);

  h_svwele_tightsel_passtriggers = fs->make<TH1F>("h_svwele_tightsel_passtriggers", ";triggers that fire w/ SVwele events; arb. units", 10, 0, 10);
  h_svwmu_tightsel_passtriggers = fs->make<TH1F>("h_svwmu_tightsel_passtriggers", ";triggers that fire w/ SVwmu events; arb. units", 10, 0, 10);

  h_leading_mutrackpT_vs_mupT_inSV = fs->make<TH2F>("h_leading_mutrackpT_vs_mupT_inSV", ";pt of leading matched mu tk (GeV); pt of leading sel mu in SV (GeV))", 200, 0, 400, 200, 0, 400);
  h_leading_eletrackpT_vs_elepT_inSV = fs->make<TH2F>("h_leading_eletrackpT_vs_elepT_inSV", ";pt of leading matched ele tk (GeV); pt of matched sel ele in SV (GeV))", 200, 0, 400, 200, 0, 400);
  h_leading_mutracknsigmadxy_vs_munsigmadxy_inSV = fs->make<TH2F>("h_leading_mutracknsigmadxy_vs_munsigmadxy_inSV", ";nsigmadxy of leading matched mu tk; nsigmadxy of leading sel mu in SV)", 100, 0, 100, 100, 0, 100);
  h_leading_eletracknsigmadxy_vs_elensigmadxy_inSV = fs->make<TH2F>("h_leading_eletracknsigmadxy_vs_elensigmadxy_inSV", ";nsigmadxy of leading matched ele tk; nsigmadxy of matched sel ele in SV)", 100, 0, 100, 100, 0, 100);

  // h_gensv_winbp = fs->make<TH1F>("h_gensv_winbp", ";# of gen sv within beampipe;arb. units", 2, 0, 2);

  //lep flavor is based on the genSV; all indicates no distinction between flavor (ele, mu, tau)
  //GEN COMMENTED OUT
  // const char* lep_flav[4] = {"all", "ele", "mu", "tau"};
  // for (int i = 0; i < 4; ++i) {
  //   h_ngenmatched_sv_[i] = fs->make<TH1F>(TString::Format("h_ngenmatched_sv_%s", lep_flav[i]), TString::Format("; n of SV < 0.02 away from %s-flavor genvtx;arb. units", lep_flav[i]), 3, 0, 3);
  //   h_sv_gensv_mag_[i] = fs->make<TH1F>(TString::Format("h_sv_%s_gensv_mag", lep_flav[i]), TString::Format("; Mag(%s-flavor genvtx, closest recovtx);arb. units", lep_flav[i]), 200, 0, 0.2);
  //   if (i != 0) {
  //     h_ngendau_[i] = fs->make<TH1F>(TString::Format("h_ngendau_%s", lep_flav[i]), TString::Format("; n of gendau %s;arb. units", lep_flav[i]), 3, 0, 3);
  //   }
  // }
  
  const char* iso_eta[2] = {"nocuts", "hltmatch_fullsel_jetlepveto"};

  for (int i=0; i <2; ++i) {
    h_svwlep_nsv_min4tk_[i] = fs->make<TH1F>(TString::Format("h_svwlep_nsv_min4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwlep_nsv_4tk_[i] = fs->make<TH1F>(TString::Format("h_svwlep_nsv_4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwlep_nsv_min5tk_[i] = fs->make<TH1F>(TString::Format("h_svwlep_nsv_min5tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);

    h_svwlep_rescale_bs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwlep_rescale_bs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.05);
    h_svwlep_rescale_pertkbs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwlep_rescale_pertkbs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) * sqrt(ntracks) (cm)", 100, 0, 0.05);
    h_svwlep_bsbs2ddist_[i] = fs->make<TH1F>(TString::Format("h_svwlep_bsbs2ddist_%s", iso_eta[i]),  "; d_{BV} (cm)", 100, 0, 0.1);
    h_svwlep_ntracks_[i] = fs->make<TH1F>(TString::Format("h_svwlep_ntracks_%s", iso_eta[i]),  ";# of tracks/SV", 40, 0, 40);
    h_svwlep_trackpairdravg_[i] = fs->make<TH1F>(TString::Format("h_svwlep_trackpairdravg_%s", iso_eta[i]),  "SV avg{#Delta R(i,j)}", 50, 0, 5);
    h_svwlep_costh_[i] = fs->make<TH1F>(TString::Format("h_svwlep_costh_%s", iso_eta[i]),  "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))", 50, -1, 1);
    h_svwlep_tracktripmassmax_[i]=fs->make<TH1F>(TString::Format("h_svwlep_tracktripmassmax_%s", iso_eta[i]),  "max #Sigma M (GeV) of three tracks in SV", 40, 0, 200);
    h_svwlep_leadinglepptinSV_[i]=fs->make<TH1F>(TString::Format("h_svwlep_leadinglepptinSV_%s", iso_eta[i]),  "leading lepton pT associated to sv", 80, 0, 400);
    h_svwlep_leadinglepdxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepdxyinSV_%s", iso_eta[i]), "; leading lepton dxy assoicated to sv; arb. units", 50, 0, 0.25);
    h_svwlep_leadinglepdxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepdxyerrinSV_%s", iso_eta[i]), "; leading lepton dxyerr assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwlep_leadingleprescaleddxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadingleprescaleddxyerrinSV_%s", iso_eta[i]), "; leading lepton dxyerr (rescaled) assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwlep_leadinglepnsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepnsigmadxyinSV_%s", iso_eta[i]), "; leading lepton nsigmadxy assoicated to sv; arb. units", 50, 0, 50);
    h_svwlep_leadingleprescalednsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadingleprescalednsigmadxyinSV_%s", iso_eta[i]), "; leading lepton nsigmadxy (rescaled) assoicated to sv; arb. units", 50, 0, 50);   
    h_svwlep_leadinglepetainSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepetainSV_%s", iso_eta[i]), "; leading lepton eta assoicated to sv; arb. units", 50, -3.4, 3.4);
    h_svwlep_leadinglepIDinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepIDinSV_%s", iso_eta[i]), "; leading lepton ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?
    h_svwlep_leadinglepisoinSV_[i] = fs->make<TH1F>(TString::Format("h_svwlep_leadinglepisoinSV_%s", iso_eta[i]), "; leading lepton iso assoicated to sv; arb. units", 60, 0, 0.15);
    h_svwlep_trackpairdravgmmax_[i] = fs->make<TH1F>(TString::Format("h_svwlep_trackpairdravgmmax_%s", iso_eta[i]),  "SV avg{#Delta R(i,j) - max #Delta R}", 50, 0, 5);
    h_svwlep_avgptnoleptkpt_[i] = fs->make<TH1F>(TString::Format("h_svwlep_avgptnoleptkpt_%s", iso_eta[i]),  "avg track pT (w/out leptk pT)", 100, 0, 100);
    h_svwlep_trackptgt3_[i] = fs->make<TH1F>(TString::Format("h_svwlep_trackptgt3_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 3 GeV; arb. units", 10, 0, 10);
    h_svwlep_trackptgt10_[i] = fs->make<TH1F>(TString::Format("h_svwlep_trackptgt10_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 10 GeV; arb. units", 10, 0, 10);
    h_svwlepjet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwlepjet_pairdr_%s", iso_eta[i]), "; deltaR between jet and lepton track within a SV; arb. units", 100, 0, 6.3); 
    h_svwlep_jet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwlep_jet_pairdr_%s", iso_eta[i]), "; deltaR between assoc lepton in SV and jet; arb. units", 100, 0, 6.3); //jet not in the SV 
    h_svwlepjet_pt_[i] = fs->make<TH1F>(TString::Format("h_svwlepjet_pt_%s", iso_eta[i]), "; leading jet pT associated to sv; arb. units", 80, 0, 400);
    h_svwlepjet_ptratio_[i] = fs->make<TH1F>(TString::Format("h_svwlepjet_ptratio_%s", iso_eta[i]), "; leading lepton pT / leading jet pT associated to SV; arb. units", 40, 0, 20);
    h_svwlep_leadinglepeta_vs_phi_inSV_[i] = fs->make<TH2F>(TString::Format("h_svwlep_leadinglepeta_vs_phi_inSV_%s", iso_eta[i]), "; leading lepton eta associated to sv; leading lepton phi associated to sv", 50, -4, 4, 50, -4, 4);

    // same but for leading lepton is mu
    h_svwmu_nsv_min4tk_[i] = fs->make<TH1F>(TString::Format("h_svwmu_nsv_min4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwmu_nsv_4tk_[i] = fs->make<TH1F>(TString::Format("h_svwmu_nsv_4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwmu_nsv_min5tk_[i] = fs->make<TH1F>(TString::Format("h_svwmu_nsv_min5tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwmu_rescale_bs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwmu_rescale_bs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.05);
    h_svwmu_rescale_pertkbs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwmu_rescale_pertkbs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) * sqrt(ntracks) (cm)", 100, 0, 0.05);
    h_svwmu_bsbs2ddist_[i] = fs->make<TH1F>(TString::Format("h_svwmu_bsbs2ddist_%s", iso_eta[i]),  "; d_{BV} (cm)", 100, 0, 0.1);
    h_svwmu_ntracks_[i] = fs->make<TH1F>(TString::Format("h_svwmu_ntracks_%s", iso_eta[i]),  ";# of tracks/SV", 40, 0, 40);
    h_svwmu_trackpairdravg_[i] = fs->make<TH1F>(TString::Format("h_svwmu_trackpairdravg_%s", iso_eta[i]),  "SV avg{#Delta R(i,j)}", 50, 0, 5);
    h_svwmu_costh_[i] = fs->make<TH1F>(TString::Format("h_svwmu_costh_%s", iso_eta[i]),  "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))", 50, -1, 1);
    h_svwmu_tracktripmassmax_[i]=fs->make<TH1F>(TString::Format("h_svwmu_tracktripmassmax_%s", iso_eta[i]),  "max #Sigma M (GeV) of three tracks in SV", 40, 0, 200);
    h_svwmu_leadinglepptinSV_[i]=fs->make<TH1F>(TString::Format("h_svwmu_leadinglepptinSV_%s", iso_eta[i]),  "leading muon pT associated to sv", 80, 0, 400);
    h_svwmu_leadinglepdxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepdxyinSV_%s", iso_eta[i]), "; leading muon dxy assoicated to sv; arb. units", 50, 0, 0.25);
    h_svwmu_leadinglepdxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepdxyerrinSV_%s", iso_eta[i]), "; leading muon dxyerr assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwmu_leadingleprescaleddxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadingleprescaleddxyerrinSV_%s", iso_eta[i]), "; leading muon dxyerr (rescaled) assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwmu_leadinglepnsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepnsigmadxyinSV_%s", iso_eta[i]), "; leading muon nsigmadxy assoicated to sv; arb. units", 50, 0, 50);
    h_svwmu_leadingleprescalednsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadingleprescalednsigmadxyinSV_%s", iso_eta[i]), "; leading muon nsigmadxy (rescaled) assoicated to sv; arb. units", 50, 0, 50);   
    h_svwmu_leadinglepetainSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepetainSV_%s", iso_eta[i]), "; leading muon eta assoicated to sv; arb. units", 50, -3.4, 3.4);
    h_svwmu_leadinglepIDinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepIDinSV_%s", iso_eta[i]), "; leading muon ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?
    h_svwmu_leadinglepisoinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglepisoinSV_%s", iso_eta[i]), "; leading muon iso assoicated to sv; arb. units", 60, 0, 0.15);
    h_svwmu_trackpairdravgmmax_[i] = fs->make<TH1F>(TString::Format("h_svwmu_trackpairdravgmmax_%s", iso_eta[i]),  "SV avg{#Delta R(i,j) - max #Delta R}", 50, 0, 5);
    h_svwmu_avgptnoleptkpt_[i] = fs->make<TH1F>(TString::Format("h_svwmu_avgptnoleptkpt_%s", iso_eta[i]),  "avg track pT (w/out mutk pt)", 100, 0, 100);
    h_svwmu_trackptgt3_[i] = fs->make<TH1F>(TString::Format("h_svwmu_trackptgt3_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 3 GeV; arb. units", 10, 0, 10);
    h_svwmu_trackptgt10_[i] = fs->make<TH1F>(TString::Format("h_svwmu_trackptgt10_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 10 GeV; arb. units", 10, 0, 10);
    h_svwmujet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwmujet_pairdr_%s", iso_eta[i]), "; deltaR between jet and leading electron within a SV; arb. units", 100, 0, 6.3); 
    h_svwmu_jet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwmu_jet_pairdr_%s", iso_eta[i]), "; deltaR between leading electron in SV and jet; arb. units", 100, 0, 6.3); //jet not in the SV 
    h_svwmujet_pt_[i] = fs->make<TH1F>(TString::Format("h_svwmujet_pt_%s", iso_eta[i]), "; leading jet pT associated to sv; arb. units", 80, 0, 400);
    h_svwmujet_ptratio_[i] = fs->make<TH1F>(TString::Format("h_svwmujet_ptratio_%s", iso_eta[i]), "; leading electron pT / leading jet pT associated to SV; arb. units", 40, 0, 20);
    h_svwmu_leadinglephltdRinSV_[i] = fs->make<TH1F>(TString::Format("h_svwmu_leadinglephltdRinSV_%s", iso_eta[i]), "; best dR between hlt lep and leading lep in SV; arb. units", 50, 0, 5);
    h_svwmu_leadinglepeta_vs_phi_inSV_[i] = fs->make<TH2F>(TString::Format("h_svwmu_leadinglepeta_vs_phi_inSV_%s", iso_eta[i]), "; leading muon eta associated to sv; leading muon phi associated to sv", 50, -4, 4, 50, -4, 4);
    // same but for leading lepton is ele
    h_svwele_nsv_min4tk_[i] = fs->make<TH1F>(TString::Format("h_svwele_nsv_min4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwele_nsv_4tk_[i] = fs->make<TH1F>(TString::Format("h_svwele_nsv_4tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwele_nsv_min5tk_[i] = fs->make<TH1F>(TString::Format("h_svwele_nsv_min5tk_%s", iso_eta[i]),  "; # of secondary vertices; arb. units", 10, 0, 10);
    h_svwele_rescale_bs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwele_rescale_bs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.05);
    h_svwele_rescale_pertkbs2derr_[i] = fs->make<TH1F>(TString::Format("h_svwele_rescale_pertkbs2derr_%s", iso_eta[i]),  "; #sigma(dist2d(SV, beamspot)) * sqrt(ntracks) (cm)", 100, 0, 0.05);
    h_svwele_bsbs2ddist_[i] = fs->make<TH1F>(TString::Format("h_svwele_bsbs2ddist_%s", iso_eta[i]),  "; d_{BV} (cm)", 100, 0, 0.1);
    h_svwele_ntracks_[i] = fs->make<TH1F>(TString::Format("h_svwele_ntracks_%s", iso_eta[i]),  ";# of tracks/SV", 40, 0, 40);
    h_svwele_trackpairdravg_[i] = fs->make<TH1F>(TString::Format("h_svwele_trackpairdravg_%s", iso_eta[i]),  "SV avg{#Delta R(i,j)}", 50, 0, 5);
    h_svwele_costh_[i] = fs->make<TH1F>(TString::Format("h_svwele_costh_%s", iso_eta[i]),  "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))", 50, -1, 1);
    h_svwele_tracktripmassmax_[i]=fs->make<TH1F>(TString::Format("h_svwele_tracktripmassmax_%s", iso_eta[i]),  "max #Sigma M (GeV) of three tracks in SV", 40, 0, 200);
    h_svwele_leadinglepptinSV_[i]=fs->make<TH1F>(TString::Format("h_svwele_leadinglepptinSV_%s", iso_eta[i]),  "leading electron pT associated to sv", 80, 0, 400);
    h_svwele_leadinglepdxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepdxyinSV_%s", iso_eta[i]), "; leading electron dxy assoicated to sv; arb. units", 50, 0, 0.25);
    h_svwele_leadinglepdxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepdxyerrinSV_%s", iso_eta[i]), "; leading electron dxyerr assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwele_leadingleprescaleddxyerrinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadingleprescaleddxyerrinSV_%s", iso_eta[i]), "; leading electron dxyerr (rescaled) assoicated to sv; arb. units", 50, 0, 0.015);
    h_svwele_leadinglepnsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepnsigmadxyinSV_%s", iso_eta[i]), "; leading electron nsigmadxy assoicated to sv; arb. units", 50, 0, 50);
    h_svwele_leadingleprescalednsigmadxyinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadingleprescalednsigmadxyinSV_%s", iso_eta[i]), "; leading electron nsigmadxy (rescaled) assoicated to sv; arb. units", 50, 0, 50);
    h_svwele_leadinglepetainSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepetainSV_%s", iso_eta[i]), "; leading electron eta assoicated to sv; arb. units", 50, -3.4, 3.4);
    h_svwele_leadinglepIDinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepIDinSV_%s", iso_eta[i]), "; leading electron ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?
    h_svwele_leadinglepisoinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglepisoinSV_%s", iso_eta[i]), "; leading electron iso assoicated to sv; arb. units", 60, 0, 0.15);
    h_svwele_trackpairdravgmmax_[i] = fs->make<TH1F>(TString::Format("h_svwele_trackpairdravgmmax_%s", iso_eta[i]),  "SV avg{#Delta R(i,j) - max #Delta R}", 50, 0, 5);
    h_svwele_avgptnoleptkpt_[i] = fs->make<TH1F>(TString::Format("h_svwele_avgptnoleptkpt_%s", iso_eta[i]),  "avg track pT (w/out eletk pt)", 100, 0, 100);
    h_svwele_trackptgt3_[i] = fs->make<TH1F>(TString::Format("h_svwele_trackptgt3_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 3 GeV; arb. units", 10, 0, 10);
    h_svwele_trackptgt10_[i] = fs->make<TH1F>(TString::Format("h_svwele_trackptgt10_%s", iso_eta[i]), ";# of tracks/SV w/ p_{T} > 10 GeV; arb. units", 10, 0, 10);
    h_svwelejet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwelejet_pairdr_%s", iso_eta[i]), "; deltaR between jet and leading electron within a SV; arb. units", 100, 0, 6.3); 
    h_svwele_jet_pairdr_[i] = fs->make<TH1F>(TString::Format("h_svwele_jet_pairdr_%s", iso_eta[i]), "; deltaR between leading electron in SV and jet; arb. units", 100, 0, 6.3); //jet not in the SV 
    h_svwelejet_pt_[i] = fs->make<TH1F>(TString::Format("h_svwelejet_pt_%s", iso_eta[i]), "; leading jet pT associated to sv; arb. units", 80, 0, 400);
    h_svwelejet_ptratio_[i] = fs->make<TH1F>(TString::Format("h_svwelejet_ptratio_%s", iso_eta[i]), "; leading electron pT / leading jet pT associated to SV; arb. units", 40, 0, 20);
    h_svwele_leadinglephltdRinSV_[i] = fs->make<TH1F>(TString::Format("h_svwele_leadinglephltdRinSV_%s", iso_eta[i]), "; best dR between hlt lep and leading lep in SV; arb. units", 50, 0, 5);
    h_svwele_leadinglepeta_vs_phi_inSV_[i] = fs->make<TH2F>(TString::Format("h_svwele_leadinglepeta_vs_phi_inSV_%s", iso_eta[i]), "; leading electron eta associated to sv; leading electron phi associated to sv", 50, -4, 4, 50, -4, 4);
    h_svwelewHEM_leadinglepeta_vs_phi_inSV_[i] = fs->make<TH2F>(TString::Format("h_svwelewHEM_leadinglepeta_vs_phi_inSV_%s", iso_eta[i]), "; leading electron eta associated to sv; leading electron phi associated to sv", 50, -4, 4, 50, -4, 4);
    h_svwelewHEM_leadinglepetainSV_[i] = fs->make<TH1F>(TString::Format("h_svwelewHEM_leadinglepetainSV_%s", iso_eta[i]), "; leading electron eta assoicated to sv; arb. units", 50, -3.4, 3.4);
    h_svwelewHEM_leadinglepphiinSV_[i] = fs->make<TH1F>(TString::Format("h_svwelewHEM_leadinglepphiinSV_%s", iso_eta[i]), "; leading electron phi assoicated to sv; arb. units", 50, -3.4, 3.4);
    // h_sv_mupt_notb[i] = fs->make<TH1F>(TString::Format("h_sv_mupt_%s_inSV_notb", iso_eta[i]), "; muon pT associated to SV NOT from Bjet; arb. units", 80, 0, 400);
    // h_sv_elept_notb[i] = fs->make<TH1F>(TString::Format("h_sv_elept_%s_inSV_notb", iso_eta[i]), "; ele pT associated to SV NOT from Bjet; arb. units", 80, 0, 400);
    // h_sv_leppt_notb[i] = fs->make<TH1F>(TString::Format("h_sv_leppt_%s_inSV_notb", iso_eta[i]), "; lepton pT associated to SV NOT from Bjet; arb. units", 80, 0, 400);

    // h_sv_mupt_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_mupt_%s_inSV_fromb", iso_eta[i]), "; muon pT associated to SV from Bjet; arb. units", 80, 0, 400);
    // h_sv_elept_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_elept_%s_inSV_fromb", iso_eta[i]), "; ele pT associated to SV from Bjet; arb. units", 80, 0, 400);
    // h_sv_leppt_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_leppt_%s_inSV_fromb", iso_eta[i]), "; lepton pT associated to SV from Bjet; arb. units", 80, 0, 400);

  }
  // the nm1 plots; all selections applied to the lepton except for the one being plotted                                                                                              
  h_svwlep_leadinglepIDinSV_nm1 = fs->make<TH1F>("h_svwlep_leadinglepIDinSV_nm1", "; leading lepton ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?       
  h_svwlep_leadinglepetainSV_nm1 = fs->make<TH1F>("h_svwlep_leadinglepetainSV_nm1", "; leading lepton eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwlep_leadinglepptinSV_nm1 =fs->make<TH1F>("h_svwlep_leadinglepptinSV_nm1",  ";leading lepton pT associated to sv; arb. units", 80, 0, 400);
  h_svwlep_leadinglepisoinSV_nm1 = fs->make<TH1F>("h_svwlep_leadinglepisoinSV_nm1", "; leading lepton iso assoicated to sv; arb. units", 60, 0, 0.5);
  h_svwlep_leadinglepishltmatchedinSV_nm1 = fs->make<TH1F>("h_svwlep_leadinglepishltmatchedSV_nm1", "; leading lepton assoicated to sv is hltmatched?; arb. units", 2, 0, 2);

  h_svwmu_leadinglepIDinSV_nm1 = fs->make<TH1F>("h_svwmu_leadinglepIDinSV_nm1", "; leading muon ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?           
  h_svwmu_leadinglepetainSV_nm1 = fs->make<TH1F>("h_svwmu_leadinglepetainSV_nm1", "; leading muon eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwmu_leadinglepptinSV_nm1 =fs->make<TH1F>("h_svwmu_leadinglepptinSV_nm1",  ";leading muon pT associated to sv; arb. units", 80, 0, 400);
  h_svwmu_leadinglepisoinSV_nm1 = fs->make<TH1F>("h_svwmu_leadinglepisoinSV_nm1", "; leading muon iso assoicated to sv; arb. units", 60, 0, 0.5);
  h_svwmu_leadinglepishltmatchedinSV_nm1 = fs->make<TH1F>("h_svwmu_leadinglepishltmatchedSV_nm1", "; leading muon assoicated to sv is hltmatched?; arb. units", 2, 0, 2);

  h_svwele_leadinglepIDinSV_nm1 = fs->make<TH1F>("h_svwele_leadinglepIDinSV_nm1", "; leading electron ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?     
  h_svwele_leadinglepetainSV_nm1 = fs->make<TH1F>("h_svwele_leadinglepetainSV_nm1", "; leading electron eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwele_leadinglepptinSV_nm1 =fs->make<TH1F>("h_svwele_leadinglepptinSV_nm1",  ";leading electron pT associated to sv; arb. units", 80, 0, 400);
  h_svwele_leadinglepisoinSV_nm1 = fs->make<TH1F>("h_svwele_leadinglepisoinSV_nm1", "; leading electron iso assoicated to sv; arb. units", 60, 0, 0.5);
  h_svwele_leadinglepishltmatchedinSV_nm1 = fs->make<TH1F>("h_svwele_leadinglepishltmatchedSV_nm1", "; leading electron assoicated to sv is hltmatched?; arb. units", 2, 0, 2);
  //no hltmatching                                                                                                                                                                     
  h_svwlep_leadinglepIDinSV_nm1h = fs->make<TH1F>("h_svwlep_leadinglepIDinSV_nm1h", "; leading lepton ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?     
  h_svwlep_leadinglepetainSV_nm1h = fs->make<TH1F>("h_svwlep_leadinglepetainSV_nm1h", "; leading lepton eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwlep_leadinglepptinSV_nm1h =fs->make<TH1F>("h_svwlep_leadinglepptinSV_nm1h",  ";leading lepton pT associated to sv", 80, 0, 400);
  h_svwlep_leadinglepisoinSV_nm1h = fs->make<TH1F>("h_svwlep_leadinglepisoinSV_nm1h", "; leading lepton iso assoicated to sv; arb. units", 60, 0, 0.5);

  h_svwmu_leadinglepIDinSV_nm1h = fs->make<TH1F>("h_svwmu_leadinglepIDinSV_nm1h", "; leading muon ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?         
  h_svwmu_leadinglepetainSV_nm1h = fs->make<TH1F>("h_svwmu_leadinglepetainSV_nm1h", "; leading muon eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwmu_leadinglepptinSV_nm1h =fs->make<TH1F>("h_svwmu_leadinglepptinSV_nm1h",  ";leading muon pT associated to sv; arb. units", 80, 0, 400);
  h_svwmu_leadinglepisoinSV_nm1h = fs->make<TH1F>("h_svwmu_leadinglepisoinSV_nm1h", "; leading muon iso assoicated to sv; arb. units", 60, 0, 0.5);

  h_svwele_leadinglepIDinSV_nm1h = fs->make<TH1F>("h_svwele_leadinglepIDinSV_nm1h", "; leading electron ID assoicated to sv; arb. units", 10, 0, 10); //odd fill structure - rework?   
  h_svwele_leadinglepetainSV_nm1h = fs->make<TH1F>("h_svwele_leadinglepetainSV_nm1h", "; leading electron eta assoicated to sv; arb. units", 50, -3.4, 3.4);
  h_svwele_leadinglepptinSV_nm1h =fs->make<TH1F>("h_svwele_leadinglepptinSV_nm1h",  "; leading electron pT associated to sv; arb. units", 80, 0, 400);
  h_svwele_leadinglepisoinSV_nm1h = fs->make<TH1F>("h_svwele_leadinglepisoinSV_nm1h", "; leading electron iso assoicated to sv; arb. units", 60, 0, 0.5);

  //lep passes all other cuts (full sel)
  h_svwlep_minjetlepdr = fs->make<TH1F>("h_svwlep_minjetlepdr", "; min jet - leading lep dR; arb. units", 100, 0, 6.3);
  h_svwele_minjetlepdr = fs->make<TH1F>("h_svwele_minjetlepdr", "; min jet - leading ele dR; arb. units", 100, 0, 6.3);
  h_svwmu_minjetlepdr = fs->make<TH1F>("h_svwmu_minjetlepdr", "; min jet - leading mu dR; arb. units", 100, 0, 6.3);


  //GEN COMMENTED OUT
//   const char* lep_tag[2] = {"ele", "mu"};
//   for (int i = 0; i< 2; ++i) {
//     // h_ngenmatched_[i] = fs->make<TH1F>(TString::Format("h_ngenmatched_%s", lep_tag[i]), TString::Format("; n of genmatched %s;arb. units", lep_tag[i]), 3, 0, 3);
//     // h_closestdR_gen_[i] = fs->make<TH1F>(TString::Format("h_closestdR_gen_%s", lep_tag[i]), TString::Format("; closest gen-reco %s dR;arb. units", lep_tag[i]), 200, 0, 2);

//     h_lepdau_novtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_novtx_%s", lep_tag[i]), TString::Format("; no SV matched - is the reco %s matched?;", lep_tag[i]), 3, 0, 3);
//     h_lepdau_wvtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_wvtx_%s", lep_tag[i]), TString::Format("; SV is matched - is the reco %s matched?;", lep_tag[i]), 3, 0, 3);
//     h_lepdau_invtx_[i] = fs->make<TH1F>(TString::Format("h_lepdau_invtx_%s", lep_tag[i]), TString::Format("; SV & %s are matched - is the %s in the SV?;", lep_tag[i], lep_tag[i]), 3, 0, 3);
//     h_lepdau_inSV_pt_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_pt_%s", lep_tag[i]), TString::Format("; genmatched %s inSV pt;", lep_tag[i]), 200, 0, 1000);
//     h_lepdau_inSV_dxy_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_dxy_%s", lep_tag[i]), TString::Format("; genmatched %s inSV dxy;", lep_tag[i]), 150, 0, 3.0);
//     h_lepdau_inSV_dxyerr_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_dxyerr_%s", lep_tag[i]), TString::Format("; genmatched %s inSV dxyerr;", lep_tag[i]), 100, 0, 0.05);
//     h_lepdau_inSV_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s inSV nsigmadxy;", lep_tag[i]), 200, 0, 200);
//     h_lepdau_inSV_missdist_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_missdist_%s", lep_tag[i]), TString::Format(";missdist btwn SV and genmatched %s inSV;", lep_tag[i]), 150, 0, 3.0);
//     h_lepdau_inSV_missdisterr_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_missdisterr_%s", lep_tag[i]), TString::Format(";missdisterr btwn SV and genmatched %s inSV;", lep_tag[i]), 100, 0, 0.05);
//     h_lepdau_inSV_missdistsig_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_missdistsig_%s", lep_tag[i]), TString::Format(";missdistsig btwn SV and genmatched %s inSV;", lep_tag[i]), 200, 0, 100);
//     h_lepdau_inSV_iso_[i] = fs->make<TH1F>(TString::Format("h_lepdau_inSV_iso_%s", lep_tag[i]), TString::Format("; iso of genmatched %s inSV;", lep_tag[i]), 100, 0, 1.0);

//     h_lepdau_outSV_pt_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_pt_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV pt;", lep_tag[i]), 200, 0, 1000);
//     h_lepdau_outSV_dxy_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_dxy_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV dxy;", lep_tag[i]), 150, 0, 3.0);
//     h_lepdau_outSV_dxyerr_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_dxyerr_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV dxyerr;", lep_tag[i]), 100, 0, 0.05);
//     h_lepdau_outSV_nsigmadxy_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_nsigmadxy_%s", lep_tag[i]), TString::Format("; genmatched %s not inSV nsigmadxy;", lep_tag[i]), 200, 0, 200);
//     h_lepdau_outSV_missdist_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_missdist_%s", lep_tag[i]), TString::Format(";missdist btwn SV and genmatched %s not inSV;", lep_tag[i]), 150, 0, 3.0);
//     h_lepdau_outSV_missdisterr_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_missdisterr_%s", lep_tag[i]), TString::Format(";missdisterr btwn SV and genmatched %s not inSV;", lep_tag[i]), 100, 0, 0.05);
//     h_lepdau_outSV_missdistsig_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_missdistsig_%s", lep_tag[i]), TString::Format(";missdistsig btwn SV and genmatched %s not inSV;", lep_tag[i]), 200, 0, 100);
//     h_lepdau_outSV_iso_[i] = fs->make<TH1F>(TString::Format("h_lepdau_outSV_iso_%s", lep_tag[i]), TString::Format("; iso of genmatched %s not inSV;", lep_tag[i]), 100, 0, 1.0);
//  }

  PairwiseHistos::HistoDefs hs;

  hs.add("x", "SV x (cm)", 100, -4, 4);
  hs.add("y", "SV y (cm)", 100, -4, 4);
  hs.add("z", "SV z (cm)", 100, -25, 25);
  hs.add("phi", "SV phi", 25, -3.15, 3.15);
  hs.add("phi_pv", "SV phi w.r.t. PV", 25, -3.15, 3.15);
  hs.add("cxx", "SV covariance xx (cm^{2})", 100, 0, 1e-5);
  hs.add("cxy", "SV covariance xy (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("cxz", "SV covariance xz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("cyy", "SV covariance yy (cm^{2})", 100, 0, 1e-5);
  hs.add("cyz", "SV covariance yz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("czz", "SV covariance zz (cm^{2})", 100, 0, 1e-5);

  hs.add("rescale_chi2", "rescaled-fit SV x (cm)", 40, 0, 10);
  hs.add("rescale_x", "rescaled-fit SV x (cm)", 100, -4, 4);
  hs.add("rescale_y", "rescaled-fit SV y (cm)", 100, -4, 4);
  hs.add("rescale_z", "rescaled-fit SV z (cm)", 100, -25, 25);
  hs.add("rescale_cxx", "rescaled-fit SV covariance xx (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_cxy", "rescaled-fit SV covariance xy (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_cxz", "rescaled-fit SV covariance xz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_cyy", "rescaled-fit SV covariance yy (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_cyz", "rescaled-fit SV covariance yz (cm^{2})", 100, -1e-5, 1e-5);
  hs.add("rescale_czz", "rescaled-fit SV covariance zz (cm^{2})", 100, 0, 1e-5);
  hs.add("rescale_dx", "rescaled-fit - nominal SV x (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dy", "rescaled-fit - nominal SV y (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dz", "rescaled-fit - nominal SV z (cm)", 100, -5e-4, 5e-4);
  hs.add("rescale_dx_big", "rescaled-fit - nominal SV x (cm)", 100, -4, 4);
  hs.add("rescale_dy_big", "rescaled-fit - nominal SV y (cm)", 100, -4, 4);
  hs.add("rescale_dz_big", "rescaled-fit - nominal SV z (cm)", 100, -4, 4);
  hs.add("rescale_d2", "rescaled-fit - nominal SV (2D) (cm)", 100, 0, 8e-4);
  hs.add("rescale_d2_big", "rescaled-fit - nominal SV (2D) (cm)", 100, 0, 4);
  hs.add("rescale_d3", "rescaled-fit - nominal SV (3D) (cm)", 100, 0, 1e-3);
  hs.add("rescale_d3_big", "rescaled-fit - nominal SV (3D) (cm)", 100, 0, 4);
  hs.add("rescale_bsbs2ddist", "rescaled-fit d_{BV} (cm)", 200, 0, 0.1);
  hs.add("rescale_bs2derr", "rescaled-fit #sigma(dist2d(SV, beamspot)) (cm)", 100, 0, 0.050);

  hs.add("max_nm1_refit_dist3_wbad", "maximum n-1 refit distance (3D) (cm)", 1001, -0.001, 1);
  hs.add("max_nm1_refit_dist3", "maximum n-1 refit distance (3D) (cm)", 1000, 0, 1);
  hs.add("max_nm1_refit_dist2", "maximum n-1 refit distance (2D) (cm)", 1000, 0, 1);
  hs.add("max_nm1_refit_distz", "maximum n-1 refit z distance (cm)", 1000, 0, 1);

  hs.add("ntracks",                       "# of tracks/SV",                                                               40,    0,      40);
  hs.add("ntracksptgt3",                  "# of tracks/SV w/ p_{T} > 3 GeV",                                              40,    0,      40);
  hs.add("ntracksptgt10",                 "# of tracks/SV w/ p_{T} > 10 GeV",                                             40,    0,      40);
  hs.add("ntracksetagt1p5",               "# of tracks/SV w/ |#eta| > 1.5",                                               40,    0,      40);
  hs.add("trackminnhits",                 "min number of hits on track per SV",                                           40,    0,      40);
  hs.add("trackmaxnhits",                 "max number of hits on track per SV",                                           40,    0,      40);
  hs.add("njetsntks",                     "# of jets assoc. by tracks to SV",                                             10,    0,      10);
  hs.add("nelectrons",                    " # of ele assoc. to SV",                                                        5,    0,       5);
  hs.add("nmuons",                        " # of mu assoc. to SV",                                                        10,    0,      10);
  hs.add("nleptons",                      " # of leptons assoc. to SV",                                                   10,    0,      10);
  hs.add("nleptonspt20",                  " # of leptons w/ p_{T} >= 20 GeV",                                             10,    0,      10);
  hs.add("chi2dof",                       "SV #chi^2/dof",                                                                50,    0,       7);
  hs.add("chi2dofprob",                   "SV p(#chi^2, dof)",                                                            50,    0,       1.2);

  hs.add("tkonlyp",                       "SV tracks-only p (GeV)",                                                       50,    0,     500);
  hs.add("tkonlypt",                      "SV tracks-only p_{T} (GeV)",                                                   50,    0,     400);
  hs.add("tkonlyeta",                     "SV tracks-only #eta",                                                          50,   -4,       4);
  hs.add("tkonlyrapidity",                "SV tracks-only rapidity",                                                      50,   -4,       4);
  hs.add("tkonlyphi",                     "SV tracks-only #phi",                                                          50,   -3.15,    3.15);
  hs.add("tkonlymass",                    "SV tracks-only mass (GeV)",                                                   100,    0,    1000);

  hs.add("jetsntkp",                      "SV jets-by-ntracks -only p (GeV)",                                             50,    0,    1000);
  hs.add("jetsntkpt",                     "SV jets-by-ntracks -only p_{T} (GeV)",                                         50,    0,    1000);
  hs.add("jetsntketa",                    "SV jets-by-ntracks -only #eta",                                                50,   -4,       4);
  hs.add("jetsntkrapidity",               "SV jets-by-ntracks -only rapidity",                                            50,   -4,       4);
  hs.add("jetsntkphi",                    "SV jets-by-ntracks -only #phi",                                                50,   -3.15,    3.15);
  hs.add("jetsntkmass",                   "SV jets-by-ntracks -only mass (GeV)",                                          50,    0,    2000);

  hs.add("tksjetsntkp",                   "SV tracks-plus-jets-by-ntracks p (GeV)",                                       50,    0,    1000);
  hs.add("tksjetsntkpt",                  "SV tracks-plus-jets-by-ntracks p_{T} (GeV)",                                   50,    0,    1000);
  hs.add("tksjetsntketa",                 "SV tracks-plus-jets-by-ntracks #eta",                                          50,   -4,       4);
  hs.add("tksjetsntkrapidity",            "SV tracks-plus-jets-by-ntracks rapidity",                                      50,   -4,       4);
  hs.add("tksjetsntkphi",                 "SV tracks-plus-jets-by-ntracks #phi",                                          50,   -3.15,    3.15);
  hs.add("tksjetsntkmass",                "SV tracks-plus-jets-by-ntracks mass (GeV)",                                   100,    0,    5000);
				        
  hs.add("costhtkonlymombs",              "cos(angle(2-momentum (tracks-only), 2-dist to BS))",                           21,   -1,       1.1);
  hs.add("costhtkonlymompv2d",            "cos(angle(2-momentum (tracks-only), 2-dist to PV))",                           21,   -1,       1.1);
  hs.add("costhtkonlymompv3d",            "cos(angle(3-momentum (tracks-only), 3-dist to PV))",                           21,   -1,       1.1);

  hs.add("costhtksjetsntkmombs",          "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to BS))",          21,   -1,       1.1);
  hs.add("costhtksjetsntkmompv2d",        "cos(angle(2-momentum (tracks-plus-jets-by-ntracks), 2-dist to PV))",          21,   -1,       1.1);
  hs.add("costhtksjetsntkmompv3d",        "cos(angle(3-momentum (tracks-plus-jets-by-ntracks), 3-dist to PV))",          21,   -1,       1.1);

  hs.add("missdisttkonlypv",              "miss dist. (tracks-only) of SV to PV (cm)",                                   100,    0,       2);
  hs.add("missdisttkonlypverr",           "#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                           100,    0,       0.05);
  hs.add("missdisttkonlypvsig",           "N#sigma(miss dist. (tracks-only) of SV to PV) (cm)",                          100,    0,     100);

  hs.add("missdisttksjetsntkpv",          "miss dist. (tracks-plus-jets-by-ntracks) of SV to PV (cm)",                   100,    0,       2);
  hs.add("missdisttksjetsntkpverr",       "#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",           100,    0,       0.05);
  hs.add("missdisttksjetsntkpvsig",       "N#sigma(miss dist. (tracks-plus-jets-by-ntracks) of SV to PV) (cm)",          100,    0,     100);
					  
  hs.add("sumpt2",                        "SV #Sigma p_{T}^{2} (GeV^2)",                                                  50,    0,    10000);

  hs.add("ntrackssharedwpv",  "number of tracks shared with the PV", 30, 0, 30);
  hs.add("ntrackssharedwpvs", "number of tracks shared with any PV", 30, 0, 30);
  hs.add("fractrackssharedwpv",  "fraction of tracks shared with the PV", 41, 0, 1.025);
  hs.add("fractrackssharedwpvs", "fraction of tracks shared with any PV", 41, 0, 1.025);
  hs.add("npvswtracksshared", "number of PVs having tracks shared",  30, 0, 30);
  
  hs.add("trackptmin", "SV min{ trk_{i} p_{T}}", 50, 0, 50);
  hs.add("trackptmax", "SV max{ trk_{i} p_{T}}", 50, 0, 200);
  hs.add("trackptavg", "SV avg{ trk_{i} p_{T}}", 50, 0, 50);
  hs.add("trackptrms", "SV rms{ trk_{i} p_{T}}", 50, 0, 50);

  hs.add("trackpairdptmin", "SV min{#Delta p_{T}(i,j)}", 50, 0, 50);
  hs.add("trackpairdptmax", "SV max{#Delta p_{T}(i,j)}", 50, 0, 200);
  hs.add("trackpairdptavg", "SV avg{#Delta p_{T}(i,j)}", 50, 0, 50);
  hs.add("trackpairdptrms", "SV rms{#Delta p_{T}(i,j)}", 50, 0, 50);


  hs.add("trackdxymin", "SV min{trk_{i} dxy(BS)} (cm)", 50, 0, 0.2);
  hs.add("trackdxymax", "SV max{trk_{i} dxy(BS)} (cm)", 50, 0, 2);
  hs.add("trackdxyavg", "SV avg{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);
  hs.add("trackdxyrms", "SV rms{trk_{i} dxy(BS)} (cm)", 50, 0, 0.5);

  hs.add("trackdzmin", "SV min{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);
  hs.add("trackdzmax", "SV max{trk_{i} dz(PV)} (cm)", 50, 0, 2);
  hs.add("trackdzavg", "SV avg{trk_{i} dz(PV)} (cm)", 50, 0, 1);
  hs.add("trackdzrms", "SV rms{trk_{i} dz(PV)} (cm)", 50, 0, 0.5);

  hs.add("trackpterrmin", "SV min{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterrmax", "SV max{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterravg", "SV avg{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);
  hs.add("trackpterrrms", "SV rms{frac. #sigma trk_{i} p_{T}}", 32, 0, 2);

  hs.add("tracketaerrmin", "SV min{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);
  hs.add("tracketaerrmax", "SV max{frac. #sigma trk_{i} #eta}", 32, 0, 0.005);
  hs.add("tracketaerravg", "SV avg{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);
  hs.add("tracketaerrrms", "SV rms{frac. #sigma trk_{i} #eta}", 32, 0, 0.002);

  hs.add("trackphierrmin", "SV min{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);
  hs.add("trackphierrmax", "SV max{frac. #sigma trk_{i} #phi}", 32, 0, 0.005);
  hs.add("trackphierravg", "SV avg{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);
  hs.add("trackphierrrms", "SV rms{frac. #sigma trk_{i} #phi}", 32, 0, 0.002);

  hs.add("trackdxynsigmamin", "SV min{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmamax", "SV max{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmaavg", "SV avg{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);
  hs.add("trackdxynsigmarms", "SV rms{N #sigma trk_{i} dxy(BS)} (cm)", 50, 0, 10);

  hs.add("trackdxyerrmin", "SV min{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.004);
  hs.add("trackdxyerrmax", "SV max{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);
  hs.add("trackdxyerravg", "SV avg{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);
  hs.add("trackdxyerrrms", "SV rms{#sigma trk_{i} dxy(BS)} (cm)", 32, 0, 0.1);

  hs.add("trackdzerrmin", "SV min{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.01);
  hs.add("trackdzerrmax", "SV max{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);
  hs.add("trackdzerravg", "SV avg{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);
  hs.add("trackdzerrrms", "SV rms{#sigma trk_{i} dz(PV)} (cm)", 32, 0, 0.1);

  hs.add("trackpairdetamin", "SV min{#Delta #eta(i,j)}", 150,    0,       1.5);
  hs.add("trackpairdetamax", "SV max{#Delta #eta(i,j)}", 150,    0,       7);
  hs.add("trackpairdetaavg", "SV avg{#Delta #eta(i,j)}", 150,    0,       5);
  hs.add("trackpairdetarms", "SV rms{#Delta #eta(i,j)}", 150,    0,       3);

  hs.add("trackpairdphimax",   "SV max{|#Delta #phi(i,j)|}",   100, 0, 3.15);
  hs.add("trackpairdphimaxm1", "SV max-1{|#Delta #phi(i,j)|}", 100, 0, 3.15);
  hs.add("trackpairdphimaxm2", "SV max-2{|#Delta #phi(i,j)|}", 100, 0, 3.15);

  hs.add("trackpairdrmin", "SV min{#Delta R(i,j)}", 150, 0, 1.5);
  hs.add("trackpairdrmax", "SV max{#Delta R(i,j)}", 150, 0, 7);
  hs.add("trackpairdravg", "SV avg{#Delta R(i,j)}", 150, 0, 5);
  hs.add("trackpairdrrms", "SV rms{#Delta R(i,j)}", 150, 0, 3);

  hs.add("costhtkmomvtxdispmin", "SV min{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispmax", "SV max{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdispavg", "SV avg{cos(angle(trk_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhtkmomvtxdisprms", "SV rms{cos(angle(trk_{i}, SV-PV))}", 50,  0, 1);

  hs.add("costhjetmomvtxdispmin", "SV min{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispmax", "SV max{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdispavg", "SV avg{cos(angle(jet_{i}, SV-PV))}", 50, -1, 1);
  hs.add("costhjetmomvtxdisprms", "SV rms{cos(angle(jet_{i}, SV-PV))}", 50,  0, 1);

  hs.add("multipv_maxdz",    "max #Delta z of PV w tracks shared (cm)", 100, 0, 10);
  hs.add("multipvbyz_maxdz", "max #Delta z of PV w track-assoc-by-z (cm)", 100, 0, 10);

  //GEN COMMENTED OUT
  // hs.add("gen2ddist",                     "dist2d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  // hs.add("gen2derr",                      "#sigma(dist2d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  // hs.add("gen2dsig",                      "N#sigma(dist2d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  // hs.add("gen3ddist",                     "dist3d(SV, closest gen vtx) (cm)",                                            200,    0,       0.2);
  // hs.add("gen3derr",                      "#sigma(dist3d(SV, closest gen vtx)) (cm)",                                    200,    0,       0.2);
  // hs.add("gen3dsig",                      "N#sigma(dist3d(SV, closest gen vtx)) (cm)",                                   200,    0,     100);
  hs.add("bs2ddist",                      "dist2d(SV, beamspot) (cm)",                                                  1000,    0,      2.5);
  hs.add("bsbs2ddist",                    "dist2d(SV, beamspot) (cm)",                                                  1000,    0,      2.5);
  hs.add("bs2derr",                       "#sigma(dist2d(SV, beamspot)) (cm)",                                           1000,    0,       0.05);
  hs.add("bs2dsig",                       "N#sigma(dist2d(SV, beamspot))",                                               100,    0,     100);
  hs.add("pv2ddist",                      "dist2d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv2derr",                       "#sigma(dist2d(SV, PV)) (cm)",                                                 100,    0,       0.05);
  hs.add("pv2dsig",                       "N#sigma(dist2d(SV, PV))",                                                     100,    0,     100);
  hs.add("pv3ddist",                      "dist3d(SV, PV) (cm)",                                                         100,    0,       0.5);
  hs.add("pv3derr",                       "#sigma(dist3d(SV, PV)) (cm)",                                                 100,    0,       0.1);
  hs.add("pv3dsig",                       "N#sigma(dist3d(SV, PV))",                                                     100,    0,     100);
  hs.add("pvdz",                          "dz(SV, PV) (cm)",                                                             100,    0,       0.5);
  hs.add("pvdzerr",                       "#sigma(dz(SV, PV)) (cm)",                                                     100,    0,       0.1);
  hs.add("pvdzsig",                       "N#sigma(dz(SV, PV))",                                                         100,    0,     100);


  const char* lmt_ex[4] = {"", "loose b-", "medium b-", "tight b-"};
  for (int i = 0; i < 4; ++i) {
    hs.add(TString::Format("jet%d_deltaphi0", i), TString::Format("|#Delta#phi| to closest %sjet", lmt_ex[i]),      25, 0, 3.15);
    hs.add(TString::Format("jet%d_deltaphi1", i), TString::Format("|#Delta#phi| to next closest %sjet", lmt_ex[i]), 25, 0, 3.15);
  }

  for (int i = 0; i < max_ntrackplots; ++i) {
    hs.add(TString::Format("track%i_weight",        i), TString::Format("track%i weight",                      i),  21,  0,      1.05);
    hs.add(TString::Format("track%i_q",             i), TString::Format("track%i charge",                      i),   4, -2,      2);
    hs.add(TString::Format("track%i_pt",            i), TString::Format("track%i p_{T} (GeV)",                 i), 200,  0,    200);
    hs.add(TString::Format("track%i_eta",           i), TString::Format("track%i #eta",                        i),  50, -4,      4);
    hs.add(TString::Format("track%i_phi",           i), TString::Format("track%i #phi",                        i),  50, -3.15,   3.15);
    hs.add(TString::Format("track%i_dxy",           i), TString::Format("track%i dxy (cm)",                    i), 100,  0,      1);
    hs.add(TString::Format("track%i_dz",            i), TString::Format("track%i dz (cm)",                     i), 100,  0,      1);
    hs.add(TString::Format("track%i_pt_err",        i), TString::Format("track%i #sigma(p_{T})/p_{T}",         i), 200,  0,      2);
    hs.add(TString::Format("track%i_eta_err",       i), TString::Format("track%i #sigma(#eta)",                i), 200,  0,      0.02);
    hs.add(TString::Format("track%i_phi_err",       i), TString::Format("track%i #sigma(#phi)",                i), 200,  0,      0.02);
    hs.add(TString::Format("track%i_dxy_err",       i), TString::Format("track%i #sigma(dxy) (cm)",            i), 100,  0,      0.1);
    hs.add(TString::Format("track%i_dz_err",        i), TString::Format("track%i #sigma(dz) (cm)",             i), 100,  0,      0.1);
    hs.add(TString::Format("track%i_nsigmadxy",     i), TString::Format("track%i n#sigma(dxy)",                i), 400,  0,     40);
    hs.add(TString::Format("track%i_chi2dof",       i), TString::Format("track%i #chi^{2}/dof",                i), 100,  0,     10);
    hs.add(TString::Format("track%i_npxhits",       i), TString::Format("track%i number of pixel hits",        i),  12,  0,     12);
    hs.add(TString::Format("track%i_nsthits",       i), TString::Format("track%i number of strip hits",        i),  28,  0,     28);
    hs.add(TString::Format("track%i_nhitsbehind",   i), TString::Format("track%i number of hits behind",       i),  10,  0,     10);
    hs.add(TString::Format("track%i_nhitslost",     i), TString::Format("track%i number of hits lost",         i),  10,  0,     10);
    hs.add(TString::Format("track%i_nhits",         i), TString::Format("track%i number of hits",              i),  40,  0,     40);
    hs.add(TString::Format("track%i_injet",         i), TString::Format("track%i in-jet?",                     i),   2,  0,      2);
    hs.add(TString::Format("track%i_inpv",          i), TString::Format("track%i in-PV?",                      i),  10, -1,      9);
    hs.add(TString::Format("track%i_jet_deltaphi0", i), TString::Format("track%i |#Delta#phi| to closest jet", i),  25,  0,      3.15);
  }

  for (int j = 0; j < sv_num_indices; ++j) {
    const char* exc = sv_index_names[j];

    h_sv[j].Init("h_sv_" + std::string(exc), hs, true, do_scatterplots);

    for (int i = 0; i < 4; ++i)
      h_sv_jets_deltaphi[i][j] = fs->make<TH1F>(TString::Format("h_sv_%s_%sjets_deltaphi", exc, lmt_ex[i]), TString::Format(";%s SV #Delta#phi to %sjets;arb. units", exc, lmt_ex[i]), 50, -3.15, 3.15);

    h_sv_bs2derr_bsbs2ddist[j] = fs->make<TH2F>(TString::Format("h_sv_%s_bs2derr_bsbs2ddist", exc), TString::Format("%s SV;dist2d(SV, beamspot) (cm);#sigma(dist2d(SV, beamspot)) (cm)", exc), 500, 0, 2.5, 100, 0, 0.05);
    h_pvrho_bsbs2ddist[j] = fs->make<TH2F>(TString::Format("h_pvrho_sv_%s_bsbs2ddist", exc), TString::Format("%s SV;dist2d(SV, beamspot) (cm);dist2d(PV, beamspot)) (cm)", exc), 5000, 0, 2.5, 200, 0, 0.1);

    h_sv_elept_eleID[j] = fs->make<TH2F>(TString::Format("h_sv_%s_elept_eleID", exc), TString::Format("%s SV;assoc. ele pt; assoc. ele ID", exc), 200, 0, 1000, 5, 0, 5);
    h_sv_elept_eleiso[j] = fs->make<TH2F>(TString::Format("h_sv_%s_elept_eleiso", exc), TString::Format("%s SV;assoc. ele pt; assoc. ele iso", exc), 200, 0, 1000, 200, 0, 0.2);
    h_sv_mupt_muID[j] = fs->make<TH2F>(TString::Format("h_sv_%s_mupt_muID", exc), TString::Format("%s SV;assoc. mu pt; assoc. mu ID", exc), 200, 0, 1000, 4, 0, 4);
    h_sv_mupt_muiso[j] = fs->make<TH2F>(TString::Format("h_sv_%s_mupt_muiso", exc), TString::Format("%s SV;assoc. mu pt; assoc. mu iso", exc), 200, 0, 1000, 200, 0, 0.2);

    h_sv_test_costh[j] = fs->make<TH1F>(TString::Format("h_sv_%s_test_costh", exc), TString::Format("; %s SV costh;arb. units", exc), 100, -1.5, 1.5);
    h_sv_tracks_sumpt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_tracks_sumpt", exc), TString::Format("; %s SV tracks sumpt;arb. units", exc), 200, 0, 1000);

    h_sv_track_weight[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_weight", exc), TString::Format(";%s SV tracks weight;arb. units", exc), 21, 0, 1.05);
    h_sv_track_q[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_q", exc), TString::Format(";%s SV tracks charge;arb. units.", exc), 4, -2, 2);
    h_sv_track_pt[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_pt", exc), TString::Format(";%s SV tracks p_{T} (GeV);arb. units", exc), 200, 0, 200);
    h_sv_track_eta[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_eta", exc), TString::Format(";%s SV tracks #eta;arb. units", exc), 50, -4, 4);
    h_sv_track_phi[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_phi", exc), TString::Format(";%s SV tracks #phi;arb. units", exc), 50, -3.15, 3.15);
    h_sv_track_dxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dxy", exc), TString::Format(";%s SV tracks dxy (cm);arb. units", exc), 100, 0, 1);
    h_sv_track_dz[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dz", exc), TString::Format(";%s SV tracks dz (cm);arb. units", exc), 100, 0, 1);
    h_sv_track_pt_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_pt_err", exc), TString::Format(";%s SV tracks #sigma(p_{T})/p_{T};arb. units", exc), 200, 0, 2);
    h_sv_track_eta_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_eta_err", exc), TString::Format(";%s SV tracks #sigma(#eta);arb. units", exc), 200, 0, 0.02);
    h_sv_track_phi_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_phi_err", exc), TString::Format(";%s SV tracks #sigma(#phi);arb. units", exc), 200, 0, 0.02);
    h_sv_track_dxy_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dxy_err", exc), TString::Format(";%s SV tracks #sigma(dxy) (cm);arb. units", exc), 100, 0, 0.1);
    h_sv_track_dz_err[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_dz_err", exc), TString::Format(";%s SV tracks #sigma(dz) (cm);arb. units", exc), 100, 0, 0.1);
    h_sv_track_nsigmadxy[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nsigmadxy", exc), TString::Format(";%s SV tracks n#sigma(dxy);arb. units", exc), 400, 0, 40);
    h_sv_track_chi2dof[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_chi2dof", exc), TString::Format(";%s SV tracks #chi^{2}/dof;arb. units", exc), 100, 0, 10);
    h_sv_track_npxhits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_npxhits", exc), TString::Format(";%s SV tracks number of pixel hits;arb. units", exc), 12, 0, 12);
    h_sv_track_nsthits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nsthits", exc), TString::Format(";%s SV tracks number of strip hits;arb. units", exc), 28, 0, 28);
    h_sv_track_nhitsbehind[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhitsbehind", exc), TString::Format(";%s SV tracks number of hits behind;arb. units", exc), 10, 0, 10);
    h_sv_track_nhitslost[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhitslost", exc), TString::Format(";%s SV tracks number of hits lost;arb. units", exc), 10, 0, 10);
    h_sv_track_nhits[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_nhits", exc), TString::Format(";%s SV tracks number of hits", exc), 40, 0, 40);
    h_sv_track_injet[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_injet", exc), TString::Format(";%s SV tracks in-jet?", exc), 2, 0, 2);
    h_sv_track_inpv[j] = fs->make<TH1F>(TString::Format("h_sv_%s_track_inpv", exc), TString::Format(";%s SV tracks in-PV?", exc), 10, -1, 9);
 }
  //GEN COMMENTED OUT
  // h_sv_gen2ddist_signed = fs->make<TH1F>("h_sv_gen2ddist_signed", ";dist2d(SV, closest gen vtx) (cm);arb. units", 400,-0.2,0.2);
  // h_sv_ntk_genbs2ddist = fs->make<TH2F>("h_sv_ntk_genbs2ddist", ";# tracks of SV;dist2d(gen vtx, beamspot) (cm)",40,0,40,500,0,2.5);
  h_sv_ntk_bs2ddist = fs->make<TH2F>("h_sv_ntk_bs2ddist", ";# tracks of SV;dist2d(SV, beamspot) (cm)",40,0,40,500,0,2.5);
  // h_sv_ntk_gen2ddist = fs->make<TH2F>("h_sv_ntk_gen2ddist", ";# tracks of SV;dist2d(SV, closest gen vtx) (cm)",40,0,40,200,0,0.2);
  h_sv_nsv_nmatchjet = fs->make<TH2F>("h_sv_nsv_nmatchjet", ";# jets matched with gen quarks;# SV", 10, 0, 10, 10, 0, 10);

  h_sv_ntkfromjets = fs->make<TH1F>("h_sv_ntkfromjets", ";# tracks from jets;arb. units", 20,0,20);
  h_sv_nallbtags = fs->make<TH3F>("h_sv_nallbtags", ";# loose B jets asso. w/SV;# medium B jets asso. w/SV;# tight B jets asso. w/SV",10,0,10,10,0,10,10,0,10);
  h_sv_nallbtks = fs->make<TH3F>("h_sv_nallbtks", ";# tracks from loose b jets;# tracks from medium b jets;# tracks from tight b jets",20,0,20,20,0,20,20,0,20);
  

  const char* bname[3] = {"loose", "medium", "tight"};

  for (int i = 0; i < 3; ++i) {
    h_sv_nbtags[i] = fs->make<TH1F>(TString::Format("h_sv_nbtags_%i",i), TString::Format(";# %s B jets asso. w/ SV;arb. units",bname[i]), 10,0,10);
    h_sv_nbtks[i] = fs->make<TH1F>(TString::Format("h_sv_nbtks_%i",i), TString::Format(";# tracks from %s B jets;arb. units",bname[i]), 20,0,20);
    h_sv_nbtks_notlep[i] = fs->make<TH1F>(TString::Format("h_sv_nbtks_notlep%i",i), TString::Format(";# tracks from %s B jets and not from sel lep;arb. units",bname[i]), 10,0,10);

    h_svmu_nbtags[i] = fs->make<TH1F>(TString::Format("h_svmu_nbtags_%i",i), TString::Format(";# %s B jets asso. w/ SVmu;arb. units",bname[i]), 10,0,10);
    h_svmu_nbtks[i] = fs->make<TH1F>(TString::Format("h_svmu_nbtks_%i",i), TString::Format(";# tracks from %s B jets;arb. units",bname[i]), 20,0,20);
    h_svmu_nbtks_notlep[i] = fs->make<TH1F>(TString::Format("h_svmu_nbtks_notlep%i",i), TString::Format(";# tracks from %s B jets and not from sel lep;arb. units",bname[i]), 10,0,10);
    h_svele_nbtags[i] = fs->make<TH1F>(TString::Format("h_svele_nbtags_%i",i), TString::Format(";# %s B jets asso. w/ SVele;arb. units",bname[i]), 10,0,10);
    h_svele_nbtks[i] = fs->make<TH1F>(TString::Format("h_svele_nbtks_%i",i), TString::Format(";# tracks from %s B jets;arb. units",bname[i]), 20,0,20);
    h_svele_nbtks_notlep[i] = fs->make<TH1F>(TString::Format("h_svele_nbtks_notlep%i",i), TString::Format(";# tracks from %s B jets and not from sel lep;arb. units",bname[i]), 10,0,10);

    h_sv_nlep_nbtks[i] = fs->make<TH1F>(TString::Format("h_sv_nlep_nbtks_%i",i), TString::Format(";# tracks from leptons and %s B jets;arb. units",bname[i]), 20,0,20);
    // h_sv_nleptks_nbtks[i] = fs->make<TH1F>(TString::Format("h_sv_nleptks_nbtks_%i",i), TString::Format(";# tracks from leptons and %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_nlepbtks[i] = fs->make<TH1F>(TString::Format("h_sv_nlepbtks_%i",i), TString::Format(";# tracks from leptons and %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_nmutks_nbtks[i] = fs->make<TH1F>(TString::Format("h_sv_nmutks_nbtks_%i",i), TString::Format(";# tracks from muon and %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_nmubtks[i] = fs->make<TH1F>(TString::Format("h_sv_nmubtks_%i",i), TString::Format(";# tracks from muon and %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_neletks_nbtks[i] = fs->make<TH1F>(TString::Format("h_sv_neletks_nbtks_%i",i), TString::Format(";# tracks from electrons and %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_nelebtks[i] = fs->make<TH1F>(TString::Format("h_sv_nelebtks_%i",i), TString::Format(";# tracks from electrons and %s B jets;arb. units",bname[i]), 10,0,10);

    // h_sv_nlep_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_nlep_fromb_%i",i), TString::Format(";# tracks from sel leptons coming from %s B jets;arb. units",bname[i]), 10,0,10);
    // h_sv_nele_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_nele_fromb_%i",i), TString::Format(";# tracks from sel electrons coming from %s B jets;arb. units", bname[i]), 10,0,10);
    // h_sv_nmu_fromb[i] = fs->make<TH1F>(TString::Format("h_sv_nmu_fromb_%i",i), TString::Format(";# tracks from sel muons coming from %s B jets;arb. units", bname[i]), 10,0,10);
    
    // h_sv_nlep_notb[i] = fs->make<TH1F>(TString::Format("h_sv_nlep_notb_%i",i), TString::Format(";# tracks from sel leptons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);
    // h_sv_nele_notb[i] = fs->make<TH1F>(TString::Format("h_sv_nele_notb_%i",i), TString::Format(";# tracks from sel electrons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);
    // h_sv_nmu_notb[i] = fs->make<TH1F>(TString::Format("h_sv_nmu_notb_%i",i), TString::Format(";# tracks from sel muons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);

    // h_sv_nlep_notbnob[i] = fs->make<TH1F>(TString::Format("h_sv_nlep_notbnob_%i",i), TString::Format(";# tracks from sel leptons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);
    // h_sv_nele_notbnob[i] = fs->make<TH1F>(TString::Format("h_sv_nele_notbnob_%i",i), TString::Format(";# tracks from sel electrons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);
    // h_sv_nmu_notbnob[i] = fs->make<TH1F>(TString::Format("h_sv_nmu_notbnob_%i",i), TString::Format(";# tracks from sel muons NOT coming from %s B jets;arb. units", bname[i]), 10,0,10);
     
    h_sv_mindeltaphi_svbjet[i] = fs->make<TH1F>(TString::Format("h_sv_mindeltaphi_svbjet_%i",i), TString::Format(";|#Delta#phi(SV-PV,closest asso. %s B jet)|;arb. units",bname[i]),50, 0, 3.15);
    h_sv_mindeltar_sv_bjet[i] = fs->make<TH1F>(TString::Format("h_sv_mindeltar_sv_bjet_%i",i), TString::Format(";#Delta R(SV-PV,closest asso. %s B jet);arb. units",bname[i]),150,0,7);
    h_sv_mindeltaphi_lepbjet[i] = fs->make<TH1F>(TString::Format("h_sv_mindeltaphi_lepbjet_%i",i), TString::Format(";|#Delta#phi(lep,closest asso. %s B jet)|;arb. units",bname[i]),50, 0, 3.15);
    h_sv_mindeltar_lep_bjet[i] = fs->make<TH1F>(TString::Format("h_sv_mindeltar_lep_bjet_%i",i), TString::Format(";#Delta R(lep,closest asso. %s B jet);arb. units",bname[i]),150,0,7);
    h_sv_mindr_ptratio_lep_bjet[i] = fs->make<TH1F>(TString::Format("h_sv_mindr_ptratio_lep_bjet_%i",i), TString::Format(";pT ratio of (lep,closest asso. %s B jet);arb. units",bname[i]),100,0,20);

    h_sv_maxdeltaphi_lepbjet[i] = fs->make<TH1F>(TString::Format("h_sv_maxdeltaphi_lepbjet_%i",i), TString::Format(";|#Delta#phi(lep,furthest asso. %s B jet)|;arb. units",bname[i]),50, 0, 3.15);
    h_sv_maxdeltar_lep_bjet[i] = fs->make<TH1F>(TString::Format("h_sv_maxdeltar_lep_bjet_%i",i), TString::Format(";#Delta R(lep,furthest asso. %s B jet);arb. units",bname[i]),150,0,7);
    h_sv_maxdr_ptratio_lep_bjet[i] = fs->make<TH1F>(TString::Format("h_sv_maxdr_ptratio_lep_bjet_%i",i), TString::Format(";pT ratio of (lep,furthest asso. %s B jet);arb. units",bname[i]),100,0,20);

  }

  h_sv_ntk_njet = fs->make<TH2F>("h_sv_ntk_njet", "; # tracks of SV; # associated jets of SV", 40,0,40,10,0,10);
  h_sv_ntk0_ntk1 = fs->make<TH2F>("h_sv_ntk0_ntk1", "; # tracks of SV0; # tracks of SV1", 40,0,40,40,0,40);
  h_sv_xy = fs->make<TH2F>("h_sv_xy", ";SV x (cm);SV y (cm)", 100, -4, 4, 100, -4, 4);
  h_sv_xy_alt = fs->make<TH2F>("h_sv_xy_alt", ";SV x (cm);SV y (cm)", 100, -4, 4, 100, -4, 4);
  h_sv_xz = fs->make<TH2F>("h_sv_xz", ";SV x (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_sv_yz = fs->make<TH2F>("h_sv_yz", ";SV y (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_sv_rz = fs->make<TH2F>("h_sv_rz", ";SV r (cm);SV z (cm)", 100, -4, 4, 100, -25, 25);
  h_svdist2d = fs->make<TH1F>("h_svdist2d", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 2);
  h_svdist3d = fs->make<TH1F>("h_svdist3d", ";dist3d(sv #0, #1) (cm);arb. units", 500, 0, 2);
  h_sumdbv = fs->make<TH1F>("h_sumdbv", ";#Sigma(d_{BV}) (cm);arb. units", 400, 0, 4);
  h_sumdbv_trigcomb = fs->make<TH2F>("h_sumdbv_trigcomb", ";#Sigma(d_{BV}) (cm);", 400, 0, 4, 9, 0, 9);   // 2016
  h_caloht_trigcomb = fs->make<TH2F>("h_caloht_trigcomb", ";CaloHT(30);",  500, 0, 2000, 9, 0, 9);   // 2016
  //h_sumdbv_trigcomb = fs->make<TH2F>("h_sumdbv_trigcomb", ";#Sigma(d_{BV}) (cm);", 400, 0, 4, 8, 0, 8); // 2017
  h_dbv0dbv1_trgbit = fs->make<TH3F>("h_dbv0dbv1_trgbit", ";;;", 200, 0, 2, 200, 0, 2, 9, 0, 9);   // 2016
  //h_dbv0dbv1_trgbit = fs->make<TH3F>("h_dbv0dbv1_trgbit", ";;;", 200, 0, 2, 200, 0, 2, 8, 0, 8); // 2017
  h_sv0pvdz_v_sv1pvdz = fs->make<TH2F>("h_sv0pvdz_v_sv1pvdz", ";sv #1 dz to PV (cm);sv #0 dz to PV (cm)", 100, 0, 0.5, 100, 0, 0.5);
  h_sv0pvdzsig_v_sv1pvdzsig = fs->make<TH2F>("h_sv0pvdzsig_v_sv1pvdzsig", ";N#sigma(sv #1 dz to PV);sv N#sigma(#0 dz to PV)", 100, 0, 50, 100, 0, 50);
  h_absdeltaphi01 = fs->make<TH1F>("h_absdeltaphi01", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 315, 0, 3.15);
  h_fractrackssharedwpv01 = fs->make<TH1F>("h_fractrackssharedwpv01", ";fraction of sv #0 and sv #1 tracks shared with the PV;arb. units", 41, 0, 1.025);
  h_fractrackssharedwpvs01 = fs->make<TH1F>("h_fractrackssharedwpvs01", ";fraction of sv #0 and sv #1 tracks shared with any PV;arb. units", 41, 0, 1.025);
  h_pvmosttracksshared = fs->make<TH2F>("h_pvmosttracksshared", ";index of pv most-shared to sv #0; index of pv most-shared to sv #1", 71, -1, 70, 71, -1, 70);
  h_sv_shared_jets  = fs->make<TH1F>("h_sv_shared_jets", ";SV tracks share jet?", 2, 0, 2);
  h_svdist2d_shared_jets = fs->make<TH1F>("h_svdist2d_shared_jets", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_svdist2d_no_shared_jets = fs->make<TH1F>("h_svdist2d_no_shared_jets", ";dist2d(sv #0, #1) (cm);arb. units", 500, 0, 1);
  h_absdeltaphi01_shared_jets = fs->make<TH1F>("h_absdeltaphi01_shared_jets", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 316, 0, 3.16);
  h_absdeltaphi01_no_shared_jets = fs->make<TH1F>("h_absdeltaphi01_no_shared_jets", ";abs(delta(phi of sv #0, phi of sv #1));arb. units", 316, 0, 3.16);
}

void MFVVertexHistos::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);
  
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  const double bsx = mevent->bsx;
  const double bsy = mevent->bsy;
  const double bsz = mevent->bsz;
  const math::XYZPoint bs(bsx, bsy, bsz);
  const math::XYZPoint pv(mevent->pvx, mevent->pvy, mevent->pvz);
  // double caloht = 0.0;

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_token, auxes);

  const int nsv = int(auxes->size());
  h_nsv->Fill(nsv, w);

  //GEN COMMENTED OUT
  // edm::Handle<reco::GenParticleCollection> gen_particles;
  // event.getByToken(gen_particles_token, gen_particles);

  int year = int(MFVNEUTRALINO_YEAR);
  assert(year == 20161 || year == 20162 || year == 2017 || year == 2018); // in case of race conditions where the compiled macro is invalid...                                         

  //random generator to determine if HEM check is applied (in MC)                                                                                                                                                                       
  float hem_check = 1 + (std::rand() % 1);                                                                                                                                                                                           
  bool isData = false; //find better way  

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // matching jets with gen quarks from LLPs and fill a 2D histogram with nsv vs. # total number of jets matched to LLPs
  // do the same but with gen leptons from LLPs;
  // nmatched 0 refers to the first llp; nmatched 1 refers to the second llp
  
  //GEN COMMENTED OUT 
  // double nmatched_0 = 0;
  // double nmatched_1 = 0;

  // std::vector<std::pair<std::string, int>> genmatchedlep{{"lep0", -1}, {"lep1", -1}}; //{ {"lepton0_type", idx}, {"lepton1_type", idx} } if lepton type is tau, force idx = -1 ? 
  
  // for (size_t i=0; i<mevent->gen_daughters.size(); ++i){
  //   // skip stops and only look at leptons and quarks
  //   // FIXME: this only works for stoplq samples
  //   // idx 0, 2 == jets; idx 1, 3 == leptons 
  //   if (abs(mevent->gen_daughter_id[i])==1000006) {
  //     continue;
  //   }
  //   else{
  //     double gd_eta = mevent->gen_daughters[i].Eta();
  //     double gd_phi = mevent->gen_daughters[i].Phi();
  //     int n_matched = 0;

  //     if (abs(mevent->gen_daughter_id[i]) >= 1 && abs(mevent->gen_daughter_id[i]) <= 5) {
  //       for (int ij = 0; ij<mevent->njets(); ++ij){
  //         double dR2 = reco::deltaR2(mevent->nth_jet_eta(ij), mevent->nth_jet_phi(ij), gd_eta, gd_phi);
  //         if (dR2<0.16){
  //           n_matched += 1;
  //         }
  //       }
  //     }
  //     else if (abs(mevent->gen_daughter_id[i]) == 11) { 
  //       genmatchedlep[(i < 2) ? 0 : 1].first = "electron";
  //       std::vector<int> matched_ele_indx; 
  //       std::vector<double> mindR;
  //       for (int ie=0; ie<mevent->nelectrons(); ++ie){
  //         double dR = reco::deltaR(mevent->nth_ele_eta(ie), mevent->nth_ele_phi(ie), gd_eta, gd_phi);
  //         mindR.push_back(dR);
  //         matched_ele_indx.push_back(ie);
  //       }
  //       if (mindR.size() !=0) {
  //         h_closestdR_gen_[0]->Fill(*min_element(mindR.begin(), mindR.end()), w);
  //         float best_dR = *min_element(mindR.begin(), mindR.end());
  //         int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
  //         int bestele_idx = matched_ele_indx[best_idx];

  //         if (best_dR < 0.2) {
  //           genmatchedlep[(i < 2) ? 0 : 1].second = bestele_idx;
  //         }
  //       }
  //     }
  //     else if (abs(mevent->gen_daughter_id[i]) == 13 ) {
  //       genmatchedlep[(i < 2) ? 0 : 1].first = "muon";
  //       std::vector<double> matched_mu_idx;
  //       std::vector<double> mindR;
  //       for (int im=0; im<mevent->nmuons(); ++im){
  //         double dR = reco::deltaR(mevent->nth_mu_eta(im), mevent->nth_mu_phi(im), gd_eta, gd_phi);
  //         mindR.push_back(dR);
  //         matched_mu_idx.push_back(im);
  //       }
  //       if (mindR.size() !=0) {
  //         h_closestdR_gen_[1]->Fill(*min_element(mindR.begin(), mindR.end()), w);
  //         float best_dR = *min_element(mindR.begin(), mindR.end());
  //         int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
  //         int bestmu_idx = matched_mu_idx[best_idx];

  //         if (best_dR < 0.2) {
  //           genmatchedlep[(i < 2) ? 0 : 1].second = bestmu_idx;
  //         }
  //       }
  //     }
  //     else if (abs(mevent->gen_daughter_id[i]) == 15 ) {
  //       genmatchedlep[(i < 2) ? 0 : 1].first = "tau";
  //     }
  //   }
  // }
  // h_sv_nsv_nmatchjet->Fill(nmatched_0+nmatched_1, nsv, w);
  
  // int ngele = 0, ngmu = 0, ngtau = 0; //gen level ele, mu, tau 
  // int ngm_ele = 0, ngm_mu = 0; //genmatched ele, mu

  // for (int i=0; i < 2; ++i){
  //   if (genmatchedlep[i].first == "electron") {
  //     ngele +=1;
  //     if (genmatchedlep[i].second >= 0) ngm_ele += 1; 
  //   }
  //   if (genmatchedlep[i].first == "muon") {
  //     ngmu += 1;
  //     if (genmatchedlep[i].second >= 0) ngm_mu += 1;
  //   }
  //   if (genmatchedlep[i].first == "tau") {
  //     ngtau += 1;
  //   }
  // }
  // h_ngendau_[1]->Fill(ngele, w);
  // h_ngendau_[2]->Fill(ngmu, w);
  // h_ngendau_[3]->Fill(ngtau, w);
  // if (ngele > 0 ) h_ngenmatched_[0]->Fill(ngm_ele, w); //only fill the histogram when expecting ele;mu
  // if  (ngmu > 0 ) h_ngenmatched_[1]->Fill(ngm_mu, w);
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  //   //if genx geny within beampipe 
  //   // if (jmt::Geometry::inside_beampipe(genx, geny)) {
  //   //   h_gensv_winbp->Fill(1,w);
  //   // }
  // }

  //for genmatching 
  //GEN COMMENTED OUT
  // std::vector<std::pair<int, float>> isv_dR; // stores which gensv the sv is closest to (0 or 1) and the dR; the index is which sv it is 
  // std::vector<std::pair<std::string, int>> genmatchedvertex{{"vertexflavor0", -1}, {"vertexflavor1", -1}}; // -1 if vertex unmatched, otherwise it is the sv index 

  //for comparison w/ bjets later. use leptons that pass the med/tight id and isolation 0.1 
  //could have two sv so make this a vector 
  std::vector<float> leading_sel_lepphi(nsv, -1.0);
  std::vector<float> leading_sel_lepeta(nsv, -1.0);
  std::vector<float> leading_sel_leppt(nsv, -1.0);
  std::vector<float> leading_sel_leptype(nsv, -1.0);


  std::vector<std::vector<std::string>> lep_tracks; // 2d vector, vector of track vectors. 


  int nsv_wlep = 0;
  int nsv_cc = 0;
  //different nsv : (nolepcuts, hltmatch_fullsellep_jetlepveto)                                                                                                                        
  std::vector<int> nsvwele_4tk = {0,0};
  std::vector<int> nsvwmu_4tk = {0,0};
  std::vector<int> nsvwele_min5tk = {0,0};
  std::vector<int> nsvwmu_min5tk = {0,0};

  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();
    if (ntracks > 3) ++nsv_cc;

    //eg ("ele", "other", "other") means track0 is an electron, no other tracks are leptons; these leptons pass id, iso 
    std::vector<std::string> leptks(ntracks, "other");

    jmt::MinValue d;
    //GEN COMMENTED OUT 
    // double sv_gen2ddist_sign = 1;
    // for (int igenv = 0; igenv < 2; ++igenv) {
    //   double genx = mevent->gen_lsp_decay[igenv*3+0];
    //   double geny = mevent->gen_lsp_decay[igenv*3+1];
    //   //getting the gen vertex flavor based on what gen daughter originates from the given sv 
    //   if (mevent->gen_daughters.size() != 0) {
    //     int genvtx_fl = abs(mevent->gen_daughter_id[igenv*2+1]);
    //     if (genvtx_fl == 11) genmatchedvertex[igenv].first = "electron";
    //     if (genvtx_fl == 13) genmatchedvertex[igenv].first = "muon";
    //     if (genvtx_fl == 15) genmatchedvertex[igenv].first = "tau";
    //   }
    //   else {
    //     genmatchedvertex[igenv].first = "none";
    //   }

    //   d(igenv, mag(aux.x-genx,
    //               aux.y-geny));  
    // }

    // if (d.i() == 0) {
    //   isv_dR.push_back(std::make_pair(0, d.v())); //sv is closer to genvertex0
    //   if (genmatchedvertex[0].first == "electron") h_sv_gensv_mag_[1]->Fill(d.v(), w);
    //   if (genmatchedvertex[0].first == "muon") h_sv_gensv_mag_[2]->Fill(d.v(), w);
    //   if (genmatchedvertex[0].first == "tau") h_sv_gensv_mag_[3]->Fill(d.v(), w);
    // }
    // if (d.i() == 1) {
    //   isv_dR.push_back(std::make_pair(1, d.v())); //sv is closer to genvertex1
    //   if (genmatchedvertex[1].first == "electron") h_sv_gensv_mag_[1]->Fill(d.v(), w);
    //   if (genmatchedvertex[1].first == "muon") h_sv_gensv_mag_[2]->Fill(d.v(), w);
    //   if (genmatchedvertex[1].first == "tau") h_sv_gensv_mag_[3]->Fill(d.v(), w);
    // }
    // h_sv_gensv_mag_[0]->Fill(d.v(), w);

    // const int genvtx_2d = d.i();
    // double genbs2ddist = mevent->mag(mevent->gen_lsp_decay[genvtx_2d*3+0] - mevent->bsx_at_z(mevent->gen_lsp_decay[genvtx_2d*3+2]),
    //                                  mevent->gen_lsp_decay[genvtx_2d*3+1] - mevent->bsy_at_z(mevent->gen_lsp_decay[genvtx_2d*3+2]) 
    //       );
    // h_sv_ntk_genbs2ddist->Fill(ntracks, genbs2ddist, w);
    // if (genbs2ddist<mevent->bs2ddist(aux))
    //   sv_gen2ddist_sign = -1;

    // h_sv_gen2ddist_signed->Fill(sv_gen2ddist_sign*aux.gen2ddist, w);

    h_sv_ntk_bs2ddist->Fill(ntracks, mevent->bs2ddist(aux), w);
    // h_sv_ntk_gen2ddist->Fill(ntracks, aux.gen2ddist, w); //GEN COMMENTED OUT
    h_sv_xy->Fill(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z), w);
    h_sv_xy_alt->Fill(aux.x, aux.y, w);
    h_sv_xz->Fill(aux.x - mevent->bsx_at_z(aux.z), aux.z - bsz, w);
    h_sv_yz->Fill(aux.y - mevent->bsy_at_z(aux.z), aux.z - bsz, w);
    h_sv_rz->Fill(mevent->bs2ddist(aux) * (aux.y - mevent->bsy_at_z(aux.z) >= 0 ? 1 : -1), aux.z - bsz, w);

    MFVVertexAux::stats trackpairdeta_stats(&aux, aux.trackpairdetas());
    MFVVertexAux::stats   trackpairdr_stats(&aux, aux.trackpairdrs());

    jmt::MaxValue max_nm1_refit_dist3_wbad, max_nm1_refit_dist3, max_nm1_refit_dist2, max_nm1_refit_distz;
    for (size_t i = 0, ie = aux.nnm1(); i < ie; ++i) {
      const double dist3 = mag(aux.nm1_x[i] - aux.x, aux.nm1_y[i] - aux.y, aux.nm1_z[i] - aux.z);
      if (aux.nm1_chi2[i] < 0)
        max_nm1_refit_dist3_wbad(std::numeric_limits<double>::max());
      else {
        max_nm1_refit_dist3_wbad(dist3);
        max_nm1_refit_dist3(dist3);
        max_nm1_refit_dist2(mag(aux.nm1_x[i] - aux.x, aux.nm1_y[i] - aux.y));
        max_nm1_refit_distz(fabs(aux.nm1_z[i] - aux.z));
      }
    }

    if (max_nm1_refit_dist3_wbad == std::numeric_limits<double>::max())
      max_nm1_refit_dist3_wbad.set(-0.0005);

    PairwiseHistos::ValueMap v = {
        {"x", aux.x - mevent->bsx_at_z(aux.z)},
        {"y", aux.y - mevent->bsy_at_z(aux.z)},
        {"z", aux.z - bsz},
        {"phi", atan2(aux.y - mevent->bsy_at_z(aux.z), aux.x - mevent->bsx_at_z(aux.z))},
        {"phi_pv", atan2(aux.y - mevent->pvy, aux.x - mevent->pvx)},
        {"cxx", aux.cxx},
        {"cxy", aux.cxy},
        {"cxz", aux.cxz},
        {"cyy", aux.cyy},
        {"cyz", aux.cyz},
        {"czz", aux.czz},

        {"rescale_chi2", aux.rescale_chi2},
        {"rescale_x", aux.rescale_x - mevent->bsx_at_z(aux.z)},
        {"rescale_y", aux.rescale_y - mevent->bsy_at_z(aux.z)},
        {"rescale_z", aux.rescale_z - bsz},
        {"rescale_cxx", aux.rescale_cxx},
        {"rescale_cxy", aux.rescale_cxy},
        {"rescale_cxz", aux.rescale_cxz},
        {"rescale_cyy", aux.rescale_cyy},
        {"rescale_cyz", aux.rescale_cyz},
        {"rescale_czz", aux.rescale_czz},
        {"rescale_dx", aux.rescale_x - aux.x},
        {"rescale_dy", aux.rescale_y - aux.y},
        {"rescale_dz", aux.rescale_z - aux.z},
        {"rescale_dx_big", aux.rescale_x - aux.x},
        {"rescale_dy_big", aux.rescale_y - aux.y},
        {"rescale_dz_big", aux.rescale_z - aux.z},
        {"rescale_d2",     mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y)},
        {"rescale_d2_big", mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y)},
        {"rescale_d3",     mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y, aux.rescale_z - aux.z)},
        {"rescale_d3_big", mag(aux.rescale_x - aux.x, aux.rescale_y - aux.y, aux.rescale_z - aux.z)},
        {"rescale_bsbs2ddist", mag(aux.x - mevent->bsx_at_z(aux.z), aux.y - mevent->bsy_at_z(aux.z))},
        {"rescale_bs2derr", aux.rescale_bs2derr},

        {"max_nm1_refit_dist3_wbad", max_nm1_refit_dist3_wbad},
        {"max_nm1_refit_dist3", max_nm1_refit_dist3},
        {"max_nm1_refit_dist2", max_nm1_refit_dist2},
        {"max_nm1_refit_distz", max_nm1_refit_distz},

        {"ntracks",                 ntracks},
        {"ntracksptgt3",            aux.ntracksptgt(3)},
        {"ntracksptgt10",           aux.ntracksptgt(10)},
        {"ntracksetagt1p5",         aux.ntracksetagt(1.5)},
        {"trackminnhits",           aux.trackminnhits()},
        {"trackmaxnhits",           aux.trackmaxnhits()},
        {"njetsntks",               aux.njets[mfv::JByNtracks]},
        {"nelectrons",              aux.nelectrons},
        {"nmuons",                  aux.nmuons},
        {"nleptons",                aux.nleptons},
        {"nleptonspt20",            aux.nlepptgt20},        
        {"chi2dof",                 aux.chi2dof()},
        {"chi2dofprob",             TMath::Prob(aux.chi2, aux.ndof())},

        {"tkonlyp",             aux.p4(mfv::PTracksOnly).P()},
        {"tkonlypt",            aux.pt[mfv::PTracksOnly]},
        {"tkonlyeta",           aux.eta[mfv::PTracksOnly]},
        {"tkonlyrapidity",      aux.p4(mfv::PTracksOnly).Rapidity()},
        {"tkonlyphi",           aux.phi[mfv::PTracksOnly]},
        {"tkonlymass",          aux.mass[mfv::PTracksOnly]},

        {"jetsntkp",             aux.p4(mfv::PJetsByNtracks).P()},
        {"jetsntkpt",            aux.pt[mfv::PJetsByNtracks]},
        {"jetsntketa",           aux.eta[mfv::PJetsByNtracks]},
        {"jetsntkrapidity",      aux.p4(mfv::PJetsByNtracks).Rapidity()},
        {"jetsntkphi",           aux.phi[mfv::PJetsByNtracks]},
        {"jetsntkmass",          aux.mass[mfv::PJetsByNtracks]},

        {"tksjetsntkp",             aux.p4(mfv::PTracksPlusJetsByNtracks).P()},
        {"tksjetsntkpt",            aux.pt[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntketa",           aux.eta[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkrapidity",      aux.p4(mfv::PTracksPlusJetsByNtracks).Rapidity()},
        {"tksjetsntkphi",           aux.phi[mfv::PTracksPlusJetsByNtracks]},
        {"tksjetsntkmass",          aux.mass[mfv::PTracksPlusJetsByNtracks]},

        {"costhtkonlymombs",         aux.costhmombs  (mfv::PTracksOnly)},
        {"costhtkonlymompv2d",       aux.costhmompv2d(mfv::PTracksOnly)},
        {"costhtkonlymompv3d",       aux.costhmompv3d(mfv::PTracksOnly)},

        {"costhtksjetsntkmombs",     aux.costhmombs  (mfv::PTracksPlusJetsByNtracks)},
        {"costhtksjetsntkmompv2d",   aux.costhmompv2d(mfv::PTracksPlusJetsByNtracks)},
        {"costhtksjetsntkmompv3d",   aux.costhmompv3d(mfv::PTracksPlusJetsByNtracks)},

        {"missdisttkonlypv",        aux.missdistpv   [mfv::PTracksOnly]},
        {"missdisttkonlypverr",     aux.missdistpverr[mfv::PTracksOnly]},
        {"missdisttkonlypvsig",     aux.missdistpvsig(mfv::PTracksOnly)},

        {"missdisttksjetsntkpv",        aux.missdistpv   [mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpverr",     aux.missdistpverr[mfv::PTracksPlusJetsByNtracks]},
        {"missdisttksjetsntkpvsig",     aux.missdistpvsig(mfv::PTracksPlusJetsByNtracks)},

        {"sumpt2",                  aux.sumpt2()},

        {"ntrackssharedwpv", aux.ntrackssharedwpv()},
        {"ntrackssharedwpvs", aux.ntrackssharedwpvs()},
        {"fractrackssharedwpv", float(aux.ntrackssharedwpv()) / ntracks},
        {"fractrackssharedwpvs", float(aux.ntrackssharedwpvs()) / ntracks},
        {"npvswtracksshared", aux.npvswtracksshared()},

        {"trackdxymin", aux.trackdxymin()},
        {"trackdxymax", aux.trackdxymax()},
        {"trackdxyavg", aux.trackdxyavg()},
        {"trackdxyrms", aux.trackdxyrms()},

        {"trackdzmin", aux.trackdzmin()},
        {"trackdzmax", aux.trackdzmax()},
        {"trackdzavg", aux.trackdzavg()},
        {"trackdzrms", aux.trackdzrms()},

        {"trackptmin", aux.mintrackpt()},
        {"trackptmax", aux.maxtrackpt()},
        {"trackptavg", aux.trackptavg()},
        {"trackptrms", aux.trackptrms()},

        {"trackpairdptmin", aux.trackpairdptmin()},
        {"trackpairdptmax", aux.trackpairdptmax()},
        {"trackpairdptavg", aux.trackpairdptavg()},
        {"trackpairdptrms", aux.trackpairdptrms()},

        {"trackpterrmin", aux.trackpterrmin()},
        {"trackpterrmax", aux.trackpterrmax()},
        {"trackpterravg", aux.trackpterravg()},
        {"trackpterrrms", aux.trackpterrrms()},

        {"tracketaerrmin", aux.tracketaerrmin()},
        {"tracketaerrmax", aux.tracketaerrmax()},
        {"tracketaerravg", aux.tracketaerravg()},
        {"tracketaerrrms", aux.tracketaerrrms()},

        {"trackphierrmin", aux.trackphierrmin()},
        {"trackphierrmax", aux.trackphierrmax()},
        {"trackphierravg", aux.trackphierravg()},
        {"trackphierrrms", aux.trackphierrrms()},

        {"trackdxyerrmin", aux.trackdxyerrmin()},
        {"trackdxyerrmax", aux.trackdxyerrmax()},
        {"trackdxyerravg", aux.trackdxyerravg()},
        {"trackdxyerrrms", aux.trackdxyerrrms()},

        {"trackdxynsigmamin", aux.trackdxynsigmamin()},
        {"trackdxynsigmamax", aux.trackdxynsigmamax()},
        {"trackdxynsigmaavg", aux.trackdxynsigmaavg()},
        {"trackdxynsigmarms", aux.trackdxynsigmarms()},

        {"trackdzerrmin", aux.trackdzerrmin()},
        {"trackdzerrmax", aux.trackdzerrmax()},
        {"trackdzerravg", aux.trackdzerravg()},
        {"trackdzerrrms", aux.trackdzerrrms()},

        {"trackpairdetamin", trackpairdeta_stats.min},
        {"trackpairdetamax", trackpairdeta_stats.max},
        {"trackpairdetaavg", trackpairdeta_stats.avg},
        {"trackpairdetarms", trackpairdeta_stats.rms},

        {"trackpairdrmin",  trackpairdr_stats.min},
        {"trackpairdrmax",  trackpairdr_stats.max},
        {"trackpairdravg",  trackpairdr_stats.avg},
        {"trackpairdrrms",  trackpairdr_stats.rms},

        {"costhtkmomvtxdispmin", aux.costhtkmomvtxdispmin()},
        {"costhtkmomvtxdispmax", aux.costhtkmomvtxdispmax()},
        {"costhtkmomvtxdispavg", aux.costhtkmomvtxdispavg()},
        {"costhtkmomvtxdisprms", aux.costhtkmomvtxdisprms()},

        {"costhjetmomvtxdispmin", aux.costhjetmomvtxdispmin()},
        {"costhjetmomvtxdispmax", aux.costhjetmomvtxdispmax()},
        {"costhjetmomvtxdispavg", aux.costhjetmomvtxdispavg()},
        {"costhjetmomvtxdisprms", aux.costhjetmomvtxdisprms()},

        //GEN COMMENTED OUT
        // {"gen2ddist",   aux.gen2ddist},
        // {"gen2derr",    aux.gen2derr},
        // {"gen2dsig",    aux.gen2dsig()},
        // {"gen3ddist",   aux.gen3ddist},
        // {"gen3derr",    aux.gen3derr},
        // {"gen3dsig",    aux.gen3dsig()},
        {"bs2ddist",    aux.bs2ddist},
        {"bsbs2ddist",  mevent->bs2ddist(aux)},
        {"bs2derr",     aux.bs2derr},
        {"bs2dsig",     aux.bs2dsig()},
        {"pv2ddist",    aux.pv2ddist},
        {"pv2derr",     aux.pv2derr},
        {"pv2dsig",     aux.pv2dsig()},
        {"pv3ddist",    aux.pv3ddist},
        {"pv3derr",     aux.pv3derr},
        {"pv3dsig",     aux.pv3dsig()},
        {"pvdz",        aux.pvdz()},
        {"pvdzerr",     aux.pvdzerr()},
        {"pvdzsig",     aux.pvdzsig()}
    };

    std::map<int,int> multipv = aux.pvswtracksshared();
    std::map<int,int> multipvbyz;
    for (int i = 0; i < ntracks; ++i) {
      jmt::MinValue closest(0.1);
      for (int j = 0; j < mevent->npv; ++j)
        closest(j, fabs(aux.track_vz[i] - mevent->pv_z(j)));
      if (closest.i() >= 0)
        ++multipvbyz[closest.i()];
    }

    auto multipv_maxdz = [&](const std::map<int,int>& m) {
      std::vector<int> mv;
      for (auto c : m)
        if (c.first != -1)
          mv.push_back(c.first);
      jmt::MaxValue v;
      const size_t n = mv.size();
      for (size_t i = 0; i < n; ++i)
        for (size_t j = i+1; j < n; ++j)
          v(fabs(mevent->pv_z(mv[i]) - mevent->pv_z(mv[j])));
      return double(v);
    };
    v["multipv_maxdz"] = multipv_maxdz(multipv);
    v["multipvbyz_maxdz"] = multipv_maxdz(multipvbyz);

    std::vector<float> trackpairdphis = aux.trackpairdphis();
    std::sort(trackpairdphis.begin(), trackpairdphis.end());
    const size_t ntrackpairs = trackpairdphis.size();
    v["trackpairdphimax"]   = ntrackpairs < 1 ? -1 : trackpairdphis[ntrackpairs-1];
    v["trackpairdphimaxm1"] = ntrackpairs < 2 ? -1 : trackpairdphis[ntrackpairs-2];
    v["trackpairdphimaxm2"] = ntrackpairs < 3 ? -1 : trackpairdphis[ntrackpairs-3];

    for (int i = 0; i < 4; ++i) {
      std::vector<double> jetdeltaphis;
      for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
          continue;
        if (((mevent->jet_id[ijet] >> 2) & 3) >= i) {
          const double dphi = reco::deltaPhi(atan2(aux.y - bsy, aux.x - bsx), mevent->jet_phi[ijet]);
          fill(h_sv_jets_deltaphi[i], isv, dphi, w);
          jetdeltaphis.push_back(fabs(dphi));
        }
      }
      std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
      int njets = jetdeltaphis.size();
      v[TString::Format("jet%d_deltaphi0", i).Data()] = 0 > njets - 1 ? -1 : jetdeltaphis[0];
      v[TString::Format("jet%d_deltaphi1", i).Data()] = 1 > njets - 1 ? -1 : jetdeltaphis[1];
    }

    fill(h_sv_bs2derr_bsbs2ddist, isv, mevent->bs2ddist(aux), aux.bs2derr, w);
    fill(h_pvrho_bsbs2ddist, isv, mevent->bs2ddist(aux), mevent->pv_rho(), w);

    double sumpt_tracks = 0;
    double sumpx_tracks = 0;
    double sumpy_tracks = 0;
    //another one but to make sure that don't have track that matches to both mu and ele; w/ iso and id 
    std::vector<bool> is_matchedtk(ntracks, false);

    double selmu = 0;
    double selele = 0;
    std::vector<float> sv_track_pt;



    for (int i = 0; i < ntracks; ++i) {
      sv_track_pt.push_back(aux.track_pt(i));
      sumpt_tracks += aux.track_pt(i);
      sumpx_tracks += aux.track_px[i];
      sumpy_tracks += aux.track_py[i];
      fill(h_sv_track_weight, isv, aux.track_weight(i), w);
      fill(h_sv_track_q, isv, aux.track_q(i), w);
      fill(h_sv_track_pt, isv, aux.track_pt(i), w);
      fill(h_sv_track_eta, isv, aux.track_eta[i], w);
      fill(h_sv_track_phi, isv, aux.track_phi[i], w);
      fill(h_sv_track_dxy, isv, aux.track_dxy[i], w);
      fill(h_sv_track_dz, isv, aux.track_dz[i], w);
      fill(h_sv_track_pt_err, isv, aux.track_pt_err[i], w);
      fill(h_sv_track_eta_err, isv, aux.track_eta_err(i), w);
      fill(h_sv_track_phi_err, isv, aux.track_phi_err(i), w);
      fill(h_sv_track_dxy_err, isv, aux.track_dxy_err(i), w);
      fill(h_sv_track_dz_err, isv, aux.track_dz_err(i), w);
      fill(h_sv_track_nsigmadxy, isv, aux.track_dxy[i] / aux.track_dxy_err(i), w);
      fill(h_sv_track_chi2dof, isv, aux.track_chi2dof(i), w);
      fill(h_sv_track_npxhits, isv, aux.track_npxhits(i), w);
      fill(h_sv_track_nsthits, isv, aux.track_nsthits(i), w);
      fill(h_sv_track_nhitsbehind, isv, aux.track_nhitsbehind(i), w);
      fill(h_sv_track_nhitslost, isv, aux.track_nhitslost(i), w);
      fill(h_sv_track_nhits, isv, aux.track_nhits(i), w);
      fill(h_sv_track_injet, isv, aux.track_injet[i], w);
      fill(h_sv_track_inpv, isv, aux.track_inpv[i], w);
      // if (aux.track_dxy[i]/ aux.track_dxy_err(i) < 3) {
      //   std::cout << 
      // }
    }

    std::sort(sv_track_pt.begin(), sv_track_pt.end(), [](auto a, auto b) { return a > b; });

    //calculating costheta by hand : 
    double bs2sv_x = aux.x-mevent->bsx_at_z(aux.z);
    double bs2sv_y = aux.y-mevent->bsy_at_z(aux.z);

    double theta = ((sumpx_tracks * bs2sv_x) + (sumpy_tracks * bs2sv_y)) / ( std::sqrt(pow(2.0, sumpx_tracks) + pow(2.0, sumpy_tracks)) + std::sqrt(pow(2.0, bs2sv_x) + pow(2.0, bs2sv_y)));
    fill(h_sv_test_costh, isv, cos(theta), w);

    fill(h_sv_tracks_sumpt, isv, sumpt_tracks, w);

    std::vector<float> assoc_lep{-1.0};
    std::vector<float> assoc_lepnsigmadxy {-999.0};
    std::vector<float> assoc_lepnsigmadxyrescaled {-999.0};
    std::vector<float> assoc_lepdxy {-999.0};
    std::vector<float> assoc_lepdxyerr {-999.0};
    std::vector<float> assoc_lepdxyerrrescaled {-999.0};

    std::vector<float> assoc_lepeta{-999.0};
    std::vector<float> assoc_lepid{-999.0};
    std::vector<float> assoc_lepiso{-999.0};
    std::vector<float> assoc_lepphi{-999.0};
    std::vector<float> assoc_lephltmatch{-1.0};
    std::vector<float> assoc_leppasstrigpt{-1.0};
    std::vector<float> assoc_leptrig{-1.0};
    std::vector<float> assoc_lephltdR{-999.0};

    //specific for 2018 to investigate HEM                                                                                                                                             
    std::vector<float> assoc_lepHEM{-1.0};
    std::vector<float> assoc_lepetaHEM{-999.0};
    std::vector<float> assoc_lepphiHEM{-999.0};
    std::vector<float> assoc_leptypeHEM{-1.0};

    for (int i=0; i < aux.nmuons; ++i) {
      assoc_lep.push_back(aux.muon_pt[i]);
      assoc_lepHEM.push_back(aux.muon_pt[i]);
      assoc_leptypeHEM.push_back(0);
      assoc_lepnsigmadxy.push_back(fabs(aux.muon_dxybs[i])/aux.muon_dxyerr[i]);
      assoc_lepnsigmadxyrescaled.push_back(fabs(aux.muon_dxybs[i])/aux.rescaled_muon_dxyerr[i]);
      assoc_lepdxy.push_back(fabs(aux.muon_dxybs[i]));
      assoc_lepdxyerr.push_back(fabs(aux.muon_dxyerr[i]));
      assoc_lepdxyerrrescaled.push_back(fabs(aux.rescaled_muon_dxyerr[i]));
      assoc_lepeta.push_back(aux.muon_eta[i]);
      assoc_lepphi.push_back(aux.muon_phi[i]);
      assoc_lepiso.push_back(aux.muon_iso[i]);
      assoc_lephltmatch.push_back(aux.mu_is_hltmatched[i]);
      assoc_lephltdR.push_back(aux.mu_besthltmatchdR[i]);

      auto temp = aux.muon_ID[i]; 
      int id = 0;
      if ( temp[0] == 0 ) id = 0; //none
      if ( temp[0] == 1 ) id = 1; //loose
      if ( temp[1] == 1 ) id = 2; //medium
      if ( temp[2] == 1 ) id = 3; //tight
      assoc_lepid.push_back(id);

      bool mu_passtrigpt = false;
      int mu_trig = -1;
      for(size_t trig : mfv::MuonTriggers) {
        if(satisfiesLepTriggerPT(mevent, auxes, i, isv, trig, setup)) {
          mu_passtrigpt = true;
          mu_trig = trig;
          break;
        }
      }
      assoc_leppasstrigpt.push_back(mu_passtrigpt);
      assoc_leptrig.push_back(mu_trig);

      //reverse match muon to the track 
      double mu_mindr = 999;
      for (int t = 0; t < ntracks; ++t) {
        double dr = reco::deltaR(aux.track_eta[t], aux.track_phi[t], aux.muon_eta[i], aux.muon_phi[i]);
        if (dr < mu_mindr ) {
          mu_mindr = dr;
          if (dr < 0.01) { 
            if (!is_matchedtk[t]) { //if not already matched
              // selections on ele : id, iso 
              if (id > 1 && aux.muon_iso[i] < 0.1) {
                is_matchedtk[t] = true; // make that particular track true 
                leptks[t] = "mu"; 
                ++selmu;
              }
            }
          }
        }
      }

      fill(h_sv_mupt_muID, isv, aux.muon_pt[i], id, w);
      fill(h_sv_mupt_muiso, isv, aux.muon_pt[i], aux.muon_iso[i], w);
    }

    //no veto HEM for plots                                                                                                                                                            
    for (int i=0; i < aux.nelectrons; ++i) {
      assoc_lepHEM.push_back(aux.electron_pt[i]);
      assoc_lepphiHEM.push_back(aux.electron_phi[i]);
      assoc_lepetaHEM.push_back(aux.electron_eta[i]);
      assoc_leptypeHEM.push_back(1);
    }

    for (int i=0; i < aux.nelectrons; ++i) {
      //here need to apply HEM : figure out if electron is in eta/phi + above 30 GeV.                                                                                                  
      // in MC : randomly decide if to keep this electron                                                                                                                              
      // in Data : starting w/ run number 319077 do not use this electron                                                                                                              

      if (year == 2018) {                                                                                                                                                           
        if (!isData) {                                                                                                                                                              
          if (hem_check > 0.352275515) {                                                                                                                                            
            if (aux.electron_pt[i] > 30 && (-3.0 < aux.electron_eta[i]) && ( aux.electron_eta[i] < -1.3) && (-1.57 < aux.electron_phi[i]) && (aux.electron_phi[i] < -0.87)) continue;                                                                                                                                                                                     
          }                                                                                                                                                                         
        }                                                                                                                                                                           
        else {                                                                                                                                                                      
          if (aux.electron_pt[i] > 30 && (-3.0 < aux.electron_eta[i]) && (aux.electron_eta[i] < -1.3) && (-1.57 < aux.electron_phi[i]) && (aux.electron_phi[i] < -0.87)) {          
            if (event.id().run() >= 319077) continue; // starting w/ run number 319077 do not use this electron                                                                     
          }                                                                                                                                                                         
        }                                                                                                                                                                           
      }    
      assoc_lep.push_back(aux.electron_pt[i]);
      assoc_lepnsigmadxy.push_back(fabs(aux.electron_dxybs[i])/aux.electron_dxyerr[i]);
      assoc_lepnsigmadxyrescaled.push_back(fabs(aux.electron_dxybs[i])/aux.rescaled_electron_dxyerr[i]);
      assoc_lepdxy.push_back(fabs(aux.electron_dxybs[i]));
      assoc_lepdxyerr.push_back(fabs(aux.electron_dxyerr[i]));
      assoc_lepdxyerrrescaled.push_back(fabs(aux.rescaled_electron_dxyerr[i]));

      assoc_lepeta.push_back(aux.electron_eta[i]);
      assoc_lepphi.push_back(aux.electron_phi[i]);
      assoc_lepiso.push_back(aux.electron_iso[i]);
      assoc_lephltmatch.push_back(aux.ele_is_hltmatched[i]);
      assoc_lephltdR.push_back(aux.ele_besthltmatchdR[i]);

      // auto temp = aux.electron_ID[i]; 
      // int id = 0;
      // if ( temp[0] == 0 ) id = 0; //none
      // if ( temp[0] == 1 ) id = 1; //veto
      // if ( temp[1] == 1 ) id = 2; //loose
      // if ( temp[2] == 1 ) id = 3; //med 
      // if ( temp[3] == 1 ) id = 4; //tight

      auto temp_noiso = aux.electron_ID_noiso[i];
      int idnoi = 0;
      if ( temp_noiso[0] == 0 ) idnoi = 0; //none
      if ( temp_noiso[0] == 1 ) idnoi = 1; //veto
      if ( temp_noiso[1] == 1 ) idnoi = 2; //loose
      if ( temp_noiso[2] == 1 ) idnoi = 3; //med 
      if ( temp_noiso[3] == 1 ) idnoi = 4; //tight

      bool ele_passtrigpt = false;
      int ele_trig = -1;
      for(size_t trig : mfv::ElectronTriggers) {
        if(satisfiesLepTriggerPT(mevent, auxes, i, isv, trig, setup)) {
          ele_passtrigpt = true;
          ele_trig = trig;
          break;
        }
      }
      assoc_leppasstrigpt.push_back(ele_passtrigpt);
      assoc_leptrig.push_back(ele_trig);

      //reverse match electron to the track 
      double ele_mindr = 999;
      for (int t = 0; t < ntracks; ++t) {
        double dr = reco::deltaR(aux.track_eta[t], aux.track_phi[t], aux.electron_eta[i], aux.electron_phi[i]);
        if (dr < ele_mindr ) {
          ele_mindr = dr;
          if (dr < 0.01) {
            if (!is_matchedtk[t]) { //so not to double count tracks already matched to mu
              // selections on ele : id, iso 
              if (idnoi > 3 && aux.electron_iso[i] < 0.1) {
                is_matchedtk[t] = true;
                leptks[t] = "ele"; 
                ++selele;
              }
            }
          }
        }
      }

      fill(h_sv_elept_eleID, isv, aux.electron_pt[i], idnoi, w);
      fill(h_sv_elept_eleiso, isv, aux.electron_pt[i], aux.electron_iso[i], w);
      assoc_lepid.push_back(idnoi + 5); //electron ID starts at 5 
    }
    if ((selmu > 0) || (selele > 0)) { 
      h_sv_selmu->Fill(selmu,  w);
      h_sv_selele->Fill(selele,  w);
      h_sv_sellep->Fill(selmu + selele,  w);
    }
    //get the leading associated jet : 
    std::vector<float> assoc_jet{-1.0};
    std::vector<float> assoc_jeteta{-999.0};
    std::vector<float> assoc_jetphi{-999.0};

    for (size_t ijet = 0; ijet < aux.njets[mfv::JByNtracks]; ++ijet) {
      assoc_jet.push_back(aux.jet_pt[mfv::JByNtracks][ijet]);
      assoc_jeteta.push_back(aux.jet_eta[mfv::JByNtracks][ijet]);
      assoc_jetphi.push_back(aux.jet_phi[mfv::JByNtracks][ijet]);
    }
    float leading_jetpt = *max_element(assoc_jet.begin(), assoc_jet.end());
    int leading_jetidx = std::max_element(assoc_jet.begin(), assoc_jet.end()) - assoc_jet.begin();

    if (aux.nelectrons + aux.nmuons > 0) nsv_wlep +=1;

    float leading_leppt = *max_element(assoc_lep.begin(), assoc_lep.end());
    int leading_lepidx = std::max_element(assoc_lep.begin(), assoc_lep.end()) - assoc_lep.begin();
    int leading_lepidxHEM = std::max_element(assoc_lepHEM.begin(), assoc_lepHEM.end()) - assoc_lepHEM.begin();

    float leading_leptrackpt = 0;
    if (leading_leppt > 0) {
      //reverse match leading lep to a track 
      double mindr = 999;
      for (int t = 0; t < ntracks; ++t) {
        double dr = reco::deltaR(aux.track_eta[t], aux.track_phi[t], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
        if (dr < mindr ) {
          mindr = dr;
          if (dr < 0.1) { //relax from 0.01 to 0.1 FIXME : Optimize
            leading_leptrackpt = aux.track_pt(t);
          }
        }
      }

      // if ((leading_leppt > 0) && (leading_leptrackpt == 0)) {
      //   std::cout << "found a leading lepton but not the track; the tightest dr was " << mindr << std::endl;
      // }

      bool isotight = false;
      bool idtight = false; //a little misleading, med mu or tight electron                                                                                                            
      bool passeta = fabs(assoc_lepeta[leading_lepidx]) < 2.4;
      bool passpt = assoc_leppasstrigpt[leading_lepidx] == 1;
      bool is_mu = false;

      if (assoc_lepid[leading_lepidx] > 4) {
        //its an electron
        idtight = assoc_lepid[leading_lepidx] > 8;
        is_mu = false;
      }
      else {
        idtight = assoc_lepid[leading_lepidx] > 1; 
        is_mu = true;
      }
      
      if (is_mu) {
        isotight = assoc_lepiso[leading_lepidx] < 0.1;
      }
      else {
        if (assoc_lepeta[leading_lepidx] <= 1.479) {
          if (assoc_lepiso[leading_lepidx] < 0.0287 + 0.506/leading_leppt) {
            isotight = true;
          }
        }
        else if (assoc_lepeta[leading_lepidx] > 1.479) {
          if (assoc_lepiso[leading_lepidx] < 0.0445 + 0.963/leading_leppt) {
            isotight = true;
          }
        }
      }

      bool tight_sel = isotight && idtight && passpt && passeta;
      bool hltmatch_nocuts = assoc_lephltmatch[leading_lepidx];
      bool hltmatch_fullsel = assoc_lephltmatch[leading_lepidx] && tight_sel;

      if (tight_sel) {
        leading_sel_lepphi[isv] = assoc_lepphi[leading_lepidx];
        leading_sel_lepeta[isv] = assoc_lepeta[leading_lepidx];
        leading_sel_leppt[isv] = leading_leppt;
        leading_sel_leptype[isv] = is_mu;  //false == is electron, true == is mu
      }

      float minjetlepdR = 10.0;
      if (mevent->jet_id.size() != 0) {
        for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
          if (mevent->jet_pt[ijet] <  mfv::min_jet_pt) continue;
          float jetlepdR = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
          if (jetlepdR < minjetlepdR) {
            minjetlepdR = jetlepdR;
          }
        }                                                                                                                                                                          
      }
      bool jetlepdRgt0p4 = minjetlepdR > 0.4;

      //the nm1 plots :                                                                                                                                                                  
      //nm1 hltmatch                                                                                                                                                                   
      if (jetlepdRgt0p4) {
        if (tight_sel) {
          h_svwlep_leadinglepishltmatchedinSV_nm1->Fill(hltmatch_nocuts, w);
          if (is_mu) h_svwmu_leadinglepishltmatchedinSV_nm1->Fill(hltmatch_nocuts, w);
          if (!is_mu) h_svwele_leadinglepishltmatchedinSV_nm1->Fill(hltmatch_nocuts, w);
        }
        //nm1 eta                                                                                                                                                                      
        if (hltmatch_nocuts && isotight && idtight && passpt) {
          h_svwlep_leadinglepetainSV_nm1->Fill(assoc_lepeta[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepetainSV_nm1->Fill(assoc_lepeta[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepetainSV_nm1->Fill(assoc_lepeta[leading_lepidx], w);
        }
        //nm1 pt                                                                                                                                                                       
        if (hltmatch_nocuts && isotight && idtight && passeta) {
          h_svwlep_leadinglepptinSV_nm1->Fill(leading_leppt, w);
          if (is_mu) h_svwmu_leadinglepptinSV_nm1->Fill(leading_leppt, w);
          if (!is_mu) h_svwele_leadinglepptinSV_nm1->Fill(leading_leppt, w);
        }
        //nm1 iso                                                                                                                                                                      
	      if (hltmatch_nocuts && idtight && passpt && passeta) {
          h_svwlep_leadinglepisoinSV_nm1->Fill(assoc_lepiso[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepisoinSV_nm1->Fill(assoc_lepiso[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepisoinSV_nm1->Fill(assoc_lepiso[leading_lepidx], w);
        }
        //nm1 ID                                                                                                                                                                       
        if (hltmatch_nocuts && isotight && passpt && passeta) {
          h_svwlep_leadinglepIDinSV_nm1->Fill(assoc_lepid[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepIDinSV_nm1->Fill(assoc_lepid[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepIDinSV_nm1->Fill(assoc_lepid[leading_lepidx], w);
        }

        //nm1h eta                                                                                                                                                                     
        if (isotight && idtight && passpt) {
          h_svwlep_leadinglepetainSV_nm1h->Fill(assoc_lepeta[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepetainSV_nm1h->Fill(assoc_lepeta[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepetainSV_nm1h->Fill(assoc_lepeta[leading_lepidx], w);
        }
        //nm1h pt                                                                                                                                                                      
        if (isotight && idtight && passeta) {
          h_svwlep_leadinglepptinSV_nm1h->Fill(leading_leppt, w);
          if (is_mu) h_svwmu_leadinglepptinSV_nm1h->Fill(leading_leppt, w);
          if (!is_mu) h_svwele_leadinglepptinSV_nm1h->Fill(leading_leppt, w);
        }
        //nm1h iso                                                                                                                                                                     
        if (idtight && passpt && passeta) {
          h_svwlep_leadinglepisoinSV_nm1h->Fill(assoc_lepiso[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepisoinSV_nm1h->Fill(assoc_lepiso[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepisoinSV_nm1h->Fill(assoc_lepiso[leading_lepidx], w);
        }
        //nm1h ID                                                                                                                                                                      
        if (isotight && passpt && passeta) {
          h_svwlep_leadinglepIDinSV_nm1h->Fill(assoc_lepid[leading_lepidx], w);
          if (is_mu) h_svwmu_leadinglepIDinSV_nm1h->Fill(assoc_lepid[leading_lepidx], w);
          if (!is_mu) h_svwele_leadinglepIDinSV_nm1h->Fill(assoc_lepid[leading_lepidx], w);
        }
      }

      //the minjetlep dR plots; leptons pass full sel 
      if (hltmatch_fullsel) {
        h_svwlep_minjetlepdr->Fill(minjetlepdR, w);
        if (!is_mu) h_svwele_minjetlepdr->Fill(minjetlepdR, w);
        else h_svwmu_minjetlepdr->Fill(minjetlepdR, w);
      }

      std::vector<bool> iso_eta = {true, (hltmatch_fullsel && jetlepdRgt0p4)};

      if (tight_sel) {
        if (is_mu) {
          // currently set up only for 2018
          bool pass_mu_trig = false; //try first mu triggers (since its a SVwmu)
          bool trig_passed = false;
          if(mevent->pass_hlt(mfv::b_HLT_IsoMu24)) {
            h_svwmu_tightsel_passtriggers->Fill(1, w);
            pass_mu_trig = true;
            trig_passed = true;
          }
          if( (mevent->pass_hlt(mfv::b_HLT_Mu50)) & !trig_passed) {
            h_svwmu_tightsel_passtriggers->Fill(2, w);
            pass_mu_trig = true;
            trig_passed = true;
          }
          if (!pass_mu_trig) { 
            if(mevent->pass_hlt(mfv::b_HLT_Ele32_WPTight_Gsf)) {
              h_svwmu_tightsel_passtriggers->Fill(3, w);
              trig_passed = true;
            }
            if( (mevent->pass_hlt(mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT)) & !trig_passed) {
              h_svwmu_tightsel_passtriggers->Fill(4, w);
              trig_passed = true;
            }
            if(( mevent->pass_hlt(mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165)) & !trig_passed) {
              h_svwmu_tightsel_passtriggers->Fill(5, w);
              trig_passed = true;
            }
            if(( mevent->pass_hlt(mfv::b_HLT_Photon200)) & !trig_passed) {
              h_svwmu_tightsel_passtriggers->Fill(6, w);
              trig_passed = true;
            }
          }
        }
        else {
          bool pass_ele_trig = false; //try first electron triggers (since its a SVwele)
          bool trig_passed = false;

          if(mevent->pass_hlt(mfv::b_HLT_Ele32_WPTight_Gsf)) {
            h_svwele_tightsel_passtriggers->Fill(3, w);
            trig_passed = true;
            pass_ele_trig = true;
          }
          if((mevent->pass_hlt(mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT)) & !trig_passed) {
            h_svwele_tightsel_passtriggers->Fill(4, w);
            trig_passed = true;
            pass_ele_trig = true;
          }
          if((mevent->pass_hlt(mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165))  & !trig_passed) {
            h_svwele_tightsel_passtriggers->Fill(5, w);
            trig_passed = true;
            pass_ele_trig = true;
          }
          if(( mevent->pass_hlt(mfv::b_HLT_Photon200)) & !trig_passed) {
            h_svwele_tightsel_passtriggers->Fill(6, w);
            trig_passed = true;
            pass_ele_trig = true;
          }
          if (!pass_ele_trig) { 
            if(mevent->pass_hlt(mfv::b_HLT_IsoMu24)) {
              h_svwele_tightsel_passtriggers->Fill(1, w);
              trig_passed = true;
            }
            if ((mevent->pass_hlt(mfv::b_HLT_Mu50)) & !trig_passed) {
              h_svwele_tightsel_passtriggers->Fill(2, w);
              trig_passed = true;
            }
          }
        }
      }

      for (int i = 0; i < 2; i++) { 
        if (iso_eta[i]) { 
          //HEM specific                                                                                                                                                               
          if (assoc_leptypeHEM[leading_lepidxHEM] == 1) {
            h_svwelewHEM_leadinglepetainSV_[i]->Fill(assoc_lepetaHEM[leading_lepidxHEM], w);
            h_svwelewHEM_leadinglepphiinSV_[i]->Fill(assoc_lepphiHEM[leading_lepidxHEM], w);
            h_svwelewHEM_leadinglepeta_vs_phi_inSV_[i]->Fill(assoc_lepetaHEM[leading_lepidxHEM], assoc_lepphiHEM[leading_lepidxHEM], w);
          }
          h_svwlep_rescale_bs2derr_[i]->Fill(aux.rescale_bs2derr, w);
          h_svwlep_rescale_pertkbs2derr_[i]->Fill(aux.rescale_bs2derr*sqrt(aux.ntracks()), w);
          h_svwlep_bsbs2ddist_[i]->Fill(mevent->bs2ddist(aux), w);
          h_svwlep_ntracks_[i]->Fill(aux.ntracks(), w);
          h_svwlep_trackpairdravg_[i]->Fill(trackpairdr_stats.avg, w);
          h_svwlep_trackpairdravgmmax_[i]->Fill(2*(trackpairdr_stats.avg*(aux.ntracks()*(aux.ntracks()-1)/2) - trackpairdr_stats.max)/( (aux.ntracks()- 2)*(aux.ntracks()+1) ), w);
          h_svwlep_avgptnoleptkpt_[i]->Fill( (sumpt_tracks - leading_leptrackpt)/(aux.ntracks()-1), w);
          h_svwlep_costh_[i]->Fill(aux.costhmombs  (mfv::PTracksPlusJetsByNtracks), w);
          h_svwlep_tracktripmassmax_[i]->Fill(aux.tracktripmassmax(), w);
          h_svwlep_leadinglepptinSV_[i]->Fill(leading_leppt, w);
          h_svwlep_leadinglepdxyinSV_[i]->Fill(assoc_lepdxy[leading_lepidx], w);
          h_svwlep_leadinglepdxyerrinSV_[i]->Fill(assoc_lepdxyerr[leading_lepidx], w);
          h_svwlep_leadingleprescaleddxyerrinSV_[i]->Fill(assoc_lepdxyerrrescaled[leading_lepidx], w);
          h_svwlep_leadinglepnsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxy[leading_lepidx], w);
          h_svwlep_leadingleprescalednsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxyrescaled[leading_lepidx], w);
          h_svwlep_leadinglepIDinSV_[i]->Fill(assoc_lepid[leading_lepidx], w);
          h_svwlep_leadinglepisoinSV_[i]->Fill(assoc_lepiso[leading_lepidx], w);
          h_svwlep_leadinglepetainSV_[i]->Fill(assoc_lepeta[leading_lepidx], w);
          h_svwlep_trackptgt3_[i]->Fill(aux.ntracksptgt(3), w);
          h_svwlep_trackptgt10_[i]->Fill(aux.ntracksptgt(10), w);
          h_svwlep_leadinglepeta_vs_phi_inSV_[i]->Fill(assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx], w);

          //same but ele 
          if (!is_mu) { 
            if (ntracks == 4) nsvwele_4tk[i] += 1;
            if (ntracks > 4)  nsvwele_min5tk[i] += 1;

            h_svwele_rescale_bs2derr_[i]->Fill(aux.rescale_bs2derr, w);
            h_svwele_rescale_pertkbs2derr_[i]->Fill(aux.rescale_bs2derr*sqrt(aux.ntracks()), w);
            h_svwele_bsbs2ddist_[i]->Fill(mevent->bs2ddist(aux), w);
            h_svwele_ntracks_[i]->Fill(aux.ntracks(), w);
            h_svwele_trackpairdravg_[i]->Fill(trackpairdr_stats.avg, w);
            h_svwele_trackpairdravgmmax_[i]->Fill(2*(trackpairdr_stats.avg*(aux.ntracks()*(aux.ntracks()-1)/2) - trackpairdr_stats.max)/( (aux.ntracks()- 2)*(aux.ntracks()+1) ), w);
            h_svwele_avgptnoleptkpt_[i]->Fill( (sumpt_tracks - leading_leptrackpt)/(aux.ntracks()-1), w);
            h_svwele_costh_[i]->Fill(aux.costhmombs  (mfv::PTracksPlusJetsByNtracks), w);
            h_svwele_tracktripmassmax_[i]->Fill(aux.tracktripmassmax(), w);
            h_svwele_leadinglepptinSV_[i]->Fill(leading_leppt, w);
            h_svwele_leadinglepdxyinSV_[i]->Fill(assoc_lepdxy[leading_lepidx], w);
            h_svwele_leadinglepdxyerrinSV_[i]->Fill(assoc_lepdxyerr[leading_lepidx], w);
            h_svwele_leadingleprescaleddxyerrinSV_[i]->Fill(assoc_lepdxyerrrescaled[leading_lepidx], w);
            h_svwele_leadinglepnsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxy[leading_lepidx], w);
            h_svwele_leadingleprescalednsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxyrescaled[leading_lepidx], w);
            h_svwele_leadinglepIDinSV_[i]->Fill(assoc_lepid[leading_lepidx], w);
            h_svwele_leadinglepisoinSV_[i]->Fill(assoc_lepiso[leading_lepidx], w);
            h_svwele_leadinglepetainSV_[i]->Fill(assoc_lepeta[leading_lepidx], w);
            h_svwele_leadinglephltdRinSV_[i]->Fill(assoc_lephltdR[leading_lepidx],w);
            h_svwele_trackptgt3_[i]->Fill(aux.ntracksptgt(3), w);
            h_svwele_trackptgt10_[i]->Fill(aux.ntracksptgt(10), w);
            h_svwele_leadinglepeta_vs_phi_inSV_[i]->Fill(assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx], w);
          }
          if (is_mu) {
            if (ntracks == 4) nsvwmu_4tk[i] += 1;
            if (ntracks > 4) nsvwmu_min5tk[i] += 1;

            h_svwmu_rescale_bs2derr_[i]->Fill(aux.rescale_bs2derr, w);
            h_svwmu_rescale_pertkbs2derr_[i]->Fill(aux.rescale_bs2derr*sqrt(aux.ntracks()), w);
            h_svwmu_bsbs2ddist_[i]->Fill(mevent->bs2ddist(aux), w);
            h_svwmu_ntracks_[i]->Fill(aux.ntracks(), w);
            h_svwmu_trackpairdravg_[i]->Fill(trackpairdr_stats.avg, w);
            h_svwmu_trackpairdravgmmax_[i]->Fill(2*(trackpairdr_stats.avg*(aux.ntracks()*(aux.ntracks()-1)/2) - trackpairdr_stats.max)/( (aux.ntracks()- 2)*(aux.ntracks()+1) ), w);
            h_svwmu_avgptnoleptkpt_[i]->Fill( (sumpt_tracks - leading_leptrackpt)/(aux.ntracks()-1), w);
            h_svwmu_costh_[i]->Fill(aux.costhmombs  (mfv::PTracksPlusJetsByNtracks), w);
            h_svwmu_tracktripmassmax_[i]->Fill(aux.tracktripmassmax(), w);
            h_svwmu_leadinglepptinSV_[i]->Fill(leading_leppt, w);
            h_svwmu_leadinglepdxyinSV_[i]->Fill(assoc_lepdxy[leading_lepidx], w);
            h_svwmu_leadinglepdxyerrinSV_[i]->Fill(assoc_lepdxyerr[leading_lepidx], w);
            h_svwmu_leadingleprescaleddxyerrinSV_[i]->Fill(assoc_lepdxyerrrescaled[leading_lepidx], w);
            h_svwmu_leadinglepnsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxy[leading_lepidx], w);
            h_svwmu_leadingleprescalednsigmadxyinSV_[i]->Fill(assoc_lepnsigmadxyrescaled[leading_lepidx], w);
            h_svwmu_leadinglepIDinSV_[i]->Fill(assoc_lepid[leading_lepidx], w);
            h_svwmu_leadinglepisoinSV_[i]->Fill(assoc_lepiso[leading_lepidx], w);
            h_svwmu_leadinglepetainSV_[i]->Fill(assoc_lepeta[leading_lepidx], w);
            h_svwmu_leadinglephltdRinSV_[i]->Fill(assoc_lephltdR[leading_lepidx],w);
            h_svwmu_trackptgt3_[i]->Fill(aux.ntracksptgt(3), w);
            h_svwmu_trackptgt10_[i]->Fill(aux.ntracksptgt(10), w);
            h_svwmu_leadinglepeta_vs_phi_inSV_[i]->Fill(assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx], w);
          }

          // next : use the leading lepton and check the delta R between it and the leading jet in the SV 
          if (leading_jetpt > 0 ) {
            h_svwlepjet_pairdr_[i]->Fill(reco::deltaR(assoc_jeteta[leading_jetidx], assoc_jetphi[leading_jetidx], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);
            h_svwlepjet_pt_[i]->Fill(leading_jetpt, w);
            h_svwlepjet_ptratio_[i]->Fill(leading_leppt/leading_jetpt, w);

            //now for ele
            if (!is_mu) { 
              h_svwelejet_pairdr_[i]->Fill(reco::deltaR(assoc_jeteta[leading_jetidx], assoc_jetphi[leading_jetidx], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);
              h_svwelejet_pt_[i]->Fill(leading_jetpt, w);
              h_svwelejet_ptratio_[i]->Fill(leading_leppt/leading_jetpt, w);
            }
            if (is_mu) {
              h_svwmujet_pairdr_[i]->Fill(reco::deltaR(assoc_jeteta[leading_jetidx], assoc_jetphi[leading_jetidx], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);
              h_svwmujet_pt_[i]->Fill(leading_jetpt, w);
              h_svwmujet_ptratio_[i]->Fill(leading_leppt/leading_jetpt, w);
            }
          }
          //if there is no associated jet, check and see if there is a jet in the event 
          else {
            if (mevent->jet_id.size() != 0) {
              if (mevent->jet_pt[0] > mfv::min_jet_pt) { 
                h_svwlep_jet_pairdr_[i]->Fill(reco::deltaR(mevent->jet_eta[0], mevent->jet_phi[0], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);

                if (!is_mu) 
                  h_svwele_jet_pairdr_[i]->Fill(reco::deltaR(mevent->jet_eta[0], mevent->jet_phi[0], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);
                if (is_mu)
                  h_svwmu_jet_pairdr_[i]->Fill(reco::deltaR(mevent->jet_eta[0], mevent->jet_phi[0], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]), w);
              }
            }
          }
        }
      }
    }

    if (max_ntrackplots > 0) {
      std::vector<std::pair<int,float>> itk_pt;
      for (int i = 0; i < ntracks; ++i)
        itk_pt.push_back(std::make_pair(i, aux.track_pt(i)));

      std::sort(itk_pt.begin(), itk_pt.end(), [](std::pair<int,float> itk_pt1, std::pair<int,float> itk_pt2) { return itk_pt1.second > itk_pt2.second; } );
      for (int i = 0; i < max_ntrackplots; ++i) {
        if (i < ntracks) {
          v[TString::Format("track%i_weight",        i).Data()] = aux.track_weight(itk_pt[i].first);
          v[TString::Format("track%i_q",             i).Data()] = aux.track_q(itk_pt[i].first);
          v[TString::Format("track%i_pt",            i).Data()] = aux.track_pt(itk_pt[i].first);
          v[TString::Format("track%i_eta",           i).Data()] = aux.track_eta[itk_pt[i].first];
          v[TString::Format("track%i_phi",           i).Data()] = aux.track_phi[itk_pt[i].first];
          v[TString::Format("track%i_dxy",           i).Data()] = aux.track_dxy[itk_pt[i].first];
          v[TString::Format("track%i_dz",            i).Data()] = aux.track_dz[itk_pt[i].first];
          v[TString::Format("track%i_pt_err",        i).Data()] = aux.track_pt_err[itk_pt[i].first];
          v[TString::Format("track%i_eta_err",       i).Data()] = aux.track_eta_err(itk_pt[i].first);
          v[TString::Format("track%i_phi_err",       i).Data()] = aux.track_phi_err(itk_pt[i].first);
          v[TString::Format("track%i_dxy_err",       i).Data()] = aux.track_dxy_err(itk_pt[i].first);
          v[TString::Format("track%i_dz_err",        i).Data()] = aux.track_dz_err(itk_pt[i].first);
          v[TString::Format("track%i_nsigmadxy",     i).Data()] = aux.track_dxy[itk_pt[i].first] / aux.track_dxy_err(itk_pt[i].first);
          v[TString::Format("track%i_chi2dof",       i).Data()] = aux.track_chi2dof(itk_pt[i].first);
          v[TString::Format("track%i_npxhits",       i).Data()] = aux.track_npxhits(itk_pt[i].first);
          v[TString::Format("track%i_nsthits",       i).Data()] = aux.track_nsthits(itk_pt[i].first);
          v[TString::Format("track%i_nhitsbehind",   i).Data()] = aux.track_nhitsbehind(itk_pt[i].first);
          v[TString::Format("track%i_nhitslost",     i).Data()] = aux.track_nhitslost(itk_pt[i].first);
          v[TString::Format("track%i_nhits",         i).Data()] = aux.track_nhits(itk_pt[i].first);
          v[TString::Format("track%i_injet",         i).Data()] = aux.track_injet[itk_pt[i].first];
          v[TString::Format("track%i_inpv",          i).Data()] = aux.track_inpv[itk_pt[i].first];

          std::vector<double> jetdeltaphis;
          for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
            if (mevent->jet_pt[ijet] < mfv::min_jet_pt)
              continue;
            jetdeltaphis.push_back(fabs(reco::deltaPhi(aux.track_phi[itk_pt[i].first], mevent->jet_phi[ijet])));
          }
          std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
          int njets = jetdeltaphis.size();
          v[TString::Format("track%i_jet_deltaphi0", i).Data()] = 0 > njets - 1 ? -1 : jetdeltaphis[0];
        } else {
          v[TString::Format("track%i_weight",        i).Data()] = -1e6;
          v[TString::Format("track%i_q",             i).Data()] = -1e6;
          v[TString::Format("track%i_pt",            i).Data()] = -1e6;
          v[TString::Format("track%i_eta",           i).Data()] = -1e6;
          v[TString::Format("track%i_phi",           i).Data()] = -1e6;
          v[TString::Format("track%i_dxy",           i).Data()] = -1e6;
          v[TString::Format("track%i_dz",            i).Data()] = -1e6;
          v[TString::Format("track%i_pt_err",        i).Data()] = -1e6;
          v[TString::Format("track%i_eta_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_phi_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_dxy_err",       i).Data()] = -1e6;
          v[TString::Format("track%i_dz_err",        i).Data()] = -1e6;
          v[TString::Format("track%i_nsigmadxy",     i).Data()] = -1e6;
          v[TString::Format("track%i_chi2dof",       i).Data()] = -1e6;
          v[TString::Format("track%i_npxhits",       i).Data()] = -1e6;
          v[TString::Format("track%i_nsthits",       i).Data()] = -1e6;
          v[TString::Format("track%i_nhitsbehind",   i).Data()] = -1e6;
          v[TString::Format("track%i_nhitslost",     i).Data()] = -1e6;
          v[TString::Format("track%i_nhits",         i).Data()] = -1e6;
          v[TString::Format("track%i_injet",         i).Data()] = -1e6;
          v[TString::Format("track%i_inpv",          i).Data()] = -1e6;
          v[TString::Format("track%i_jet_deltaphi0", i).Data()] = -1e6;
        }
      }
    }

    fill(h_sv, isv, v, w);

    lep_tracks.push_back(leptks);
  }
  h_nsv_wlep->Fill(nsv_wlep, w);
  h_nsv_cc->Fill(nsv_cc, w);

  for(int i=0; i < 2; ++i) {
    h_svwmu_nsv_4tk_[i]->Fill(nsvwmu_4tk[i], w);
    h_svwele_nsv_4tk_[i]->Fill(nsvwele_4tk[i], w);
    h_svwlep_nsv_4tk_[i]->Fill((nsvwmu_4tk[i]+nsvwele_4tk[i]), w);

    h_svwmu_nsv_min4tk_[i]->Fill(nsvwmu_4tk[i] + nsvwmu_min5tk[i], w);
    h_svwele_nsv_min4tk_[i]->Fill(nsvwele_4tk[i]+ nsvwele_min5tk[i], w);
    h_svwlep_nsv_min4tk_[i]->Fill((nsvwmu_4tk[i]+nsvwele_4tk[i] + nsvwmu_min5tk[i] + nsvwele_4tk[i]), w);

    h_svwmu_nsv_min5tk_[i]->Fill(nsvwmu_min5tk[i], w);
    h_svwele_nsv_min5tk_[i]->Fill(nsvwele_min5tk[i], w);
    h_svwlep_nsv_min5tk_[i]->Fill((nsvwmu_min5tk[i]+nsvwele_min5tk[i]), w);
  }
 ////////////////////////////////////////////////////////////////////////////////////////
  //3. Find the best match (reco vtx to gen vtx)
  //GEN COMMENTED OUT 
  // std::pair<int, float> best_gen0_dR{-1, 99.0}; //another pair-- need to know not only the best dR but which sv it is coming from
  // std::pair<int, float> best_gen1_dR{-1, 99.0};
  // std::pair<bool, bool> lepinvertex = {false, false}; // is the lepton in the vertex? --> lep0invtx0, lep1invtx1 
  // std::pair<int, int> idx_lepinvtx = {-1, -1}; // this is the idx of the lepton from the set of leptons associated to the vertexer 
  // int isv = 0;
  // for (const auto& n : isv_dR) {
  //   if (n.first == 0) {
  //     if (n.second < best_gen0_dR.second) {
  //       best_gen0_dR.first = isv;
  //       best_gen0_dR.second = n.second;
  //     }
  //   }
  //   if (n.first == 1) {
  //     if (n.second < best_gen1_dR.second) {
  //       best_gen1_dR.first = isv;
  //       best_gen1_dR.second = n.second;
  //     }
  //   }
  //   isv +=1;
  // }
  // //now we have the best match (i.e. the ivtx for 0 and 1) 
  // // do not consider the possibility that the flavor of the vertex will not be the same flavor of the genmatched lepton flavor. 
  // int ngm_elevtx = 0;
  // int ngm_muvtx = 0;
  // int ngm_tauvtx = 0;
  // if (best_gen0_dR.second < 0.02) {
  //   genmatchedvertex[0].second = best_gen0_dR.first;
  //   if (genmatchedvertex[0].first == "electron") ngm_elevtx +=1;
  //   if (genmatchedvertex[0].first == "muon") ngm_muvtx +=1;
  //   if (genmatchedvertex[0].first == "tau") ngm_tauvtx +=1;
  
  //   //now to see if the lepton is in the vertex 
  //   const MFVVertexAux& aux = auxes->at(best_gen0_dR.first);
  //   bool ilepinvertex = false;
  //   int idx_lep = -1;
  //   if(genmatchedlep[0].first == "electron") {
  //     int eleidx = genmatchedlep[0].second;
  //     if (! (eleidx < 0) ) {
  //       for (int i=0; i < aux.nelectrons; ++i) {
  //         if (mevent->electron_eta[eleidx] == aux.electron_eta[i]) {
  //           if (mevent->electron_phi[eleidx] == aux.electron_phi[i]) {    
  //             ilepinvertex = true;
  //             idx_lep = i;
  //           }
  //         }
  //       }
  //     }
  //   }
  //   if(genmatchedlep[0].first == "muon") {
  //     int muidx = genmatchedlep[0].second;
  //     if (! (muidx < 0)) {
  //       for (int i=0; i < aux.nmuons; ++i) {
  //         if (mevent->muon_eta[muidx] == aux.muon_eta[i]) {
  //           if (mevent->muon_phi[muidx] == aux.muon_phi[i]) {
  //             ilepinvertex = true;
  //             idx_lep = i;
  //           }
  //         }
  //       }
  //     }
  //   }
  //   lepinvertex.first = ilepinvertex; 
  //   idx_lepinvtx.first = idx_lep;
  // }
  // if (best_gen1_dR.second < 0.02) {
  //   genmatchedvertex[1].second = best_gen1_dR.first;
  //   if (genmatchedvertex[1].first == "electron") ngm_elevtx +=1;
  //   if (genmatchedvertex[1].first == "muon") ngm_muvtx +=1;
  //   if (genmatchedvertex[1].first == "tau") ngm_tauvtx +=1;
  
  //   //now to see if the lepton is in the vertex 
  //   const MFVVertexAux& aux = auxes->at(best_gen1_dR.first);
  //   bool ilepinvertex = false;
  //   int idx_lep = -1;
  //   //as long as the electron has been genmatched, check if the electron is in the vertex. 
  //   if(genmatchedlep[1].first == "electron") {
  //     int eleidx = genmatchedlep[1].second;
  //     if (! (eleidx < 0) ) {
  //       for (int i=0; i < aux.nelectrons; ++i) {
  //         if (mevent->electron_eta[eleidx] == aux.electron_eta[i]) {
  //           if (mevent->electron_phi[eleidx] == aux.electron_phi[i]) {    
  //             ilepinvertex = true;
  //             idx_lep = i;
  //           }
  //         }
  //       }
  //     }
  //   }
  //   //as long as the muon has been genmatched, check if the muon is in the vertex. 
  //   if(genmatchedlep[1].first == "muon") {
  //     int muidx = genmatchedlep[1].second;
  //     if (! (muidx < 0) ) { 
  //       for (int i=0; i < aux.nmuons; ++i) {
  //         if (mevent->muon_eta[muidx] == aux.muon_eta[i]) {
  //           if (mevent->muon_phi[muidx] == aux.muon_phi[i]) {
  //             ilepinvertex = true;
  //             idx_lep = i;
  //           }
  //         }
  //       }
  //     }
  //   }
  //   lepinvertex.second = ilepinvertex;
  //   idx_lepinvtx.second = idx_lep;
  // }
  // h_ngenmatched_sv_[0]->Fill(ngm_elevtx + ngm_muvtx + ngm_tauvtx, w);
  // if (ngele > 0)  h_ngenmatched_sv_[1]->Fill(ngm_elevtx, w); //only fill if expect at least 1 ele vtx; (etc)
  // if (ngmu > 0 )  h_ngenmatched_sv_[2]->Fill(ngm_muvtx, w);
  // if (ngtau > 0)  h_ngenmatched_sv_[3]->Fill(ngm_tauvtx, w);


  // //so now we have info on : 
  // // if lepton has been genmatched and to which LLP (0, 1) 
  // // if vertex has been genmatched, which LLP (0,1) and if the corresponding lepton is in the vertex. 
  // //loop over the results from both LLPs (2 genmatched vertices, 2 genmatched leptons)
  // // double pvarr[9] {mevent->pvcxx, mevent->pvcxy, mevent->pvcxz, mevent->pvcxy, mevent->pvcyy, mevent->pvcyz, mevent->pvcxz, mevent->pvcyz, mevent->pvczz};
  // for (int i =0; i < 2; ++i) {
    
  //   int vidx = genmatchedvertex[i].second; // -1 if not matched; 0 - X gives vertex idx 
  //   bool sv_exists = vidx >= 0;
  //   int idx = genmatchedlep[i].second;
  //   bool lep_exists = idx >= 0;
  //   bool lep_invtx = (i < 1) ? lepinvertex.first : lepinvertex.second;
  //   int lepidx_invtx = (i < 1) ? idx_lepinvtx.first : idx_lepinvtx.second;
  //   if (sv_exists) {
  //     const MFVVertexAux& aux = auxes->at(vidx);
  //     // const math::XYZPoint pos_isv(aux.x, aux.y, aux.z);
  //     // double svarr[9] {aux.cxx, aux.cxy, aux.cxz, aux.cxy, aux.cyy, aux.cyz, aux.cxz, aux.cyz, aux.czz};

  //     if (genmatchedlep[i].first == "electron") {
  //       h_lepdau_wvtx_[0]->Fill(lep_exists, w);
  //       if (lep_exists) {
  //         h_lepdau_invtx_[0]->Fill(lep_invtx, w);

  //         // const math::XYZPoint elepos(mevent->electron_x[idx], mevent->electron_y[idx], mevent->electron_z[idx]);
  //         // // const math::XYZTLorentzVector elepos(mevent->electron_pt[i], mevent->electron_eta[i], mevent->electron_phi[w], 0);
  //         // double ele_md= miss_dist(pv, pos_isv, elepos, pvarr, svarr).value();
  //         // double ele_err= miss_dist(pv, pos_isv, elepos, pvarr, svarr).error();
        
  //         if ( lep_invtx ) {
  //           h_lepdau_inSV_pt_[0]->Fill(mevent->electron_pt[idx], w);
  //           h_lepdau_inSV_dxy_[0]->Fill(mevent->electron_dxybs[idx], w);
  //           h_lepdau_inSV_dxyerr_[0]->Fill(mevent->electron_dxyerr[idx], w);
  //           h_lepdau_inSV_nsigmadxy_[0]->Fill(mevent->electron_dxybs[idx] / mevent->electron_dxyerr[idx], w);
  //           //assuming that the index from mevent will not be the same as from aux 
  //           h_lepdau_inSV_missdist_[0]->Fill(aux.elevtxtip[lepidx_invtx], w);
  //           h_lepdau_inSV_missdisterr_[0]->Fill(aux.elevtxtiperr[lepidx_invtx], w);
  //           h_lepdau_inSV_missdistsig_[0]->Fill(aux.elevtxtipsig[lepidx_invtx], w);
  //           h_lepdau_inSV_iso_[0]->Fill(mevent->electron_iso[lepidx_invtx], w);
  //         }
  //         else {
  //           h_lepdau_outSV_pt_[0]->Fill(mevent->electron_pt[idx], w);
  //           h_lepdau_outSV_dxy_[0]->Fill(mevent->electron_dxybs[idx], w);
  //           h_lepdau_outSV_dxyerr_[0]->Fill(mevent->electron_dxyerr[idx], w);
  //           h_lepdau_outSV_nsigmadxy_[0]->Fill(mevent->electron_dxybs[idx] / mevent->electron_dxyerr[idx], w);    
  //           // h_lepdau_outSV_missdist_[0]->Fill(aux.elevtxtip[lepidx_invtx], w);
  //           // h_lepdau_outSV_missdisterr_[0]->Fill(aux.elevtxtiperr[lepidx_invtx], w); 
  //           // h_lepdau_outSV_missdistsig_[0]->Fill(aux.elevtxtipsig[lepidx_invtx], w);
  //           h_lepdau_outSV_iso_[0]->Fill(mevent->electron_iso[idx], w);
  //         }
  //       }
  //     }
  //     if (genmatchedlep[i].first == "muon") {
  //       h_lepdau_wvtx_[1]->Fill(lep_exists, w);
  //       if (lep_exists) {
  //         h_lepdau_invtx_[1]->Fill(lep_invtx, w);

  //         // const math::XYZPoint mupos(mevent->muon_x[idx], mevent->muon_y[idx], mevent->muon_z[idx]);
  //         // // const math::XYZTLorentzVector mupos(mevent->muon_pt[i], mevent->muon_eta[i], mevent->muon_phi[w], 0);
  //         // double mu_md= miss_dist(pv, pos_isv, mupos, pvarr, svarr).value();
  //         // double mu_err= miss_dist(pv, pos_isv, mupos, pvarr, svarr).error();

  //         if ( lep_invtx ) {
  //           h_lepdau_inSV_pt_[1]->Fill(mevent->muon_pt[idx], w);
  //           h_lepdau_inSV_dxy_[1]->Fill(mevent->muon_dxybs[idx], w);
  //           h_lepdau_inSV_dxyerr_[1]->Fill(mevent->muon_dxyerr[idx], w);
  //           h_lepdau_inSV_nsigmadxy_[1]->Fill(mevent->muon_dxybs[idx] / mevent->muon_dxyerr[idx], w);
  //           h_lepdau_inSV_missdist_[1]->Fill(aux.muvtxtip[lepidx_invtx], w);
  //           h_lepdau_inSV_missdisterr_[1]->Fill(aux.muvtxtiperr[lepidx_invtx], w);
  //           h_lepdau_inSV_missdistsig_[1]->Fill(aux.muvtxtipsig[lepidx_invtx], w);
  //           h_lepdau_inSV_iso_[1]->Fill(mevent->muon_iso[idx], w);
  //         }
  //         else {
  //           h_lepdau_outSV_pt_[1]->Fill(mevent->muon_pt[idx], w);
  //           h_lepdau_outSV_dxy_[1]->Fill(mevent->muon_dxybs[idx], w);
  //           h_lepdau_outSV_dxyerr_[1]->Fill(mevent->muon_dxyerr[idx], w);
  //           h_lepdau_outSV_nsigmadxy_[1]->Fill(mevent->muon_dxybs[idx] / mevent->muon_dxyerr[idx], w);  
  //           //of course can't use these for leptons not found in the vertex... have to get the track somehow 
  //           // h_lepdau_outSV_missdist_[1]->Fill(aux.muvtxtip[lepidx_invtx], w);
  //           // h_lepdau_outSV_missdisterr_[1]->Fill(aux.muvtxtiperr[lepidx_invtx], w);   
  //           // h_lepdau_outSV_missdistsig_[1]->Fill(aux.muvtxtipsig[lepidx_invtx], w);
  //           h_lepdau_outSV_iso_[1]->Fill(mevent->muon_iso[idx], w);
  //         }
  //       }
  //     }
  //   }
  //   if (!sv_exists) {
  //     if (genmatchedlep[i].first == "electron") h_lepdau_novtx_[0]->Fill(lep_exists, w);
  //     if (genmatchedlep[i].first == "muon") h_lepdau_novtx_[1]->Fill(lep_exists, w);
  //   }
  // }

  // if (nsv >= 2) {
  //   const MFVVertexAux& sv0 = auxes->at(0);
  //   const MFVVertexAux& sv1 = auxes->at(1);
  //   h_sv_ntk0_ntk1->Fill(sv0.ntracks(), sv1.ntracks(), w);
  //   double svdist2d = mag(sv0.x - sv1.x, sv0.y - sv1.y);
  //   double svdist3d = mag(sv0.x - sv1.x, sv0.y - sv1.y, sv0.z - sv1.z);
  //   double bs3ddist0 = mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z), (float)(sv0.z-bsz));
  //   double bs3ddist1 = mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z), (float)(sv1.z-bsz));
  //   h_svdist2d->Fill(svdist2d, w);
  //   h_svdist3d->Fill(svdist3d, w);
  //   h_sum_bsbs2ddist->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)) + mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
	
	//   double sum_bsbs2ddist = mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)) + mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z));

	//   if (sum_bsbs2ddist < 0.04) {
	// 	  h_sum_bsbs2ddist_lt_400um->Fill(0.0, w);
  //     if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_lt_400um->Fill(1.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_lt_400um->Fill(2.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //       h_sum_bsbs2ddist_lt_400um->Fill(3.0, w);
  //     }
  //     //GEN COMMENTED OUT 
  //     // if (sv0.gen3ddist < 0.008) {
  //     // 	h_lt_400um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_lt_400um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_lt_400um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_lt_400um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }
  //     // if (sv1.gen3ddist < 0.008) {
  //     // 	h_lt_400um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_lt_400um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_lt_400um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_lt_400um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }

  //   }
  //   else if (sum_bsbs2ddist > 0.04 && sum_bsbs2ddist < 0.07) {
  //     h_sum_bsbs2ddist_gt_400um_lt_700um->Fill(0.0, w);
  //     if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_gt_400um_lt_700um->Fill(1.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_gt_400um_lt_700um->Fill(2.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //       h_sum_bsbs2ddist_gt_400um_lt_700um->Fill(3.0, w);
  //     }
  //     //GEN COMMENTED OUT 
  //     // if (sv0.gen3ddist < 0.008) {
  //     // 	h_gt_400um_lt_700um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }
  //     // if (sv1.gen3ddist < 0.008) {
  //     // 	h_gt_400um_lt_700um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_gt_400um_lt_700um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }
  //   }
  //   else {
  //     h_sum_bsbs2ddist_gt_700um->Fill(0.0, w);
  //     if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_gt_700um->Fill(1.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //       h_sum_bsbs2ddist_gt_700um->Fill(2.0, w);
  //     }
  //     if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //       h_sum_bsbs2ddist_gt_700um->Fill(3.0, w);
  //     }

  //     //GEN COMMENTED OUT 
  //     // if (sv0.gen3ddist < 0.008) {
  //     // 	h_gt_700um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_gt_700um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_gt_700um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_gt_700um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }
  //     // if (sv1.gen3ddist < 0.008) {
  //     // 	h_gt_700um_llp_res80um->Fill(0.0, w);
  //     // 	if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4) {
  //     // 		h_gt_700um_llp_res80um->Fill(1.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     // 		h_gt_700um_llp_res80um->Fill(2.0, w);
  //     // 	}
  //     // 	if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     // 		h_gt_700um_llp_res80um->Fill(3.0, w);
  //     // 	}
  //     // }

  //   }

  //   if (sv0.ntracks() >= 4 && sv1.ntracks() >= 4){
  //     h_sum_bsbs2ddist_atleast_4x4->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)) + mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //     h_rescaled_bsbs2ddist_atleast_4x4->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)));
  //     h_rescaled_bsbs2ddist_atleast_4x4->Fill(mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //   }

  //   if (sv0.ntracks() >= 5 && sv1.ntracks() >= 4) {
  //     h_sum_bsbs2ddist_atleast_4x5->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)) + mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //     h_rescaled_bsbs2ddist_atleast_4x5->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)));
  //     h_rescaled_bsbs2ddist_atleast_4x5->Fill(mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //   }

  //   if (sv0.ntracks() >= 5 && sv1.ntracks() >= 5) {
  //     h_sum_bsbs2ddist_atleast_5x5->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)) + mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //     h_rescaled_bsbs2ddist_atleast_5x5->Fill(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)));
  //     h_rescaled_bsbs2ddist_atleast_5x5->Fill(mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z)));
  //   }

    
  //   h_sum_bs3ddist->Fill(bs3ddist0 + bs3ddist1);
  //   h_sqsum_bsbs2ddist->Fill(hypot(mag(sv0.x - mevent->bsx_at_z(sv0.z), sv0.y - mevent->bsy_at_z(sv0.z)), mag(sv1.x - mevent->bsx_at_z(sv1.z), sv1.y - mevent->bsy_at_z(sv1.z))));
  //   h_sv0pvdz_v_sv1pvdz->Fill(sv0.pvdz(), sv1.pvdz(), w);
  //   h_sv0pvdzsig_v_sv1pvdzsig->Fill(sv0.pvdzsig(), sv1.pvdzsig(), w);
  //   double phi0 = atan2(sv0.y - bsy, sv0.x - bsx);
  //   double phi1 = atan2(sv1.y - bsy, sv1.x - bsx);
  //   h_absdeltaphi01->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);

  //   h_fractrackssharedwpv01 ->Fill(float(sv0.ntrackssharedwpv () + sv1.ntrackssharedwpv ())/(sv0.ntracks() + sv1.ntracks()), w);
  //   h_fractrackssharedwpvs01->Fill(float(sv0.ntrackssharedwpvs() + sv1.ntrackssharedwpvs())/(sv0.ntracks() + sv1.ntracks()), w);
  //   h_pvmosttracksshared->Fill(sv0.ntrackssharedwpvs() ? sv0.pvmosttracksshared() : -1,
  //                               sv1.ntrackssharedwpvs() ? sv1.pvmosttracksshared() : -1,
  //                               w);

  //   std::vector<std::vector<int> > sv_track_which_jet;
  //   for (int isv = 0; isv < nsv; ++isv) {
  //     const MFVVertexAux& aux = auxes->at(isv);
  //     const int ntracks = aux.ntracks();

  //     std::vector<int> track_which_jet;
  //     for (int i = 0; i < ntracks; ++i) {
  //       double match_threshold = 1.3;
  //       int jet_index = 255;
  //       for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
  //         double a = fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
  //         double b = fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) + 1;
  //         double c = fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) + 1;
  //         if (a * b * c < match_threshold) {
  //           match_threshold = a * b * c;
  //           jet_index = mevent->jet_track_which_jet[j];
  //         }
  //       }
  //       if (jet_index != 255) {
  //         track_which_jet.push_back((int) jet_index);
  //       }
  //     }
  //     sv_track_which_jet.push_back(track_which_jet);
  //   }

  //   bool shared_jet = std::find_first_of (sv_track_which_jet[0].begin(), sv_track_which_jet[0].end(), sv_track_which_jet[1].begin(), sv_track_which_jet[1].end()) != sv_track_which_jet[0].end();
  //   h_sv_shared_jets->Fill(shared_jet, w);
  //   if (shared_jet) {
  //     h_svdist2d_shared_jets->Fill(svdist2d, w);
  //     h_absdeltaphi01_shared_jets->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);
  //   } else {
  //     h_svdist2d_no_shared_jets->Fill(svdist2d, w);
  //     h_absdeltaphi01_no_shared_jets->Fill(fabs(reco::deltaPhi(phi0, phi1)), w);
  //   }

  //   std::vector<double> vec_sv0_nsigmadxy = {};
  //   std::vector<double> vec_sv0_dxy = {};
  //   for (int i = 0; i < sv0.ntracks(); ++i) {
  //     vec_sv0_nsigmadxy.push_back(fabs(sv0.track_dxy[i] / sv0.track_dxy_err(i)));
  //     vec_sv0_dxy.push_back(sv0.track_dxy[i]);
  //   }
  //   sort(vec_sv0_nsigmadxy.begin(), vec_sv0_nsigmadxy.end());
  //   sort(vec_sv0_dxy.begin(), vec_sv0_dxy.end());
  //   if (sv0.ntracks() >= 3){
  //     h_sv0_first_large_nsigmadxy_bsp->Fill(vec_sv0_nsigmadxy[vec_sv0_nsigmadxy.size()-1], w);
  //     h_sv0_second_large_nsigmadxy_bsp->Fill(vec_sv0_nsigmadxy[vec_sv0_nsigmadxy.size()-2], w);
  //     h_sv0_third_large_nsigmadxy_bsp->Fill(vec_sv0_nsigmadxy[vec_sv0_nsigmadxy.size()-3], w);
  //     h_sv0_first_large_dxy_bsp->Fill(vec_sv0_dxy[vec_sv0_dxy.size()-1], w);
  //     h_sv0_second_large_dxy_bsp->Fill(vec_sv0_dxy[vec_sv0_dxy.size()-2], w);
  //     h_sv0_third_large_dxy_bsp->Fill(vec_sv0_dxy[vec_sv0_dxy.size()-3], w);
  //     if (sv0.ntracks() % 2 == 0) {
  //       h_sv0_med_nsigmadxy_bsp->Fill((vec_sv0_nsigmadxy[sv0.ntracks()/2] + vec_sv0_nsigmadxy[(sv0.ntracks()/2)-1])/2, w);
  //       h_sv0_med_dxy_bsp->Fill((vec_sv0_dxy[sv0.ntracks()/2] + vec_sv0_dxy[(sv0.ntracks()/2) - 1])/2, w);
  //     }  
  //     else {
  //       h_sv0_med_nsigmadxy_bsp->Fill(vec_sv0_nsigmadxy[(sv0.ntracks()-1)/2], w);
  //       h_sv0_med_dxy_bsp->Fill(vec_sv0_dxy[(sv0.ntracks()-1)/2], w);
  //     }
  //   }

  //   std::vector<double> vec_sv1_nsigmadxy = {};
  //   std::vector<double> vec_sv1_dxy = {};
  //   for (int i = 0; i < sv1.ntracks(); ++i) {
  //     vec_sv1_nsigmadxy.push_back(fabs(sv1.track_dxy[i] / sv1.track_dxy_err(i)));
  //     vec_sv1_dxy.push_back(sv1.track_dxy[i]);
  //   }
  //   sort(vec_sv1_nsigmadxy.begin(), vec_sv1_nsigmadxy.end());
  //   sort(vec_sv1_dxy.begin(), vec_sv1_dxy.end());

  //   if (sv1.ntracks() >= 3){
  //     h_sv1_first_large_nsigmadxy_bsp->Fill(vec_sv1_nsigmadxy[vec_sv1_nsigmadxy.size() - 1], w);
  //     h_sv1_second_large_nsigmadxy_bsp->Fill(vec_sv1_nsigmadxy[vec_sv1_nsigmadxy.size() - 2], w);
  //     h_sv1_third_large_nsigmadxy_bsp->Fill(vec_sv1_nsigmadxy[vec_sv1_nsigmadxy.size() - 3], w);
  //     h_sv1_first_large_dxy_bsp->Fill(vec_sv1_dxy[vec_sv1_dxy.size() - 1], w);
  //     h_sv1_second_large_dxy_bsp->Fill(vec_sv1_dxy[vec_sv1_dxy.size() - 2], w);
  //     h_sv1_third_large_dxy_bsp->Fill(vec_sv1_dxy[vec_sv1_dxy.size() - 3], w);
  //     if (sv1.ntracks() % 2 == 0) {
  //       h_sv1_med_nsigmadxy_bsp->Fill((vec_sv1_nsigmadxy[sv1.ntracks() / 2] + vec_sv1_nsigmadxy[(sv1.ntracks() / 2) - 1]) / 2, w);
  //       h_sv1_med_dxy_bsp->Fill((vec_sv1_dxy[sv1.ntracks() / 2] + vec_sv1_dxy[(sv1.ntracks() / 2) - 1]) / 2, w);
  //     }  
  //     else {
  //       h_sv1_med_nsigmadxy_bsp->Fill(vec_sv1_nsigmadxy[(sv1.ntracks() - 1) / 2], w);
  //       h_sv1_med_dxy_bsp->Fill(vec_sv1_dxy[(sv1.ntracks() - 1) / 2], w);
  //     }  
  //   }

  // }

  // number of jets associated with SVs 
  // and leptons 
  for (int isv = 0; isv < nsv; ++isv) {
    if (leading_sel_leppt[isv] < 0) continue; //only loop over sv that have sel leptons 
    const MFVVertexAux& aux = auxes->at(isv);
    const int ntracks = aux.ntracks();

    const math::XYZPoint pv2sv(aux.x-mevent->pvx, aux.y-mevent->pvy,aux.z-mevent->pvz);
    std::set<int> sv_jetasso;
    unsigned int njettrack = 0;

    std::vector<std::set<int>> sv_bjetasso(3);
    std::vector<unsigned int> nbtrack = {0,0,0};
    std::vector<unsigned int> nbtrack_notlep = {0,0,0}; //btracks not leptons

    //these are leptons passing id, iso 
    // std::vector<unsigned int> nele_notfromb = {0,0,0};
    // std::vector<unsigned int> nmu_notfromb = {0,0,0};
    unsigned int nele_notfromb = 0;
    unsigned int nmu_notfromb = 0;

    std::vector<unsigned int> nele_fromb = {0,0,0};
    std::vector<unsigned int> nmu_fromb = {0,0,0};

    //loop over tracks in SV
    for (int i = 0; i < ntracks; ++i) {

      //these reset every time so checking a) if the track is a lepton, and b) what type of lepton and c) what cuts it passes
      bool is_lepmatched = false;
      bool is_mu = false;
      bool is_ele = false;
      bool is_bjetmatched = false;

      if (lep_tracks[isv][i] != "other") is_lepmatched = true;
      if (lep_tracks[isv][i] == "ele") is_ele = true;
      if (lep_tracks[isv][i] == "mu") is_mu = true;

      //getting the number of btracks 
	    double match_threshold = 1.3;
	    int jet_index = 255;
	    for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
	      double a = fabs(aux.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
	      double b = fabs(aux.track_eta[i] - mevent->jet_track_eta[j]) + 1;
	      double c = fabs(aux.track_phi[i] - mevent->jet_track_phi[j]) + 1;
	      if (a * b * c < match_threshold) {
	        match_threshold = a * b * c;
	        jet_index = mevent->jet_track_which_jet[j];
	      }
	    }
	    if (jet_index != 255) {
        sv_jetasso.insert((int) jet_index);
        ++njettrack;
  
        //now checking of those matched jets, which one is btagged
        for(int ibdisc=0; ibdisc<3; ++ibdisc){
          if (mevent->is_btagged(jet_index, ibdisc)){
            sv_bjetasso[ibdisc].insert((int) jet_index);
            ++nbtrack[ibdisc];
            is_bjetmatched = true;
            if (!is_lepmatched) ++nbtrack_notlep[ibdisc];
            else {
              // these tracks are both lepton matched and in the bjet
              if (is_mu) ++nmu_fromb[ibdisc];
              else if (is_ele) ++nele_fromb[ibdisc];
            }
          }
        }
      }
      if (!is_bjetmatched) { //this will mean that the track was not found in the bjet - loose, med, tight
        if (is_lepmatched) {
          if (is_mu) ++nmu_notfromb;
          else if (is_ele) ++nele_notfromb;
        }
      }
	  }

    h_sv_ntk_njet->Fill(ntracks, sv_jetasso.size(), w);
    h_sv_ntkfromjets->Fill(njettrack, w);
    
    
    //math::XYZVector pv2sv;
    //pv2sv.SetXYZ(aux.x-mevent->pvx, aux.y-mevent->pvy,aux.z-mevent->pvz);
    for(int ibdisc=0; ibdisc<3; ++ibdisc){


      h_sv_nbtags[ibdisc]->Fill(sv_bjetasso[ibdisc].size(), w);
      h_sv_nbtks[ibdisc]->Fill(nbtrack[ibdisc], w);
      h_sv_nbtks_notlep[ibdisc]->Fill(nbtrack_notlep[ibdisc],w);
      h_sv_nlep_nbtks[ibdisc]->Fill(nbtrack[ibdisc] + aux.nleptons, w); //TOFIX

      //repeat but now separated by ele, mu 
      if (leading_sel_leptype[isv]){
        h_svmu_nbtags[ibdisc]->Fill(sv_bjetasso[ibdisc].size(), w);
        h_svmu_nbtks[ibdisc]->Fill(nbtrack[ibdisc], w);
        h_svmu_nbtks_notlep[ibdisc]->Fill(nbtrack_notlep[ibdisc],w);
      }
      if (!leading_sel_leptype[isv]) {
        h_svele_nbtags[ibdisc]->Fill(sv_bjetasso[ibdisc].size(), w);
        h_svele_nbtks[ibdisc]->Fill(nbtrack[ibdisc], w);
        h_svele_nbtks_notlep[ibdisc]->Fill(nbtrack_notlep[ibdisc],w);
      }
      //notice : something is still not quite right with bjet + lep track logic... 
      // if ( (nbtrack_notlep[ibdisc] == nbtrack[ibdisc]) && (nbtrack[ibdisc] > 0) ) { //means that all btracks are not sel lepton tracks 
      //   h_sv_nlepbtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nele_notfromb + nmu_notfromb, w);
      //   h_sv_nmubtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nmu_notfromb, w);
      //   h_sv_nelebtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nele_notfromb, w);

      //   h_sv_nlep_notb[ibdisc]->Fill(nele_notfromb + nmu_notfromb, w);
      //   h_sv_nele_notb[ibdisc]->Fill(nele_notfromb, w);
      //   h_sv_nmu_notb[ibdisc]->Fill(nmu_notfromb, w);
      // }


      // if ( (nbtrack[ibdisc] - nbtrack_notlep[ibdisc] > 0) && nbtrack_notlep[ibdisc] > 0) { //means that there is at least 1 track in the bjet that is a sel lepton; and there should be a lepton...
      //   h_sv_nleptks_nbtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nele_fromb[ibdisc] + nmu_fromb[ibdisc], w);
      //   h_sv_nmutks_nbtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nmu_fromb[ibdisc], w);
      //   h_sv_neletks_nbtks[ibdisc]->Fill(nbtrack_notlep[ibdisc] + nele_fromb[ibdisc], w);

      //   h_sv_nlep_fromb[ibdisc]->Fill(nele_fromb[ibdisc] + nmu_fromb[ibdisc], w);
      //   h_sv_nele_fromb[ibdisc]->Fill(nele_fromb[ibdisc], w);
      //   h_sv_nmu_fromb[ibdisc]->Fill(nmu_fromb[ibdisc], w);
      // }

      // if (nbtrack[ibdisc] ==0) { //means that did not find any tracks from bjets so by default, the lepton will not be from b
      //   h_sv_nlep_notbnob[ibdisc]->Fill(nele_notfromb + nmu_notfromb, w);
      //   h_sv_nele_notbnob[ibdisc]->Fill(nele_notfromb, w);
      //   h_sv_nmu_notbnob[ibdisc]->Fill(nmu_notfromb, w);
      // }
      h_sv_nallbtags->Fill(sv_bjetasso[0].size(), sv_bjetasso[1].size(), sv_bjetasso[2].size(), w);
      h_sv_nallbtks->Fill(nbtrack[0], nbtrack[1], nbtrack[2], w);

    

      double mindphi_svbjet = 999;
      double mindr_svbjet = 999;

      double mindphi_lepbjet = 999;
      double mindr_lepbjet = 999;
      float min_bjet_pt = -1.0;

      double maxdphi_lepbjet = -1.0;
      double maxdr_lepbjet = -1.0;
      float max_bjet_pt = -1.0;

      for(auto &ib:sv_bjetasso[ibdisc]){
        double idphi = fabs(reco::deltaPhi(pv2sv.phi(),mevent->nth_jet_phi(ib)));
        double idr = reco::deltaR(pv2sv.eta(), pv2sv.phi(), mevent->nth_jet_eta(ib), mevent->nth_jet_phi(ib));
        if(idr<mindr_svbjet){
          mindr_svbjet = idr;
          mindphi_svbjet = idphi;
        }
        if (leading_sel_leppt[isv] > 0) { 
          double idphi_lep = fabs(reco::deltaPhi(leading_sel_lepphi[isv], mevent->nth_jet_phi(ib)));
          double idr_lep = reco::deltaR(leading_sel_lepeta[isv], leading_sel_lepphi[isv], mevent->nth_jet_eta(ib), mevent->nth_jet_phi(ib));
          if(idr_lep<mindr_lepbjet){
            mindr_lepbjet = idr_lep;
            mindphi_lepbjet = idphi_lep;
            min_bjet_pt = mevent->nth_jet_pt(ib);
          }
          if(idr_lep>maxdr_lepbjet){
            maxdr_lepbjet = idr_lep;
            maxdphi_lepbjet = idphi_lep;
            max_bjet_pt = mevent->nth_jet_pt(ib);
          }
        }
        
      }
      if((mindr_svbjet!=999)&&(mindphi_svbjet!=999)){
        h_sv_mindeltaphi_svbjet[ibdisc]->Fill(mindphi_svbjet, w);
        h_sv_mindeltar_sv_bjet[ibdisc]->Fill(mindr_svbjet, w);
      }
      if((mindr_lepbjet!=999)&&(mindphi_lepbjet!=999)){
        h_sv_mindeltaphi_lepbjet[ibdisc]->Fill(mindphi_lepbjet, w);
        h_sv_mindeltar_lep_bjet[ibdisc]->Fill(mindr_lepbjet, w);
        h_sv_mindr_ptratio_lep_bjet[ibdisc]->Fill(leading_sel_leppt[isv]/min_bjet_pt, w);
      }
      if((maxdr_lepbjet!=-1)&&(maxdphi_lepbjet!=-1)){
        h_sv_maxdeltaphi_lepbjet[ibdisc]->Fill(maxdphi_lepbjet, w);
        h_sv_maxdeltar_lep_bjet[ibdisc]->Fill(maxdr_lepbjet, w);
        h_sv_maxdr_ptratio_lep_bjet[ibdisc]->Fill(leading_sel_leppt[isv]/max_bjet_pt, w);
      }
    }
  } 
}

//splitting up the satisfieslep trigger into muon/ele trigger -> just checking if the electron or muon passes pT requirement given which trigger fired -> this is for the muons and electrons in the SV 
bool MFVVertexHistos::satisfiesLepTriggerPT(edm::Handle<MFVEvent> mevent, edm::Handle<MFVVertexAuxCollection> auxes, int it, int isv, size_t trig, const edm::EventSetup& setup) { 
  if(!mevent->pass_hlt(trig)) return false;
  
  const MFVVertexAux& aux = auxes->at(isv);

  int year = int(MFVNEUTRALINO_YEAR);
  assert(year == 20161 || year == 20162 || year == 2017 || year == 2018); // in case of race conditions where the compiled macro is invalid...

  // int nmuons     = mevent->nmuons();
  // int nelectrons = mevent->nelectrons();
  int njets      = mevent->njets(20);
    
  bool passed_kinematics = false;

  switch(trig){
  case mfv::b_HLT_Ele27_WPTight_Gsf : //for 2016
    {
    if (year != 20161 and year !=20162) return false;
    if (aux.electron_pt[it] > 30) passed_kinematics = true; //for 2016
    return passed_kinematics;
    }
  case mfv::b_HLT_Ele35_WPTight_Gsf : //for 2017
    {
    if (year != 2017) return false;
    if (aux.electron_pt[it] > 38) passed_kinematics = true; //for 2017
    return passed_kinematics;
  }
  case mfv::b_HLT_Ele32_WPTight_Gsf : //for 2018
    {
    if (year != 2018) return false;
    if (aux.electron_pt[it] > 35) passed_kinematics = true; //for 2018
    return passed_kinematics;
  }

  case mfv::b_HLT_IsoMu27 : //for 2017
    {
    if (year != 2017) return false;
    if (aux.muon_pt[it] > 30) passed_kinematics = true; 
    return passed_kinematics;
  }
  case mfv::b_HLT_IsoMu24 : //for 2018, 2016
    {
      if (year == 2017) return false;
      if (aux.muon_pt[it] > 27) passed_kinematics = true;
      return passed_kinematics;
    }
  
  case mfv::b_HLT_Mu50 :
    {
    if (aux.muon_pt[it] > 53) passed_kinematics = true;
    return passed_kinematics;
    }
    
  case mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT :
    {
    if (aux.electron_pt[it] > 120) passed_kinematics = true;
    return passed_kinematics;
    }
    
  case  mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165 :
    {
    if (aux.electron_pt[it] > 55) {
      for(int j0=0; j0 < njets; ++j0){
        if (!jet_hlt_match(mevent, j0) || mevent->jet_pt[j0] < 170) continue; //just looking for a jet in the event
        passed_kinematics = true;
      }
    }
    return passed_kinematics;
    }
  case mfv::b_HLT_Photon175 : //for  2016 
    {
      if (year != 20161 and year != 20162) return false;
      if (aux.electron_pt[it] > 180) passed_kinematics = true; 
      return passed_kinematics;
    }
  case mfv::b_HLT_Photon200 : //for 2018, 2017
    {
      if (year != 2018 and year != 2017) return false;
      if (aux.electron_pt[it] > 205) passed_kinematics = true;
      return passed_kinematics;
    }
  default :
    {
      throw std::invalid_argument(std::string(mfv::hlt_paths[trig]) + " not implemented in satisfiesLepTrigger");
    }
  }

  return false;

}

DEFINE_FWK_MODULE(MFVVertexHistos);
