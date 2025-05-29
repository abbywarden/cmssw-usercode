#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'ULV13Lepm'
ps = plot_saver(plot_dir('sigeff_%s' % version), size=(800,600), pdf=True, log=False)

#CURRENTLY : Set up to compare cut and count Displaced SUSY with BDT results 
multijet = Samples.mfv_signal_samples_2017
dijet = Samples.mfv_stopdbardbar_samples_2017

semilep_ld = Samples.mfv_stopld_samples_2018
semilep_lb = Samples.mfv_stoplb_samples_2018

#search = ["cc", "bdt", "bdt_iso"]
# nice_ld = ['#tilde{t} #rightarrow ld cc', '#tilde{t} #rightarrow ld bdt', '#tilde{t} #rightarrow ld bdt iso']
# nice_lb = ['#tilde{t} #rightarrow lb cc', '#tilde{t} #rightarrow lb bdt', '#tilde{t} #rightarrow lb bdt iso']
# colors_ld = [ROOT.kRed, ROOT.kMagenta, ROOT.kViolet-3]
# colors_lb = [ROOT.kBlue, ROOT.kGreen+2, ROOT.kCyan+1]

search = ["cc", "bdt"]
nice_ld = ['#tilde{t} #rightarrow ld cc', '#tilde{t} #rightarrow ld bdt']
nice_lb = ['#tilde{t} #rightarrow lb cc', '#tilde{t} #rightarrow lb bdt']
colors_ld = [ROOT.kRed, ROOT.kMagenta]
colors_lb = [ROOT.kBlue, ROOT.kGreen+2]

# search = ["bdt_sellep", "bdt"]
# nice_ld = ['#tilde{t} #rightarrow ld sellep', '#tilde{t} #rightarrow ld bdt']
# nice_lb = ['#tilde{t} #rightarrow lb sellep', '#tilde{t} #rightarrow lb bdt']
# colors_ld = [ROOT.kRed, ROOT.kMagenta]
# colors_lb = [ROOT.kBlue, ROOT.kGreen+2]


#the grouping is : [model (stopld then stoplb), then mass, then lifetime]


# BDT April 23rd : BDT >= 0.95; hltmatched lepton w/ jetlep veto and photon trigger 
BDT = [
    
    2092, 9370, 21286, 29213, 21670, 
    4289, 16885, 33926, 41066, 29853, 
    6287, 21927, 42940, 51085, 38515, 
    8113, 28696, 53889, 65464, 48604, 
    9223, 32879, 60179, 36470, 53808, 
    9777, 34603, 62976, 38497, 58146, 
    9787, 35961, 66918, 40327, 62198, 
    10104, 37493, 67709, 42460, 64729, 
    10304, 37386, 35114, 42761, 32476, 
    10789, 38346, 35180, 43221, 21055, 

    942 , 4654,  11510, 16322, 11938,
    2270, 10142, 21631, 27639, 19836,
    3577, 15061, 30726, 38594, 27299,
    5592, 21676, 42725, 53326, 39976,
    6940, 26699, 52150, 31979, 47609,
    7915, 28794, 55660, 35103, 52554,
    8317, 31153, 60288, 36797, 56564,
    8790, 33037, 63511, 39272, 60053,
    9281, 34798, 32895, 41119, 31152,
    9609, 35600, 33637, 41844, 31819
]

# #BDT : require lepton in SV, bs2derr < 50um, dbv > 100um, ntracks >= 4, BDT >= 0.964, leading lepton iso < 0.1, tigh,med cutbased lep, v5 BDT
# #2018
# BDT_sellep = [
# 3100, 12651, 25513, 30332, 21416,
# 4924, 19484, 37607, 41836, 29412,
# 6650, 23413, 44891, 49387, 36010,
# 8133, 29137, 53292, 58422, 41771,
# 9105, 32724, 58280, 31798, 44840,
# 9571, 34124, 60272, 32911, 47754,
# 9481, 35170, 63524, 33885, 50696,
# 9708, 36533, 64175, 35716, 52340,
# 9821, 36174, 32999, 35552, 26039,
# 10217,37134, 33118, 36032, 14914,

# 1426, 6533 , 14175, 17352, 11856,
# 2668, 11897, 24615, 28966, 19944,
# 3861, 16358, 32588, 37970, 26041,
# 5638, 22192, 42702, 48696, 35121,
# 6817, 26725, 50894, 28296, 40542,
# 7694, 28416, 53425, 30717, 44225,
# 8021, 30688, 57850, 31805, 47165,
# 8396, 32305, 60639, 33771, 49668,
# 8787, 33900, 31248, 35246, 25695,
# 9201, 34552, 31899, 35436, 26056,

# ]

# BDT = [ 
#  3287, 13587, 27435, 32495, 22707, 
#  5355, 21136, 41003, 45169, 31370, 
#  7281, 25806, 49374, 53761, 38659, 
#  9131, 32502, 59849, 64403, 45563, 
# 10310, 37280, 66401, 35530, 49472, 
# 10938, 39135, 69296, 37096, 52979, 
# 11041, 40913, 73940, 38565, 56820, 
# 11371, 42853, 75183, 40955, 59226, 
# 11572, 42882, 39247, 41039, 29616, 
# 12263, 44397, 39578, 41848, 17018, 

#  1504,  6992, 15157, 18515, 12579,
#  2860, 12776, 26629, 31045, 21249,
#  4176, 17783, 35420, 41006, 27848,
#  6188, 24529, 47129, 53163, 37929,
#  7553, 29893, 56770, 31080, 44245,
#  8680, 32009, 60268, 34123, 48702,
#  9136, 34904, 65845, 35621, 52214,
#  9674, 36992, 69513, 38123, 55610,
# 10199, 39222, 36250, 40077, 28902,
# 10757, 40332, 37176, 40676, 29634      
# ]



#for sample in multijet + dijet:
for idx, sample in enumerate(semilep_ld + semilep_lb) :
    fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s/allsig_nogenmatch' % version, sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree_Standard/t')
    hr = draw_hist_register(t, True)
    #cut = 'nvtx>=2' # && svdist > 0.04'
    cut = 'nvtx>=2' # && svdist > 0.04'
    h = hr.draw('weight', cut, binning='1,0,1', goff=True)
    num, _ = get_integral(h)
    den = Samples.norm_from_file(f)
    print(num)
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
    
    #sample.ys = { "cc" : clopper_pearson(num, den), "bdt" : clopper_pearson(BDT[idx], den), "bdt_iso" : clopper_pearson(BDT_iso[idx], den)}
    sample.ys = { "cc" : clopper_pearson(num, den), "bdt" : clopper_pearson(BDT[idx], den)}
    #sample.ys = { "bdt_sellep" : clopper_pearson(BDT_sellep[idx], den), "bdt" : clopper_pearson(BDT[idx], den)}

    print(sample.name)
    print("Total events : ", den)
    print(sample.ys["cc"][0])
    print(sample.ys["bdt"][0])
    print( sample.ys["cc"][0]/sample.ys["bdt"][0])
    
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
        fn = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s/allsig_nogenmatch' % version, sample.name + '.root')
        if not os.path.exists(fn) :
            continue 
        sample.y, sample.yl, sample.yh = sample.ys[stype]
    per.add(semilep_ld, title=nice_ld[itype], color=colors_ld[itype])
    per.add(semilep_lb, title=nice_lb[itype], color=colors_lb[itype])


# per.add(semilep_lb, title='#tilde{t} #rightarrow lb', color=ROOT.kBlue)
# per.add(semilep_ld, title='#tilde{t} #rightarrow ld', color=ROOT.kMagenta)

per.draw(canvas=ps.c)
ps.save('sigeff_compareBDT_fullsel_wlep')
