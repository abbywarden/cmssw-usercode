#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Sample
from JMTucker.Tools import Samples
from ROOT import TEfficiency, TCanvas, SetOwnership, TH1F, TLegend
#from JMTucker.MFVNeutralino.PerSignal import PerSignal

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

set_style()
version = 'V29Lepm_nodxycut'
ps = plot_saver(plot_dir('leptsigeff_%s' % version), size=(600,600), pdf=True, log=False)

stoplb = Samples.mfv_stoplb_samples_2018[:1]
#stopld = Samples.mfv_stopld_samples_2018

for sample in stoplb : # + stopld:
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    num = f.Get('mfvEventHistosPreSel/h_electron_pt_tight')
    den = f.Get('mfvEventHistosPreSel/h_electron_pt')

    c = newCanvas()
    
   # hr_num = draw_hist_register(num, True)
   # hr_den = draw_hist_register(den, True)
   # cut = 'nvtx>=1'
    cut = ''
    #h_num = hr_num.draw('weight', cut, binning='100,0,100', goff=True)
   # h_den = hr_den.draw('weight', cut, binning='100,0,100', goff=True)
    eff = TEfficiency(num, den)

    eff.Draw();
    c.Update()
    c.Print("lepton_sigeff_%s.pdf" % (sample.name))
    
    #sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
   
    #print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)
       
#per = PerSignal('efficiency', y_range=(0.,1.05))


#per.add(stoplb, title='#tilde{t} #rightarrow lb')
#per.add(stopld, title='#tilde{t} #rightarrow ld', color=ROOT.kBlue)

#per.draw(canvas=ps.c)
#ps.save('sigeff')
