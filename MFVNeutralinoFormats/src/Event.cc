#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/TrackReco/interface/Track.h"

void MFVEvent::muon_push_back(const reco::Muon& muon,
			      const reco::Track& trk,
			      const math::XYZPoint& beamspot,
                              const math::XYZPoint& primary_vertex) {

  muon_pt.push_back(muon.pt());
  muon_eta.push_back(muon.eta());
  muon_phi.push_back(muon.phi());
  muon_pt_err.push_back(trk.ptError());
  muon_eta_err.push_back(trk.etaError());
  muon_phi_err.push_back(trk.phiError());
  
  muon_dxy.push_back(trk.dxy(primary_vertex));
  muon_dz.push_back(trk.dz(primary_vertex));
  muon_dxybs.push_back(trk.dxy(beamspot));
  muon_dxyerr.push_back(trk.d0Error());
  muon_dzerr.push_back(trk.dzError());
  

  muon_chi2dof.push_back(trk.normalizedChi2());
  muon_hp_push_back(trk.hitPattern().numberOfValidPixelHits(),
		   trk.hitPattern().numberOfValidStripHits(),
		   trk.hitPattern().pixelLayersWithMeasurement(),
                   trk.hitPattern().stripLayersWithMeasurement());
  
}

void MFVEvent::electron_push_back(const reco::GsfElectron& electron,
				  const reco::Track& trk,
				  const math::XYZPoint& beamspot,
				  const math::XYZPoint& primary_vertex) {

   electron_pt.push_back(electron.pt());
   electron_eta.push_back(electron.eta());
   electron_phi.push_back(electron.phi());
   electron_pt_err.push_back(trk.ptError());
   electron_eta_err.push_back(trk.etaError());
   electron_phi_err.push_back(trk.phiError());

   electron_dxy.push_back(trk.dxy(primary_vertex));
   electron_dz.push_back(trk.dz(primary_vertex));
   electron_dxybs.push_back(trk.dxy(beamspot));
   electron_dxyerr.push_back(trk.d0Error());
   electron_dzerr.push_back(trk.dzError());
   

   electron_chi2dof.push_back(trk.normalizedChi2());
   electron_hp_push_back(trk.hitPattern().numberOfValidPixelHits(),
			 trk.hitPattern().numberOfValidStripHits(),
			 trk.hitPattern().pixelLayersWithMeasurement(),
			 trk.hitPattern().stripLayersWithMeasurement());

}

  
void MFVEvent::jet_hlt_push_back(const reco::Candidate& jet, const std::vector<TLorentzVector>& hltjets, bool is_displaced_calojets){

  // use dR = 0.4 for the matching (in eta x phi)
  double hltmatchdist2 = 0.4*0.4;
  TLorentzVector hltmatch;
  for (auto hlt : hltjets) {
    const double dist2 = reco::deltaR2(jet.eta(), jet.phi(), hlt.Eta(), hlt.Phi());
    if (dist2 < hltmatchdist2) {
      hltmatchdist2 = dist2;
      hltmatch = hlt;
    }
  }

  if(is_displaced_calojets){
    displaced_jet_hlt_pt.push_back(hltmatch.Pt());
    displaced_jet_hlt_eta.push_back(hltmatch.Eta());
    displaced_jet_hlt_phi.push_back(hltmatch.Phi());
    displaced_jet_hlt_energy.push_back(hltmatch.E());
  }
  else{
    jet_hlt_pt.push_back(hltmatch.Pt());
    jet_hlt_eta.push_back(hltmatch.Eta());
    jet_hlt_phi.push_back(hltmatch.Phi());
    jet_hlt_energy.push_back(hltmatch.E());
  }
}

  
  
					  
                 
