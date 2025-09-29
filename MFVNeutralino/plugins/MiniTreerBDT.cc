#include "TTree.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "JMTucker/MFVNeutralinoFormats/interface/Event.h"
#include "JMTucker/MFVNeutralinoFormats/interface/VertexAux.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtupleBDT.h"
#include "JMTucker/Tools/interface/Utilities.h"
#include "JMTucker/Tools/interface/ExtValue.h"
#include "JMTucker/Tools/interface/Math.h"
#include "JMTucker/Tools/interface/Year.h"


class MFVMiniTreerBDT : public edm::EDAnalyzer {
public:
  explicit MFVMiniTreerBDT(const edm::ParameterSet&);
  void analyze(const edm::Event&, const edm::EventSetup&);

  MFVVertexAux xform_vertex(const MFVEvent&, const MFVVertexAux&) const;

  const edm::EDGetTokenT<MFVEvent> event_token;
  const edm::EDGetTokenT<MFVVertexAuxCollection> vertex_token;
  const edm::EDGetTokenT<double> weight_token;
  const bool do_genmatching;
  const bool isData;

 
  //splitting up the satisfieslep trigger into muon/ele trigger -> just checking if the electron or muon passes pT requirement given which trigger fired -> this is for the muons and electrons in the SV 
  bool satisfiesLepTriggerPT(edm::Handle<MFVEvent> mevent, const MFVVertexAux& aux, int it, size_t trig, const edm::EventSetup& setup) { 
    if(!mevent->pass_hlt(trig)) return false;
    
    int year = int(MFVNEUTRALINO_YEAR);
    assert(year == 20161 || year == 20162 || year == 2017 || year == 2018); // in case of race conditions where the compiled macro is invalid...

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
          if ( mevent->jet_hlt_pt.at(j0) < 20. || mevent->jet_pt[j0] < 170 ) continue;
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

  TH1F* h_nsv;
  TH1F* h_nsvsel;

  mfv::MiniNtupleBDT nt;
  TTree* tree;
};

MFVMiniTreerBDT::MFVMiniTreerBDT(const edm::ParameterSet& cfg)
  : event_token(consumes<MFVEvent>(cfg.getParameter<edm::InputTag>("event_src"))),
    vertex_token(consumes<MFVVertexAuxCollection>(cfg.getParameter<edm::InputTag>("vertex_src"))),
    weight_token(consumes<double>(cfg.getParameter<edm::InputTag>("weight_src"))),
    do_genmatching(cfg.getParameter<bool>("do_genmatching")),
    isData(cfg.getParameter<bool>("isData"))
{
  edm::Service<TFileService> fs;

  h_nsv = fs->make<TH1F>("h_nsv", "", 10, 0, 10);
  h_nsvsel = fs->make<TH1F>("h_nsvsel", "", 10, 0, 10);

  tree = fs->make<TTree>("t", "");
  mfv::write_to_tree(tree, nt);
}

MFVVertexAux MFVMiniTreerBDT::xform_vertex(const MFVEvent& mevent, const MFVVertexAux& v) const {
  MFVVertexAux v2(v);
  v2.x -= mevent.bsx_at_z(v.z);
  v2.y -= mevent.bsy_at_z(v.z);
  v2.z -= mevent.bsz;
  return v2;
}

void MFVMiniTreerBDT::analyze(const edm::Event& event, const edm::EventSetup& setup) {
  // const bool is_mc = !event.isRealData();
  int nlep = 0;

  nt.clear();
  nt.run   = event.id().run();
  nt.lumi  = event.luminosityBlock();
  nt.event = event.id().event();

  edm::Handle<MFVEvent> mevent;
  event.getByToken(event_token, mevent);

  int year = int(MFVNEUTRALINO_YEAR);
  assert(year == 20161 || year == 20162 || year == 2017 || year == 2018); // in case of race conditions where the compiled macro is invalid...

  //random generator to determine if HEM check is applied (in MC)
  float hem_check = 1 + (std::rand() % 1);

  // nt.gen_flavor_code = mevent->gen_flavor_code;
  // nt.pass_hlt is currently an unsigned int, i.e. 32 bits available
  // static_assert(mfv::n_hlt_paths <= 32); 
  // nt.pass_hlt = mevent->pass_hlt_bits();
  // nt.l1_htt = mevent->l1_htt;
  // nt.l1_myhtt = mevent->l1_myhtt;
  // nt.l1_myhttwbug = mevent->l1_myhttwbug;
  // nt.hlt_ht = mevent->hlt_ht;
  // nt.bsx = mevent->bsx;
  // nt.bsy = mevent->bsy;
  // nt.bsz = mevent->bsz;
  // nt.bsdxdz = mevent->bsdxdz;
  // nt.bsdydz = mevent->bsdydz;
  // nt.npv = int2uchar(mevent->npv);
  // nt.pvx = mevent->pvx - mevent->bsx_at_z(mevent->pvz);
  // nt.pvy = mevent->pvy - mevent->bsy_at_z(mevent->pvz);
  // nt.pvz = mevent->pvz - mevent->bsz;
  // nt.npu = is_mc ? int2uchar(mevent->npu) : 0;

  edm::Handle<double> weight;
  event.getByToken(weight_token, weight);
  nt.weight = *weight;


  //event level info first 
  nt.njets = int2uchar(mevent->njets(mfv::min_jet_pt));
  nt.jetht = mevent->jet_ht(mfv::min_jet_pt);
  nt.nmuons = mevent->nmuons();
  nt.nelectrons = mevent->nelectrons();
  if (nt.njets > 50)
    throw cms::Exception("CheckYourPremises") << "too many jets in event: " << nt.njets;
  if (nt.nmuons > 50)
    throw cms::Exception("CheckYourPremises") << "too many muons in event: " << nt.nmuons;
  if (nt.nelectrons > 50)
    throw cms::Exception("CheckYourPremises") << "too many electrons in event: " << nt.nelectrons;

  for (int i = 0; i < mevent->njets(); ++i) {
    if (mevent->jet_pt[i] < mfv::min_jet_pt)
      continue;
    nt.jet_pt[i] = mevent->jet_pt[i];
    nt.jet_eta[i] = mevent->jet_eta[i];
    nt.jet_phi[i] = mevent->jet_phi[i];
    nt.jet_energy[i] = mevent->jet_energy[i];
  }
  nt.jet0_pt = mevent->nth_jet_pt(0);
  nt.jet1_pt = mevent->nth_jet_pt(1);

  //////////////////////////////////////////////////////////////
  //FIXME : require leptons to pass standard cuts 
  std::vector<std::tuple<std::string, int, float, float, float, float, float, float, float>> lep_tuple; // store leptons w/ pt >= 50 {lep, idx, pt, phi, eta, dxy, dxyerr, x, y}  

  for (int i = 0; i < mevent->nelectrons(); ++i) {
    nlep +=1;
    if (mevent->electron_pt[i] >= 50.0) {
      lep_tuple.push_back(std::make_tuple("electron", i, mevent->electron_pt[i], 
                                          mevent->electron_phi[i], mevent->electron_eta[i], 
                                          mevent->electron_dxybs[i], mevent->electron_dxyerr[i],
                                          mevent->electron_x[i], mevent->electron_y[i]));
    }
    nt.electron_pt[i] = mevent->electron_pt[i];
    nt.electron_eta[i] = mevent->electron_eta[i];
    nt.electron_phi[i] = mevent->electron_phi[i];
    nt.electron_sigmadxy[i] = mevent->electron_dxybs[i]/mevent->electron_dxyerr[i];    
  }

  for (int i = 0; i < mevent->nmuons(); ++i) {
    nlep +=1;
    if (mevent->muon_pt[i] >= 50.0) {
      lep_tuple.push_back(std::make_tuple("muon", i, mevent->muon_pt[i], 
                                          mevent->muon_phi[i], mevent->muon_eta[i],
                                          mevent->muon_dxybs[i], mevent->muon_dxyerr[i],
                                          mevent->muon_x[i], mevent->muon_y[i]));
    }
    nt.muon_pt[i] = mevent->muon_pt[i];
    nt.muon_eta[i] = mevent->muon_eta[i];
    nt.muon_phi[i] = mevent->muon_phi[i];
    nt.muon_sigmadxy[i] = mevent->muon_dxybs[i]/mevent->muon_dxyerr[i];
  }

  std::vector<std::tuple<std::string, int, float, float, float, float, float, float, float>> leading_lep_tuple; // store only max two highest 
  // {lep 0, idx 1, pt 2, phi 3, eta 4, dxy 5, dxyerr 6 x 7, y 8} 

  //first need to sort the tuple by pt 
  std::sort(lep_tuple.begin(), lep_tuple.end(), [](auto &left, auto &right) {
      return std::get<2>(left) > std::get<2>(right);
  });

  //now fill the two highest lep, sellep pairs --> but we can only do it as long as lep_tuple has ≥ 1 
  int ilep = 0;
  for (const auto& n : lep_tuple) {
    leading_lep_tuple.push_back(n);
    ilep +=1;
    if (ilep >= 2) break;
  }

  nt.nleptons=nlep;
//{lep 0, idx 1, pt 2, phi 3,  eta 4, dxy 5, dxyerr 6, x 7, y 8} 
  if (leading_lep_tuple.size() > 0) {  
    nt.leading_lep_pt = std::get<2>(leading_lep_tuple[0]);
    nt.leading_lep_dxy = std::get<5>(leading_lep_tuple[0]);
    nt.leading_lep_dxyerr = std::get<6>(leading_lep_tuple[0]);
    nt.leading_lep_sigmadxy = std::get<5>(leading_lep_tuple[0])/std::get<6>(leading_lep_tuple[0]);
    nt.leading_jetlep_pt = mevent->nth_jet_pt(0) + std::get<2>(leading_lep_tuple[0]); 
    if (leading_lep_tuple.size() > 1) {
      nt.subleading_lep_pt = std::get<2>(leading_lep_tuple[1]);
      nt.subleading_lep_dxy = std::get<5>(leading_lep_tuple[1]);
      nt.subleading_lep_dxyerr = std::get<6>(leading_lep_tuple[1]);
      nt.subleading_lep_sigmadxy = std::get<5>(leading_lep_tuple[1])/std::get<6>(leading_lep_tuple[1]);
      nt.double_jetlep_pt = mevent->nth_jet_pt(0) + mevent->nth_jet_pt(1) + std::get<2>(leading_lep_tuple[0]) + std::get<2>(leading_lep_tuple[1]); 
    }
    else {
      nt.double_jetlep_pt = mevent->nth_jet_pt(0) + mevent->nth_jet_pt(1) + std::get<2>(leading_lep_tuple[0]); 
    }
  }
//////////////////////////////////////////////////////////////

  for (int i = 0; i < 2; ++i) {
    const double z = mevent->gen_lsp_decay[i*3+2];
    nt.gen_x[i] = mevent->gen_lsp_decay[i*3+0] - mevent->bsx_at_z(z);
    nt.gen_y[i] = mevent->gen_lsp_decay[i*3+1] - mevent->bsy_at_z(z);
    nt.gen_z[i] = z - mevent->bsz;
    nt.gen_lsp_pt[i] = mevent->gen_lsp_pt[i];
    nt.gen_lsp_eta[i] = mevent->gen_lsp_eta[i];
    nt.gen_lsp_phi[i] = mevent->gen_lsp_phi[i];
    nt.gen_lsp_mass[i] = mevent->gen_lsp_mass[i];
  }
  nt.gen_daughters = mevent->gen_daughters;
  nt.gen_daughter_id = mevent->gen_daughter_id;
  nt.gen_leptons = mevent->gen_leptons;


  edm::Handle<MFVVertexAuxCollection> input_vertices;
  event.getByToken(vertex_token, input_vertices);

  MFVVertexAuxCollection vertices;
  MFVVertexAuxCollection genmatch_vertices;

  h_nsv->Fill(input_vertices->size());

  std::vector<float> genvertex0_dR;
  std::vector<float> genvertex1_dR;

  std::vector<float> lep_sv_2ddist;
  std::vector<float> dphi;
  std::vector<float> dphi_2;

  for (const MFVVertexAux& v : *input_vertices) {
    // if : signal -- only consider the gen matched vertices : will have to find the closest vertex to each gen vertex 

    // FIXME : ttbar has gen level info so will enter this loop and consequently be considered like signal. current fix is to add another condition but should be reworked 
    if (do_genmatching) {
      if ( (mevent->gen_daughters.size() != 0) & (mevent->lspdist2d() != 0) ) {
        jmt::MinValue d;
        for (int igenv = 0; igenv < 2; ++igenv) {
          double genx = mevent->gen_lsp_decay[igenv*3+0];
          double geny = mevent->gen_lsp_decay[igenv*3+1];
          d(igenv, mag(v.x-genx, v.y-geny));
        }
        if (d.i() == 0) {
          genvertex0_dR.push_back(d.v());
          genvertex1_dR.push_back(10.);
        }
        else if (d.i() == 1) {
          genvertex1_dR.push_back(d.v());
          genvertex0_dR.push_back(10.);
        }
      }
    }
    //background -- just fill the vertex information for all (or for signal when not need genmatching)
    else {
      vertices.push_back(xform_vertex(*mevent, v));
      // math::XYZVector bs2sv = v.position() - beamspot->position();
      math::XYZPoint vposition(v.x, v.y, v.z);
      math::XYZPoint bs(mevent->bsx, mevent->bsy, mevent->bsz);
      math::XYZVector bs2sv = vposition - bs;
      nt.ntracks.push_back(v.ntracks());

      
      float sumpt = 0;
      // float sumptx = 0;
      // float sumpty = 0;
      // float sumptz = 0;
      float sumeta = 0;
      float sumphi = 0;

      std::vector<std::set<int>> sv_bjetasso(3);
      std::vector<unsigned int> nbtrack = {0,0,0};

      for (int i =0; i < v.ntracks(); ++i) {
        sumpt += fabs(v.track_pt(i));
        // sumptx += v.track_px[i];
        // sumpty += v.track_py[i];
        // sumptz += v.track_pz[i];
        sumeta += v.track_eta[i];
        sumphi += v.track_phi[i];
        // double nsigmadxybs = (v.track_dxy[i] / v.track_dxy_err(i));
        // double nsigmadz = (v.track_dz[i] / v.track_dz_err(i) );

        //   // track information -- not present in ntuples; should check again       
        //   // nt.trackmass.push_back(track_p4(i, mass));
        //   nt.trackpt.push_back(v.track_pt(i));
        //   nt.trackpterr.push_back(v.track_pt_err[i]);
        //   nt.tracketa.push_back(v.track_eta[i]);
        //   nt.tracketaerr.push_back(v.track_eta_err(i));
        //   nt.trackphi.push_back(v.track_phi[i]);
        //   nt.trackphierr.push_back(v.track_phi_err(i));
        //   nt.tracknsigmadxybs.push_back(nsigmadxybs);
        //   nt.trackdxy.push_back(v.track_dxy[i]);
        //   nt.trackdxyerr.push_back(v.track_dxy_err(i));
        //   nt.trackdz.push_back(v.track_dz[i]);
        //   nt.trackdzerr.push_back(v.track_dz_err(i));
        //   nt.tracknsigmadz.push_back(nsigmadz);
        //   //nt.trackabsnsigmadz.push_back(fabs(nsigmadz));
        //   nt.trackchi2ndof.push_back(v.track_chi2dof(i));
        //   nt.track_injet.push_back(v.track_injet[i]);


        //determine if any of the tracks is assocated to bjet 
        double match_threshold = 1.3;
        int jet_index = 255;
        for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
          double a = fabs(v.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
          double b = fabs(v.track_eta[i] - mevent->jet_track_eta[j]) + 1;
          double c = fabs(v.track_phi[i] - mevent->jet_track_phi[j]) + 1;
          if (a * b * c < match_threshold) {
            match_threshold = a * b * c;
            jet_index = mevent->jet_track_which_jet[j];
          }
        }
        if (jet_index != 255) {
          for(int ibdisc=0; ibdisc<3; ++ibdisc){
            if (mevent->is_btagged(jet_index, ibdisc)){
              sv_bjetasso[ibdisc].insert((int) jet_index);
              ++nbtrack[ibdisc];
            }
          }
        }
      }
      // //filling for bjets 
      nt.nbtags_loose.push_back(sv_bjetasso[0].size());
      nt.nbtks_loose.push_back(nbtrack[0]);
      nt.nbtags_med.push_back(sv_bjetasso[1].size());
      nt.nbtks_med.push_back(nbtrack[1]);
      nt.nbtags_tight.push_back(sv_bjetasso[2].size());
      nt.nbtks_tight.push_back(nbtrack[2]);

      nt.maxtrackpt.push_back(v.maxtrackpt());
      nt.avgpt.push_back(sumpt/v.ntracks());
      // nt.sumptx.push_back(sumptx);
      // nt.sumpty.push_back(sumpty);
      // nt.sumptz.push_back(sumptz);
      nt.tracketaavg.push_back(sumeta/v.ntracks());
      nt.trackphiavg.push_back(sumphi/v.ntracks());
      // nt.ntrackssharedwpv.push_back(v.ntrackssharedwpv());
      // nt.ntrackssharedwpvs.push_back(v.ntrackssharedwpvs());
      // nt.ntracksetagt1p5.push_back(v.ntracksetagt(1.5));
      nt.sumpt2.push_back(v.sumpt2());
      // nt.x.push_back(v.x);
      // nt.y.push_back(v.y);
      // nt.z.push_back(v.z);
      nt.rescale_bs2derr.push_back(v.rescale_bs2derr);
      nt.rescale_bs2ddist.push_back(v.rescale_bs2ddist);
      nt.bs2derr.push_back(v.bs2derr);
      // nt.bs2ddist.push_back(v.bs2ddist);
      nt.bsbs2ddist.push_back(mevent->bs2ddist(v));
      // nt.pvdz.push_back(v.pvdz());
      // nt.pvdzerr.push_back(v.pvdzerr());
      // nt.chi2.push_back(v.chi2);
      // nt.ndof.push_back(v.ndof());
      // nt.chi2dof.push_back(v.chi2dof());
      nt.nele_inSV.push_back(v.nelectrons);
      nt.nmu_inSV.push_back(v.nmuons);
      nt.nlep_inSV.push_back(v.nelectrons + v.nmuons);
  
      //get the highest pt ele, highest pt mu, highest pt lep associated to SV 
      //initialize to -1 -> means there is no assoc lep 
      std::vector<float> assoc_ele{-1.0};
      std::vector<float> assoc_mu{-1.0};
      std::vector<float> assoc_lep{-1.0};
      std::vector<float> assoc_leptype{-1.0}; // 0 == muon, 1 == electron

      std::vector<float> assoc_eleiso{-1.0};
      std::vector<float> assoc_muiso{-1.0};
      std::vector<float> assoc_lepiso{-1.0};
      std::vector<float> assoc_lepID {-5.0};
      std::vector<float> assoc_lepnsigmadxy_rescaled {-999.0};
      std::vector<float> assoc_lepnsigmadxy {-999.0};
      std::vector<float> assoc_lepdxy {-999.0};
      std::vector<float> assoc_lepdxyerr {-999.0};
      std::vector<float> assoc_lepeta {-999.0};
      std::vector<float> assoc_lepphi { -999.0};
      std::vector<float> assoc_lephltmatch {-1.0};
      std::vector<float> assoc_leptrigpt {-1.0}; //boolean flag if leading lepton passes the trigger pT threshold 
      //all assoc jet pt? 
      // v.pt[mfv::PJetsByNtracks]

      int nselele = 0;
      for (int i =0; i < v.nelectrons; ++i){
        //here need to apply HEM : figure out if electron is in eta/phi + above 30 GeV. 
        // in MC : randomly decide if to keep this electron 
        if (year == 2018) { 
          if (!isData) {
            if (hem_check > 0.352275515) {
              if (v.electron_pt[i] > 30 && (-3.0 < v.electron_eta[i]) && ( v.electron_eta[i] < -1.3) && (-1.57 < v.electron_phi[i]) && (v.electron_phi[i] < -0.87)) continue;
            }
          }
          else {
            if (v.electron_pt[i] > 30 && (-3.0 < v.electron_eta[i]) && (v.electron_eta[i] < -1.3) && (-1.57 < v.electron_phi[i]) && (v.electron_phi[i] < -0.87)) {
              if (event.id().run() >= 319077) continue; // starting w/ run number 319077 do not use this electron 
            }
          }
        }

        nt.all_elept_inSV.push_back(v.electron_pt[i]);
        nt.all_leppt_inSV.push_back(v.electron_pt[i]);
        assoc_ele.push_back(v.electron_pt[i]);
        assoc_lep.push_back(v.electron_pt[i]);
        assoc_leptype.push_back(1);
        assoc_lepiso.push_back(v.electron_iso[i]);
        assoc_lepeta.push_back(v.electron_eta[i]);
        assoc_lepphi.push_back(v.electron_phi[i]);
        assoc_lephltmatch.push_back(v.ele_is_hltmatched[i]);
        
        bool satisfies_leptrigpt = false;
        for(size_t trig : mfv::ElectronTriggers) { 
          satisfies_leptrigpt = satisfiesLepTriggerPT(mevent, v, i, trig, setup);
          if (satisfies_leptrigpt) break; //if find a match, then break out of loop 
        }
        assoc_leptrigpt.push_back(satisfies_leptrigpt);

        //below is standard cutbased ID w/out iso 
        // auto temp = v.electron_ID[i]; 
        auto temp = v.electron_ID_noiso[i]; 
        int id = 0;
        if ( temp[0] == 0 ) id = 0; 
        if ( temp[0] == 1 ) id = 1;
        if ( temp[1] == 1 ) id = 2; 
        if ( temp[2] == 1 ) id = 3;
        if ( temp[3] == 1 ) id = 4;
        // 


        assoc_lepID.push_back(id);
        assoc_lepnsigmadxy_rescaled.push_back(fabs(v.electron_dxybs[i])/v.rescaled_electron_dxyerr[i]);
        assoc_lepnsigmadxy.push_back(fabs(v.electron_dxybs[i])/v.electron_dxyerr[i]);
        assoc_lepdxy.push_back(fabs(v.electron_dxybs[i]));
        assoc_lepdxyerr.push_back(v.rescaled_electron_dxyerr[i]); 

        if (v.electron_iso[i] < 0.1 && id == 4) nselele +=1; 

      } 
      int nselmu = 0;
      for (int i =0; i < v.nmuons; ++i){
        nt.all_mupt_inSV.push_back(v.muon_pt[i]);
        nt.all_leppt_inSV.push_back(v.muon_pt[i]);
        assoc_mu.push_back(v.muon_pt[i]);
        assoc_lep.push_back(v.muon_pt[i]);
        assoc_leptype.push_back(0);
        assoc_lepiso.push_back(v.muon_iso[i]);
        assoc_lepeta.push_back(v.muon_eta[i]);
        assoc_lepphi.push_back(v.muon_phi[i]);
        assoc_lephltmatch.push_back(v.mu_is_hltmatched[i]);

        bool satisfies_leptrigpt = false;
        for(size_t trig : mfv::MuonTriggers) { 
          satisfies_leptrigpt = satisfiesLepTriggerPT(mevent, v, i, trig, setup);
          if (satisfies_leptrigpt) break; //if find a match, then break out of loop 
        }
        assoc_leptrigpt.push_back(satisfies_leptrigpt);

        auto temp = v.muon_ID[i]; 
        int id = 0;
        if ( temp[0] == 0 ) id = 0; 
        if ( temp[0] == 1 ) id = 1;
        if ( temp[1] == 1 ) id = 2; 
        if ( temp[2] == 1 ) id = 3;
        assoc_lepID.push_back(id);
        assoc_lepnsigmadxy_rescaled.push_back(fabs(v.muon_dxybs[i])/v.rescaled_muon_dxyerr[i]);
        assoc_lepnsigmadxy.push_back(fabs(v.muon_dxybs[i])/v.muon_dxyerr[i]);
        assoc_lepdxy.push_back(fabs(v.muon_dxybs[i]));
        assoc_lepdxyerr.push_back(v.rescaled_muon_dxyerr[i]); 
        
        if (v.muon_iso[i] < 0.1 && id >1) nselmu +=1;
      } 

      float leading_leppt = *max_element(assoc_lep.begin(), assoc_lep.end());
      int leading_lepidx = std::max_element(assoc_lep.begin(), assoc_lep.end()) - assoc_lep.begin();

      nt.leading_leppt_inSV.push_back(leading_leppt);
      nt.leading_leptype_inSV.push_back(assoc_leptype[leading_lepidx]);
      nt.leading_lepiso_inSV.push_back(assoc_lepiso[leading_lepidx]);
      nt.leading_lepID_inSV.push_back(assoc_lepID[leading_lepidx]);
      nt.leading_lepnsigmadxy_inSV.push_back(assoc_lepnsigmadxy[leading_lepidx]);
      nt.leading_lepnsigmadxy_rescaled_inSV.push_back(assoc_lepnsigmadxy_rescaled[leading_lepidx]);
      nt.leading_lepdxy_inSV.push_back(assoc_lepdxy[leading_lepidx]);
      nt.leading_lepdxyerr_inSV.push_back(assoc_lepdxyerr[leading_lepidx]);
      nt.leading_lepeta_inSV.push_back(assoc_lepeta[leading_lepidx]);
      nt.leading_lepphi_inSV.push_back(assoc_lepphi[leading_lepidx]);
      nt.leading_lephltmatched_inSV.push_back(assoc_lephltmatch[leading_lepidx]);
      nt.leading_leppasstrigpt_inSV.push_back(assoc_leptrigpt[leading_lepidx]); //leading lepton also passes the pT trigger requirement

      nt.nselele_inSV.push_back(nselele);
      nt.nselmu_inSV.push_back(nselmu);


      float leading_elept = *max_element(assoc_ele.begin(), assoc_ele.end());
      nt.leading_elept_inSV.push_back(leading_elept);

      float leading_mupt = *max_element(assoc_mu.begin(), assoc_mu.end());
      nt.leading_mupt_inSV.push_back(leading_mupt);

      float nmleptracketaavg = 0;
      float nmleptrackphiavg = 0;
      if (assoc_lepeta[leading_lepidx] > 0) //if positive 
        nmleptracketaavg = (sumeta-assoc_lepeta[leading_lepidx])/(v.ntracks()-1);
      else if (assoc_lepeta[leading_lepidx] < 0) //if negative 
        nmleptracketaavg = (sumeta+assoc_lepeta[leading_lepidx])/(v.ntracks()-1);
      if (assoc_lepphi[leading_lepidx] > 0) //if positive 
        nmleptrackphiavg = (sumphi-assoc_lepphi[leading_lepidx])/(v.ntracks()-1);
      else if (assoc_lepphi[leading_lepidx] < 0) //if positive 
        nmleptrackphiavg = (sumphi+assoc_lepphi[leading_lepidx])/(v.ntracks()-1);
      
      nt.nmleptracketaavg.push_back(nmleptracketaavg);
      nt.nmleptrackphiavg.push_back(nmleptrackphiavg);
      nt.dr_avgtracks_lep.push_back(sqrt(pow(2, (assoc_lepeta[leading_lepidx]-nmleptracketaavg)) + pow(2, (assoc_lepphi[leading_lepidx]-nmleptrackphiavg))));


      // now leading jet 
      std::vector<float> assoc_jet{-1.0};
      std::vector<float> assoc_jeteta{-999.0};
      std::vector<float> assoc_jetphi{-999.0};

      for (size_t ijet = 0; ijet < v.njets[mfv::JByNtracks]; ++ijet) {
        assoc_jet.push_back(v.jet_pt[mfv::JByNtracks][ijet]);
      }

      float leading_jetpt = *max_element(assoc_jet.begin(), assoc_jet.end());

      float minjetlepdR = 10.0;
      if (leading_leppt > 0) { 
        if (mevent->jet_id.size() != 0) {
          for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
            if (mevent->jet_pt[ijet] <  mfv::min_jet_pt) continue; 
            float jetlepdR = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
            if (jetlepdR < minjetlepdR) {
              minjetlepdR = jetlepdR;
            }
          }
        }
      }
      nt.leading_lepjet_pairdr.push_back(minjetlepdR);

      nt.leading_jetpt_inSV.push_back(leading_jetpt);
      
      //find the track pT "assoc" to the lepton; also determine costheta for : just the lepton, and all tracks except the lepton 
      // math::XYZTLorentzVector sumtk_p4;
      // math::XYZTLorentzVector tknolep_p4;
      // math::XYZTLorentzVector lep_p4;

      if (leading_leppt > 0){ 
        std::vector<double> mindR;
        for (int i = 0; i < v.ntracks(); ++i) {
          // sumtk_p4 +=math::XYZTLorentzVector(v.track_px[i], v.track_py[i], v.track_pz[i], v.track_p(i));
          double dr = reco::deltaR(v.track_eta[i], v.track_phi[i], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
          mindR.push_back(dr);
        }
        nt.closestdR_track_leadinglep.push_back(*min_element(mindR.begin(), mindR.end()));
        int track_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
        nt.avgptnolep.push_back((sumpt - v.track_pt(track_idx))/(v.ntracks()-1));
        
        // lep_p4 = math::XYZTLorentzVector(v.track_px[track_idx], v.track_py[track_idx], v.track_pz[track_idx], v.track_p(track_idx));
        // tknolep_p4 = sumtk_p4 - lep_p4; 
        
        // nt.costhlepmombs.push_back(jmt::costh2(lep_p4, bs2sv));
        // nt.costhnolepmombs.push_back(jmt::costh2(tknolep_p4, bs2sv));

      }
      else if (leading_leppt < 0) {
        nt.closestdR_track_leadinglep.push_back(20);
        nt.avgptnolep.push_back(sumpt/(v.ntracks()));
        // nt.costhlepmombs.push_back(-5.0);
        // nt.costhnolepmombs.push_back(jmt::costh2(sumtk_p4, bs2sv)); 
      }


      //figuring out : if lepton is in the vertex
      // -1 : lepton not avail. 0 : lepton not in vertex. 1 : lepton in vertex. 
      std::pair<int, int> lep{-1, -1}; // {leading lep == 0, subleading lep == 1}
      TLorentzVector lep0_sv_p4;
      TLorentzVector lep1_sv_p4;
      TLorentzVector sv_p4; 
     
      //first determine if lepton is in SV. : check the leading and subleading leptons to see if they are in the vertex 
      //{lep 0, idx 1, pt 2, phi 3,  eta 4, dxy 5, dxyerr 6, x 7, y 8} 
      int ilep = 0;
      for (const auto& p : leading_lep_tuple) {
        if (std::get<0>(p) == "electron") {
          ilep > 0 ? lep.second = 0 : lep.first = 0;
          for (int i=0; i < v.nelectrons; ++i) {
            if (std::get<3>(p) == v.electron_phi[i]) {
              if (std::get<4>(p) == v.electron_eta[i]) {
                ilep > 0 ? lep.second = 1 : lep.first = 1;
              }
            }
          }
        }
        if (std::get<0>(p) == "muon") {
          ilep > 0 ? lep.second = 0 : lep.first = 0;
          for (int i=0; i < v.nmuons; ++i) {
            if (std::get<3>(p) == v.muon_phi[i]) {
              if (std::get<4>(p) == v.muon_eta[i]) {
                ilep > 0 ? lep.second = 1 : lep.first = 1;
              }
            }
          }
        }
        ilep += 1;
      }
      //now to calculate the lepton-SV distance & lepton-SV deltaphi 
      // making sure the leading lep is not in SV
      float lep0_sv_2ddist = -999.0;
      float lep1_sv_2ddist = -999.0;
      float dphi0 = -999.0; //calcuation using p4 vector
      float dphi1 = -999.0; 
      float dphi0_2 = -999.0; // calculation using the arctan(SV-BS, lepton_phi)
      float dphi1_2 = -999.0; // calculation using the arctan(SV-BS, lepton_phi)

      if (lep.first == 0) { 
        for (int i =0; i < v.ntracks(); ++i) {
          TLorentzVector vt;
          vt.SetPtEtaPhiM(v.track_pt(i), v.track_eta[i], v.track_phi[i], 0);
          lep0_sv_p4 += vt;
        }
        lep0_sv_2ddist = (mag( (v.x - std::get<7>(leading_lep_tuple[0])), (v.y - std::get<8>(leading_lep_tuple[0])) ));
        dphi0 = fabs(reco::deltaPhi( lep0_sv_p4.Phi(), std::get<3>(leading_lep_tuple[0])) );
        dphi0_2 = fabs(reco::deltaPhi(atan2(v.y - mevent->bsy, v.x - mevent->bsx), std::get<3>(leading_lep_tuple[0])));
      }
      //making sure the subleading lep is not in SV 
      if (lep.second == 0) {
        for (int i =0; i < v.ntracks(); ++i) {
          TLorentzVector vt;
          vt.SetPtEtaPhiM(v.track_pt(i), v.track_eta[i], v.track_phi[i], 0);
          lep1_sv_p4 += vt;
        }
        lep1_sv_2ddist = (mag( (v.x - std::get<7>(leading_lep_tuple[1])), (v.y - std::get<8>(leading_lep_tuple[1])) ));
        dphi1 = fabs(reco::deltaPhi( lep0_sv_p4.Phi(), std::get<3>(leading_lep_tuple[1])) );
        dphi1_2 = fabs(reco::deltaPhi(atan2(v.y - mevent->bsy, v.x - mevent->bsx), std::get<3>(leading_lep_tuple[1])));
      }

      //now that I have the distance and dphi between lep and sv, now decide which lep - sv pair to pick up 
      // ie largest lep-sv distance & lep-sv dphi. 
      // store in a vector 
      if (lep0_sv_2ddist > lep1_sv_2ddist ) lep_sv_2ddist.push_back(lep0_sv_2ddist);
      if (lep1_sv_2ddist > lep0_sv_2ddist ) lep_sv_2ddist.push_back(lep1_sv_2ddist);
      if ( (lep1_sv_2ddist == -999.0) && (lep0_sv_2ddist == -999.0) ) lep_sv_2ddist.push_back(-999.0); // just as placeholder? 
      if (dphi0 > dphi1) dphi.push_back(dphi0);
      if (dphi1 > dphi0) dphi.push_back(dphi1);
      if ( (dphi0 == -999.0) && (dphi1 == -999.0) )  dphi.push_back(-999.0); // placeholder ? 
      if (dphi0_2 > dphi1_2) dphi_2.push_back(dphi0_2);
      if (dphi1_2 > dphi0_2) dphi_2.push_back(dphi1_2);
      if ( (dphi0_2 == -999.0 ) && (dphi1_2 == -999.0) ) dphi_2.push_back(-999.0); // placeholder ? 

      //just also wanting the basic phi, eta variables of the SV (here we want all tracks because not comparing to lep)
      math::XYZTLorentzVector mom_p4;
      float sum_trackdxynsigma = 0;
      for (int i = 0; i < v.ntracks(); ++i) {
        TLorentzVector vt;
        vt.SetPtEtaPhiM(v.track_pt(i), v.track_eta[i], v.track_phi[i], 0);
        sv_p4 += vt;
        mom_p4 +=math::XYZTLorentzVector(v.track_px[i], v.track_py[i], v.track_pz[i], v.track_p(i));
        sum_trackdxynsigma += fabs(v.track_dxy_nsigma(i));
      }
      nt.sv_eta.push_back(sv_p4.Eta());
      nt.sv_phi.push_back(sv_p4.Phi());
      nt.costhmombs.push_back(jmt::costh2(mom_p4, bs2sv));
      //angle variables
      nt.trackpairdetaavg.push_back(v.trackpairdetaavg());
      // nt.trackpairdetamin.push_back(v.trackpairdetamin());
      // nt.trackpairdetamax.push_back(v.trackpairdetamax());

      // nt.trackpairdphiavg.push_back(v.trackpairdetaavg());
      // nt.trackpairdphimin.push_back(v.trackpairdetamin());
      // nt.trackpairdphimax.push_back(v.trackpairdetamax());

      nt.trackpairdravg.push_back(v.trackpairdravg());
      nt.trackpairdrmax.push_back(v.trackpairdrmax());
      nt.trackpairdrmin.push_back(v.trackpairdrmin());


      nt.trackpairdptrms.push_back(v.trackpairdptrms());
      nt.trackpairdptavg.push_back(v.trackpairdptavg());
      nt.trackpairdptmax.push_back(v.trackpairdptmax());
      nt.trackpairdptmin.push_back(v.trackpairdptmin());
      nt.trackptrms.push_back(v.trackptrms());
      nt.trackptavg.push_back(v.trackptavg());
      nt.trackptmax.push_back(v.maxtrackpt());
      nt.trackptmin.push_back(v.mintrackpt());

      //mass variables (tri -track because that's the min # of tracks required in vertex)
      // nt.tracktripmassavg.push_back(v.tracktripmassavg());
      nt.tracktripmassmax.push_back(v.tracktripmassmax());
      // nt.tracktripmassmin.push_back(v.tracktripmassmin());

      nt.trackdxynsigmaavg.push_back(v.trackdxynsigmaavg());
      nt.trackdxynsigmamax.push_back(v.trackdxynsigmamax());
      nt.trackdxynsigmamin.push_back(v.trackdxynsigmamin());
      nt.trackdxynsigmarms.push_back(v.trackdxynsigmarms());
     // nt.sum_trackdxynsigma.push_back(sum_trackdxynsigma/v.ntracks());

      // nt.costhmombs.push_back(v.costhmombs_alltks()); //found out this is the same as costhmombs (the orig) --> it is just tracks in SV (not associated to jets)
      nt.costhtksjetsntkmombs.push_back(v.costhmombs(mfv::PTracksPlusJetsByNtracks));
      // nt.costhtkmomvtxdispmin.push_back(v.costhtkmomvtxdispmin()); 
      // nt.costhtkmomvtxdispmax.push_back(v.costhtkmomvtxdispmax());
      // nt.costhtkmomvtxdispavg.push_back(v.costhtkmomvtxdispavg());
      // nt.costhjetmomvtxdispmin.push_back(v.costhjetmomvtxdispmin()); 
      // nt.costhjetmomvtxdispmax.push_back(v.costhjetmomvtxdispmax());
      // nt.costhjetmomvtxdispavg.push_back(v.costhjetmomvtxdispavg());

      //other variables (new set) 
      // nt.ntracksptgt10.push_back(v.ntracksptgt(10));
      // nt.jetsntkpt.push_back(v.pt[mfv::PJetsByNtracks]);
      // nt.tksjetsntkpt.push_back(v.pt[mfv::PTracksPlusJetsByNtracks]);
      // nt.tksjetsntkmass.push_back(v.mass[mfv::PTracksPlusJetsByNtracks]);

      //jet-SV deltaphi
      std::vector<double> jetdeltaphis;
      for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
        if (mevent->jet_pt[ijet] < mfv::min_jet_pt) continue;
        const double dphi = reco::deltaPhi(atan2(v.y - mevent->bsy, v.x - mevent->bsx), mevent->jet_phi[ijet]);
        nt.alljetsvdeltaphi.push_back(dphi);
        jetdeltaphis.push_back(fabs(dphi));
      }
      if (jetdeltaphis.size() != 0) {
        std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
        nt.maxjetsvdeltaphi.push_back(jetdeltaphis.back()); 
        nt.minjetsvdeltaphi.push_back(jetdeltaphis[0]);
        nt.avgjetsvdeltaphi.push_back((jetdeltaphis.begin(), jetdeltaphis.end(),0) / jetdeltaphis.size());
      }
      if (jetdeltaphis.size() == 0) {
        nt.minjetsvdeltaphi.push_back(-999.0);
        nt.maxjetsvdeltaphi.push_back(-999.0);
        nt.avgjetsvdeltaphi.push_back(-999.0);
      }
    }
  }


  // now just for signal when want to gen_match -- choosing the reconstructed vertices that are closest to the gen vertices 
  if (do_genmatching) {
    if (genvertex0_dR.size() !=0) {
      float best_sv_gen0_dR = *min_element(genvertex0_dR.begin(), genvertex0_dR.end());
      int best_sv_gen0_isv = std::min_element(genvertex0_dR.begin(), genvertex0_dR.end()) - genvertex0_dR.begin();

      // these two cases should be filled if we have nsv == 2 or nsv == 1 (matched)
      if (best_sv_gen0_dR < 0.02) {
        const MFVVertexAux& gensv = input_vertices->at(best_sv_gen0_isv);
        genmatch_vertices.push_back(gensv);
      }
      
    }
    if (genvertex1_dR.size() !=0) {
      float best_sv_gen1_dR = *min_element(genvertex1_dR.begin(), genvertex1_dR.end());
      int best_sv_gen1_isv = std::min_element(genvertex1_dR.begin(), genvertex1_dR.end()) - genvertex1_dR.begin();
      
      if (best_sv_gen1_dR < 0.02) {
        const MFVVertexAux& gensv = input_vertices->at(best_sv_gen1_isv);
        genmatch_vertices.push_back(gensv);
      }
    }

    if (genmatch_vertices.size() != 0) {
      for (const MFVVertexAux& sv : genmatch_vertices) {
        vertices.push_back(xform_vertex(*mevent, sv));
        math::XYZPoint vposition(sv.x, sv.y, sv.z);
        math::XYZPoint bs(mevent->bsx, mevent->bsy, mevent->bsz);
        math::XYZVector bs2sv = vposition - bs;


        nt.ntracks.push_back(sv.ntracks());
        float sumpt = 0;
        // float sumptx = 0;
        // float sumpty = 0;
        // float sumptz = 0;
        float sumeta = 0;
        float sumphi = 0;


        std::vector<std::set<int>> sv_bjetasso(3);
        std::vector<unsigned int> nbtrack = {0,0,0};

        for (int i =0; i < sv.ntracks(); ++i) {

          // std::cout << "track (i), pt, eta, phi : " << i << " " << sv.track_pt(i) << " " << sv.track_eta[i]<< " "  << sv.track_phi[i]<< " " << std::endl;
          sumpt += fabs(sv.track_pt(i));
          // sumptx += sv.track_px[i];
          // sumpty += sv.track_py[i];
          // sumptz += sv.track_pz[i];
          sumeta += sv.track_eta[i];
          sumphi += sv.track_phi[i];
          //     double nsigmadxybs = (sv.track_dxy[i] / sv.track_dxy_err(i));
          //     double nsigmadz = (sv.track_dz[i] / sv.track_dz_err(i) );

          //     // track information ??         
          //     // nt.trackmass.push_back(track_p4(i, mass));
          //     nt.trackpt.push_back(sv.track_pt(i));
          //     nt.trackpterr.push_back(sv.track_pt_err[i]);
          //     nt.tracketa.push_back(sv.track_eta[i]);
          //     nt.tracketaerr.push_back(sv.track_eta_err(i));
          //     nt.trackphi.push_back(sv.track_phi[i]);
          //     nt.trackphierr.push_back(sv.track_phi_err(i));
          //     nt.tracknsigmadxybs.push_back(nsigmadxybs);
          //     nt.trackdxy.push_back(sv.track_dxy[i]);
          //     nt.trackdxyerr.push_back(sv.track_dxy_err(i));
          //     nt.trackdz.push_back(sv.track_dz[i]);
          //     nt.trackdzerr.push_back(sv.track_dz_err(i));
          //     nt.tracknsigmadz.push_back(nsigmadz);
          //     //nt.trackabsnsigmadz.push_back(fabs(nsigmadz));
          //     nt.trackchi2ndof.push_back(sv.track_chi2dof(i));
          //     nt.track_injet.push_back(sv.track_injet[i]);

          //determine if any of the tracks is assocated to bjet 
          double match_threshold = 1.3;
          int jet_index = 255;
          for (unsigned j = 0; j < mevent->jet_track_which_jet.size(); ++j) {
            double a = fabs(sv.track_pt(i) - fabs(mevent->jet_track_qpt[j])) + 1;
            double b = fabs(sv.track_eta[i] - mevent->jet_track_eta[j]) + 1;
            double c = fabs(sv.track_phi[i] - mevent->jet_track_phi[j]) + 1;
            if (a * b * c < match_threshold) {
              match_threshold = a * b * c;
              jet_index = mevent->jet_track_which_jet[j];
            }
          }
          if (jet_index != 255) {
            for(int ibdisc=0; ibdisc<3; ++ibdisc){
              if (mevent->is_btagged(jet_index, ibdisc)){
                sv_bjetasso[ibdisc].insert((int) jet_index);
                ++nbtrack[ibdisc];
              }
            }
          }
        }
      
        //filling for bjets 
        nt.nbtags_loose.push_back(sv_bjetasso[0].size());
        nt.nbtks_loose.push_back(nbtrack[0]);
        nt.nbtags_med.push_back(sv_bjetasso[1].size());
        nt.nbtks_med.push_back(nbtrack[1]);
        nt.nbtags_tight.push_back(sv_bjetasso[2].size());
        nt.nbtks_tight.push_back(nbtrack[2]);

        nt.maxtrackpt.push_back(sv.maxtrackpt());
        nt.avgpt.push_back(sumpt/sv.ntracks());
        // nt.sumptx.push_back(sumptx);
        // nt.sumpty.push_back(sumpty);
        // nt.sumptz.push_back(sumptz);
        nt.tracketaavg.push_back(sumeta/sv.ntracks());
        nt.trackphiavg.push_back(sumphi/sv.ntracks());

        // nt.ntrackssharedwpv.push_back(sv.ntrackssharedwpv());
        // nt.ntrackssharedwpvs.push_back(sv.ntrackssharedwpvs());
        // nt.ntracksetagt1p5.push_back(sv.ntracksetagt(1.5));
        nt.sumpt2.push_back(sv.sumpt2());
        // nt.x.push_back(sv.x);
        // nt.y.push_back(sv.y);
        // nt.z.push_back(sv.z);
        nt.rescale_bs2derr.push_back(sv.rescale_bs2derr);
        nt.rescale_bs2ddist.push_back(sv.rescale_bs2ddist);
        nt.bs2derr.push_back(sv.bs2derr);
        // nt.bs2ddist.push_back(sv.bs2ddist);
        nt.bsbs2ddist.push_back(mevent->bs2ddist(sv));
        // nt.pvdz.push_back(sv.pvdz());
        // nt.pvdzerr.push_back(sv.pvdzerr());
        // nt.chi2.push_back(sv.chi2);
        // nt.ndof.push_back(sv.ndof());
        // nt.chi2dof.push_back(sv.chi2dof());
        nt.nele_inSV.push_back(sv.nelectrons);
        nt.nmu_inSV.push_back(sv.nmuons);
        nt.nlep_inSV.push_back(sv.nelectrons + sv.nmuons);

        //get the highest pt ele, highest pt mu, highest pt lep associated to SV 
        //initialize to -1 -> means there is no assoc lep 
        std::vector<float> assoc_ele {-1.0};
        std::vector<float> assoc_mu {-1.0};
        std::vector<float> assoc_lep {-1.0};
        std::vector<float> assoc_leptype{-1.0}; //0 == muon, 1 == electron
        std::vector<float> assoc_lepiso {-1.0};
        std::vector<float> assoc_lepID {-5.0};
        std::vector<float> assoc_lepnsigmadxy {-999.0};
        std::vector<float> assoc_lepnsigmadxy_rescaled {-999.0};
        std::vector<float> assoc_lepdxy {-999.0};
        std::vector<float> assoc_lepdxyerr{-999.0};
        std::vector<float> assoc_lepeta {-999.0};
        std::vector<float> assoc_lepphi {-999.0};
        std::vector<float> assoc_lephltmatch {-1.0};
        std::vector<float> assoc_leptrigpt { -1.0};
        int nselele = 0;
        for (int i =0; i < sv.nelectrons; ++i){

          //here need to apply HEM : figure out if electron is in eta/phi + above 30 GeV. 
          // in MC : randomly decide if to keep this electron 
          // in Data : starting w/ run number 319077 do not use this electron (this is genmatched so this is never the case)
          // if (year == 2018) { 
          //   if (hem_check > 0.352275515) {
          //     if (sv.electron_pt[i] > 30 && (-3.0 < sv.electron_eta[i]) && (sv.electron_eta[i] < -1.3) && (-1.57 < sv.electron_phi[i]) && (sv.electron_phi[i] < -0.87)) continue;
          //   }
          // }
        
          nt.all_elept_inSV.push_back(sv.electron_pt[i]);
          nt.all_leppt_inSV.push_back(sv.electron_pt[i]);
          assoc_ele.push_back(sv.electron_pt[i]);
          assoc_lep.push_back(sv.electron_pt[i]);
          assoc_leptype.push_back(1);
          assoc_lepiso.push_back(sv.electron_iso[i]);
          assoc_lepeta.push_back(sv.electron_eta[i]);
          assoc_lepphi.push_back(sv.electron_phi[i]);
          assoc_lephltmatch.push_back(sv.ele_is_hltmatched[i]);
          bool satisfies_leptrigpt = false;
          for(size_t trig : mfv::ElectronTriggers) { 
            satisfies_leptrigpt = satisfiesLepTriggerPT(mevent, sv, i, trig, setup);
            if (satisfies_leptrigpt) break; //if find a match, then break out of loop 
          }
          assoc_leptrigpt.push_back(satisfies_leptrigpt);

          auto temp = sv.electron_ID_noiso[i]; 
          int id = 0;
          if ( temp[0] == 0 ) id = 0; 
          if ( temp[0] == 1 ) id = 1;
          if ( temp[1] == 1 ) id = 2; 
          if ( temp[2] == 1 ) id = 3;
          if ( temp[3] == 1 ) id = 4;
          assoc_lepID.push_back(id);
          assoc_lepnsigmadxy_rescaled.push_back(fabs(sv.electron_dxybs[i])/sv.rescaled_electron_dxyerr[i]);
          assoc_lepnsigmadxy.push_back(fabs(sv.electron_dxybs[i])/sv.electron_dxyerr[i]);
          assoc_lepdxy.push_back(fabs(sv.electron_dxybs[i]));
          assoc_lepdxyerr.push_back(sv.rescaled_electron_dxyerr[i]); 
          
          if(sv.electron_iso[i] < 0.1 && id ==4) nselele +=1;
        } 

        int nselmu = 0;
        for (int i =0; i < sv.nmuons; ++i){
          nt.all_mupt_inSV.push_back(sv.muon_pt[i]);
          nt.all_leppt_inSV.push_back(sv.muon_pt[i]);
          assoc_mu.push_back(sv.muon_pt[i]);
          assoc_lep.push_back(sv.muon_pt[i]);
          assoc_leptype.push_back(0);
          assoc_lepiso.push_back(sv.muon_iso[i]);
          assoc_lepeta.push_back(sv.muon_eta[i]);
          assoc_lepphi.push_back(sv.muon_phi[i]);
          assoc_lephltmatch.push_back(sv.mu_is_hltmatched[i]);
          bool satisfies_leptrigpt = false;
          for(size_t trig : mfv::MuonTriggers) { 
            satisfies_leptrigpt = satisfiesLepTriggerPT(mevent, sv, i, trig, setup);
            if (satisfies_leptrigpt) break; //if find a match, then break out of loop 
          }
          assoc_leptrigpt.push_back(satisfies_leptrigpt);

          auto temp = sv.muon_ID[i]; 
          int id = 0;
          if ( temp[0] == 0 ) id = 0; 
          if ( temp[0] == 1 ) id = 1;
          if ( temp[1] == 1 ) id = 2; 
          if ( temp[2] == 1 ) id = 3;
          if ( temp[3] == 1 ) id = 4;
          assoc_lepID.push_back(id);
          assoc_lepnsigmadxy.push_back(fabs(sv.muon_dxybs[i])/sv.muon_dxyerr[i]);
          assoc_lepnsigmadxy_rescaled.push_back(fabs(sv.muon_dxybs[i])/sv.rescaled_muon_dxyerr[i]);
          assoc_lepdxy.push_back(fabs(sv.muon_dxybs[i]));
          assoc_lepdxyerr.push_back(sv.rescaled_muon_dxyerr[i]); 

          if (sv.muon_iso[i] < 0.1 && id > 1) nselmu +=1;
        } 

        nt.nselele_inSV.push_back(nselele);
        nt.nselmu_inSV.push_back(nselmu);
        
        float leading_leppt = *max_element(assoc_lep.begin(), assoc_lep.end());
        int leading_lepidx = std::max_element(assoc_lep.begin(), assoc_lep.end()) - assoc_lep.begin();
        nt.leading_leppt_inSV.push_back(leading_leppt);
        nt.leading_leptype_inSV.push_back(assoc_leptype[leading_lepidx]);
        nt.leading_lepiso_inSV.push_back(assoc_lepiso[leading_lepidx]);
        nt.leading_lepID_inSV.push_back(assoc_lepID[leading_lepidx]);
        nt.leading_lepnsigmadxy_inSV.push_back(assoc_lepnsigmadxy[leading_lepidx]);
        nt.leading_lepnsigmadxy_rescaled_inSV.push_back(assoc_lepnsigmadxy_rescaled[leading_lepidx]);
        nt.leading_lepdxy_inSV.push_back(assoc_lepdxy[leading_lepidx]);
        nt.leading_lepdxyerr_inSV.push_back(assoc_lepdxyerr[leading_lepidx]);
        nt.leading_lepeta_inSV.push_back(assoc_lepeta[leading_lepidx]);
        nt.leading_lepphi_inSV.push_back(assoc_lepphi[leading_lepidx]);
        nt.leading_lephltmatched_inSV.push_back(assoc_lephltmatch[leading_lepidx]);
        nt.leading_leppasstrigpt_inSV.push_back(assoc_leptrigpt[leading_lepidx]);

        float leading_elept = *max_element(assoc_ele.begin(), assoc_ele.end());
        nt.leading_elept_inSV.push_back(leading_elept);

        float leading_mupt = *max_element(assoc_mu.begin(), assoc_mu.end());
        nt.leading_mupt_inSV.push_back(leading_mupt);

        float nmleptracketaavg = 0;
        float nmleptrackphiavg = 0;
        if (assoc_lepeta[leading_lepidx] > 0) //if positive 
          nmleptracketaavg = (sumeta-assoc_lepeta[leading_lepidx])/(sv.ntracks()-1);
        else if (assoc_lepeta[leading_lepidx] < 0) //if negative 
          nmleptracketaavg = (sumeta+assoc_lepeta[leading_lepidx])/(sv.ntracks()-1);
        if (assoc_lepphi[leading_lepidx] > 0) //if positive 
          nmleptrackphiavg = (sumphi-assoc_lepphi[leading_lepidx])/(sv.ntracks()-1);
        else if (assoc_lepphi[leading_lepidx] < 0) //if negative 
          nmleptrackphiavg = (sumphi+assoc_lepphi[leading_lepidx])/(sv.ntracks()-1);
        
        nt.nmleptracketaavg.push_back(nmleptracketaavg);
        nt.nmleptrackphiavg.push_back(nmleptrackphiavg);
        nt.dr_avgtracks_lep.push_back(sqrt(pow(2, (assoc_lepeta[leading_lepidx]-nmleptracketaavg)) + pow(2, (assoc_lepphi[leading_lepidx]-nmleptrackphiavg))));

      //find the track pT "assoc" to the lepton; also determine costheta for : just the lepton, and all tracks except the lepton 
      // math::XYZTLorentzVector sumtk_p4;
      // math::XYZTLorentzVector tknolep_p4;
      // math::XYZTLorentzVector lep_p4;

      if (leading_leppt > 0){ 
        std::vector<double> mindR;
        for (int i = 0; i < sv.ntracks(); ++i) {
          // sumtk_p4 +=math::XYZTLorentzVector(sv.track_px[i], sv.track_py[i], sv.track_pz[i], sv.track_p(i));
          double dr = reco::deltaR(sv.track_eta[i], sv.track_phi[i], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
          mindR.push_back(dr);
        }
        nt.closestdR_track_leadinglep.push_back(*min_element(mindR.begin(), mindR.end()));
        int track_idx = std::min_element(mindR.begin(), mindR.end()) - mindR.begin();
        nt.avgptnolep.push_back((sumpt - sv.track_pt(track_idx))/(sv.ntracks()-1));

        // lep_p4 = math::XYZTLorentzVector(sv.track_px[track_idx], sv.track_py[track_idx], sv.track_pz[track_idx], sv.track_p(track_idx));
        // tknolep_p4 = sumtk_p4 - lep_p4;
        // nt.costhlepmombs.push_back(jmt::costh2(lep_p4, bs2sv));
        // nt.costhnolepmombs.push_back(jmt::costh2(tknolep_p4, bs2sv));
      }
      else if (leading_leppt < 0) {
        nt.closestdR_track_leadinglep.push_back(20);
        nt.avgptnolep.push_back(sumpt/(sv.ntracks()));
        // nt.costhlepmombs.push_back(-5.0);
        // nt.costhnolepmombs.push_back(jmt::costh2(sumtk_p4, bs2sv));
      }

        // now leading jet 
        std::vector<float> assoc_jet{-1.0};
        std::vector<float> assoc_jeteta{-999.0};
        std::vector<float> assoc_jetphi{-999.0};

        for (size_t ijet = 0; ijet < sv.njets[mfv::JByNtracks]; ++ijet) {
          assoc_jet.push_back(sv.jet_pt[mfv::JByNtracks][ijet]);
        }

        float leading_jetpt = *max_element(assoc_jet.begin(), assoc_jet.end());

        float minjetlepdR = 10.0;
        if (leading_leppt > 0) { 
          if (mevent->jet_id.size() != 0) {
            for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
              if (mevent->jet_pt[ijet] <  mfv::min_jet_pt) continue; 
              float jetlepdR = reco::deltaR(mevent->jet_eta[ijet], mevent->jet_phi[ijet], assoc_lepeta[leading_lepidx], assoc_lepphi[leading_lepidx]);
              if (jetlepdR < minjetlepdR) {
                minjetlepdR = jetlepdR;
              }
            }
          }
        }
        nt.leading_lepjet_pairdr.push_back(minjetlepdR);
        nt.leading_jetpt_inSV.push_back(leading_jetpt);
        
        std::pair<int, int> lep{-1, -1}; // {leading lep == idx0, subleading lep == idx1}  -1 == lepton not available (ie no ≥ 2 lep ≥ 50GeV). 0 == lepton not in SV. 1 == lepton in SV 
        TLorentzVector lep0_sv_p4;
        TLorentzVector lep1_sv_p4;
        TLorentzVector sv_p4;

        //first determine if lepton is in SV. : check the leading and subleading leptons to see if they are in the vertex 
        //{lep 0, idx 1, pt 2, phi 3,  eta 4, dxy 5, dxyerr 6, x 7, y 8} 
        int ilep = 0;
        for (const auto& p : leading_lep_tuple) {
          if (std::get<0>(p) == "electron") {
            ilep > 0 ? lep.second = 0 : lep.first = 0;
            for (int i=0; i < sv.nelectrons; ++i) {
              if (std::get<3>(p) == sv.electron_phi[i]) {
                if (std::get<4>(p) == sv.electron_eta[i]) {
                  ilep > 0 ? lep.second = 1 : lep.first = 1;
                }
              }
            }
          }
          if (std::get<0>(p) == "muon") {
            ilep > 0 ? lep.second = 0 : lep.first = 0;
            for (int i=0; i < sv.nmuons; ++i) {
              if (std::get<3>(p) == sv.muon_phi[i]) {
                if (std::get<4>(p) == sv.muon_eta[i]) {
                  ilep > 0 ? lep.second = 1 : lep.first = 1;
                }
              }
            }
          }
          ilep += 1;
        }
        //now to calculate the lepton-SV distance & lepton-SV deltaphi 
        // making sure the leading lep is not in SV
        float lep0_sv_2ddist = -999.0;
        float lep1_sv_2ddist = -999.0;
        float dphi0 = -999.0; //calcuation using p4 vector
        float dphi1 = -999.0; 
        float dphi0_2 = -999.0; // calculation using the arctan(SV-BS, lepton_phi)
        float dphi1_2 = -999.0; // calculation using the arctan(SV-BS, lepton_phi)

        //making sure leading lepton is not in SV 
        if (lep.first == 0) { 
          for (int i =0; i < sv.ntracks(); ++i) {
            TLorentzVector vt;
            vt.SetPtEtaPhiM(sv.track_pt(i), sv.track_eta[i], sv.track_phi[i], 0);
            lep0_sv_p4 += vt;
          }
          lep0_sv_2ddist = (mag( (sv.x - std::get<7>(leading_lep_tuple[0])), (sv.y - std::get<8>(leading_lep_tuple[0])) ));
          dphi0 = fabs(reco::deltaPhi( lep0_sv_p4.Phi(), std::get<3>(leading_lep_tuple[0])) );
          dphi0_2 = fabs(reco::deltaPhi(atan2(sv.y - mevent->bsy, sv.x - mevent->bsx), std::get<3>(leading_lep_tuple[0])));
        }
        //making sure the subleading lep is not in SV 
        if (lep.second == 0) {
          for (int i =0; i < sv.ntracks(); ++i) {
            TLorentzVector vt;
            vt.SetPtEtaPhiM(sv.track_pt(i), sv.track_eta[i], sv.track_phi[i], 0);
            lep1_sv_p4 += vt;
          }
          lep1_sv_2ddist = (mag( (sv.x - std::get<7>(leading_lep_tuple[1])), (sv.y - std::get<8>(leading_lep_tuple[1])) ));
          dphi1 = fabs(reco::deltaPhi( lep0_sv_p4.Phi(), std::get<3>(leading_lep_tuple[1])) );
          dphi1_2 = fabs(reco::deltaPhi(atan2(sv.y - mevent->bsy, sv.x - mevent->bsx), std::get<3>(leading_lep_tuple[1])));
        }

        //now that I have the distance and dphi between leading/subleading lep and sv, now decide which lep - sv pair to pick up 
        // ie largest lep-sv distance & lep-sv dphi. 
        // store in a vector 
        if (lep0_sv_2ddist > lep1_sv_2ddist ) lep_sv_2ddist.push_back(lep0_sv_2ddist);
        if (lep1_sv_2ddist > lep0_sv_2ddist ) lep_sv_2ddist.push_back(lep1_sv_2ddist);
        if ( (lep1_sv_2ddist == -999) && (lep0_sv_2ddist == -999.0 ) ) lep_sv_2ddist.push_back(-999.0); // just as placeholder? 
        if (dphi0 > dphi1) dphi.push_back(dphi0);
        if (dphi1 > dphi0) dphi.push_back(dphi1);
        if ( (dphi0 == -999) && (dphi1 == -999.0) ) dphi.push_back(-999.0); // placeholder ? 
        if (dphi0_2 > dphi1_2) dphi_2.push_back(dphi0_2);
        if (dphi1_2 > dphi0_2) dphi_2.push_back(dphi1_2);
        if ( (dphi0_2 == -999.0) && (dphi1_2 == -999.0) ) dphi_2.push_back(-999.0); // placeholder ? 
        
        //just also wanting the basic phi, eta variables of the SV (here we want all tracks because not comparing to lep)
        math::XYZTLorentzVector mom_p4;
        float sum_trackdxynsigma = 0;
        for (int i = 0; i < sv.ntracks(); ++i) {
          TLorentzVector vt;
          vt.SetPtEtaPhiM(sv.track_pt(i), sv.track_eta[i], sv.track_phi[i], 0);
          sv_p4 += vt;
          mom_p4 += math::XYZTLorentzVector(sv.track_px[i], sv.track_py[i], sv.track_pz[i], sv.track_p(i));
          sum_trackdxynsigma += sv.track_dxy_nsigma(i);
        }
        nt.sv_eta.push_back(sv_p4.Eta());
        nt.sv_phi.push_back(sv_p4.Phi());
        nt.costhmombs.push_back(jmt::costh2(mom_p4, bs2sv));
        //angle variables
        nt.trackpairdravg.push_back(sv.trackpairdravg());
        nt.trackpairdrmax.push_back(sv.trackpairdrmax());
        nt.trackpairdrmin.push_back(sv.trackpairdrmin());

        nt.trackpairdetaavg.push_back(sv.trackpairdetaavg());
        // nt.trackpairdetamin.push_back(sv.trackpairdetamin());
        // nt.trackpairdetamax.push_back(sv.trackpairdetamax());

        // nt.trackpairdphiavg.push_back(sv.trackpairdetaavg());
        // nt.trackpairdphimin.push_back(sv.trackpairdetamin());
        // nt.trackpairdphimax.push_back(sv.trackpairdetamax());

        //mass variables (tri -track because that's the min # of tracks required in vertex)
        // nt.tracktripmassavg.push_back(sv.tracktripmassavg());
        nt.tracktripmassmax.push_back(sv.tracktripmassmax());
        // nt.tracktripmassmin.push_back(sv.tracktripmassmin());
        nt.trackdxynsigmaavg.push_back(sv.trackdxynsigmaavg());
        nt.trackdxynsigmamax.push_back(sv.trackdxynsigmamax());

        nt.trackdxynsigmamin.push_back(sv.trackdxynsigmamin());
        nt.trackdxynsigmarms.push_back(sv.trackdxynsigmarms());

        // nt.sum_trackdxynsigma.push_back(sum_trackdxynsigma/sv.ntracks());
        
        // nt.costhmombs.push_back(sv.costhmombs_alltks());
        nt.costhtksjetsntkmombs.push_back(sv.costhmombs(mfv::PTracksPlusJetsByNtracks));
        // nt.costhtkmomvtxdispmin.push_back(sv.costhtkmomvtxdispmin()); 
        // nt.costhtkmomvtxdispmax.push_back(sv.costhtkmomvtxdispmax());
        // nt.costhtkmomvtxdispavg.push_back(sv.costhtkmomvtxdispavg());
        // nt.costhjetmomvtxdispmin.push_back(sv.costhjetmomvtxdispmin()); 
        // nt.costhjetmomvtxdispmax.push_back(sv.costhjetmomvtxdispmax());
        // nt.costhjetmomvtxdispavg.push_back(sv.costhjetmomvtxdispavg());

        //other variables (new set) 
        // nt.ntracksptgt10.push_back(sv.ntracksptgt(10));
        // nt.jetsntkpt.push_back(sv.pt[mfv::PJetsByNtracks]);
        // nt.tksjetsntkpt.push_back(sv.pt[mfv::PTracksPlusJetsByNtracks]);
        // nt.tksjetsntkmass.push_back(sv.mass[mfv::PTracksPlusJetsByNtracks]);

        //jet-SV deltaphi --> get the max? 
        std::vector<double> jetdeltaphis;
        for (size_t ijet = 0; ijet < mevent->jet_id.size(); ++ijet) {
          if (mevent->jet_pt[ijet] < mfv::min_jet_pt) continue;
          // if (((mevent->jet_id[ijet] >> 2) & 3) >= 0) {
          const double dphi = reco::deltaPhi(atan2(sv.y - mevent->bsy, sv.x - mevent->bsx), mevent->jet_phi[ijet]);
          nt.alljetsvdeltaphi.push_back(dphi);
          jetdeltaphis.push_back(fabs(dphi));
          // }
        }
        if (jetdeltaphis.size() != 0) {
          std::sort(jetdeltaphis.begin(), jetdeltaphis.end());
          nt.maxjetsvdeltaphi.push_back(jetdeltaphis.back());
          nt.minjetsvdeltaphi.push_back(jetdeltaphis[0]);
          nt.avgjetsvdeltaphi.push_back((jetdeltaphis.begin(), jetdeltaphis.end(),0) / jetdeltaphis.size());
        }
        if (jetdeltaphis.size() == 0) {
          nt.minjetsvdeltaphi.push_back(-999.0);
          nt.maxjetsvdeltaphi.push_back(-999.0);
          nt.avgjetsvdeltaphi.push_back(-999.0);
        }
      }
    }
  }
  //determine the max lep-sv pair now out of the sv0, sv1 ..
  if (lep_sv_2ddist.size() != 0) nt.max_lep_sv_2ddist = *std::max_element(lep_sv_2ddist.begin(), lep_sv_2ddist.end());
  if (dphi.size() != 0) nt.max_lep_sv_dphi = *std::max_element(dphi.begin(), dphi.end());
  if (dphi_2.size() != 0) nt.max_lep_sv_dphi_2 = *std::max_element(dphi_2.begin(), dphi_2.end());

  if (lep_sv_2ddist.size() == 0) nt.max_lep_sv_2ddist = -999.0;
  if (dphi.size() == 0)  nt.max_lep_sv_dphi = -999.0;
  if (dphi_2.size() == 0) nt.max_lep_sv_dphi_2 = -999.0;

  if (vertices.size() == 1) nt.nvtx = 1;
  else if (vertices.size() >= 2) nt.nvtx = int2uchar(int(vertices.size()));
  h_nsvsel->Fill(vertices.size());

  tree->Fill();  
}

DEFINE_FWK_MODULE(MFVMiniTreerBDT);
