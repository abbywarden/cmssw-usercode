#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "JMTucker/MFVNeutralino/interface/MiniNtupleBDT.h"
#include "JMTucker/MFVNeutralinoFormats/interface/TriggerEnum.h"
#include "JMTucker/Tools/interface/Year.h"

namespace mfv {
  MiniNtupleBDT::MiniNtupleBDT() {
    clear();
  }

  void MiniNtupleBDT::clear() {
    run = lumi = 0;
    event = 0;
    nvtx = 0;
    gen_flavor_code = pass_hlt = npv = npu = njets = nelectrons = nmuons = nleptons = 0;
    l1_htt = l1_myhtt = l1_myhttwbug = hlt_ht = bsx = bsy = bsz = bsdxdz = bsdydz = pvx = pvy = pvz = weight = 0;
    jet0_pt = jet1_pt = jetht = 0;
    leading_lep_pt = leading_lep_dxy = leading_lep_dxyerr = leading_lep_sigmadxy = leading_jetlep_pt = 0;
    subleading_lep_pt = subleading_lep_dxy = subleading_lep_dxyerr = subleading_lep_sigmadxy = double_jetlep_pt = 0;
    max_lep_sv_2ddist = max_lep_sv_dphi = max_lep_sv_dphi_2 = 0;

    nele_inSV.clear();
    nmu_inSV.clear();
    nlep_inSV.clear();
    nselele_inSV.clear();
    nselmu_inSV.clear();
    ntracks.clear();
    ntrackssharedwpv.clear();
    ntrackssharedwpvs.clear();
    ntracksetagt1p5.clear();
    all_elept_inSV.clear();
    all_mupt_inSV.clear();
    all_leppt_inSV.clear();
    leading_elept_inSV.clear();
    leading_mupt_inSV.clear();
    leading_leppt_inSV.clear();
    leading_leptype_inSV.clear();
    leading_lepiso_inSV.clear();
    leading_lepID_inSV.clear();
    leading_lepnsigmadxy_inSV.clear();
    leading_lepnsigmadxy_rescaled_inSV.clear();
    leading_lepdxy_inSV.clear();
    leading_lepdxyerr_inSV.clear();
    leading_lepeta_inSV.clear();
    leading_lepphi_inSV.clear();
    leading_lephltmatched_inSV.clear();
    leading_jetlep_pairdr.clear();
    leading_jetpt_inSV.clear();

    // nbtags[3].clear();
    // nbtks[3].clear();
    nbtags_loose.clear();
    nbtks_loose.clear();
    nbtags_med.clear();
    nbtks_med.clear();   
    nbtags_tight.clear();
    nbtks_tight.clear();  

    // max_lep_sv_2ddist.clear();
    // max_lep_sv_dphi.clear();
    // max_lep_sv_dphi_2.clear();

    x.clear();
    y.clear();
    z.clear();
    sv_eta.clear();
    sv_phi.clear();
    bs2derr.clear();
    bsbs2ddist.clear();
    rescale_bs2derr.clear();
    rescale_bs2ddist.clear();
    pvdz.clear();
    pvdzerr.clear();
    chi2.clear();
    ndof.clear();
    chi2dof.clear();
    maxtrackpt.clear();
    avgpt.clear();
    sumptx.clear();
    sumpty.clear();
    sumptz.clear();
    sumpt2.clear();
    tracketaavg.clear();
    trackphiavg.clear();
    nmleptracketaavg.clear();
    nmleptrackphiavg.clear();
    dr_avgtracks_lep.clear();
    
    trackptmin.clear();
    trackptmax.clear();
    trackptavg.clear();
    trackptrms.clear();
    trackpairdptmin.clear();
    trackpairdptmax.clear();
    trackpairdptavg.clear();
    trackpairdptrms.clear();

    trackpairdravg.clear();
    trackpairdrmax.clear();
    trackpairdrmin.clear();
    trackpairdetaavg.clear();
    trackpairdetamax.clear();
    trackpairdetamin.clear();
    // trackpairdphiavg.clear();
    trackpairdphimax.clear();
    trackpairdphimin.clear();
    tracktripmassavg.clear();
    tracktripmassmax.clear();
    tracktripmassmin.clear();
    trackdxynsigmaavg.clear();
    trackdxynsigmamax.clear();
    trackdxynsigmamin.clear();
    sum_trackdxynsigma.clear();

    ntracksptgt10.clear();
    // jetsntkpt.clear();
    // tksjetsntkpt.clear();
    tksjetsntkmass.clear();
    costhtkmomvtxdispmin.clear();
    costhtkmomvtxdispmax.clear();
    costhtkmomvtxdispavg.clear();
    costhjetmomvtxdispmin.clear();
    costhjetmomvtxdispmax.clear();
    costhjetmomvtxdispavg.clear();
    alljetsvdeltaphi.clear();
    minjetsvdeltaphi.clear();
    maxjetsvdeltaphi.clear();
    avgjetsvdeltaphi.clear();

    costhmombs.clear();
    costhtksjetsntkmombs.clear();

    for (int i = 0; i < 2; ++i)
      gen_x[i] = gen_y[i] = gen_z[i] = gen_lsp_pt[i] = gen_lsp_eta[i] = gen_lsp_phi[i] = gen_lsp_mass[i] = 0;
    gen_daughters.clear();
    gen_daughter_id.clear();
    gen_leptons.clear();
    for (int i = 0; i < 50; ++i) {
      jet_pt[i] = jet_eta[i] = jet_phi[i] = jet_energy[i] = 0;
    }
    for (int i = 0; i < 50; ++i) {
      electron_pt[i] = electron_eta[i] = electron_phi[i] = electron_sigmadxy[i] = 0;
    }
    for (int i = 0; i < 50; ++i) {
      muon_pt[i] = muon_eta[i] = muon_phi[i] = muon_sigmadxy[i] = 0;
    }
  }

  bool MiniNtupleBDT::satisfiesTrigger(size_t trig) const {
    return bool((pass_hlt >> trig) & 1);
  }

  void write_to_tree(TTree* tree, MiniNtupleBDT& nt) {
    tree->Branch("run", &nt.run);
    tree->Branch("lumi", &nt.lumi);
    tree->Branch("event", &nt.event);
    tree->Branch("gen_flavor_code", &nt.gen_flavor_code);
    tree->Branch("pass_hlt", &nt.pass_hlt);
    tree->Branch("l1_htt", &nt.l1_htt);
    tree->Branch("l1_myhtt", &nt.l1_myhtt);
    tree->Branch("l1_myhttwbug", &nt.l1_myhttwbug);
    tree->Branch("hlt_ht", &nt.hlt_ht);
    tree->Branch("bsx", &nt.bsx);
    tree->Branch("bsy", &nt.bsy);
    tree->Branch("bsz", &nt.bsz);
    tree->Branch("bsdxdz", &nt.bsdxdz);
    tree->Branch("bsdydz", &nt.bsdydz);
    tree->Branch("npv", &nt.npv);
    tree->Branch("pvx", &nt.pvx);
    tree->Branch("pvy", &nt.pvy);
    tree->Branch("pvz", &nt.pvz);
    tree->Branch("npu", &nt.npu);
    tree->Branch("weight", &nt.weight);
    tree->Branch("nvtx", &nt.nvtx);
    tree->Branch("njets", &nt.njets);
    tree->Branch("jet_pt", nt.jet_pt, "jet_pt[njets]/F");
    tree->Branch("jet_eta", nt.jet_eta, "jet_eta[njets]/F");
    tree->Branch("jet_phi", nt.jet_phi, "jet_phi[njets]/F");
    tree->Branch("jet_energy", nt.jet_energy, "jet_energy[njets]/F");
    tree->Branch("jetht", &nt.jetht);
    tree->Branch("jet0_pt", &nt.jet0_pt);
    tree->Branch("jet1_pt", &nt.jet1_pt);
    tree->Branch("nelectrons", &nt.nelectrons);
    tree->Branch("electron_pt",  nt.electron_pt,  "electron_pt[nelectrons]/F");
    tree->Branch("electron_eta", nt.electron_eta, "electron_eta[nelectrons]/F");
    tree->Branch("electron_phi", nt.electron_phi, "electron_phi[nelectrons]/F");
    tree->Branch("electron_sigmadxy", nt.electron_sigmadxy, "electron_sigmadxy[nelectrons]/F");
    tree->Branch("nmuons", &nt.nmuons);
    tree->Branch("muon_pt",  nt.muon_pt,  "muon_pt[nmuons]/F");
    tree->Branch("muon_eta", nt.muon_eta, "muon_eta[nmuons]/F");
    tree->Branch("muon_phi", nt.muon_phi, "muon_phi[nmuons]/F");
    tree->Branch("muon_sigmadxy", nt.muon_sigmadxy, "muon_sigmadxy[nmuons]/F");
    tree->Branch("nleptons", &nt.nleptons);

    tree->Branch("gen_x", nt.gen_x, "gen_x[2]/F");
    tree->Branch("gen_y", nt.gen_y, "gen_y[2]/F");
    tree->Branch("gen_z", nt.gen_z, "gen_z[2]/F");
    tree->Branch("gen_lsp_pt", nt.gen_lsp_pt, "gen_lsp_pt[2]/F");
    tree->Branch("gen_lsp_eta", nt.gen_lsp_eta, "gen_lsp_eta[2]/F");
    tree->Branch("gen_lsp_phi", nt.gen_lsp_phi, "gen_lsp_phi[2]/F");
    tree->Branch("gen_lsp_mass", nt.gen_lsp_mass, "gen_lsp_mass[2]/F");
    tree->Branch("gen_daughters", &nt.gen_daughters, 32000, 0);
    tree->Branch("gen_daughter_id", &nt.gen_daughter_id);
    tree->Branch("gen_leptons", &nt.gen_leptons, 32000, 0);
    tree->Branch("ntracks", &nt.ntracks);
    //tree->Branch("trackmass", &nt.trackmass);
    // tree->Branch("trackpt", &nt.trackpt);
    // tree->Branch("trackpterr", &nt.trackpterr);
    // tree->Branch("tracketa", &nt.tracketa);
    // tree->Branch("tracketaerr", &nt.tracketaerr);
    // tree->Branch("trackphi", &nt.trackphi);
    // tree->Branch("trackphierr", &nt.trackphierr);
    // tree->Branch("trackdxy", &nt.trackdxy);
    // tree->Branch("trackdxyerr", &nt.trackdxyerr);
    // tree->Branch("tracknsigmadxybs", &nt.tracknsigmadxybs);
    // // tree->Branch("trackabsdz", &nt.trackabsdz);
    // tree->Branch("trackdz", &nt.trackdz);
    // tree->Branch("trackdzerr", &nt.trackdzerr);
    // tree->Branch("tracknsigmadz", &nt.tracknsigmadz);
    // tree->Branch("trackchi2ndof", &nt.trackchi2ndof);

    tree->Branch("ntrackssharedwpv", &nt.ntrackssharedwpv);
    tree->Branch("ntrackssharedwpvs", &nt.ntrackssharedwpvs);
    tree->Branch("ntracksetagt1p5", &nt.ntracksetagt1p5);
    tree->Branch("maxtrackpt", &nt.maxtrackpt);
    tree->Branch("avgpt", &nt.avgpt);
    tree->Branch("sumptx", &nt.sumptx);
    tree->Branch("sumpty", &nt.sumpty);
    tree->Branch("sumptz", &nt.sumptz);
    tree->Branch("sumpt2", &nt.sumpt2);
    tree->Branch("nele_inSV", &nt.nele_inSV);
    tree->Branch("nmu_inSV", &nt.nmu_inSV);
    tree->Branch("nlep_inSV", &nt.nlep_inSV);
    tree->Branch("nselele_inSV", &nt.nselele_inSV);
    tree->Branch("nselmu_inSV", &nt.nselmu_inSV);
    tree->Branch("all_elept_inSV", &nt.all_elept_inSV);
    tree->Branch("all_mupt_inSV", &nt.all_mupt_inSV);
    tree->Branch("all_leppt_inSV", &nt.all_leppt_inSV);
    tree->Branch("leading_elept_inSV", &nt.leading_elept_inSV);
    tree->Branch("leading_mupt_inSV", &nt.leading_mupt_inSV);
    tree->Branch("leading_leppt_inSV", &nt.leading_leppt_inSV);
    tree->Branch("leading_leptype_inSV", &nt.leading_leptype_inSV);
    tree->Branch("leading_lepiso_inSV", &nt.leading_lepiso_inSV);
    tree->Branch("leading_lepID_inSV", &nt.leading_lepID_inSV);
    tree->Branch("leading_lepnsigmadxy_inSV", &nt.leading_lepnsigmadxy_inSV);
    tree->Branch("leading_lepnsigmadxy_rescaled_inSV", &nt.leading_lepnsigmadxy_rescaled_inSV);
    tree->Branch("leading_lepdxy_inSV", &nt.leading_lepdxy_inSV);
    tree->Branch("leading_lepdxyerr_inSV", &nt.leading_lepdxyerr_inSV);
    tree->Branch("leading_lepeta_inSV", &nt.leading_lepeta_inSV);
    tree->Branch("leading_lepphi_inSV", &nt.leading_lepphi_inSV);
    tree->Branch("leading_lephltmatched_inSV", &nt.leading_lephltmatched_inSV);
    tree->Branch("leading_jetlep_pairdr", &nt.leading_jetlep_pairdr);
    tree->Branch("leading_jetpt_inSV", &nt.leading_jetpt_inSV);
    tree->Branch("nbtags_loose", &nt.nbtags_loose);
    tree->Branch("nbtags_med", &nt.nbtags_med);
    tree->Branch("nbtags_tight", &nt.nbtags_tight);
    tree->Branch("nbtks_loose", &nt.nbtks_loose);
    tree->Branch("nbtks_med", &nt.nbtks_med);
    tree->Branch("nbtks_tight", &nt.nbtks_tight);

    tree->Branch("max_lep_sv_2ddist", &nt.max_lep_sv_2ddist);
    tree->Branch("max_lep_sv_dphi", &nt.max_lep_sv_dphi);
    tree->Branch("max_lep_sv_dphi_2", &nt.max_lep_sv_dphi_2);
    tree->Branch("leading_lep_pt", &nt.leading_lep_pt);
    tree->Branch("leading_lep_dxy", &nt.leading_lep_dxy);
    tree->Branch("leading_lep_dxyerr", &nt.leading_lep_dxyerr);
    tree->Branch("leading_lep_sigmadxy", &nt.leading_lep_sigmadxy);
    tree->Branch("leading_jetlep_pt", &nt.leading_jetlep_pt);
    tree->Branch("subleading_lep_pt", &nt.subleading_lep_pt);
    tree->Branch("subleading_lep_dxy", &nt.subleading_lep_dxy);
    tree->Branch("subleading_lep_dxyerr", &nt.subleading_lep_dxyerr);
    tree->Branch("subleading_lep_sigmadxy", &nt.subleading_lep_sigmadxy);
    tree->Branch("double_jetlep_pt", &nt.double_jetlep_pt);

    tree->Branch("x", &nt.x);
    tree->Branch("y", &nt.y);
    tree->Branch("z", &nt.z);
    tree->Branch("sv_eta", &nt.sv_eta);
    tree->Branch("sv_phi", &nt.sv_phi);
    tree->Branch("bs2derr", &nt.bs2derr);
    tree->Branch("bsbs2ddist", &nt.bsbs2ddist);
    tree->Branch("rescale_bs2derr", &nt.rescale_bs2derr);
    tree->Branch("rescale_bs2ddist", &nt.rescale_bs2ddist);
    tree->Branch("pvdz", &nt.pvdz);
    tree->Branch("pvdzerr", &nt.pvdzerr);
    tree->Branch("chi2", &nt.chi2);
    tree->Branch("ndof", &nt.ndof);
    tree->Branch("chi2dof", &nt.chi2dof);
    tree->Branch("tracketaavg", &nt.tracketaavg);
    tree->Branch("trackphiavg", &nt.trackphiavg);
    tree->Branch("nmleptracketaavg", &nt.nmleptracketaavg);
    tree->Branch("nmleptrackphiavg", &nt.nmleptrackphiavg);
    tree->Branch("dr_avgtracks_lep", &nt.dr_avgtracks_lep);

    tree->Branch("trackptmin", &nt.trackptmin);
    tree->Branch("trackptmax", &nt.trackptmax);
    tree->Branch("trackptavg", &nt.trackptavg);
    tree->Branch("trackptrms", &nt.trackptrms);
    tree->Branch("trackpairdptmin", &nt.trackpairdptmin);
    tree->Branch("trackpairdptmax", &nt.trackpairdptmax);
    tree->Branch("trackpairdptavg", &nt.trackpairdptavg);
    tree->Branch("trackpairdptrms", &nt.trackpairdptrms);

    tree->Branch("trackpairdravg", &nt.trackpairdravg);
    tree->Branch("trackpairdrmax", &nt.trackpairdrmax);
    tree->Branch("trackpairdrmin", &nt.trackpairdrmin);
    tree->Branch("trackpairdetaavg", &nt.trackpairdetaavg);
    tree->Branch("trackpairdetamax", &nt.trackpairdetamax);
    tree->Branch("trackpairdetamin", &nt.trackpairdetamin);
    // tree->Branch("trackpairdphiavg", &nt.trackpairdphiavg);
    tree->Branch("trackpairdphimax", &nt.trackpairdphimax);
    tree->Branch("trackpairdphimin", &nt.trackpairdphimin);
    tree->Branch("tracktripmassavg", &nt.tracktripmassavg);
    tree->Branch("tracktripmassmax", &nt.tracktripmassmax);
    tree->Branch("tracktripmassmin", &nt.tracktripmassmin);
    tree->Branch("trackdxynsigmaavg", &nt.trackdxynsigmaavg);
    tree->Branch("trackdxynsigmamax", &nt.trackdxynsigmamax);
    tree->Branch("trackdxynsigmamin", &nt.trackdxynsigmamin);
    tree->Branch("sum_trackdxynsigma", &nt.sum_trackdxynsigma);
    tree->Branch("costhmombs", &nt.costhmombs);
    tree->Branch("costhtksjetsntkmombs", &nt.costhtksjetsntkmombs);

    tree->Branch("ntracksptgt10", &nt.ntracksptgt10);
    // tree->Branch("jetsntkpt", &nt.jetsntkpt);
    // tree->Branch("tksjetsntkpt", &nt.tksjetsntkpt);
    tree->Branch("tksjetsntkmass", &nt.tksjetsntkmass);
    tree->Branch("costhtkmomvtxdispmin", &nt.costhtkmomvtxdispmin);
    tree->Branch("costhtkmomvtxdispmax", &nt.costhtkmomvtxdispmax);
    tree->Branch("costhtkmomvtxdispavg", &nt.costhtkmomvtxdispavg);
    tree->Branch("costhjetmomvtxdispmin", &nt.costhjetmomvtxdispmin);
    tree->Branch("costhjetmomvtxdispmax", &nt.costhjetmomvtxdispmax);
    tree->Branch("costhjetmomvtxdispavg", &nt.costhjetmomvtxdispavg);
    tree->Branch("alljetsvdeltaphi", &nt.alljetsvdeltaphi);
    tree->Branch("minjetsvdeltaphi", &nt.minjetsvdeltaphi);
    tree->Branch("maxjetsvdeltaphi", &nt.maxjetsvdeltaphi);
    tree->Branch("avgjetsvdeltaphi", &nt.avgjetsvdeltaphi);


  }

  void read_from_tree(TTree* tree, MiniNtupleBDT& nt) {
    tree->SetBranchAddress("run", &nt.run);
    tree->SetBranchAddress("lumi", &nt.lumi);
    tree->SetBranchAddress("event", &nt.event);
    tree->SetBranchAddress("gen_flavor_code", &nt.gen_flavor_code);
    tree->SetBranchAddress("pass_hlt", &nt.pass_hlt);
    tree->SetBranchAddress("l1_htt", &nt.l1_htt);
    tree->SetBranchAddress("l1_myhtt", &nt.l1_myhtt);
    tree->SetBranchAddress("l1_myhttwbug", &nt.l1_myhttwbug);
    tree->SetBranchAddress("hlt_ht", &nt.hlt_ht);
    tree->SetBranchAddress("bsx", &nt.bsx);
    tree->SetBranchAddress("bsy", &nt.bsy);
    tree->SetBranchAddress("bsz", &nt.bsz);
    tree->SetBranchAddress("bsdxdz", &nt.bsdxdz);
    tree->SetBranchAddress("bsdydz", &nt.bsdydz);
    tree->SetBranchAddress("npv", &nt.npv);
    tree->SetBranchAddress("pvx", &nt.pvx);
    tree->SetBranchAddress("pvy", &nt.pvy);
    tree->SetBranchAddress("pvz", &nt.pvz);
    tree->SetBranchAddress("npu", &nt.npu);
    tree->SetBranchAddress("weight", &nt.weight);
    tree->SetBranchAddress("nvtx", &nt.nvtx);
    tree->SetBranchAddress("njets", &nt.njets);
    tree->SetBranchAddress("jet_pt", nt.jet_pt);
    tree->SetBranchAddress("jet_eta", nt.jet_eta);
    tree->SetBranchAddress("jet_phi", nt.jet_phi);
    tree->SetBranchAddress("jet_energy", nt.jet_energy);
    tree->SetBranchAddress("jetht", &nt.jetht);
    tree->SetBranchAddress("jet0_pt", &nt.jet0_pt);
    tree->SetBranchAddress("jet1_pt", &nt.jet1_pt);
    tree->SetBranchAddress("nelectrons", &nt.nelectrons);
    tree->SetBranchAddress("electron_pt", nt.electron_pt);
    tree->SetBranchAddress("electron_eta", nt.electron_eta);
    tree->SetBranchAddress("electron_phi", nt.electron_phi);
    tree->SetBranchAddress("electron_sigmadxy", nt.electron_sigmadxy);
    tree->SetBranchAddress("nmuons", &nt.nmuons);
    tree->SetBranchAddress("muon_pt", nt.muon_pt);
    tree->SetBranchAddress("muon_eta", nt.muon_eta);
    tree->SetBranchAddress("muon_phi", nt.muon_phi);
    tree->SetBranchAddress("muon_sigmadxy", nt.muon_sigmadxy);
    tree->SetBranchAddress("nleptons", &nt.nleptons);

    tree->SetBranchAddress("gen_x", nt.gen_x);
    tree->SetBranchAddress("gen_y", nt.gen_y);
    tree->SetBranchAddress("gen_z", nt.gen_z);
    tree->SetBranchAddress("gen_lsp_pt", nt.gen_lsp_pt);
    tree->SetBranchAddress("gen_lsp_eta", nt.gen_lsp_eta);
    tree->SetBranchAddress("gen_lsp_phi", nt.gen_lsp_phi);
    tree->SetBranchAddress("gen_lsp_mass", nt.gen_lsp_mass);
    tree->SetBranchAddress("gen_daughters", &nt.p_gen_daughters);
    tree->SetBranchAddress("gen_daughter_id", &nt.p_gen_daughter_id);
    tree->SetBranchAddress("gen_leptons", &nt.p_gen_leptons);
    tree->SetBranchAddress("ntracks", &nt.ntracks);
    // // tree->SetBranchAddress("trackmass", &nt.trackmass);
    // tree->SetBranchAddress("trackpt", &nt.trackpt);
    // tree->SetBranchAddress("trackpterr", &nt.trackpterr);
    // tree->SetBranchAddress("tracketa", &nt.tracketa);
    // tree->SetBranchAddress("tracketaerr", &nt.tracketaerr);
    // tree->SetBranchAddress("trackphi", &nt.trackphi);
    // tree->SetBranchAddress("trackphierr", &nt.trackphierr);
    // tree->SetBranchAddress("trackdxy", &nt.trackdxy);
    // tree->SetBranchAddress("trackdxyerr", &nt.trackdxyerr);
    // tree->SetBranchAddress("tracknsigmadxybs", &nt.tracknsigmadxybs);
    // tree->SetBranchAddress("trackdz", &nt.trackdz);
    // tree->SetBranchAddress("trackdzerr", &nt.trackdzerr);
    // tree->SetBranchAddress("tracknsigmadz", &nt.tracknsigmadz);
    // tree->SetBranchAddress("trackchi2ndof", &nt.trackchi2ndof);
    tree->SetBranchAddress("ntrackssharedwpv", & nt.ntrackssharedwpv);
    tree->SetBranchAddress("ntrackssharedwpvs", & nt.ntrackssharedwpvs);
    tree->SetBranchAddress("ntracksetagt1p5", & nt.ntracksetagt1p5);
    tree->SetBranchAddress("maxtrackpt", &nt.maxtrackpt);
    tree->SetBranchAddress("avgpt", &nt.avgpt);
    tree->SetBranchAddress("sumptx", &nt.sumptx);
    tree->SetBranchAddress("sumpty", &nt.sumpty);
    tree->SetBranchAddress("sumptz", &nt.sumptz);
    tree->SetBranchAddress("sumpt2", &nt.sumpt2);
    tree->SetBranchAddress("nele_inSV", &nt.nele_inSV);
    tree->SetBranchAddress("nmu_inSV", &nt.nmu_inSV);
    tree->SetBranchAddress("nselele_inSV", &nt.nselele_inSV);
    tree->SetBranchAddress("nselmu_inSV", &nt.nselmu_inSV);
    tree->SetBranchAddress("nlep_inSV", &nt.nlep_inSV);
    tree->SetBranchAddress("all_elept_inSV", &nt.all_elept_inSV);
    tree->SetBranchAddress("all_mupt_inSV", &nt.all_mupt_inSV);
    tree->SetBranchAddress("all_leppt_inSV", &nt.all_leppt_inSV);
    tree->SetBranchAddress("leading_elept_inSV", &nt.leading_elept_inSV);
    tree->SetBranchAddress("leading_mupt_inSV", &nt.leading_mupt_inSV);
    tree->SetBranchAddress("leading_leppt_inSV", &nt.leading_leppt_inSV);
    tree->SetBranchAddress("leading_leptype_inSV", &nt.leading_leptype_inSV);
    tree->SetBranchAddress("leading_lepiso_inSV", &nt.leading_lepiso_inSV);
    tree->SetBranchAddress("leading_lepID_inSV", &nt.leading_lepID_inSV);
    tree->SetBranchAddress("leading_lepnsigmadxy_inSV", &nt.leading_lepnsigmadxy_inSV);
    tree->SetBranchAddress("leading_lepnsigmadxy_rescaled_inSV", &nt.leading_lepnsigmadxy_rescaled_inSV);
    tree->SetBranchAddress("leading_lepdxy_inSV", &nt.leading_lepdxy_inSV);
    tree->SetBranchAddress("leading_lepdxyerr_inSV", &nt.leading_lepdxyerr_inSV);
    tree->SetBranchAddress("leading_lepeta_inSV", &nt.leading_lepeta_inSV);
    tree->SetBranchAddress("leading_lepphi_inSV", &nt.leading_lepphi_inSV);
    tree->SetBranchAddress("leading_lephltmatched_inSV", &nt.leading_lephltmatched_inSV);
    tree->SetBranchAddress("leading_jetlep_pairdr", &nt.leading_jetlep_pairdr);
    tree->SetBranchAddress("leading_jetpt_inSV", &nt.leading_jetpt_inSV);
    tree->SetBranchAddress("nbtags_loose", &nt.nbtags_loose);
    tree->SetBranchAddress("nbtags_med", &nt.nbtags_med);
    tree->SetBranchAddress("nbtags_tight", &nt.nbtags_tight);
    tree->SetBranchAddress("nbtks_loose", &nt.nbtks_loose);
    tree->SetBranchAddress("nbtks_med", &nt.nbtks_med);
    tree->SetBranchAddress("nbtks_tight", &nt.nbtks_tight);

    tree->SetBranchAddress("max_lep_sv_2ddist", &nt.max_lep_sv_2ddist);
    tree->SetBranchAddress("max_lep_sv_dphi", &nt.max_lep_sv_dphi);
    tree->SetBranchAddress("max_lep_sv_dphi_2", &nt.max_lep_sv_dphi_2);
    tree->SetBranchAddress("leading_lep_pt", &nt.leading_lep_pt);
    tree->SetBranchAddress("leading_lep_dxy", &nt.leading_lep_dxy);
    tree->SetBranchAddress("leading_lep_dxyerr", &nt.leading_lep_dxyerr);
    tree->SetBranchAddress("leading_lep_sigmadxy", &nt.leading_lep_sigmadxy);
    tree->SetBranchAddress("leading_jetlep_pt", &nt.leading_jetlep_pt);
    tree->SetBranchAddress("subleading_lep_pt", &nt.subleading_lep_pt);
    tree->SetBranchAddress("subleading_lep_dxy", &nt.subleading_lep_dxy);
    tree->SetBranchAddress("subleading_lep_dxyerr", &nt.subleading_lep_dxyerr);
    tree->SetBranchAddress("subleading_lep_sigmadxy", &nt.subleading_lep_sigmadxy);
    tree->SetBranchAddress("double_jetlep_pt", &nt.double_jetlep_pt);

    tree->SetBranchAddress("x", &nt.x);
    tree->SetBranchAddress("y", &nt.y);
    tree->SetBranchAddress("z", &nt.z);
    tree->SetBranchAddress("sv_eta", &nt.sv_eta);
    tree->SetBranchAddress("sv_phi", &nt.sv_phi);
    tree->SetBranchAddress("bs2derr", &nt.bs2derr);
    tree->SetBranchAddress("bsbs2ddist", &nt.bsbs2ddist);
    tree->SetBranchAddress("rescale_bs2derr", &nt.rescale_bs2derr);
    tree->SetBranchAddress("rescale_bs2ddist", &nt.rescale_bs2ddist);
    tree->SetBranchAddress("pvdz", &nt.pvdz);
    tree->SetBranchAddress("pvdzerr", &nt.pvdzerr);
    tree->SetBranchAddress("chi2", &nt.chi2);
    tree->SetBranchAddress("ndof", &nt.ndof);
    tree->SetBranchAddress("chi2dof", &nt.chi2dof);
    tree->SetBranchAddress("tracketaavg", &nt.tracketaavg);
    tree->SetBranchAddress("trackphiavg", &nt.trackphiavg);
    tree->SetBranchAddress("nmleptracketaavg", &nt.nmleptracketaavg);
    tree->SetBranchAddress("nmleptrackphiavg", &nt.nmleptrackphiavg);
    tree->SetBranchAddress("dr_avgtracks_lep", &nt.dr_avgtracks_lep);

    tree->SetBranchAddress("trackptmin", &nt.trackptmin);
    tree->SetBranchAddress("trackptmax", &nt.trackptmax);
    tree->SetBranchAddress("trackptavg", &nt.trackptavg);
    tree->SetBranchAddress("trackptrms", &nt.trackptrms);
    tree->SetBranchAddress("trackpairdptmin", &nt.trackpairdptmin);
    tree->SetBranchAddress("trackpairdptmax", &nt.trackpairdptmax);
    tree->SetBranchAddress("trackpairdptavg", &nt.trackpairdptavg);
    tree->SetBranchAddress("trackpairdptrms", &nt.trackpairdptrms);

    tree->SetBranchAddress("trackpairdravg", &nt.trackpairdravg);
    tree->SetBranchAddress("trackpairdrmax", &nt.trackpairdrmax);
    tree->SetBranchAddress("trackpairdrmin", &nt.trackpairdrmin);
    tree->SetBranchAddress("trackpairdetaavg", &nt.trackpairdetaavg);
    tree->SetBranchAddress("trackpairdetamax", &nt.trackpairdetamax);
    tree->SetBranchAddress("trackpairdetamin", &nt.trackpairdetamin);
    // tree->SetBranchAddress("trackpairdphiavg", &nt.trackpairdphiavg);
    tree->SetBranchAddress("trackpairdphimax", &nt.trackpairdphimax);
    tree->SetBranchAddress("trackpairdphimin", &nt.trackpairdphimin);
    tree->SetBranchAddress("tracktripmassavg", &nt.tracktripmassavg);
    tree->SetBranchAddress("tracktripmassmax", &nt.tracktripmassmax);
    tree->SetBranchAddress("tracktripmassmin", &nt.tracktripmassmin);
    tree->SetBranchAddress("trackdxynsigmaavg", &nt.trackdxynsigmaavg);
    tree->SetBranchAddress("trackdxynsigmamax", &nt.trackdxynsigmamax);
    tree->SetBranchAddress("trackdxynsigmamin", &nt.trackdxynsigmamin);
    tree->SetBranchAddress("sum_trackdxynsigma", &nt.sum_trackdxynsigma);
    tree->SetBranchAddress("costhmombs", &nt.costhmombs);
    tree->SetBranchAddress("costhtksjetsntkmombs", &nt.costhtksjetsntkmombs);
    tree->SetBranchAddress("ntracksptgt10", &nt.ntracksptgt10);
    // tree->SetBranchAddress("jetsntkpt", &nt.jetsntkpt);
    // tree->SetBranchAddress("tksjetsntkpt", &nt.tksjetsntkpt);
    tree->SetBranchAddress("tksjetsntkmass", &nt.tksjetsntkmass);
    tree->SetBranchAddress("costhtkmomvtxdispmin", &nt.costhtkmomvtxdispmin);
    tree->SetBranchAddress("costhtkmomvtxdispmax", &nt.costhtkmomvtxdispmax);
    tree->SetBranchAddress("costhtkmomvtxdispavg", &nt.costhtkmomvtxdispavg);
    tree->SetBranchAddress("costhjetmomvtxdispmin", &nt.costhjetmomvtxdispmin);
    tree->SetBranchAddress("costhjetmomvtxdispmax", &nt.costhjetmomvtxdispmax);
    tree->SetBranchAddress("costhjetmomvtxdispavg", &nt.costhjetmomvtxdispavg);
    tree->SetBranchAddress("alljetsvdeltaphi", &nt.alljetsvdeltaphi);
    tree->SetBranchAddress("minjetsvdeltaphi", &nt.minjetsvdeltaphi);
    tree->SetBranchAddress("maxjetsvdeltaphi", &nt.maxjetsvdeltaphi);
    tree->SetBranchAddress("avgjetsvdeltaphi", &nt.avgjetsvdeltaphi);


  }

 MiniNtupleBDT* clone(const MiniNtupleBDT& nt) {
    MiniNtupleBDT* nnt = new MiniNtupleBDT(nt);

    if (nt.p_gen_daughters) nnt->gen_daughters = *nt.p_gen_daughters;
    if (nt.p_gen_daughter_id) nnt->gen_daughter_id = *nt.p_gen_daughter_id;
    if (nt.p_gen_leptons) nnt->gen_leptons = *nt.p_gen_leptons;

    nnt->p_gen_daughters = nnt->p_gen_leptons = 0;
    nnt->p_gen_daughter_id = 0;

    return nnt;
  }



  long long loop(const char* fn, const char* tree_path, bool (*fcn)(long long, long long, const mfv::MiniNtupleBDT&)) {
    TFile* f = TFile::Open(fn);
    assert(f);

    // Set the year for the proper btagging WPs
    int year = 0;
    TH1F* h_sums = (TH1F*) f->Get("mfvWeight/h_sums");
    assert(h_sums);

    for(int ibin = 1; ibin < h_sums->GetNbinsX()+1; ++ibin){
      const std::string bin_label = h_sums->GetXaxis()->GetBinLabel(ibin);
      if(bin_label == "yearcode_x_nfiles"){
        const double yearcode_val = h_sums->GetBinContent(ibin);
        year = jmt::yearcode(yearcode_val).year();
      }
    }
    assert(year > 0);
    jmt::Year::set(year);

    TTree* tree = (TTree*)f->Get(tree_path);
    assert(tree);

    mfv::MiniNtupleBDT nt;
    mfv::read_from_tree(tree, nt);

    long long j = 0, je = tree->GetEntriesFast();
    for (; j < je; ++j) {
      if (tree->LoadTree(j) < 0) break;
      if (tree->GetEntry(j) <= 0) continue;
      if (!fcn(j, je, nt)) break;
    }

    f->Close();
    delete f;

    return j;
  }
}