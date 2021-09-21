#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'V27Lepm'
ps = plot_saver(plot_dir('sigeff_%s' % version), size=(600,600), pdf=True, log=False)

#multijet = Samples.mfv_signal_samples_2017
#dijet = Samples.mfv_stopdbardbar_samples_2017
stoplb = Samples.mfv_stoplb_samples_2018
stopld = Samples.mfv_stopld_samples_2018

for sample in stoplb + stopld:
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree/t')
    hr = draw_hist_register(t, True)
    cut = 'nvtx>=2' # && svdist > 0.04'
    h = hr.draw('weight', cut, binning='1,0,1', goff=True)
    num, _ = get_integral(h)
    den = Samples.norm_from_file(f)
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('efficiency', y_range=(0.,1.05))

#per.add(multijet, title='#tilde{N} #rightarrow tbs')
#per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)

per.add(stoplb, title='#tilde{t} #rightarrow lb')
per.add(stopld, title='#tilde{t} #rightarrow ld', color=ROOT.kBlue)

per.draw(canvas=ps.c)
ps.save('sigeff')
