#ifndef JMTucker_MFVNeutralino_interface_MiniNtupleBDT_h
#define JMTucker_MFVNeutralino_interface_MiniNtupleBDT_h

#include "Math/SMatrix.h"
#include "TLorentzVector.h"
#include "TTree.h"

#define JMT_STANDALONE_BTAGGING
#include "JMTucker/Tools/interface/BTagging.h"

namespace mfv {
  typedef ROOT::Math::SMatrix<double, 5, 5, ROOT::Math::MatRepSym<double, 5> >  TrackCovarianceMatrix;

  struct MiniNtupleBDT {
    MiniNtupleBDT();
    void clear();

    unsigned run;
    unsigned lumi;
    unsigned long long event;
    unsigned char gen_flavor_code;
    unsigned int pass_hlt;
    float l1_htt;
    float l1_myhtt;
    float l1_myhttwbug;
    float hlt_ht;

    float bsx;
    float bsy;
    float bsz;
    float bsdxdz;
    float bsdydz;
    float bsx_at_z(float z) const { return bsx + bsdxdz * (z - bsz); }
    float bsy_at_z(float z) const { return bsy + bsdydz * (z - bsz); }
    unsigned char npv;
    float pvx;
    float pvy;
    float pvz;
    unsigned char npu;
    float weight;
    unsigned char nvtx;
    
    unsigned char njets;
    float jet_pt[50];
    float jet_eta[50];
    float jet_phi[50];
    float jet_energy[50];
    float jet0_pt;
    float jet1_pt;
    float jetht;
    float jet_hlt_pt[50];

    unsigned char nelectrons;
    float electron_pt[50];
    float electron_eta[50];
    float electron_phi[50];
    float electron_sigmadxy[50];

    unsigned char nmuons;
    float muon_pt[50];
    float muon_eta[50];
    float muon_phi[50];
    float muon_sigmadxy[50];

    unsigned char nleptons;

    float leading_lep_pt;
    float leading_lep_dxy;
    float leading_lep_dxyerr;
    float leading_lep_sigmadxy;
    float leading_jetlep_pt;
    float subleading_lep_pt;
    float subleading_lep_dxy;
    float subleading_lep_dxyerr;
    float subleading_lep_sigmadxy;
    float double_jetlep_pt;

    float max_lep_sv_2ddist;
    float max_lep_sv_dphi;
    float max_lep_sv_dphi_2;

    float gen_x[2];
    float gen_y[2];
    float gen_z[2];
    float gen_lsp_pt[2];
    float gen_lsp_eta[2];
    float gen_lsp_phi[2];
    float gen_lsp_mass[2];
    std::vector<TLorentzVector> gen_daughters;
    std::vector<int> gen_daughter_id;
    std::vector<TLorentzVector> gen_leptons;
    std::vector<TLorentzVector>* p_gen_daughters;
    std::vector<int>* p_gen_daughter_id;
    std::vector<TLorentzVector>* p_gen_leptons;

    // std::vector<float> trackmass;
    // std::vector<float> trackpt;
    // std::vector<float> trackpterr;
    // std::vector<float> tracketa;
    // std::vector<float> tracketaerr;
    // std::vector<float> trackphi;
    // std::vector<float> trackphierr;
    // std::vector<float> tracknsigmadxybs;
    // std::vector<float> trackdxy;
    // std::vector<float> trackdxyerr;
    // std::vector<float> trackdz;
    // std::vector<float> trackdzerr;
    // std::vector<float> tracknsigmadz;
    // // std::vector<float> trackabsnsigmadz;
    // std::vector<float> trackchi2ndof;
    // std::vector<float> track_injet;

    std::vector<int> ntracks;
    std::vector<int> ntrackssharedwpv;
    std::vector<int> ntrackssharedwpvs;
    std::vector<int> ntracksetagt1p5;
    std::vector<int> nmu_inSV;
    std::vector<int> nele_inSV;
    std::vector<int> nlep_inSV;
    std::vector<int> nselmu_inSV;
    std::vector<int> nselele_inSV;
    std::vector<float> all_elept_inSV;
    std::vector<float> all_mupt_inSV;
    std::vector<float> all_leppt_inSV;
    std::vector<float> leading_elept_inSV;
    std::vector<float> leading_mupt_inSV;
    std::vector<float> leading_leppt_inSV;
    std::vector<float> leading_leptype_inSV;
    std::vector<float> leading_lepiso_inSV;
    std::vector<float> leading_lepID_inSV;
    std::vector<float> leading_lepnsigmadxy_inSV;
    std::vector<float> leading_lepnsigmadxy_rescaled_inSV;
    std::vector<float> leading_lepdxy_inSV;
    std::vector<float> leading_lepdxyerr_inSV;
    std::vector<float> leading_lepeta_inSV;
    std::vector<float> leading_lepphi_inSV;
    std::vector<float> leading_lephltmatched_inSV;
    std::vector<float> leading_leppasstrigpt_inSV;
    std::vector<float> closestdR_track_leadinglep;
    std::vector<float> avgptnolep;
    // std::vector<float> max_lep_sv_2ddist;
    // std::vector<float> max_lep_sv_dphi;
    // std::vector<float> max_lep_sv_dphi_2;

    std::vector<float> leading_jetpt_inSV;
    std::vector<float> leading_lepjet_pairdr;
    
    std::vector<float> nbtags_loose; //
    std::vector<float> nbtags_med; //
    std::vector<float> nbtags_tight; //

    std::vector<float> nbtks_loose;
    std::vector<float> nbtks_med;
    std::vector<float> nbtks_tight;

    std::vector<float> maxtrackpt;
    std::vector<float> avgpt;
    std::vector<float> sumptx;
    std::vector<float> sumpty;
    std::vector<float> sumptz;
    std::vector<float> sumpt2;
    std::vector<float> x;
    std::vector<float> y;
    std::vector<float> z;
    std::vector<float> sv_eta;
    std::vector<float> sv_phi;
    std::vector<float> bs2derr;
    std::vector<float> bsbs2ddist;
    std::vector<float> rescale_bs2derr;
    std::vector<float> rescale_bs2ddist;
    std::vector<float> pvdz;
    std::vector<float> pvdzerr;
    std::vector<float> chi2;
    std::vector<float> ndof;
    std::vector<float> chi2dof;

    std::vector<float> tracketaavg;
    std::vector<float> trackphiavg;
    std::vector<float> nmleptracketaavg; //all tracks except lepton
    std::vector<float> nmleptrackphiavg;
    std::vector<float> dr_avgtracks_lep;
    
    std::vector<float> trackpairdravg;
    std::vector<float> trackpairdrmax;
    std::vector<float> trackpairdrmin;
    std::vector<float> trackpairdetaavg;
    std::vector<float> trackpairdetamax;
    std::vector<float> trackpairdetamin;
    std::vector<float> trackpairdphiavg;
    std::vector<float> trackpairdphimax;
    std::vector<float> trackpairdphimin;
    std::vector<float> tracktripmassavg;
    std::vector<float> tracktripmassmax;
    std::vector<float> tracktripmassmin;
    std::vector<float> trackdxynsigmaavg;
    std::vector<float> trackdxynsigmamax;
    std::vector<float> trackdxynsigmamin;
    std::vector<float> trackdxynsigmarms;
    std::vector<float> sum_trackdxynsigma;

    std::vector<float> trackptmin;
    std::vector<float> trackptmax;
    std::vector<float> trackptavg;
    std::vector<float> trackptrms;
    std::vector<float> trackpairdptmin;
    std::vector<float> trackpairdptmax;
    std::vector<float> trackpairdptavg;
    std::vector<float> trackpairdptrms;

    std::vector<float> costhmombs;
    std::vector<float> costhtksjetsntkmombs;
    std::vector<float> ntracksptgt10;
    // std::vector<float> jetsntkpt;
    // std::vector<float> tksjetsntkpt;
    std::vector<float> tksjetsntkmass;
    std::vector<float> costhtkmomvtxdispmin;
    std::vector<float> costhtkmomvtxdispmax;
    std::vector<float> costhtkmomvtxdispavg;
    std::vector<float> costhjetmomvtxdispmin;
    std::vector<float> costhjetmomvtxdispmax;
    std::vector<float> costhjetmomvtxdispavg;
    std::vector<float> alljetsvdeltaphi;
    std::vector<float> minjetsvdeltaphi;
    std::vector<float> maxjetsvdeltaphi;
    std::vector<float> avgjetsvdeltaphi;

    bool satisfiesTrigger(size_t trig) const;

  };

  void write_to_tree(TTree* tree, MiniNtupleBDT& nt);
  void read_from_tree(TTree* tree, MiniNtupleBDT& nt);
  MiniNtupleBDT* clone(const MiniNtupleBDT& nt);
  long long loop(const char* fn, const char* tree_path, bool (*)(long long, long long, const mfv::MiniNtupleBDT&));
}

#endif
