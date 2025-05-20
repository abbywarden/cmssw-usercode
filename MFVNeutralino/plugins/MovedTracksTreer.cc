#include "JMTucker/MFVNeutralino/interface/NtupleFiller.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Utilities.h"

class MFVMovedTracksTreer : public edm::EDAnalyzer {
public:
  explicit MFVMovedTracksTreer(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

private:
  mfv::MovedTracksNtuple nt;
  jmt::TrackingAndJetsNtupleFiller nt_filler;
  mfv::GenTruthSubNtupleFiller gentruth_filler;

  const edm::EDGetTokenT<MFVVertexAuxCollection> vertices_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> sel_tracks_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> sel_mutracks_token;
  const edm::EDGetTokenT<std::vector<reco::TrackRef>> sel_eletracks_token;
  const std::string mover_src;
  const edm::EDGetTokenT<reco::TrackCollection> all_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> moved_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> moved_electron_tracks_token;
  const edm::EDGetTokenT<reco::TrackCollection> moved_muon_tracks_token;
  const edm::EDGetTokenT<int> npreseljets_token;
  const edm::EDGetTokenT<int> npreselbjets_token;
  const edm::EDGetTokenT<int> npreselmu_token;
  const edm::EDGetTokenT<int> npreselele_token;
  const edm::EDGetTokenT<pat::JetCollection> jets_used_token;
  const edm::EDGetTokenT<pat::JetCollection> bjets_used_token;
  const edm::EDGetTokenT<pat::MuonCollection> muons_used_token;
  const edm::EDGetTokenT<pat::ElectronCollection> ele_used_token;
  const edm::EDGetTokenT<std::vector<double> > move_vertex_token;
  const edm::EDGetTokenT<std::vector<double> > move_lep_pos_token;
  const edm::EDGetTokenT<std::vector<double> > move_jet_pos_token;
  const edm::EDGetTokenT<double> jet_lep_deltadz_token;

  const double max_dist2move;
  const bool apply_presel;
  const unsigned njets_req;
  const unsigned nbjets_req;
  const unsigned nlep_req;
  const bool for_mctruth;
};

MFVMovedTracksTreer::MFVMovedTracksTreer(const edm::ParameterSet& cfg)
  : nt_filler(nt, cfg, NF_CC_TrackingAndJets_v,
              jmt::TrackingAndJetsNtupleFillerParams()
                .pvs_subtract_bs(true) // JMTBAD get rid of beamspot subtraction everywhere
                .fill_tracks(false)),
    gentruth_filler(nt.gentruth(), cfg, consumesCollector()),
    vertices_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertices_src"))),
    sel_tracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("sel_tracks_src"))),
    sel_mutracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("sel_mutracks_src"))),
    sel_eletracks_token(consumes<std::vector<reco::TrackRef>>(cfg.getParameter<edm::InputTag>("sel_eletracks_src"))),
    mover_src(cfg.getParameter<std::string>("mover_src")),
    all_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src))),
    moved_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src, "moved"))),
    moved_electron_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src, "movedele"))),
    moved_muon_tracks_token(consumes<reco::TrackCollection>(edm::InputTag(mover_src, "movedmu"))),    
    npreseljets_token(consumes<int>(edm::InputTag(mover_src, "npreseljets"))),
    npreselbjets_token(consumes<int>(edm::InputTag(mover_src, "npreselbjets"))),
    npreselmu_token(consumes<int>(edm::InputTag(mover_src, "npreselmu"))),
    npreselele_token(consumes<int>(edm::InputTag(mover_src, "npreselele"))),
    jets_used_token(consumes<pat::JetCollection>(edm::InputTag(mover_src, "jetsUsed"))),
    bjets_used_token(consumes<pat::JetCollection>(edm::InputTag(mover_src, "bjetsUsed"))),
    muons_used_token(consumes<pat::MuonCollection>(edm::InputTag(mover_src, "muonsUsed"))),
    ele_used_token(consumes<pat::ElectronCollection>(edm::InputTag(mover_src, "eleUsed"))),

    move_vertex_token(consumes<std::vector<double> >(edm::InputTag(mover_src, "moveVertex"))),
    move_lep_pos_token(consumes<std::vector<double> >(edm::InputTag(mover_src, "moveLepPos"))),
    move_jet_pos_token(consumes<std::vector<double> >(edm::InputTag(mover_src, "moveJetPos"))),
    jet_lep_deltadz_token(consumes<double>(edm::InputTag(mover_src, "jetlepdeltadz"))),

    max_dist2move(cfg.getParameter<double>("max_dist2move")),
    apply_presel(cfg.getParameter<bool>("apply_presel")),
    njets_req(cfg.getParameter<unsigned>("njets_req")),
    nbjets_req(cfg.getParameter<unsigned>("nbjets_req")),
    nlep_req(cfg.getParameter<unsigned>("nlep_req")),
    for_mctruth(cfg.getParameter<bool>("for_mctruth"))
{}

namespace {
  double mag2(double x, double y, double z)           { return x*x + y*y + z*z; }
  double mag2(double x, double y, double z, double w) { return x*x + y*y + z*z + w*w; }
}

void MFVMovedTracksTreer::analyze(const edm::Event& event, const edm::EventSetup&) {
  nt_filler.fill(event);
  gentruth_filler(event);
  auto tks_push_back = [&](const reco::Track& tk) { NtupleAdd(nt.tracks(), tk); };

  if (for_mctruth) {
    edm::Handle<std::vector<reco::TrackRef>> sel_tracks;
    event.getByToken(sel_tracks_token, sel_tracks);

    edm::Handle<std::vector<reco::TrackRef>> sel_mutracks;
    event.getByToken(sel_mutracks_token, sel_mutracks);

    edm::Handle<std::vector<reco::TrackRef>> sel_eletracks;
    event.getByToken(sel_eletracks_token, sel_eletracks);

    for (reco::TrackRef tk : *sel_tracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*tk);
      nt.set_tk_moved(whichtk); // not really "moved" but this is to distinguish sel tracks from tracks coming in from jets below

      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, tk);
      nt.tracks().set_which_pv(whichtk, whichpv);
    }

    //same as above but for muons, electrons ... 
    for (reco::TrackRef mutk : *sel_mutracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*mutk);
      nt.set_mtk_moved(whichtk); // not really "moved" but this is to distinguish sel tracks from tracks coming in from jets below

      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, mutk);
      nt.tracks().set_which_pv(whichtk, whichpv);
      // std::cout << "muon track point : " << mutk->vx() << " " << mutk->vy() << " " << mutk->vz() << std::endl;
    }

    for (reco::TrackRef eletk : *sel_eletracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*eletk);
      nt.set_etk_moved(whichtk); // not really "moved" but this is to distinguish sel tracks from tracks coming in from jets below

      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, eletk);
      nt.tracks().set_which_pv(whichtk, whichpv);
      // std::cout << "electron track point : " << eletk->vx() << " " << eletk->vy() << " " << eletk->vz() << std::endl;

    }

    // JMTBAD use TracksSubNtupleFiller::which_jet?
    for (const pat::Jet& jet : nt_filler.jets_filler().jets(event)) {
      double dist2min = 0.1;
      int whichjet = -1;

      for (int j = 0, je = nt.jets().n(); j < je; ++j) {
        const double dist2 = mag2(jet.pt()     - nt.jets().pt(j),
                                  jet.eta()    - nt.jets().eta(j),
                                  jet.phi()    - nt.jets().phi(j),
                                  jet.energy() - nt.jets().energy(j));
        if (dist2 < dist2min) {
          dist2min = dist2;
          whichjet = j;
        }
      }

      assert(whichjet != -1);

      for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
        const reco::Track* tk = jetDaughterTrack(jet, idau);
        if (tk) {
          double dist2min = 0.1;
          int whichtk = -1;
          for (size_t i = 0, ie = nt.tracks().n(); i < ie; ++i) {
            const double dist2 = mag2(tk->charge() * tk->pt() - nt.tracks().qpt(i),
                                      tk->eta()               - nt.tracks().eta(i),
                                      tk->phi()               - nt.tracks().phi(i));
            if (dist2 < dist2min) {
              dist2min = dist2;
              whichtk = i;
            }
          }

          if (whichtk == -1) {
            whichtk = nt.tracks().n();
            tks_push_back(*tk);
          }
          else { 
            nt.set_jet_moved(whichjet);
            // std::cout << "jet track 'moved' : " << tk->vx() << " " << tk->vy() << " " << tk->vz() << std::endl;
          }
          nt.tracks().set_which_jet(whichtk, whichjet);
        }
      }
    }
  }
  else {
    // edm::Handle<reco::TrackCollection> all_tracks, moved_tracks;
    edm::Handle<reco::TrackCollection> all_tracks, moved_tracks, moved_electron_tracks, moved_muon_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_mutracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_eletracks;
    edm::Handle<int> npreseljets, npreselbjets, npreselmu, npreselele;
    edm::Handle<pat::JetCollection> jets_used, bjets_used;
    edm::Handle<pat::ElectronCollection> ele_used;
    edm::Handle<pat::MuonCollection> muons_used;
    edm::Handle<std::vector<double> > move_vertex;
    edm::Handle<std::vector<double> > move_lep_pos;
    edm::Handle<std::vector<double> > move_jet_pos;
    edm::Handle<double> jetlepdeltadz;
    event.getByToken(all_tracks_token,   all_tracks);
    event.getByToken(sel_tracks_token,   sel_tracks);
    event.getByToken(sel_mutracks_token,   sel_mutracks);
    event.getByToken(sel_eletracks_token,   sel_eletracks);
    event.getByToken(moved_tracks_token, moved_tracks);
    event.getByToken(moved_electron_tracks_token, moved_electron_tracks);
    event.getByToken(moved_muon_tracks_token, moved_muon_tracks);
    event.getByToken(npreseljets_token,  npreseljets);
    event.getByToken(npreselbjets_token, npreselbjets);
    event.getByToken(npreselele_token, npreselele);
    event.getByToken(npreselmu_token, npreselmu);
    event.getByToken(jets_used_token,    jets_used);
    event.getByToken(bjets_used_token,   bjets_used);
    event.getByToken(muons_used_token,   muons_used);
    event.getByToken(ele_used_token,     ele_used);
    event.getByToken(move_vertex_token,  move_vertex);
    event.getByToken(move_lep_pos_token, move_lep_pos);
    event.getByToken(move_jet_pos_token, move_jet_pos);
    event.getByToken(jet_lep_deltadz_token, jetlepdeltadz);

    nt.tm().set(all_tracks->size(), moved_tracks->size(), moved_electron_tracks->size(), moved_muon_tracks->size(), *npreseljets, *npreselbjets, *npreselmu, *npreselele,
                (*move_vertex)[0] - nt_filler.bs().x((*move_vertex)[2]), // JMTBAD get rid of beamspot subtraction everywhere
                (*move_vertex)[1] - nt_filler.bs().y((*move_vertex)[2]),
                (*move_vertex)[2],
                (*move_lep_pos)[0], (*move_lep_pos)[1], (*move_lep_pos)[2], 
                (*move_jet_pos)[0], (*move_jet_pos)[1], (*move_jet_pos)[2], *jetlepdeltadz
              );
    // nt.tm().set(all_tracks->size(), moved_tracks->size(), *npreseljets, *npreselbjets, *npreselmu, *npreselele,
    //             (*move_vertex)[0] - nt_filler.bs().x((*move_vertex)[2]), // JMTBAD get rid of beamspot subtraction everywhere
    //             (*move_vertex)[1] - nt_filler.bs().y((*move_vertex)[2]),
    //             (*move_vertex)[2]);


    for (reco::TrackRef tk : *sel_tracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*tk);
      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, tk);
      nt.tracks().set_which_pv(whichtk, whichpv);
    }
    for (reco::TrackRef mtk : *sel_mutracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*mtk);
      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, mtk);
      nt.tracks().set_which_pv(whichtk, whichpv);

    }
    for (reco::TrackRef etk : *sel_eletracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*etk);
      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, etk);
      nt.tracks().set_which_pv(whichtk, whichpv);

    }

    // std::cout << "checking moved tracks " << std::endl;
    for (const reco::Track& tk : *moved_tracks) {
      double dist2min = 0.1;
      int which = -1;
      for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
        // std::cout << "(from tks_filler) track  pt, eta, phi : " << tk.pt() << " " << tk.eta() << " " << tk.phi() << " "  << std::endl;
        // std::cout << "(from nt.tracks()) track pt, eta, phi : " << nt.tracks().qpt(i) << " " << nt.tracks().eta(i) << " " << nt.tracks().phi(i) << " " << std::endl;
        const double dist2 = mag2(tk.charge() * tk.pt() - nt.tracks().qpt(i),
                                  tk.eta()              - nt.tracks().eta(i),
                                  tk.phi()              - nt.tracks().phi(i));
        if (dist2 < dist2min) {
          dist2min = dist2;
          which = i;
        }
      }

      // if (which != -1) {
      //   nt.set_tk_moved(which);
      //   // std::cout << "found moved track idx : " << which << std::endl;  
      // }
      // else if (which == -1) {
      //   which = nt.tracks().n();
      //   tks_push_back(tk);
      // }

      //original (is this wrong??) 
      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(tk);
      }
      nt.set_tk_moved(which);
      // std::cout << "found moved track idx : " << which << std::endl;

    }

    //electrons 
    // double moved_eletk_pt = 0.0;
    // double moved_eletk_phi = -1.0;
    // double moved_eletk_eta = -1.0;
    for (const reco::Track& etk : *moved_electron_tracks) {
      double dist2min = 0.1;
      int which = -1;
      //only do the matching for moved electron tracks of pT >=  20 
      if (etk.pt() >= 20) { 
        // std::cout << "(from etks_filler) track  pt, eta, phi : " << etk.pt() << " " << etk.eta() << " " << etk.phi() << " "  << std::endl;
        for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
          // std::cout << "(from nt.tracks()) track pt, eta, phi : " << nt.tracks().qpt(i) << " " << nt.tracks().eta(i) << " " << nt.tracks().phi(i) << " " << std::endl;
          const double dist2 = mag2(etk.charge() * etk.pt() - nt.tracks().qpt(i),
                                    etk.eta()              - nt.tracks().eta(i),
                                    etk.phi()              - nt.tracks().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
            // moved_eletk_pt = etk.pt();
            // moved_eletk_phi = etk.phi();
            // moved_eletk_eta = etk.eta();
          }
        }
      }
      // // std::cout << " checking moved electron tracks : (which track matched?) " << which << " and dist2min was : " << dist2min << std::endl;
      // if (which != -1) {
      //   nt.set_etk_moved(which); 
      //   // std::cout << "found moved electron track idx : " << which << std::endl;  
      // }

      // else if (which == -1) {
      //   which = nt.tracks().n();
      //   tks_push_back(etk);
      // }

      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(etk);
      }
      nt.set_etk_moved(which);
      // std::cout << "found moved ele track idx : " << which << std::endl;


    }

    //muons 
    // double moved_mutk_pt = 0.0;
    // double moved_mutk_phi = -1.0;
    // double moved_mutk_eta = -1.0;
    // std::cout << "checking moved muon tracks" << std::endl;
    // only do the matching for moved muon tracks of pT >= 20
    for (const reco::Track& mtk : *moved_muon_tracks) {
      double dist2min = 0.1;
      int which = -1;
      if (mtk.pt() >= 20) { 
        // std::cout << "(from moved muon tracks) track  pt, eta, phi : " << mtk.pt() << " " << mtk.eta() << " " << mtk.phi() << " "  << std::endl;
        for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
          // std::cout << "(from nt.tracks()) track pt, eta, phi : " << nt.tracks().qpt(i) << " " << nt.tracks().eta(i) << " " << nt.tracks().phi(i) << " " << std::endl;
          const double dist2 = mag2(mtk.charge() * mtk.pt() - nt.tracks().qpt(i),
                                    mtk.eta()              - nt.tracks().eta(i),
                                    mtk.phi()              - nt.tracks().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
            // moved_mutk_pt = mtk.pt();
            // moved_mutk_phi = mtk.phi();
            // moved_mutk_eta = mtk.eta();
          }
        }
      }
      // std::cout << " checking moved muon tracks : (which track matched?) " << which << " and dist2min was : " << dist2min << std::endl;
      
      // if (which != -1) {
      //   nt.set_mtk_moved(which);
      //   // std::cout << "found moved muon track idx : " << which << std::endl;  
      // }
      // else if (which == -1) {
      //   which = nt.tracks().n();
      //   tks_push_back(mtk);
      // }
      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(mtk);
      }
      nt.set_mtk_moved(which);
      // std::cout << "found moved ele track idx : " << which << std::endl;


    }

    //now flagging the muon objects that are moved 
    // std::cout << "moving to checking which muon candidates were moved .. " << std::endl;
    const size_t nmovedmu = muons_used->size();
    // double moved_muon_pt = 0.0;
    // double moved_muon_eta = -1.0;
    // double moved_muon_phi = -1.0;

    std::vector<int> whichs_mu(nmovedmu, -1);
    int m = -1;
    for (const pat::MuonCollection* muons : {&*muons_used}) {
      for (const pat::Muon& mu : *muons) {
        ++m;
        double dist2min = 0.1;
        int which = -1;

        for (int i = 0, im = nt.muons().n(); i < im; ++i) { 
          // std::cout << "(from muons_filler) muon  pt, eta, phi : " << mu.pt() << " " << mu.eta() << " " << mu.phi() << " "  << std::endl;
          // std::cout << "(from nt.muons()) muon pt, eta, phi : " << nt.muons().pt(i) << " " << nt.muons().eta(i) << " " << nt.muons().phi(i) << " " << std::endl;
          const double dist2 = mag2(mu.pt()     - nt.muons().pt(i),
                                    mu.eta()    - nt.muons().eta(i),
                                    mu.phi()    - nt.muons().phi(i));
          // std::cout << "dist2 : " << dist2 << std::endl;
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
            // moved_muon_pt = mu.pt();
            // moved_muon_eta = mu.eta();
            // moved_muon_phi = mu.phi();
          }
        }
        // std::cout << "which mu ? " << which << std::endl;
        assert(which != -1);
        whichs_mu[m] = which;
        nt.set_muon_moved(which);
      }
    }


    // now flagging the electron objects that are moved 
    // std::cout << "moving to checking which electron candidates were moved .. " << std::endl;
    const size_t nmovedele = ele_used->size();
    // double moved_electron_pt = 0.0;
    // double moved_electron_eta = -1.0;
    // double moved_electron_phi = -1.0;
    std::vector<int> whichs_ele(nmovedele, -1);

    int e = -1;
    for (const pat::ElectronCollection* electrons : { &*ele_used }) {
      for (const pat::Electron& ele : *electrons) {
        ++e;
        double dist2min = 0.1;
        int which = -1;

        for (int i = 0, ie = nt.electrons().n(); i < ie; ++i) { 
          // std::cout << "(from electrons_filler) ele  pt, eta, phi : " << ele.pt() << " " << ele.eta() << " " << ele.phi() << " "  << std::endl;
          // std::cout << "(from nt.electrons()) ele pt, eta, phi : " << nt.electrons().pt(i) << " " << nt.electrons().eta(i) << " " << nt.electrons().phi(i) << " " << std::endl;
          const double dist2 = mag2(ele.pt()     - nt.electrons().pt(i),
                                    ele.eta()    - nt.electrons().eta(i),
                                    ele.phi()    - nt.electrons().phi(i));

          // std::cout << "dist2 : " << dist2 << std::endl;
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
            // moved_electron_pt = ele.pt();
            // moved_electron_eta = ele.eta();
            // moved_electron_phi = ele.phi();
          }
        }
        // std::cout << "which ele ? " << which << std::endl;
        assert(which != -1);
        whichs_ele[e] = which;
        nt.set_electron_moved(which);
      }
    }

    // double moved_lepdR = 5.0;
    // if (moved_mutk_pt || moved_muon_pt > 0) {
    //   moved_lepdR = reco::deltaR(moved_mutk_eta, moved_mutk_phi, moved_muon_eta, moved_muon_phi);
    // }
    // if (moved_eletk_pt || moved_electron_pt > 0) {
    //   moved_lepdR = reco::deltaR(moved_eletk_eta, moved_eletk_phi, moved_electron_eta, moved_electron_phi);
    // }
    // if (moved_lepdR > 0.1) { 
    //   std::cout << " finished setting moved leptons and their tracks ... but they don't match ??: " << std::endl;
    //   printf("muon track (pt, eta, phi) : (%f, %f, %f), and the muon candidate (pt, eta, phi) : (%f, %f, %f)\n", moved_mutk_pt, moved_mutk_eta, moved_mutk_phi, moved_muon_pt, moved_muon_eta, moved_muon_phi);
    //   printf("electron track (pt, eta, phi) : (%f, %f, %f), and the electron candidate (pt, eta, phi) : (%f, %f, %f)\n", moved_eletk_pt, moved_eletk_eta, moved_eletk_phi, moved_electron_pt, moved_electron_eta, moved_electron_phi);
    //   std::cout << " --------------------------------------------------------------------------" << std::endl;
    // }

    // std::cout << "setting which tracks belong to which jet " << std::endl;
    for (const pat::Jet& jet : nt_filler.jets_filler().jets(event)) {
      double dist2min = 0.1;
      int whichjet = -1;
      
      for (int j = 0, je = nt.jets().n(); j < je; ++j) {
        // std::cout << "(from jets_filler) jet idx, pt, eta, phi, energy : " << j << " " << jet.pt() << " " << jet.eta() << " " << jet.phi() << " " << jet.energy() << std::endl;
        // std::cout << "(from nt.jets()) jet idx, pt, eta, phi, energy : " << j << " " << nt.jets().pt(j) << " " << nt.jets().eta(j) << " " << nt.jets().phi(j) << " " << nt.jets().energy(j) << std::endl;
        const double dist2 = mag2(jet.pt()     - nt.jets().pt(j),
                                  jet.eta()    - nt.jets().eta(j),
                                  jet.phi()    - nt.jets().phi(j),
                                  jet.energy() - nt.jets().energy(j));
        if (dist2 < dist2min) {
          dist2min = dist2;
          whichjet = j;
        }
      }

      assert(whichjet != -1);

      for (size_t idau = 0, idaue = jet.numberOfDaughters(); idau < idaue; ++idau) {
        const reco::Track* tk = jetDaughterTrack(jet, idau);
        if (tk) {
          double dist2min = 0.1;
          int whichtk = -1;
          for (size_t i = 0, ie = nt.tracks().n(); i < ie; ++i) {
            const double dist2 = mag2(tk->charge() * tk->pt() - nt.tracks().qpt(i),
                                      tk->eta()               - nt.tracks().eta(i),
                                      tk->phi()               - nt.tracks().phi(i));
            if (dist2 < dist2min) {
              dist2min = dist2;
              whichtk = i;
            }
          }
          if (whichtk != -1) {
            nt.tracks().set_which_jet(whichtk, whichjet);
          }
        }
      }
    }

    const size_t nmovedjets = jets_used->size() + bjets_used->size();
    std::vector<int> whichs(nmovedjets, -1);

    int i = -1;
    for (const pat::JetCollection* jets : { &*jets_used, &*bjets_used }) {
      for (const pat::Jet& jet : *jets) {
        ++i;
        double dist2min = 0.1;
        int which = -1;

        for (size_t j = 0, je = nt.jets().n(); j < je; ++j) {
          const double dist2 = mag2(jet.pt()     - nt.jets().pt(j),
                                    jet.eta()    - nt.jets().eta(j),
                                    jet.phi()    - nt.jets().phi(j),
                                    jet.energy() - nt.jets().energy(j));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = j;
          }
        }

        assert(which != -1);
        whichs[i] = which;
        nt.set_jet_moved(which);
      }
    }

    for (size_t i = 0; i < nmovedjets; ++i)
      for (size_t j = i+1; j < nmovedjets; ++j)
        assert(whichs[i] != whichs[j]);
  }

  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);
  // std::cout << "going to vertices .. " << std::endl;
  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - nt_filler.bs().x(v.z); // JMTBAD get rid of beamspot subtraction everywhere
    const double vy = v.y - nt_filler.bs().y(v.z);
    const double vz = v.z;

    if (!for_mctruth) {
      const double dist2move = sqrt(mag2(vx - nt.tm().move_x(),
                                         vy - nt.tm().move_y(),
                                         vz - nt.tm().move_z()));
      if (dist2move > max_dist2move)
        continue;
    }

    nt.vertices().add(v.chi2, vx, vy, vz, v.cxx, v.cxy, v.cxz, v.cyy, v.cyz, v.czz,
                      v.rescale_chi2, v.rescale_x - nt_filler.bs().x(v.rescale_z), v.rescale_y - nt_filler.bs().y(v.rescale_z), v.rescale_z, v.rescale_cxx, v.rescale_cxy, v.rescale_cxz, v.rescale_cyy, v.rescale_cyz, v.rescale_czz, // JMTBAD get rid of beamspot subtraction everywhere (then just use NtupleAdd here)
                      v.ntracks(), v.njets[0], v.bs2derr, v.rescale_bs2derr, false,
                      v.pt[mfv::PTracksPlusJetsByNtracks], v.eta[mfv::PTracksPlusJetsByNtracks], v.phi[mfv::PTracksPlusJetsByNtracks], v.mass[mfv::PTracksPlusJetsByNtracks]);
     
    for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
      /*
      jmt::MinValue m(0.1);
      for (size_t j = 0, je = nt.tracks().n(); j < je; ++j){
        m(j, mag2(v.track_qpt(i) - nt.tracks().qpt(j),
                  v.track_eta[i] - nt.tracks().eta(j),
                  v.track_phi[i] - nt.tracks().phi(j)));
        }

      assert(m.i() != -1);
      std::cout << " m.i() " << m.i() << std::endl;
      if (nt.tracks().which_sv(m.i()) != 255) {
        const int w = nt.tracks().which_sv(m.i());
        cms::Exception ce("BadAssumption");
        ce << "vertex w " << v.ntracks() << " tracks @ <" << v.x << ", " << v.y << ", " << v.z
           << ">: track <" << v.track_qpt(i) << ", " << v.track_eta[i] << ", " << v.track_phi[i] << "> with mindist " << m.v()
           << " to general track " << m.i() << "/" << nt.tracks().n() << ": <" << nt.tracks().qpt(m.i()) << ", " << nt.tracks().eta(m.i()) << ", " << nt.tracks().phi(m.i())
           << "> but already found in other vertex #" << w;
        if (nt.tracks().which_sv(m.i()) < nt.vertices().n())
          ce << " with " << nt.vertices().ntracks(w) << " tracks @ <" << nt.vertices().x(w) << ", " << nt.vertices().y(w) << ", " << nt.vertices().z(w) << ">\n";
        else
          ce << "--this isn't a valid vertex number (max " << nt.vertices().n() << ")\n";
        throw ce;
      }
      */
      const size_t iv = nt.vertices().n() - 1;
      // std::cout << "vertex number (?) " << iv << std::endl;
      assert(iv < 255);
      nt.tracks().set_which_sv(99, iv); //FIXME
    }
  }

  if (apply_presel) {
    if ((!for_mctruth && (nt.tm().npreseljets() < njets_req || nt.tm().npreselbjets() < nbjets_req || (nt.tm().npreselele() + nt.tm().npreselmu()) < nlep_req))) // || nt.jets().ht() < 1000)
    // if ((!for_mctruth && (nt.tm().npreseljets() < njets_req || nt.tm().npreselbjets() < nbjets_req))) // || nt.jets().ht() < 1000)
      return;
  }
  nt_filler.finalize();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
