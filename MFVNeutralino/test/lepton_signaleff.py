#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Sample
from JMTucker.Tools import Samples
#from JMTucker.MFVNeutralino.PerSignal import PerSignal
from ROOT import kBlue
from ROOT import TCanvas, SetOwnership, TH1F, TLegend, TEfficiency

def newCanvas():
    H_ref = 600;
    W_ref = 800;
    H  = H_ref
    W = W_ref

    # references for T, B, L, R
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref

    c = TCanvas("c","c",50,50,W,H)
    c.Clear()
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )

    SetOwnership(c, False)
    return c

def ANDtwo(cut1,cut2):
    """AND of two TCuts in PyROOT"""
    if cut1.GetTitle() == "":
        return cut2
    if cut2.GetTitle() == "":
        return cut1
    return TCut("(%s) && (%s)"%(cut1.GetTitle(),cut2.GetTitle()))


def AND(*arg):
    """AND of any number of TCuts in PyROOT"""
    length = len(arg)
    if length == 0:
        print("ERROR: invalid number of arguments")
        return
    if length == 1:
        return arg[0]
    if length==2:
        return ANDtwo(arg[0],arg[1])
    if length>2:
        result = arg[0]
        for i in range(1,len(arg)):
            result = ANDtwo(result,arg[i])
        return result


####################################################################################

# helper cuts ??


def draw_geff(t, title, h_bins, h_den, h_num,
              opt = "", color = kBlue, marker_st = 1, marker_sz = 1.):
    """Make an efficiency plot"""

    #num_cut = AND(den_cut,extra_num_cut)
    
    ## PyROOT works a little different than ROOT when you are plotting
    ## histograms directly from tree. Hence, this work-around
    nBins  = int(h_bins[1:-1].split(',')[0])
    minBin = float(h_bins[1:-1].split(',')[1])
    maxBin = float(h_bins[1:-1].split(',')[2])

    
    num = TH1F("num", "", nBins, minBin, maxBin)
    den = TH1F("den", "", nBins, minBin, maxBin)

    num_hist = t.Get(h_num)
    den_hist = t.Get(h_den)
    

    debug = True
    if debug:
        print("Denominator cut", h_den, den_hist.GetEntries())
        print("Numerator cut", h_num, num_hist.GetEntries())

    ## check if the number of passed entries larger than total entries
    doConsistencyCheck = False
    if doConsistencyCheck:
        for i in range(0,nBins):
            print(i, num_hist.GetBinContent(i), den_hist.GetBinContent(i))
            if num_hist.GetBinContent(i) > den_hist.GetBinContent(i):
                print(">>>Error: passed entries > total entries")

    eff = TEfficiency(num_hist, den_hist)

       ## plotting options
    if not "same" in opt:
        num.Reset()
        num.GetYaxis().SetRangeUser(0.0,1.1)
        num.SetStats(0)
        num.SetTitle(title)
        num.Draw()

    eff.SetLineWidth(2)
    eff.SetLineColor(color)
    eff.SetMarkerStyle(marker_st)
    eff.SetMarkerColor(color)
    eff.SetMarkerSize(marker_sz)
    eff.Draw(opt + " same")

    SetOwnership(eff, False)
    return eff

# def draw_1D(t, title, h_bins, to_draw, extra_cut, opt = "", color = kBlue, marker_st = 20):
    
#     nBins  = int(h_bins[1:-1].split(',')[0])
#     minBin = float(h_bins[1:-1].split(',')[1])
#     maxBin = float(h_bins[1:-1].split(',')[2])

#     num = TH1F("num", "", nBins, minBin, maxBin)

#     num_hist = t.Get(
    


##############################################################################################################################
version = 'V29Lepm_nodxycut'
#ps = plot_saver(plot_dir('lepton_sigeff_%s' % version), size=(600,600), pdf=True, log=False)

#multijet = Samples.mfv_signal_samples_2017
#dijet = Samples.mfv_stopdbardbar_samples_2017
stoplb = Samples.mfv_stoplb_samples_2018[:1]
#stopld = Samples.mfv_stopld_samples_2018

for sample in stoplb :
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version, sample.name + '.root')
    if not os.path.exists(fn) :
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvEventHistosPreSel')
   # print t
    # toPlot = "pt"
    num = 'h_electron_pt_tight'
    den = 'h_electron_pt'

    topTitle = ""
    xTitle = "electron p_{T} GeV"
   # xTitle = "electron abs(dxy) cm"
    yTitle = "Efficiency"
    title = "%s;%s;%s"%(topTitle,xTitle,yTitle)
    

    
   # h_bins = "(80, 0, 0.5)"
    h_bins = "(500, 0, 1000)"
    nBins = int(h_bins[1:-1].split(',')[0])
    minBin = float(h_bins[1:-1].split(',')[1])
    maxBin = float(h_bins[1:-1].split(',')[2])

    
    c = newCanvas()
    base  = TH1F("base",title,nBins,minBin,maxBin)
    base.SetMinimum(0.0)
    base.SetMaximum(1.1)
    base.GetXaxis().SetLabelSize(0.05)
    base.GetYaxis().SetLabelSize(0.05)
    base.GetXaxis().SetTitleSize(0.05)
    base.GetYaxis().SetTitleSize(0.05)
    base.Draw("")


    h2 = draw_geff(t, title, h_bins, den, num, "same", kBlue)

    leg = TLegend(0.45,0.2,.75,0.5, "", "brNDC")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextSize(0.05)
    leg.AddEntry(h2, "electron pt","pl")
    leg.Draw("same")


    c.Update()
    c.Print("lepton_sigeff_%s.pdf" % (num))

    del c, base, leg, h2
