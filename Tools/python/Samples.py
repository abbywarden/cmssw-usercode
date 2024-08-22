#!/usr/bin/env python

from JMTucker.Tools.Sample import *
from JMTucker.Tools.CMSSWTools import json_path

########################################################################

def _model(sample):
    s = sample if type(sample) == str else sample.name
    return s.split('_tau')[0]

def _tau(sample):
    s = sample if type(sample) == str else sample.name
    is_um = '0um_' in s
    x = int(s[s.index('tau')+3:s.index('um_' if is_um else 'mm_')])
    if not is_um:
        x *= 1000
    return x

def _mass(sample):
    s = sample if type(sample) == str else sample.name
    x = s.index('_M')
    y = s.find('_',x+1)
    if y == -1:
        y = len(s)
    return int(s[x+2:y])

def _decay(sample):
    s = sample if type(sample) == str else sample.name
    if s.startswith('of_'):
        s = s[3:]
    decay = {
        'mfv_neu': r'\tilde{N} \rightarrow tbs',
        'xx4j': r'X \rightarrow q\bar{q}',
        'mfv_ddbar': r'\tilde{g} \rightarrow d\bar{d}',
        'mfv_neuuds': r'\tilde{N} \rightarrow uds',
        'mfv_neuudmu': r'\tilde{N} \rightarrow u\bar{d}\mu^{\minus}',
        'mfv_neuude': r'\tilde{N} \rightarrow u\bar{d}e^{\minus}',
        'mfv_neucdb': r'\tilde{N} \rightarrow cdb',
        'mfv_neucds': r'\tilde{N} \rightarrow cds',
        'mfv_neutbb': r'\tilde{N} \rightarrow tbb',
        'mfv_neutds': r'\tilde{N} \rightarrow tds',
        'mfv_neuubb': r'\tilde{N} \rightarrow ubb',
        'mfv_neuudb': r'\tilde{N} \rightarrow udb',
        'mfv_neuudtu': r'\tilde{N} \rightarrow u\bar{d}\tau^{\minus}',
        'mfv_xxddbar': r'X \rightarrow d\bar{d}',
        'mfv_stopdbardbar': r'\tilde{t} \rightarrow \bar{d}\bar{d}',
        'mfv_stopbbarbbar': r'\tilde{t} \rightarrow \bar{b}\bar{b}',
        'mfv_stoplb': r'\tilde{t} \rightarrow lb',
        'mfv_stopld': r'\tilde{t} \rightarrow ld', 
        'mfv_splitSUSY': r'\tilde{g} \rightarrow qq\tilde{\chi}',
        'ggHToSSTobbbb' : r'ggH \rightarrow SS \rightarrow b\bar{b}b\bar{b}',
        'ggHToSSTodddd' : r'ggH \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'ggHToSSTo4l' : r'ggH \rightarrow SS \rightarrow llll',
        'ZHToSSTodddd' : r'ZH \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'WplusHToSSTodddd' : r'W^{\plus}H \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        'WminusHToSSTodddd' : r'W^{\minus}H \rightarrow SS \rightarrow d\bar{d}d\bar{d}',
        }[_model(s)]
    year = int(s.rsplit('_')[-1])
    assert 2015 <= year <= 2018 or year==20161 or year == 20162
    decay += ' (%i)' % year
    return decay

def _latex(sample):
    tau = _tau(sample)
    if tau < 1000:
        tau = '%3i\mum' % tau
    else:
        assert tau % 1000 == 0
        tau = '%4i\mm' % (tau/1000)
    return r'$%s$,   $c\tau = %s$, $M = %4s\GeV$' % (_decay(sample), tau, _mass(sample))

def _set_signal_stuff(sample):
    sample.is_signal = True
    sample.model = _model(sample)
    sample.decay = _decay(sample)
    sample.tau = _tau(sample)
    sample.mass = _mass(sample)
    sample.latex = _latex(sample)
    #sample.xsec = 1e-3
    if (sample.name.startswith('WplusH')):
        sample.xsec = 3*(9.426e-02)*0.01# xsec(pp->3*(W+->lv)H) * br(1% of H->SS) for 3 lepton flavours as in https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt13TeV#ppWH_Total_Cross_Section_with_ap and https://github.com/cms-sw/genproductions/blob/master/bin/Powheg/production/2017/13TeV/Higgs/WplusHJ_HanythingJ_NNPDF31_13TeV/HWplusJ_HanythingJ_NNPDF31_13TeV_M125_Vleptonic.input  
    else:
        #print(sample.name)
        sample.xsec = 1e-3
    sample.is_private = sample.dataset.startswith('/mfv_') and sample.dataset.endswith('/USER')
    if sample.is_private:
        sample.dbs_inst = 'phys03'
        sample.condor = True
        sample.xrootd_url = xrootd_sites['T3_US_FNALLPC']

########################################################################

########
# 2016 1 MC
########

qcd_samples_20161 = [
    MCSample('qcdht0100_20161', '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 73633197, nice='QCD, $100 < H_{T} < 200$ \\GeV',  color=802, syst_frac=0.20, xsec=2.366e7),
    MCSample('qcdht0200_20161', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 52503973, nice='QCD, $200 < H_{T} < 300$ \\GeV',  color=802, syst_frac=0.20, xsec=1.550e6),
    MCSample('qcdht0300_20161', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 52664292, nice='QCD, $300 < H_{T} < 500$ \\GeV',  color=803, syst_frac=0.20, xsec=3.245e5), 
    MCSample('qcdht0500_20161', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 58559243, nice='QCD, $500 < H_{T} < 700$ \\GeV', color=804, syst_frac=0.20, xsec=3.032e4),
    MCSample('qcdht0700_20161', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 45526707, nice='QCD, $700 < H_{T} < 1000$ \\GeV',  color=805, syst_frac=0.20, xsec=6.430e3),
    MCSample('qcdht1000_20161', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 14081307, nice='QCD, $1000 < H_{T} < 1500$ \\GeV', color=806, syst_frac=0.20, xsec=1.118e3),
    MCSample('qcdht1500_20161', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM', 10300081, nice='QCD, $1500 < H_{T} < 2000$ \\GeV', color=807, syst_frac=0.20, xsec=1.080e+02), 
    MCSample('qcdht2000_20161', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECOAPV-106X_mcRun2_asymptotic_preVFP_v8-v1/AODSIM',  5080758, nice='QCD, $H_{T} > 2000$ \\GeV', color=808, syst_frac=0.20, xsec=2.201e+01),
]


qcd_lep_samples_20161 = [
    MCSample('qcdempt015_20161',    '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   4062805, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_20161',     '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   8685279, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',  color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_20161',    '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   7156441, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_20161',    '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   4361931, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_20161',    '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   5440758, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_20161',    '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  4847354, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_20161',    '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 4852573, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_20161',    '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 1855461, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_20161',    '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 1142775, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',        color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept020_20161', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',        7913320, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_20161', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',        7967312, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_20161', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',       7690702, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_20161', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',      7342849, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_20161', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',      6856820, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
]

leptonic_samples_20161 = [
    MCSample('wjetstolnu_0j_20161',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      152373244,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=52.780e3), 
    MCSample('wjetstolnu_1j_20161',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      173468850,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=8.832e3), 
    MCSample('wjetstolnu_2j_20161',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',      87929021,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=3.276e3), 
    MCSample('dyjetstollM10_20161',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 25799525, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20161',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',     95170542, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20161 = [
    #MCSample('ttbar_20161',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                    94164991, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

ttbar_samples_20161 = [
    #MCSample('ttbar_20161',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                    94164991, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
    MCSample('ttbar_lep_20161',     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                    37505000, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_20161', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',             132178000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_20161',     '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',                 97600000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]


diboson_samples_20161 = [
    MCSample('ww_20161', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15859000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_20161', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  1282000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_20161', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  7934000, nice='WZ', color = 9, syst_frac=0.10, xsec=27.6)
]


mfv_signal_samples_20161 = [
    MCSample('mfv_neu_tau000100um_M0200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_neu_tau000300um_M0200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  75000),
    MCSample('mfv_neu_tau001000um_M0200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',    22000),
    MCSample('mfv_neu_tau010000um_M0200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_neu_tau030000um_M0200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   30000),
    MCSample('mfv_neu_tau000100um_M0300_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_neu_tau000300um_M0300_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  75000),
    MCSample('mfv_neu_tau001000um_M0300_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',    22000),
    MCSample('mfv_neu_tau010000um_M0300_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_neu_tau030000um_M0300_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   30000),
    MCSample('mfv_neu_tau000100um_M0400_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_neu_tau000300um_M0400_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  75000),
    MCSample('mfv_neu_tau001000um_M0400_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',    22000),
    MCSample('mfv_neu_tau010000um_M0400_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_neu_tau030000um_M0400_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   30000),
    MCSample('mfv_neu_tau000100um_M0600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_neu_tau000300um_M0600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  45000),
    MCSample('mfv_neu_tau001000um_M0600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',    14000),
    MCSample('mfv_neu_tau010000um_M0600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   8000),
    MCSample('mfv_neu_tau030000um_M0600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   13000),
    MCSample('mfv_neu_tau000100um_M0800_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_neu_tau000300um_M0800_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  37000),
    MCSample('mfv_neu_tau001000um_M0800_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    12000),
    MCSample('mfv_neu_tau010000um_M0800_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   7000),
    MCSample('mfv_neu_tau030000um_M0800_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   11000),
    MCSample('mfv_neu_tau000100um_M1200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 31000),
    MCSample('mfv_neu_tau001000um_M1200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   11000),
    MCSample('mfv_neu_tau010000um_M1200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  7000),
    MCSample('mfv_neu_tau030000um_M1200_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  9000),
    MCSample('mfv_neu_tau000100um_M1600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau001000um_M1600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   11000),
    MCSample('mfv_neu_tau010000um_M1600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  6000),
    MCSample('mfv_neu_tau030000um_M1600_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  9000),
    MCSample('mfv_neu_tau000100um_M3000_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 29000),
    MCSample('mfv_neu_tau001000um_M3000_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   10000),
    MCSample('mfv_neu_tau010000um_M3000_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  6000),
    MCSample('mfv_neu_tau030000um_M3000_20161', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  8000),
]

mfv_selected_signal_samples_20161 = [mfv_signal_samples_20161[21], mfv_signal_samples_20161[22]] 

mfv_stopdbardbar_samples_20161 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0200_20161', '/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0200_20161', '/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0200_20161', '/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0200_20161', '/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0200_20161', '/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0300_20161', '/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0300_20161', '/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0300_20161', '/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0300_20161', '/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0300_20161', '/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0400_20161', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_20161', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_20161', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_20161', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_20161', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_20161', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_20161', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 70000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_20161', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 18000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_20161', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 9000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_20161', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_20161', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_20161', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 58000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_20161', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 16000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_20161', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 8000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_20161', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 13000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_20161', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_20161', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_20161', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_20161', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 8000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_20161', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 12000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_20161', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_20161', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 45000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_20161', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 14000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_20161', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 8000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_20161', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 12000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_20161', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_20161', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_20161', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 14000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_20161', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 6000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_20161', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 10000),
]

mfv_selected_stopdbardbar_samples_20161 = [mfv_stopdbardbar_samples_20161[21], mfv_stopdbardbar_samples_20161[22]] 

mfv_stopbbarbbar_samples_20161 = [
    MCSample('mfv_stopbbarbbar_tau000100um_M0200_20161', '/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0200_20161', '/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0200_20161', '/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',    25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0200_20161', '/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0200_20161', '/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0300_20161', '/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0300_20161', '/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0300_20161', '/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0300_20161', '/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0300_20161', '/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0400_20161', '/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0400_20161', '/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0400_20161', '/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0400_20161', '/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0400_20161', '/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',   22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0600_20161', '/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0600_20161', '/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  70000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0600_20161', '/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    18000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0600_20161', '/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   9000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0600_20161', '/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   15000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0800_20161', '/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0800_20161', '/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  58000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0800_20161', '/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',    16000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0800_20161', '/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   9000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0800_20161', '/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   13000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1200_20161', '/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1200_20161', '/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  50000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1200_20161', '/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    15000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1200_20161', '/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   8000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1200_20161', '/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',   12000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1600_20161', '/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  96000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1600_20161', '/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',  40000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1600_20161', '/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    14000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1600_20161', '/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   8000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1600_20161', '/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   12000),
    MCSample('mfv_stopbbarbbar_tau000100um_M3000_20161', '/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M3000_20161', '/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',  44000),
    MCSample('mfv_stopbbarbbar_tau001000um_M3000_20161', '/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',    14000),
    MCSample('mfv_stopbbarbbar_tau010000um_M3000_20161', '/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM',   7000),
    MCSample('mfv_stopbbarbbar_tau030000um_M3000_20161', '/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',   10000),
]

mfv_selected_stopbbarbbar_samples_20161 = [mfv_stopbbarbbar_samples_20161[21], mfv_stopbbarbbar_samples_20161[22]] 

mfv_stoplb_samples_20161 = [
    MCSample('mfv_stoplb_tau000100um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98890),
    MCSample('mfv_stoplb_tau000300um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99090),
    MCSample('mfv_stoplb_tau010000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49863),
    MCSample('mfv_stoplb_tau001000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99632),
    MCSample('mfv_stoplb_tau030000um_M1000_20161', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99612),
    MCSample('mfv_stoplb_tau000100um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99340),
    MCSample('mfv_stoplb_tau000300um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99010),
    MCSample('mfv_stoplb_tau010000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49944),
    MCSample('mfv_stoplb_tau001000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 97995),
    MCSample('mfv_stoplb_tau030000um_M1200_20161', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101825),
    MCSample('mfv_stoplb_tau000100um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100444),
    MCSample('mfv_stoplb_tau000300um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98629),
    MCSample('mfv_stoplb_tau010000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49531),
    MCSample('mfv_stoplb_tau001000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99778),
    MCSample('mfv_stoplb_tau030000um_M1400_20161', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99896),
    MCSample('mfv_stoplb_tau000100um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99251),
    MCSample('mfv_stoplb_tau000300um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99184),
    MCSample('mfv_stoplb_tau010000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50317),
    MCSample('mfv_stoplb_tau001000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49741),
    MCSample('mfv_stoplb_tau030000um_M1600_20161', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 48712),
    MCSample('mfv_stoplb_tau000100um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100766),
    MCSample('mfv_stoplb_tau000300um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 81729),
    MCSample('mfv_stoplb_tau010000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49090),
    MCSample('mfv_stoplb_tau001000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49049),
    MCSample('mfv_stoplb_tau030000um_M1800_20161', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49438),
    MCSample('mfv_stoplb_tau000100um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99188),
    MCSample('mfv_stoplb_tau000300um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100726),
    MCSample('mfv_stoplb_tau010000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99023),
    MCSample('mfv_stoplb_tau001000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99012),
    MCSample('mfv_stoplb_tau030000um_M0200_20161', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99812),
    MCSample('mfv_stoplb_tau000100um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100222),
    MCSample('mfv_stoplb_tau000300um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100150),
    MCSample('mfv_stoplb_tau010000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98854),
    MCSample('mfv_stoplb_tau001000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100049),
    MCSample('mfv_stoplb_tau030000um_M0300_20161', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99401),
    MCSample('mfv_stoplb_tau000100um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100672),
    MCSample('mfv_stoplb_tau000300um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98457),
    MCSample('mfv_stoplb_tau010000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99343),
    MCSample('mfv_stoplb_tau001000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99760),
    MCSample('mfv_stoplb_tau030000um_M0400_20161', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98676),
    MCSample('mfv_stoplb_tau000100um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100158),
    MCSample('mfv_stoplb_tau000300um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98762),
    MCSample('mfv_stoplb_tau010000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99264),
    MCSample('mfv_stoplb_tau001000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101849),
    MCSample('mfv_stoplb_tau030000um_M0600_20161', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100390),
    MCSample('mfv_stoplb_tau000100um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98204),
    MCSample('mfv_stoplb_tau000300um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100784),
    MCSample('mfv_stoplb_tau010000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 48963),
    MCSample('mfv_stoplb_tau001000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100377),
    MCSample('mfv_stoplb_tau030000um_M0800_20161', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99164)
]

mfv_stopld_samples_20161 = [
    MCSample('mfv_stopld_tau000100um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99017),
    MCSample('mfv_stopld_tau000300um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99362),
    MCSample('mfv_stopld_tau010000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49856),
    MCSample('mfv_stopld_tau001000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98183),
    MCSample('mfv_stopld_tau030000um_M1000_20161', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100852),
    MCSample('mfv_stopld_tau000100um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99830),
    MCSample('mfv_stopld_tau000300um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99813),
    MCSample('mfv_stopld_tau010000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49767),
    MCSample('mfv_stopld_tau001000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100012),
    MCSample('mfv_stopld_tau030000um_M1200_20161', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99996),
    MCSample('mfv_stopld_tau000100um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100303),
    MCSample('mfv_stopld_tau000300um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98700),
    MCSample('mfv_stopld_tau010000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49501),
    MCSample('mfv_stopld_tau001000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99221),
    MCSample('mfv_stopld_tau030000um_M1400_20161', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99706),
    MCSample('mfv_stopld_tau000100um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98875),
    MCSample('mfv_stopld_tau000300um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98632),
    MCSample('mfv_stopld_tau010000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49359),
    MCSample('mfv_stopld_tau001000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50121),
    MCSample('mfv_stopld_tau030000um_M1600_20161', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50681),
    MCSample('mfv_stopld_tau000100um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99761),
    MCSample('mfv_stopld_tau000300um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100032),
    MCSample('mfv_stopld_tau010000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49884),
    MCSample('mfv_stopld_tau001000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49871),
    MCSample('mfv_stopld_tau030000um_M1800_20161', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49634),
    MCSample('mfv_stopld_tau000100um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101080),
    MCSample('mfv_stopld_tau000300um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98938),
    MCSample('mfv_stopld_tau010000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99845),
    MCSample('mfv_stopld_tau001000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99943),
    MCSample('mfv_stopld_tau030000um_M0200_20161', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99418),
    MCSample('mfv_stopld_tau000100um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101171),
    MCSample('mfv_stopld_tau000300um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100455),
    MCSample('mfv_stopld_tau010000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100892),
    MCSample('mfv_stopld_tau001000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99556),
    MCSample('mfv_stopld_tau030000um_M0300_20161', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99447),
    MCSample('mfv_stopld_tau000100um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100509),
    MCSample('mfv_stopld_tau000300um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99765),
    MCSample('mfv_stopld_tau010000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99682),
    MCSample('mfv_stopld_tau001000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99890),
    MCSample('mfv_stopld_tau030000um_M0400_20161', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99531),
    MCSample('mfv_stopld_tau000100um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100034),
    MCSample('mfv_stopld_tau000300um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99611),
    MCSample('mfv_stopld_tau010000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99643),
    MCSample('mfv_stopld_tau001000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99924),
    MCSample('mfv_stopld_tau030000um_M0600_20161', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 101612),
    MCSample('mfv_stopld_tau000100um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 100466),
    MCSample('mfv_stopld_tau000300um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98676),
    MCSample('mfv_stopld_tau010000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50147),
    MCSample('mfv_stopld_tau001000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 98387),
    MCSample('mfv_stopld_tau030000um_M0800_20161', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 99914)
]

ZHToSSTodddd_samples_20161 = [ 
    MCSample('ZHToSSTodddd_tau300um_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
    MCSample('ZHToSSTodddd_tau1mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49990), 
]

WplusHToSSTodddd_samples_20161 = [
    MCSample('WplusHToSSTodddd_tau300um_M55_20161','/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  24999),
    MCSample('WplusHToSSTodddd_tau1mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999),
]

WminusHToSSTodddd_samples_20161 = [
    MCSample('WminusHToSSTodddd_tau300um_M55_20161','/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999),
    MCSample('WminusHToSSTodddd_tau1mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24995),
]

ggHToSSTodddd_samples_20161 = [ 
    MCSample('ggHToSSTodddd_tau1mm_M55_20161',     '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',   256935),
    #MCSample('ggHToSSTodddd_tau10mm_M55_20161',    '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM',  270736),
    #MCSample('ggHToSSTodddd_tau100mm_M55_20161',   '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 268570),
]


#all_signal_samples_20161 = ZHToSSTodddd_samples_20161 + WplusHToSSTodddd_samples_20161 + WminusHToSSTodddd_samples_20161
all_signal_samples_20161 = mfv_stoplb_samples_20161 + mfv_stopld_samples_20161

#######
#2016 2 MC
#######

qcd_samples_20162 = [
    MCSample('qcdht0100_20162', '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 76121774, nice='QCD, $100 < H_{T} < 200$ \\GeV',  color=802, syst_frac=0.20, xsec=2.366e7),
    MCSample('qcdht0200_20162', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 43481129, nice='QCD, $200 < H_{T} < 300$ \\GeV',  color=802, syst_frac=0.20, xsec=1.550e6),
    MCSample('qcdht0300_20162', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 52221303, nice='QCD, $300 < H_{T} < 500$ \\GeV',  color=803, syst_frac=0.20, xsec=3.245e5), 
    MCSample('qcdht0500_20162', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 59109804, nice='QCD, $500 < H_{T} < 700$ \\GeV', color=804, syst_frac=0.20, xsec=3.032e4),
    MCSample('qcdht0700_20162', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 46439412, nice='QCD, $700 < H_{T} < 1000$ \\GeV',  color=805, syst_frac=0.20, xsec=6.430e3),
    MCSample('qcdht1000_20162', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 12675816, nice='QCD, $1000 < H_{T} < 1500$ \\GeV', color=806, syst_frac=0.20, xsec=1.118e3),
    MCSample('qcdht1500_20162', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM', 9387470, nice='QCD, $1500 < H_{T} < 2000$ \\GeV', color=807, syst_frac=0.20, xsec=1.080e+02), 
    MCSample('qcdht2000_20162', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer20UL16RECO-106X_mcRun2_asymptotic_v13-v1/AODSIM',  4980828, nice='QCD, $H_{T} > 2000$ \\GeV',            color=808, syst_frac=0.20, xsec=2.201e+01),
]


qcd_lep_samples_20162 = [
    MCSample('qcdempt015_20162',    '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',   4026314, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdmupt15_20162',     '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   8884250, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV',  color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt020_20162',    '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   7134788, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_20162',    '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   4351014, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_20162',    '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   5443934, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_20162',    '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',  4804788, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_20162',    '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 5007347, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_20162',    '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 1861129, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched',  color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_20162',    '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 1138742, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',        color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept020_20162', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',        7308299, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_20162', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',        7714512, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_20162', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',       7882938, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_20162', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',      7863538, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_20162', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',      8152626, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),
]
    
leptonic_samples_20162 = [
    MCSample('wjetstolnu_0j_20162',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      159895674,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=52.780e3), 
    MCSample('wjetstolnu_1j_20162',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      167715035,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=8.832e3), 
    MCSample('wjetstolnu_2j_20162',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',      85825681,nice='W + jets #rightarrow l#nu', color= 9, syst_fac=0.10, xsec=3.276e3), 
    MCSample('dyjetstollM10_20162',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 23706672, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_20162',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',     82448537, nice='DY + jets #rightarrow ll, M > 50 GeV',      color= 32, syst_frac=0.10, xsec=5.34e3),
]

met_samples_20162 = [
    #MCSample('ttbar_20162',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    90609841, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
]

ttbar_samples_20162 = [
    MCSample('ttbar_20162',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    90609841, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
    MCSample('ttbar_lep_20162',     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    43630000, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_20162', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',             144974000 , nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_20162',     '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                 109380000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]

ttbar_samples_20162 = [
    MCSample('ttbar_lep_20162',     '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    43630000, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_20162', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',             144974000 , nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_20162',     '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                 109380000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]


diboson_samples_20162 = [
    MCSample('ww_20162', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15821000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_20162', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  1151000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_20162', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',  7584000, nice='WZ', color = 9, syst_frac=0.10, xsec=27.6)
]

mfv_signal_samples_20162 = [
    MCSample('mfv_neu_tau000100um_M0200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 75000),
    MCSample('mfv_neu_tau001000um_M0200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 22000),
    MCSample('mfv_neu_tau010000um_M0200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_neu_tau030000um_M0200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau000100um_M0300_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0300_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 75000),
    MCSample('mfv_neu_tau001000um_M0300_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 22000),
    MCSample('mfv_neu_tau010000um_M0300_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 15000),
    MCSample('mfv_neu_tau030000um_M0300_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau000100um_M0400_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0400_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 75000),
    MCSample('mfv_neu_tau001000um_M0400_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 22000),
    MCSample('mfv_neu_tau010000um_M0400_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_neu_tau030000um_M0400_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau000100um_M0600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 45000),
    MCSample('mfv_neu_tau001000um_M0600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 14000),
    MCSample('mfv_neu_tau010000um_M0600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 8000),
    MCSample('mfv_neu_tau030000um_M0600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 13000),
    MCSample('mfv_neu_tau000100um_M0800_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M0800_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 37000),
    MCSample('mfv_neu_tau001000um_M0800_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 12000),
    MCSample('mfv_neu_tau010000um_M0800_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 7000),
    MCSample('mfv_neu_tau030000um_M0800_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 11000),
    MCSample('mfv_neu_tau000100um_M1200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 31000),
    MCSample('mfv_neu_tau001000um_M1200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 11000),
    MCSample('mfv_neu_tau010000um_M1200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 7000),
    MCSample('mfv_neu_tau030000um_M1200_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 9000),
    MCSample('mfv_neu_tau000100um_M1600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M1600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau001000um_M1600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 11000),
    MCSample('mfv_neu_tau010000um_M1600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 6000),
    MCSample('mfv_neu_tau030000um_M1600_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 9000),
    MCSample('mfv_neu_tau000100um_M3000_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_neu_tau000300um_M3000_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 29000),
    MCSample('mfv_neu_tau001000um_M3000_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 10000),
    MCSample('mfv_neu_tau010000um_M3000_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 6000),
    MCSample('mfv_neu_tau030000um_M3000_20162', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 8000),
]

mfv_selected_signal_samples_20162 = [mfv_signal_samples_20162[21], mfv_signal_samples_20162[22]] 

mfv_stopdbardbar_samples_20162 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0200_20162', '/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0200_20162', '/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0200_20162', '/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0200_20162', '/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0200_20162', '/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0300_20162', '/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0300_20162', '/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0300_20162', '/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0300_20162', '/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0300_20162', '/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0400_20162', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_20162', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_20162', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_20162', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_20162', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_20162', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_20162', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 70000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_20162', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 18000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_20162', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 9000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_20162', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_20162', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_20162', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 58000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_20162', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 16000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_20162', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 9000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_20162', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 13000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_20162', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_20162', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_20162', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_20162', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 8000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_20162', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 12000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_20162', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_20162', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 45000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_20162', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 14000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_20162', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 8000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_20162', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 12000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_20162', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_20162', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_20162', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 14000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_20162', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 7000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_20162', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 10000),
]

mfv_selected_stopdbardbar_samples_20162 = [mfv_stopdbardbar_samples_20162[21], mfv_stopdbardbar_samples_20162[22]] 

mfv_stopbbarbbar_samples_20162 = [
    MCSample('mfv_stopbbarbbar_tau000100um_M0200_20162', '/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0200_20162', '/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0200_20162', '/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0200_20162', '/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0200_20162', '/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0300_20162', '/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0300_20162', '/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0300_20162', '/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0300_20162', '/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0300_20162', '/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0400_20162', '/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0400_20162', '/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0400_20162', '/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0400_20162', '/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0400_20162', '/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 22000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0600_20162', '/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0600_20162', '/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 70000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0600_20162', '/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 18000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0600_20162', '/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 9000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0600_20162', '/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0800_20162', '/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0800_20162', '/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 58000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0800_20162', '/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 16000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0800_20162', '/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 9000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0800_20162', '/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 13000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1200_20162', '/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1200_20162', '/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1200_20162', '/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1200_20162', '/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 8000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1200_20162', '/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 12000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1600_20162', '/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1600_20162', '/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 45000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1600_20162', '/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 14000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1600_20162', '/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 8000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1600_20162', '/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 12000),
    MCSample('mfv_stopbbarbbar_tau000100um_M3000_20162', '/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100000),
    MCSample('mfv_stopbbarbbar_tau000300um_M3000_20162', '/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau001000um_M3000_20162', '/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 14000),
    MCSample('mfv_stopbbarbbar_tau010000um_M3000_20162', '/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 7000),
    MCSample('mfv_stopbbarbbar_tau030000um_M3000_20162', '/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 10000),
]

mfv_selected_stopbbarbbar_samples_20162 = [mfv_stopbbarbbar_samples_20162[21], mfv_stopbbarbbar_samples_20162[22]] 

mfv_stoplb_samples_20162 = [
    MCSample('mfv_stoplb_tau000100um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99539),
    MCSample('mfv_stoplb_tau000300um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99257),
    MCSample('mfv_stoplb_tau010000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 47714),
    MCSample('mfv_stoplb_tau001000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98557),
    MCSample('mfv_stoplb_tau030000um_M1000_20162', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99898),
    MCSample('mfv_stoplb_tau000100um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100330),
    MCSample('mfv_stoplb_tau000300um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98676),
    MCSample('mfv_stoplb_tau010000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49832),
    MCSample('mfv_stoplb_tau001000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98582),
    MCSample('mfv_stoplb_tau030000um_M1200_20162', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100391),
    MCSample('mfv_stoplb_tau000100um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100112),
    MCSample('mfv_stoplb_tau000300um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99840),
    MCSample('mfv_stoplb_tau010000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49856),
    MCSample('mfv_stoplb_tau001000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99508),
    MCSample('mfv_stoplb_tau030000um_M1400_20162', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99537),
    MCSample('mfv_stoplb_tau000100um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99744),
    MCSample('mfv_stoplb_tau000300um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99902),
    MCSample('mfv_stoplb_tau010000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49227),
    MCSample('mfv_stoplb_tau001000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50163),
    MCSample('mfv_stoplb_tau030000um_M1600_20162', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50181),
    MCSample('mfv_stoplb_tau000100um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98144),
    MCSample('mfv_stoplb_tau000300um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101235),
    MCSample('mfv_stoplb_tau010000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50608),
    MCSample('mfv_stoplb_tau001000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49712),
    MCSample('mfv_stoplb_tau030000um_M1800_20162', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49799),
    MCSample('mfv_stoplb_tau000100um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 99793),
    MCSample('mfv_stoplb_tau000300um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99406),
    MCSample('mfv_stoplb_tau010000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99401),
    MCSample('mfv_stoplb_tau001000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 97820),
    MCSample('mfv_stoplb_tau030000um_M0200_20162', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101202),
    MCSample('mfv_stoplb_tau000100um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99857),
    MCSample('mfv_stoplb_tau000300um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99010),
    MCSample('mfv_stoplb_tau010000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101044),
    MCSample('mfv_stoplb_tau001000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99219),
    MCSample('mfv_stoplb_tau030000um_M0300_20162', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99207),
    MCSample('mfv_stoplb_tau000100um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98268),
    MCSample('mfv_stoplb_tau000300um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100008),
    MCSample('mfv_stoplb_tau010000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101168),
    MCSample('mfv_stoplb_tau001000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99255),
    MCSample('mfv_stoplb_tau030000um_M0400_20162', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99198),
    MCSample('mfv_stoplb_tau000100um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100291),
    MCSample('mfv_stoplb_tau000300um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 86231),
    MCSample('mfv_stoplb_tau010000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100170),
    MCSample('mfv_stoplb_tau001000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99575),
    MCSample('mfv_stoplb_tau030000um_M0600_20162', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100308),
    MCSample('mfv_stoplb_tau000100um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100987),
    MCSample('mfv_stoplb_tau000300um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100012),
    MCSample('mfv_stoplb_tau010000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50027),
    MCSample('mfv_stoplb_tau001000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99440),
    MCSample('mfv_stoplb_tau030000um_M0800_20162', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98586)

]

mfv_stopld_samples_20162 = [
    MCSample('mfv_stopld_tau000100um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99376),
    MCSample('mfv_stopld_tau000300um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100018),
    MCSample('mfv_stopld_tau010000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49142),
    MCSample('mfv_stopld_tau001000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100845),
    MCSample('mfv_stopld_tau030000um_M1000_20162', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99794),
    MCSample('mfv_stopld_tau000100um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99574),
    MCSample('mfv_stopld_tau000300um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99868),
    MCSample('mfv_stopld_tau010000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49886),
    MCSample('mfv_stopld_tau001000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99291),
    MCSample('mfv_stopld_tau030000um_M1200_20162', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99929),
    MCSample('mfv_stopld_tau000100um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100532),
    MCSample('mfv_stopld_tau000300um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99932),
    MCSample('mfv_stopld_tau010000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49788),
    MCSample('mfv_stopld_tau001000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 98682),
    MCSample('mfv_stopld_tau030000um_M1400_20162', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 101616),
    MCSample('mfv_stopld_tau000100um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100675),
    MCSample('mfv_stopld_tau000300um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100486),
    MCSample('mfv_stopld_tau010000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49732),
    MCSample('mfv_stopld_tau001000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50045),
    MCSample('mfv_stopld_tau030000um_M1600_20162', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49682),
    MCSample('mfv_stopld_tau000100um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99094),
    MCSample('mfv_stopld_tau000300um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99749),
    MCSample('mfv_stopld_tau010000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49663),
    MCSample('mfv_stopld_tau001000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49813),
    MCSample('mfv_stopld_tau030000um_M1800_20162', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50468),
    MCSample('mfv_stopld_tau000100um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100260),
    MCSample('mfv_stopld_tau000300um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99340),
    MCSample('mfv_stopld_tau010000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99542),
    MCSample('mfv_stopld_tau001000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 97872),
    MCSample('mfv_stopld_tau030000um_M0200_20162', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100076),
    MCSample('mfv_stopld_tau000100um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100170),
    MCSample('mfv_stopld_tau000300um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100594),
    MCSample('mfv_stopld_tau010000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99759),
    MCSample('mfv_stopld_tau001000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99504),
    MCSample('mfv_stopld_tau030000um_M0300_20162', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99243),
    MCSample('mfv_stopld_tau000100um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100052),
    MCSample('mfv_stopld_tau000300um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99431),
    MCSample('mfv_stopld_tau010000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99314),
    MCSample('mfv_stopld_tau001000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100447),
    MCSample('mfv_stopld_tau030000um_M0400_20162', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99547),
    MCSample('mfv_stopld_tau000100um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100954),
    MCSample('mfv_stopld_tau000300um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99589),
    MCSample('mfv_stopld_tau010000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100599),
    MCSample('mfv_stopld_tau001000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99859),
    MCSample('mfv_stopld_tau030000um_M0600_20162', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100128),
    MCSample('mfv_stopld_tau000100um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99282),
    MCSample('mfv_stopld_tau000300um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 99263),
    MCSample('mfv_stopld_tau010000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49387),
    MCSample('mfv_stopld_tau001000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100038),
    MCSample('mfv_stopld_tau030000um_M0800_20162', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 100282)
]

ZHToSSTodddd_samples_20162 = [ 
    MCSample('ZHToSSTodddd_tau300um_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau1mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49998), 
]

WplusHToSSTodddd_samples_20162 = [
    MCSample('WplusHToSSTodddd_tau300um_M55_20162','/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',  24997),
    MCSample('WplusHToSSTodddd_tau1mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998),
]

WminusHToSSTodddd_samples_20162 = [
    MCSample('WminusHToSSTodddd_tau300um_M55_20162','/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998),
    MCSample('WminusHToSSTodddd_tau1mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998),
]

ggHToSSTodddd_samples_20162 = [ 
    MCSample('ggHToSSTodddd_tau1mm_M55_20162',     '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',   271240),
    #MCSample('ggHToSSTodddd_tau10mm_M55_20162',    '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',  259184),
    #MCSample('ggHToSSTodddd_tau100mm_M55_20162',   '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 261360),
]

#all_signal_samples_20162 = ZHToSSTodddd_samples_20162 + WplusHToSSTodddd_samples_20162 + WminusHToSSTodddd_samples_20162
all_signal_samples_20162 = mfv_stoplb_samples_20162 + mfv_stopld_samples_20162 

########
# 2017 MC 
########

qcd_samples_2017 = [
    MCSample('qcdht0200_2017', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57816581, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57097305, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 9183471, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0500ext_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6_ext1-v1/AODSIM', 59037642, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 45774525, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 15420054, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',     7711548, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   5451735, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    ]

qcd_lep_samples_2017 = [
    MCSample('qcdmupt15_2017',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',  17716270, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    # MCSample('qcdpt15mupt5_2017',  '/QCD_Pt-15To20_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  9019841, nice='QCD, 20 GeV > #hat{p}_{T} > 15 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.8e6),
    # MCSample('qcdpt20mupt5_2017',  '/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  64634535, nice='QCD, 30 GeV > #hat{p}_{T} > 20 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.527e6),
    # MCSample('qcdpt30mupt5_2017',  '/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  58749714, nice='QCD, 50 GeV > #hat{p}_{T} > 30 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=1.367e6),
    # MCSample('qcdpt50mupt5_2017',  '/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  40377957, nice='QCD, 80 GeV > #hat{p}_{T} > 50 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=3.817e5),
    # MCSample('qcdpt80mupt5_2017',  '/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  45981017, nice='QCD, 120 GeV > #hat{p}_{T} > 80 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=8.774e4),
    # MCSample('qcdpt120mupt5_2017',  '/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM',  39394151, nice='QCD, 170 GeV > #hat{p}_{T} > 120 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=2.128e4),
    # MCSample('qcdpt170mupt5_2017',  '/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 73071987, nice='QCD, 300 GeV > #hat{p}_{T} > 170 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=7e3),
    # MCSample('qcdpt300mupt5_2017',  '/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 58692910, nice='QCD, 470 GeV > #hat{p}_{T} > 300 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=6.226e2),
    # MCSample('qcdpt470mupt5_2017',  '/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 39491752, nice='QCD, 600 GeV > #hat{p}_{T} > 470 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=58.9),
    # MCSample('qcdpt600mupt5_2017',  '/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 39321940, nice='QCD, 800 GeV > #hat{p}_{T} > 600 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=18.12),
    # MCSample('qcdpt800mupt5_2017',  '/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 78215559, nice='QCD, 1 TeV GeV > #hat{p}_{T} > 800 GeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=3.318),
    # MCSample('qcdpt1000mupt5_2017',  '/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v9-v2/AODSIM', 27478273, nice='QCD, #hat{p}_{T} > 1 TeV, #mu p_{T} > 5 GeV', color=801, syst_frac=0.20, xsec=1.085),
    MCSample('qcdempt015_2017', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   7966910, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6), #Alec added from here 
    MCSample('qcdempt020_2017', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   14166147, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2017', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   8784542, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2017', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   10590542, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2017', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',   9615795, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2017', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  9904245, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2017', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  3678200, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2017', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  2214934, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0), #Alec to here  
    MCSample('qcdbctoept015_2017', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',      18671506, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.862e5),
    MCSample('qcdbctoept020_2017', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      14248556, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5), #Alec add from here 
    MCSample('qcdbctoept030_2017', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',      15656025, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2017', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',     16158199, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2017', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',    15940531, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2017', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM',    16028600, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5), #Alec to here
    ]
    
ttbar_samples_2017 = [
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',  249133364, nice='t#bar{t}', color=4,   syst_frac=0.15, xsec=831.76),
    MCSample('ttbar_lep_2017',            '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',             106724000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_2017', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM',             355332000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_2017',         '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',             235719999, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]

bjet_samples_2017 = [
    ]

leptonic_samples_2017 = [
    #MCSample('wjetstolnu_2017',   '/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 26838734, nice='NLO W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=6.735e4),
    MCSample('wjetstolnu_0j_2017','/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 169421340, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=52.78e3),
    MCSample('wjetstolnu_1j_2017','/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 180015088, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=8.832e3),
    MCSample('wjetstolnu_2j_2017','/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 96032711, nice='W + jets #rightarrow l#nu', color= 38, syst_fac=0.10, xsec=3.276e3),
    MCSample('dyjetstollM10_2017',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/AODSIM',                  68480179, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/AODSIM',          103344974, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
    ]


example_samples_zz_2017 = [
    MCSample('example_zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    ]

met_samples_2017 = [
    #MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',    249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76),
    MCSample('ttbar_2017',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  249133364, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=831.76), #Alec commented this line
    ]

diboson_samples_2017 = [
    MCSample('ww_2017', '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15883000, nice='WW', color = 9, syst_frac=0.10, xsec=75.8),
    MCSample('zz_2017', '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 2708000, nice='ZZ', color = 9, syst_frac=0.10, xsec=12.140),
    MCSample('wz_2017', '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 7898000, nice='WZ', color =9, syst_frac=0.10, xsec=27.6),
    ]

Zvv_samples_2017 = [
    MCSample('zjetstonunuht0100_2017', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 19141242, nice='Z + jets #rightarrow #nu #nu 100 < H_{T} < 200 GeV', color=1, syst_frac=0.20, xsec=302.8),
    MCSample('zjetstonunuht0200_2017', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 17468549, nice='Z + jets #rightarrow #nu #nu 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=92.59),
    MCSample('zjetstonunuht0400_2017', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 13963690, nice='Z + jets #rightarrow #nu #nu 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=13.18),
    MCSample('zjetstonunuht0600_2017', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 4418971, nice='Z + jets #rightarrow #nu #nu 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=3.257),
    MCSample('zjetstonunuht0800_2017', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 1513585, nice='Z + jets #rightarrow #nu #nu 800 < H_{T} < 1200 GeV', color=1, syst_frac=0.20, xsec=1.49),
    MCSample('zjetstonunuht1200_2017', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 267125, nice='Z + jets #rightarrow #nu #nu 1200 < H_{T} < 2500 GeV', color=1, syst_frac=0.20, xsec=0.3419),
    MCSample('zjetstonunuht2500_2017', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM', 176201, nice='Z + jets #rightarrow #nu #nu H_{T} > 2500 GeV', color=1, syst_frac=0.20, xsec=0.005146),
    ]

mfv_splitSUSY_samples_2017 = [
  MCSample('mfv_splitSUSY_tau000001000um_M1400_1200_2017', '/mfv_splitSUSY_tau000001000um_M1400_1200_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M1400_1200_2017', '/mfv_splitSUSY_tau000010000um_M1400_1200_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M1200_1100_2017', '/mfv_splitSUSY_tau000001000um_M1200_1100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M1200_1100_2017', '/mfv_splitSUSY_tau000010000um_M1200_1100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2000_1800_2017', '/mfv_splitSUSY_tau000000100um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2000_1800_2017', '/mfv_splitSUSY_tau000000300um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1800_2017', '/mfv_splitSUSY_tau000010000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1800_2017', '/mfv_splitSUSY_tau000001000um_M2000_1800_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2000_1900_2017', '/mfv_splitSUSY_tau000000100um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2000_1900_2017', '/mfv_splitSUSY_tau000000300um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2000_1900_2017', '/mfv_splitSUSY_tau000010000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2000_1900_2017', '/mfv_splitSUSY_tau000001000um_M2000_1900_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2400_100_2017', '/mfv_splitSUSY_tau000000100um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2400_100_2017', '/mfv_splitSUSY_tau000000300um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_100_2017', '/mfv_splitSUSY_tau000010000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_100_2017', '/mfv_splitSUSY_tau000001000um_M2400_100_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000100um_M2400_2300_2017', '/mfv_splitSUSY_tau000000100um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000000300um_M2400_2300_2017', '/mfv_splitSUSY_tau000000300um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000010000um_M2400_2300_2017', '/mfv_splitSUSY_tau000010000um_M2400_2300_2017/None/USER', 10000),
  MCSample('mfv_splitSUSY_tau000001000um_M2400_2300_2017', '/mfv_splitSUSY_tau000001000um_M2400_2300_2017/None/USER', 10000),
]

mfv_signal_samples_2017 = [
    MCSample('mfv_neu_tau000100um_M0200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 150000),
    # 1mm M0200
    MCSample('mfv_neu_tau010000um_M0200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0300_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0300_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 150000),
    MCSample('mfv_neu_tau001000um_M0300_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 43000),
    MCSample('mfv_neu_tau010000um_M0300_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0300_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    # 300um M0400 
    MCSample('mfv_neu_tau001000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 43000),
    MCSample('mfv_neu_tau010000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0400_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 89000),
    MCSample('mfv_neu_tau001000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 27000),
    MCSample('mfv_neu_tau010000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 16000),
    MCSample('mfv_neu_tau030000um_M0600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 25000),
    MCSample('mfv_neu_tau000300um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 73000),
    MCSample('mfv_neu_tau001000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 24000),
    MCSample('mfv_neu_tau010000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 14000),
    MCSample('mfv_neu_tau030000um_M0800_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 21000),
    MCSample('mfv_neu_tau000100um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 62000),
    MCSample('mfv_neu_tau001000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 22000),
    MCSample('mfv_neu_tau010000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 13000),
    MCSample('mfv_neu_tau030000um_M1200_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 18000),
    MCSample('mfv_neu_tau000100um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 59000),
    MCSample('mfv_neu_tau001000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 21000),
    MCSample('mfv_neu_tau010000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 12000),
    MCSample('mfv_neu_tau030000um_M1600_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 17000),
    MCSample('mfv_neu_tau000100um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 58000),
    MCSample('mfv_neu_tau001000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 20000),
    MCSample('mfv_neu_tau010000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 12000),
    MCSample('mfv_neu_tau030000um_M3000_2017', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15000),
]

mfv_selected_signal_samples_2017 = [mfv_signal_samples_2017[18], mfv_signal_samples_2017[19]] 
mfv_signal_samples_lowmass_2017 = [mfv_signal_samples_2017[2], mfv_signal_samples_2017[6], mfv_signal_samples_2017[7]]
mfv_signal_samples_temp_2017 = mfv_signal_samples_2017[:-16]

mfv_stopdbardbar_samples_2017 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0200_2017', '/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0200_2017', '/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0200_2017', '/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0200_2017', '/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0200_2017', '/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0300_2017', '/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0300_2017', '/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0300_2017', '/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0300_2017', '/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0300_2017', '/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2017', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 140000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 18000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2017', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 29000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 116000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 32000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 17000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2017', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 26000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 29000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2017', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 23000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 28000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2017', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 23000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 88000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 28000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 13000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2017', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 20000),
]

mfv_selected_stopdbardbar_samples_2017 = [mfv_stopdbardbar_samples_2017[20], mfv_stopdbardbar_samples_2017[21]] 

mfv_stopdbardbar_samples_lowmass_2017 = [mfv_stopdbardbar_samples_2017[2], mfv_stopdbardbar_samples_2017[3], mfv_stopdbardbar_samples_2017[7], mfv_stopdbardbar_samples_2017[8]]
mfv_stopdbardbar_samples_temp_2017 = mfv_stopdbardbar_samples_2017[:-15]

mfv_stopbbarbbar_samples_2017 = [
    MCSample('mfv_stopbbarbbar_tau000100um_M0200_2017', '/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0200_2017', '/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0200_2017', '/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0200_2017', '/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0200_2017', '/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0300_2017', '/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0300_2017', '/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0300_2017', '/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0300_2017', '/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0300_2017', '/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0400_2017', '/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0400_2017', '/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0400_2017', '/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0400_2017', '/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0400_2017', '/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0600_2017', '/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0600_2017', '/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 140000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0600_2017', '/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 36000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0600_2017', '/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 18000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0600_2017', '/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 29000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0800_2017', '/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0800_2017', '/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 116000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0800_2017', '/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 32000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0800_2017', '/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 17000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0800_2017', '/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 26000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1200_2017', '/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1200_2017', '/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1200_2017', '/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 29000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1200_2017', '/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1200_2017', '/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 23000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1600_2017', '/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 89000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1600_2017', '/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 28000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1600_2017', '/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1600_2017', '/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 23000),
    MCSample('mfv_stopbbarbbar_tau000100um_M3000_2017', '/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M3000_2017', '/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 88000),
    MCSample('mfv_stopbbarbbar_tau001000um_M3000_2017', '/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 28000),
    MCSample('mfv_stopbbarbbar_tau010000um_M3000_2017', '/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 13000),
    MCSample('mfv_stopbbarbbar_tau030000um_M3000_2017', '/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 20000),
]

mfv_selected_stopbbarbbar_samples_2017 = [mfv_stopbbarbbar_samples_2017[21], mfv_stopbbarbbar_samples_2017[22]] 
mfv_stopbbarbbar_samples_lowmass_2017 = [mfv_stopbbarbbar_samples_2017[2], mfv_stopbbarbbar_samples_2017[3], mfv_stopbbarbbar_samples_2017[7], mfv_stopbbarbbar_samples_2017[8]]
mfv_stopbbarbbar_samples_temp_2017 = mfv_stopbbarbbar_samples_2017[:-15]


mfv_stoplb_samples_2017 = [
    MCSample('mfv_stoplb_tau000100um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 194928),
    MCSample('mfv_stoplb_tau000300um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200301),
    MCSample('mfv_stoplb_tau010000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98261),
    MCSample('mfv_stoplb_tau001000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197193),
    MCSample('mfv_stoplb_tau030000um_M1000_2017', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200668),
    MCSample('mfv_stoplb_tau000100um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199921),
    MCSample('mfv_stoplb_tau000300um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195189),
    MCSample('mfv_stoplb_tau010000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100156),
    MCSample('mfv_stoplb_tau001000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197902),
    MCSample('mfv_stoplb_tau030000um_M1200_2017', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200464),
    MCSample('mfv_stoplb_tau000100um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199322),
    MCSample('mfv_stoplb_tau000300um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200304),
    MCSample('mfv_stoplb_tau010000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98900),
    MCSample('mfv_stoplb_tau001000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196297),
    MCSample('mfv_stoplb_tau030000um_M1400_2017', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198644),
    MCSample('mfv_stoplb_tau000100um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 202021),
    MCSample('mfv_stoplb_tau000300um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199079),
    MCSample('mfv_stoplb_tau010000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98745),
    MCSample('mfv_stoplb_tau001000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98921),
    MCSample('mfv_stoplb_tau030000um_M1600_2017', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100284),
    MCSample('mfv_stoplb_tau000100um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199639),
    MCSample('mfv_stoplb_tau000300um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200792),
    MCSample('mfv_stoplb_tau010000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 101386),
    MCSample('mfv_stoplb_tau001000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98858),
    MCSample('mfv_stoplb_tau030000um_M1800_2017', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100172),
    MCSample('mfv_stoplb_tau000100um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198760),
    MCSample('mfv_stoplb_tau000300um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198899),
    MCSample('mfv_stoplb_tau010000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199948),
    MCSample('mfv_stoplb_tau001000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196687),
    MCSample('mfv_stoplb_tau030000um_M0200_2017', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199267),
    MCSample('mfv_stoplb_tau000100um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198231),
    MCSample('mfv_stoplb_tau000300um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198170),
    MCSample('mfv_stoplb_tau010000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199832),
    MCSample('mfv_stoplb_tau001000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200296),
    MCSample('mfv_stoplb_tau030000um_M0300_2017', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200170),
    MCSample('mfv_stoplb_tau000100um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197597),
    MCSample('mfv_stoplb_tau000300um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200230),
    MCSample('mfv_stoplb_tau010000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198737),
    MCSample('mfv_stoplb_tau001000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197003),
    MCSample('mfv_stoplb_tau030000um_M0400_2017', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198930),
    MCSample('mfv_stoplb_tau000100um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201812),
    MCSample('mfv_stoplb_tau000300um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201839),
    MCSample('mfv_stoplb_tau010000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197409),
    MCSample('mfv_stoplb_tau001000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195368),
    MCSample('mfv_stoplb_tau030000um_M0600_2017', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200005),
    MCSample('mfv_stoplb_tau000100um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198566),
    MCSample('mfv_stoplb_tau000300um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197615),
    MCSample('mfv_stoplb_tau010000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98799),
    MCSample('mfv_stoplb_tau001000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197479),
    MCSample('mfv_stoplb_tau030000um_M0800_2017', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201690),
]

mfv_stopld_samples_2017 = [
    MCSample('mfv_stopld_tau000100um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199076),
    MCSample('mfv_stopld_tau000300um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198992),
    MCSample('mfv_stopld_tau010000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98679),
    MCSample('mfv_stopld_tau001000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198608),
    MCSample('mfv_stopld_tau030000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 199499),
    MCSample('mfv_stopld_tau000100um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198263),
    MCSample('mfv_stopld_tau000300um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 0),
    MCSample('mfv_stopld_tau010000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100349),
    MCSample('mfv_stopld_tau001000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201191),
    MCSample('mfv_stopld_tau030000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200851),
    MCSample('mfv_stopld_tau000100um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198812),
    MCSample('mfv_stopld_tau000300um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 194591),
    MCSample('mfv_stopld_tau010000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98583),
    MCSample('mfv_stopld_tau001000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198538),
    MCSample('mfv_stopld_tau030000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200714),
    MCSample('mfv_stopld_tau000100um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201051),
    MCSample('mfv_stopld_tau000300um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196540),
    MCSample('mfv_stopld_tau010000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100274),
    MCSample('mfv_stopld_tau001000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99126),
    MCSample('mfv_stopld_tau030000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100345),
    MCSample('mfv_stopld_tau000100um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200828),
    MCSample('mfv_stopld_tau000300um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198147),
    MCSample('mfv_stopld_tau010000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99667),
    MCSample('mfv_stopld_tau001000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 101005),
    MCSample('mfv_stopld_tau030000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99787),
    MCSample('mfv_stopld_tau000100um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201843),
    MCSample('mfv_stopld_tau000300um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199789),
    MCSample('mfv_stopld_tau010000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197403),
    MCSample('mfv_stopld_tau001000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198275),
    MCSample('mfv_stopld_tau030000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198511),
    MCSample('mfv_stopld_tau000100um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197379),
    MCSample('mfv_stopld_tau000300um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197934),
    MCSample('mfv_stopld_tau010000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197990),
    MCSample('mfv_stopld_tau001000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199705),
    MCSample('mfv_stopld_tau030000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199931),
    MCSample('mfv_stopld_tau000100um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 202735),
    MCSample('mfv_stopld_tau000300um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199890),
    MCSample('mfv_stopld_tau010000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201845),
    MCSample('mfv_stopld_tau001000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197130),
    MCSample('mfv_stopld_tau030000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198731),
    MCSample('mfv_stopld_tau000100um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203406),
    MCSample('mfv_stopld_tau000300um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199321),
    MCSample('mfv_stopld_tau010000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195818),
    MCSample('mfv_stopld_tau001000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203302),
    MCSample('mfv_stopld_tau030000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199944),
    MCSample('mfv_stopld_tau000100um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200077),
    MCSample('mfv_stopld_tau000300um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200814),
    MCSample('mfv_stopld_tau010000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99313),
    MCSample('mfv_stopld_tau001000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200829),
    MCSample('mfv_stopld_tau030000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200140),
]

#HToSSTobbbb_samples_2017 = [
    #MCSample('ggHToSSTobbbb_tau1000mm_M15_2017', '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 159693),
    #MCSample('ggHToSSTobbbb_tau100mm_M15_2017',  '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 159747),
    #MCSample('ggHToSSTobbbb_tau10mm_M15_2017',   '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 157205),
    #MCSample('ggHToSSTobbbb_tau1mm_M15_2017',    '/ggH_HToSSTobbbb_MH-125_MS-15_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 168529),
    #MCSample('ggHToSSTobbbb_tau1000mm_M40_2017', '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 168492),
    #MCSample('ggHToSSTobbbb_tau100mm_M40_2017',  '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 161541),
    #MCSample('ggHToSSTobbbb_tau10mm_M40_2017',   '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 174041),
    #MCSample('ggHToSSTobbbb_tau1mm_M40_2017',    '/ggH_HToSSTobbbb_MH-125_MS-40_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 155202),
    #MCSample('ggHToSSTobbbb_tau1000mm_M55_2017', '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 200804),
    #MCSample('ggHToSSTobbbb_tau100mm_M55_2017',  '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 174229),
    #MCSample('ggHToSSTobbbb_tau10mm_M55_2017',   '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 163136),
    #MCSample('ggHToSSTobbbb_tau1mm_M55_2017',    '/ggH_HToSSTobbbb_MH-125_MS-55_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 182247),
#]

ZHToSSTodddd_samples_2017 = [ 
    MCSample('ZHToSSTodddd_tau100um_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49121), 
    MCSample('ZHToSSTodddd_tau300um_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau1mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau3mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau10mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau30mm_M15_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 

    MCSample('ZHToSSTodddd_tau100um_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau300um_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau1mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49996), 
    MCSample('ZHToSSTodddd_tau10mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
    MCSample('ZHToSSTodddd_tau30mm_M40_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 

    MCSample('ZHToSSTodddd_tau100um_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau300um_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau1mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau3mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('ZHToSSTodddd_tau10mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('ZHToSSTodddd_tau30mm_M55_2017', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
]

WplusHToSSTodddd_samples_2017 = [
    MCSample('WplusHToSSTodddd_tau100um_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WplusHToSSTodddd_tau300um_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49000), 
    MCSample('WplusHToSSTodddd_tau1mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau3mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WplusHToSSTodddd_tau30mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    
    #No WplusHToSSTodddd_tau100um_M40_2017
    MCSample('WplusHToSSTodddd_tau300um_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49996), 
    MCSample('WplusHToSSTodddd_tau1mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau3mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WplusHToSSTodddd_tau30mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
    #No WplusHToSSTodddd_tau10mm_M55_2017
]

WminusHToSSTodddd_samples_2017 = [
    #No WminusHToSSTodddd_tau100um_M15_2017 
    #No WminusHToSSTodddd_tau300um_M40_2017 
    MCSample('WminusHToSSTodddd_tau1mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau3mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau10mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WminusHToSSTodddd_tau30mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 

    #No WminusHToSSTodddd_tau100um_M40_2017 
    MCSample('WminusHToSSTodddd_tau300um_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau1mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WminusHToSSTodddd_tau3mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau10mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WminusHToSSTodddd_tau30mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
   
    #No WminusHToSSTodddd_tau100um_M55_2017 
    MCSample('WminusHToSSTodddd_tau300um_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47995), 
    MCSample('WminusHToSSTodddd_tau1mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WminusHToSSTodddd_tau3mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49992), 
    MCSample('WminusHToSSTodddd_tau10mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49994), 
    MCSample('WminusHToSSTodddd_tau30mm_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49993), 
]

ggHToSSTodddd_samples_2017 = [
    #MCSample('ggHToSSTodddd_tau1000mm_M15_2017', '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 164515),
    #MCSample('ggHToSSTodddd_tau100mm_M15_2017',  '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 160691),
    #MCSample('ggHToSSTodddd_tau10mm_M15_2017',   '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 202418),
    #MCSample('ggHToSSTodddd_tau1mm_M15_2017',    '/ggH_HToSSTodddd_MH-125_MS-15_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 170288),
    #MCSample('ggHToSSTodddd_tau1000mm_M40_2017', '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 200772),
    #MCSample('ggHToSSTodddd_tau100mm_M40_2017',  '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 178325),
    #MCSample('ggHToSSTodddd_tau10mm_M40_2017',   '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 191158),
    #MCSample('ggHToSSTodddd_tau1mm_M40_2017',    '/ggH_HToSSTodddd_MH-125_MS-40_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 176899),
    #MCSample('ggHToSSTodddd_tau1000mm_M55_2017', '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1000_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 233111),
    #MCSample('ggHToSSTodddd_tau100mm_M55_2017',  '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 186454),
    #MCSample('ggHToSSTodddd_tau10mm_M55_2017',   '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 171704),
    MCSample('ggHToSSTodddd_tau1mm_M55_2017',    '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_pT75_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 186554),

]

ggHToSSTo4l_samples_2017 = [
    MCSample('ggHToSSTo4l_tau1mm_M350_2017', '/ggH_HToSSTo4l_lowctau_MH-800_MS-350_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49643),
]


#all_signal_samples_2017 = mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017 + mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 + HToSSTobbbb_samples_2017 + HToSSTodddd_samples_2017 + mfv_splitSUSY_samples_2017
all_signal_samples_2017 = mfv_stoplb_samples_2017 + mfv_stopld_samples_2017 #+ ZHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 
#all_signal_samples_2017 = mfv_selected_signal_samples_2017 + mfv_selected_stopdbardbar_samples_2017 + mfv_selected_stopbbarbbar_samples_2017+ ggHToSSTodddd_samples_2017  
#all_signal_samples_2017 = ZHToSSTodddd_samples_2017 + WplusHToSSTodddd_samples_2017 + WminusHToSSTodddd_samples_2017 
#all_signal_samples_2017 = WplusHToSSTodddd_samples_2017 

splitSUSY_samples_2017 = mfv_splitSUSY_samples_2017

########
# 2018 MC
########

qcd_samples_2018 = [
    MCSample('qcdht0200_2018', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 22841038, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0200ext_2018', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1_ext1-v1/AODSIM', 34740016, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0300_2018', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 55198123, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    MCSample('qcdht0500_2018', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 58437786, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0700_2018', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 47725353, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    MCSample('qcdht1000_2018', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 15685044, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    MCSample('qcdht1500_2018', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 10615310, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    MCSample('qcdht2000_2018', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',   4532754, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    ]

# need to make these MiniAODv2 
qcd_lep_samples_2018 = [
    MCSample('qcdmupt15_2018',  '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    17392472, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
    MCSample('qcdempt015_2018', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    7899865, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.324e6),
    MCSample('qcdempt020_2018', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',    14328846, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, EM enriched', color=801, syst_frac=0.20, xsec=4.896e6),
    MCSample('qcdempt030_2018', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    8574589, nice='QCD,  30 < #hat{p}_{T} <  50 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.447e6),
    MCSample('qcdempt050_2018', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    10524400, nice='QCD,  50 < #hat{p}_{T} <  80 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.988e6),
    MCSample('qcdempt080_2018', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    9468372, nice='QCD,  80 < #hat{p}_{T} < 120 GeV, EM enriched', color=801, syst_frac=0.20, xsec=3.675e5),
    MCSample('qcdempt120_2018', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   9677904, nice='QCD, 120 < #hat{p}_{T} < 170 GeV, EM enriched', color=801, syst_frac=0.20, xsec=6.659e4),
    MCSample('qcdempt170_2018', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   3714642, nice='QCD, 170 < #hat{p}_{T} < 300 GeV, EM enriched', color=801, syst_frac=0.20, xsec=1.662e4),
    MCSample('qcdempt300_2018', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   2215994, nice='QCD, #hat{p}_{T} > 300 GeV, EM enriched',       color=801, syst_frac=0.20, xsec=1104.0),
    MCSample('qcdbctoept015_2018', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      16549971, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.862e5),
    MCSample('qcdbctoept020_2018', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      14061214, nice='QCD,  20 < #hat{p}_{T} <  30 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.038e5),
    MCSample('qcdbctoept030_2018', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      15358726, nice='QCD,  30 < #hat{p}_{T} <  80 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.623e5),
    MCSample('qcdbctoept080_2018', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     15186397, nice='QCD,  80 < #hat{p}_{T} < 170 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.37e4),
    MCSample('qcdbctoept170_2018', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',    15735786, nice='QCD, 170 < #hat{p}_{T} < 250 GeV, HF electrons', color=801, syst_frac=0.20, xsec=2.125e3),
    MCSample('qcdbctoept250_2018', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',    15767690, nice='QCD, #hat{p}_{T} > 250 GeV, HF electrons',       color=801, syst_frac=0.20, xsec=562.5),

]

ttbar_samples_2018 = [
    MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
    MCSample('ttbar_lep_2018',            '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',             146010000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_2018', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',             478982000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_2018',         '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',             343248000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]

bjet_samples_2018 = []

leptonic_samples_2018 = [
    #MCSample('wjetstolnu_2018',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',          82442496, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=5.294e4),
    #MCSample('wjetstolnu_ext_2018',       '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/MINIAODSIM',     79648036, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=5.294e4),
    MCSample('wjetstolnu_0j_2018',    '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      172138190, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=52.780e3),   
    MCSample('wjetstolnu_1j_2018',    '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',      184564696, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=8.832e3),   
    MCSample('wjetstolnu_2j_2018',    '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',      94925903, nice='$W + jets #rightarrow l#nu$', color=  9, syst_frac=0.10, xsec=3.276e3),   
    MCSample('dyjetstollM10_2018',    '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 99288125, nice='$DY + jets #rightarrow ll$, $10 < M < 50$ \\GeV', color= 29, syst_frac=0.10, xsec=1.589e4),
    MCSample('dyjetstollM50_2018',    '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',     96233328, nice='$DY + jets #rightarrow ll$, $M > 50$ \\GeV', color= 32, syst_frac=0.10, xsec=5.398e3),
]

met_samples_2018 = [
    #MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
]

# diboson_samples_2018 = [
#     MCSample('ww_2018',    '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',          15679000, nice='WW', color= 32, syst_frac=0.10, xsec=7.587e+01),
#     MCSample('wz_2018',    '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',           7988000, nice='WZ', color= 32, syst_frac=0.10, xsec=2.756e+01),
#     MCSample('zz_2018',    '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',           4000000, nice='ZZ', color= 32, syst_frac=0.10, xsec=1.214e+01),
# ]

diboson_samples_2018 = [
    MCSample('ww_2018',    '/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',          15679000, nice='WW', color= 32, syst_frac=0.10, xsec=7.587e+01),
    MCSample('wz_2018',    '/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',           7988000, nice='WZ', color= 32, syst_frac=0.10, xsec=2.756e+01),
    MCSample('zz_2018',    '/ZZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',           3526000, nice='ZZ', color= 32, syst_frac=0.10, xsec=1.214e+01),
]

Zvv_samples_2018 = [
    MCSample('zjetstonunuht0100_2018', '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 29116252, nice='Z + jets #rightarrow #nu #nu 100 < H_{T} < 200 GeV', color=1, syst_frac=0.20, xsec=302.8),
    MCSample('zjetstonunuht0200_2018', '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 23570033, nice='Z + jets #rightarrow #nu #nu 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=92.59),
    MCSample('zjetstonunuht0400_2018', '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 20718934, nice='Z + jets #rightarrow #nu #nu 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=13.18),
    MCSample('zjetstonunuht0600_2018', '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',  5968910, nice='Z + jets #rightarrow #nu #nu 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=3.257),
    MCSample('zjetstonunuht0800_2018', '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 2144959, nice='Z + jets #rightarrow #nu #nu 800 < H_{T} < 1200 GeV', color=1, syst_frac=0.20, xsec=1.49),
    MCSample('zjetstonunuht1200_2018', '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM', 381695, nice='Z + jets #rightarrow #nu #nu 1200 < H_{T} < 2500 GeV', color=1, syst_frac=0.20, xsec=0.3419),
    MCSample('zjetstonunuht2500_2018', '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v1/AODSIM',  268224, nice='Z + jets #rightarrow #nu #nu H_{T} > 2500 GeV', color=1, syst_frac=0.20, xsec=0.005146),
    ]

mfv_splitSUSY_samples_2018 = []


mfv_signal_samples_2018 = [
    MCSample('mfv_neu_tau000100um_M0200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 150000),
    MCSample('mfv_neu_tau010000um_M0200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0300_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0300_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 150000),
    MCSample('mfv_neu_tau001000um_M0300_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 43000),
    MCSample('mfv_neu_tau010000um_M0300_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0300_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 150000),
    MCSample('mfv_neu_tau001000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 43000),
    MCSample('mfv_neu_tau010000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 30000),
    MCSample('mfv_neu_tau030000um_M0400_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 60000),
    MCSample('mfv_neu_tau000100um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau001000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 27000),
    MCSample('mfv_neu_tau010000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 16000),
    MCSample('mfv_neu_tau030000um_M0600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 25000),
    MCSample('mfv_neu_tau000100um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 73000),
    MCSample('mfv_neu_tau001000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 24000),
    MCSample('mfv_neu_tau010000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 14000),
    MCSample('mfv_neu_tau030000um_M0800_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 21000),
    MCSample('mfv_neu_tau000100um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 62000),
    MCSample('mfv_neu_tau001000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 22000),
    MCSample('mfv_neu_tau010000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 13000),
    MCSample('mfv_neu_tau030000um_M1200_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 18000),
    MCSample('mfv_neu_tau000100um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 59000),
    MCSample('mfv_neu_tau001000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 21000),
    MCSample('mfv_neu_tau010000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 12000),
    MCSample('mfv_neu_tau030000um_M1600_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 17000),
    MCSample('mfv_neu_tau000100um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_neu_tau000300um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 58000),
    MCSample('mfv_neu_tau001000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 20000),
    MCSample('mfv_neu_tau010000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 12000),
    MCSample('mfv_neu_tau030000um_M3000_2018', '/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 15000),
]

mfv_selected_signal_samples_2018 = [mfv_signal_samples_2018[19], mfv_signal_samples_2018[20]] #mfv_signal_samples_2018[0:24]

mfv_stopdbardbar_samples_2018 = [
    MCSample('mfv_stopdbardbar_tau000100um_M0200_2018', '/StopStopbarTo2Dbar2D_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0200_2018', '/StopStopbarTo2Dbar2D_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0200_2018', '/StopStopbarTo2Dbar2D_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0200_2018', '/StopStopbarTo2Dbar2D_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0200_2018', '/StopStopbarTo2Dbar2D_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',   44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0300_2018', '/StopStopbarTo2Dbar2D_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0300_2018', '/StopStopbarTo2Dbar2D_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',  197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0300_2018', '/StopStopbarTo2Dbar2D_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',    50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0300_2018', '/StopStopbarTo2Dbar2D_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0300_2018', '/StopStopbarTo2Dbar2D_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',   44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  197000),
    MCSample('mfv_stopdbardbar_tau001000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    50000),
    MCSample('mfv_stopdbardbar_tau010000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   30000),
    MCSample('mfv_stopdbardbar_tau030000um_M0400_2018', '/StopStopbarTo2Dbar2D_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   44000),
    MCSample('mfv_stopdbardbar_tau000100um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  140000),
    MCSample('mfv_stopdbardbar_tau001000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',    36000),
    MCSample('mfv_stopdbardbar_tau010000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',   18000),
    MCSample('mfv_stopdbardbar_tau030000um_M0600_2018', '/StopStopbarTo2Dbar2D_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   29000),
    MCSample('mfv_stopdbardbar_tau000100um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  200000),
    MCSample('mfv_stopdbardbar_tau000300um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  116000),
    MCSample('mfv_stopdbardbar_tau001000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',    32000),
    MCSample('mfv_stopdbardbar_tau010000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   17000),
    MCSample('mfv_stopdbardbar_tau030000um_M0800_2018', '/StopStopbarTo2Dbar2D_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   26000),
    MCSample('mfv_stopdbardbar_tau000100um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopdbardbar_tau000300um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 99000),
    MCSample('mfv_stopdbardbar_tau001000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   29000),
    MCSample('mfv_stopdbardbar_tau010000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  15000),
    MCSample('mfv_stopdbardbar_tau030000um_M1200_2018', '/StopStopbarTo2Dbar2D_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',  23000),
    MCSample('mfv_stopdbardbar_tau000100um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopdbardbar_tau000300um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 89000),
    MCSample('mfv_stopdbardbar_tau001000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   28000),
    MCSample('mfv_stopdbardbar_tau010000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  15000),
    MCSample('mfv_stopdbardbar_tau030000um_M1600_2018', '/StopStopbarTo2Dbar2D_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  23000),
    MCSample('mfv_stopdbardbar_tau000100um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 201000),
    MCSample('mfv_stopdbardbar_tau000300um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 85000),
    MCSample('mfv_stopdbardbar_tau001000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',   28000),
    MCSample('mfv_stopdbardbar_tau010000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  13000),
    MCSample('mfv_stopdbardbar_tau030000um_M3000_2018', '/StopStopbarTo2Dbar2D_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM',  20000),
]

mfv_selected_stopdbardbar_samples_2018 = [mfv_stopdbardbar_samples_2018[21], mfv_stopdbardbar_samples_2018[22]] #mfv_stopdbardbar_samples_2018[0:24]

mfv_stopbbarbbar_samples_2018 = [
    MCSample('mfv_stopbbarbbar_tau000100um_M0200_2018', '/StopStopbarTo2Bbar2B_M-200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0200_2018', '/StopStopbarTo2Bbar2B_M-200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0200_2018', '/StopStopbarTo2Bbar2B_M-200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0200_2018', '/StopStopbarTo2Bbar2B_M-200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0200_2018', '/StopStopbarTo2Bbar2B_M-200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0300_2018', '/StopStopbarTo2Bbar2B_M-300_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0300_2018', '/StopStopbarTo2Bbar2B_M-300_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0300_2018', '/StopStopbarTo2Bbar2B_M-300_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0300_2018', '/StopStopbarTo2Bbar2B_M-300_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0300_2018', '/StopStopbarTo2Bbar2B_M-300_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0400_2018', '/StopStopbarTo2Bbar2B_M-400_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0400_2018', '/StopStopbarTo2Bbar2B_M-400_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0400_2018', '/StopStopbarTo2Bbar2B_M-400_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0400_2018', '/StopStopbarTo2Bbar2B_M-400_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 30000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0400_2018', '/StopStopbarTo2Bbar2B_M-400_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 44000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0600_2018', '/StopStopbarTo2Bbar2B_M-600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 201000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0600_2018', '/StopStopbarTo2Bbar2B_M-600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 140000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0600_2018', '/StopStopbarTo2Bbar2B_M-600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 36000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0600_2018', '/StopStopbarTo2Bbar2B_M-600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 18000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0600_2018', '/StopStopbarTo2Bbar2B_M-600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 29000),
    MCSample('mfv_stopbbarbbar_tau000100um_M0800_2018', '/StopStopbarTo2Bbar2B_M-800_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M0800_2018', '/StopStopbarTo2Bbar2B_M-800_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 116000),
    MCSample('mfv_stopbbarbbar_tau001000um_M0800_2018', '/StopStopbarTo2Bbar2B_M-800_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 32000),
    MCSample('mfv_stopbbarbbar_tau010000um_M0800_2018', '/StopStopbarTo2Bbar2B_M-800_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 17000),
    MCSample('mfv_stopbbarbbar_tau030000um_M0800_2018', '/StopStopbarTo2Bbar2B_M-800_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 26000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1200_2018', '/StopStopbarTo2Bbar2B_M-1200_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1200_2018', '/StopStopbarTo2Bbar2B_M-1200_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1200_2018', '/StopStopbarTo2Bbar2B_M-1200_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 29000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1200_2018', '/StopStopbarTo2Bbar2B_M-1200_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1200_2018', '/StopStopbarTo2Bbar2B_M-1200_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 23000),
    MCSample('mfv_stopbbarbbar_tau000100um_M1600_2018', '/StopStopbarTo2Bbar2B_M-1600_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 201000),
    MCSample('mfv_stopbbarbbar_tau000300um_M1600_2018', '/StopStopbarTo2Bbar2B_M-1600_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 89000),
    MCSample('mfv_stopbbarbbar_tau001000um_M1600_2018', '/StopStopbarTo2Bbar2B_M-1600_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 28000),
    MCSample('mfv_stopbbarbbar_tau010000um_M1600_2018', '/StopStopbarTo2Bbar2B_M-1600_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 15000),
    MCSample('mfv_stopbbarbbar_tau030000um_M1600_2018', '/StopStopbarTo2Bbar2B_M-1600_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 23000),
    MCSample('mfv_stopbbarbbar_tau000100um_M3000_2018', '/StopStopbarTo2Bbar2B_M-3000_CTau-100um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200000),
    MCSample('mfv_stopbbarbbar_tau000300um_M3000_2018', '/StopStopbarTo2Bbar2B_M-3000_CTau-300um_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 88000),
    MCSample('mfv_stopbbarbbar_tau001000um_M3000_2018', '/StopStopbarTo2Bbar2B_M-3000_CTau-1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 28000),
    MCSample('mfv_stopbbarbbar_tau010000um_M3000_2018', '/StopStopbarTo2Bbar2B_M-3000_CTau-10mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 13000),
    MCSample('mfv_stopbbarbbar_tau030000um_M3000_2018', '/StopStopbarTo2Bbar2B_M-3000_CTau-30mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 20000),
]

mfv_selected_stopbbarbbar_samples_2018 = [mfv_stopbbarbbar_samples_2018[21], mfv_stopbbarbbar_samples_2018[22]] #mfv_stopbbarbbar_samples_2018[0:24]

mfv_stoplb_samples_2018 = [
    MCSample('mfv_stoplb_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198986),
    MCSample('mfv_stoplb_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199542),
    MCSample('mfv_stoplb_tau001000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198269),
    MCSample('mfv_stoplb_tau010000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198147),
    MCSample('mfv_stoplb_tau030000um_M0200_2018', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197780),
    MCSample('mfv_stoplb_tau000100um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198372),
    MCSample('mfv_stoplb_tau000300um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 203023),
    MCSample('mfv_stoplb_tau001000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197602),
    MCSample('mfv_stoplb_tau010000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196154),
    MCSample('mfv_stoplb_tau030000um_M0300_2018', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196763),
    MCSample('mfv_stoplb_tau000100um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200505),
    MCSample('mfv_stoplb_tau000300um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200842),
    MCSample('mfv_stoplb_tau001000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199860),
    MCSample('mfv_stoplb_tau010000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198963),
    MCSample('mfv_stoplb_tau030000um_M0400_2018', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198368),
    MCSample('mfv_stoplb_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198211),
    MCSample('mfv_stoplb_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199368),
    MCSample('mfv_stoplb_tau001000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196032),
    MCSample('mfv_stoplb_tau010000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197845),
    MCSample('mfv_stoplb_tau030000um_M0600_2018', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201533),
    MCSample('mfv_stoplb_tau000100um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202319),
    MCSample('mfv_stoplb_tau000300um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200738),
    MCSample('mfv_stoplb_tau001000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202348),    
    MCSample('mfv_stoplb_tau010000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99747),
    MCSample('mfv_stoplb_tau030000um_M0800_2018', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199087),
    MCSample('mfv_stoplb_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202114),
    MCSample('mfv_stoplb_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196665),
    MCSample('mfv_stoplb_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196748),    
    MCSample('mfv_stoplb_tau010000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99062),
    MCSample('mfv_stoplb_tau030000um_M1000_2018', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199216),
    MCSample('mfv_stoplb_tau000100um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197949),
    MCSample('mfv_stoplb_tau000300um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198241),
    MCSample('mfv_stoplb_tau001000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199473),   
    MCSample('mfv_stoplb_tau010000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98201),
    MCSample('mfv_stoplb_tau030000um_M1200_2018', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199458),
    MCSample('mfv_stoplb_tau000100um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199272),
    MCSample('mfv_stoplb_tau000300um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200098),
    MCSample('mfv_stoplb_tau001000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200807),   
    MCSample('mfv_stoplb_tau010000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99970),
    MCSample('mfv_stoplb_tau030000um_M1400_2018', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200816),
    MCSample('mfv_stoplb_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199366),
    MCSample('mfv_stoplb_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202756),
    MCSample('mfv_stoplb_tau001000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99806),    
    MCSample('mfv_stoplb_tau010000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 101586),
    MCSample('mfv_stoplb_tau030000um_M1600_2018', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100560),
    MCSample('mfv_stoplb_tau000100um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200523),
    MCSample('mfv_stoplb_tau000300um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199868),
    MCSample('mfv_stoplb_tau001000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100171),   
    MCSample('mfv_stoplb_tau010000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 101211),
    MCSample('mfv_stoplb_tau030000um_M1800_2018', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100346),
]

mfv_stopld_samples_2018 = [
    MCSample('mfv_stopld_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197970),
    MCSample('mfv_stopld_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198800),
    MCSample('mfv_stopld_tau001000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200411),   
    MCSample('mfv_stopld_tau010000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199856),
    MCSample('mfv_stopld_tau030000um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202558),
    MCSample('mfv_stopld_tau000100um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196635),
    MCSample('mfv_stopld_tau000300um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198796),
    MCSample('mfv_stopld_tau001000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200543),   
    MCSample('mfv_stopld_tau010000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197769),
    MCSample('mfv_stopld_tau030000um_M0300_2018', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198495),
    MCSample('mfv_stopld_tau000100um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201643),
    MCSample('mfv_stopld_tau000300um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197079),
    MCSample('mfv_stopld_tau001000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200098),   
    MCSample('mfv_stopld_tau010000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198270),
    MCSample('mfv_stopld_tau030000um_M0400_2018', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 203160),
    MCSample('mfv_stopld_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198964),
    MCSample('mfv_stopld_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198408),
    MCSample('mfv_stopld_tau001000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199759),   
    MCSample('mfv_stopld_tau010000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200404),
    MCSample('mfv_stopld_tau030000um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200030),
    MCSample('mfv_stopld_tau000100um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197872),
    MCSample('mfv_stopld_tau000300um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202036),
    MCSample('mfv_stopld_tau001000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199217),   
    MCSample('mfv_stopld_tau010000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100507),
    MCSample('mfv_stopld_tau030000um_M0800_2018', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197136),
    MCSample('mfv_stopld_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 198858),
    MCSample('mfv_stopld_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199006),
    MCSample('mfv_stopld_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196285),   
    MCSample('mfv_stopld_tau010000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98581),
    MCSample('mfv_stopld_tau030000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199499),
    MCSample('mfv_stopld_tau000100um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 195354),
    MCSample('mfv_stopld_tau000300um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 195508,),
    MCSample('mfv_stopld_tau001000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200103),   
    MCSample('mfv_stopld_tau010000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98617),
    MCSample('mfv_stopld_tau030000um_M1200_2018', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200964),
    MCSample('mfv_stopld_tau000100um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 200045),
    MCSample('mfv_stopld_tau000300um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202529),
    MCSample('mfv_stopld_tau001000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 196708),   
    MCSample('mfv_stopld_tau010000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100228),
    MCSample('mfv_stopld_tau030000um_M1400_2018', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201992),
    MCSample('mfv_stopld_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 201300),
    MCSample('mfv_stopld_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 197421),
    MCSample('mfv_stopld_tau001000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 100838),  
    MCSample('mfv_stopld_tau010000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99387),
    MCSample('mfv_stopld_tau030000um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 97752),
    MCSample('mfv_stopld_tau000100um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 202746),
    MCSample('mfv_stopld_tau000300um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 199924),
    MCSample('mfv_stopld_tau001000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99515),   
    MCSample('mfv_stopld_tau010000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 99400),
    MCSample('mfv_stopld_tau030000um_M1800_2018', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 98449),
]
# private samples 
# mfv_stopld_samples_2018 = [
#     MCSample('mfv_stopld_tau000100um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 4089),
#     MCSample('mfv_stopld_tau000300um_M0200_2018', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 4050),
#     MCSample('mfv_stopld_tau000100um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2821),
#     MCSample('mfv_stopld_tau000300um_M0600_2018', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2802),
#     MCSample('mfv_stopld_tau000100um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2579),
#     MCSample('mfv_stopld_tau000300um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2604),
#    # MCSample('mfv_stopld_tau001000um_M1000_2018', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2555),
#     MCSample('mfv_stopld_tau000100um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2472),
#     MCSample('mfv_stopld_tau000300um_M1600_2018', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/awarden-RunIISummer20UL18_MiniAOD-dd00e8e5190104a7aafdc4fba9805483/USER', 2478),
# ]

ZHToSSTodddd_samples_2018 = [ 
    
    MCSample('ZHToSSTodddd_tau300um_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49995), 
    MCSample('ZHToSSTodddd_tau1mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999), 
]

WplusHToSSTodddd_samples_2018 = [
    MCSample('WplusHToSSTodddd_tau300um_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994),
]

WminusHToSSTodddd_samples_2018 = [
    MCSample('WminusHToSSTodddd_tau300um_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49992), 
    MCSample('WminusHToSSTodddd_tau1mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49995),
]

ggHToSSTodddd_samples_2018 = [
    MCSample('ggHToSSTodddd_tau1mm_M55_2018',   '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',   546940),
    #MCSample('ggHToSSTodddd_tau10mm_M55_2018',  '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',  525760),
    #MCSample('ggHToSSTodddd_tau100mm_M55_2018', '/ggH_HToSSTodddd_MH-125_MS-55_ctauS-100_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 506379),
]

#all_signal_samples_2018 = mfv_splitSUSY_samples_2018
all_signal_samples_2018 = mfv_stoplb_samples_2018 + mfv_stopld_samples_2018
#all_signal_samples_2018 =  mfv_selected_signal_samples_2018 + mfv_selected_stopdbardbar_samples_2018 + mfv_selected_stopbbarbbar_samples_2018 + ggHToSSTodddd_samples_2018  
#all_signal_samples_2018 = ZHToSSTodddd_samples_2018 + WplusHToSSTodddd_samples_2018 + WminusHToSSTodddd_samples_2018 
########
# data
########

BTagCSV_data_samples_20161 = [
    DataSample('BTagCSV20161B', '/BTagCSV/Run2016B-21Feb2020_ver2_UL2016_HIPM-v1/MINIAOD'),
    DataSample('BTagCSV20161C', '/BTagCSV/Run2016C-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
    DataSample('BTagCSV20161D', '/BTagCSV/Run2016D-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
    DataSample('BTagCSV20161F', '/BTagCSV/Run2016F-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
]

DisplacedJet_data_samples_20161 = [
    DataSample('DisplacedJet20161B', '/DisplacedJet/Run2016B-21Feb2020_ver2_UL2016_HIPM-v1/MINIAOD'),
    DataSample('DisplacedJet20161C', '/DisplacedJet/Run2016C-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
    DataSample('DisplacedJet20161D', '/DisplacedJet/Run2016D-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
    DataSample('DisplacedJet20161E', '/DisplacedJet/Run2016E-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
    DataSample('DisplacedJet20161F', '/DisplacedJet/Run2016F-21Feb2020_UL2016_HIPM-v1/MINIAOD'),
]

Lepton_data_samples_20161 = [
    #DataSample('SingleMuon20161B1', '/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'), #FIXME failed TM ntupling
    DataSample('SingleMuon20161B', '/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161C',  '/SingleMuon/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161D',  '/SingleMuon/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161E',  '/SingleMuon/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20161F',  '/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161B1', '/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161B2', '/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161C',  '/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161D',  '/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161E',  '/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2-v5/MINIAOD'),
    DataSample('SingleElectron20161F',  '/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
]

BTagCSV_data_samples_20162 = [
    DataSample('BTagCSV2016F', '/BTagCSV/Run2016F-21Feb2020_UL2016-v1/MINIAOD'),
    DataSample('BTagCSV2016G', '/BTagCSV/Run2016G-21Feb2020_UL2016-v1/MINIAOD'),
    DataSample('BTagCSV2016H', '/BTagCSV/Run2016H-21Feb2020_UL2016-v1/MINIAOD'),
]

DisplacedJet_data_samples_20162 = [
    DataSample('DisplacedJet2016F', '/DisplacedJet/Run2016F-21Feb2020_UL2016-v1/MINIAOD'),
    DataSample('DisplacedJet2016G', '/DisplacedJet/Run2016G-21Feb2020_UL2016-v1/MINIAOD'),
    DataSample('DisplacedJet2016H', '/DisplacedJet/Run2016H-21Feb2020_UL2016-v1/MINIAOD'),
]

Lepton_data_samples_20162 = [
    DataSample('SingleMuon20162F', '/SingleMuon/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20162G', '/SingleMuon/Run2016G-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon20162H', '/SingleMuon/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20162F', '/SingleElectron/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20162G', '/SingleElectron/Run2016G-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20162H', '/SingleElectron/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'),

]

#auxiliary_data_samples_2017 = [                                                       # in dataset      in json          int lumi avail (/fb)
#    DataSample('MET2017B', '/MET/Run2017B-09Aug2019_UL2017_rsb-v1/AOD'),  
#    DataSample('MET2017C', '/MET/Run2017C-09Aug2019_UL2017_rsb-v1/AOD'),  
#    DataSample('MET2017D', '/MET/Run2017D-09Aug2019_UL2017_rsb-v1/AOD'),  
#    DataSample('MET2017E', '/MET/Run2017E-09Aug2019_UL2017_rsb-v1/AOD'),  
#    DataSample('MET2017F', '/MET/Run2017F-09Aug2019_UL2017_rsb-v1/AOD'),  
#    ]

#FIXME: may need to reorganize how data is loaded for different cases
JetHT_data_samples_2017 = []

BTagCSV_data_samples_2017 = [
    DataSample('BTagCSV2017B', '/BTagCSV/Run2017B-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('BTagCSV2017C', '/BTagCSV/Run2017C-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('BTagCSV2017D', '/BTagCSV/Run2017D-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('BTagCSV2017E', '/BTagCSV/Run2017E-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('BTagCSV2017F', '/BTagCSV/Run2017F-09Aug2019_UL2017-v1/MINIAOD'),
    ]

DisplacedJet_data_samples_2017 = [
    DataSample('DisplacedJet2017C', '/DisplacedJet/Run2017C-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('DisplacedJet2017D', '/DisplacedJet/Run2017D-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('DisplacedJet2017E', '/DisplacedJet/Run2017E-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('DisplacedJet2017F', '/DisplacedJet/Run2017F-09Aug2019_UL2017-v1/MINIAOD'),
    ]

Lepton_data_samples_2017 = [
    # DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    # DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    # DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    # DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    # DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-UL2017_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2017B',     '/SingleMuon/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleMuon2017C',     '/SingleMuon/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleMuon2017D',     '/SingleMuon/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleMuon2017E',     '/SingleMuon/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleMuon2017F',     '/SingleMuon/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
    ]    

#auxiliary_data_samples_2017 = [
#    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
#    ]   Alec commented and replaced with below 

#singleelectron_data_samples_2017 = [
#    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
#] Alec commented and replaced with below

singleelectron_data_samples_2017 = [
    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
]

#Switching data with auxiliary data
#auxiliary_data_samples_2018 = [
#    DataSample('MET2018A', '/MET/Run2018A-12Nov2019_UL2018-v3/AOD'),  
#    DataSample('MET2018B', '/MET/Run2018B-12Nov2019_UL2018-v3/AOD'),  
#    DataSample('MET2018C', '/MET/Run2018C-12Nov2019_UL2018_rsb-v1/AOD'), 
#    DataSample('MET2018D', '/MET/Run2018D-12Nov2019_UL2018_rsb-v2/AOD'), 
#]

#FIXME: may need to reorganize how data is loaded for different cases
#JetHT_data_samples_2018 = [  #Alec commented from here
#    DataSample('SingleMuon2017B', '/SingleMuon/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017C', '/SingleMuon/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017D', '/SingleMuon/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017E', '/SingleMuon/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleMuon2017F', '/SingleMuon/Run2017F-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017B', '/SingleElectron/Run2017B-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017C', '/SingleElectron/Run2017C-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017D', '/SingleElectron/Run2017D-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017E', '/SingleElectron/Run2017E-09Aug2019_UL2017-v1/AOD'),
#    DataSample('SingleElectron2017F', '/SingleElectron/Run2017F-09Aug2019_UL2017_rsb-v2/AOD'),
#] #Alec to here


BTagCSV_data_samples_2018 = [
    DataSample('BTagCSV2018A', '/BTagCSV/Run2018A-15Feb2022_UL2018-v2/MINIAOD'),
    DataSample('BTagCSV2018B', '/BTagCSV/Run2018B-15Feb2022_UL2018-v1/MINIAOD'),
    DataSample('BTagCSV2018C', '/BTagCSV/Run2018C-15Feb2022_UL2018-v1/MINIAOD'),
    ]

DisplacedJet_data_samples_2018 = [
    DataSample('DisplacedJet2018A', '/DisplacedJet/Run2018A-15Feb2022_UL2018-v1/MINIAOD'),
    DataSample('DisplacedJet2018B', '/DisplacedJet/Run2018B-15Feb2022_UL2018-v1/MINIAOD'),
    DataSample('DisplacedJet2018C', '/DisplacedJet/Run2018C-15Feb2022_UL2018-v1/MINIAOD'),
    DataSample('DisplacedJet2018D', '/DisplacedJet/Run2018D-15Feb2022_UL2018-v1/MINIAOD'),
    ]

Lepton_data_samples_2018 = [
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-UL2018_MiniAODv2-v3/MINIAOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-UL2018_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-UL2018_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-UL2018_MiniAODv2-v3/MINIAOD'),
    DataSample('EGamma2018A', '/EGamma/Run2018A-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018B', '/EGamma/Run2018B-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018C', '/EGamma/Run2018C-UL2018_MiniAODv2-v1/MINIAOD'),
    DataSample('EGamma2018D', '/EGamma/Run2018D-UL2018_MiniAODv2-v2/MINIAOD'),
]

# egamma_data_samples_2018 = [
#     DataSample('EGamma2018A', '/EGamma/Run2018A-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018B', '/EGamma/Run2018B-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018C', '/EGamma/Run2018C-12Nov2019_UL2018-v2/AOD'),
#     DataSample('EGamma2018D', '/EGamma/Run2018D-12Nov2019_UL2018-v8/AOD'),
#     ]

########################################################################

registry = SamplesRegistry()

# shortcuts, be careful:
# - can't add data by primary (have the same primary for different datasets)
from functools import partial
_adbp = registry.add_dataset_by_primary
_adbp3 = partial(_adbp, dbs_inst='phys03')

# have to comment out some sets due to repeated samples 
__all__ = [
    'qcd_samples_20161',
    'qcd_samples_20162',
    'qcd_lep_samples_20161',
    'qcd_lep_samples_20162',
    'leptonic_samples_20161',
    'leptonic_samples_20162',
    'BTagCSV_data_samples_20161',
    'BTagCSV_data_samples_20162',
    'DisplacedJet_data_samples_20161',
    'DisplacedJet_data_samples_20162',
    'Lepton_data_samples_20161',
    'Lepton_data_samples_20162',
    'met_samples_20161',
    'met_samples_20162',
    'ttbar_samples_20161',
    'ttbar_samples_20162',
    'diboson_samples_20161',
    'diboson_samples_20162',
    'mfv_signal_samples_20161',
    'mfv_signal_samples_20162',
    'mfv_stopdbardbar_samples_20161',
    'mfv_stopdbardbar_samples_20162',
    'mfv_stopbbarbbar_samples_20161',
    'mfv_stopbbarbbar_samples_20162',
    'mfv_stoplb_samples_20161',
    'mfv_stopld_samples_20161',
    'mfv_stoplb_samples_20162',
    'mfv_stopld_samples_20162',
    'qcd_samples_2017',
    'qcd_lep_samples_2017',
    'ttbar_samples_2017',
    'bjet_samples_2017',
    'leptonic_samples_2017',
    'diboson_samples_2017',
    'met_samples_2017',
    'Zvv_samples_2017',
    'mfv_splitSUSY_samples_2017',
    'mfv_signal_samples_2017',
    'mfv_stopdbardbar_samples_2017',
    'mfv_stopbbarbbar_samples_2017',
    'mfv_stoplb_samples_2017',
    'mfv_stopld_samples_2017',
    'ZHToSSTodddd_samples_20161',
    'WplusHToSSTodddd_samples_20161',
    'WminusHToSSTodddd_samples_20161',
    'ggHToSSTodddd_samples_20161',
    'ZHToSSTodddd_samples_20162',
    'WplusHToSSTodddd_samples_20162',
    'WminusHToSSTodddd_samples_20162',
    'ggHToSSTodddd_samples_20162',
    #'HToSSTobbbb_samples_2017',
    'ggHToSSTodddd_samples_2017',
    'ggHToSSTo4l_samples_2017',
    'ZHToSSTodddd_samples_2017',
    'WplusHToSSTodddd_samples_2017',
    'WminusHToSSTodddd_samples_2017',
    'qcd_samples_2018',
    'qcd_lep_samples_2018',
    'ttbar_samples_2018',
    'bjet_samples_2018',
    'leptonic_samples_2018',
    'met_samples_2018',
    'diboson_samples_2018',
    'Zvv_samples_2018',
    'mfv_splitSUSY_samples_2018',
    'mfv_signal_samples_2018',
    'mfv_stopdbardbar_samples_2018',
    'mfv_stopbbarbbar_samples_2018',
    'mfv_stoplb_samples_2018',
    'mfv_stopld_samples_2018',
    'ZHToSSTodddd_samples_2018',
    'WplusHToSSTodddd_samples_2018',
    'WminusHToSSTodddd_samples_2018',
    'ggHToSSTodddd_samples_2018',
    'JetHT_data_samples_2017',
    'BTagCSV_data_samples_2017',
    'DisplacedJet_data_samples_2017',
    'Lepton_data_samples_2017',
    #'auxiliary_data_samples_2017',
    #'singleelectron_data_samples_2017',
    'BTagCSV_data_samples_2018',
    'DisplacedJet_data_samples_2018',
    'Lepton_data_samples_2018',
    #'JetHT_data_samples_2018',
    #'auxiliary_data_samples_2018',
    #'egamma_data_samples_2018',
    'registry',
    ]

for x in __all__:
    o = eval(x)
    if type(o) == list:
        registry.add_list(x,o)
        for sample in o:
            registry.add(sample)
            exec '%s = sample' % sample.name
            __all__.append(sample.name)


#span_signal_samples_2017 = [eval('mfv_%s_tau%06ium_M%04i_2017' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]
span_signal_samples_2017 = [
]
#span_signal_samples_2018 = [eval('mfv_%s_tau%06ium_M%04i_2018' % (a,b,c)) for a in ('neu','stopdbardbar') for b in (300,1000,10000) for c in (800,1600,3000)]
span_signal_samples_2018 = [
]

_alls = [
    'all_signal_samples_20161',
    'all_signal_samples_20162',
    'all_signal_samples_2017',
    'all_signal_samples_2018',
    'span_signal_samples_2017',
    'span_signal_samples_2018',
    ]
__all__ += _alls
for x in _alls:
    registry.add_list(x, eval(x))

########################################################################

########
# Extra datasets and other overrides go here.
########

########
# miniaod
########


for sample in Lepton_data_samples_20161 + BTagCSV_data_samples_20161 + DisplacedJet_data_samples_20161:
    sample.add_dataset('miniaod', sample.dataset)
for sample in Lepton_data_samples_20162 + BTagCSV_data_samples_20162 + DisplacedJet_data_samples_20162:
    sample.add_dataset('miniaod', sample.dataset)
for sample in Lepton_data_samples_2017 + BTagCSV_data_samples_2017 + DisplacedJet_data_samples_2017:
    sample.add_dataset('miniaod', sample.dataset)
for sample in Lepton_data_samples_2018 + BTagCSV_data_samples_2018 + DisplacedJet_data_samples_2018:
    sample.add_dataset('miniaod', sample.dataset)


for sample in qcd_samples_2018 + qcd_lep_samples_2018 + leptonic_samples_2018 + diboson_samples_2018 + met_samples_2018 + ttbar_samples_2018: 
    sample.add_dataset('miniaod', sample.dataset)
    
for sample in qcd_samples_2017 + qcd_lep_samples_2017 + leptonic_samples_2017 + diboson_samples_2017 + met_samples_2017 + ttbar_samples_2017:
    sample.add_dataset('miniaod', sample.dataset)
    
for sample in qcd_samples_20161 + qcd_lep_samples_20161 + leptonic_samples_20161 + diboson_samples_20161 + met_samples_20161 + ttbar_samples_20161:
    sample.add_dataset('miniaod', sample.dataset)
    
for sample in qcd_samples_20162 + qcd_lep_samples_20162 + leptonic_samples_20162 + diboson_samples_20162 + met_samples_20162 + ttbar_samples_20162:
    sample.add_dataset('miniaod', sample.dataset)
    

mfv_splitSUSY_tau000010000um_M1200_1100_2017.add_dataset('miniaod', '/splitSUSY_M1200_1100_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M1200_1100_2017.add_dataset('miniaod', '/splitSUSY_M1200_1100_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M1400_1200_2017.add_dataset('miniaod', '/splitSUSY_M1400_1200_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M1400_1200_2017.add_dataset('miniaod', '/splitSUSY_M1400_1200_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2000_1800_2017.add_dataset('miniaod', '/splitSUSY_M2000_1800_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2000_1900_2017.add_dataset('miniaod', '/splitSUSY_M2000_1900_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2400_100_2017.add_dataset('miniaod', '/splitSUSY_M2400_100_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000100um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau0p1_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000000300um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau0p3_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000010000um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau10p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)
mfv_splitSUSY_tau000001000um_M2400_2300_2017.add_dataset('miniaod', '/splitSUSY_M2400_2300_ctau1p0_TuneCP2_13TeV_pythia8/lian-RunIISummer20UL17_MiniAOD-e67f9b5d033cede4d000433a2a96d4fb/USER', 10000)

for sample in ZHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ggHToSSTodddd_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ggHToSSTodddd_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
#for sample in HToSSTobbbb_samples_2017 :
#    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ggHToSSTodddd_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_signal_samples_20161 + mfv_stopdbardbar_samples_20161 + mfv_stopbbarbbar_samples_20161:
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_signal_samples_20162 + mfv_stopdbardbar_samples_20162 + mfv_stopbbarbbar_samples_20162:
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_signal_samples_2017 + mfv_stopdbardbar_samples_2017 + mfv_stopbbarbbar_samples_2017:
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_signal_samples_2018 + mfv_stopdbardbar_samples_2018 + mfv_stopbbarbbar_samples_2018:
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_20161 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_20162 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_2017 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stoplb_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in mfv_stopld_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ZHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WminusHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in ggHToSSTodddd_samples_2018 :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)

for s in all_signal_samples_20161: 
    _set_signal_stuff(s)
for s in all_signal_samples_20162:
    _set_signal_stuff(s)
for s in all_signal_samples_2017:
    _set_signal_stuff(s)
for s in all_signal_samples_2018:
    _set_signal_stuff(s)


########
# ntuples
########
for x in wjetstolnu_0j_20161, wjetstolnu_1j_20161, wjetstolnu_2j_20161, dyjetstollM10_20161, dyjetstollM50_20161, ww_20161, zz_20161, wz_20161, wjetstolnu_0j_20162, wjetstolnu_1j_20162, wjetstolnu_2j_20162, dyjetstollM10_20162, dyjetstollM50_20162, ww_20162, zz_20162, wz_20162, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon20161B, SingleMuon20161C, SingleMuon20161D, SingleMuon20161E, SingleMuon20161F, SingleMuon20162F, SingleMuon20162G, SingleMuon20162H, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D:
    x.add_dataset("trackmover0p03onnormdzulv30lepmumv8")
"""
for x in wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F:
    x.add_dataset("trackmoveronnormdzulv30lepmumawdv8")
"""

#WplusHToSSTodddd_tau1mm_M55_20161.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WplusHToSSTodddd_tau1mm_M55_20162.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WplusHToSSTodddd_tau300um_M55_2017.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WplusHToSSTodddd_tau300um_M55_2018.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WminusHToSSTodddd_tau1mm_M55_20161.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WminusHToSSTodddd_tau1mm_M55_20162.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WminusHToSSTodddd_tau300um_M55_2017.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#WminusHToSSTodddd_tau300um_M55_2018.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#ZHToSSTodddd_tau1mm_M55_20161.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#ZHToSSTodddd_tau1mm_M55_20162.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
ZHToSSTodddd_tau300um_M55_2017.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
#ZHToSSTodddd_tau300um_M55_2018.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")

# for x in qcdmupt15_2017, qcdpt15mupt5_2017, qcdpt20mupt5_2017, qcdpt30mupt5_2017, qcdpt50mupt5_2017, qcdpt80mupt5_2017, qcdpt120mupt5_2017, qcdpt170mupt5_2017, qcdpt300mupt5_2017, qcdpt470mupt5_2017, qcdpt600mupt5_2017, qcdpt800mupt5_2017, qcdpt1000mupt5_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017:
#     x.add_dataset("ntupleonnorm3p5dzulv30lepmum")

#is this the correct ntuple version? 
#mfv_stopld_tau001000um_M1000_2018
#for x in mfv_stopld_tau000100um_M0200_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau000100um_M0600_2018, mfv_stopld_tau000300um_M0600_2018, mfv_stopld_tau000100um_M1000_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau000300um_M1600_2018:                                                                                                                                                  
SingleElectron2017B.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-8c7c2bda1cd22d80173e548f51d2f831/USER', -1)
SingleElectron2017C.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-e4d56933c86918c3bd148722113778ad/USER', -1)
SingleElectron2017E.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-b263ccec0b85cece65a88cc4bcb47b85/USER', -1)
SingleElectron2017F.add_dataset('ntuple_K0_DYmuontrig', '/FakeDataset/fakefile-FakePublish-618b1b5f1913656e40f0cfb572514b20/USER', -1)
# for x in qcdmupt15_2017, qcdpt15mupt5_2017, qcdpt20mupt5_2017, qcdpt30mupt5_2017, qcdpt50mupt5_2017, qcdpt80mupt5_2017, qcdpt120mupt5_2017, qcdpt170mupt5_2017, qcdpt300mupt5_2017, qcdpt470mupt5_2017, qcdpt600mupt5_2017, qcdpt800mupt5_2017, qcdpt1000mupt5_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, ttbar_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017D:  #wjetstolnu_amcatnlo_2017, Abby removed
#     x.add_dataset("ntuple_K0_DYmuontrig")

ttbar_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-0b62fe2c2e68572d7b19020908d49d6d/USER', -1)
#wjetstolnu_amcatnlo_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-60cc39a06694799dea9f2d0159f6f14f/USER', -1)
dyjetstollM10_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-99411c72ade5979f99b481f27dd2ba8e/USER', -1)
dyjetstollM50_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-a9976aaa8cda96912597725368bdee78/USER', -1)
ww_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-6cd7d064e8348c4bfe63bac0035e610a/USER', -1)
zz_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-b6cd6a80dc9138ea429a74c6b1c29c05/USER', -1)
wz_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-99ffc914d00c091e9cddbc3ac2cd696a/USER', -1)
SingleMuon2017B.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-74ddfb1a658d0533a28148c11269a049/USER', -1)
SingleMuon2017C.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-64a61bd220abd9a9181478ca1c6ea276/USER', -1)
SingleMuon2017D.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-f9ea7deae9a0cc186751fff11ec12be4/USER', -1)
SingleMuon2017E.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-0bddb82dedbe9c6e67f0b6c20885d0f0/USER', -1)
SingleMuon2017F.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-6caa49f987d65320974610076f13f9f1/USER', -1)
SingleElectron2017B.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-fffd5d27db72a108c4bf9c34c49242f1/USER', -1)
SingleElectron2017C.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-9a4aa03a14030ee0b61bcd34f0ab13f1/USER', -1)
SingleElectron2017D.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-657210c092ccffd2f73f4b3ec4718cb7/USER', -1)
SingleElectron2017E.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-255956d95e24e484da66a0e321b65d10/USER', -1)
SingleElectron2017F.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-080e1718700dbe488f081d85bf920901/USER', -1)
    
#WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('trackmovermctruthulv30lepmv9', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)

WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
WplusHToSSTodddd_tau1mm_M15_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)


SingleElectron2017B.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017C.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017E.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
for x in qcdmupt15_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017,  dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleElectron2017D:                                                    # ^   wjetstolnu_2017,   Alec removed; wjetstolnu_amcatnlo_2017,  Abby removed
    x.add_dataset("trackmoverulv30lepelemv7")

"""
# #for tracking tree : cut 0
# for x in ttbar_2017:
#     x.add_dataset("trackingtreerulv1_lepm_cut0")
for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_cut0")

#For tracking tree : cut 0
# including info on leptons and lepton tracks

for x in dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
    x.add_dataset("trackingtreerulv1_lepm_wlep")

# #including info on leptons (including lepton sel tracks & good lepton sel tracks 
# for x in wjetstolnu_2017, dyjetstollM10_2017, dyjetstollM50_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
#     x.add_dataset("trackingtreerulv1_lepm_wsellep")

#we now have run over everything : good lepton sel tracks + tracks matched to a good lepton

for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F:
    x.add_dataset("trackingtreerulv1_lepm_wsellep")
"""

#for tracking tree : cut 1

for x in dyjetstollM10_2017, dyjetstollM50_2017:
    x.add_dataset("trackingtreerulv1_lepm_cut1")


#brand new vertexer -- did not do anything about the lepton tracks in the dz fit (bad? good?)
## note that some samples are incomplete -- need to continue resub 
qcdmupt15_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-68d6fedeb43ac199e0ae232bbb6cf7ec/USER', 2343)
qcdempt015_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-58b42aaa30a41e3441604491064b13ba/USER', 2)
qcdempt020_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-4147242f43eb8dd2a11daf87ed93d40a/USER', 3)
qcdempt030_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-ef1f916dc795562e84f9a6bfc6fd2082/USER', 7)
qcdempt050_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-7120fdee8977f04120f0d2a67867f5dd/USER', 36)
qcdempt080_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-0ae68c34e5b783445538bd40ac0bcb58/USER', 93)
qcdempt120_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-a1469dc38625e19badb71c31c432f5df/USER', 196)
qcdempt170_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-aa45b020659525475fd6cb8a39e742cc/USER', 146)
qcdbctoept015_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-e78e9c2603b214e69565d1decb3efc5f/USER', -1)
qcdbctoept020_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-2cc51a310cc87dd5d9002711cd1f9100/USER', 0)
qcdbctoept030_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-175e8f5b816012a1454e7131342a1f25/USER', 328)
qcdbctoept080_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-14a5045475c4aa0d9279d641d9e909f2/USER', 1187)
qcdbctoept170_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-4ee74a89462cb7524923658f38bc4dad/USER', 2312)
qcdbctoept250_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV9Lepm_2018-a3775781c9765b2519fcfd779beb8190/USER', 2612)
qcdempt300_2018.add_dataset('ntupleulv9lepm', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-6e2d5b97e605293f1d4259dae635ea54/USER', 181)
#ttbar_lep_2018.add_dataset('ntupleulv9lepm', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-2fc48f1c8c128973a3fe730ed10f9592/USER', 4020170)
#ttbar_semilep_2018.add_dataset('ntupleulv9lepm', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-1b8b79ac74e2b468f71e7fa452fa9a7c/USER', 1112073)
#ttbar_had_2018.add_dataset('ntupleulv9lepm', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-d6245750e8321d2371af3cb19607efef/USER', 4166)
#ttbar_lep_2018.add_dataset('ntupleulv9lepm', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-06df96a356c2fe710ebc71bd964744e9/USER', 23971522)
#ttbar_semilep_2018.add_dataset('ntupleulv9lepm', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-bf891447412321d36949f8c9ada687fd/USER', 47008700)
#ttbar_had_2018.add_dataset('ntupleulv9lepm', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_2018-a0b0736c0dbc753a3e3d166ec880a1f1/USER', 93981)

# wjetstolnu_2018.add_dataset('ntupleulv9lepm', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV9Lepm_2018-0821f8ca1009fd8745a2ee05397979d5/USER', 77257)
dyjetstollM10_2018.add_dataset('ntupleulv9lepm', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV9Lepm_2018-f69fb0daea531bb34fe7b3b1fbb05f40/USER', 1707)
dyjetstollM50_2018.add_dataset('ntupleulv9lepm', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV9Lepm_2018-caab6aed847e3a2a3f77c9777139026f/USER', 243774)
ww_2018.add_dataset('ntupleulv9lepm', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-f924a3b2bd27945aeba0f6439bbdc149/USER', 33539)
wz_2018.add_dataset('ntupleulv9lepm', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-01ab62e6819417fa51a78100a2b4d238/USER', 30581)
zz_2018.add_dataset('ntupleulv9lepm', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV9Lepm_2018-0b996e2d8f82269f570ca92c32a24840/USER', 14418)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-3a84019dd49089a07dbbcc6678fda3ea/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-1f8cef2e0fd2e9396583c43efaeecacd/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-8f65e80bfa6ca6393139204cffdffca0/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-21a7939abc0541f52e633bb963a86565/USER', 198147)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-50dd9c2cfb2053fb32eabcfd9ddf9f65/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-9b7470991ed4ef70b74d13d15948b1c1/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-c039b50b129ac525897134865bbcdd0e/USER', 203023)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-3b5e4f0495724bde79c862343be2186e/USER', 197602)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-26715ed09b1506cd8f44b4ce7d2d19f7/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-40f4a49bb75dd958be37be9b826d3ded/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-c621303522b2599815b71742fb21c3eb/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-eeba5a2b3eda89a7a478d40221ed4016/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-3cd334d39721d4bb26422bea692f6591/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-dc75c6e373117e1501ea70d4b3b1b62d/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-be8f4fbf23b0fb469cd89d6646b45658/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-1ac4a6bdc61399723c7ddaa4acb7fb5b/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-13bf23456958593ac629b5e80710315f/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-534b734eb8362b797caa0fff0ecca0aa/USER', 196032)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2b6cd5fd99db40a4632a278feca24fd8/USER', 197845)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-d9c83e71a567e8e6a4bbb8c871ebe6d4/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-98b6123e3911ac85072daffea8498f77/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-557b79c1a7d8a0877744a2df27637725/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-080a24100b753a103823882be5c8cdd7/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-816e354efc2b9b4a5d43fe8d15c31a38/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-cd560754c08ff968510ddb173c53f5c6/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-994b05603c5e3b0ffbe320d335dc2c3a/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-e21c394dd1135d618d1227239d8a455e/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-e1f5a855f5c876be06e1fc47758d6ba4/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-e118adc79abaa03a2e0e359fe506609b/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-83d7e53a354854d1c8bf66a7a7f75998/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-8621923df4e6df2f833550b10db45114/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-cf3ba95cee0bc1ba4769f2c19df1c221/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-00a0d6ee16912d00ca49f79826803640/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-1c00cf9fbaa91596bacf0fed13361faa/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-f0c457d005127d1a8ffcffb9a73d9987/USER', 197406)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-6c4d81c4787658c37e3377560df95b83/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-f035d444852162d5bfa499119b0f070f/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-d405ff60ed1e8b6d9403ebab6feb1806/USER', 200807)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-4218d349323a47688295da686ac3497a/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-c6373c51192b66b2282ef5e3bace715e/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-96f5688281cd42bc9619fe0141395d8d/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-ed252f1aa5673337d35d655f051b75e9/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-15e45a64455503071d21524645f3beb7/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-71c40d6c85228512445f9d43242bcedb/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-82a5ae9dddf83c504370afb0dc945853/USER', 99525)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-dfcdc022f64ab35cf150cfbb8ee8f51b/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-4d7bd86a3176ce2e201b309ff45412e9/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-dfaeee6e51710396975704992792717c/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-c8d997d607ebaa96bc6d4aca4995294d/USER', 101211)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-f9905209ff3aecd8143800189352b30c/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-475f952ffaaa647e75d540d8ab50bccd/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2e51e594f8dd45ec8ce5736f7173d781/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-94dda374106298324250505e51291196/USER', 198397)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-d3b7119f46c8bed01f229dd04a3901e4/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-10a775cb7d99b698338c88725a9ddc20/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-a528ec9d9a271a80127d30016d3cffd9/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-b8b1c739d24692b9f523d159c3254c5a/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-52c264cc131c71319299ac53ce0e5188/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-9d4851083a728c972649969f6239f3e3/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-91c29dd03883d97edbb191ac905fd05d/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-4edd66e977de261ef74afa2d372e0985/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2e5ea9a34f36d189aeda68fb1d777191/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-48dbd65f81ead014c0b32fc6fb4c342a/USER', 200098)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-b9ff767ab3846e9cc4deae0e9229125a/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-d1cb2c7a0f22573e36ca274386784797/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-186adfb4b6ec5b56a7cc964cab1aa04c/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-d5700879bc6c7171c1e6ad8188f57b82/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-0f7b0014aaf7d44e516eb35e0a159cae/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-acf8782479886c3cefdaed9d87ccad45/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-988badbeff18ea821244eade4e104955/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-65f7f1e45691165eee0479da2cf7d0b1/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-0bb9b3d1293a5d9b77d7f7cc48071b32/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-03479b6abe61fa57459d57b8bcafe6e2/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-ffe40e08b5c1f98d9eb1c83f29f54cc1/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-9a9b47122c2decfc9f35bc34eb48a889/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-0c89f5d26866f41964cbe677675cbf5b/USER', 197829)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-270f55b304c5874862d15af9ed799743/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-1fedc8a824b1a8bb0e0f653eed45b86d/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2bdb3b2dc24a00e8228733520fc9a3de/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-5cfc45e99e0e2ed2af958575fee09dbb/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-be023545ce17af44405d66c54093c483/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-62e98ce1faa2691f35bd93150642d6a6/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-28b2be848618828892382e82cf8c0927/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-da0be38ffc8aa18c75ffc90bb88505fb/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2d166a7b2d311598d83b5f462b270e06/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-c037a92165925cd7b2e3329e400d107e/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2ebb2360d902a797a4da3e69df7f439b/USER', 202529)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-6e24151861dbdadd0944a3df13e5673c/USER', 196708)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-525759dc2af6a3291945406aafcb3ca4/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-a019f1326af01602b4a02a7c95f43434/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-6a3c0cb1502edd6690e0d77e0747d3e0/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-136227bab19898ad2548f0b1c0177681/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-e957a79897713ec5c89e98dabc924713/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-2e495008f2b05825c661008e2d53720f/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-26489bcbb9a46c21acd5fefd8f1ae508/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-924b95e9a5968bcf4165353f618a1bc2/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-f2f00896773c14a101288fb32fdd4629/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-dd7c644e5fd148e5c059f55fa760f2f2/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-a4f7123cf81f679aac50f42421c10eb4/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv9lepm', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV9Lepm_2018-4535a031c94be29f724d8a62d1fd5b5f/USER', 98449)

#ttbar_lep_2018.add_dataset('ntupleulv9lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_WGen_2018-1a1f79d40f6b7126d1571e12d51e9079/USER', 23971511)
#ttbar_semilep_2018.add_dataset('ntupleulv9lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_WGen_2018-06f4ccf7f9e99c1dac78d05f90f8be5a/USER', 46976261)
ttbar_had_2018.add_dataset('ntupleulv9lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV9Lepm_WGen_2018-51733bae56d3b337b429fa4fdf7900e3/USER', 94370)


qcdempt015_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6adf86f355597a8cbd5eedaca0add5ac/USER', 0)
qcdmupt15_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-e759ad98d0f43d744f979317e3216c20/USER', 1577)
qcdempt020_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-32777b99a831f30d065fbb741f8bb203/USER', 0)
qcdempt030_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-45ba33279f3302e43bb2f6bdda73a5d6/USER', 1)
qcdempt050_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-324311abd707e3d6d3617f762f208000/USER', 5)
qcdempt080_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-74a6409cbf11a3d14b86fb779737f5a8/USER', 16)
qcdempt120_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-f90fcd9cbf90b05084d846b238d31e68/USER', 30)
qcdempt170_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-9e12e5a9ebff9b8f2bb21e4b4d480d1f/USER', 23)
qcdempt300_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ff917c63a0e7b573fe888c911faecef5/USER', 33)
qcdbctoept015_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2017-1b5ddeed8c16444c6c369a611fe44e6c/USER', 1)
qcdbctoept020_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2017-5d0d527312d450948487d854e6dcad31/USER', 3)
qcdbctoept030_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2017-2f30b3e38adb5150ea7452c11a3c5ff0/USER', 33)
qcdbctoept170_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2017-3c2d1c72f32ece4864698f103344109d/USER', 394)
qcdbctoept250_2017.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2017-83bb4850816a7cb34fdeeadd11799176/USER', 457)
#ttbar_lep_2017.add_dataset('ntupleulv10lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2017-44875180c7e0a7e786d0be03ff04c39d/USER', 3392501)
#ttbar_semilep_2017.add_dataset('ntupleulv10lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2017-9d1c1933b9a9786844c1cdb4f077e413/USER', 6744007)
ttbar_had_2017.add_dataset('ntupleulv10lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2017-b3f3cb9bcbb5be506ef1d05a2eedea09/USER', -1)
wjetstolnu_2017.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2017-cab01ddde62ca73a08de1f75923a7d05/USER', 12251)
dyjetstollM10_2017.add_dataset('ntupleulv10lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ddf0ea42e4b142c55af59f28d4d08ced/USER', 639)
dyjetstollM50_2017.add_dataset('ntupleulv10lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ebaf08bb96d68ab7498581396da57d12/USER', 46190)
ww_2017.add_dataset('ntupleulv10lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-039ae08dd48d974f53d0244f0e18c89f/USER', 5381)
zz_2017.add_dataset('ntupleulv10lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-a2416a7af05b6a1895122e3bf3cb73cc/USER', 1966)
wz_2017.add_dataset('ntupleulv10lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d5748ad80d3e4149e84f703f20461cd1/USER', 5105)


mfv_stoplb_tau000100um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-10564226111eda5b8bd0b4cb22dbe4a4/USER', 194928)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-62a1448ca11b2004ed681f205cfc79dc/USER', 200301)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6c81359334eec995f0b84b86b58175c7/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-1b11950e631292c2cd8accb35da2c320/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-2b3d757477cb3de3108bc5a161dc3cba/USER', 200668)
mfv_stoplb_tau000100um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-493a17e2be7f019d0215d79699ba924c/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-0665867a96728d541aafb58819cc2ce7/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-151fa707f1916312cefb0e96f7cff235/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-a6c00373e81a44f196612db86c1188f7/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-1f00eec6ad919046d8474c4402fb1ba6/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-04cb92fcddcc9c6132efca502de52b95/USER', 199322)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-5f469786a00255fdeea5650aae8af086/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-21be329fd428072488de7dac28b2b249/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-61f0461ed0a71f088f8417f2e4cf5fb6/USER', 196297)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ea7c782013072c1fe87f9db5567ed4bb/USER', 198644)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-44f4fa941c500d0ed68e67f21fec6926/USER', 202021)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-cf8e7a72f68d22df2bb51090b50fecf7/USER', 199079)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ea50561931d1acd07a6c1ddabde30896/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-98d13ad3a80bac024991efb86a292022/USER', 98921)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-39a865ce42e627169d5a5bbc5625a77a/USER', 100284)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-e8d834d229ec7e6e2055e25b39797c7d/USER', 199639)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d5fc1b0e0b6d2625edcc8898a066d65d/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-b13c0ed8646f13127483621b927bad50/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-728e7e76809f1777ba2bc2a209fa3859/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-e59acbcaa96f8350e427e2d4689a1e32/USER', 100172)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d6dc711b3435053e63edbaa56a901967/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6f3a89ea89ec220e711a2e90d8e14928/USER', 198899)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-41bfc5301f6932beb6b6b8b634873ab6/USER', 199948)
mfv_stoplb_tau001000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-454488d0fad764beeed89faf9948f86a/USER', 196687)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-c001a338f5111c3ed52db344cea58b55/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-2ad593b0cb1c5b103c97ba56ecb5ec0b/USER', 198231)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-3f17232b1953b56338327854fb660d2f/USER', 198170)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-1442ae90d9bc31485e53d11ea984f789/USER', 199832)
mfv_stoplb_tau001000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-bd51f9acfe909ae0ac7275f0b5d42df3/USER', 200296)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-a8f429251b5ca9ddd3b83c1a045a443f/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-a8966490b6d2ababd318625b9f9d7d8c/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-4854170a33288131dce4d7e21fd3969c/USER', 200230)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-44c18f96220ed5f80002c816eb3a2b09/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-46e47fcbc118dae790ae398c385b2801/USER', 197003)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-c1f86b7a08cacd5a6b13f65807861c80/USER', 198930)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-f390c3eded763a650e1ad879f18fdf35/USER', 201812)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-0461e108fac010d0f57beb9e9a73feab/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ac49931a3f70377af9c16162184a68ac/USER', 197409)
mfv_stoplb_tau001000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-cd78a2bf9ced63f8b2a1f2f35a981472/USER', 195368)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-806d99ff654381232678d7969a89d9f6/USER', 200005)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-1eef189c43617bb6e4824310e4e0e916/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d602a002e0f251191a221a1ca49770a0/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-8a42214e7746d393d72ec43d05e057b7/USER', 98799)
mfv_stoplb_tau001000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-4b2e277b7877a032ff6542007150119c/USER', 197479)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-3dc7ea79616188c1c2ee6000fdc5e70c/USER', 201690)
mfv_stopld_tau000100um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-2d23bb9de91c74013419f6497cd056d0/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-9bb34a47dca9a0059449b65eb3363937/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-26876345911a578728b7de58d3053eb2/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-0536e7a21901c9b8acffa23803a98413/USER', 198608)
mfv_stopld_tau030000um_M1000_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6925948c94be0e702b951a1e68d007bc/USER', 199499)
mfv_stopld_tau000100um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-bc0bcc1cf0a42f57417547e4616894b5/USER', 198263)
mfv_stopld_tau000300um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-ea554d6d3108deb3dfc742bc75418851/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-bbd31092203cb1a1d4e3bebb65aacd37/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-4ffbae23acb1ec8604af75a91d4f924d/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-84f62a190e9f268f6ff8eb02ed06bdaf/USER', 200851)
mfv_stopld_tau000100um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-de2e2c7b2c8e213de4ae83a53311da77/USER', 198812)
mfv_stopld_tau000300um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-8146bf540ee8c435c745fbe7608b371d/USER', 194591)
mfv_stopld_tau010000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-498fa19aacb4691b938937f95ca78c1a/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-095a8d6285fac9e2fbaabdb61ec9a805/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d74195bd8a0381bfe02c165b1bcdef0a/USER', 200714)
mfv_stopld_tau000100um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-7802b90fe36ca36732860c5850886c92/USER', 201051)
mfv_stopld_tau000300um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-28fddaae0fd0e85d5f00dd10b934f203/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6f1ca8d6b77cd4ac026c26dab5b3563e/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-0c5bcdab50914c907ca8e1447c5925d6/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-9b06c9d9b70f998d788c056cc353091a/USER', 100345)
mfv_stopld_tau000100um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-98187f008119a7506d61b53223c44609/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-38c7eb2ba84997658dd92a29e3fc9d91/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-809696663b27c781cd56247d4fcd9d9b/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-7426b814bac416b79ba1bd19cf731dfd/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-94bcbc035aa15b33ee10d597997c7f7d/USER', 99787)
mfv_stopld_tau000100um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-07a0d642e872cb2da200cebfe4cc0216/USER', 201843)
mfv_stopld_tau000300um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-a0046dd2013253000bebfa0470500547/USER', 199789)
mfv_stopld_tau010000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-353b410052f0c056498f9523fcb92389/USER', 197403)
mfv_stopld_tau001000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-b30664739c8d6636b3b0114f00b97339/USER', 198275)
mfv_stopld_tau030000um_M0200_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-932ec33779eef4bb898d8591aec49f45/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-63e09e3efa1bdaf69989f8085e12ee74/USER', 197379)
mfv_stopld_tau000300um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-2484446757d01caa715413b6ce2883b1/USER', 197934)
mfv_stopld_tau010000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-0e7df70312eee62fe463ca0402e0433f/USER', 197990)
mfv_stopld_tau001000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-c4afa7ef63cb71374cc8ccd0de47fda1/USER', 199705)
mfv_stopld_tau030000um_M0300_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-3e026ff8dca25ec47d207d6787f6430d/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d7161a744e178b3556973d002c2e7bf5/USER', 202735)
mfv_stopld_tau000300um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-3609daabff77213139e446fca3c37fdb/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-32c5d0dbeeab9ce3b8fc6edd115db26b/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-57ff6678c4e4a05c74fa91b5c6a7666d/USER', 197130)
mfv_stopld_tau030000um_M0400_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-cae73051d8ce162bb090ae67b8b844fe/USER', 198731)
mfv_stopld_tau000100um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-e182d193d21e79012b6df6f7950660cd/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-d437dda8d96c39bfcf7494d07dc05053/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-f691a9a83e1663896a149498909b32d0/USER', 9103)
mfv_stopld_tau001000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-13ef0b12865cc214f538a86333266a43/USER', 203302)
mfv_stopld_tau030000um_M0600_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-6b0c1598fc448bccf2ed4020a60f6e70/USER', 199944)
mfv_stopld_tau000100um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-28b5f83f93f0d8fe38d433b8e953ccd6/USER', 200077)
mfv_stopld_tau000300um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-10200a42e6092672dee7d83f51a31e40/USER', 200814)
mfv_stopld_tau010000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-dae8e12ceb72c2aa2a587961fabfb623/USER', 99313)
mfv_stopld_tau001000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-fafd17e10dcca6d88af5f87abd864f57/USER', 200829)
mfv_stopld_tau030000um_M0800_2017.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2017-08a05382a58e45abd3c6a081d1f3d1bc/USER', 200140)

qcdmupt15_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-27b9ab289cca8ca38b9d327087a28258/USER', 2516)
qcdempt015_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-59be9dd00c204f67eecf7ddfe58ef742/USER', 2)
qcdempt020_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-557b7f4299649f24381bbe49fb6d03f6/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-effee8529027ff380fc2aafd2b8015b7/USER', 3)
qcdempt050_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-613ea0e4c40fa65808a033a3659c8f19/USER', 8)
qcdempt080_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-9192ecd8c8b5e7504e652407c72c8b2e/USER', 22)
qcdempt120_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-b9afc6670103c587ce44a0a01370a25b/USER', 51)
qcdempt170_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-d63f89af35d39ead9181e8f1a0ba5c7d/USER', 27)
qcdbctoept015_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-f746d6ae72d6db9537bbde289f35bbb9/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-72b53b05e44d322ba366e5ffae755df8/USER', 3)
qcdbctoept030_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-54dad8897e891fbe6d63abc695de33d7/USER', 77)
qcdbctoept080_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-91bccc63bf2d39652452a68ee7ee2637/USER', 240)
qcdbctoept170_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-08e766210c756cd2f697de87e77e7098/USER', 459)
qcdbctoept250_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV10Lepm_WGen_2018-0aab1d9158c673e1aa3876c07e4aff8e/USER', 516)
qcdempt300_2018.add_dataset('ntupleulv10lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-a33b436af2d8bfeca9352100db4d5ee1/USER', 37)
ttbar_lep_2018.add_dataset('ntupleulv10lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2018-b1f588cbac5e905ba5cf417dfd0d2a35/USER', 5344185)
ttbar_semilep_2018.add_dataset('ntupleulv10lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2018-bd2160b6f2bf031424f844eb16332ec4/USER', 10655075)
ttbar_had_2018.add_dataset('ntupleulv10lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8a587e26ecc8fa3e672eefdf17ce89ad/USER', 20455)
wjetstolnu_2018.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8d1d0e41b6052d5727c7f6571d0cfbc2/USER', 15365)
wjetstolnu_ext_2018.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4d2ff0e0a0c7201da5516dcd6193e9b8/USER', 14741)
dyjetstollM10_2018.add_dataset('ntupleulv10lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c1e96c5ddfa0c9a5a980983e452aa15d/USER', 1308)
dyjetstollM50_2018.add_dataset('ntupleulv10lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-5a6c962c0a4950e690513bff4faef011/USER', 50318)
ww_2018.add_dataset('ntupleulv10lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-411e74744422c54f39a3ccbd367af000/USER', 6468)
wz_2018.add_dataset('ntupleulv10lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-00b976bfd971507532052a53197205d3/USER', 6144)
zz_2018.add_dataset('ntupleulv10lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV10Lepm_WGen_2018-74b858adc5ff9a1f60429f9fd943bdd4/USER', 2968)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-e13bcd2da8f19338bb6dbbcb2ea4f266/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-5470a3730bd2e2f5008f5f417a3ea446/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-80795b1c9dff349540fe7a26ca6f21d6/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-1f971155aa43c44bf6beb12680a1984f/USER', 198147)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-fa763de07d8d85f2a6514c64a3856207/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4d9ac9424f4c47b0f12a498825a34458/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3033574ff62668257bf20ff2ad6ae99c/USER', 203023)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2f46120d79ff704a2ada251ad46b5086/USER', 197602)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4caf689fed5b7e0258169bf162dcefa1/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2c834fd628b2f3cb56900bc2d8df6f1a/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-675889cf02ebe69b555496146e211ce7/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-cf63fba8dae81a0af3285de9e854b10c/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-bd4fb02c9b7e73d9d628ea864c6ca8f1/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-bdec33f9f93ec1d43f7ba1a451ba2bc9/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-ceb2c5996ed6088acf3763765bbc5477/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-cce303f2e6b2ca50056a4ccf0113d2ff/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-e428f3b7f4b6b177caa64771311b2ee4/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-474e8f31895827432637a545b470decb/USER', 196032)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-cd821fcf6fdf747a055aa3957912d06f/USER', 197845)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-47a6e2ff981c823288be0032b18acbaf/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-80c6925ae3c558fb2712193e688d2304/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-ac97e56ea476cedaae5a27fba139a1cc/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-01d197bfe17bc9bf1880629c8c61ce8b/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-624caa6b90e88d28568ec260474b1137/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-0f8cfd55acddfe062dbce51381db42e6/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8540196bdb2d28d1999903c202505779/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-fce8eb8ae946e11a7ea9dbbfb20d885e/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-5bfa39cc9c474cae97dbf4031c833950/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-d5af327e892b333abca0df76d131bb14/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-82bd35f30af91c8471ca7f518895dd81/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-0df826a67103c5e5295d9a48b89e32ff/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-341b616369651588a94ccf5a27d12880/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-e5f88616922add1c546105f2fd072444/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2405c4c1683556107c0f4f653c03d220/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2c161b2441c01f2a4e480234cf7fd9ca/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-5a4809895749c12b6583488babf4f416/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3e7da20461b7e17b9949ef03031b5ff5/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4c5f47731b2f8801017d5fd8eabd166c/USER', 200807)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-cdb41ab6e48b69aa85e5aaf35958382c/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8a4822cf5527df20623344f597656cdb/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-da64a39daa6f8c4417e29b858173b437/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-0ba82d938ce311c044116269e70f20f5/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-92330c94d799ba67a446a9a22ca90444/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-ed7e7e3c4da80ce7ce0db854ef09606f/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8cc1b183441f286a0562a555194a9d92/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-53c1864867a8934c01a4d65feb2422fc/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-ce5774fff337618dcfb6158d7e3228eb/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-fa3f79188ed0bf9b8474eced49bf54c2/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-fc7790a335a7cb860220ab0e46936b62/USER', 101211)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-1762b62fbaa26568702a1317d73047bd/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-812a643a57313815652478c7206b7e93/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-7e28daf6f0f7073b163191ba6d070f60/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-056bb612e8c051562692aa4cf8e1f45e/USER', 200411)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c08ed17c6c526b529400e92a18868144/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-beefb0cf6c1671195b80bf05f5d86743/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-93fc89dac85d1cd40cca17c07a1f703b/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-5136905aa5bdd58821d10b0f660618c3/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-b5d12beb5971f6f5f21b57449082efa4/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-e7c163bd66728ad9bf3fdaf90b36bd7e/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-31185a8533a9c7b3481a82c3ed46a155/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-bf2af0da36a38fcc63a4e465e7774f46/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-607b37c5b8e715623e4f115316d93303/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4365ec6147d724960deaf885d9fcd3aa/USER', 200098)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-07208a53f23178d5be6578e7a530cf14/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c69c735f630eee24750d4dca80e9b8cd/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-483f4711b39ca9095d0b871c6bfed707/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-21abefc02282ad70102ba8343fb48b80/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-36985a9451374efbaece2e7c27a849b5/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-77409a68145e0a2b389d06c80671b946/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-70be16734ce582a40d830e35cc2e6599/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-80f733af650e384c521fa7b20aaf65bc/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2ec60e862ea274e30bd0466f017c1c4e/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-bde1556d12c95b8cca801bb9a89c6c25/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3b6f4c56d15024f533e512cf9e051329/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c8af84285a46251563f634997dadbe8d/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-a9c060eb70d46be61ff052522e08fdd1/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-1ea8595b47b53a7c7a32109c4f144027/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c1063df5076ddbd47e155a2718f1a6fd/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-2667f62a1e53cfe0a4fe7f065de7e098/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-35a47c4e0839de367f012f90e52f0cd0/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8ade4640ae00595f3f508764eed5dd17/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-19b0a50b1cdd61ae6e021aa2a7cd16a9/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4aebe6b7d8f101a4cee0890c2c217407/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-d696099b38745dd651eb76df31ced651/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-d05f2451cbb34ff9ffc0656eddb8e492/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-298d226a17f4379dec11a6f567a4d205/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-065a29c8082e0e5f352a95cd13bd59d5/USER', 202529)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3f387f94c27deebb9b4148b3be621f13/USER', 196708)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-f2338d8646e44d24b70ee5f8fd019df1/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3f711e704a0996820555e6f1e35428bc/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-68727bdeb58b6900fb11f9c2e205a8ad/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-7d15d6bf9202b69a41b329525dd94ef8/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-e2d7a0a04c51bab4d185694e6a63a8f9/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-ae7902a27240ada5228ab0645b692b5e/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8ebaee4ba09439fd827bbfcd8ee38d48/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-645a09a3e859106bab87b4bc392ac6c8/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8e869066c6cec4b6b2bb1528b6ba8278/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-f9fa6e8672fffe82b97e52293a0e0a89/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-c67fa6ffea6327d1cfd9d70e1ce6afa7/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv10lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV10Lepm_WGen_2018-3a492504849b30bc5436181606cf347c/USER', 98449)

##rescaled applied for 2018
qcdmupt15_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-01dbe37f0428f82dc0ff633f12635df3/USER', 2348)
qcdempt015_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2b14f5f2bc30ad7138142e1ebfa015cb/USER', 2)
qcdempt020_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-cd21bd70b61a87db8ce1dcd07b43f02c/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e736bbde135f0b31353aa5f40d00f5b7/USER', 2)
qcdempt050_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-66e6da1654b8db95138d4fe740280ffb/USER', 6)
qcdempt080_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-54fe1c721e04c6ad2d02dac0173c2208/USER', 22)
qcdempt120_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e2ddcbb485aaf31382c75e094eae9513/USER', 43)
qcdempt170_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e63883287f7a68fc524fa75549a590ae/USER', 27)
qcdbctoept015_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-d0686305ed5b303202ad5931c5f8b06c/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-f924c6e57715ca6fd42dcc0256af23d4/USER', 2)
qcdbctoept030_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-84d830d10255f23a8ce0eabbe6ccd21c/USER', 68)
qcdbctoept080_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-5318f7e64f9b413b1f0b2a4b247051f0/USER', 219)
qcdbctoept170_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-33db88c1d08b091fb9a3759573ed8097/USER', 426)
qcdbctoept250_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV11Lepm_WGen_2018-53b9279816bc480d36767cea7f107f86/USER', 468)
qcdempt300_2018.add_dataset('ntupleulv11lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-72a7bb591a76a7acc8f1d6a96c212321/USER', 35)
ttbar_lep_2018.add_dataset('ntupleulv11lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV11Lepm_WGen_2018-368894d6df77bd72e6069f8bbd9878b1/USER', 4950352)
ttbar_semilep_2018.add_dataset('ntupleulv11lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2bcf268631be7c56a61554df42a3379f/USER', 9828694)
ttbar_had_2018.add_dataset('ntupleulv11lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2ea000149053cc355113943de0b039ab/USER', 18749)
wjetstolnu_2018.add_dataset('ntupleulv11lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-85617d746c7fd561d6e94c637a6e8f2a/USER', 13696)
wjetstolnu_ext_2018.add_dataset('ntupleulv11lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-9d1b462a9f502086b20c1023b078537e/USER', 13249)
dyjetstollM10_2018.add_dataset('ntupleulv11lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-15d0a04347fac5a39a5011eedd31a25d/USER', 1161)
dyjetstollM50_2018.add_dataset('ntupleulv11lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d0edd7e2aa6308880f3b9da109ecc600/USER', 45063)
ww_2018.add_dataset('ntupleulv11lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-4bf2420e1b2a690f828b26fe1ce33ee5/USER', 5782)
wz_2018.add_dataset('ntupleulv11lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-19406ef4a6cded5b601ebcee08d2a592/USER', 5602)
zz_2018.add_dataset('ntupleulv11lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV11Lepm_WGen_2018-b0ea2e58eb5b546878bd7113b7303350/USER', 2757)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-bd332dc19425ce17325fed9ae2806678/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-64211cdba612952e99e382f37d1985c8/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-f44f122ebb4e378238d74aba6a8017b3/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d995716b94b47bc2d39f44a5e1decb6c/USER', 198147)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-a70adaf82446bc467470cb1c91e6e381/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-8de525a0472e55c0339fae91d0222913/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-044a96b15ecb23e7506c040f13c29fb1/USER', 203023)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-ee7893a4cb394dd0c65cedf279ed91c3/USER', 197602)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-8efee5c81b87c8ee1a371378642186c0/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-753f482c725fa66d3e39c1b1981e09b0/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-8e1ead53fe88c851c9d1cb66246c9b01/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d54c630412912ab9afb95b8d1121477e/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-f1908997fd8d2c224f23f9f9a6e30a56/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-30ea2750e8ad204188df6e039a46e5ce/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e44493941f7f27702543c854ac48696f/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-1aab6081266499701866e3c57396f734/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-8ba1df574d8ed11ee34378b04e3c8bfc/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-9645b92005f2f09f39dfe3d6f14a2f19/USER', 196032)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-82a9fe93a6f31fe0cd3ee163489d2c2d/USER', 197845)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-52e734044b6c789218b2b1a0bb429d02/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-b9afe0476fa6969c848a1031096cd370/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e5f64e32219f35531b0c68646790d8c4/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-69a515ad1550b9f0cfbe89f5b2a2b2b7/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-0bfe3bb8123e4a09dd0c34d462ff12cb/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-00a941c23d5bf66266365341fcfecfa5/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-c144fc55cd17e15453f0bac703c3f98b/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-4f2debe1007bf039e58df7420060981c/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-a231ac8f26891fd3fae3e676bcac8903/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-126485d34034671c3e0016549376bb22/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-842ffc76c985c790fc312141924cc4ef/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-de16a0abcc50ad4390292352ed192fff/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-def277645e64c87b49a0e8c68dfa568d/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-18c01528450f7e44a10757cb8b6024a3/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-cc12bdee206621a2469a9a817b6d3be5/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-5b02efc36dcc2f58a0e83c6e703f296a/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e59560cfa9c6e6da93b2ac930ddcac7c/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-7cea4ace6e9fb8562f17e4f2a124e187/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-4b585aedeea5a8200ade7596479037c0/USER', 200807)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-deca824298b894652a798880ef75f090/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-28504a602f8d7a19eb857d28a6493125/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-48cf3ed932cb8fe6c4046a8106ec74c5/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-dfc1955574c22c3f6b453e99dec569e4/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-1cae4ebc1b87961bf414383f88a50b62/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-6edc8a1e7e66a201840c4edd2db3e2c7/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-f4bac6cac64b7471eb4a28ef8b2ca148/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-0847a7463926e51599d1f61439e51ee0/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d945f739f1a7bf2b1c85171c755270d4/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e4e62dbfd16d2c899f4446c842d4f15e/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2ba1cad8da4cf6116a329206089ca026/USER', 101211)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-6491f3fa9c2316089f3f89746e5c4e58/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-df372a5dfa00c4b50bd1c8e248b3f7f8/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-7bd56e0cd2fd373641523be88152cd7f/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-b4e5382631ffc90fb21c897756105aa7/USER', 200411)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-dcde152519fe912b9b8a3924f19a2864/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d4b5e0bcdc9aa006585533233ad6b9bc/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-4899c1265d2104c5674099fe6f293409/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-a42c43c2dec7ba66ab28e703d26fd48f/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-444e715f60efbd6586d73cb5f32b170f/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-51ade41a6bee2e0b2db1366164ba816e/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-8264e6c172d485f867f5b5dc0253212b/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-cdf470f0f72445ec5067ad9688c72463/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d6c9cc246f89a9c883178d01abb3a455/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-93030e05d691aaa1c693f8b1ea40ee3e/USER', 200098)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d3513fd1e8c71fb29e39cc486d4a7483/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d5f80d1b6d712f0bc43f60caeb95dd1d/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-dbddb4158178fd6321a27951e33d07d1/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-954ee112a7da8cae62c8351f88ca29d8/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d93f7b36e25d1d7d327490c7cbc3af92/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-55050b104aee587f8106b6317af72792/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-0a1abfc1e7b99904d66741e12e4cb67c/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-da1240b1baa1a85ed95f2c96181561a3/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-d9040cb36f801add050b95210ef4d9ef/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2b6f9944d2c8317b9561104395ce4e6b/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-1c8b4086a197dc962bc5242d1c3d0366/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-52e6eb00ef2485961fc89be78dacf3f0/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-ef852e943aea5d701f62ffcd94b8b79e/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-14fcd369a83abf145d81188120ae21ca/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-08069757697b6a6b59d2b59efe5d713d/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-f2f32395f801d40c9680e65ef5d58259/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-2ed2b88afa994d6c80e1f96907dbad86/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-7ec1e853a590e503b12e5dcc8f82e8fa/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-7b8bdf1fca6b54e5c06f6a5ae2b5cae8/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-0384fce770c057800ca9d5f3f0ec5fa6/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-66b32369e5c5861ce2460dfb9bdcddc5/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-c52c389237da7a0ef8157d05cc9c41d4/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-86f8fa6135815925b480c06e13ca833d/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-09c69983b043f4ce6340b6db3fab384a/USER', 202529)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-0c0d78c987df38cc4ccc410130ad72f2/USER', 196708)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-5b8ed3e00c268faaad5d1fff402c792d/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-a12841b727b2577d9d8aa3179f52fe01/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-1b54c087c5775628419b1fa2ead8c3dd/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-6eb8035a189d3c89dad73db4e17e37d8/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-afbcbf74537b1f30362b0eeab0a435f3/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-a7daed77bbfa04ac5514c945059b4e6c/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-900670092204a2262ef6b78a80f79f85/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-101e7928e50cee3d4c4270d5382b476d/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-3de568a9df6ccb4a2de8fa07cbdf5143/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-e27850b5f9b463ae3e6a7876ceaec5d5/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-9b0b465b3e1e2234731cebb6ba8ecb57/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv11lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV11Lepm_WGen_2018-ebcfbb8a7549044c1f5e9ac3a76824d7/USER', 98449)


#second round of track rescaler -> straight fits past 200 GeV 
#note : 2018 was submitted before big merge w/ Peace's UL_Lepton updates
qcdmupt15_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2ef2d5f8dc5fa8d9eb726b3f58e27515/USER', 2232)
qcdempt015_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6e23252bcb631202086e097f926aaad1/USER', 2)
qcdempt020_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-64fcfd9ceb8ef7bda1742bf0efd6908c/USER', 0)
qcdempt030_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-97dfa45c2b57990619bef70eea027ad7/USER', 2)
qcdempt050_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ec383c0b5806344bd6191963af9c1c14/USER', 6)
qcdempt080_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0fb69d55e272959cd36bdeaca306072c/USER', 23)
qcdempt120_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-4fd036688e688d7de7b6afe42d251e1f/USER', 45)
qcdempt170_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-842db9e178690b1190a156062ddf2332/USER', 21)
qcdbctoept015_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-e48cb7470f694af578afc0e2521844d3/USER', 0)
qcdbctoept020_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-45e5eca46387849384384ef124903050/USER', 1)
qcdbctoept030_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-590afc641ec759945744e586804820c0/USER', 67)
qcdbctoept080_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-749dfa02e3e98e61fffb62aa4d5cb1b0/USER', 202)
qcdbctoept170_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-7fe8fdfbf40c513466392395564a4c63/USER', 396)
qcdbctoept250_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-87be3a9175ae61785f3b98da56a10af7/USER', 434)
qcdempt300_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5be2acab74d046459e517d4111eba551/USER', 33)
ttbar_lep_2018.add_dataset('ntupleulv12lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-577c5574e26b062ab4289f39f61d8db3/USER', 4531160)
ttbar_semilep_2018.add_dataset('ntupleulv12lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2428d0c4cad0ff255c704e4bb7ccabd2/USER', 9234609)
ttbar_had_2018.add_dataset('ntupleulv12lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-fe1fcd8737cf48d1cc64b42188161405/USER', 16882)
# wjetstolnu_2018.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-afbf4796e8b2b49e769bc1f54d39418e/USER', 11803)
#wjetstolnu_ext_2018.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c0e7fc9b48d689c98216b8dfedf7fa0d/USER', 11709)
dyjetstollM10_2018.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3aa02e44d01214ab8ecc49a806311ea6/USER', 992)
dyjetstollM50_2018.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-81165c7da7f89a6d0e7d5f9299123153/USER', 35279)
ww_2018.add_dataset('ntupleulv12lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2111925ad37132244b29eacd0b07bcb9/USER', 4426)
wz_2018.add_dataset('ntupleulv12lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-99d7244c913abdbc0b43457068395032/USER', 4357)
zz_2018.add_dataset('ntupleulv12lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-16c16886c353efb77dc82661423c76ce/USER', 2604)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f64a4788209b08080588cf0668af606a/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6131c6d2ff15fe3944d9b903570c5244/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7cc6d68992edd148af97f40648bed159/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-df8dbc33c6904fd1e6d7ad97ab6ab726/USER', 198147)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2f1ad82d010a19c20e51af84ecb137c2/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-75410f888fe7e1befe6677892aed1c0f/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f0a93cf76d090f49e1189b5c42fbf5e0/USER', 202015)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-29636b78b9fb994fb2990d3b3b520c10/USER', 196585)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e86b01dc6e32c174d6db1d8b1586a527/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5c025de4714e5ebe19e95ad51445be42/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-73727bd0d84a34842e78ef7e7f6bfbc4/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1bc1c71b915040160e7c3ebfcbed3975/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f3767e6595f3fd4596edfbec1ca95c8d/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d9585e16303dcbcf43b8f679d337f3e3/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3d68d88dd4e550a470ee6a25fb740794/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-45f46c174ead664bf295d57f83cc403b/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3e7e6e3910175cdb885b16b807d3bd11/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-4134d3667c4371943954dfc440ffdf8e/USER', 195016)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b87c2911e73fc97c896b4018e0582b39/USER', 197845)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-40ae1efd24467fa098b2668986c24079/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-dd40227446fe3e3f22688eabf9bea424/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2a950bdbbb42ef18fef034467cb88d7e/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9cee0bc6189e22a1f0a43149c6de73d9/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c7f60633c8fc8d3efc33ce485e16729b/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5d226f18508a0efcafb3edf450595522/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c978728517893075d6906e27d032f615/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d643dc7047df4450dc280b7f3341b3d7/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-966017dcc3c031f2f90035fb001cbeb9/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0b9e948adbb2f209cbab98e8df5477c1/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-82cb5f02690d3c1fcdf13943bd430650/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e2c75184ac9c6d912bcbde6885a966ed/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6b50b15908fff4972a0f0ac9f3b506ca/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-99f3a3888cf58e39d0c55fbf9dca3186/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e6fe58e40b9c8d77a34a01e004979fff/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7d9a00d4611507241de10a602f799485/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ccab34399728547936d5641efd8a9fcb/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5e6c47ae0dbb99075e468f75cd58c540/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0f6cdfcbe5d71cfc81f5b4579e57f358/USER', 199812)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b801762924f27ae09ad650e57dd7074a/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-56d8e869d9a686ae8b7b49e74112ada6/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-749e19d9faf8079e001cba6648dd471e/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b47363b9094008928443d7284bb7bad4/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1a186ba792138d47e00ec44bf8874aa2/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b1e135e9a16b33274b9795e762657425/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2dbb1da7f2a0447af30882b07181ecca/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5d550f606c58f6c12215832ccf3b95b5/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-82249d3805d251ee4195394f2bb5af50/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8fafa546f9bdb90c53b45ede035a5b5c/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-66152a1002d7f79beed48c8abd1b1fa7/USER', 100146)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-55824fc0313ab0fd4d21e9c370f8ed20/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c0a593309390442db9e2cbfc9f27da71/USER', 196994)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ef947dc454c9b25232bbc6f96eae5569/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f8a50cb5cf0cd141770d4d42b15b78bd/USER', 200411)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-fb8bb562d3235f62f8caec41875d8a8c/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c668be94cdf6b936e89286271a36cb35/USER', 201583)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e86c1b87ea09bf6a4cd7e03bb88054c4/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-44dd604a147fa780d47f44607244a3ea/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-614834ccde45abfee4f2889d7dfd2de5/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c694e8cebeab9d1d246684f49da935a5/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3862b31eedac32eb2c3387b36d8dc94f/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5e1cc23ca855c29ae29eb225665fcd53/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2b66ccd856052b525386bb52f82db29c/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c26268444bcb3ad5365ba45e88898112/USER', 199099)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7540feb7a79f64d78fe65a138ab24cf1/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-a4a12700ff051aff39691d4aabb05e9d/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-46e5832aafbba6b9be251caa03f8991a/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3f8e73dd9fe0e0976423c24c849352e4/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-474946ea5850bffd43021b04fa793349/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e2d50f7815a8f1d9ae55f2141fa7083a/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ee5ca19978ea2c729f5c6ad92c430966/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c173c9df8f39452743c73e75d367439f/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7a1cb6c5edb799d29f46c00200b052b3/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-494bbb00a9dcec1337b36b3e46c614ed/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-32a7f31444c0b558d8298fbd7918d704/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-73b177ba63e4bd13c2822197d0ee1914/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-54b85f2f8d94beebe935379fc6b39743/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6f4e6fcdbce19cba47d4ea7f74c15724/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8dc045142699ba35552f179fefefdede/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-59a9ac03007b091e92911961f793f0c0/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1fc1d8b78d3da55dae46a66305f59774/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f6af79a9240737ffc1449e38779b8455/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-07239d5ea52f5a521c9b6e3c6ec84568/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-53d897d1b5ce2c67da3ec5833c874af7/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5bbd61a1a83c63ba4946436f47c6f9bb/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9ef9ef4d8691037e85318cd2058dda18/USER', 199952)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-65b0aa212e552ada0dcffe4b2c2bd9b3/USER', 200045)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-439b175b1bbacf6685bddfbfa70a0c1e/USER', 194781)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e33769003a0bda52a88e890ebfa4b36b/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-37d08a616a4dacef8b41f37123fa717a/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-807b33de42ff77fad74c8da8b45e4700/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5eb08a4cb1508fdae08e45ed6555d68d/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-146b50de22e7ae61bbe98de4928e81d1/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-963e55f3b7a6c48a1d097b2592cf7c05/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b80ef0b14e1064a515d642580ae80dd7/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3550efa110e016918dcfa4174c477ab2/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b7971909445d5b87c241ac132a693079/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-bd5daa745fd614bdcabaf81b5dcaddf3/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-4d26ad70581f9118a094109f0452561a/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-627b5f3b3256a0e0c46b93850b28b015/USER', 93533)


#new updated way of dealing with lepton tracks (getting their track collections from unpackedtrackcandidates)
# qcdempt015_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-81080072e10b8bb32ad7c8b9efd53317/USER', -1)
# qcdmupt15_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-5cb5b97e8fa839cb22d64e0d8e270e1c/USER', -1)
# qcdempt020_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-8ab42841555dcf8b7f38fa082702293d/USER', -1)
# qcdempt030_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-cf789909cddb195d07ba3b8b8e8d4654/USER', -1)
# qcdempt050_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-f4d53e05393e67e4eaf57ea7dff563c4/USER', -1)
# qcdempt080_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-a080851cd5a4bd0135edd6591ca3929c/USER', -1)
# qcdempt120_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-b65b1cd0280bc5d9d5bb4bbdc20fe2c3/USER', -1)
# qcdempt170_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-906c7107dfb2a55f0f0ce74977c470e3/USER', -1)
# qcdempt300_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-12e2eeb4b020e7c9d05240730ab948b8/USER', -1)
# qcdbctoept020_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-d10a36e7ab048c37fa4c71f60c1d2e52/USER', -1)
# qcdbctoept030_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-9474da6810b6b72f917c152e90ddeb61/USER', -1)
# qcdbctoept080_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-3db69f237c5237dfb54c348c37479d99/USER', -1)
# qcdbctoept170_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-a2d0cd8e4fc186f20bc08a92fc13fc05/USER', -1)
# qcdbctoept250_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-612671dd991387b5a342e588eb6b7ff3/USER', -1)
# wjetstolnu_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-fc25882ec8d35249401850b30766542d/USER', -1)
# dyjetstollM10_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-eea13692dc1480e298536830551fffe2/USER', -1)
# dyjetstollM50_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-a94d220ce3f9844723fc7e8ca4f60aa8/USER', -1)
# ttbar_lep_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-23ef285c723793319ffaad73e2b64fcc/USER', -1)
# ttbar_semilep_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-77cda344640b4075635c4098e34a94b4/USER', -1)
# ttbar_had_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-f4e798988109e538ba8491c310971011/USER', -1)
# ww_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-594dfe545746512e2b19fefaa214bc8a/USER', -1)
# zz_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-5897b65d7cd5b0d543b6d9b4f5ba4314/USER', -1)
# wz_20161.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e2beab25eba0259e41f6e438b19290c2/USER', -1)
qcdempt015_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e145a1cc4ca70274b4d8930e9f266e93/USER', -1)
qcdmupt15_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e101359b576879b5beb90d7be4f142de/USER', -1)
qcdempt020_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-f0c2ede40768223131b030df8244dd65/USER', -1)
qcdempt030_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-cea7d094f59f97b50cb5470f82267c65/USER', -1)
qcdempt050_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-a33a8c2c4b8c68fd878f042a8d62592f/USER', -1)
qcdempt080_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-d313e54189fb5396c7ee879653abfff9/USER', -1)
qcdempt120_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-ff45ae1fecce27ba2185b107e33b862c/USER', -1)
qcdempt170_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-8bdb3a04f9c826b3d07a4853df3e711a/USER', -1)
qcdempt300_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-99630c71736746952f42dfe860d134d8/USER', -1)
qcdbctoept015_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e81797f0296fc599cb725a72db74a5f0/USER', -1)
qcdbctoept020_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-cc769fb6979b3ac77a2cc7d6c8616e27/USER', -1)
qcdbctoept030_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-d4445c686cf228b1b51bb077fd19f033/USER', -1)
qcdbctoept080_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-cd52bd6558bd47a45d46285f6fd5d7a1/USER', -1)
qcdbctoept170_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-f4c27dc20b03200ee1cd5e5823d98318/USER', -1)
qcdbctoept250_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-3a3121947e3383803e96d61c41e8f077/USER', -1)
#ttbar_lep_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-6d1022a79198e857833e04736d5a3608/USER', -1)
#ttbar_semilep_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-fb5da08188b1526fa412a48b29c96205/USER', -1)
ttbar_had_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-0d97fa28c07a26dabbf1b0468fe5dd54/USER', -1)
wjetstolnu_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-b7c9637ef3610c24dea4766ba4184da4/USER', -1)
dyjetstollM10_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-74a1db7a4b1344e022db79e0596c5d95/USER', -1)
dyjetstollM50_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e5f3943dea755e2b0d94443e76e726fd/USER', -1)
ww_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-679c61a92d2cae61c640be0370fb922f/USER', -1)
zz_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-590cb40d8679d5bdd18ca414a59745a2/USER', -1)
wz_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-3a8183d92bdc03afaba1df0bbd960568/USER', -1)
SingleMuon2017B.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-36ccc3f3144aa11e7f0e4f3068ae20f7/USER', -1)
SingleMuon2017C.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-09659d9c77a7051504a98251b4019eda/USER', -1)
SingleMuon2017D.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-fdebebf2f0e9b1fa8f13130bb2a4a359/USER', -1)
SingleMuon2017E.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-5f3feb8e0113d386964de1cb7034487e/USER', -1)
SingleMuon2017F.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e55d462e2f7bedf9348fc1713fa473e7/USER', -1)
SingleElectron2017B.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-69f6c2f167071290adb202145627e5d5/USER', -1)
SingleElectron2017C.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-8e4411c433d348698ce900fd72927d84/USER', -1)
SingleElectron2017D.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-b0c27ba4627941ef110f1a17ffd7a9d6/USER', -1)
SingleElectron2017E.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-17b7725f8e394f69b06b64970f376147/USER', -1)
SingleElectron2017F.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-ea5b141e2a8c9d0dca0bcdd8156923c8/USER', -1)

# qcdmupt15_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-57e6f8178a34b8e2e5c621fbd6f632a3/USER', -1)
# qcdempt015_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-8d0bb2893ae771ed72a13a93f0ff28c9/USER', -1)
# qcdempt020_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-3d5eb0fadebcc1e3493f805129f7a0c9/USER', -1)
# qcdempt030_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-2e37f609aa2ca796fd82e59b14d5597f/USER', -1)
# qcdempt050_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-774dc24c8b779a18a30de7e1373d2943/USER', -1)
# qcdempt080_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-3d3a9bb4bae29d526c8902418c85effc/USER', -1)
# qcdempt120_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-42d777d6cf8930145836f2245cf9a66a/USER', -1)
# qcdempt170_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-1d67c3a23c63bd7d507a4f12d07afbdd/USER', -1)
# qcdbctoept015_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-d0b90ad6b566c62184a5342be4b52fd5/USER', -1)
# qcdbctoept020_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e83480d57efdb7820616e38d6fdb5536/USER', -1)
# qcdbctoept030_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-8feae7e63c27ba32363c890f5e318a7a/USER', -1)
# qcdbctoept080_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-fa2c4b842370424aa2272aede7372883/USER', -1)
# qcdbctoept170_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-4a1300618c09400df4596982254631dc/USER', -1)
# qcdbctoept250_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-87b1041012c880954aca39539f537372/USER', -1)
# qcdempt300_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-e97fd92089c87691908ca0ccda10c593/USER', -1)
# ttbar_lep_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-15731f77f2342e215e6314a5992dba63/USER', -1)
# ttbar_semilep_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-959dc482742f6915a50e02ee819e91c1/USER', -1)
# ttbar_had_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-10d2d93e1b70fd8d058971094817c0e7/USER', -1)
# wjetstolnu_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-2aceabd1a29ff059c229de694ded997a/USER', -1)
# dyjetstollM10_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-fc205b4664299ead9ec4837f83ee46dd/USER', -1)
# dyjetstollM50_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-058831422f259436c7e1079dc96a60f5/USER', -1)
# ww_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-7b69e4b5d4b6c7c0451b0870a5b53687/USER', -1)
# wz_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-d468d63484c4ae53ade806c07dc4ccf9/USER', -1)
# zz_2018.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-530a12543d526e20cd45f01c47b9a3a5/USER', -1)
# SingleMuon2018A.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-39d6987329e28fc64a913f399c5eb39c/USER', -1)
# SingleMuon2018B.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-b3f78812642aa21ba1d7ed4f7957c085/USER', -1)
# SingleMuon2018C.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-cc25a26af93e8e8c3b64519f437ce73f/USER', -1)
# SingleMuon2018D.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-15c92c5279452db5950e2a0f745e0b44/USER', -1)
# EGamma2018A.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-f2aec5a6f0dfa043e401aad925467bbd/USER', -1)
# EGamma2018B.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-208c5af72da89ca85d487e585df0bea4/USER', -1)
# EGamma2018C.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-df9aa619a845826dc9595de34ffba110/USER', -1)
# EGamma2018D.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-337bc985c82a89c5d68cff2e51677389/USER', -1)


########
# automatic condor declarations for ntuples
########

for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in 'ntuple', 'nr_':
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']
                

########
# other condor declarations, generate condorable dict with Shed/condor_list.py
########
# be careful about the list, some samples are distributed at different samples so it won't work
condorable = {
    "T2_DE_DESY": {
        "miniaod": [] # [MET2017E, MET2018A, MET2018B, zjetstonunuht0100_2018, zjetstonunuht0200_2018, zjetstonunuht0400_2018, zjetstonunuht0600_2018, zjetstonunuht0800_2018, zjetstonunuht1200_2018], #EGamma2018D
        },
    "T3_US_FNALLPC": {
        "miniaod": mfv_splitSUSY_samples_2017
        
        },
    "T1_US_FNAL_Disk": {
        "miniaod": Lepton_data_samples_20161 + mfv_stopdbardbar_samples_2017  #+ diboson_samples_2017 + leptonic_samples_2017 + qcd_lep_samples_2017 + met_samples_2017 # SingleElectron2017B, SingleElectron2017D, SingleElectron2017E, 
        
            #mfv_stoplb_tau010000um_M1000_2017, mfv_stoplb_tau000300um_M1200_2017, mfv_stoplb_tau010000um_M1200_2017, mfv_stoplb_tau001000um_M1200_2017, mfv_stoplb_tau000300um_M1600_2017, mfv_stoplb_tau001000um_M1600_2017, mfv_stoplb_tau000100um_M0300_2017, mfv_stoplb_tau000300um_M0300_2017, mfv_stoplb_tau001000um_M0300_2017, mfv_stoplb_tau001000um_M0400_2017, mfv_stoplb_tau010000um_M0600_2017, mfv_stopld_tau000300um_M1000_2017, mfv_stopld_tau010000um_M1000_2017, mfv_stopld_tau010000um_M1200_2017, mfv_stopld_tau001000um_M1400_2017, mfv_stopld_tau000300um_M1600_2017, mfv_stopld_tau010000um_M0200_2017, mfv_stopld_tau000300um_M0300_2017, mfv_stopld_tau001000um_M0400_2017, mfv_stopld_tau000300um_M0600_2017, mfv_stopld_tau010000um_M0600_2017, mfv_stopld_tau001000um_M0600_2017, mfv_stopld_tau010000um_M0800_2017, mfv_stoplb_tau010000um_M1200_2018, mfv_stoplb_tau001000um_M1200_2018, mfv_stoplb_tau010000um_M1400_2018, mfv_stoplb_tau001000um_M1400_2018, mfv_stoplb_tau010000um_M1600_2018, mfv_stoplb_tau001000um_M1600_2018, mfv_stoplb_tau001000um_M0200_2018, mfv_stoplb_tau010000um_M0300_2018, mfv_stoplb_tau010000um_M0400_2018, mfv_stoplb_tau001000um_M0400_2018, mfv_stoplb_tau001000um_M0600_2018, mfv_stoplb_tau000300um_M0800_2018, mfv_stoplb_tau001000um_M0800_2018, mfv_stopld_tau000300um_M1000_2018, mfv_stopld_tau000300um_M1200_2018, mfv_stopld_tau000100um_M1400_2018, mfv_stopld_tau000100um_M1600_2018, mfv_stopld_tau010000um_M1600_2018, mfv_stopld_tau000300um_M0200_2018, mfv_stopld_tau001000um_M0200_2018, mfv_stopld_tau001000um_M0300_2018, mfv_stopld_tau000300um_M0400_2018, mfv_stopld_tau001000um_M0600_2018],
        },
    "T2_US_Wisconsin": {
       # "miniaod": mfv_stopld_samples_2018 + [mfv_stopld_tau010000um_M0400_2018],
       # "miniaod": [mfv_stopld_tau010000um_M0400_2018],
        },
    "T2_US_Purdue": {
        },
    "T2_US_UCSD": {
       # "miniaod" : [mfv_stoplb_tau000300um_M1000_2017, mfv_stoplb_tau000100um_M1200_2017, mfv_stoplb_tau030000um_M1200_2017, mfv_stoplb_tau030000um_M1400_2017, mfv_stoplb_tau000300um_M1800_2017, mfv_stoplb_tau000100um_M0200_2017, mfv_stoplb_tau000300um_M0200_2017, mfv_stoplb_tau001000um_M0200_2017, mfv_stoplb_tau030000um_M0200_2017, mfv_stoplb_tau010000um_M0300_2017, mfv_stoplb_tau030000um_M0300_2017, mfv_stoplb_tau000100um_M0400_2017, mfv_stoplb_tau000300um_M0400_2017, mfv_stoplb_tau030000um_M0400_2017, mfv_stoplb_tau000100um_M0800_2017, mfv_stoplb_tau000300um_M0800_2017, mfv_stoplb_tau001000um_M0800_2017, mfv_stoplb_tau030000um_M0800_2017, mfv_stopld_tau030000um_M1000_2017, mfv_stopld_tau030000um_M1200_2017, mfv_stopld_tau000100um_M1400_2017, mfv_stopld_tau030000um_M1600_2017, mfv_stopld_tau000300um_M1800_2017, mfv_stopld_tau030000um_M1800_2017, mfv_stopld_tau001000um_M0200_2017, mfv_stopld_tau000100um_M0300_2017, mfv_stopld_tau030000um_M0300_2017, mfv_stopld_tau000100um_M0400_2017, mfv_stopld_tau000300um_M0400_2017, mfv_stopld_tau010000um_M0400_2017, mfv_stopld_tau030000um_M0400_2017, mfv_stopld_tau030000um_M0600_2017, mfv_stopld_tau001000um_M0800_2017, mfv_stopld_tau030000um_M0800_2017, mfv_stoplb_tau000100um_M1000_2018, mfv_stoplb_tau001000um_M1000_2018, mfv_stoplb_tau000100um_M1200_2018, mfv_stoplb_tau030000um_M1600_2018, mfv_stoplb_tau010000um_M1800_2018, mfv_stoplb_tau000300um_M0200_2018, mfv_stoplb_tau010000um_M0200_2018, mfv_stoplb_tau000300um_M0300_2018, mfv_stoplb_tau030000um_M0400_2018, mfv_stoplb_tau000300um_M0600_2018, mfv_stoplb_tau000100um_M0800_2018, mfv_stopld_tau000100um_M1200_2018, mfv_stopld_tau010000um_M1200_2018, mfv_stopld_tau030000um_M1200_2018, mfv_stopld_tau030000um_M1400_2018, mfv_stopld_tau010000um_M1800_2018, mfv_stopld_tau001000um_M1800_2018, mfv_stopld_tau000100um_M0200_2018, mfv_stopld_tau010000um_M0200_2018, mfv_stopld_tau000100um_M0300_2018, mfv_stopld_tau001000um_M0400_2018, mfv_stopld_tau001000um_M0800_2018, mfv_stopld_tau030000um_M0800_2018],
        },
    # "T2_US_Caltech": {
    #     "miniaod" : [mfv_stoplb_tau001000um_M1000_2017, mfv_stoplb_tau030000um_M1000_2017, mfv_stoplb_tau010000um_M0400_2017, mfv_stoplb_tau030000um_M0600_2017, mfv_stoplb_tau010000um_M0800_2017, mfv_stopld_tau030000um_M1400_2017, mfv_stopld_tau001000um_M1600_2017, mfv_stopld_tau000100um_M1800_2017, mfv_stopld_tau030000um_M0200_2017, mfv_stopld_tau000100um_M0600_2017, mfv_stopld_tau000100um_M0800_2017, mfv_stopld_tau001000um_M1000_2018, mfv_stopld_tau001000um_M1600_2018, mfv_stopld_tau000100um_M1800_2018, mfv_stopld_tau030000um_M0200_2018, mfv_stopld_tau030000um_M0300_2018, mfv_stopld_tau000100um_M0600_2018],
    #     },
}

_seen = set()
for site, d in condorable.iteritems():
    if not xrootd_sites.has_key(site):
        raise ValueError('need entry in xrootd_sites for %s' % site)
    for ds, samples in d.iteritems():
        for s in samples:
            if s in _seen:
                raise ValueError('%s duplicated in condorable dict' % s.name)
            _seen.add(s)
            s.datasets[ds].condor = True
            s.datasets[ds].xrootd_url = xrootd_sites[site]

# can only run signal ntuples via condor where we can split by nevents, so require they're all reachable
for s in mfv_splitSUSY_samples_2017:
    if s not in _seen:
        raise ValueError('%s not in condorable dict' % s.name)

########
# other info
########

for ds in 'main', 'miniaod':
    # these in status=PRODUCTION
    #for s in ():
    #    s.datasets[ds].ignore_invalid = True

    # 'PU2017' in dataset can be a lie https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/3128.html
    #for s in qcdht0700_2017, dyjetstollM10_2017, dyjetstollM50_2017, dyjetstollM50ext_2017:
    #    s.datasets[ds].notes['buggedpileup2017'] = True

    # set up jsons
    #for y,ss in (2017, data_samples_2017 + auxiliary_data_samples_2017 + singleelectron_data_samples_2017), (2018, data_samples_2018 + auxiliary_data_samples_2018 + egamma_data_samples_2018):
    for y,ss in (20161, Lepton_data_samples_20161 + BTagCSV_data_samples_20161 + DisplacedJet_data_samples_20161), (20162, Lepton_data_samples_20162 + BTagCSV_data_samples_20162 + DisplacedJet_data_samples_20162), (2017, Lepton_data_samples_2017 + BTagCSV_data_samples_2017 + DisplacedJet_data_samples_2017), (2018, Lepton_data_samples_2018 + BTagCSV_data_samples_2018 + DisplacedJet_data_samples_2018):
        for s in ss:
            s.datasets[ds].json      = json_path('ana_%s.json'      % y)
            s.datasets[ds].json_10pc = json_path('ana_%s_10pc.json' % y)
            s.datasets[ds].json_1pc  = json_path('ana_%s_1pc.json'  % y)

########################################################################

if __name__ == '__main__':
    main(registry)

    import sys, re
    from pprint import pprint
    from JMTucker.Tools import DBS, colors
    from JMTucker.Tools.general import popen

    if 0:
        for year in 2017, 2018:
            for line in file(str(year)):
                if line.startswith('/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S'):
                    model = 'mfv_neu'
                elif line.startswith('/StopStopbarTo2Dbar2D'):
                    model = 'mfv_stopdbardbar'
                else:
                    print 'unrecognized line %r' % line
                    continue
                dataset = line.strip()
                mass, tau_s = re.search(r'M-(\d+)_CTau-(.*)_Tune', line).groups()
                mass, tau, tau_unit = int(mass), int(tau_s[:-2]), tau_s[-2:]
                if tau_unit == 'mm':
                    tau *= 1000
                else:
                    assert tau_unit == 'um'
                if mass in [400,600,800,1200,1600,3000] and tau in [100,300,1000,10000,30000]:
                    nevents = DBS.numevents_in_dataset(dataset)
                    print "    MCSample('%s_tau%06ium_M%04i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)

    if 0:
        for s in all_signal_samples_2017 + all_signal_samples_2018:
            l = DBS.datasets('/%s/*/MINIAODSIM' % s.primary_dataset)
            if len(l) == 1:
                nevents = DBS.numevents_in_dataset(l[0])
                print "_adbp('miniaod', '%s', %i)" % (l[0], nevents)
            else:
                print colors.boldred('no miniaod for %s' % s.name)

    if 0:
        for s in qcd_samples_2017 + ttbar_samples_2017 + qcd_samples_2018 + ttbar_samples_2018:
            s.set_curr_dataset('miniaod')
            il = s.int_lumi_orig / 1000
            nfn = len(s.filenames)
            print s.name, nfn, il, '->', int(400/il*nfn), int(400/il*s.nevents_orig)
