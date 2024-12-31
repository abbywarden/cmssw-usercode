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
#include "JMTucker/Tools/interface/Geometry.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/EventTools.h"
#include "JMTucker/Tools/interface/Year.h"

class MFVCutFlowHistos : public edm::EDAnalyzer {
 public:
  explicit MFVCutFlowHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
   
 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_aux_token;
  const edm::EDGetTokenT<double> weight_token;
  std::pair<bool, std::string> satisfiesLepTrigger(edm::Handle<MFVEvent>, size_t);

  TH1F* h_w;
  TH1F* h_nsv;
  
// first one : lepton selections -> then trigger -> then all vtx selections
// second : all vtx selections -> then trigger & lepton selections 
// note : the leptons in the vertex don't have to pass the cuts, just a lepton in the event 
  // enum {einsv, einsv_pt, einsv_id, einsv_eta, einsv_iso, einsv_trigger, einsv_fullvtx};
  // TH1D* h_e_lepvtx_cutflow;

  // enum {einsv2, einsv_mintrack, einsv_mindbv, einsv_maxdbvunc, einsv_trigger2, einsv_fullsel};
  // TH1D* h_e_vtxlep_cutflow;

  // enum {minsv, minsv_pt, minsv_id, minsv_eta, minsv_iso, minsv_trigger, minsv_fullvtx};
  // TH1D* h_m_lepvtx_cutflow;

  // enum {minsv2, minsv_mintrack, minsv_mindbv, minsv_maxdbvunc, minsv_trigger2, minsv_fullsel};
  // TH1D* h_m_vtxlep_cutflow;

//vertices that should have a lepton but do not (i.e. vertex is reconstructed, lepton is reconstructed but no match btwn the two)
  // enum {e_atleast_1vtx, e_pass_mintrack, e_pass_mindbv, e_pass_maxdbv_unc};
  // TH1D* h_evertex_cutflow;

  // enum {m_atleast_1vtx, m_pass_mintrack, m_pass_mindbv, m_pass_maxdbv_unc};
  // TH1D* h_mvertex_cutflow;

  // enum {e_atleast_1vtx_at, e_pass_mintrack_at, e_pass_mindbv_at, e_pass_maxdbv_unc_at};
  // TH1D* h_evtx_at_cutflow;

  // enum {m_atleast_1vtx_at, m_pass_mintrack_at, m_pass_mindbv_at, m_pass_maxdbv_unc_at};
  // TH1D* h_mvtx_at_cutflow;

  //pass trigger, pass ID, pass iso 
  enum {pass_trig, pass_trigreq, pass_ID, pass_iso, pass_nsigmadxy, pass_sv3tkwlep};
  TH1D* h_sellep_sv_cutflow;

  //looking at lowpt trig and seeing if there is a pass_sv3tkwlep
  enum {pass_lowpttrig, pass_lowpttrigreq, pass_lowpttrig_lepID, pass_lowpttrig_lepiso, pass_lowpttrig_sv3tkwlep};
  TH1D* h_lowpttrig_cutflow;

  //looking at highpt trig and seeing if there is a pass_sv3tkwlep
  enum {pass_highpttrig, pass_highpttrigreq, pass_highpttrig_lepID, pass_highpttrig_lepiso, pass_highpttrig_sv3tkwlep};
  TH1D* h_highpttrig_cutflow;

};


MFVCutFlowHistos::MFVCutFlowHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_aux_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_aux_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src")))
{
  edm::Service<TFileService> fs;


  //make the histograms
  h_w = fs->make<TH1F>("h_w", ";event weight;events/0.1", 100, 0, 10);
  h_nsv = fs->make<TH1F>("h_nsv", ";# of secondary vertices; arb.units", 15, 0, 15);
  
  h_sellep_sv_cutflow = fs->make<TH1D>("h_sellep_cutflow", ";events", 6,0,6);
  int lbin = 1;
  for (const char* l : {"pass_trigger", "pass_offline", "pass_lepID", "pass_lepiso", "pass_lepnsigmadxy", "pass_sv3tkwlep"})
    h_sellep_sv_cutflow->GetXaxis()->SetBinLabel(lbin++, l);
  
  h_lowpttrig_cutflow = fs->make<TH1D>("h_lowpttrig_cutflow", ";events", 5,0,5);
  int xbin = 1;
  for (const char* x : {"pass_lowpttrig", "pass_lowpttrigreq", "pass_lowpttrig_lepID", "pass_lowpttrig_lepiso", "pass_lowpttrig_sv3tkwlep"})
    h_lowpttrig_cutflow->GetXaxis()->SetBinLabel(xbin++, x);
  
  h_highpttrig_cutflow = fs->make<TH1D>("h_highpttrig_cutflow", ";events", 5,0,5);
  int ybin = 1;
  for (const char* y : {"pass_highpttrig", "pass_highpttrigreq", "pass_highpttrig_lepID", "pass_highpttrig_lepiso", "pass_highpttrig_sv3tkwlep"})
    h_highpttrig_cutflow->GetXaxis()->SetBinLabel(ybin++, y);
  

  // h_e_lepvtx_cutflow = fs->make<TH1D>("h_e_lepvtx_cutflow", ";events", 8, 0, 8);
  // int nbin = 1;
  // for (const char* n : {"atleast_1vtx_w/e", "pass_ept", "pass_eid", "pass_eeta", "pass_eiso", "pass_trigger", "pass_efullvtx"})
  //   h_e_lepvtx_cutflow->GetXaxis()->SetBinLabel(nbin++, n);

  // h_m_lepvtx_cutflow = fs->make<TH1D>("h_m_lepvtx_cutflow", ";events", 8, 0, 8);
  // int mbin = 1;
  // for (const char* m : {"atleast_1vtx_w/m", "pass_mpt", "pass_mid", "pass_meta", "pass_miso", "pass_trigger", "pass_mfullvtx"})
  //   h_m_lepvtx_cutflow->GetXaxis()->SetBinLabel(mbin++, m);

  // h_e_vtxlep_cutflow = fs->make<TH1D>("h_e_vtxlep_cutflow", ";events", 7, 0, 7);
  // int obin = 1;
  // for (const char* o : {"atleast_1vtx_w/e", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc", "pass_trigger", "pass_efullsel"})
  //   h_e_vtxlep_cutflow->GetXaxis()->SetBinLabel(obin++, o);

  // h_m_vtxlep_cutflow = fs->make<TH1D>("h_m_vtxlep_cutflow", ";events", 7, 0, 7);
  // int pbin = 1;
  // for (const char* p : {"atleast_1vtx_w/m", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc", "pass_trigger", "pass_mfullsel"})
  //   h_m_vtxlep_cutflow->GetXaxis()->SetBinLabel(pbin++, p);


  // h_evertex_cutflow = fs->make<TH1D>("h_noe_vtx_cutflow", ";events", 5, 0, 5);
  // int qbin = 1;
  // for (const char* q : {"vtx_butno_ele", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc"})
  //   h_evertex_cutflow->GetXaxis()->SetBinLabel(qbin++, q);

  // h_mvertex_cutflow = fs->make<TH1D>("h_nom_vtx_cutflow", ";events", 5, 0, 5);
  // int rbin = 1;
  // for (const char* r : {"vtx_butno_mu", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc"})
  //   h_mvertex_cutflow->GetXaxis()->SetBinLabel(rbin++, r);

  // h_evtx_at_cutflow = fs->make<TH1D>("h_noe_vtx_at_cutflow", ";events", 7, 0, 7);
  // int sbin = 1;
  // for (const char* s : {"vtx_butno_ele", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc"})
  //   h_evtx_at_cutflow->GetXaxis()->SetBinLabel(sbin++, s);

  // h_mvtx_at_cutflow = fs->make<TH1D>("h_nom_vtx_at_cutflow", ";events", 7, 0, 7);
  // int tbin = 1;
  // for (const char* t : {"vtx_butno_mu", "pass_min4trk", "pass_mindbv", "pass_maxdbv_unc"})
  //   h_mvtx_at_cutflow->GetXaxis()->SetBinLabel(tbin++, t);
}

void MFVCutFlowHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_aux_token, auxes);
  
  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  const double w = *weight;
  h_w->Fill(w);

  const int nsv = int(auxes->size());
  h_nsv->Fill(nsv, w);
  //bool at_least_one_trigger_passed = false;
  bool pass_lowpt_trigger = false;
  bool pass_highpt_trigger = false;
  bool pass_lowpt_trigreq = false;
  bool pass_highpt_trigreq = false;

  // pt, ID, eta, iso
  // std::vector<bool> pass_el {false, false, false, false};
  // std::vector<bool> pass_mu {false, false, false, false};

  //ID, iso, nsigmadxy -- independent of the other cuts... 
  std::vector<bool> pass_selele {false, false, false};
  std::vector<bool> pass_selmu {false, false, false};

// first getting event - level information (concerning leptons)
  int nmuons = mevent->nmuons();
  int nelectrons= mevent->nelectrons();
        
  for(int ie =0; ie < nelectrons; ++ie){
    if (mevent->electron_ID[ie][3] == 1) {
      pass_selele[0] = true;
      if (mevent->electron_iso[ie] < 0.10){
        pass_selele[1] = true;
        if (fabs(mevent->electron_dxybs[ie])/mevent->electron_dxyerr[ie] > 3) {
          pass_selele[2] = true;
        }
      }
    }
  


    // if (mevent->electron_pt[ie] < 35) continue;
    //   pass_el[0]= true;
    //   if (mevent->electron_ID[ie][3] == 1) {
    //     pass_el[1] = true;
    //     if (abs(mevent->electron_eta[ie]) < 2.4) {
    //       pass_el[2] = true;
    //       if (mevent->electron_iso[ie] < 0.10) {
    //         pass_el[3] = true;
    //       }  
    //     }
    //   }

  }

  for(int im =0; im < nmuons; ++im) {

    if (mevent->muon_ID[im][1] == 1) {
      pass_selmu[0] = true;
      if (mevent->muon_iso[im] < 0.10) {
        pass_selmu[1] = true;
        if (fabs(mevent->muon_dxybs[im])/mevent->muon_dxyerr[im] > 3) {
          pass_selmu[2] = true;
        }
      }
    }

    // if (mevent->muon_pt[im] < 30) continue;
    //   pass_mu[0] = true;
    //   if (mevent->muon_ID[im][1] == 1) {
    //     pass_mu[1] = true;
    //     if (abs(mevent->muon_eta[im]) < 2.4) {
    //       pass_mu[2] = true;
    //       if (mevent->muon_iso[im] < 0.15) {
    //         pass_mu[3] = true;
    //       }
    //     }
    //   }
  }

 
  // for(size_t trig : mfv::MuonTriggers){
  //   if(mevent->pass_hlt(trig)) { 
  //     pass_trigger = true;
  //   }
  // }
  // for(size_t trig : mfv::ElectronTriggers){
  //   if(mevent->pass_hlt(trig)) { 
  //     pass_trigger = true;
  //   }
  // }

  for(size_t trig : mfv::MuonTriggers){
    if(mevent->pass_hlt(trig)) {
      std::pair<bool, std::string> result = satisfiesLepTrigger(mevent, trig);
      if(result.second == "low") {
        pass_lowpt_trigger = true;
        if (result.first) pass_lowpt_trigreq = true;
      }
      else if (result.second == "high") {
        pass_highpt_trigger = true;
        if (result.first) pass_highpt_trigreq = true;
      }
    }
  }
  for(size_t trig : mfv::ElectronTriggers){
    if(mevent->pass_hlt(trig)) {
      std::pair<bool, std::string> result = satisfiesLepTrigger(mevent, trig);
      if(result.second == "low") {
        pass_lowpt_trigger = true;
        if (result.first) pass_lowpt_trigreq = true;
      }
      else if (result.second == "high") {
        pass_highpt_trigger = true;
        if (result.first) pass_highpt_trigreq = true;
      }
    }
  }

  

  // // looking to see if the gen daughter was reconstructed. If so, then will use later when looking at : 
  // // vertices that should have leptons (both lepton + sv have been genmatched & reconstructed but the lepton is not in the SV)
  // double nelematched_0 = 0;
  // double nelematched_1 = 0;
  // double nmumatched_0 = 0;
  // double nmumatched_1 = 0;
  // //first is eta, then phi 
  // std::vector<float> elematched_0; 
  // std::vector<float> elematched_1;
  // std::vector<float> mumatched_0;
  // std::vector<float> mumatched_1;
  // int ngen_tau = 0;
  // int ngen_ele = 0;
  // int ngen_mu = 0;
  // for (size_t i=0; i<mevent->gen_daughters.size(); ++i){
  //   // skip stops and only look at leptons and quarks
  //   // FIXME: this only works for stoplq samples
  //   if (abs(mevent->gen_daughter_id[i])==1000006) {
  //     continue;
  //   }
  //   else{
  //     double gd_eta = mevent->gen_daughters[i].Eta();
  //     double gd_phi = mevent->gen_daughters[i].Phi();
  //     int n_ematched = 0;
  //     int n_mmatched = 0;
      
  //     if ( abs(mevent->gen_daughter_id[i]) == 11 ) { 
  //       ngen_ele += 1;
  //       std::vector<double> mindR;
  //       std::vector<float> ele_eta;
  //       std::vector<float> ele_phi;
  //       for (int ie=0; ie<mevent->nelectrons(); ++ie){
  //         double dR = reco::deltaR(mevent->nth_ele_eta(ie), mevent->nth_ele_phi(ie), gd_eta, gd_phi);
  //         mindR.push_back(dR);
  //         ele_eta.push_back(mevent->nth_ele_eta(ie));
  //         ele_phi.push_back(mevent->nth_ele_phi(ie));
  //       }
  //       if (mindR.size() !=0) {
  //         float best_dR = *min_element(mindR.begin(), mindR.end());
  //         int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
  //         if (best_dR < 0.1) {
  //           n_ematched +=1;
  //           if (i < 2) {
  //             elematched_0.push_back(ele_eta[best_idx]);
  //             elematched_0.push_back(ele_phi[best_idx]);
  //           }
  //           else if (i>2) {
  //             elematched_1.push_back(ele_eta[best_idx]);
  //             elematched_1.push_back(ele_phi[best_idx]);
  //           }
  //         }
  //       }
  //     }
  //     else if ( abs(mevent->gen_daughter_id[i]) == 13 ) {
  //       ngen_mu += 1;
  //       std::vector<double> mindR;
  //       std::vector<float> mu_eta;
  //       std::vector<float> mu_phi;
  //       for (int im=0; im<mevent->nmuons(); ++im){
  //         double dR = reco::deltaR(mevent->nth_mu_eta(im), mevent->nth_mu_phi(im), gd_eta, gd_phi);
  //         mindR.push_back(dR);
  //         mu_eta.push_back(mevent->nth_mu_eta(im));
  //         mu_phi.push_back(mevent->nth_mu_phi(im));
  //       }
  //       if (mindR.size() !=0) {
  //         float best_dR = *min_element(mindR.begin(), mindR.end());
  //         int best_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
  //         if (best_dR < 0.1) {
  //           n_mmatched +=1;
  //           if (i < 2) {
  //             mumatched_0.push_back(mu_eta[best_idx]);
  //             mumatched_0.push_back(mu_phi[best_idx]);
  //           }
  //           else if (i>2) {
  //             mumatched_1.push_back(mu_eta[best_idx]);
  //             mumatched_1.push_back(mu_phi[best_idx]);
  //           }
  //         }
  //       }
  //     }
  //     else if (abs(mevent->gen_daughter_id[i]) == 15 ) {
  //       ngen_tau +=1;
  //     }
  //     //should be 4 gen daughters; i = 0,1 belong to first vertex; i = 2,3 belong to second vertex
  //     if (i<2){
  //       nelematched_0 += n_ematched;
  //       nmumatched_0 += n_mmatched;
  //     }
  //     else{
  //       nelematched_1 += n_ematched;
  //       nmumatched_1 += n_mmatched;
  //     }
  //   }
  // }
  // have to find the lepton vertices again : (exactly what is done in vertex histos -- with some unneccesary stuff removed )

  // 2d vector storing : 
  // (e, mu, tau) 
  // index is sv 
  // std::vector<std::vector<int>> vtx_flavor;
  // std::vector<std::vector<int>> lepdau_flavor_invtx;

  //index is sv
  std::vector<bool> vtx_pass_mintks;
  std::vector<bool> vtx_pass_inbp;
  std::vector<bool> vtx_pass_dbv;
  std::vector<bool> vtx_pass_bs2derr;
  std::vector<bool> vtx_pass_sellepinSV;

  // // the dR between isv and gen vtx; 
  // // index is sv
  // // this is not 2d; instead keeping dR 
  // std::vector<float> genvertex0_dR;
  // std::vector<float> genvertex1_dR;
  // //index should be sv
  // std::vector<bool> genmatchedele0_bylep;
  // std::vector<bool> genmatchedmu0_bylep;
  // std::vector<bool> genmatchedele1_bylep;
  // std::vector<bool> genmatchedmu1_bylep;
  bool sv_presel = false;
  for (int isv = 0; isv < nsv; ++isv) {
    const MFVVertexAux& aux = auxes->at(isv);


    // //first checking different sv parameters and pushing back result 
    // //ntracks
    // vtx_pass_mintks.push_back(aux.ntracks()>= 3);

    // //inside beampipe
	  // vtx_pass_inbp.push_back(jmt::Geometry::inside_beampipe(true, aux.x, aux.y));

    // //dbv 
	  // vtx_pass_dbv.push_back(aux.bs2ddist > 0.01);

    // //bs2derr 
    // vtx_pass_bs2derr.push_back(aux.bs2derr < 0.0050);

    // std::vector<int> vflavor{0,0,0};
    // std::vector<int> lepdauinvtx{0,0,0};
    
    // bool genmatchedele0_lep = false;
    // bool genmatchedmu0_lep = false;
    // bool genmatchedele1_lep = false;
    // bool genmatchedmu1_lep = false;

    const int nmuons = aux.nmuons;
    const int nelectrons = aux.nelectrons;

    bool found_sellep = false;
    for (int m=0; m < nmuons; ++m) {
      auto temp = aux.muon_ID[m]; 
      int id = 0;
      if ( temp[0] == 0 ) id = 0; //none
      if ( temp[0] == 1 ) id = 1; //loose
      if ( temp[1] == 1 ) id = 2; //medium
      if ( temp[2] == 1 ) id = 3; //tight

      if (id > 1) {
        if (aux.muon_iso[m] < 0.1) {
          if (!found_sellep) {
            vtx_pass_sellepinSV.push_back(true);
            found_sellep = true;
          } 
        }
      }
    }
    for (int e=0; e < nelectrons; ++e) {
      auto temp = aux.electron_ID[e]; 
      int id = 0;
      if ( temp[0] == 0 ) id = 0; //none
      if ( temp[0] == 1 ) id = 1; //veto
      if ( temp[1] == 1 ) id = 2; //loose
      if ( temp[2] == 1 ) id = 3; //med
      if ( temp[3] == 1 ) id = 4; //tight

      if (id > 3) {
        if (aux.electron_iso[e] < 0.1) {
          if (!found_sellep) { 
            vtx_pass_sellepinSV.push_back(true);
            found_sellep = true;
          }
        }
      }
    }
    // vtx_pass_mintks.push_back(aux.ntracks()>= 3);

    // //inside beampipe
	  // vtx_pass_inbp.push_back(jmt::Geometry::inside_beampipe(true, aux.x, aux.y));

    // //dbv 
	  // vtx_pass_dbv.push_back(aux.bs2ddist > 0.01);

    // //bs2derr 
    // vtx_pass_bs2derr.push_back(aux.bs2derr < 0.0050);

    if (found_sellep) {
      if (aux.ntracks() == 3) {
        if (jmt::Geometry::inside_beampipe(true, aux.x, aux.y)) {
          if (aux.bs2ddist > 0.01) {
            if (aux.bs2derr < 0.0050) {
              sv_presel = true;
            }
          }
        }
      }
    }

  //   std::vector<int> genvtx_flavor;
  //   jmt::MinValue d;
  //   for (int igenv = 0; igenv < 2; ++igenv) {
  //     double genx = mevent->gen_lsp_decay[igenv*3+0];
  //     double geny = mevent->gen_lsp_decay[igenv*3+1];
  //     int genvtx_fl = abs(mevent->gen_daughter_id[igenv*2+1]);
  //     genvtx_flavor.push_back(genvtx_fl);
  //     d(igenv, mag(aux.x-genx,
  //                  aux.y-geny));
  //   }

  //   const int closest_genvtx_flavor = genvtx_flavor[d.i()];
  //   if (closest_genvtx_flavor == 11 ) vflavor[0] += 1;
  //   if (closest_genvtx_flavor == 13 ) vflavor[1] += 1;
  //   if (closest_genvtx_flavor == 15 ) vflavor[2] += 1;

  //   vtx_flavor.push_back(vflavor);

  //   //needed a work-around to keep dR for each of the gen vertices separate. while also keeping nentries at nsv 
  //   // so : dummy fill a large number : 10 for the gen vertex that isn't the closest to the reco vertex. 
  //   if (d.i() == 0) {
  //     genvertex0_dR.push_back(d.v());
  //     genvertex1_dR.push_back(10.);
  //     if (elematched_0.size() != 0) {
  //       for (int i=0; i < nelectrons; ++i) {
  //         if (elematched_0[0] == aux.electron_eta[i]) {
  //           if (elematched_0[1] == aux.electron_phi[i]) {    
  //             genmatchedele0_lep = true;
  //           }
  //         }
  //       }
  //     }
  //     if (mumatched_0.size() != 0) {
  //       for (int i=0; i < nmuons; ++i) {
  //         if (mumatched_0[0] == aux.muon_eta[i]) {
  //           if (mumatched_0[1] == aux.muon_phi[i]) {
  //             genmatchedmu0_lep = true;
  //           }
  //         }
  //       }
  //     }
  //   }
  //   if (d.i() == 1) {
  //     genvertex1_dR.push_back(d.v());
  //     genvertex0_dR.push_back(10.);
  //     if (elematched_1.size() != 0) {
  //       for (int i=0; i < nelectrons; ++i) {
  //         if (elematched_1[0] == aux.electron_eta[i]) {
  //           if (elematched_1[1] == aux.electron_phi[i]) {
  //             genmatchedele1_lep = true;
  //           }
  //         } 
  //       }
  //     }
  //     if (mumatched_1.size() != 0) {
  //       for (int i=0; i < nmuons; ++i) {
  //         if (mumatched_1[0] == aux.muon_eta[i]) {
  //           if (mumatched_1[1] == aux.muon_phi[i]) {
  //             genmatchedmu1_lep = true;
  //           }
  //         }
  //       }
  //     }
  //   }

  //   genmatchedele0_bylep.push_back(genmatchedele0_lep);
  //   genmatchedmu0_bylep.push_back(genmatchedmu0_lep);
  //   genmatchedele1_bylep.push_back(genmatchedele1_lep);
  //   genmatchedmu1_bylep.push_back(genmatchedmu1_lep);

  }

  // int good_match_sv = 0;
  // //int good_match_lepinsv = 0;
  // // separating by which gen vertex is matched to be able to separate cases better 
  // // first index is matched sv to gen vtx 0; next index corresponds to gen vtx 1;
  // std::vector<bool> good_match_elinsv{false,false};
  // std::vector<bool> good_match_muinsv{false,false};

  // std::vector<bool> nogood_match_elinsv{false,false};
  // std::vector<bool> nogood_match_muinsv{false,false};

  // // 2d vector : [ first vertex, second vertex ] where  vertex == 
  // // [ pass min tk, pass beampipe, pass dbv, pass bs2derr ]
  // std::vector<bool> elevtx0_sel;
  // std::vector<bool> muvtx0_sel;
  // std::vector<bool> elevtx1_sel;
  // std::vector<bool> muvtx1_sel;

  // //same time of 2d vector as above; but now for the sv that should have lepton but without lepton 
  // std::vector<bool> noelevtx0_sel;
  // std::vector<bool> nomuvtx0_sel;
  // std::vector<bool> noelevtx1_sel;
  // std::vector<bool> nomuvtx1_sel;

  // // now its time to find the reconstructed vertices that are the closest to gen vertex 0 and gen vertex 1
  // // also getting the index of the min element 
  // if (genvertex0_dR.size() !=0) {
  //   float best_sv_gen0_dR = *min_element(genvertex0_dR.begin(), genvertex0_dR.end());
  //   int best_sv_gen0_isv = std::min_element(genvertex0_dR.begin(), genvertex0_dR.end()) - genvertex0_dR.begin();

  //   if (best_sv_gen0_dR < 0.02) {
  //     // sv matches 
  //     good_match_sv += 1;
  //     for (int i=0; i<3; ++i) {
  //       if (vtx_flavor[best_sv_gen0_isv][i]>0) {
  //         if (i==0) { 
  //           if (genmatchedele0_bylep[best_sv_gen0_isv]) {
  //             good_match_elinsv[0] = true;
  //             //checking vertex selections 
  //             elevtx0_sel.push_back(vtx_pass_mintks[best_sv_gen0_isv]);
  //             elevtx0_sel.push_back(vtx_pass_inbp[best_sv_gen0_isv]);
  //             elevtx0_sel.push_back(vtx_pass_dbv[best_sv_gen0_isv]);
  //             elevtx0_sel.push_back(vtx_pass_bs2derr[best_sv_gen0_isv]);
  //           }
  //           else {
  //             if (nelematched_0) {
  //               nogood_match_elinsv[0] = true;
  //               noelevtx0_sel.push_back(vtx_pass_mintks[best_sv_gen0_isv]);
  //               noelevtx0_sel.push_back(vtx_pass_inbp[best_sv_gen0_isv]);
  //               noelevtx0_sel.push_back(vtx_pass_dbv[best_sv_gen0_isv]);
  //               noelevtx0_sel.push_back(vtx_pass_bs2derr[best_sv_gen0_isv]);
  //             }
  //           }
  //         }
  //         if (i==1) {
  //           if (genmatchedmu0_bylep[best_sv_gen0_isv]) {
  //             good_match_muinsv[0] = true;
  //             muvtx0_sel.push_back(vtx_pass_mintks[best_sv_gen0_isv]);
  //             muvtx0_sel.push_back(vtx_pass_inbp[best_sv_gen0_isv]);
  //             muvtx0_sel.push_back(vtx_pass_dbv[best_sv_gen0_isv]);
  //             muvtx0_sel.push_back(vtx_pass_bs2derr[best_sv_gen0_isv]);
  //           }
  //           else {
  //             if (nmumatched_0) {
  //               nogood_match_muinsv[0] = true;
  //               nomuvtx0_sel.push_back(vtx_pass_mintks[best_sv_gen0_isv]);
  //               nomuvtx0_sel.push_back(vtx_pass_inbp[best_sv_gen0_isv]);
  //               nomuvtx0_sel.push_back(vtx_pass_dbv[best_sv_gen0_isv]);
  //               nomuvtx0_sel.push_back(vtx_pass_bs2derr[best_sv_gen0_isv]);
  //             }
  //           }
  //         }
  //         else continue;
  //       }
  //     }
  //   }
  // } 
  // if (genvertex1_dR.size() !=0) {
  //   float best_sv_gen1_dR = *min_element(genvertex1_dR.begin(), genvertex1_dR.end());
  //   int best_sv_gen1_isv = std::min_element(genvertex1_dR.begin(), genvertex1_dR.end()) - genvertex1_dR.begin();

  //   if (best_sv_gen1_dR < 0.02) {
  //     // sv matches 
  //     good_match_sv += 1;
  //     for (int i=0; i<3; ++i) {
  //       if (vtx_flavor[best_sv_gen1_isv][i]>0) {
  //         if (i==0) { 
  //           if (genmatchedele1_bylep[best_sv_gen1_isv]) {
  //             good_match_elinsv[1] = true;
  //             //checking vertex selections 
  //             elevtx1_sel.push_back(vtx_pass_mintks[best_sv_gen1_isv]);
  //             elevtx1_sel.push_back(vtx_pass_inbp[best_sv_gen1_isv]);
  //             elevtx1_sel.push_back(vtx_pass_dbv[best_sv_gen1_isv]);
  //             elevtx1_sel.push_back(vtx_pass_bs2derr[best_sv_gen1_isv]);
  //           }
  //           else {
  //             if (nelematched_1) {
  //               nogood_match_elinsv[1] = true;
  //               noelevtx1_sel.push_back(vtx_pass_mintks[best_sv_gen1_isv]);
  //               noelevtx1_sel.push_back(vtx_pass_inbp[best_sv_gen1_isv]);
  //               noelevtx1_sel.push_back(vtx_pass_dbv[best_sv_gen1_isv]);
  //               noelevtx1_sel.push_back(vtx_pass_bs2derr[best_sv_gen1_isv]);
  //             }
  //           }
  //         }
  //         if (i==1) {
  //           if (genmatchedmu1_bylep[best_sv_gen1_isv]) {
  //             good_match_muinsv[1] = true;
  //             muvtx1_sel.push_back(vtx_pass_mintks[best_sv_gen1_isv]);
  //             muvtx1_sel.push_back(vtx_pass_inbp[best_sv_gen1_isv]);
  //             muvtx1_sel.push_back(vtx_pass_dbv[best_sv_gen1_isv]);
  //             muvtx1_sel.push_back(vtx_pass_bs2derr[best_sv_gen1_isv]);
  //           }
  //           else {
  //             if (nmumatched_1) {
  //               nogood_match_muinsv[1] = true;
  //               nomuvtx1_sel.push_back(vtx_pass_mintks[best_sv_gen1_isv]);
  //               nomuvtx1_sel.push_back(vtx_pass_inbp[best_sv_gen1_isv]);
  //               nomuvtx1_sel.push_back(vtx_pass_dbv[best_sv_gen1_isv]);
  //               nomuvtx1_sel.push_back(vtx_pass_bs2derr[best_sv_gen1_isv]);
  //             }
  //           }
  //         }
  //         else continue;
  //       }
  //     }
  //   }
  



  // if (pass_trigger) {
  if (pass_lowpt_trigger || pass_highpt_trigger) {
    h_sellep_sv_cutflow->Fill(pass_trig, w);
    // if (pass_el[3] || pass_mu[3]) {
    bool lowpt = (pass_lowpt_trigger && pass_lowpt_trigreq);
    bool highpt = (pass_highpt_trigger && pass_highpt_trigreq);
    
    if ( lowpt || highpt)  { 
      h_sellep_sv_cutflow->Fill(pass_trigreq, w);
      if (pass_selele[0] || pass_selmu[0]) {
        h_sellep_sv_cutflow->Fill(pass_ID, w);
        if (pass_selele[1] || pass_selmu[1]) {
          h_sellep_sv_cutflow->Fill(pass_iso, w);
          if (pass_selele[2] || pass_selmu[2]) {
            h_sellep_sv_cutflow->Fill(pass_nsigmadxy, w);
            if (sv_presel)
            h_sellep_sv_cutflow->Fill(pass_sv3tkwlep, w);
          }
        }
      }
    }
  }

  if (!pass_highpt_trigger) { 
    if (pass_lowpt_trigger ) {
      h_lowpttrig_cutflow->Fill(pass_lowpttrig, w);
      if (pass_lowpt_trigreq) { 
        h_lowpttrig_cutflow->Fill(pass_lowpttrigreq, w);
        if (pass_selele[0] || pass_selmu[0]) {
          h_lowpttrig_cutflow->Fill(pass_lowpttrig_lepID, w);
          if (pass_selele[1] || pass_selmu[1]) {
            h_lowpttrig_cutflow->Fill(pass_lowpttrig_lepiso, w);
            if (sv_presel) {
              h_lowpttrig_cutflow->Fill(pass_lowpttrig_sv3tkwlep, w);
            }
          }
        }
      }
    }
  }


  if (pass_highpt_trigger ) {
    h_highpttrig_cutflow->Fill(pass_highpttrig, w);
    if (pass_highpt_trigreq) { 
      h_highpttrig_cutflow->Fill(pass_highpttrigreq, w);
      if (pass_selele[0] || pass_selmu[0]) {
        h_highpttrig_cutflow->Fill(pass_highpttrig_lepID, w);
        if (pass_selele[1] || pass_selmu[1]) {
          h_highpttrig_cutflow->Fill(pass_highpttrig_lepiso, w);
          if (sv_presel) {
            h_highpttrig_cutflow->Fill(pass_highpttrig_sv3tkwlep, w);
          }
        }
      }
    }
  }




//filling cutflows 
  // if (good_match_elinsv[0]) {
  //   h_e_vtxlep_cutflow->Fill(einsv2, w);
  //   if (elevtx0_sel[0]) {
  //     h_e_vtxlep_cutflow->Fill(einsv_mintrack, w);
  //     if (elevtx0_sel[2]) {
  //       h_e_vtxlep_cutflow->Fill(einsv_mindbv, w);
  //       if (elevtx0_sel[3]) {
  //         h_e_vtxlep_cutflow->Fill(einsv_maxdbvunc, w);
  //         if (pass_trigger) {
  //           h_e_vtxlep_cutflow->Fill(einsv_trigger2, w);
  //           if (pass_el[0] && pass_el[1] && pass_el[2] && pass_el[3]) {
  //             h_e_vtxlep_cutflow->Fill(einsv_fullsel*good_match_sv);
  //           }
  //         }
  //       } 
  //     }
  //   }
  // } 
  
  // if (good_match_elinsv[1]) {
  //   h_e_vtxlep_cutflow->Fill(einsv2, w);
  //   if (elevtx1_sel[0]) {
  //     h_e_vtxlep_cutflow->Fill(einsv_mintrack, w);
  //     if (elevtx1_sel[2]) {
  //       h_e_vtxlep_cutflow->Fill(einsv_mindbv, w);
  //       if (elevtx1_sel[3]) {
  //         h_e_vtxlep_cutflow->Fill(einsv_maxdbvunc, w);
  //         if (pass_trigger) {
  //           h_e_vtxlep_cutflow->Fill(einsv_trigger2, w);
  //           if (pass_el[0] && pass_el[1] && pass_el[2] && pass_el[3]) {
  //             h_e_vtxlep_cutflow->Fill(einsv_fullsel*good_match_sv);
  //           }
  //         }
  //       }
  //     }
  //   } 
  // }
  // if (good_match_muinsv[0]) {
  //   h_m_vtxlep_cutflow->Fill(minsv2, w);
  //   if (muvtx0_sel[0]) {
  //     h_m_vtxlep_cutflow->Fill(minsv_mintrack, w);
  //     if (muvtx0_sel[2]) {
  //       h_m_vtxlep_cutflow->Fill(minsv_mindbv, w);
  //       if (muvtx0_sel[3]) {
  //         h_m_vtxlep_cutflow->Fill(minsv_maxdbvunc, w);
  //         if (pass_trigger) {
  //           h_m_vtxlep_cutflow->Fill(minsv_trigger2, w);
  //           if (pass_mu[0] && pass_mu[1] && pass_mu[2] && pass_mu[3]) {
  //             h_m_vtxlep_cutflow->Fill(minsv_fullsel);
  //           }
  //         }
  //       }
  //     }
  //   } 
  // }
  // if (good_match_muinsv[1]) {
  //   h_m_vtxlep_cutflow->Fill(minsv2, w);
  //     if (muvtx1_sel[0]) {
  //     h_m_vtxlep_cutflow->Fill(minsv_mintrack, w);
  //     if (muvtx1_sel[2]) {
  //       h_m_vtxlep_cutflow->Fill(minsv_mindbv, w);
  //       if (muvtx1_sel[3]) {
  //         h_m_vtxlep_cutflow->Fill(minsv_maxdbvunc, w);
  //         if (pass_trigger) {
  //           h_m_vtxlep_cutflow->Fill(minsv_trigger2, w);
  //           if (pass_mu[0] && pass_mu[1] && pass_mu[2] && pass_mu[3]) {
  //             h_m_vtxlep_cutflow->Fill(minsv_fullsel);
  //           }  
  //         }
  //       }
  //     }
  //   } 
  // }

  // // again, but now consider the lepton requirements first; then vertex 
  // if (good_match_elinsv[0]) {
  //   h_e_lepvtx_cutflow->Fill(einsv, w);
  //   if (pass_el[0]) {
  //     h_e_lepvtx_cutflow->Fill(einsv_pt, w);
  //     if (pass_el[1]) {
  //       h_e_lepvtx_cutflow->Fill(einsv_id, w);
  //       if (pass_el[2]) {
  //         h_e_lepvtx_cutflow->Fill(einsv_eta, w);
  //         if (pass_el[3]) {
  //           h_e_lepvtx_cutflow->Fill(einsv_iso, w);
  //           if (pass_trigger) {
  //             h_e_lepvtx_cutflow->Fill(einsv_trigger, w);
  //             if(elevtx0_sel[0] && elevtx0_sel[2] && elevtx0_sel[3]) {
  //               h_e_lepvtx_cutflow->Fill(einsv_fullvtx, w);
  //             }
  //           }
  //         }
  //       }
  //     }
  //   }
  // }

  // if (good_match_elinsv[1]) {
  //   h_e_lepvtx_cutflow->Fill(einsv, w);
  //   if (pass_el[0]) {
  //     h_e_lepvtx_cutflow->Fill(einsv_pt, w);
  //     if (pass_el[1]) {
  //       h_e_lepvtx_cutflow->Fill(einsv_id, w);
  //       if (pass_el[2]) {
  //         h_e_lepvtx_cutflow->Fill(einsv_eta, w);
  //         if (pass_el[3]) {
  //           h_e_lepvtx_cutflow->Fill(einsv_iso, w);
  //           if (pass_trigger) {
  //             h_e_lepvtx_cutflow->Fill(einsv_trigger, w);
  //             if(elevtx1_sel[0] && elevtx1_sel[2] && elevtx1_sel[3]) {
  //               h_e_lepvtx_cutflow->Fill(einsv_fullvtx, w);
  //             }
  //           }
  //         }
  //       }
  //     }
  //   }

  // }

//   if (good_match_muinsv[0]) {
//     h_m_lepvtx_cutflow->Fill(minsv, w);
//     if (pass_mu[0]) {
//       h_m_lepvtx_cutflow->Fill(minsv_pt, w);
//       if (pass_mu[1]) {
//         h_m_lepvtx_cutflow->Fill(minsv_id, w);
//         if (pass_mu[2]) {
//           h_m_lepvtx_cutflow->Fill(minsv_eta, w);
//           if (pass_mu[3]) {
//             h_m_lepvtx_cutflow->Fill(minsv_iso, w);
//             if (pass_trigger) {
//               h_m_lepvtx_cutflow->Fill(minsv_trigger, w);
//               if(muvtx0_sel[0] && muvtx0_sel[2] && muvtx0_sel[3]) {
//                 h_m_lepvtx_cutflow->Fill(minsv_fullvtx, w);
//               }
//             }
//           }
//         }
//       }
//     }
//   }

//   if (good_match_muinsv[1]) {
//     h_m_lepvtx_cutflow->Fill(minsv, w);
//     if (pass_mu[0]) {
//       h_m_lepvtx_cutflow->Fill(minsv_pt, w);
//       if (pass_mu[1]) {
//         h_m_lepvtx_cutflow->Fill(minsv_id, w);
//         if (pass_mu[2]) {
//           h_m_lepvtx_cutflow->Fill(minsv_eta, w);
//           if (pass_mu[3]) {
//             h_m_lepvtx_cutflow->Fill(minsv_iso, w);
//             if (pass_trigger) {
//               h_m_lepvtx_cutflow->Fill(minsv_trigger, w);
//               if(muvtx1_sel[0] && muvtx1_sel[2] && muvtx1_sel[3]) {
//                 h_m_lepvtx_cutflow->Fill(minsv_fullvtx, w);
//               }
//             }
//           }
//         }
//       }
//     }
//   }

// // new : filling the cutflows with the sv that should have leptons but do not : 
// // also requiring that the gen lepton was reconstructed 
// // so this is purely for the case in which the lepton was not in the SV even though both were genmatched 
//   if (nogood_match_elinsv[0]) {
//     h_evertex_cutflow->Fill(e_atleast_1vtx, w);
//     if (noelevtx0_sel[0]) {
//       h_evertex_cutflow->Fill(e_pass_mintrack, w);
//       if (noelevtx0_sel[2]) {
//         h_evertex_cutflow->Fill(e_pass_mindbv, w);
//         if (noelevtx0_sel[3]) {
//           h_evertex_cutflow->Fill(e_pass_maxdbv_unc, w);
//         } 
//       }
//     }
//   } 
  
//   if (nogood_match_elinsv[1]) {
//     h_evertex_cutflow->Fill(e_atleast_1vtx, w);
//     if (noelevtx1_sel[0]) {
//       h_evertex_cutflow->Fill(e_pass_mintrack, w);
//       if (noelevtx1_sel[2]) {
//         h_evertex_cutflow->Fill(e_pass_mindbv, w);
//         if (noelevtx1_sel[3]) {
//           h_evertex_cutflow->Fill(e_pass_maxdbv_unc, w);
//         }
//       }
//     } 
//   }
//   if (nogood_match_muinsv[0]) {
//     h_mvertex_cutflow->Fill(m_atleast_1vtx, w);
//     if (nomuvtx0_sel[0]) {
//       h_mvertex_cutflow->Fill(m_pass_mintrack, w);
//       if (nomuvtx0_sel[2]) {
//         h_mvertex_cutflow->Fill(m_pass_mindbv, w);
//         if (nomuvtx0_sel[3]) {
//           h_mvertex_cutflow->Fill(m_pass_maxdbv_unc, w);
//         }
//       }
//     } 
//   }
//   if (nogood_match_muinsv[1]) {
//     h_mvertex_cutflow->Fill(m_atleast_1vtx, w);
//     if (nomuvtx1_sel[0]) {
//       h_mvertex_cutflow->Fill(m_pass_mintrack, w);
//       if (nomuvtx1_sel[2]) {
//         h_mvertex_cutflow->Fill(m_pass_mindbv, w);
//         if (nomuvtx1_sel[3]) {
//           h_mvertex_cutflow->Fill(m_pass_maxdbv_unc, w);
//         }
//       }
//     } 
//   }

//   if (pass_trigger) {
//     if (pass_mu[0] && pass_mu[1] && pass_mu[2] && pass_mu[3]) {
//       if (nogood_match_muinsv[0]) {
//         h_mvtx_at_cutflow->Fill(m_atleast_1vtx_at, w);
//         if (nomuvtx0_sel[0]) {
//           h_mvtx_at_cutflow->Fill(m_pass_mintrack_at, w);
//           if (nomuvtx0_sel[2]) {
//             h_mvtx_at_cutflow->Fill(m_pass_mindbv_at, w);
//             if (nomuvtx0_sel[3]) {
//               h_mvtx_at_cutflow->Fill(m_pass_maxdbv_unc_at, w);
//             }
//           }
//         }
//       }
//       if (nogood_match_muinsv[1]) {
//         h_mvertex_cutflow->Fill(m_atleast_1vtx_at, w);
//         if (nomuvtx1_sel[0]) {
//           h_mvertex_cutflow->Fill(m_pass_mintrack_at, w);
//           if (nomuvtx1_sel[2]) {
//             h_mvertex_cutflow->Fill(m_pass_mindbv_at, w);
//             if (nomuvtx1_sel[3]) {
//               h_mvertex_cutflow->Fill(m_pass_maxdbv_unc_at, w);
//             }
//           }
//         } 
//       }
//     }
//   }
//   if (pass_trigger) {
//     if (pass_el[0] && pass_el[1] && pass_el[2] && pass_el[3]) {
//       if (nogood_match_elinsv[0]) {
//         h_evtx_at_cutflow->Fill(e_atleast_1vtx_at, w);
//         if (noelevtx0_sel[0]) {
//           h_evtx_at_cutflow->Fill(e_pass_mintrack_at, w);
//           if (noelevtx0_sel[2]) {
//             h_evtx_at_cutflow->Fill(e_pass_mindbv_at, w);
//             if (noelevtx0_sel[3]) {
//               h_evtx_at_cutflow->Fill(e_pass_maxdbv_unc_at, w);
//             } 
//           }
//         }
//       } 
//       if (nogood_match_elinsv[1]) {
//         h_evtx_at_cutflow->Fill(e_atleast_1vtx_at, w);
//         if (noelevtx1_sel[0]) {
//           h_evtx_at_cutflow->Fill(e_pass_mintrack_at, w);
//           if (noelevtx1_sel[2]) {
//             h_evtx_at_cutflow->Fill(e_pass_mindbv_at, w);
//             if (noelevtx1_sel[3]) {
//               h_evtx_at_cutflow->Fill(e_pass_maxdbv_unc_at, w);
//             }
//           } 
//         }
//       }
//     }
//   }
}

std::pair<bool, std::string> MFVCutFlowHistos::satisfiesLepTrigger(edm::Handle<MFVEvent> mevent, size_t trig) { 

  int year = int(MFVNEUTRALINO_YEAR);
  int nmuons     = mevent->nmuons();
  int nelectrons = mevent->nelectrons();
  int njets      = mevent->njets(20);
    
  bool passed_kinematics = false;

  switch(trig){
  case mfv::b_HLT_Ele27_WPTight_Gsf : //for 2016
    {
    if (year != 20161 || year !=20162) return std::make_pair(false, "na");
    for(int ie =0; ie < nelectrons; ++ie){
      if (mevent->electron_pt[ie] < 30) continue; //for 2016
      if (mevent->electron_ID[ie][3] == 1) {
        if (abs(mevent->electron_eta[ie]) < 2.4) { 
          if (mevent->electron_iso[ie] < 0.10) {
            passed_kinematics = true;
          } 
        }
      }
    }
    // return passed_kinematics;
    return std::make_pair(passed_kinematics, std::string("low"));

  }
  case mfv::b_HLT_Ele35_WPTight_Gsf : //for 2017
    {
    if (year != 2017) return std::make_pair(false, "na");
    for(int ie =0; ie < nelectrons; ++ie){
      if (mevent->electron_pt[ie] < 38) continue; //for 2017
      if (mevent->electron_ID[ie][3] == 1) {
        if (abs(mevent->electron_eta[ie]) < 2.4) { 
          if (mevent->electron_iso[ie] < 0.10) {
            passed_kinematics = true;
          } 
        }
      }
    }
    // return passed_kinematics;
    return std::make_pair(passed_kinematics, std::string("low"));
  }
  case mfv::b_HLT_Ele32_WPTight_Gsf : //for 2018
    {
      if (year != 2018) return std::make_pair(false, "na");
      for(int ie =0; ie < nelectrons; ++ie){
        if (mevent->electron_pt[ie] < 35) continue; //for 2018
	      if (mevent->electron_ID[ie][3] == 1) {
	        if (abs(mevent->electron_eta[ie]) < 2.4) { 
	          if (mevent->electron_iso[ie] < 0.10) {
	            passed_kinematics = true;
	          } 
	        }
	      }
      }
      // return passed_kinematics;
      return std::make_pair(passed_kinematics, std::string("low"));

    }

  case mfv::b_HLT_IsoMu27 : //for 2017
    {
    if (year != 2017) return std::make_pair(false, "na");
    for(int im =0; im < nmuons; ++im) {
      if (mevent->muon_pt[im] < 30) continue; 
      if (mevent->muon_ID[im][1] == 1) {
        if (abs(mevent->muon_eta[im]) < 2.4) {
          if (mevent->muon_iso[im] < 0.15) {
            passed_kinematics = true;
          }
        }
      }
    }
    // return passed_kinematics;
    return std::make_pair(passed_kinematics, std::string("low"));

  }
  case mfv::b_HLT_IsoMu24 : //for 2018, 2016
    {
      if (year != 2016 || year != 2018) return std::make_pair(false, "na");
      for(int im =0; im < nmuons; ++im) {
        if (mevent->muon_pt[im] < 27) continue;
	      if (mevent->muon_ID[im][1] == 1) {
	        if (abs(mevent->muon_eta[im]) < 2.4) {
	          if (mevent->muon_iso[im] < 0.15) {
	            passed_kinematics = true;
	          }
	        }
	      }
      }
      // return passed_kinematics;
      return std::make_pair(passed_kinematics, std::string("low"));

    }
  
  case mfv::b_HLT_Mu50 :
    {
      for(int im=0; im < nmuons; ++im) {
	    if (mevent->muon_pt[im] < 53) continue;
	      if (mevent->muon_ID[im][1] == 1) {
	        if (abs(mevent->muon_eta[im]) < 2.4) {
	          if (mevent->muon_iso[im] < 0.15) {
	            passed_kinematics = true;
	          }
	        }
	      }
      }
      // return passed_kinematics;
      return std::make_pair(passed_kinematics, std::string("high"));

    }
    
  case mfv::b_HLT_Ele115_CaloIdVT_GsfTrkIdT :
    {
      for(int ie =0; ie < nelectrons; ++ie){
	      if (mevent->electron_pt[ie] < 120) continue;
	      if (mevent->electron_ID[ie][3] == 1) {
	        if (abs(mevent->electron_eta[ie]) < 2.4) { 
	          if (mevent->electron_iso[ie] < 0.10) {
	            passed_kinematics = true;
	          }
	        }
	      }
      }
      // return passed_kinematics;
      return std::make_pair(passed_kinematics, std::string("high"));

    }
    
  case  mfv::b_HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165 :
    {
      for(int ie =0; ie < nelectrons; ++ie){
	      if (mevent->electron_pt[ie] < 55) continue;
	      if (mevent->electron_ID[ie][3] == 1) {
	        if (abs(mevent->electron_eta[ie]) < 2.4) { 
	          if (mevent->electron_iso[ie] < 0.10) {
	            for(int j0=0; j0 < njets; ++j0){
		            if (mevent->jet_pt[j0] < 170) continue;
		            passed_kinematics = true;
	            }
	          }
	        }
	      }
      }
      // return passed_kinematics;
      return std::make_pair(passed_kinematics, std::string("high"));

    }
  default :
    {
      throw std::invalid_argument(std::string(mfv::hlt_paths[trig]) + " not implemented in satisfiesTrigger");
    }
  }

  return std::make_pair(false, "na");

}

  
DEFINE_FWK_MODULE(MFVCutFlowHistos);
