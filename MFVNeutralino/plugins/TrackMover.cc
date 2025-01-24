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
#include "RecoEgamma/EgammaTools/interface/EffectiveAreas.h"


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
  //
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

    // Pick the (b-)jets we'll use.
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
      if (b_disc < jmt::BTagging::discriminator_min(jmt::BTagging::loose))
        presel_jets.push_back(&jet);
      else if (b_disc > jmt::BTagging::discriminator_min(jmt::BTagging::tight))
        presel_bjets.push_back(&jet);
    }

    *npreseljets = presel_jets.size();
    *npreselbjets = presel_bjets.size();
    // const bool pass_presel = presel_jets.size() >= njets && presel_bjets.size() >= nbjets;

    // Pick the leptons we'll use. 
    for (const pat::Muon& muon : *muons) {
      bool isMedMuon = muon.passed(reco::Muon::CutBasedIdMedium);
      if (isMedMuon && muon.pt() > 5 && abs(muon.eta()) < 2.4) {
        const float iso = (muon.pfIsolationR04().sumChargedHadronPt + std::max(0., muon.pfIsolationR04().sumNeutralHadronEt + muon.pfIsolationR04().sumPhotonEt -0.5*muon.pfIsolationR04().sumPUPt))/muon.pt();
        if (iso < 0.1) {
          presel_mu.push_back(&muon);
        }
      }
    }
    for (const pat::Electron& electron : *electrons) {
      bool isTightEl = electron.electronID("cutBasedElectronID-Fall17-94X-V1-tight");
      const bool passveto = electron.passConversionVeto();
      
      if (isTightEl && passveto && electron.pt() > 5 && abs(electron.eta()) < 2.4) {
    
        // bool h_Escaled = electron.hadronicOverEm() < (electron.isEB() ? 0.05 + 1.12 + 0.0368 * *rho : 0.0414 + 0.5 + 0.201 * *rho) / electron.superCluster()->energy();
        // float ooEmooP = fabs(1.0/electron.ecalEnergy() - electron.eSuperClusterOverP()/electron.ecalEnergy() );
        // int expectedMissingInnerHits = electron.gsfTrack()->hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);

        const auto pfIso = electron.pfIsolationVariables();
        const float eA = electron_effective_areas.getEffectiveArea(fabs(electron.superCluster()->eta()));
        const float iso = (pfIso.sumChargedHadronPt + std::max(0., pfIso.sumNeutralHadronEt + pfIso.sumPhotonEt - *rho*eA)) / electron.pt();
        if (iso < 0.1)  {
          presel_ele.push_back(&electron);

        }
      }
    }

    *npreselele = presel_ele.size();
    *npreselmu = presel_mu.size();
    const bool pass_presel = presel_jets.size() >= njets && presel_bjets.size() >= nbjets && (presel_ele.size() + presel_mu.size()) >= nlep;


    if (pass_presel) {
      for (int i : knuth_select(njets, presel_jets.size())) {
        selected_jets.push_back(presel_jets[i]);
        jets_used->push_back(*presel_jets[i]);
      }

      for (int i : knuth_select(nbjets, presel_bjets.size())) {
        selected_jets.push_back(presel_bjets[i]);
        bjets_used->push_back(*presel_bjets[i]);
      }

      //determine which lep collection to pull from : 
      if (presel_ele.size() == 0) { 
        for (int i : knuth_select(nlep, presel_mu.size())) {
          selected_mu.push_back(presel_mu[i]);
          muons_used->push_back(*presel_mu[i]);
        }      
      }
      else if (presel_mu.size() == 0) {
        for (int i : knuth_select(nlep, presel_ele.size())) {
          selected_ele.push_back(presel_ele[i]);
          ele_used->push_back(*presel_ele[i]);

        }            
      }
      else {
        //there are both presel mu and ele -- choose the higher pT ? 
        if (presel_mu[0]->pt() > presel_ele[0]->pt()) {
          for (int i : knuth_select(nlep, presel_mu.size())) {
            selected_mu.push_back(presel_mu[i]);
            muons_used->push_back(*presel_mu[i]);

          }      
        }
        else if (presel_ele[0]->pt() > presel_mu[0]->pt()) {
          for (int i : knuth_select(nlep, presel_ele.size())) {
            selected_ele.push_back(presel_ele[i]);
            ele_used->push_back(*presel_ele[i]);

          }           
        }
      }

      // Find the energy-weighted average direction of all the (b-)jets to
      // be the flight axis.
      //the lepton(s) will be moved to the (b-)jet 

      TVector3 flight_axis;
      for (const pat::Jet* jet : selected_jets)
        flight_axis += TVector3(jet->px(), jet->py(), jet->pz());
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
    }
  
    // Copy all the input tracks, except for those corresponding to the
    // above jets and/or lep; for the latter, clone the tracks but move their
    // reference points to the move vertex.

      //leptons don't currently have trackrefgetter - so just following same procedure as LeptonVertexAssociator
      // have to find closest ctf track used to build the electron


    //currently set up with separated track collections for ele and mu 

    if (use_separated_leptons) { 
      edm::Handle<reco::TrackCollection> muon_tracks;
      event.getByToken(muon_tracks_token, muon_tracks);
      for (size_t i = 0, im = muon_tracks->size(); i < im; ++i) { 
        reco::TrackRef tk(muon_tracks, i);
        bool mu_to_move = false;
        if (!tk.isNull()) {
          for (size_t imuon = 0; imuon < selected_mu.size(); ++imuon) {
            const pat::Muon& muon = muons->at(imuon); 
            reco::TrackRef mtk = muon.innerTrack();
            if (!mtk.isNull()) {
              if (tk->pt() - mtk->pt() < 0.1) {
                mu_to_move = true;
              }
            }
          }
        }
      
        if (mu_to_move) {
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

          output_muon_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
          reco::Track& new_mutk = output_muon_tracks->back();
          new_mutk.setQualityMask(tk->qualityMask());
          new_mutk.setNLoops(tk->nLoops());
          reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_mutk.hitPattern());  *hp = tk->hitPattern(); // lmao
          moved_muon_tracks->push_back(new_mutk);
          // std::cout << "moving muon track" << std::endl;
        }
        else
          output_muon_tracks->push_back(*tk);

        output_mutracks_map->insert(tk, reco::TrackRef(h_output_mutracks, output_muon_tracks->size() - 1));
      }

      edm::Handle<reco::TrackCollection> electron_tracks;
      event.getByToken(electron_tracks_token, electron_tracks);
      for (size_t i = 0, ie = electron_tracks->size(); i < ie; ++i) {
        reco::TrackRef tk(electron_tracks, i);
        bool ele_to_move = false;
        if (!tk.isNull()) {
          for (size_t iele = 0; iele < selected_ele.size(); ++iele) {
            const pat::Electron& electron = electrons->at(iele);
            // reco::GsfTrackRef etk = electron.gsfTrack();
            reco::TrackRef ctf_etk = electron.closestCtfTrackRef();
            if (!ctf_etk.isNull()) { 
              if (tk->pt() - ctf_etk->pt() < 0.1) {
                ele_to_move = true;
              }
            }
          }
        }
        if (ele_to_move) {

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

          output_electron_tracks->push_back(reco::Track(tk->chi2(), tk->ndof(), new_point, tk->momentum(), tk->charge(), tk->covariance(), tk->algo()));
          reco::Track& new_eletk = output_electron_tracks->back();
          new_eletk.setQualityMask(tk->qualityMask());
          new_eletk.setNLoops(tk->nLoops());
          reco::HitPattern* hp = const_cast<reco::HitPattern*>(&new_eletk.hitPattern());  *hp = tk->hitPattern(); // lmao
          moved_electron_tracks->push_back(new_eletk);
        }
        else
          output_electron_tracks->push_back(*tk);

        output_eletracks_map->insert(tk, reco::TrackRef(h_output_eletracks, output_electron_tracks->size() - 1));
      }
    }


    edm::Handle<reco::TrackCollection> tracks;
    event.getByToken(tracks_token, tracks);

    for (size_t i = 0, ie = tracks->size(); i < ie; ++i) {
      reco::TrackRef tk(tracks, i);
      bool to_move = false;
      for (const pat::Jet* jet : selected_jets)
        for (const reco::TrackRef& jet_tk : track_ref_getter.tracks(event, *jet))
          if (tk == jet_tk) {
            to_move = true;
            goto done_check_to_move;
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
}

DEFINE_FWK_MODULE(MFVTrackMover);
