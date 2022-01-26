// #include "CommonTools/UtilAlgos/interface/TFileService.h"
// #include "TH2F.h"
// #include "DataFormats/Math/interface/deltaPhi.h"
// #include "FWCore/Framework/interface/EDFilter.h"
// #include "FWCore/Framework/interface/Event.h"
// #include "FWCore/Framework/interface/Frameworkfwd.h"
// #include "FWCore/ServiceRegistry/interface/Service.h"
// #include "FWCore/Framework/interface/MakerMacros.h"
// #include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
// #include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
// #include "JMTucker/MFVNeutralino/interface/EventTools.h"

// //also need to include things for creating histograms (hopefully this can be done with EDFilter)
// /// honestly, I think this can be done using just another analyzer. not a filter. 

// class MFVCutFlowCuts : public edm::EDFilter {
// public:
//   explicit MFVCutFlowCuts(const edm::ParameterSet&);

// private:
//   virtual bool filter(edm::Event&, const edm::EventSetup&);
//   const edm::InputTag mevent_src;
//   const edm::EDGetTokenT<MFVEvent> mevent_token;
//   const edm::EDGetTokenT<MFVVertexAuxCollection> tk5_vertex_token;
//   const edm::EDGetTokenT<MFVVertexAuxCollection> tk4_vertex_token;
//   const edm::EDGetTokenT<MFVVertexAuxCollection> tk3_vertex_token;

//   const bool use_mevent;
//   const int apply_presel;
//   const int apply_trigger;
//   const bool apply_vertex_cuts;

//   enum {pass_trigger, pass_lepsel, pass_jetsel};
//   TH1D* h_event_cutflow;
  
//   enum {Min3tk_Min1sv, Min4tk_Min1sv, Min5tk_Min1sv, Min3tk_Min2sv, Min4tk_Min2sv, Min5tk_Min2sv};
//   TH1D* h_vertex_cutflow;

//   enum { any_electron, full5x5sigmaIetaIeta, delta_eta_seed, delta_phi, HoverE, ooEmooP, expected_missing_inner_hits, pass_conversion_veto, PF_Iso};
//   TH1D* h_loose_ele_cutflow;

//   enum { isVetoEle, isLooseEle, isMedEle, isTightEle};
//   TH1D* h_electron_cutflow;
  
//   enum { isLooseMuon, isMedMuon, isTightMuon};
//   TH1D* h_muon_cutflow;
  
// };

// MFVCutFlowCuts::MFVCutFlowCuts(const edm::ParameterSet& cfg)
//   : mevent_src(cfg.getParameter<edm::InputTag>("mevent_src")),
//     mevent_token(consumes<MFVEvent>(mevent_src)),
//     tk5_vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("tk5_vertex_src"))),
//     tk4_vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("tk4_vertex_src"))),
//     tk3_vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("tk3_vertex_src"))),

//     use_mevent(mevent_src.label() != ""),
//     apply_presel(cfg.getParameter<int>("apply_presel")),
//     apply_trigger(apply_presel ? 0 : cfg.getParameter<int>("apply_trigger")),
//     apply_vertex_cuts(cfg.getParameter<bool>("apply_vertex_cuts"))


//     //anything else?

// {
//   edm::Service<TFileService> fs;

//   h_event_cutflow = fs->make<TH1D>("h_event_cutflow", ";events", 3, 0, 3);
//   int evbin = 1;
//   for (const char* x : {"pass_trigger", "pass_lepsel", "pass_jetsel"})
//     h_event_cutflow->GetXaxis()->SetBinLabel(evbin++, x);

//   h_vertex_cutflow = fs->make<TH1D>("h_vertex_cutflow", ";events", 6, 0, 6);
//   int vbin = 1;
//   for (const char* y : {"Min3tk_Min1sv", "Min4tk_Min1sv", "Min5tk_Min1sv", "Min3tk_Min2sv", "Min4tk_Min2sv", "Min5tk_Min2sv"})
//     h_vertex_cutflow->GetXaxis()->SetBinLabel(vbin++, y);

//   h_loose_ele_cutflow = fs->make<TH1D>("h_loose_ele_cuflow", ";events", 9, 0, 9);
//   int elbin = 1;
//   for (const char* a : {"any_electron", "full5x5sigmaIetaIeta", "delta_eta_seed", "delta_phi", "HoverE", "ooEmooP", "expected_missing_inner_hits", "pass_conversion_veto", "PF_Iso"})
//     h_loose_ele_cutflow->GetXaxis()->SetBinLabel(elbin++, a);

//   h_electron_cutflow = fs->make<TH1D>("h_electron_cutflow", ";events", 4, 0 ,4);
//   int ebin = 1;
//   for (const char* c : {"isVetoEle", "isLooseEle", "isMedEle", "isTightEle"})
//     h_electron_cutflow->GetXaxis()->SetBinLabel(ebin++, c);
  
//   h_muon_cutflow = fs->make<TH1D>("h_muon_cutflow", ";events", 3, 0, 3);
//   int mubin=1;
//   for (const char* b : {"isLooseMuon", "isMedMuon", "isTightMuon"})
//     h_muon_cutflow->GetXaxis()->SetBinLabel(mubin++, b);

  
// }

// bool MFVCutFlowCuts::filter(edm::Event& event, const edm::EventSetup&) {
//   edm::Handle<MFVEvent> mevent;




//   ////////////////////////////////////////////////////////////////////////////////////////////
//   if (use_mevent) {
//     event.getByToken(mevent_token, mevent);


//     //preselection is currently just passing trigger which makes the next, apply trigger, mute 
//     if (apply_presel == 2) {
//       bool success = false;
//       for(size_t trig : mfv::LeptonOrDisplacedLeptonTriggers){
// 	if (mevent->pass_hlt(trig)) {
// 	  success = true;

// 	  h_event_cutflow->Fill(pass_trigger, 1);
// 	  // std::cout << "found event that passes a trigger" << std::endl;
// 	  break;
// 	}
//       }
//       //  if (!success) return false;
//     }

//     //just the trigger
//     if (apply_trigger == 2) {
//       bool at_least_one_trigger_passed = false;
//       for(size_t trig : mfv::LeptonOrDisplacedLeptonTriggers){
// 	if(mevent->pass_hlt(trig)){
// 	  at_least_one_trigger_passed = true;
// 	  break;
// 	}
//       }
//       //  if(!at_least_one_trigger_passed) return false;
//     }


//     //electron and muon cutflows; after pass trigger ... (is this what we want?)
//     //need to check logic
    
//     // electrons

//     // just to make things a bit easier later on; not pretty but gets the job done
//     bool pass_loose_ele = false;
//     //  bool pass_veto_ele = false;
//     //  bool pass_med_ele = false;
//     //  bool pass_tight_ele = false;
//     //  bool pass_loose_mu = false;
//     bool pass_med_mu = false;
//     // bool pass_tight_mu = false;
    
//     for (int iel = 0; iel < mevent->nelectrons(); ++iel) {
	
//       bool isEB = mevent->electron_isEB[iel] == 1;
//       bool isEE = mevent->electron_isEE[iel] == 1;
//       h_loose_ele_cutflow->Fill(any_electron, 1);

//       if ( !isEB && !isEE ) return false;
      
//       if ( mevent->electron_sigmaIetaIeta5x5[iel] < (isEB ? 0.0112 : 0.0425) ) {
// 	h_loose_ele_cutflow->Fill(full5x5sigmaIetaIeta, 1);
	
// 	if ( mevent->electron_dEtaAtVtx[iel] < (isEB ? 0.00377 : 0.00674) ) {
// 	  h_loose_ele_cutflow->Fill(delta_eta_seed, 1);
	  
// 	  if ( mevent->electron_dPhiAtVtx[iel] < (isEB ? 0.0884 : 0.169) ) {
// 	    h_loose_ele_cutflow->Fill(delta_phi, 1);
	    
// 	    if ( mevent->electron_HE[iel] == 1 ) {
// 	      h_loose_ele_cutflow->Fill(HoverE, 1);
	      
// 	      if ( mevent->electron_ooEmooP[iel] < (isEB ? 0.193 : 0.111) ) {
// 		h_loose_ele_cutflow->Fill(ooEmooP, 1);
		
// 		if ( mevent->electron_expectedMissingInnerHits[iel] < 1 ) {
// 		  h_loose_ele_cutflow->Fill(expected_missing_inner_hits, 1);
		  
// 		  if (mevent->electron_passveto[iel] == 1) {
// 		    h_loose_ele_cutflow->Fill(pass_conversion_veto, 1);
		    
// 		    if (mevent->electron_iso[iel] < (isEB ? 0.112+0.506/mevent->electron_pt[iel] : 0.108+0.963/mevent->electron_pt[iel]) ) {
// 		      h_loose_ele_cutflow->Fill(PF_Iso, 1);
// 		    }
// 		  }
// 		}
// 	      }
// 	    }
// 	  }
// 	}
//       }

//       // currently filling the lepton cutflows AFTER PT cut. Is this what we want? 
//       if (mevent->electron_pt[iel] > 32) {
	
// 	// if (mevent->electron_ID[iel][1] == 1) {
// 	//   h_electron_cutflow->Fill(isVetoEle, 1);
// 	//   pass_veto_ele = true;
// 	// }
// 	if (mevent->electron_ID[iel][2] == 1) {
// 	  h_electron_cutflow->Fill(isLooseEle, 1);
// 	  pass_loose_ele = true;
// 	}
// 	// if (mevent->electron_ID[iel][3] == 1) {
// 	//   h_electron_cutflow->Fill(isMedEle, 1);
// 	//   pass_med_ele = true;
// 	// }
// 	// if (mevent->electron_ID[iel][4] == 1) {
// 	//   h_electron_cutflow->Fill(isTightEle, 1);
// 	//   pass_tight_ele = true;
// 	// }
//       }
//     }

    
    
    
//     for (int imu = 0; imu < mevent->nmuons(); ++imu) {

//       if (mevent->muon_pt[imu] > 24) {
	
// 	// if (mevent->muon_ID[imu][0] == 1) {
// 	//   h_muon_cutflow->Fill(isLooseMuon, 1);
// 	//   pass_loose_mu = true;
// 	// }
// 	if (mevent->muon_ID[imu][1] == 1) {
// 	  h_muon_cutflow->Fill(isMedMuon, 1);
// 	  pass_med_mu = true;
// 	}
// 	// if(mevent->muon_ID[imu][2] == 1) {
// 	//   h_muon_cutflow->Fill(isTightMuon, 1);
// 	//   pass_tight_mu = true;
// 	// }
//       }
//     }
//     //pass lepton selection; currently need to find at least 1 good lepton
//     // either: med  cutbased muon OR loose cutbased electron with pt > 24/32 GeV

//     //the event cutflow only matters when we are applying lepton selection criteria;
//     // remember that this filter is applied independently of analysis cuts 
//     if ( pass_med_mu || pass_loose_ele ) {
//       //  return false;

//       h_event_cutflow->Fill(pass_lepsel, 1);
    
//       //njets; 
//       if (mevent->njets(20) < 2 || mevent->njets(20) > 100000)
// 	// return false;


// 	h_event_cutflow->Fill(pass_jetsel, 1);
//     }

//     ////////////////////////////////////////////////////////////////////////////////////////////
    
//     if (apply_vertex_cuts) {
//       edm::Handle<MFVVertexAuxCollection> tk5_vertices;
//       event.getByToken(tk5_vertex_token, tk5_vertices);

//       edm::Handle<MFVVertexAuxCollection> tk4_vertices;
//       event.getByToken(tk4_vertex_token, tk4_vertices);

//       edm::Handle<MFVVertexAuxCollection> tk3_vertices;
//       event.getByToken(tk3_vertex_token, tk3_vertices);
      
//       const int tk5_nsv = int(tk5_vertices->size());
//       const int tk4_nsv = int(tk4_vertices->size());
//       const int tk3_nsv = int(tk3_vertices->size());

//       if (tk3_nsv < 1)
// 	return false;

//       if (tk3_nsv >= 1)
// 	h_vertex_cutflow->Fill(Min3tk_Min1sv, 1);
//       if (tk4_nsv >= 1)
//       	h_vertex_cutflow->Fill(Min4tk_Min1sv, 1);
//       if (tk5_nsv >= 1)
//       	h_vertex_cutflow->Fill(Min5tk_Min1sv, 1);

//       if (tk3_nsv >= 2)
// 	h_vertex_cutflow->Fill(Min3tk_Min2sv, 1);
//       if (tk4_nsv >= 2)
//       	h_vertex_cutflow->Fill(Min4tk_Min2sv, 1);
//       if (tk5_nsv >= 2)
//       	h_vertex_cutflow->Fill(Min5tk_Min2sv, 1);
      
//     }
//   }  
//   return true;
// }

// DEFINE_FWK_MODULE(MFVCutFlowCuts);
