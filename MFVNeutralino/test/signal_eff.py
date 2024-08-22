#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'ULV10Lepm'
ps = plot_saver(plot_dir('sigeff_%s' % version), size=(800,600), pdf=True, log=False)

#CURRENTLY : Set up to compare cut and count Displaced SUSY with BDT results 
multijet = Samples.mfv_signal_samples_2017
dijet = Samples.mfv_stopdbardbar_samples_2017

semilep_ld = Samples.mfv_stopld_samples_2018
semilep_lb = Samples.mfv_stoplb_samples_2018

search = ["cc", "bdt"]
nice_ld = ['#tilde{t} #rightarrow ld cc', '#tilde{t} #rightarrow ld bdt']
nice_lb = ['#tilde{t} #rightarrow lb cc', '#tilde{t} #rightarrow lb bdt']
colors_ld = [ROOT.kRed, ROOT.kMagenta]
colors_lb = [ROOT.kBlue, ROOT.kGreen+2]

#the grouping is : [model (stopld then stoplb), then mass, then lifetime]
# BDT : require lepton in SV, bs2derr < 50um, dbv > 100um, ntracks >= 4, BDT >= 0.989 if bdt < 200um, BDT >= 0.974 if bdt >= 200um 
BDT = [ 
#stopld
6939,  26343, 50738, 60198, 43803,
9284, 34202, 64056, 72136, 52218,
11407, 38823, 71381, 80071, 60116,
12672, 44211, 79517, 88834, 66007,
13593, 47981, 84248, 46785, 68099,
13879, 48381, 85433, 47634, 71050,
13507, 49364, 89121, 48309, 74380,
13498, 50847, 88922, 50136, 75742,
13767, 50193, 46118, 49912, 37292,
14047, 51040, 45928, 50191, 8147,

#stoplb
2819, 12879, 28180, 35635, 25369,
4618, 19964, 41149, 50528, 35989,
6203, 25548, 51173, 61533, 43823,
8422, 32702, 62797, 74236, 55343,
9934, 38028, 72409, 41508, 61429,
10800, 39432, 74986, 43977, 65773,
11032, 41974, 79844, 45069, 69223,
11397, 43916, 83075, 47482, 72215,
11919, 46024, 42683, 49159, 37069,
12427, 46762, 43475, 49446, 37573
]


#for sample in multijet + dijet:
for idx, sample in enumerate(semilep_ld + semilep_lb) :
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree_Standard/t')
    hr = draw_hist_register(t, True)
    cut = 'nvtx>=2' # && svdist > 0.04'
    h = hr.draw('weight', cut, binning='1,0,1', goff=True)
    num, _ = get_integral(h)
    den = Samples.norm_from_file(f)
    
    # cut_lep = 'nvtx>=1 && leading_leppt_inSV > 0'
    # hlep = hr.draw('weight', cut_lep, binning='1,0,1', goff=True)
    # numlep, lep_ = get_integral(hlep)
    
    #cut_den = 'pSkimSel'
    #cut_num = 'pSkimSel'
    #h_den = hr.draw('weight', cut_den, binning='1,0,1', goff=True)
    #h_num = hr.draw('weight', cut_num, binning='1,0,1', goff=True)
    #den, _ = get_integral(h_den)
    #num, _ = get_integral(h_num)

    #sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    #sample.y, sample.yl, sample.yh = clopper_pearson(BDT_sig_num[idx], BDT_sig_den[idx]) # ignore integral != entries, just get central value right
    
    sample.ys = { "cc" : clopper_pearson(num, den), "bdt" : clopper_pearson(BDT[idx], den)}
    #print(sample.name)
    #print(sample.ys["cc"][0])
    #print(sample.ys["bdt"][0])
    #print(sample.ys["bdt"][0] - sample.ys["cc"][0])
    
    # if num != 0 :
    #     sample.y = 10000/sample.y
    #     sample.yl = 10000/sample.yl
    #     sample.yh = 10000/sample.yh
    # #make it out of bounds 
    # else :
    #     sample.y =  10000000
    #     sample.yl = 10000000
    #     sample.yh = 10000000
    
    #print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)
    #print '%26s: nrequest = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('efficiency', y_range=(0.,1.0))
for itype, stype in enumerate(search):
    for sample in semilep_ld + semilep_lb:
        fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s' % version, sample.name + '.root')
        if not os.path.exists(fn) :
            continue 
        sample.y, sample.yl, sample.yh = sample.ys[stype]
    per.add(semilep_ld, title=nice_ld[itype], color=colors_ld[itype])
    per.add(semilep_lb, title=nice_lb[itype], color=colors_lb[itype])


# per.add(semilep_lb, title='#tilde{t} #rightarrow lb', color=ROOT.kBlue)
# per.add(semilep_ld, title='#tilde{t} #rightarrow ld', color=ROOT.kMagenta)

per.draw(canvas=ps.c)
ps.save('sigeff_compareBDT_fullsel_wlep_CC')
