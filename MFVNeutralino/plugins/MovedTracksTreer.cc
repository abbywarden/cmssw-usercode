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
  const edm::EDGetTokenT<double> move_lep_dxypv_token;
  const edm::EDGetTokenT<double> move_jet_dxypv_token; //currently the average dxy over all jet tracks 
  const edm::EDGetTokenT<double> jet_lep_deltadz_token; //using the jet's average dz over all jet tracks 

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
    move_lep_dxypv_token(consumes<double>(edm::InputTag(mover_src, "movelepdxypv"))),
    move_jet_dxypv_token(consumes<double>(edm::InputTag(mover_src, "movejetdxypv"))),
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

  //declaring here so can use it later 
  std::vector<int> whichs_mu;
  std::vector<int> whichs_ele;

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
    }

    for (reco::TrackRef eletk : *sel_eletracks) {
      const int whichtk = nt.tracks().n();
      tks_push_back(*eletk);
      nt.set_etk_moved(whichtk); // not really "moved" but this is to distinguish sel tracks from tracks coming in from jets below

      auto vf = nt_filler.pvs_filler();
      const int whichpv = nt_filler.tracks_filler().which_pv(event, &vf, eletk);
      nt.tracks().set_which_pv(whichtk, whichpv);
    }

    // JMTBAD use TracksSubNtupleFiller::which_jet?

    //FIXME? (time)
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
          }
          nt.tracks().set_which_jet(whichtk, whichjet);
        }
      }
    }
  }
  else {
    edm::Handle<reco::TrackCollection> all_tracks, moved_tracks, moved_electron_tracks, moved_muon_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_tracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_mutracks;
    edm::Handle<std::vector<reco::TrackRef>> sel_eletracks;
    edm::Handle<int> npreseljets, npreselbjets, npreselmu, npreselele;
    edm::Handle<pat::JetCollection> jets_used, bjets_used;
    edm::Handle<pat::ElectronCollection> ele_used;
    edm::Handle<pat::MuonCollection> muons_used;
    edm::Handle<std::vector<double> > move_vertex;
    edm::Handle<double> movelepdxypv;
    edm::Handle<double> movejetdxypv;
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
    event.getByToken(move_lep_dxypv_token, movelepdxypv);
    event.getByToken(move_jet_dxypv_token, movejetdxypv);
    event.getByToken(jet_lep_deltadz_token, jetlepdeltadz);

    nt.tm().set(all_tracks->size(), moved_tracks->size(), moved_electron_tracks->size(), moved_muon_tracks->size(), *npreseljets, *npreselbjets, *npreselmu, *npreselele,
                (*move_vertex)[0] - nt_filler.bs().x((*move_vertex)[2]), // JMTBAD get rid of beamspot subtraction everywhere
                (*move_vertex)[1] - nt_filler.bs().y((*move_vertex)[2]),
                (*move_vertex)[2], *movelepdxypv, *movejetdxypv, *jetlepdeltadz
              );

    //try and speed things up ... 
    if (apply_presel) {
      if (((nt.tm().npreseljets() < njets_req || nt.tm().npreselbjets() < nbjets_req || (nt.tm().npreselele() + nt.tm().npreselmu()) < nlep_req))) // || nt.jets().ht() < 1000)
        return;
    }

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

    //FIXME? (time) 
    for (const reco::Track& tk : *moved_tracks) {
      double dist2min = 0.1;
      int which = -1;
      for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
        const double dist2 = mag2(tk.charge() * tk.pt() - nt.tracks().qpt(i),
                                  tk.eta()              - nt.tracks().eta(i),
                                  tk.phi()              - nt.tracks().phi(i));
        if (dist2 < dist2min) {
          dist2min = dist2;
          which = i;
        }
      }
      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(tk);
      }
      nt.set_tk_moved(which);
    }

    //electrons 
    for (const reco::Track& etk : *moved_electron_tracks) {
      double dist2min = 0.1;
      int which = -1;
      //only do the matching for moved electron tracks of pT >=  20 
      if (etk.pt() >= 20) { 
        for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
          const double dist2 = mag2(etk.charge() * etk.pt() - nt.tracks().qpt(i),
                                    etk.eta()              - nt.tracks().eta(i),
                                    etk.phi()              - nt.tracks().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
      }

      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(etk);
      }
      nt.set_etk_moved(which);


    }

    //muons 
    // only do the matching for moved muon tracks of pT >= 20
    for (const reco::Track& mtk : *moved_muon_tracks) {
      double dist2min = 0.1;
      int which = -1;
      if (mtk.pt() >= 20) { 
        for (int i = 0, ie = nt.tracks().n(); i < ie; ++i) {
          const double dist2 = mag2(mtk.charge() * mtk.pt() - nt.tracks().qpt(i),
                                    mtk.eta()              - nt.tracks().eta(i),
                                    mtk.phi()              - nt.tracks().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
      }
      if (which == -1) {
        which = nt.tracks().n();
        tks_push_back(mtk);
      }
      nt.set_mtk_moved(which);


    }

    //now flagging the muon objects that are moved 
    const size_t nmovedmu = muons_used->size();
    whichs_mu.resize(nmovedmu, -1);
    int m = -1;
    for (const pat::MuonCollection* muons : {&*muons_used}) {
      for (const pat::Muon& mu : *muons) {
        ++m;
        double dist2min = 0.1;
        int which = -1;

        for (int i = 0, im = nt.muons().n(); i < im; ++i) { 
          const double dist2 = mag2(mu.pt()     - nt.muons().pt(i),
                                    mu.eta()    - nt.muons().eta(i),
                                    mu.phi()    - nt.muons().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
        assert(which != -1);
        whichs_mu[m] = which;
        nt.set_muon_moved(which);
      }
    }


    // now flagging the electron objects that are moved 
    const size_t nmovedele = ele_used->size();
    whichs_ele.resize(nmovedele, -1);

    int e = -1;
    for (const pat::ElectronCollection* electrons : { &*ele_used }) {
      for (const pat::Electron& ele : *electrons) {
        ++e;
        double dist2min = 0.1;
        int which = -1;

        for (int i = 0, ie = nt.electrons().n(); i < ie; ++i) { 
          const double dist2 = mag2(ele.pt()     - nt.electrons().pt(i),
                                    ele.eta()    - nt.electrons().eta(i),
                                    ele.phi()    - nt.electrons().phi(i));

          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
        assert(which != -1);
        whichs_ele[e] = which;
        nt.set_electron_moved(which);
      }
    }

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
          if (whichtk != -1) {
            nt.tracks().set_which_jet(whichtk, whichjet);
          }
        }
      }
    }

    const size_t nmovedjets = jets_used->size() + bjets_used->size();
    std::vector<int> whichs(nmovedjets, -1);

    int i = -1;
    //FIXME? (time) 
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

    // //calculate here what is used for the reweighing : jetsumpt, jet lep dR, movedist2d, movedist3d   //FIXME? (time)
    const TVector3& move_vector = nt.move_vector();
    const double movedist2 = move_vector.Perp();
    const double movedist3 = move_vector.Mag();

    double jetsumpt = -1.0;
    double jet_pt = -1.0;
    double jetsump = -1.0;
    double electron_pt = -1.0;
    double muon_pt = -1.0;
    double jeteledR = -1.0;
    double jetmudR = -1.0;


    TLorentzVector ele_p4;
    TLorentzVector mu_p4;
    bool lep_ismu = false;
    bool lep_isele = false;
    if (whichs_ele.size() + whichs_mu.size() + whichs.size() > 3) std::cout << "SIZE PROBLEM : (ele size, mu size, jet size):  " << whichs_ele.size() << " " << whichs_mu.size() << " " << whichs.size() << std::endl;
    //only works for 1 moved ele // 1 moved mu  
    for (auto ele_idx : whichs_ele) {
      ele_p4 = nt.electrons().p4(ele_idx);
      lep_isele = true;
    }
    for (auto mu_idx : whichs_mu) {
      mu_p4 = nt.muons().p4(mu_idx);
      lep_ismu = true;
    }
    //only works for 1 moved jet 
    std::vector<int> jet0_tracks;
    TLorentzVector jet0_p4; //what is calculated from the jet sum p 

    for (auto jet_idx : whichs) {
      jet_pt = nt.jets().pt(jet_idx);
      jet0_tracks = nt.tracks().tks_for_jet(jet_idx);
    }

    for (int j = 0; j < nt.tracks().n(); ++j) {
      auto it0 = std::find(jet0_tracks.begin(), jet0_tracks.end(), j);
      if (it0 != jet0_tracks.end() && nt.tracks().pass_sel(j) && nt.tk_moved(j)){
        jet0_p4 += nt.tracks().p4(j);
        jetsump+=nt.tracks().p(j); //sump_0
        jetsumpt+=nt.tracks().pt(j); //sumpt_0
      }
    }

    if (lep_isele) {
      electron_pt = ele_p4.Pt();
      jeteledR = jet0_p4.DeltaR(ele_p4); 
    }
    if (lep_ismu) {
      muon_pt = mu_p4.Pt();
      jetmudR = jet0_p4.DeltaR(mu_p4); 
    }

  
    nt.tmw().add(movedist2, movedist3, jetsumpt, jet_pt, jetsump, electron_pt, muon_pt, jeteledR, jetmudR);

  }


  edm::Handle<MFVVertexAuxCollection> vertices;
  event.getByToken(vertices_token, vertices);
  for (const MFVVertexAux& v : *vertices) {
    const double vx = v.x - nt_filler.bs().x(v.z); // JMTBAD get rid of beamspot subtraction everywhere
    const double vy = v.y - nt_filler.bs().y(v.z);
    const double vz = v.z;

    float leading_leppt_inSV = -99.0;
    float leading_lepdxy_inSV = 99.0;
    float leading_lepdxyerr_inSV = 99.0;
    float leading_lepnsigmadxy_inSV = -99.0;
    float leading_lepiso_inSV = 99.0;
    float leading_leptype_inSV = -1.0;
    float leading_lepID_inSV = -1.0;
    float leading_lepeta_inSV = 10.0;
    float leading_lephltmatched_inSV = -1.0;
    float leading_leppasstrigpt_inSV = -1.0;
    float leading_lepjet_pairdr = 20.0;
    float trackpairdravg = 20.0;
    float avgptnolep = -1.0;


    if (!for_mctruth) {
      const double dist2move = sqrt(mag2(vx - nt.tm().move_x(),
                                         vy - nt.tm().move_y(),
                                         vz - nt.tm().move_z()));
      if (dist2move > max_dist2move)
        continue;
    }

    //need to extract the leading lepton associated to SV info for mctruth
    if(for_mctruth) {
      //step 1 : find leading lepton 
      std::vector<float> assoc_lep{-1.0};
      std::vector<float> assoc_leptype{-1.0}; // 0 == muon, 1 == electron
      std::vector<int> assoc_lepidx{-1};
      for (int i =0; i < v.nelectrons; ++i){
        assoc_lep.push_back(v.electron_pt[i]);
        assoc_leptype.push_back(1);
        assoc_lepidx.push_back(i);
      }
      for (int i =0; i < v.nmuons; ++i){
        assoc_lep.push_back(v.muon_pt[i]);
        assoc_leptype.push_back(0);
        assoc_lepidx.push_back(i);
      }
      int leading_lepidx = std::max_element(assoc_lep.begin(), assoc_lep.end()) - assoc_lep.begin();
      
      //step 2 : match to the ntuple muons/ electrons 
      if (assoc_leptype[leading_lepidx] == 0) {
        int muidx = assoc_lepidx[leading_lepidx];
        double dist2min = 0.1;
        int which = -1;
        //this should be reco vs. reco -> so there should be a match ...
        for (int i = 0, im = nt.muons().n(); i < im; ++i) { 
          const double dist2 = mag2(v.muon_pt[muidx]     - nt.muons().pt(i),
                                    v.muon_eta[muidx]   - nt.muons().eta(i),
                                    v.muon_phi[muidx]    - nt.muons().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
        assert(which != -1);
        //get the lepton info we want here : 
        leading_leppt_inSV = fabs(nt.muons().qpt(which)); 
        leading_lepeta_inSV = nt.muons().eta(which);
        leading_lepiso_inSV = nt.muons().iso(which);
        leading_lephltmatched_inSV = nt.muons().hltmatched(which); //broken ? 
        leading_leppasstrigpt_inSV = nt.muons().passtrigpt(which); //broken ? 
        leading_lepID_inSV = nt.muons().ID(which);

        //check what the minimum lepton - jet dR is (amongst all jets in the event)
        float minjetlepdR = 10.0;
        for (int j = 0, je = nt.jets().n(); j < je; ++j) {
          if (nt.jets().pt(j) < 20) continue;
          float jetlepdR = reco::deltaR(nt.jets().eta(j), nt.jets().phi(j), nt.muons().eta(which), nt.muons().phi(which));
          if (jetlepdR < minjetlepdR) minjetlepdR = jetlepdR;
        }
        leading_lepjet_pairdr = minjetlepdR;
      }

      else if (assoc_leptype[leading_lepidx] == 1) {
        int elidx = assoc_lepidx[leading_lepidx];
        double dist2min = 0.1;
        int which = -1;
        //this should be reco vs. reco -> so there should be a match ...
        for (int i = 0, im = nt.electrons().n(); i < im; ++i) { 
          const double dist2 = mag2(v.electron_pt[elidx]     - nt.electrons().pt(i),
                                    v.electron_eta[elidx]   -  nt.electrons().eta(i),
                                    v.electron_phi[elidx]    - nt.electrons().phi(i));
          if (dist2 < dist2min) {
            dist2min = dist2;
            which = i;
          }
        }
        assert(which != -1);
        //get the lepton info we want here 
        leading_leppt_inSV = fabs(nt.electrons().qpt(which)); 
        leading_lepeta_inSV = nt.electrons().eta(which);
        leading_lepiso_inSV = nt.electrons().iso(which);
        leading_lephltmatched_inSV = nt.electrons().hltmatched(which); //broken?
        leading_leppasstrigpt_inSV = nt.electrons().passtrigpt(which); //broken?
        leading_lepID_inSV = nt.electrons().ID(which);

        float minjetlepdR = 10.0;
        for (int j = 0, je = nt.jets().n(); j < je; ++j) {
          if (nt.jets().pt(j) < 20) continue;
          float jetlepdR = reco::deltaR(nt.jets().eta(j), nt.jets().phi(j), nt.electrons().eta(which), nt.electrons().phi(which));
          if (jetlepdR < minjetlepdR) minjetlepdR = jetlepdR;
        }
        leading_lepjet_pairdr = minjetlepdR;
      }
    }


    nt.vertices().add(v.chi2, vx, vy, vz, v.cxx, v.cxy, v.cxz, v.cyy, v.cyz, v.czz,
                      v.rescale_chi2, v.rescale_x - nt_filler.bs().x(v.rescale_z), v.rescale_y - nt_filler.bs().y(v.rescale_z), v.rescale_z, v.rescale_cxx, v.rescale_cxy, v.rescale_cxz, v.rescale_cyy, v.rescale_cyz, v.rescale_czz, // JMTBAD get rid of beamspot subtraction everywhere (then just use NtupleAdd here)
                      v.ntracks(), v.njets[0], v.bs2derr, v.rescale_bs2derr, false,
                      v.pt[mfv::PTracksPlusJetsByNtracks], v.eta[mfv::PTracksPlusJetsByNtracks], v.phi[mfv::PTracksPlusJetsByNtracks], v.mass[mfv::PTracksPlusJetsByNtracks]);
     
    trackpairdravg = v.trackpairdravg(); 

    float sumptnolep = 0.0;
    //FIXME? (time)
    for (size_t i = 0, ie = v.ntracks(); i < ie; ++i) {
      jmt::MinValue m(0.1);
      for (size_t j = 0, je = nt.tracks().n(); j < je; ++j){
        m(j, mag2(v.track_qpt(i) - nt.tracks().qpt(j),
                  v.track_eta[i] - nt.tracks().eta(j),
                  v.track_phi[i] - nt.tracks().phi(j)));
      }

      assert(m.i() != -1);
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
      
      const size_t iv = nt.vertices().n() - 1;
      assert(iv < 255);
      nt.tracks().set_which_sv(m.i(), iv);

      // retrieving the lepton track information 
      //do a matching for the lepton track 
      if (nt.tracks().misc_etk(m.i())) {
        leading_leptype_inSV = 1;
        leading_lepdxy_inSV = v.track_dxy[i];
        leading_lepdxyerr_inSV = v.track_dxy_err(i);
        leading_lepnsigmadxy_inSV = leading_lepdxy_inSV / leading_lepdxyerr_inSV;
      }
      if (nt.tracks().misc_mtk(m.i())) {
        leading_leptype_inSV = 0;
        leading_lepdxy_inSV = v.track_dxy[i];
        leading_lepdxyerr_inSV = v.track_dxy_err(i);
        leading_lepnsigmadxy_inSV = leading_lepdxy_inSV / leading_lepdxyerr_inSV;
      }

      if (!nt.tracks().misc_etk(m.i()) && !nt.tracks().misc_mtk(m.i())) sumptnolep += fabs(v.track_qpt(i));


      //now as long as this is not mctruth, we need to grab the lepton that was moved -> and check if it belongs to the SV 
      if (!for_mctruth) { 
        //need to match the moved lepton to one of the tracks in the SV 
        jmt::MinValue me(0.1); //min ele
        jmt::MinValue mm(0.1); //min mu 
        for (auto ele_idx : whichs_ele) {
            me(ele_idx, mag2(v.track_eta[i] - nt.electrons().eta(ele_idx),
                      v.track_phi[i] - nt.electrons().phi(ele_idx)));
        }
        for (auto mu_idx : whichs_mu) {
          mm(mu_idx, mag2(v.track_eta[i] - nt.muons().eta(mu_idx),
                      v.track_phi[i] - nt.muons().phi(mu_idx)));
        }
        
        //if there is a match, get the lepton values 
        if (me.v() + mm.v() < 0.2) { 
          //found a moved electron matched to a track in the sv
          if (me.v() < mm.v()) { 
            leading_leppt_inSV = fabs(nt.electrons().qpt(me.i())); 
            leading_lepeta_inSV = nt.electrons().eta(me.i());
            leading_lepiso_inSV = nt.electrons().iso(me.i());
            leading_lephltmatched_inSV = nt.electrons().hltmatched(me.i()); //check
            leading_leppasstrigpt_inSV = nt.electrons().passtrigpt(me.i()); //check
            leading_lepID_inSV = nt.electrons().ID(me.i());

            //check what the minimum lepton - jet dR is (amonst all jets in the event)
            float minjetlepdR = 10.0;
            for (int j = 0, je = nt.jets().n(); j < je; ++j) {
              if (nt.jets().pt(j) < 20) continue;
              float jetlepdR = reco::deltaR(nt.jets().eta(j), nt.jets().phi(j), nt.electrons().eta(me.i()), nt.electrons().phi(me.i()));
              if (jetlepdR < minjetlepdR) minjetlepdR = jetlepdR;
            }
            leading_lepjet_pairdr = minjetlepdR;
          }
          //found a moved muon matched to a track in the SV
          else if (mm.v() < me.v()) {
            leading_leppt_inSV = fabs(nt.muons().qpt(mm.i())); 
            leading_lepeta_inSV = nt.muons().eta(mm.i());
            leading_lepiso_inSV = nt.muons().iso(mm.i());
            leading_lephltmatched_inSV = nt.muons().hltmatched(mm.i()); //broken ? 
            leading_leppasstrigpt_inSV = nt.muons().passtrigpt(mm.i()); //broken ? 
            leading_lepID_inSV = nt.muons().ID(mm.i());

            //check what the minimum lepton - jet dR is (amonst all jets in the event)
            float minjetlepdR = 10.0;
            for (int j = 0, je = nt.jets().n(); j < je; ++j) {
              if (nt.jets().pt(j) < 20) continue;
              float jetlepdR = reco::deltaR(nt.jets().eta(j), nt.jets().phi(j), nt.muons().eta(mm.i()), nt.muons().phi(mm.i()));
              if (jetlepdR < minjetlepdR) minjetlepdR = jetlepdR;
            }
            leading_lepjet_pairdr = minjetlepdR;
          }
        }
      }
    } //end loop over tracks in SV 
    avgptnolep = sumptnolep/(v.ntracks() - 1);

    //FIXME? (time)
    nt.lepinvertices().add(leading_leppt_inSV, leading_lepdxy_inSV, leading_lepdxyerr_inSV, leading_lepnsigmadxy_inSV, 
      leading_lepiso_inSV, leading_leptype_inSV, leading_lepID_inSV, leading_lepeta_inSV, leading_lephltmatched_inSV,
      leading_leppasstrigpt_inSV, leading_lepjet_pairdr, trackpairdravg, avgptnolep);

  }


  //move earlier in hopes to reduce time?? 
  // if (apply_presel) {
  //   if ((!for_mctruth && (nt.tm().npreseljets() < njets_req || nt.tm().npreselbjets() < nbjets_req || (nt.tm().npreselele() + nt.tm().npreselmu()) < nlep_req))) // || nt.jets().ht() < 1000)
  //     return;
  // }
  nt_filler.finalize();
}

DEFINE_FWK_MODULE(MFVMovedTracksTreer);
