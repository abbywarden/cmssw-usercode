#include "TVector3.h"
#include "CLHEP/Random/RandomEngine.h"
#include "CLHEP/Random/RandExponential.h"
#include "CLHEP/Random/RandGauss.h"
#include "CLHEP/Random/RandBinomial.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Utilities/interface/RandomNumberGenerator.h"
#include "JMTucker/Formats/interface/TracksMap.h"
#include "JMTucker/Tools/interface/BTagging.h"
#include "JMTucker/Tools/interface/TrackRefGetter.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerFloats.h"


class MFVTrackMover : public edm::EDProducer {
public:
  explicit MFVTrackMover(const edm::ParameterSet&);

private:
  virtual void produce(edm::Event&, const edm::EventSetup&);

  const edm::EDGetTokenT<reco::TrackCollection> tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> electron_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> muon_tracks_token;
  const edm::EDGetTokenT<reco::VertexCollection> primary_vertices_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_token;
  const edm::EDGetTokenT<pat::ElectronCollection> electrons_token;
  const edm::EDGetTokenT<double> rho_token;
  EffectiveAreas electron_effective_areas;
  const edm::EDGetTokenT<mfv::TriggerFloats> triggerfloats_token;

  jmt::TrackRefGetter track_ref_getter;

  const double min_jet_pt;
  const unsigned min_jet_ntracks;

  const unsigned njets;
  const unsigned nbjets;
  const unsigned nlep;
  const double tau;
  const bool use_separated_leptons;
  const bool halftoss;
  const double sig_theta;
  const double sig_phi;

};

MFVTrackMover::MFVTrackMover(const edm::ParameterSet& cfg) 
  : tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("tracks_src"))),
    electron_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("electron_tracks_src"))),
    muon_tracks_token(consumes<reco::TrackCollection>(cfg.getParameter<edm::InputTag>("muon_tracks_src"))),
    primary_vertices_token(consumes<reco::VertexCollection>(cfg.getParameter<edm::InputTag>("primary_vertices_src"))),
    jets_token(consumes<pat::JetCollection>(cfg.getParameter<edm::InputTag>("jets_src"))),
    muons_token(consumes<pat::MuonCollection>(cfg.getParameter<edm::InputTag>("muons_src"))),
    electrons_token(consumes<pat::ElectronCollection>(cfg.getParameter<edm::InputTag>("electrons_src"))),
    rho_token(consumes<double>(cfg.getParameter<edm::InputTag>("rho_src"))),
    electron_effective_areas(cfg.getParameter<edm::FileInPath>("electron_effective_areas").fullPath()),
	  triggerfloats_token(consumes<mfv::TriggerFloats>(cfg.getParameter<edm::InputTag>("triggerfloats_src"))),

    track_ref_getter(cfg.getParameter<std::string>("@module_label"),
                         cfg.getParameter<edm::ParameterSet>("track_ref_getter"),
                         consumesCollector()),
    min_jet_pt(cfg.getParameter<double>("min_jet_pt")),
    min_jet_ntracks(cfg.getParameter<unsigned>("min_jet_ntracks")),
    njets(cfg.getParameter<unsigned>("njets")),
    nbjets(cfg.getParameter<unsigned>("nbjets")),
    nlep(cfg.getParameter<unsigned>("nlep")),
    tau(cfg.getParameter<double>("tau")),
    use_separated_leptons(cfg.getParameter<bool>("use_separated_leptons")),
    halftoss(cfg.getParameter<bool>("halftoss")),
    sig_theta(cfg.getParameter<double>("sig_theta")),
    sig_phi(cfg.getParameter<double>("sig_phi"))

{
  edm::Service<edm::RandomNumberGenerator> rng;
  if (!rng.isAvailable())
    throw cms::Exception("MFVTrackMover", "RandomNumberGeneratorService not available");

  produces<reco::TrackCollection>();
  produces<jmt::TracksMap>();
  produces<reco::TrackCollection>("moved");
  //below are filled only if use_separated_leptons is True 
  produces<reco::TrackCollection>("electrons");
  produces<jmt::TracksMap>("elemap");
  produces<reco::TrackCollection>("movedele");
  produces<reco::TrackCollection>("muons");
  produces<jmt::TracksMap>("mumap");
  produces<reco::TrackCollection>("movedmu");
  
  produces<int>("npreseljets");
  produces<int>("npreselbjets");
  produces<int>("npreselele");
  produces<int>("npreselmu");
  produces<pat::JetCollection>("jetsUsed");
  produces<pat::JetCollection>("bjetsUsed");
  produces<pat::MuonCollection>("muonsUsed");
  produces<pat::ElectronCollection>("eleUsed");
  produces<std::vector<double> >("flightAxis");
  produces<std::vector<double> >("moveVertex");
  produces<std::vector<double> >("moveLepPos");
  // produces<std::vector<std::vector<double>> >("moveJetPos");
  produces<std::vector<double> >("moveJetPos");
  produces<double>("jetlepdeltadz");

}

void MFVTrackMover::produce(edm::Event& event, const edm::EventSetup&) {
  edm::Service<edm::RandomNumberGenerator> rng;
  CLHEP::HepRandomEngine& rng_engine = rng->getEngine(event.streamID());

  auto knuth_select = [&rng_engine](int n, int N) -> std::vector<int> {
    std::vector<int> ts;
    int t = 0, m = 0;
    while (m < n) {
      if ((N - t) * rng_engine.flat() >= n - m)
        ++t;
      else {
        ++m;
        ts.push_back(t++);
      }
    }
    return ts;
  };

  auto output_tracks = std::make_unique<reco::TrackCollection>();
  reco::TrackRefProd h_output_tracks = event.getRefBeforePut<reco::TrackCollection>();
  auto output_tracks_map = std::make_unique<jmt::TracksMap>();
  auto moved_tracks = std::make_unique<reco::TrackCollection>(); // JMTBAD just write a vector<bool> and pick it up in MovedTracksTreer

  //below are filled only if use_separated_leptons is True 
  auto output_electron_tracks = std::make_unique<reco::TrackCollection>();
  reco::TrackRefProd h_output_eletracks = event.getRefBeforePut<reco::TrackCollection>();
  auto output_eletracks_map = std::make_unique<jmt::TracksMap>();
  auto moved_electron_tracks = std::make_unique<reco::TrackCollection>();

  auto output_muon_tracks = std::make_unique<reco::TrackCollection>();
  reco::TrackRefProd h_output_mutracks = event.getRefBeforePut<reco::TrackCollection>();
  auto output_mutracks_map = std::make_unique<jmt::TracksMap>();
  auto moved_muon_tracks = std::make_unique<reco::TrackCollection>();

  //
  auto npreseljets = std::make_unique<int>();
  auto npreselbjets = std::make_unique<int>();
  auto npreselele = std::make_unique<int>();
  auto npreselmu = std::make_unique<int>();
  auto jets_used = std::make_unique<pat::JetCollection>();
  auto bjets_used = std::make_unique<pat::JetCollection>();
  auto muons_used = std::make_unique<pat::MuonCollection>();
  auto ele_used = std::make_unique<pat::ElectronCollection>();
  auto flight_vect = std::make_unique<std::vector<double>>(3, 0.);
  auto move_vertex = std::make_unique<std::vector<double>>(3, 0.);
  auto move_lep_pos = std::make_unique<std::vector<double>>(3, 0.);
  // auto move_jet_pos = std::make_unique<std::vector<std::vector<double>>>(3, 0.);
  auto move_jet_pos = std::make_unique<std::vector<double>>(3, 0.);
  auto jetlepdeltadz = std::make_unique<double>();
  edm::Handle<reco::VertexCollection> primary_vertices;
  event.getByToken(primary_vertices_token, primary_vertices);
  const reco::Vertex* pv = primary_vertices->size() ? &(*primary_vertices)[0] : 0;

  if (pv) {
    edm::Handle<pat::JetCollection> jets;
    event.getByToken(jets_token, jets);
    
    edm::Handle<pat::MuonCollection> muons;
    edm::Handle<pat::ElectronCollection> electrons;
    event.getByToken(muons_token, muons);
    event.getByToken(electrons_token, electrons);

    edm::Handle<mfv::TriggerFloats> triggerfloats;
    event.getByToken(triggerfloats_token, triggerfloats);

    edm::Handle<double> rho;
    event.getByToken(rho_token, rho);

    CLHEP::RandExponential rexp(rng_engine);
    CLHEP::RandGauss rgau(rng_engine);
    CLHEP::RandBinomial rint(rng_engine);

    std::vector<const pat::Jet*> presel_jets;
    std::vector<const pat::Jet*> presel_bjets;
    std::vector<const pat::Muon*> presel_mu;
    std::vector<const pat::Electron*> presel_ele;
    std::vector<const pat::Jet*> selected_jets;
    std::vector<const pat::Muon*> selected_mu;
    std::vector<const pat::Electron*> selected_ele;

    TVector3 move;


    // Pick the lepton we'll use. --> want : picking the triggered lepton 
    for (const pat::Muon& muon : *muons) {

      //triggered lepton 
      double hltmatchdist2 = 0.1;
      double best_hltmatchdR = 5.;
      TLorentzVector hltmatch;
      for (auto hlt : triggerfloats->hltmuons) {
        const double dist2 = reco::deltaR2(muon.eta(), muon.phi(), hlt.Eta(), hlt.Phi());
        if (dist2 < best_hltmatchdR) best_hltmatchdR = dist2;
        if (dist2 < hltmatchdist2) {
          hltmatchdist2 = dist2;
          hltmatch = hlt;
        }
      }

      bool isHLTMu = hltmatch.Pt() > 0;
      bool isMedMuon = muon.passed(reco::Muon::CutBasedIdMedium);
      // bool isTightMuon = muon.passed(reco::Muon::CutBasedIdTight); //for the dz, d0 cuts... but could go tighter
      if (isMedMuon && muon.pt() > 5 && abs(muon.eta()) < 2.4 && isHLTMu) {
        const float iso = (muon.pfIsolationR04().sumChargedHadronPt + std::max(0., muon.pfIsolationR04().sumNeutralHadronEt + muon.pfIsolationR04().sumPhotonEt -0.5*muon.pfIsolationR04().sumPUPt))/muon.pt();
        if (iso < 0.1) {
          presel_mu.push_back(&muon);
        }
      }
    }
    for (const pat::Electron& electron : *electrons) {

      double hltmatchdist2 = 0.1;
      double best_hltmatchdR = 5.;
      TLorentzVector hltmatch;
      for (auto hlt : triggerfloats->hltelectrons) {
        const double dist2 = reco::deltaR2(electron.eta(), electron.phi(), hlt.Eta(), hlt.Phi());
        if (dist2 < best_hltmatchdR) best_hltmatchdR = dist2;
        if (dist2 < hltmatchdist2) {
          hltmatchdist2 = dist2;
          hltmatch = hlt;
        }
      }

      bool isHLTEle = hltmatch.Pt() > 0;
      bool isTightEl = electron.electronID("cutBasedElectronID-Fall17-94X-V1-tight");
      const bool passveto = electron.passConversionVeto();


      if (isTightEl && passveto && electron.pt() > 5 && abs(electron.eta()) < 2.4 && isHLTEle) {

        // const bool eleprompt_dxy = fabs(electron.eta()) < 1.479 ? (electron.gsfTrack()->dxy(primary_vertices->at(0).position()) < 0.05) : (electron.gsfTrack()->dxy(primary_vertices->at(0).position()) < 0.10);
        // const bool eleprompt_dz = fabs(electron.eta()) < 1.479 ? (electron.gsfTrack()->dz(primary_vertices->at(0).position()) < 0.05) : (electron.gsfTrack()->dz(primary_vertices->at(0).position()) < 0.10);
        // const bool eleprompt = eleprompt_dxy && eleprompt_dz;

        // bool h_Escaled = electron.hadronicOverEm() < (electron.isEB() ? 0.05 + 1.12 + 0.0368 * *rho : 0.0414 + 0.5 + 0.201 * *rho) / electron.superCluster()->energy();
        // float ooEmooP = fabs(1.0/electron.ecalEnergy() - electron.eSuperClusterOverP()/electron.ecalEnergy() );
        // int expectedMissingInnerHits = electron.gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);

        const auto pfIso = electron.pfIsolationVariables();
        const float eA = electron_effective_areas.getEffectiveArea(fabs(electron.superCluster()->eta()));
        const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - *rho*eA)) / electron.pt();
        if (abs(electron.eta() <= 1.479)) {
          if (iso < (0.0287 + 0.506/electron.pt())) {
            // if (eleprompt)
            presel_ele.push_back(&electron);
          }
        }
        else {
          if (iso < (0.0445 + 0.963/electron.pt())) {
            // if (eleprompt)
            presel_ele.push_back(&electron);
          }
        }
      }
    }
    // std::cout << "presel ele and mu size : " << presel_ele.size() << " " << presel_mu.size() << std::endl;
    *npreselele = presel_ele.size();
    *npreselmu = presel_mu.size();

    // Pick the (b-)jets we'll use.
    //keep track of the jet's average dz to be used to decide which jet to move 
    std::vector<double> presel_jet_avgdz; //need to repeat for bjets when ready
    for (const pat::Jet& jet : *jets) {
      if (jet.pt() < min_jet_pt || track_ref_getter.tracks(event, jet).size() < min_jet_ntracks)
        continue;
      int muonjets = 0;
      for (const pat::Muon& muon : *muons) {
        bool isLooseMuon = muon.passed(reco::Muon::CutBasedIdLoose);
        double ljet_absdR = reco::deltaR(muon.eta(), muon.phi(), jet.eta(), jet.phi()); 
        if (isLooseMuon && abs(ljet_absdR) < 0.4) muonjets++;
      }
      int elejets = 0;
      for (const pat::Electron& electron : *electrons) {
        bool isTightEl = electron.electronID("cutBasedElectronID-Fall17-94X-V1-tight");
        double ljet_absdR = reco::deltaR(electron.eta(), electron.phi(), jet.eta(), jet.phi()); 
        if (isTightEl && abs(ljet_absdR) < 0.4) elejets++;
      }
      if (muonjets > 0 || elejets > 0)
        continue;
      const double b_disc = jmt::BTagging::discriminator(jet);
      if (b_disc < jmt::BTagging::discriminator_min(jmt::BTagging::loose)) { 
        presel_jets.push_back(&jet);

        //step 1 : get jet tracks 
        std::set<reco::TrackRef> jet_tracks;
        for (auto r : track_ref_getter.tracks(event, jet))
          jet_tracks.insert(r);
        const size_t n_jet_tracks = jet_tracks.size();
        //step 2 : get the average dz
        double jettk_sumdz = 0;
        for (auto r : jet_tracks)
          jettk_sumdz += r->dz(primary_vertices->at(0).position());
        // std::cout << "jettk sumdz : " << jettk_sumdz << std::endl;
        // std::cout << "njettracks : " << n_jet_tracks << std::endl;
        presel_jet_avgdz.push_back(jettk_sumdz/n_jet_tracks);

      }

      else if (b_disc > jmt::BTagging::discriminator_min(jmt::BTagging::tight))
        presel_bjets.push_back(&jet);
    }

    *npreseljets = presel_jets.size();
    *npreselbjets = presel_bjets.size();
    // const bool pass_presel = presel_jets.size() >= njets && presel_bjets.size() >= nbjets;

    const bool pass_presel = presel_jets.size() >= njets && presel_bjets.size() >= nbjets && (presel_ele.size() + presel_mu.size()) >= nlep;

    if (pass_presel) {
 
      //here is randomly choosing a jet to move
      // for (int i : knuth_select(njets, presel_jets.size())) {
      //   selected_jets.push_back(presel_jets[i]);
      //   jets_used->push_back(*presel_jets[i]);
      // }

      for (int i : knuth_select(nbjets, presel_bjets.size())) {
        selected_jets.push_back(presel_bjets[i]);
        bjets_used->push_back(*presel_bjets[i]);
      }

      // //determine which lep collection to pull from : 
      // also have the lepton's dz on hand 
      double presel_lepdz = 0;
      if (presel_ele.size() == 0) { 
        // printf("presel muon (pt, eta, phi) : (%f, %f, %f)\n", presel_mu[0]->pt(), presel_mu[0]->eta(), presel_mu[0]->phi());

        selected_mu.push_back(presel_mu[0]);
        muons_used->push_back(*presel_mu[0]);
        presel_lepdz = presel_mu[0]->innerTrack()->dz(primary_vertices->at(0).position());
        // for (int i : knuth_select(nlep, presel_mu.size())) {
        //   selected_mu.push_back(presel_mu[i]);
        //   muons_used->push_back(*presel_mu[i]);
        // }      
      }
      else if (presel_mu.size() == 0) {
        // printf("presel electron (pt, eta, phi) : (%f, %f, %f)\n", presel_ele[0]->pt(), presel_ele[0]->eta(), presel_ele[0]->phi());

        selected_ele.push_back(presel_ele[0]);
        ele_used->push_back(*presel_ele[0]);
        presel_lepdz = presel_ele[0]->gsfTrack()->dz(primary_vertices->at(0).position());

        // for (int i : knuth_select(nlep, presel_ele.size())) {
        //   selected_ele.push_back(presel_ele[i]);
        //   ele_used->push_back(*presel_ele[i]);
        // }            
      }
      else {
        //there are both presel mu and ele -- choose the higher pT ? 
        if (presel_mu[0]->pt() > presel_ele[0]->pt()) {
          // printf("presel muon chosen over electron (pt, eta, phi) : (%f, %f, %f)\n", presel_mu[0]->pt(), presel_mu[0]->eta(), presel_mu[0]->phi());

          selected_mu.push_back(presel_mu[0]);
          muons_used->push_back(*presel_mu[0]);
          presel_lepdz = presel_mu[0]->innerTrack()->dz(primary_vertices->at(0).position());

          // for (int i : knuth_select(nlep, presel_mu.size())) {
          //   selected_mu.push_back(presel_mu[i]);
          //   muons_used->push_back(*presel_mu[i]);
          // }      
        }
        else if (presel_ele[0]->pt() > presel_mu[0]->pt()) {
          // printf("presel electron chosen over muon (pt, eta, phi) : (%f, %f, %f)\n", presel_ele[0]->pt(), presel_ele[0]->eta(), presel_ele[0]->phi());
          selected_ele.push_back(presel_ele[0]);
          ele_used->push_back(*presel_ele[0]);
          presel_lepdz = presel_ele[0]->gsfTrack()->dz(primary_vertices->at(0).position());

          // for (int i : knuth_select(nlep, presel_ele.size())) {
          //   selected_ele.push_back(presel_ele[i]);
          //   ele_used->push_back(*presel_ele[i]);
          // }           
        }
      }

      //instead of randomly choosing a jet from the presel_jets, chose the closest jet to the lepton in terms of dz. 
      jmt::MinValue m(9.0); //was 0.1
      // std::cout << "presel_lepdz : " << presel_lepdz << std::endl;
      for (size_t j = 0, jt = presel_jet_avgdz.size(); j < jt; ++j) {
        // std::cout << " presel jet avgdz : " << presel_jet_avgdz[j] << std::endl;
        // std::cout << "presel jet idx : " << j << "delta dz : " << fabs(presel_lepdz - presel_jet_avgdz[j]) << std::endl;
        m(j, fabs(presel_lepdz - presel_jet_avgdz[j]));
      }
      *jetlepdeltadz = m.v();

      //as long as the lepton and jet are decently close, select the jet to be moved;
      //otherwise, will not have any moved jet and things shouldn't break ... 
      // std::cout << "m.i(), m.v() " << m.i() << " " << m.v() << std::endl;
      if (m.i() != -1)  { 
        //here it's only choosing 1 jet so no need for loop 
        // for (int i : knuth_select(njets, presel_jets.size())) {
        selected_jets.push_back(presel_jets[m.i()]);
        jets_used->push_back(*presel_jets[m.i()]);
      }
      // }

      // Find the energy-weighted average direction of all the (b-)jets (+ leptons) to
      // be the flight axis.
      //the lepton(s) will then be moved to the (b-)jet 

      TVector3 flight_axis;
      for (const pat::Jet* jet : selected_jets)
        flight_axis += TVector3(jet->px(), jet->py(), jet->pz());

      for (const pat::Muon* mu : selected_mu)
        flight_axis += TVector3(mu->px(), mu->py(), mu->pz());
      for (const pat::Electron* ele : selected_ele)
        flight_axis += TVector3(ele->px(), ele->py(), ele->pz());

      flight_axis.SetMag(1.);
      flight_vect->at(0) = flight_axis.x();
      flight_vect->at(1) = flight_axis.y();
      flight_vect->at(2) = flight_axis.z();

      // Find the move vertex: pick a flight distance using Exp(dist|tau)
      // and a direction around the flight axis using
      // Gaus(theta|sig_theta) * Gaus(phi|sig_phi).

      const double dist = rexp.fire(tau);
      const double theta = rgau.fire(flight_axis.Theta(), sig_theta);
      const double phi   = rgau.fire(flight_axis.Phi(),   sig_phi);
      move.SetMagThetaPhi(dist, theta, phi);
      move_vertex->at(0) = primary_vertices->at(0).x() + move.x();
      move_vertex->at(1) = primary_vertices->at(0).y() + move.y();
      move_vertex->at(2) = primary_vertices->at(0).z() + move.z();
      // std::cout << "move vertex position : " << move_vertex->at(0) << ", " << move_vertex->at(1) << ", " << move_vertex->at(2) << std::endl;
    }
  
    // Copy all the input tracks, except for those corresponding to the
    // above jets and/or lep; for the latter, clone the tracks but move their
    // reference points to the move vertex.

    //leptons don't currently have trackrefgetter - so just following same procedure as LeptonVertexAssociator
    // have to find closest ctf track used to build the electron

    edm::Handle<reco::TrackCollection> tracks;
    event.getByToken(tracks_token, tracks);

    double sum_jettk_x = 0.0;
    double sum_jettk_y = 0.0;
    double sum_jettk_z = 0.0;
    size_t njettks = 0;
    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tk(tracks, i);
      bool to_move = false;
      for (const pat::Jet* jet : selected_jets){
        for (const reco::TrackRef& jet_tk : track_ref_getter.tracks(event, *jet))
          if (tk == jet_tk) {
            to_move = true;
            njettks += 1; //setup works only for 1 jet 
            goto done_check_to_move;
          }
      }
      done_check_to_move:

      if (to_move) {
        //move only quality tracks 
        const double pt = tk->pt();
        const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
        const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
        const auto trackLostInnerHits = tk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
        int min_r = 2000000000;
        for (int i = 1; i <= 4; ++i){
           if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
             min_r = i;
             break;
           }
        }
        if (!(pt > 1.0 && npxlayers >= 2 && nstlayers >= 6 && (min_r <= 1.0 || (min_r == 2.0 && trackLostInnerHits == 0) ))) continue;
       
        if (rint.fire(1,0.5) == 0 && halftoss==true) continue; //To toss out a track randomly

        reco::TrackBase::Point new_point(tk->vx() + move.x(),
                                         tk->vy() + move.y(),
                                         tk->vz() + move.z());

        sum_jettk_x += tk->vx() + move.x();
        sum_jettk_y += tk->vy() + move.y();
        sum_jettk_z += tk->vz() + move.z();

        move_jet_pos->at(0) = tk->vx() + move.x(); //make these vectors
        move_jet_pos->at(1) = tk->vy() + move.y(); // make these vectors 
        move_jet_pos->at(2) = tk->vz() + move.z(); //make these vectors

        // std::cout << "og point for jet track :  " <<  tk->vx() << ", " << tk->vy() << ", " << tk->vz() << std::endl;
        // std::cout << "new point for jet track :  " <<  new_point << std::endl;


        output_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
        reco::Track& new_tk = output_tracks->back();
        new_tk.setQualityMask(tk->qualityMask());
        new_tk.setNLoops(tk->nLoops());
        reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_tk.hitPattern());  *hp = tk->hitPattern(); // lmao
        moved_tracks->push_back(new_tk);
      }
      
      else
        output_tracks->push_back(*tk);

      output_tracks_map->insert(tk, reco::TrackRef(h_output_tracks, output_tracks->size() - 1));
    }
    // move_jet_pos->at(0) = sum_jettk_x/njettks;
    // move_jet_pos->at(1) = sum_jettk_y/njettks;
    // move_jet_pos->at(2) = sum_jettk_z/njettks;
    // std::cout << " --------------------------------------- " << std::endl;


    //put here moving leptons 
    //currently set up with separated track collections for ele and mu 

    if (use_separated_leptons) { 
      edm::Handle<reco::TrackCollection> muon_tracks;
      event.getByToken(muon_tracks_token, muon_tracks);
      for (size_t i = 0, im = muon_tracks->size(); i < im; ++i) { 
        reco::TrackRef tk(muon_tracks, i);
        // printf("comparing muon track (pt, eta, phi) : (%f, %f, %f)\n", tk->pt(), tk->eta(), tk->phi());

        bool mu_to_move = false;
        if (!tk.isNull()) {
          //wrong 
          // for (size_t imuon = 0; imuon < selected_mu.size(); ++imuon) {
            // const pat::Muon& muon = muons->at(imuon); 
          //
          for (const pat::Muon* muon : selected_mu){

            reco::TrackRef mtk = muon->innerTrack();
            if (!mtk.isNull()) {
              // printf("muon candidate selected (pt, eta, phi) : (%f, %f, %f)\n", mtk->pt(), mtk->eta(), mtk->phi());

              double dr = reco::deltaR(tk->eta(), tk->phi(), mtk->eta(), mtk->phi());
              // if (dr > 0.001) {
              //   std::cout << "questionable selected muon to move : " << mtk->pt() << " " << mtk->eta() << " " << mtk->phi() << std::endl;
              //   std::cout << "questionable mu tk to compare : " << tk->pt() << " " << tk->eta() << " " << tk->phi() << std::endl;
              // }
              if (dr < 0.001) {
                mu_to_move = true;
              }
            }
          }
        }
        
        if (mu_to_move) {
          // std::cout << " --------------------------------------- " << std::endl;

          // printf("the track has been matched to the muon and set to move! ... ");
          //move only quality tracks 
          const double pt = tk->pt();
          const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
          const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
          const auto trackLostInnerHits = tk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
          int min_r = 2000000000;
          for (int i = 1; i <= 4; ++i){
            if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
              min_r = i;
              break;
            }
          }
          if (!(pt >= 20.0 && npxlayers >= 2 && nstlayers >= 6 && (min_r <= 1.0 || (min_r == 2.0 && trackLostInnerHits == 0) ))) continue;

          if (rint.fire(1,0.5) == 0 && halftoss==true) continue; //To toss out a track randomly

          reco::TrackBase::Point new_point(tk->vx() + move.x(),
                                         tk->vy() + move.y(),
                                         tk->vz() + move.z());

          move_lep_pos->at(0) = tk->vx() + move.x();
          move_lep_pos->at(1) = tk->vy() + move.y();
          move_lep_pos->at(2) = tk->vz() + move.z();

          // reco::TrackBase::Point new_point(sum_jettk_x/njettks,
          //                                  sum_jettk_y/njettks,
          //                                  sum_jettk_z/njettks);

          // move_lep_pos->at(0) = sum_jettk_x/njettks;
          // move_lep_pos->at(1) = sum_jettk_y/njettks;
          // move_lep_pos->at(2) = sum_jettk_z/njettks;

          output_muon_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
          reco::Track& new_mutk = output_muon_tracks->back();
          new_mutk.setQualityMask(tk->qualityMask());
          new_mutk.setNLoops(tk->nLoops());
          reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_mutk.hitPattern());  *hp = tk->hitPattern(); // lmao
          moved_muon_tracks->push_back(new_mutk);
          // printf("muon track moved (pt, eta, phi) : (%f, %f, %f)\n", new_mutk.pt(), new_mutk.eta(), new_mutk.phi());
          // moved_tracks->push_back(new_mutk);

        }
        else
          output_muon_tracks->push_back(*tk);

        output_mutracks_map->insert(tk, reco::TrackRef(h_output_mutracks, output_muon_tracks->size() - 1));
      }

      edm::Handle<reco::TrackCollection> electron_tracks;
      event.getByToken(electron_tracks_token, electron_tracks);
      for (size_t i = 0, ie = electron_tracks->size(); i < ie; ++i) {

        reco::TrackRef tk(electron_tracks, i);
        // printf("comparing electron track (pt, eta, phi) : (%f, %f, %f)\n", tk->pt(), tk->eta(), tk->phi());

        bool ele_to_move = false;
        if (!tk.isNull()) {
          double mindR = 5.0;
          // wrong 
          // for (size_t iele = 0; iele < selected_ele.size(); ++iele) {
          //   const pat::Electron& electron = electrons->at(iele);
          // 
          for (const pat::Electron* electron : selected_ele){

            // reco::GsfTrackRef etk = electron.gsfTrack();
            reco::TrackRef ctf_etk = electron->closestCtfTrackRef();
            if (!ctf_etk.isNull()) { 
              // printf("electron candidate selected (pt, eta, phi) : (%f, %f, %f)\n", ctf_etk->pt(), ctf_etk->eta(), ctf_etk->phi());
              double dr = reco::deltaR(tk->eta(), tk->phi(), ctf_etk->eta(), ctf_etk->phi());
              // if (dr > 0.001) {
              //   std::cout << "questionable selected electron to move : " << ctf_etk->pt() << " " << ctf_etk->eta() << " " << ctf_etk->phi() << std::endl;
              //   std::cout << "questionable ele tk to compare : " << tk->pt() << " " << tk->eta() << " " << tk->phi() << std::endl;
              //   std::cout << dr << std::endl;
              // }
              // if (dr < 0.01 ) {
              //   ele_to_move = true;
              // }
              if (dr < mindR) mindR = dr;
            }
          }
          if (mindR < 0.01) ele_to_move = true;
        }
        // if (selected_ele.size() > 0 && !ele_to_move) std::cout << " did not find an electron track" << std::endl;
        if (ele_to_move) {
          // std::cout << " --------------------------------------- " << std::endl;
          // printf("the track has been matched to the electron and set to move! ... ");

          //move only quality tracks; these electrons need to have pt equal to or greater than 20 GeV (should already have this though?? idk)
          const double pt = tk->pt();
          const int npxlayers = tk->hitPattern().pixelLayersWithMeasurement();
          const int nstlayers = tk->hitPattern().stripLayersWithMeasurement();
          const auto trackLostInnerHits = tk->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
          int min_r = 2000000000;
          for (int i = 1; i <= 4; ++i){
            if (tk->hitPattern().hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel,i)) {
              min_r = i;
              break;
            }
          }
          if (!(pt >= 20.0 && npxlayers >= 2 && nstlayers >= 6 && (min_r <= 1.0 || (min_r == 2.0 && trackLostInnerHits == 0) ))) continue;
          if (rint.fire(1,0.5) == 0 && halftoss==true) continue; //To toss out a track randomly

          reco::TrackBase::Point new_point(tk->vx() + move.x(),
                                         tk->vy() + move.y(),
                                         tk->vz() + move.z());
          
          move_lep_pos->at(0) = tk->vx() + move.x();
          move_lep_pos->at(1) = tk->vy() + move.y();
          move_lep_pos->at(2) = tk->vz() + move.z();

          // reco::TrackBase::Point new_point(sum_jettk_x/njettks,
          //   sum_jettk_y/njettks,
          //   sum_jettk_z/njettks);

          // move_lep_pos->at(0) = sum_jettk_x/njettks;
          // move_lep_pos->at(1) = sum_jettk_y/njettks;
          // move_lep_pos->at(2) = sum_jettk_z/njettks;

          output_electron_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
          reco::Track& new_eletk = output_electron_tracks->back();
          new_eletk.setQualityMask(tk->qualityMask());
          new_eletk.setNLoops(tk->nLoops());
          reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_eletk.hitPattern());  *hp = tk->hitPattern(); // lmao
          moved_electron_tracks->push_back(new_eletk);
          // printf("electron track moved (pt, eta, phi) : (%f, %f, %f)\n", new_eletk.pt(), new_eletk.eta(), new_eletk.phi());
          // moved_tracks->push_back(new_eletk);

        }
        else
          output_electron_tracks->push_back(*tk);

        output_eletracks_map->insert(tk, reco::TrackRef(h_output_eletracks, output_electron_tracks->size() - 1));
      }
    }
    // std::cout << "done checking mu and ele tracks to move " << std::endl;
    // std::cout << "--------------------------------------- " << std::endl;

  }
  event.put(std::move(output_tracks));
  event.put(std::move(output_tracks_map));
  event.put(std::move(moved_tracks), "moved"); 
  //leptons 
  event.put(std::move(output_electron_tracks), "electrons");
  event.put(std::move(output_eletracks_map), "elemap");
  event.put(std::move(moved_electron_tracks), "movedele");
  event.put(std::move(output_muon_tracks), "muons");
  event.put(std::move(output_mutracks_map), "mumap");
  event.put(std::move(moved_muon_tracks), "movedmu");
  //
  event.put(std::move(npreseljets), "npreseljets");
  event.put(std::move(npreselbjets), "npreselbjets");
  event.put(std::move(npreselmu), "npreselmu");
  event.put(std::move(npreselele), "npreselele");
  event.put(std::move(jets_used), "jetsUsed");
  event.put(std::move(bjets_used), "bjetsUsed");
  event.put(std::move(muons_used), "muonsUsed");
  event.put(std::move(ele_used), "eleUsed");
  event.put(std::move(flight_vect), "flightAxis");
  event.put(std::move(move_vertex), "moveVertex");
  event.put(std::move(move_lep_pos), "moveLepPos");
  event.put(std::move(move_jet_pos), "moveJetPos");
  event.put(std::move(jetlepdeltadz), "jetlepdeltadz");

}

DEFINE_FWK_MODULE(MFVTrackMover);
