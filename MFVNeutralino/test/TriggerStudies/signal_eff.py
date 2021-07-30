#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
#from JMTucker.MFVNeutralino.PerSignal import PerSignal
from JMTucker.MFVNeutralino.PerSignal_hnl import PerSignal_hnl

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(1200,600), log=False)

study_new_triggers = True

if study_new_triggers :
    root_file_dir = '/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1025p1/src/JMTucker/MFVNeutralino/test/TriggerStudies/TrigFilt/hnl_trilept/'
    #trigs = ['Trigger','TriggerBjets','TriggerDispDijet','TriggerOR']
    #nice = ['HT1050','Bjet','DisplacedDijet','Logical OR']
    #trigs = ['TriggerLeptons', 'TriggerDispLeptonsORLeptons', 'TriggerLeptonsORDiLeptons', 'TriggerDispLeptonsORDiLeptons']
    #nice = ['Lepton', '2DispLorL', 'Lor2L', '2DispLor2L']

    trigs = ['TriggerLeptons','TriggerDispLeptons','TriggerDiLeptons']
    nice = ['Lepton','Displ Dilept','Dilept']
    
   # trigs = ['TriggerLeptonsORHT','TriggerDispLeptonsORHT', 'TriggerDispLeptonsORLeptons','TriggerLeptonsORDiLeptons', 'TriggerDispLeptonsORDiLeptons']
   # nice = ['LorHT', '2DispLorHT', '2DispLorL', 'Lor2L', '2DispLor2L']

    #trigs = ['TriggerLeptons', 'TriggerLepton2', 'TriggerLepton3']
    #nice = ['orig lept', 'slim lept1', 'slim lept2']

   # trigs = ['TriggerLeptons', 'TriggerLepton2', 'TriggerDispLeptonsORLeptons', 'TriggerDispLeptonsORLepton2']
   # nice = ['orig lept', 'slim lept1', 'Disp2LorL', 'Disp2LorSlimL']

    



    #max 5
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+3, ROOT.kMagenta-3]
else :
    root_file_dir = '/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1025p1/src/JMTucker/MFVNeutralino/test/TriggerStudies/'
    trigs = ['Trigger']
    nice = ['PFHT1050']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kBlack]

def sample_ok(s):
    return True #s.mass not in (500,3000)

#semilept = Samples.mfv_stoplb_samples_2018
#semilept = Samples.mfv_stopld_samples_2018
#hnl_trilept_e =  Samples.hnl_trilept_e_samples_2018
hnl_trilept_mu = Samples.hnl_trilept_mu_samples_2018
#hnl_semilept_e = Samples.hnl_semilept_e_samples_2018
#hnl_semilept_mu = Samples.hnl_semilept_mu_samples_2018
#multijet = Samples.mfv_signal_samples_2018

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


for sample in hnl_trilept_mu:
    fn = os.path.join(root_file_dir, sample.name + '.root')
    if not os.path.exists(fn):
        print sample.name + '; not finding it'
        continue
    f = ROOT.TFile(fn)
    sample.ys = {n: getit(f,'p'+n) for n in trigs}

    
if len(trigs) > 1:
    kind = 'hnl_trilept_mu'
    #kind = 'hnl_semilept_e'
    samples = hnl_trilept_mu
    #y range original 1.15
    per = PerSignal_hnl('efficiency', y_range=(0.,1.15))
    for itrig, trig in enumerate(trigs):
        for sample in samples:
            sample.y, sample.yl, sample.yh = sample.ys[trig]
        per.add(samples, title=nice[itrig], color=colors[itrig])
    per.draw(canvas=ps.c)

    if study_new_triggers :
        #if need shorter; used 0.16, 0.18 for di-e; y range 0.2
        # emu used 0.5, 0.55; y range 0.6
        
       # mvpave(per.decay_paves[0], 5.0, 1.04, 9.8, 1.1)
        #mvpave(per.decay_paves[1], 10.0, 1.04, 14.8, 1.1)
        #mvpave(per.decay_paves[2], 15.0,  1.04, 19.8, 1.1) 
       # mvpave(per.decay_paves[2], 20.0, 1.04, 24.8, 1.1)
        
         mvpave(per.decay_paves[0], 2.0, 1.04, 3.5, 1.1)
         mvpave(per.decay_paves[1], 3.6, 1.04, 5.1, 1.1)
         mvpave(per.decay_paves[2], 5.2, 1.04, 6.8, 1.1)
         
        # mvpave(per.decay_paves[3], 18.5, 1.04, 22.8, 1.1)
        # mvpave(per.decay_paves[4], 23.0, 1.04, 27.3, 1.1)
        
       
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
        #used for emu: 0.45, 0.55; ee: 0.15, 0.18
        tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow lb')
        #tlatex.DrawLatex(0.15, 0.18, '#tilde{t} #rightarrow lb')
    elif kind == 'semilept_ld':
        tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow ld')
    elif kind == 'hnl_trilept_e':
        tlatex.DrawLatex(0.725, 1.05, "N #rightarrow ee#nu")
    elif kind == 'hnl_semilept_e':
        tlatex.DrawLatex(0.725, 1.005, "N #rightarrow jje")

    title = 'hnl_trilept_mu_test'
    ps.save(title)
    #ps.save(kind)
        
# else:
#     for sample in multijet + dijet:
#         fn = os.path.join(root_file_dir, sample.name + '.root')
#         if not os.path.exists(fn):
#             continue
#         f = ROOT.TFile(fn)
#         sample.ys = {n: getit(f,'p'+n) for n in trigs}
#         sample.y, sample.yl, sample.yh = sample.ys[trigs[0]]

#     per = PerSignal('efficiency', y_range=(0.,1.05))
#     per.add(multijet, title='#tilde{N} #rightarrow tbs')
#     per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
#     per.draw(canvas=ps.c)
#     mvpave(per.decay_paves[0], 0.703, 0.098, 6, 0.158)
#     mvpave(per.decay_paves[1], 0.703, 0.038, 6, 0.098)
#     ps.save('trigeff')

