import sys, os
from ROOT import TLegend
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
#from pprint import pprint

def stat_box(hist, movement=1, color_from_hist = True):
    s = hist.FindObject('stats')
    if not s:
        return
    if color_from_hist:
        new_color = hist.GetLineColor()

    if new_color is not None:
        s.SetTextColor(new_color)
        s.SetLineColor(new_color)

    if type(movement) == int:
        movement = (0,movement)
    m,n = movement
    
    x1,x2 = s.GetX1NDC(), s.GetX2NDC()
    y1,y2 = s.GetY1NDC(), s.GetY2NDC()


    s.SetX1NDC(x1 - (x2-x1)*m)
    s.SetX2NDC(x2 - (x2-x1)*m)
    s.SetY1NDC(y1 - (y2-y1)*n)
    s.SetY2NDC(y2 - (y2-y1)*n)

    return s

## compare two histograms in same directory in same file; repeat for a set of files
file_path = "/afs/hep.wisc.edu/home/acwarden/crabdirs/HistosV30Lepm_matchTrig_wfull/"
#dir_path = "mfvIsolationHistosPreSel/"

samples = ["mfv_stoplb_tau001000um_M0400_2018", "mfv_stoplb_tau001000um_M1400_2018", "mfv_stoplb_tau010000um_M0400_2018", "mfv_stoplb_tau010000um_M1400_2018", "ttbar_2018"]

# dxy_a = ["h_muon_had_iso_a", "h_muon_neutral_iso_a", "h_muon_photon_iso_a", "h_muon_corr_a", "h_electron_had_iso_a", "h_electron_neutral_iso_a", "h_electron_photon_iso_a", "h_electron_corr_a"]
# dxy_b = ["h_muon_had_iso_b", "h_muon_neutral_iso_b", "h_muon_photon_iso_b", "h_muon_corr_b", "h_electron_had_iso_b", "h_electron_neutral_iso_b", "h_electron_photon_iso_b", "h_electron_corr_b"]
# dxy_c = ["h_muon_had_iso_c", "h_muon_neutral_iso_c", "h_muon_photon_iso_c", "h_muon_corr_c", "h_electron_had_iso_c", "h_electron_neutral_iso_c", "h_electron_photon_iso_c", "h_electron_corr_c"]
# dxy_d = ["h_muon_had_iso_d", "h_muon_neutral_iso_d", "h_muon_photon_iso_d", "h_muon_corr_d", "h_electron_had_iso_d", "h_electron_neutral_iso_d", "h_electron_photon_iso_d", "h_electron_corr_d"]
# dxy_e = ["h_muon_had_iso_e", "h_muon_neutral_iso_e", "h_muon_photon_iso_e", "h_muon_corr_e", "h_electron_had_iso_e", "h_electron_neutral_iso_e", "h_electron_photon_iso_e", "h_electron_corr_e"]


# dxy_a = ["h_med_muon_had_iso_a", "h_med_muon_neutral_iso_a", "h_med_muon_photon_iso_a", "h_med_muon_corr_a", "h_tight_electron_had_iso_a", "h_tight_electron_neutral_iso_a", "h_tight_electron_photon_iso_a", "h_tight_electron_corr_a"]
# dxy_b = ["h_med_muon_had_iso_b", "h_med_muon_neutral_iso_b", "h_med_muon_photon_iso_b", "h_med_muon_corr_b", "h_tight_electron_had_iso_b", "h_tight_electron_neutral_iso_b", "h_tight_electron_photon_iso_b", "h_tight_electron_corr_b"]
# dxy_c = ["h_med_muon_had_iso_c", "h_med_muon_neutral_iso_c", "h_med_muon_photon_iso_c", "h_med_muon_corr_c", "h_tight_electron_had_iso_c", "h_tight_electron_neutral_iso_c", "h_tight_electron_photon_iso_c", "h_tight_electron_corr_c"]
# dxy_d = ["h_med_muon_had_iso_d", "h_med_muon_neutral_iso_d", "h_med_muon_photon_iso_d", "h_med_muon_corr_d", "h_tight_electron_had_iso_d", "h_tight_electron_neutral_iso_d", "h_tight_electron_photon_iso_d", "h_tight_electron_corr_d"]
# dxy_e = ["h_med_muon_had_iso_e", "h_med_muon_neutral_iso_e", "h_med_muon_photon_iso_e", "h_med_muon_corr_e", "h_tight_electron_had_iso_e", "h_tight_electron_neutral_iso_e", "h_tight_electron_photon_iso_e", "h_tight_electron_corr_e"]

#nice = ["muhadIso", "muneutIso", "muphoIso", "muCorr", "elehadIso", "eleneutIso", "elephoIso", "eleCorr"]


## just for ease of printing out 2d hists for a set of files
dir_path = "MinNtk4vtxHst1VNoBs2derr/"

histos = ["h_sv_all_bs2derr_pfmuiso", "h_sv_all_bs2derr_pfeliso", "h_sv_all_bs2derr_jetmu_deltaR", "h_sv_all_bs2derr_jetel_deltaR", "h_sv_all_bs2derr_nbjet"]
nice = ["2Dpfmuiso", "2Dpfeliso", "2DjetmudeltaR", "2DjeteldeltaR", "2Dnbjet"]

for sample in samples:
    fn = os.path.join(file_path, sample + '.root')
    if not os.path.exists(fn):
        raise ValueError("sample file %s not found" % sample)

    f = ROOT.TFile(fn)
    # for ah, bh, ch, dh, eh, name in zip(dxy_a, dxy_b, dxy_c, dxy_d, dxy_e, nice) :
    #     a_hist = f.Get(dir_path + ah)
    #     b_hist = f.Get(dir_path + bh)
    #     c_hist = f.Get(dir_path + ch)
    #     d_hist = f.Get(dir_path + dh)
    #     e_hist = f.Get(dir_path + eh)

    for h, name in zip(histos, nice) :
        hist = f.Get(dir_path + h)
        
        c = ROOT.TCanvas()
       ### c.SetLogy()
        ROOT.gStyle.SetOptStat(0)

        # a_hist.SetLineColor(ROOT.kRed)
        # a_hist.SetMarkerColor(ROOT.kRed)
        # b_hist.SetLineColor(ROOT.kBlue)
        # b_hist.SetMarkerColor(ROOT.kBlue)
        # c_hist.SetLineColor(ROOT.kGreen)
        # c_hist.SetMarkerColor(ROOT.kGreen)
        # d_hist.SetLineColor(ROOT.kOrange)
        # d_hist.SetMarkerColor(ROOT.kOrange)
        # e_hist.SetLineColor(ROOT.kMagenta)
        # e_hist.SetMarkerColor(ROOT.kMagenta)

        # a_hist.Scale(1./a_hist.Integral())
        # b_hist.Scale(1./b_hist.Integral())
        # c_hist.Scale(1./c_hist.Integral())
        # d_hist.Scale(1./d_hist.Integral())
        # e_hist.Scale(1./e_hist.Integral())
        
        
        hist.Draw('COLZ')
        # a_hist.Draw()
        # b_hist.Draw("sames")
        # c_hist.Draw("sames")
        # d_hist.Draw("sames")
        # e_hist.Draw("sames")

        # legend = TLegend(0.55, 0.65, 0.76, 0.82);
        # legend.AddEntry(a_hist, "|dxy| < 100um", "l");
        # legend.AddEntry(b_hist, "100 < |dxy| < 500um", "l");
        # legend.AddEntry(c_hist, "500 < |dxy| < 1000um", "l");
        # legend.AddEntry(d_hist, "1000 < |dxy| < 3000um", "l");
        # legend.AddEntry(e_hist, "3000um < |dxy|", "l");
        # legend.Draw();
        
        c.Update()

        c.Print("comparison_%s_%s.pdf" % (sample, name))


