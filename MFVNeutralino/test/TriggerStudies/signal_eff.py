import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(600,600), log=False, pdf=True)

# where "new" triggers = bjet and displaced dijet triggers
study_new_triggers = True

if study_new_triggers :

    root_file_dir = '/afs/hep.wisc.edu/home/acwarden/crabdirs/TrigFiltCheckV3/'
    trigs = ['TriggerLeptons', 'TriggerEMu_35_27', 'TriggerEMu_35_50', 'TriggerEMu_50_27', 'TriggerEMu_50_50']
    nice = ['SingleLep', 'EMu_35_27', 'EMu_35_50', 'EMu_50_27', 'EMu_50_50']

    #root_file_dir = '/uscms/home/ali/nobackup/LLP/crabdir/TrigFiltCheckV3/'
    #trigs = ['Trigger','TriggerBjets','TriggerDispDijet','TriggerMET']
    #nice = ['HT1050','Bjet','DisplacedDijet','MET']
    #root_file_dir = '/uscms/home/pkotamni/nobackup/crabdirs/TrigFiltCheckP0/'
    #trigs = ['Trigger','TriggerMET','TriggerMuons']
    #nice = ['HT1050','MET','Muons']
    
    #root_file_dir = '/uscms_data/d3/shogan/crab_dirs/TrigFiltCheckV3'
    #trigs = ['TriggerBjets','TriggerDispDijet','TriggerOR']
    #nice = ['Bjet','DisplacedDijet','Logical OR']
    #colors = [ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+3]
    #trigs = ['TriggerOR']
    #nice = ['Logical OR']
    #colors = [ROOT.kOrange+3]
else :
    root_file_dir = '/uscms_data/d2/tucker/crab_dirs/TrigFiltCheckV1'
    trigs = ['Trigger']
    nice = ['PFHT1050']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kBlack]

def sample_ok(s):
    return True #s.mass not in (500,3000)
#multijet = [s for s in Samples.mfv_signal_samples_2018 if sample_ok(s)]
#dijet = [s for s in Samples.mfv_stopdbardbar_samples_2018 if sample_ok(s)]
#splitSUSY = Samples.mfv_splitSUSY_samples_M2000_2017
multijet = [s for s in Samples.mfv_signal_samples_2016 if sample_ok(s)]
dijet_d = [s for s in Samples.mfv_stopdbardbar_samples_2016 if sample_ok(s)]
dijet_b = [s for s in Samples.mfv_stopbbarbbar_samples_2016 if sample_ok(s)]
#higgs   = [s for s in Samples.HToSSTodddd_samples_2016 if sample_ok(s)]

def getit(f, n):
    hnum = f.Get('SimpleTriggerEfficiency/triggers_pass_num')
    hden = f.Get('SimpleTriggerEfficiency/triggers_pass_den')
    for ibin in xrange(1, hnum.GetNbinsX()+1):
        if hnum.GetXaxis().GetBinLabel(ibin) == n:
            break
    return clopper_pearson(hnum.GetBinContent(ibin), hden.GetBinContent(ibin))

def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)


for sample in DisplacedSUSY: 
#for sample in multijet + dijet:
#for sample in splitSUSY:
#for sample in multijet + dijet_d + dijet_b:# +  higgs:
    fn = os.path.join(root_file_dir, sample.name + '.root')
    if not os.path.exists(fn):
        continue
    f = ROOT.TFile(fn)
    sample.ys = {n: getit(f,'p'+n) for n in trigs}

if len(trigs) > 1:
    #for kind, samples in ('multijet', multijet), ('dijet_d', dijet_d), ('dijet_b', dijet_b):
    kind = 'semilept_lb'
    samples = DisplacedSUSY

    per = PerSignal('efficiency', y_range=(0.,1.15))
    for itrig, trig in enumerate(trigs):
        for sample in samples:
            sample.y, sample.yl, sample.yh = sample.ys[trig]
        per.add(samples, title=nice[itrig], color=colors[itrig])
    per.draw(canvas=ps.c)

    if study_new_triggers :
        mvpave(per.decay_paves[0], 7.5, 1.04, 10.4, 1.1)
        mvpave(per.decay_paves[1], 11.5,1.00 , 17.5, 1.14)
        mvpave(per.decay_paves[2], 18.5,  1.04, 23.5, 1.1) 
    #    mvpave(per.decay_paves[3], 11.5, 1.04, 13.5, 1.1) 
    else :
        mvpave(per.decay_paves[0], 0.703, 1.018, 6.227, 1.098)
        mvpave(per.decay_paves[1], 6.729, 1.021, 14.073, 1.101)
        mvpave(per.decay_paves[2], 14.45, 1.033, 21.794, 1.093) 
        

    tlatex = ROOT.TLatex()
    tlatex.SetTextSize(0.04)
    if kind == 'multijet' :
        tlatex.DrawLatex(0.725, 1.05, '#tilde{N} #rightarrow tbs')
    elif kind == 'dijet' :
        tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow #bar{d}#bar{d}')
    elif kind == 'semilept_lb':
        tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow lb')
    elif kind == 'semilept_ld':
        tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow ld')
    elif kind == 'higgs':
        tlatex.DrawLatex(0.725, 1.05, 'WH #rightarrow SS #rightarrow d#bar{d}d#bar{d}') 
    else:
        tlatex.DrawLatex(0.725, 1.05, kind)
        
    ps.save(kind)
else:
    for sample in multijet + dijet_d + dijet_b:# + higgs:
        print sample.name
        fn = os.path.join(root_file_dir, sample.name + '.root')
        if not os.path.exists(fn):
            continue
        f = ROOT.TFile(fn)
        sample.ys = {n: getit(f,'p'+n) for n in trigs}
        sample.y, sample.yl, sample.yh = sample.ys[trigs[0]]
    per = PerSignal('efficiency', y_range=(0.,1.05))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet_d, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kGreen+2)
    per.add(dijet_b, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)
#    per.add(higgs, title='H #rightarrow SS #rightarrow 4d', color=ROOT.kBlack)
    per.draw(canvas=ps.c)
    mvpave(per.decay_paves[0], 0.703, 0.218, 6, 0.278)
    mvpave(per.decay_paves[1], 0.703, 0.158, 6, 0.218)
    mvpave(per.decay_paves[2], 0.703, 0.098, 6, 0.158)
#    mvpave(per.decay_paves[3], 0.703, 0.038, 8, 0.098)
    ps.save('trigeff_nopresel')

