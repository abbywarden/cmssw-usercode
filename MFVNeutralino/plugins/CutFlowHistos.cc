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

class MFVCutFlowHistos : public edm::EDAnalyzer {
 public:
  explicit MFVCutFlowHistos(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);
   
 private:
  const edm::EDGetTokenT<MFVEvent> mevent_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_aux_token;
  

  // enum { pass_trigger, pass_jetsel, pass_ID, pass_pt, pass_eta, pass_iso, pass_displept_50um, pass_dispsellept_50um };
  // TH1D* h_event_cutflow;


  enum { any_electron, full5x5sigmaIetaIeta, delta_eta_seed, delta_phi, HoverE, ooEmooP, expected_missing_inner_hits, pass_conversion_veto };
  TH1D* h_tight_ele_cutflow;

  enum { isMedMuon, muiso_vl, muiso_l, muiso_med, muiso_tight, muiso_vt };
  TH1D* h_muiso_cutflow;

  enum { isTightEl, eliso_vl, eliso_l, eliso_med, eliso_tight, eliso_vt };
  TH1D* h_eleiso_cutflow;

  // enum { Apass_trigger, Apass_jetsel, Apass_lepsel, Apass_displept_50um, Ansv_goe_1, Aexclude_beampipe, Amintks_4, Amin_bs2ddist, Amax_rescale_bs2derr };
  // TH1D* h_selA_cutflow;

  // enum { Bpass_trigger, Bpass_jetsel, Bpass_lepsel, Bpass_dispsellept_50um, Bnsv_goe_1, Bexclude_beampipe, Bmintks_4, Bmin_bs2ddist, Bmax_rescale_bs2derr };
  // TH1D* h_selB_cutflow;

  //lepton cutflows
  enum {l_pass_trig, pass_lepgoe, pass_leppt, pass_lepeta, pass_lepID, pass_lepiso};
  TH1D* h_lepton_cutflow;

  enum {e_pass_trig, pass_egoe, pass_ept, pass_eeta, pass_eID, pass_eiso};
  TH1D* h_electron_cutflow;

  enum {m_pass_trig, pass_mgoe, pass_mpt, pass_meta, pass_mID, pass_miso};
  TH1D* h_muon_cutflow;

};


MFVCutFlowHistos::MFVCutFlowHistos(const edm::ParameterSet& cfg)
  : mevent_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("mevent_src"))),
    vertex_aux_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_aux_src")))
  
{
  edm::Service<TFileService> fs;


  //make the histograms
  
  
  // electron cutflow for criteria related to cutbased; filled after trigger is satisfied 
  h_tight_ele_cutflow = fs->make<TH1D>("h_tight_ele_cuflow", ";events", 8, 0, 8);
  int elbin = 1;
  for (const char* a : {"any_electron", "full5x5sigmaIetaIeta", "delta_eta_seed", "delta_phi", "HoverE", "ooEmooP", "expected_missing_inner_hits", "pass_conversion_veto"})
    h_tight_ele_cutflow->GetXaxis()->SetBinLabel(elbin++, a);

  // electron and muon cutflow to look at different isolation cuts 
  h_eleiso_cutflow = fs->make<TH1D>("h_eleiso_cutflow", ";events", 6, 0, 6);
  int elibin = 1;
  for (const char* b : {"isTightEl", "eliso_vl","eliso_l", "eliso_med", "eliso_tight", "eliso_vt"})
    h_eleiso_cutflow->GetXaxis()->SetBinLabel(elibin++, b);
  
  h_muiso_cutflow = fs->make<TH1D>("h_muiso_cutflow", ";events", 6, 0, 6);
  int mubin = 1;
  for (const char* c : {"isMedMuon", "muiso_vl","muiso_l", "muiso_med", "muiso_tight", "muiso_vt"})
    h_muiso_cutflow->GetXaxis()->SetBinLabel(mubin++, c);

  // different full selection cutflows : 1 with displaced lepton cut, the other with a displaced selected lepton 
  // h_selA_cutflow = fs->make<TH1D>("h_selA_cutflow", ";events", 9, 0, 9);
  // int sbin = 1;
  // for (const char* d : {"pass_trigger", "pass_jetsel", "pass_lepsel", "pass_displept_50um", "nsv_goe_1", "exclude_beampipe", "mintks_4", "min_bs2ddist", "max_rescale_bs2derr"})
  //   h_selA_cutflow->GetXaxis()->SetBinLabel(sbin++, d);

  // h_selB_cutflow = fs->make<TH1D>("h_selB_cutflow", ";events", 9, 0, 9);
  // int tbin = 1;
  // for (const char* f : {"pass_trigger", "pass_jetsel", "pass_lepsel", "pass_dispsellept_50um", "nsv_goe_1", "exclude_beampipe", "mintks_4", "min_bs2ddist", "max_rescale_bs2derr"})
  //   h_selB_cutflow->GetXaxis()->SetBinLabel(tbin++, f);

  // h_event_cutflow = fs->make<TH1D>("h_event_cutflow", ";events", 8, 0, 8);
  // int vbin = 1;
  // for (const char* v : {"pass_trigger", "pass_jetsel", "pass_ID", "pass_pt", "pass_eta", "pass_iso", "pass_displept_50um", "pass_dispsellept_50um" })
  //   h_event_cutflow->GetXaxis()->SetBinLabel(vbin++, v);

  h_lepton_cutflow = fs->make<TH1D>("h_lepton_cutflow", ";events", 6, 0, 6);
  int lepbin = 1;
  for (const char* d : {"pass_trigger", "lep_goe_1", "pass_basept", "pass_eta", "pass_ID", "pass_iso"})
    h_lepton_cutflow->GetXaxis()->SetBinLabel(lepbin++, d);

  h_electron_cutflow = fs->make<TH1D>("h_electron_cutflow", ";events", 6, 0, 6);
  int ebin = 1;
  for (const char* f : {"pass_trigger", "ele_goe_1", "pass_basept", "pass_eta", "pass_ID", "pass_iso"})
    h_electron_cutflow->GetXaxis()->SetBinLabel(ebin++, f);

  h_muon_cutflow = fs->make<TH1D>("h_muon_cutflow", ";events", 6, 0, 6);
  int mbin = 1;
  for (const char* g : {"pass_trigger", "mu_goe_1", "pass_basept", "pass_eta", "pass_ID","pass_iso"})
    h_muon_cutflow->GetXaxis()->SetBinLabel(mbin++, g);

  
  
}

void MFVCutFlowHistos::analyze(const edm::Event& event, const edm::EventSetup&) {
  edm::Handle<MFVEvent> mevent;
  event.getByToken(mevent_token, mevent);

  edm::Handle<MFVVertexAuxCollection> auxes;
  event.getByToken(vertex_aux_token, auxes);


  // const int nsv = int(auxes->size());

  bool at_least_one_trigger_passed = false;
  bool  pass_ele_goe = false;
  bool  pass_ele_ID = false;
  bool  pass_ele_pt = false;
  bool  pass_ele_eta = false;
  bool  pass_ele_iso = false;
  bool  pass_mu_goe = false;
  bool  pass_mu_ID = false;
  bool  pass_mu_pt = false;
  bool  pass_mu_eta = false;
  bool  pass_mu_iso = false;
  // bool mevent_pass_displep = false;
  // bool mevent_pass_dispsellep = false;

  // bool vertex_in_beampipe = false;
  // bool vertex_has_min4tks = false;
  // bool vertex_pass_bs2ddist = false;
  // bool vertex_pass_bs2derr = false;
    
 
  for(size_t trig : mfv::LeptonOrDisplacedLeptonTriggers) {
    if (mevent->pass_hlt(trig)) {
      at_least_one_trigger_passed = true;
      break;
    }
  }


  // separate if loop to determine if event pass lepton cuts & fill separate muon, electron cutflows
  if (at_least_one_trigger_passed) {

    if (mevent->nelectrons() > 0) {
      pass_ele_goe = true;
    
      for (int iel = 0; iel < mevent->nelectrons(); ++iel) {
      
      // if (abs(mevent->electron_dxybs[iel]) >= 0.005)
      // 	mevent_pass_displep = true;
	if (mevent->electron_pt[iel] > 35) {
	  pass_ele_pt = true;
	  if (abs(mevent->electron_eta[iel]) < 2.4) {
	    pass_ele_eta = true;
	    if (mevent->electron_ID[iel][3]) {
	      pass_ele_ID = true;
	      if (mevent->electron_iso[iel] < 0.10) {
		pass_ele_iso = true;
        
	      // if (abs(mevent->electron_dxybs[iel]) >= 0.005)
	      //   mevent_pass_dispsellep = true;
	      }
	    }
	  }
	}
      

      // cutflows
	if (mevent->electron_ID[iel][3] == 1) {
	  h_eleiso_cutflow->Fill(isTightEl, 1);
	  if (mevent->electron_iso[iel] < 0.25 )
	    h_eleiso_cutflow->Fill(eliso_vl, 1);
	  if (mevent->electron_iso[iel] < 0.20 )
	    h_eleiso_cutflow->Fill(eliso_l, 1);
	  if (mevent->electron_iso[iel] < 0.15 )
	    h_eleiso_cutflow->Fill(eliso_med, 1);
	  if (mevent->electron_iso[iel] < 0.10 )
	    h_eleiso_cutflow->Fill(eliso_tight, 1);
	  if (mevent->electron_iso[iel] < 0.05 )
	    h_eleiso_cutflow->Fill(eliso_vt, 1);
	}
	
	bool isEB = mevent->electron_isEB[iel] == 1;
	bool isEE = mevent->electron_isEE[iel] == 1;
	if ( !isEB && !isEE ) break;
	
	h_tight_ele_cutflow->Fill(any_electron, 1);
	if ( mevent->electron_sigmaIetaIeta5x5[iel] < (isEB ? 0.0104 : 0.0353) ) {
	  h_tight_ele_cutflow->Fill(full5x5sigmaIetaIeta, 1);
	  
	  if ( mevent->electron_dEtaAtVtx[iel] < (isEB ? 0.00255 : 0.00501) ) {
	    h_tight_ele_cutflow->Fill(delta_eta_seed, 1);
	    
	    if ( mevent->electron_dPhiAtVtx[iel] < (isEB ? 0.022 : 0.0236) ) {
	      h_tight_ele_cutflow->Fill(delta_phi, 1);
	      
	      if ( mevent->electron_HE[iel] == 1 ) {
		h_tight_ele_cutflow->Fill(HoverE, 1);
		
		if ( mevent->electron_ooEmooP[iel] < (isEB ? 0.159 : 0.0197) ) {
		  h_tight_ele_cutflow->Fill(ooEmooP, 1);
		  
		  if ( mevent->electron_expectedMissingInnerHits[iel] < 1 ) {
		    h_tight_ele_cutflow->Fill(expected_missing_inner_hits, 1);
		    if ( mevent->electron_passveto[iel] == 1) {
		      h_tight_ele_cutflow->Fill(pass_conversion_veto, 1);
		    }
		  }
		}
	      }
	    }	  
	  }
	}	
      }
    }
    if (mevent->nmuons() > 0) {
      pass_mu_goe = true;
      for (int imu = 0; imu < mevent->nmuons(); ++imu) {

      // if (abs(mevent->muon_dxybs[imu]) > 0.005) 
      //   mevent_pass_displep = true;
      
	if (mevent->muon_pt[imu] > 26) {
	  pass_mu_pt = true;
	  if (abs(mevent->muon_eta[imu]) < 2.4) {
	    pass_mu_eta = true;
	    if (mevent->muon_ID[imu][1] == 1) {
	      pass_mu_ID = true;
	      if (mevent->muon_iso[imu] < 0.15) {
	        pass_mu_iso = true;
	   
	      // if (abs(mevent->muon_dxybs[imu]) > 0.005) 
	      // 	mevent_pass_dispsellep = true;
	      }
	    }
	  }
	}    
      
	if (mevent->muon_ID[imu][1] == 1) {
	  h_muiso_cutflow->Fill(isMedMuon, 1);
	  
	  if (mevent->muon_iso[imu] < 0.4 )
	    h_muiso_cutflow->Fill(muiso_vl, 1);
	  if (mevent->muon_iso[imu] < 0.25 )
	    h_muiso_cutflow->Fill(muiso_l, 1);
	  if (mevent->muon_iso[imu] < 0.20 )
	    h_muiso_cutflow->Fill(muiso_med, 1);
	  if (mevent->muon_iso[imu] < 0.15 )
	    h_muiso_cutflow->Fill(muiso_tight, 1);
	  if (mevent->muon_iso[imu] < 0.10 )
	    h_muiso_cutflow->Fill(muiso_vt, 1);
	}
      }
    }
  }

  //separate section to determine if vertex passes cuts

  // bool at_least_one_vertex = false;
  
  // if (nsv >= 1) {
  //   at_least_one_vertex = true;
  // }
    
  // for (const MFVVertexAux& vtx : *auxes) {
  //   if (jmt::Geometry::inside_beampipe(true, vtx.x, vtx.y)) {
  //     vertex_in_beampipe = true;
      
  //     if (vtx.ntracks() >= 4) {
  // 	vertex_has_min4tks = true;
    
  // 	if (vtx.bs2ddist > 0.001) {
  // 	  vertex_pass_bs2ddist = true;
    
  // 	  if (vtx.bs2derr < 0.0025) {
  // 	    vertex_pass_bs2derr = true;
	    
  // 	  }
  // 	}
  //     }
  //   }
  // }

  // now to fill the event & sel cutflows 
  // if (at_least_one_trigger_passed) {

    // h_event_cutflow->Fill(pass_trigger, 1);
    // h_selA_cutflow->Fill(Apass_trigger, 1);
    // h_selB_cutflow->Fill(Bpass_trigger, 1);
    
    // if (mevent->njets(20) > 1) {
      
    //   h_event_cutflow->Fill(pass_jetsel, 1);
    //   h_selA_cutflow->Fill(Apass_jetsel, 1);
    //   h_selB_cutflow->Fill(Bpass_jetsel, 1);
      
  //     if (mevent_pass_ID) {
  // 	h_event_cutflow->Fill(pass_ID, 1);
  // 	if (mevent_pass_pt) {
  // 	  h_event_cutflow->Fill(pass_pt, 1);
  // 	  if (mevent_pass_eta) {
  // 	    h_event_cutflow->Fill(pass_eta, 1);
  // 	    if (mevent_pass_iso) {
  // 	      h_event_cutflow->Fill(pass_iso, 1);
  // 	      if (mevent_pass_displep) {
  // 		h_event_cutflow->Fill(pass_displept_50um, 1);
  // 		if (mevent_pass_dispsellep) {
  // 		  h_event_cutflow->Fill(pass_dispsellept_50um, 1);
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
  //     }
      
  //     if (mevent_pass_lepsel) {
  // 	h_selA_cutflow->Fill(Apass_lepsel, 1);
  // 	h_selB_cutflow->Fill(Bpass_lepsel, 1);

  // 	if (mevent_pass_displep) {
  // 	  h_selA_cutflow->Fill(Apass_displept_50um, 1);
  // 	  if (at_least_one_vertex) {
  // 	    h_selA_cutflow->Fill(Ansv_goe_1, 1);
  // 	    if (vertex_in_beampipe) {
  // 	      h_selA_cutflow->Fill(Aexclude_beampipe, 1);
  // 	      if(vertex_has_min4tks) {
  // 		h_selA_cutflow->Fill(Amintks_4, 1);
  // 		if(vertex_pass_bs2ddist) {
  // 		  h_selA_cutflow->Fill(Amin_bs2ddist, 1);
  // 		  if(vertex_pass_bs2derr) {
  // 		    h_selA_cutflow->Fill(Amax_rescale_bs2derr, 1);
  // 		  }
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
	 
  // 	if (mevent_pass_dispsellep) {
  // 	  h_selB_cutflow->Fill(Bpass_dispsellept_50um, 1);
  // 	  if (at_least_one_vertex) {
  // 	    h_selB_cutflow->Fill(Bnsv_goe_1, 1);
  // 	    if (vertex_in_beampipe) {
  // 	      h_selB_cutflow->Fill(Bexclude_beampipe, 1);
  // 	      if(vertex_has_min4tks) {
  // 		h_selB_cutflow->Fill(Bmintks_4, 1);
  // 		if(vertex_pass_bs2ddist) {
  // 		  h_selB_cutflow->Fill(Bmin_bs2ddist, 1);		    
  // 		  if(vertex_pass_bs2derr) {
  // 		    h_selB_cutflow->Fill(Bmax_rescale_bs2derr, 1);

  // 		  }
  // 		}
  // 	      }
  // 	    }
  // 	  }
  // 	}
  //     }
  //   }
  // }

  //fill the lepton cutflows
  if (at_least_one_trigger_passed) {
    h_lepton_cutflow->Fill(l_pass_trig, 1);
    h_electron_cutflow->Fill(e_pass_trig, 1);
    h_muon_cutflow->Fill(m_pass_trig, 1);

    if (pass_ele_goe) {
      h_electron_cutflow->Fill(pass_egoe, 1);
      if (pass_ele_pt) {
	h_electron_cutflow->Fill(pass_ept, 1);
	if (pass_ele_eta) {
	  h_electron_cutflow->Fill(pass_eeta, 1);
	  if (pass_ele_ID) {
	    h_electron_cutflow->Fill(pass_eID, 1);
	    if (pass_ele_iso) {
	      h_electron_cutflow->Fill(pass_eiso, 1);
	    }
	  }
	}
      }
    }
    if (pass_mu_goe) {
      h_muon_cutflow->Fill(pass_mgoe, 1);
      if (pass_mu_pt) {
	h_muon_cutflow->Fill(pass_mpt, 1);
	if (pass_mu_eta) {
	  h_muon_cutflow->Fill(pass_meta, 1);
	  if (pass_mu_ID) {
	    h_muon_cutflow->Fill(pass_mID, 1);
	    if (pass_mu_iso) {
	      h_muon_cutflow->Fill(pass_miso, 1);
	    }
	  }
	}
      }
    }
    if (pass_mu_goe || pass_ele_goe) {
      h_lepton_cutflow->Fill(pass_lepgoe, 1);
      if (pass_mu_pt || pass_ele_pt) {
	h_lepton_cutflow->Fill(pass_leppt, 1);
	if (pass_mu_eta || pass_ele_eta) {
	  h_lepton_cutflow->Fill(pass_lepeta, 1);
	  if (pass_mu_ID || pass_ele_ID) {
	    h_lepton_cutflow->Fill(pass_lepID, 1);
	    if (pass_mu_iso || pass_ele_iso) {
	      h_lepton_cutflow->Fill(pass_lepiso, 1);
	    }
	  }
	}
      }
    }
  }

}

DEFINE_FWK_MODULE(MFVCutFlowHistos);
