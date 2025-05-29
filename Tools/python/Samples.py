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
        #sample.xsec = 1.254
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
    MCSample('qcdbctoept015_20161', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM',        9381897, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=3.0e5), #FIXME
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

mfv_selected_stopbbarbbar_samples_20161 = [mfv_stopbbarbbar_samples_20161[3], mfv_stopbbarbbar_samples_20161[22]] 

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
    
    MCSample('ZHToSSTodddd_tau100um_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau300um_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau1mm_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau10mm_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau30mm_M15_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 25000), 

    MCSample('ZHToSSTodddd_tau100um_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('ZHToSSTodddd_tau300um_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('ZHToSSTodddd_tau1mm_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau10mm_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau30mm_M40_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 


    MCSample('ZHToSSTodddd_tau100um_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 24998), 
    MCSample('ZHToSSTodddd_tau300um_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
    MCSample('ZHToSSTodddd_tau1mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49990), 
    MCSample('ZHToSSTodddd_tau3mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24996), 
    MCSample('ZHToSSTodddd_tau10mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 49996), 
    MCSample('ZHToSSTodddd_tau30mm_M55_20161', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
]

WplusHToSSTodddd_samples_20161 = [
    
    MCSample('WplusHToSSTodddd_tau100um_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau300um_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau1mm_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau3mm_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau10mm_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau30mm_M15_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 

    MCSample('WplusHToSSTodddd_tau100um_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau300um_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau1mm_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 24998), 
    MCSample('WplusHToSSTodddd_tau3mm_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau10mm_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau30mm_M40_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 24998), 


    MCSample('WplusHToSSTodddd_tau100um_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau300um_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
    MCSample('WplusHToSSTodddd_tau30mm_M55_20161', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
  
]

WminusHToSSTodddd_samples_20161 = [
    
    MCSample('WminusHToSSTodddd_tau100um_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau300um_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau1mm_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau3mm_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau10mm_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau30mm_M15_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 

    MCSample('WminusHToSSTodddd_tau100um_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24998), 
    MCSample('WminusHToSSTodddd_tau300um_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau1mm_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau3mm_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM', 24999), 
    MCSample('WminusHToSSTodddd_tau10mm_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v3/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau30mm_M40_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v1/MINIAODSIM', 24999), 


    MCSample('WminusHToSSTodddd_tau100um_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau300um_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24999), 
    MCSample('WminusHToSSTodddd_tau1mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24995), 
    MCSample('WminusHToSSTodddd_tau3mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
    MCSample('WminusHToSSTodddd_tau10mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24997), 
    MCSample('WminusHToSSTodddd_tau30mm_M55_20161', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM', 24998), 
  
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
    MCSample('qcdbctoept015_20162', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM',        8336997, nice='QCD,  15 < #hat{p}_{T} <  20 GeV, HF electrons', color=801, syst_frac=0.20, xsec=1.862e5),
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
    #MCSample('ttbar_20162',     '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM',                    90609841, nice='t#bar{t}',                                  color=4,   syst_frac=0.15, xsec=831.76),
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
    MCSample('ZHToSSTodddd_tau100um_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau300um_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau1mm_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau10mm_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau30mm_M15_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 

    MCSample('ZHToSSTodddd_tau100um_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau300um_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('ZHToSSTodddd_tau1mm_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 50000), 
    MCSample('ZHToSSTodddd_tau3mm_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau10mm_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49998), 
    MCSample('ZHToSSTodddd_tau30mm_M40_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 


    MCSample('ZHToSSTodddd_tau100um_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('ZHToSSTodddd_tau300um_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau1mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49998), 
    MCSample('ZHToSSTodddd_tau3mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('ZHToSSTodddd_tau10mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 49997), 
    MCSample('ZHToSSTodddd_tau30mm_M55_20162', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    
]

WplusHToSSTodddd_samples_20162 = [
    
    MCSample('WplusHToSSTodddd_tau100um_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau300um_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau1mm_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau3mm_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 24998), 
    MCSample('WplusHToSSTodddd_tau10mm_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau30mm_M15_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 

    MCSample('WplusHToSSTodddd_tau100um_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WplusHToSSTodddd_tau300um_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WplusHToSSTodddd_tau1mm_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24997), 
    MCSample('WplusHToSSTodddd_tau3mm_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau10mm_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 
    MCSample('WplusHToSSTodddd_tau30mm_M40_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 


    MCSample('WplusHToSSTodddd_tau100um_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v1/MINIAODSIM', 24997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24997), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24202), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WplusHToSSTodddd_tau30mm_M55_20162', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    
]

WminusHToSSTodddd_samples_20162 = [
    
    MCSample('WminusHToSSTodddd_tau100um_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau300um_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau1mm_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau3mm_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau10mm_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau30mm_M15_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24246), 

    MCSample('WminusHToSSTodddd_tau100um_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 
    MCSample('WminusHToSSTodddd_tau300um_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24245), 
    MCSample('WminusHToSSTodddd_tau1mm_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WminusHToSSTodddd_tau3mm_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24999), 
    MCSample('WminusHToSSTodddd_tau10mm_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 25000), 
    MCSample('WminusHToSSTodddd_tau30mm_M40_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24996), 


    MCSample('WminusHToSSTodddd_tau100um_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24996), 
    MCSample('WminusHToSSTodddd_tau300um_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WminusHToSSTodddd_tau1mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24998), 
    MCSample('WminusHToSSTodddd_tau3mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 24996), 
    MCSample('WminusHToSSTodddd_tau10mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v3/MINIAODSIM', 24998), 
    MCSample('WminusHToSSTodddd_tau30mm_M55_20162', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16MiniAODv2-106X_mcRun2_asymptotic_v17-v2/MINIAODSIM', 24996), 
    
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
    #MCSample('qcdht0200_2017', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57816581, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    MCSample('qcdht0200_2017', '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 57456603, nice='QCD, 200 < H_{T} < 300 GeV',  color=802, syst_frac=0.20, xsec=1.554e6),
    #MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 57097305, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    MCSample('qcdht0300_2017', '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 56497917, nice='QCD, 300 < H_{T} < 500 GeV',  color=803, syst_frac=0.20, xsec=3.226e5), #xsec not available
    #MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 9183471, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    MCSample('qcdht0500_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 9183471, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    #MCSample('qcdht0500ext_2017', '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6_ext1-v1/AODSIM', 59037642, nice='QCD, 500 < H_{T} < 700 GeV', color=804, syst_frac=0.20, xsec=3.028e4),
    #MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 45774525, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    MCSample('qcdht0700_2017', '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 45613978, nice='QCD, 700 < H_{T} < 1000 GeV',  color=805, syst_frac=0.20, xsec=6.392e3),
    #MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM', 15420054, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    MCSample('qcdht1000_2017', '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 15250184, nice='QCD, 1000 < H_{T} < 1500 GeV', color=806, syst_frac=0.20, xsec=1.096e3), #xsec not available
    #MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM',     7711548, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    MCSample('qcdht1500_2017', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 10581460, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    #MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17RECO-106X_mc2017_realistic_v6-v2/AODSIM',   5451735, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    MCSample('qcdht2000_2017', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 5451735, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
    ]

qcd_lep_samples_2017 = [
    MCSample('qcdmupt15_2017', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM',  17716270, nice='QCD, #hat{p}_{T} > 20 GeV, #mu p_{T} > 15 GeV', color=801, syst_frac=0.20, xsec=2.39e5),
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
    MCSample('dyjetstollM10_2017','/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v1/MINIAODSIM', 68480179, nice='DY + jets #rightarrow ll, 10 < M < 50 GeV', color= 29, syst_frac=0.10, xsec=1.58e4),
    MCSample('dyjetstollM50_2017','/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 103344974, nice='DY + jets #rightarrow ll, M > 50 GeV', color= 32, syst_frac=0.10, xsec=5.34e3),
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
    MCSample('mfv_stopld_tau000100um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201843),
    MCSample('mfv_stopld_tau000300um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199789),
    MCSample('mfv_stopld_tau001000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198275),
    MCSample('mfv_stopld_tau010000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197403),
    MCSample('mfv_stopld_tau030000um_M0200_2017', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198511),
    MCSample('mfv_stopld_tau000100um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197379),
    MCSample('mfv_stopld_tau000300um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197934),
    MCSample('mfv_stopld_tau001000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199705),
    MCSample('mfv_stopld_tau010000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197990),
    MCSample('mfv_stopld_tau030000um_M0300_2017', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199931),
    MCSample('mfv_stopld_tau000100um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 202735),
    MCSample('mfv_stopld_tau000300um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199890),
    MCSample('mfv_stopld_tau001000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 197130),
    MCSample('mfv_stopld_tau010000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201845),
    MCSample('mfv_stopld_tau030000um_M0400_2017', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198731),
    MCSample('mfv_stopld_tau000100um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203406),
    MCSample('mfv_stopld_tau000300um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199321),
    MCSample('mfv_stopld_tau001000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 203302),
    MCSample('mfv_stopld_tau010000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 195818),
    MCSample('mfv_stopld_tau030000um_M0600_2017', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199944),
    MCSample('mfv_stopld_tau000100um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200077),
    MCSample('mfv_stopld_tau000300um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200814),
    MCSample('mfv_stopld_tau001000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200829),
    MCSample('mfv_stopld_tau010000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99313),
    MCSample('mfv_stopld_tau030000um_M0800_2017', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200140),
    MCSample('mfv_stopld_tau000100um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 199076),
    MCSample('mfv_stopld_tau000300um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198992),
    MCSample('mfv_stopld_tau001000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198608),
    MCSample('mfv_stopld_tau010000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98679),
    MCSample('mfv_stopld_tau030000um_M1000_2017', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 199499),
    MCSample('mfv_stopld_tau000100um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198263),
    MCSample('mfv_stopld_tau000300um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 0),
    MCSample('mfv_stopld_tau001000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201191), 
    MCSample('mfv_stopld_tau010000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100349),
    MCSample('mfv_stopld_tau030000um_M1200_2017', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200851),
    MCSample('mfv_stopld_tau000100um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198812),
    MCSample('mfv_stopld_tau000300um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 194591),
    MCSample('mfv_stopld_tau001000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198538),  
    MCSample('mfv_stopld_tau010000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 98583),
    MCSample('mfv_stopld_tau030000um_M1400_2017', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200714),
    MCSample('mfv_stopld_tau000100um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 201051),
    MCSample('mfv_stopld_tau000300um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 196540),
    MCSample('mfv_stopld_tau001000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99126),
    MCSample('mfv_stopld_tau010000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100274),
    MCSample('mfv_stopld_tau030000um_M1600_2017', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 100345),
    MCSample('mfv_stopld_tau000100um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 200828),
    MCSample('mfv_stopld_tau000300um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 198147),
    MCSample('mfv_stopld_tau001000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 101005), 
    MCSample('mfv_stopld_tau010000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99667),
    MCSample('mfv_stopld_tau030000um_M1800_2017', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 99787),
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
    MCSample('WplusHToSSTodddd_tau10mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WplusHToSSTodddd_tau30mm_M15_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    
    MCSample('WplusHToSSTodddd_tau100um_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau300um_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49996), 
    MCSample('WplusHToSSTodddd_tau1mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau3mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WplusHToSSTodddd_tau10mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WplusHToSSTodddd_tau30mm_M40_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49992),
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
]

WplusHToSSTodddd_samples_2017Mu = [

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49992),
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
]

WplusHToSSTodddd_samples_2017Ele = [

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49992),
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
]

WplusHToSSTodddd_samples_2017Lep = [

    MCSample('WplusHToSSTodddd_tau100um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WplusHToSSTodddd_tau300um_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49995), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau3mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49991), 
    MCSample('WplusHToSSTodddd_tau10mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49992),
    MCSample('WplusHToSSTodddd_tau30mm_M55_2017', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 47998), 
    
]

WminusHToSSTodddd_samples_2017 = [
    
    MCSample('WminusHToSSTodddd_tau100um_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49999), 
    MCSample('WminusHToSSTodddd_tau300um_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 50000), 
    MCSample('WminusHToSSTodddd_tau1mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau3mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48999), 
    MCSample('WminusHToSSTodddd_tau10mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 
    MCSample('WminusHToSSTodddd_tau30mm_M15_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 50000), 

    MCSample('WminusHToSSTodddd_tau100um_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 50000), 
    MCSample('WminusHToSSTodddd_tau300um_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau1mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 48000), 
    MCSample('WminusHToSSTodddd_tau3mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49997), 
    MCSample('WminusHToSSTodddd_tau10mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49999), 
    MCSample('WminusHToSSTodddd_tau30mm_M40_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM', 49998), 
   
    MCSample('WminusHToSSTodddd_tau100um_M55_2017', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v3/MINIAODSIM', 49995), 
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
    #MCSample('qcdht1500_2018', '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM', 10615310, nice='QCD, 1500 < H_{T} < 2000 GeV', color=807, syst_frac=0.20, xsec=99.0), #xsec not available
    #MCSample('qcdht2000_2018', '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8/RunIISummer19UL18RECO-106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM',   4532754, nice='QCD, H_{T} > 2000',            color=808, syst_frac=0.20, xsec=21.93),
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
    #MCSample('ttbar_2018',            '/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',            306142112, nice='t#bar{t}',                   color=4,   syst_frac=0.15, xsec=7.572e+02),
    MCSample('ttbar_lep_2018',            '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',             146010000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=88.29),
    MCSample('ttbar_semilep_2018', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM',             478982000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=365.34),
    MCSample('ttbar_had_2018',         '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM',             343248000, nice='t#bar{t}',                                 color=4,   syst_frac=0.15, xsec=377.96),
]

bjet_samples_2018 = []

leptonic_samples_2018 = [
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

#should also add Wqq? need to double check this XS need a better name ...?
Zqq_samples_2018 = [
    MCSample('zjetstoqqht0200_2018', '/ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 14808858, nice='Z + jets #rightarrow qq 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=1002.0),
    MCSample('zjetstoqqht0400_2018', '/ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 13930474, nice='Z + jets #rightarrow qq 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=116.6),
    MCSample('zjetstoqqht0600_2018', '/ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 12029507, nice='Z + jets #rightarrow qq 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=25.47),
    MCSample('zjetstoqqht0800_2018', '/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 9681521, nice='Z + jets #rightarrow qq H_{T} > 800 GeV', color=1, syst_frac=0.20, xsec=12.99),
    MCSample('wjetstoqqht0200_2018', '/WJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 14494966, nice='W + jets #rightarrow qq 200 < H_{T} < 400 GeV', color=1, syst_frac=0.20, xsec=2546.0),
    MCSample('wjetstoqqht0400_2018', '/WJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 9335298, nice='W + jets #rightarrow qq 400 < H_{T} < 600 GeV', color=1, syst_frac=0.20, xsec=275.4),
    MCSample('wjetstoqqht0600_2018', '/WJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 13633226, nice='W + jets #rightarrow qq 600 < H_{T} < 800 GeV', color=1, syst_frac=0.20, xsec=59.55),
    MCSample('wjetstoqqht0800_2018', '/WJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 13581343, nice='W + jets #rightarrow qq H_{T} > 800 GeV', color=1, syst_frac=0.20, xsec=29.1),
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
   
    MCSample('ZHToSSTodddd_tau100um_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 49999),
    MCSample('ZHToSSTodddd_tau300um_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 50000),
    MCSample('ZHToSSTodddd_tau1mm_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('ZHToSSTodddd_tau3mm_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('ZHToSSTodddd_tau10mm_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('ZHToSSTodddd_tau30mm_M15_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    
    
    MCSample('ZHToSSTodddd_tau100um_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('ZHToSSTodddd_tau300um_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49145),
    MCSample('ZHToSSTodddd_tau1mm_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('ZHToSSTodddd_tau3mm_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('ZHToSSTodddd_tau10mm_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('ZHToSSTodddd_tau30mm_M40_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),

    
    MCSample('ZHToSSTodddd_tau100um_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 49992),
    MCSample('ZHToSSTodddd_tau300um_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49995),
    MCSample('ZHToSSTodddd_tau1mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999), 
    MCSample('ZHToSSTodddd_tau3mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 49998), 
    MCSample('ZHToSSTodddd_tau10mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49996), 
    MCSample('ZHToSSTodddd_tau30mm_M55_2018', '/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49996),

]

WplusHToSSTodddd_samples_2018 = [

    MCSample('WplusHToSSTodddd_tau100um_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('WplusHToSSTodddd_tau300um_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('WplusHToSSTodddd_tau1mm_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('WplusHToSSTodddd_tau3mm_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM', 49998),
    MCSample('WplusHToSSTodddd_tau10mm_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('WplusHToSSTodddd_tau30mm_M15_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),

    MCSample('WplusHToSSTodddd_tau100um_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('WplusHToSSTodddd_tau300um_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WplusHToSSTodddd_tau1mm_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('WplusHToSSTodddd_tau3mm_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WplusHToSSTodddd_tau10mm_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WplusHToSSTodddd_tau30mm_M40_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),


    MCSample('WplusHToSSTodddd_tau100um_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994),
    MCSample('WplusHToSSTodddd_tau300um_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994), 
    MCSample('WplusHToSSTodddd_tau1mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994),
    MCSample('WplusHToSSTodddd_tau3mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49991),
    MCSample('WplusHToSSTodddd_tau10mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 48993),
    MCSample('WplusHToSSTodddd_tau30mm_M55_2018', '/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49996),
    
]

WminusHToSSTodddd_samples_2018 = [
    
    MCSample('WminusHToSSTodddd_tau100um_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('WminusHToSSTodddd_tau300um_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 49999),
    MCSample('WminusHToSSTodddd_tau1mm_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WminusHToSSTodddd_tau3mm_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),
    MCSample('WminusHToSSTodddd_tau10mm_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 50000),
    MCSample('WminusHToSSTodddd_tau30mm_M15_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-15_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 50000),    

    MCSample('WminusHToSSTodddd_tau100um_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 48998),
    MCSample('WminusHToSSTodddd_tau300um_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('WminusHToSSTodddd_tau1mm_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 49996),
    MCSample('WminusHToSSTodddd_tau3mm_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),
    MCSample('WminusHToSSTodddd_tau10mm_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WminusHToSSTodddd_tau30mm_M40_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-40_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49998),


    MCSample('WminusHToSSTodddd_tau100um_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49993),
    MCSample('WminusHToSSTodddd_tau300um_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-0p3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49992),
    MCSample('WminusHToSSTodddd_tau1mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49995),
    MCSample('WminusHToSSTodddd_tau3mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-3_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v3/MINIAODSIM', 49994),
    MCSample('WminusHToSSTodddd_tau10mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-10_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49999),
    MCSample('WminusHToSSTodddd_tau30mm_M55_2018', '/WminusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-30_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM', 49994),

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
    #DataSample('SingleElectron20161B1', '/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161B2', '/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161C',  '/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161D',  '/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SingleElectron20161E',  '/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2-v5/MINIAOD'),
    DataSample('SingleElectron20161F',  '/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SinglePhoton20161B', '/SinglePhoton/Run2016B-ver2_HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SinglePhoton20161C', '/SinglePhoton/Run2016C-HIPM_UL2016_MiniAODv2-v4/MINIAOD'),
    DataSample('SinglePhoton20161D', '/SinglePhoton/Run2016D-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SinglePhoton20161E', '/SinglePhoton/Run2016E-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SinglePhoton20161F', '/SinglePhoton/Run2016F-HIPM_UL2016_MiniAODv2-v2/MINIAOD'),

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
    DataSample('SinglePhoton20162F', '/SinglePhoton/Run2016F-UL2016_MiniAODv2-v2/MINIAOD'),
    DataSample('SinglePhoton20162G', '/SinglePhoton/Run2016G-UL2016_MiniAODv2-v3/MINIAOD'),
    DataSample('SinglePhoton20162H', '/SinglePhoton/Run2016H-UL2016_MiniAODv2-v2/MINIAOD'),

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
    #DataSample('BTagCSV2017B', '/BTagCSV/Run2017B-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('BTagCSV2017C', '/BTagCSV/Run2017C-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('BTagCSV2017D', '/BTagCSV/Run2017D-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('BTagCSV2017E', '/BTagCSV/Run2017E-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('BTagCSV2017F', '/BTagCSV/Run2017F-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('BTagCSV2017B', '/BTagCSV/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('BTagCSV2017C', '/BTagCSV/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('BTagCSV2017D', '/BTagCSV/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('BTagCSV2017E', '/BTagCSV/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('BTagCSV2017F', '/BTagCSV/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
    ]

DisplacedJet_data_samples_2017 = [
    #DataSample('DisplacedJet2017C', '/DisplacedJet/Run2017C-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('DisplacedJet2017D', '/DisplacedJet/Run2017D-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('DisplacedJet2017E', '/DisplacedJet/Run2017E-09Aug2019_UL2017-v1/MINIAOD'),
    #DataSample('DisplacedJet2017F', '/DisplacedJet/Run2017F-09Aug2019_UL2017-v1/MINIAOD'),
    DataSample('DisplacedJet2017C', '/DisplacedJet/Run2017C-UL2017_MiniAODv2-v2/MINIAOD'),
    DataSample('DisplacedJet2017D', '/DisplacedJet/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('DisplacedJet2017E', '/DisplacedJet/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('DisplacedJet2017F', '/DisplacedJet/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
    ]

Lepton_data_samples_2017 = [
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
    DataSample('SinglePhoton2017B', '/SinglePhoton/Run2017B-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SinglePhoton2017C', '/SinglePhoton/Run2017C-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SinglePhoton2017D', '/SinglePhoton/Run2017D-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SinglePhoton2017E', '/SinglePhoton/Run2017E-UL2017_MiniAODv2-v1/MINIAOD'),
    DataSample('SinglePhoton2017F', '/SinglePhoton/Run2017F-UL2017_MiniAODv2-v1/MINIAOD'),
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
    DataSample('SingleMuon2018A', '/SingleMuon/Run2018A-UL2018_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2018B', '/SingleMuon/Run2018B-UL2018_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('SingleMuon2018C', '/SingleMuon/Run2018C-UL2018_MiniAODv2_GT36-v3/MINIAOD'),
    DataSample('SingleMuon2018D', '/SingleMuon/Run2018D-UL2018_MiniAODv2_GT36-v2/MINIAOD'),
    DataSample('EGamma2018A', '/EGamma/Run2018A-UL2018_MiniAODv2_GT36-v1/MINIAOD'),
    DataSample('EGamma2018B', '/EGamma/Run2018B-UL2018_MiniAODv2_GT36-v1/MINIAOD'),
    DataSample('EGamma2018C', '/EGamma/Run2018C-UL2018_MiniAODv2_GT36-v1/MINIAOD'),
    DataSample('EGamma2018D', '/EGamma/Run2018D-UL2018_MiniAODv2_GT36-v3/MINIAOD'),
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
    # 'WplusHToSSTodddd_samples_20161',
    'WminusHToSSTodddd_samples_20161',
    'ggHToSSTodddd_samples_20161',
    'ZHToSSTodddd_samples_20162',
    # 'WplusHToSSTodddd_samples_20162',
    'WminusHToSSTodddd_samples_20162',
    'ggHToSSTodddd_samples_20162',
    #'HToSSTobbbb_samples_2017',
    'ggHToSSTodddd_samples_2017',
    'ggHToSSTo4l_samples_2017',
    'ZHToSSTodddd_samples_2017',
    # 'WplusHToSSTodddd_samples_2017',
    # 'WplusHToSSTodddd_samples_2017Mu',
    # 'WplusHToSSTodddd_samples_2017Ele',
    # 'WplusHToSSTodddd_samples_2017Lep',
    'WminusHToSSTodddd_samples_2017',
    'qcd_samples_2018',
    'qcd_lep_samples_2018',
    'ttbar_samples_2018',
    'bjet_samples_2018',
    'leptonic_samples_2018',
    'met_samples_2018',
    'diboson_samples_2018',
    'Zvv_samples_2018',
    'Zqq_samples_2018',
    'mfv_splitSUSY_samples_2018',
    'mfv_signal_samples_2018',
    'mfv_stopdbardbar_samples_2018',
    'mfv_stopbbarbbar_samples_2018',
    'mfv_stoplb_samples_2018',
    'mfv_stopld_samples_2018',
    'ZHToSSTodddd_samples_2018',
    # 'WplusHToSSTodddd_samples_2018',
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


for sample in qcd_samples_2018 + qcd_lep_samples_2018 + leptonic_samples_2018 + diboson_samples_2018 + met_samples_2018 + ttbar_samples_2018 + Zqq_samples_2018: 
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
for sample in WplusHToSSTodddd_samples_2017Mu :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2017Lep :
    sample.add_dataset('miniaod', sample.dataset, sample.nevents_orig)
for sample in WplusHToSSTodddd_samples_2017Ele :
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

ww_2018.add_dataset('trackmoverulv12lepmofftossv8', '/FakeDataset/fakefile-FakePublish-c86795bafeab2ee1900f00da0cbfe2cc/USER', -1)
# wz_2018.add_dataset('trackmoverulv12lepmofftossv8', '/FakeDataset/fakefile-FakePublish-728f2ab7e8b8c6d1c111f3d5d76436ae/USER', -1)
# zz_2018.add_dataset('trackmoverulv12lepmofftossv8', '/FakeDataset/fakefile-FakePublish-d5e140db62063bcebfba9bbfbd70d3e1/USER', -1)
#ww_2018.add_dataset('trackmoverulv12lepmofftossv8')

#ww_20161.add_dataset('trackmoverulv12lepmofftossv8', '/FakeDataset/fakefile-FakePublish-420c23010c26d46e528d6d85f444b280/USER', -1) #this does not have lepton moved to jet - test
ww_20161.add_dataset('trackmoverulv12lepmofftossv8', '/FakeDataset/fakefile-FakePublish-c2915a376c69481dbbffcd0c5d3e2f50/USER', -1) #this has lepton moved to jet - test (but updated Ntuple I think?)



# for x in ZHToSSTodddd_tau100um_M15_20161, ZHToSSTodddd_tau300um_M15_20161, ZHToSSTodddd_tau1mm_M15_20161, ZHToSSTodddd_tau3mm_M15_20161, ZHToSSTodddd_tau10mm_M15_20161, ZHToSSTodddd_tau30mm_M15_20161, ZHToSSTodddd_tau100um_M40_20161, ZHToSSTodddd_tau300um_M40_20161, ZHToSSTodddd_tau1mm_M40_20161, ZHToSSTodddd_tau3mm_M40_20161, ZHToSSTodddd_tau10mm_M40_20161, ZHToSSTodddd_tau30mm_M40_20161, ZHToSSTodddd_tau100um_M55_20161, ZHToSSTodddd_tau300um_M55_20161, ZHToSSTodddd_tau1mm_M55_20161, ZHToSSTodddd_tau3mm_M55_20161, ZHToSSTodddd_tau10mm_M55_20161, ZHToSSTodddd_tau30mm_M55_20161, WplusHToSSTodddd_tau100um_M15_20161, WplusHToSSTodddd_tau300um_M15_20161, WplusHToSSTodddd_tau1mm_M15_20161, WplusHToSSTodddd_tau3mm_M15_20161, WplusHToSSTodddd_tau10mm_M15_20161, WplusHToSSTodddd_tau30mm_M15_20161, WplusHToSSTodddd_tau100um_M40_20161, WplusHToSSTodddd_tau300um_M40_20161, WplusHToSSTodddd_tau1mm_M40_20161, WplusHToSSTodddd_tau3mm_M40_20161, WplusHToSSTodddd_tau10mm_M40_20161, WplusHToSSTodddd_tau30mm_M40_20161, WplusHToSSTodddd_tau100um_M55_20161, WplusHToSSTodddd_tau300um_M55_20161, WplusHToSSTodddd_tau1mm_M55_20161, WplusHToSSTodddd_tau3mm_M55_20161, WplusHToSSTodddd_tau10mm_M55_20161, WplusHToSSTodddd_tau30mm_M55_20161, WminusHToSSTodddd_tau100um_M15_20161, WminusHToSSTodddd_tau300um_M15_20161, WminusHToSSTodddd_tau1mm_M15_20161, WminusHToSSTodddd_tau3mm_M15_20161, WminusHToSSTodddd_tau10mm_M15_20161, WminusHToSSTodddd_tau30mm_M15_20161, WminusHToSSTodddd_tau100um_M40_20161, WminusHToSSTodddd_tau300um_M40_20161, WminusHToSSTodddd_tau1mm_M40_20161, WminusHToSSTodddd_tau3mm_M40_20161, WminusHToSSTodddd_tau10mm_M40_20161, WminusHToSSTodddd_tau30mm_M40_20161, WminusHToSSTodddd_tau100um_M55_20161, WminusHToSSTodddd_tau300um_M55_20161, WminusHToSSTodddd_tau1mm_M55_20161, WminusHToSSTodddd_tau3mm_M55_20161, WminusHToSSTodddd_tau10mm_M55_20161, WminusHToSSTodddd_tau30mm_M55_20161, ZHToSSTodddd_tau100um_M15_20162, ZHToSSTodddd_tau300um_M15_20162, ZHToSSTodddd_tau1mm_M15_20162, ZHToSSTodddd_tau3mm_M15_20162, ZHToSSTodddd_tau10mm_M15_20162, ZHToSSTodddd_tau30mm_M15_20162, ZHToSSTodddd_tau100um_M40_20162, ZHToSSTodddd_tau300um_M40_20162, ZHToSSTodddd_tau3mm_M40_20162, ZHToSSTodddd_tau10mm_M40_20162, ZHToSSTodddd_tau30mm_M40_20162, ZHToSSTodddd_tau100um_M55_20162, ZHToSSTodddd_tau300um_M55_20162, ZHToSSTodddd_tau3mm_M55_20162, ZHToSSTodddd_tau10mm_M55_20162, ZHToSSTodddd_tau30mm_M55_20162, WplusHToSSTodddd_tau100um_M15_20162, WplusHToSSTodddd_tau300um_M15_20162, WplusHToSSTodddd_tau1mm_M15_20162, WplusHToSSTodddd_tau3mm_M15_20162, WplusHToSSTodddd_tau10mm_M15_20162, WplusHToSSTodddd_tau30mm_M15_20162, WplusHToSSTodddd_tau100um_M40_20162, WplusHToSSTodddd_tau300um_M40_20162, WplusHToSSTodddd_tau1mm_M40_20162, WplusHToSSTodddd_tau3mm_M40_20162, WplusHToSSTodddd_tau10mm_M40_20162, WplusHToSSTodddd_tau30mm_M40_20162, WplusHToSSTodddd_tau100um_M55_20162, WplusHToSSTodddd_tau300um_M55_20162, WplusHToSSTodddd_tau1mm_M55_20162, WplusHToSSTodddd_tau3mm_M55_20162, WplusHToSSTodddd_tau10mm_M55_20162, WplusHToSSTodddd_tau30mm_M55_20162, WminusHToSSTodddd_tau100um_M15_20162, WminusHToSSTodddd_tau300um_M15_20162, WminusHToSSTodddd_tau1mm_M15_20162, WminusHToSSTodddd_tau3mm_M15_20162, WminusHToSSTodddd_tau10mm_M15_20162, WminusHToSSTodddd_tau100um_M40_20162, WminusHToSSTodddd_tau300um_M40_20162, WminusHToSSTodddd_tau1mm_M40_20162, WminusHToSSTodddd_tau3mm_M40_20162, WminusHToSSTodddd_tau10mm_M40_20162, WminusHToSSTodddd_tau30mm_M40_20162, WminusHToSSTodddd_tau100um_M55_20162, WminusHToSSTodddd_tau300um_M55_20162, WminusHToSSTodddd_tau1mm_M55_20162, WminusHToSSTodddd_tau3mm_M55_20162, WminusHToSSTodddd_tau10mm_M55_20162, WminusHToSSTodddd_tau30mm_M55_20162, ZHToSSTodddd_tau100um_M15_2017, ZHToSSTodddd_tau300um_M15_2017, ZHToSSTodddd_tau1mm_M15_2017, ZHToSSTodddd_tau3mm_M15_2017, ZHToSSTodddd_tau10mm_M15_2017, ZHToSSTodddd_tau30mm_M15_2017, ZHToSSTodddd_tau100um_M40_2017, ZHToSSTodddd_tau300um_M40_2017, ZHToSSTodddd_tau1mm_M40_2017, ZHToSSTodddd_tau3mm_M40_2017, ZHToSSTodddd_tau10mm_M40_2017, ZHToSSTodddd_tau30mm_M40_2017, ZHToSSTodddd_tau100um_M55_2017, ZHToSSTodddd_tau300um_M55_2017, ZHToSSTodddd_tau1mm_M55_2017, ZHToSSTodddd_tau3mm_M55_2017, ZHToSSTodddd_tau10mm_M55_2017, ZHToSSTodddd_tau30mm_M55_2017, WplusHToSSTodddd_tau100um_M15_2017, WplusHToSSTodddd_tau300um_M15_2017, WplusHToSSTodddd_tau1mm_M15_2017, WplusHToSSTodddd_tau3mm_M15_2017, WplusHToSSTodddd_tau10mm_M15_2017, WplusHToSSTodddd_tau30mm_M15_2017, WplusHToSSTodddd_tau100um_M40_2017, WplusHToSSTodddd_tau300um_M40_2017, WplusHToSSTodddd_tau1mm_M40_2017, WplusHToSSTodddd_tau3mm_M40_2017, WplusHToSSTodddd_tau10mm_M40_2017, WplusHToSSTodddd_tau30mm_M40_2017, WplusHToSSTodddd_tau100um_M55_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017, WplusHToSSTodddd_tau3mm_M55_2017, WplusHToSSTodddd_tau10mm_M55_2017, WplusHToSSTodddd_tau30mm_M55_2017, WminusHToSSTodddd_tau100um_M15_2017, WminusHToSSTodddd_tau300um_M15_2017, WminusHToSSTodddd_tau1mm_M15_2017, WminusHToSSTodddd_tau3mm_M15_2017, WminusHToSSTodddd_tau10mm_M15_2017, WminusHToSSTodddd_tau30mm_M15_2017, WminusHToSSTodddd_tau100um_M40_2017, WminusHToSSTodddd_tau300um_M40_2017, WminusHToSSTodddd_tau1mm_M40_2017, WminusHToSSTodddd_tau3mm_M40_2017, WminusHToSSTodddd_tau10mm_M40_2017, WminusHToSSTodddd_tau30mm_M40_2017, WminusHToSSTodddd_tau100um_M55_2017, WminusHToSSTodddd_tau300um_M55_2017, WminusHToSSTodddd_tau1mm_M55_2017, WminusHToSSTodddd_tau3mm_M55_2017, WminusHToSSTodddd_tau10mm_M55_2017, WminusHToSSTodddd_tau30mm_M55_2017, ZHToSSTodddd_tau100um_M15_2018, ZHToSSTodddd_tau300um_M15_2018, ZHToSSTodddd_tau1mm_M15_2018, ZHToSSTodddd_tau3mm_M15_2018, ZHToSSTodddd_tau10mm_M15_2018, ZHToSSTodddd_tau30mm_M15_2018, ZHToSSTodddd_tau100um_M40_2018, ZHToSSTodddd_tau300um_M40_2018, ZHToSSTodddd_tau1mm_M40_2018, ZHToSSTodddd_tau3mm_M40_2018, ZHToSSTodddd_tau10mm_M40_2018, ZHToSSTodddd_tau30mm_M40_2018, ZHToSSTodddd_tau100um_M55_2018, ZHToSSTodddd_tau300um_M55_2018, ZHToSSTodddd_tau1mm_M55_2018, ZHToSSTodddd_tau3mm_M55_2018, ZHToSSTodddd_tau10mm_M55_2018, ZHToSSTodddd_tau30mm_M55_2018, WplusHToSSTodddd_tau100um_M15_2018, WplusHToSSTodddd_tau300um_M15_2018, WplusHToSSTodddd_tau1mm_M15_2018, WplusHToSSTodddd_tau3mm_M15_2018, WplusHToSSTodddd_tau10mm_M15_2018, WplusHToSSTodddd_tau30mm_M15_2018, WplusHToSSTodddd_tau100um_M40_2018, WplusHToSSTodddd_tau300um_M40_2018, WplusHToSSTodddd_tau3mm_M40_2018, WplusHToSSTodddd_tau10mm_M40_2018, WplusHToSSTodddd_tau30mm_M40_2018, WplusHToSSTodddd_tau100um_M55_2018, WplusHToSSTodddd_tau300um_M55_2018, WplusHToSSTodddd_tau1mm_M55_2018, WplusHToSSTodddd_tau3mm_M55_2018, WplusHToSSTodddd_tau10mm_M55_2018, WplusHToSSTodddd_tau30mm_M55_2018, WminusHToSSTodddd_tau100um_M15_2018, WminusHToSSTodddd_tau300um_M15_2018, WminusHToSSTodddd_tau1mm_M15_2018, WminusHToSSTodddd_tau3mm_M15_2018, WminusHToSSTodddd_tau10mm_M15_2018, WminusHToSSTodddd_tau30mm_M15_2018, WminusHToSSTodddd_tau100um_M40_2018, WminusHToSSTodddd_tau300um_M40_2018, WminusHToSSTodddd_tau1mm_M40_2018, WminusHToSSTodddd_tau3mm_M40_2018, WminusHToSSTodddd_tau10mm_M40_2018, WminusHToSSTodddd_tau30mm_M40_2018, WminusHToSSTodddd_tau100um_M55_2018, WminusHToSSTodddd_tau300um_M55_2018, WminusHToSSTodddd_tau1mm_M55_2018, WminusHToSSTodddd_tau3mm_M55_2018, WminusHToSSTodddd_tau10mm_M55_2018, WminusHToSSTodddd_tau30mm_M55_2018:
#     x.add_dataset("ntupleonnormdzulv30lepm_noef")

# for x in WplusHToSSTodddd_tau100um_M55_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017, WplusHToSSTodddd_tau3mm_M55_2017, WplusHToSSTodddd_tau10mm_M55_2017, WplusHToSSTodddd_tau30mm_M55_2017, WplusHToSSTodddd_tau100um_M55_2018, WplusHToSSTodddd_tau300um_M55_2018, WplusHToSSTodddd_tau1mm_M55_2018, WplusHToSSTodddd_tau3mm_M55_2018, WplusHToSSTodddd_tau10mm_M55_2018, WplusHToSSTodddd_tau30mm_M55_2018:
#     x.add_dataset("ntupleonnormdzulv30bm_noef")

# for x in ttbar_20161, ttbar_had_20161, ww_20161, zz_20161, wz_20161, BTagCSV20161B, BTagCSV20161D, BTagCSV20161F, DisplacedJet20161B:
#     x.add_dataset("trackmoveronnormdzulv30bmofftossv8")


# for x in wjetstolnu_0j_20161, wjetstolnu_1j_20161, wjetstolnu_2j_20161, dyjetstollM10_20161, dyjetstollM50_20161, ttbar_20161, ww_20161, zz_20161, wz_20161, wjetstolnu_0j_20162, wjetstolnu_1j_20162, wjetstolnu_2j_20162, dyjetstollM10_20162, dyjetstollM50_20162, ttbar_20162, ww_20162, zz_20162, wz_20162, ttbar_2017, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, ttbar_2018, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon20161B, SingleMuon20161C, SingleMuon20161D, SingleMuon20161E, SingleMuon20161F, SingleMuon20162F, SingleMuon20162G, SingleMuon20162H, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017F, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D:
#     x.add_dataset("trackmover0p03onnormdzulv30lepmumv8")

# """
# for x in wjetstolnu_0j_20161, wjetstolnu_1j_20161, wjetstolnu_2j_20161, dyjetstollM10_20161, dyjetstollM50_20161, ww_20161, zz_20161, wz_20161, wjetstolnu_0j_20162, wjetstolnu_1j_20162, wjetstolnu_2j_20162, dyjetstollM10_20162, dyjetstollM50_20162, ww_20162, zz_20162, wz_20162, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, wjetstolnu_0j_2018, wjetstolnu_1j_2018, wjetstolnu_2j_2018, dyjetstollM10_2018, dyjetstollM50_2018, ww_2018, wz_2018, zz_2018, SingleMuon20161B, SingleMuon20161C, SingleMuon20161D, SingleMuon20161E, SingleMuon20161F, SingleMuon20162F, SingleMuon20162G, SingleMuon20162H, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleMuon2018A, SingleMuon2018B, SingleMuon2018C, SingleMuon2018D:
#     x.add_dataset("trackmoveronnormdzulv30lepmumv8")
# """
# for x in ZHToSSTodddd_tau100um_M15_20161, ZHToSSTodddd_tau300um_M15_20161, ZHToSSTodddd_tau1mm_M15_20161, ZHToSSTodddd_tau3mm_M15_20161, ZHToSSTodddd_tau10mm_M15_20161, ZHToSSTodddd_tau30mm_M15_20161, ZHToSSTodddd_tau100um_M40_20161, ZHToSSTodddd_tau300um_M40_20161, ZHToSSTodddd_tau1mm_M40_20161, ZHToSSTodddd_tau3mm_M40_20161, ZHToSSTodddd_tau10mm_M40_20161, ZHToSSTodddd_tau30mm_M40_20161, ZHToSSTodddd_tau100um_M55_20161, ZHToSSTodddd_tau300um_M55_20161, ZHToSSTodddd_tau1mm_M55_20161, ZHToSSTodddd_tau3mm_M55_20161, ZHToSSTodddd_tau10mm_M55_20161, ZHToSSTodddd_tau30mm_M55_20161, WplusHToSSTodddd_tau100um_M15_20161, WplusHToSSTodddd_tau300um_M15_20161, WplusHToSSTodddd_tau1mm_M15_20161, WplusHToSSTodddd_tau3mm_M15_20161, WplusHToSSTodddd_tau10mm_M15_20161, WplusHToSSTodddd_tau30mm_M15_20161, WplusHToSSTodddd_tau100um_M40_20161, WplusHToSSTodddd_tau300um_M40_20161, WplusHToSSTodddd_tau1mm_M40_20161, WplusHToSSTodddd_tau3mm_M40_20161, WplusHToSSTodddd_tau10mm_M40_20161, WplusHToSSTodddd_tau30mm_M40_20161, WplusHToSSTodddd_tau100um_M55_20161, WplusHToSSTodddd_tau300um_M55_20161, WplusHToSSTodddd_tau1mm_M55_20161, WplusHToSSTodddd_tau3mm_M55_20161, WplusHToSSTodddd_tau10mm_M55_20161, WplusHToSSTodddd_tau30mm_M55_20161, WminusHToSSTodddd_tau100um_M15_20161, WminusHToSSTodddd_tau300um_M15_20161, WminusHToSSTodddd_tau1mm_M15_20161, WminusHToSSTodddd_tau3mm_M15_20161, WminusHToSSTodddd_tau10mm_M15_20161, WminusHToSSTodddd_tau30mm_M15_20161, WminusHToSSTodddd_tau100um_M40_20161, WminusHToSSTodddd_tau300um_M40_20161, WminusHToSSTodddd_tau1mm_M40_20161, WminusHToSSTodddd_tau3mm_M40_20161, WminusHToSSTodddd_tau10mm_M40_20161, WminusHToSSTodddd_tau30mm_M40_20161, WminusHToSSTodddd_tau100um_M55_20161, WminusHToSSTodddd_tau300um_M55_20161, WminusHToSSTodddd_tau1mm_M55_20161, WminusHToSSTodddd_tau3mm_M55_20161, WminusHToSSTodddd_tau10mm_M55_20161, WminusHToSSTodddd_tau30mm_M55_20161, ZHToSSTodddd_tau100um_M15_20162, ZHToSSTodddd_tau300um_M15_20162, ZHToSSTodddd_tau1mm_M15_20162, ZHToSSTodddd_tau3mm_M15_20162, ZHToSSTodddd_tau10mm_M15_20162, ZHToSSTodddd_tau30mm_M15_20162, ZHToSSTodddd_tau100um_M40_20162, ZHToSSTodddd_tau300um_M40_20162, ZHToSSTodddd_tau1mm_M40_20162, ZHToSSTodddd_tau3mm_M40_20162, ZHToSSTodddd_tau10mm_M40_20162, ZHToSSTodddd_tau30mm_M40_20162, ZHToSSTodddd_tau100um_M55_20162, ZHToSSTodddd_tau300um_M55_20162, ZHToSSTodddd_tau1mm_M55_20162, ZHToSSTodddd_tau3mm_M55_20162, ZHToSSTodddd_tau10mm_M55_20162, ZHToSSTodddd_tau30mm_M55_20162, WplusHToSSTodddd_tau100um_M15_20162, WplusHToSSTodddd_tau300um_M15_20162, WplusHToSSTodddd_tau1mm_M15_20162, WplusHToSSTodddd_tau3mm_M15_20162, WplusHToSSTodddd_tau10mm_M15_20162, WplusHToSSTodddd_tau30mm_M15_20162, WplusHToSSTodddd_tau100um_M40_20162, WplusHToSSTodddd_tau300um_M40_20162, WplusHToSSTodddd_tau1mm_M40_20162, WplusHToSSTodddd_tau3mm_M40_20162, WplusHToSSTodddd_tau10mm_M40_20162, WplusHToSSTodddd_tau30mm_M40_20162, WplusHToSSTodddd_tau100um_M55_20162, WplusHToSSTodddd_tau300um_M55_20162, WplusHToSSTodddd_tau1mm_M55_20162, WplusHToSSTodddd_tau3mm_M55_20162, WplusHToSSTodddd_tau10mm_M55_20162, WplusHToSSTodddd_tau30mm_M55_20162, WminusHToSSTodddd_tau100um_M15_20162, WminusHToSSTodddd_tau300um_M15_20162, WminusHToSSTodddd_tau1mm_M15_20162, WminusHToSSTodddd_tau3mm_M15_20162, WminusHToSSTodddd_tau10mm_M15_20162, WminusHToSSTodddd_tau100um_M40_20162, WminusHToSSTodddd_tau300um_M40_20162, WminusHToSSTodddd_tau1mm_M40_20162, WminusHToSSTodddd_tau3mm_M40_20162, WminusHToSSTodddd_tau10mm_M40_20162, WminusHToSSTodddd_tau30mm_M40_20162, WminusHToSSTodddd_tau100um_M55_20162, WminusHToSSTodddd_tau300um_M55_20162, WminusHToSSTodddd_tau1mm_M55_20162, WminusHToSSTodddd_tau3mm_M55_20162, WminusHToSSTodddd_tau10mm_M55_20162, WminusHToSSTodddd_tau30mm_M55_20162, ZHToSSTodddd_tau300um_M15_2017, ZHToSSTodddd_tau1mm_M15_2017, ZHToSSTodddd_tau3mm_M15_2017, ZHToSSTodddd_tau10mm_M15_2017, ZHToSSTodddd_tau30mm_M15_2017, ZHToSSTodddd_tau100um_M40_2017, ZHToSSTodddd_tau300um_M40_2017, ZHToSSTodddd_tau1mm_M40_2017, ZHToSSTodddd_tau3mm_M40_2017, ZHToSSTodddd_tau10mm_M40_2017, ZHToSSTodddd_tau30mm_M40_2017, ZHToSSTodddd_tau100um_M55_2017, ZHToSSTodddd_tau300um_M55_2017, ZHToSSTodddd_tau1mm_M55_2017, ZHToSSTodddd_tau3mm_M55_2017, ZHToSSTodddd_tau10mm_M55_2017, ZHToSSTodddd_tau30mm_M55_2017, WplusHToSSTodddd_tau100um_M15_2017, WplusHToSSTodddd_tau300um_M15_2017, WplusHToSSTodddd_tau1mm_M15_2017, WplusHToSSTodddd_tau3mm_M15_2017, WplusHToSSTodddd_tau30mm_M15_2017, WplusHToSSTodddd_tau100um_M40_2017, WplusHToSSTodddd_tau300um_M40_2017, WplusHToSSTodddd_tau1mm_M40_2017, WplusHToSSTodddd_tau3mm_M40_2017, WplusHToSSTodddd_tau10mm_M40_2017, WplusHToSSTodddd_tau30mm_M40_2017, WplusHToSSTodddd_tau100um_M55_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017, WplusHToSSTodddd_tau3mm_M55_2017, WplusHToSSTodddd_tau10mm_M55_2017, WplusHToSSTodddd_tau30mm_M55_2017, WminusHToSSTodddd_tau100um_M15_2017, WminusHToSSTodddd_tau300um_M15_2017, WminusHToSSTodddd_tau1mm_M15_2017, WminusHToSSTodddd_tau3mm_M15_2017, WminusHToSSTodddd_tau10mm_M15_2017, WminusHToSSTodddd_tau30mm_M15_2017, WminusHToSSTodddd_tau100um_M40_2017, WminusHToSSTodddd_tau300um_M40_2017, WminusHToSSTodddd_tau1mm_M40_2017, WminusHToSSTodddd_tau3mm_M40_2017, WminusHToSSTodddd_tau10mm_M40_2017, WminusHToSSTodddd_tau30mm_M40_2017, WminusHToSSTodddd_tau100um_M55_2017, WminusHToSSTodddd_tau300um_M55_2017, WminusHToSSTodddd_tau1mm_M55_2017, WminusHToSSTodddd_tau3mm_M55_2017, WminusHToSSTodddd_tau10mm_M55_2017, WminusHToSSTodddd_tau30mm_M55_2017, ZHToSSTodddd_tau100um_M15_2018, ZHToSSTodddd_tau300um_M15_2018, ZHToSSTodddd_tau1mm_M15_2018, ZHToSSTodddd_tau3mm_M15_2018, ZHToSSTodddd_tau10mm_M15_2018, ZHToSSTodddd_tau30mm_M15_2018, ZHToSSTodddd_tau100um_M40_2018, ZHToSSTodddd_tau300um_M40_2018, ZHToSSTodddd_tau1mm_M40_2018, ZHToSSTodddd_tau3mm_M40_2018, ZHToSSTodddd_tau10mm_M40_2018, ZHToSSTodddd_tau30mm_M40_2018, ZHToSSTodddd_tau100um_M55_2018, ZHToSSTodddd_tau300um_M55_2018, ZHToSSTodddd_tau1mm_M55_2018, ZHToSSTodddd_tau3mm_M55_2018, ZHToSSTodddd_tau10mm_M55_2018, ZHToSSTodddd_tau30mm_M55_2018, WplusHToSSTodddd_tau100um_M15_2018, WplusHToSSTodddd_tau300um_M15_2018, WplusHToSSTodddd_tau1mm_M15_2018, WplusHToSSTodddd_tau3mm_M15_2018, WplusHToSSTodddd_tau10mm_M15_2018, WplusHToSSTodddd_tau30mm_M15_2018, WplusHToSSTodddd_tau100um_M40_2018, WplusHToSSTodddd_tau300um_M40_2018, WplusHToSSTodddd_tau3mm_M40_2018, WplusHToSSTodddd_tau10mm_M40_2018, WplusHToSSTodddd_tau30mm_M40_2018, WplusHToSSTodddd_tau100um_M55_2018, WplusHToSSTodddd_tau300um_M55_2018, WplusHToSSTodddd_tau1mm_M55_2018, WplusHToSSTodddd_tau3mm_M55_2018, WplusHToSSTodddd_tau10mm_M55_2018, WplusHToSSTodddd_tau30mm_M55_2018, WminusHToSSTodddd_tau100um_M15_2018, WminusHToSSTodddd_tau300um_M15_2018, WminusHToSSTodddd_tau1mm_M15_2018, WminusHToSSTodddd_tau3mm_M15_2018, WminusHToSSTodddd_tau10mm_M15_2018, WminusHToSSTodddd_tau30mm_M15_2018, WminusHToSSTodddd_tau100um_M40_2018, WminusHToSSTodddd_tau1mm_M40_2018, WminusHToSSTodddd_tau3mm_M40_2018, WminusHToSSTodddd_tau10mm_M40_2018, WminusHToSSTodddd_tau30mm_M40_2018, WminusHToSSTodddd_tau100um_M55_2018, WminusHToSSTodddd_tau300um_M55_2018, WminusHToSSTodddd_tau1mm_M55_2018, WminusHToSSTodddd_tau3mm_M55_2018, WminusHToSSTodddd_tau10mm_M55_2018, WminusHToSSTodddd_tau30mm_M55_2018:
#     if "tau1mm_M55_2017" in x.name:
#         x.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")

# #for x in mfv_stopdbardbar_tau001000um_M0800_20161, mfv_stopbbarbbar_tau001000um_M0800_20161:
# #   x.add_dataset("trackmovermctruthonnormdzulv30bmv6")
# for x in mfv_stopbbarbbar_tau001000um_M0200_20161, ggHToSSTodddd_tau1mm_M55_20161:
#   x.add_dataset("trackmovermctruthonnormdzulv30bmv6")


#for x in qcdmupt15_2017, qcdpt15mupt5_2017, qcdpt20mupt5_2017, qcdpt30mupt5_2017, qcdpt50mupt5_2017, qcdpt80mupt5_2017, qcdpt120mupt5_2017, qcdpt170mupt5_2017, qcdpt300mupt5_2017, qcdpt470mupt5_2017, qcdpt600mupt5_2017, qcdpt800mupt5_2017, qcdpt1000mupt5_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, wjetstolnu_0j_2017, wjetstolnu_1j_2017, wjetstolnu_2j_2017, dyjetstollM10_2017, dyjetstollM50_2017, ttbar_2017, ww_2017, zz_2017, wz_2017, WplusHToSSTodddd_tau300um_M55_2017, WplusHToSSTodddd_tau1mm_M55_2017:
#    x.add_dataset("ntupleonnormdzulv30lepmum")

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
# ZHToSSTodddd_tau300um_M55_2017.add_dataset("trackmovermctruthonnormdzulv30lepmumv6")
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

#ttbar_2017.add_dataset('ntuple_K0_DYmuontrig_masswide', '/FakeDataset/fakefile-FakePublish-0b62fe2c2e68572d7b19020908d49d6d/USER', -1)
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

# WplusHToSSTodddd_tau1mm_M55_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
# WplusHToSSTodddd_tau1mm_M15_2017.add_dataset('trackmovermctruthulv30lepmumv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)


SingleElectron2017B.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017C.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017E.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
SingleElectron2017F.add_dataset('trackmoverulv30lepelemv7', '/FakeDataset/fakefile-FakePublish-5b6a581e4ddd41b130711a045d5fecb9/USER', -1)
for x in qcdmupt15_2017, qcdempt015_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017,  dyjetstollM10_2017, dyjetstollM50_2017, ww_2017, zz_2017, wz_2017, SingleElectron2017D:  #ttbar_2017,                                                  # ^   wjetstolnu_2017,   Alec removed; wjetstolnu_amcatnlo_2017,  Abby removed
    x.add_dataset("trackmoverulv30lepelemv7")

"""
# #for tracking tree : cut 0
# for x in ttbar_2017:
#     x.add_dataset("trackingtreerulv1_lepm_cut0")
for x in qcdempt015_2017, qcdmupt15_2017, qcdempt020_2017, qcdempt030_2017, qcdempt050_2017, qcdempt080_2017, qcdempt120_2017, qcdempt170_2017, qcdempt300_2017, qcdbctoept020_2017, qcdbctoept030_2017, qcdbctoept080_2017, qcdbctoept170_2017, qcdbctoept250_2017, dyjetstollM10_2017, dyjetstollM50_2017,  ww_2017, zz_2017, wz_2017, SingleMuon2017B, SingleMuon2017C, SingleMuon2017D, SingleMuon2017E, SingleMuon2017F, SingleElectron2017B, SingleElectron2017C, SingleElectron2017D, SingleElectron2017E, SingleElectron2017F:
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
#wjetstolnu_2017.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2017-cab01ddde62ca73a08de1f75923a7d05/USER', 12251)
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
#wjetstolnu_2018.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-8d1d0e41b6052d5727c7f6571d0cfbc2/USER', 15365)
#wjetstolnu_ext_2018.add_dataset('ntupleulv10lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV10Lepm_WGen_2018-4d2ff0e0a0c7201da5516dcd6193e9b8/USER', 14741)
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
#wjetstolnu_2018.add_dataset('ntupleulv11lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-85617d746c7fd561d6e94c637a6e8f2a/USER', 13696)
#wjetstolnu_ext_2018.add_dataset('ntupleulv11lepm_wgen', '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV11Lepm_WGen_2018-9d1b462a9f502086b20c1023b078537e/USER', 13249)
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


#second round of track rescaler -> straight fits past 200 GeV after big merge w/ Peace's UL_Lepton updates; 2018 has abs(sigmadxy) for general tracks as well (not 2017 *yet*)
#need to redo 2016 still w/ photon trigger + looser hlt matching; but 2017 and 2018 pretty much done -> waiting on a few 2018 samples and 2017 data
qcdmupt15_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-af8490a9909b55282d9bb6890435f3c3/USER', 160715)
qcdempt015_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5994a48e15a1950c78932a8f5c4774fe/USER', 225)
qcdempt020_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-839f5b06067160f846ca1b8c0d1b2e58/USER', 752)
qcdempt030_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a2033abc97998ac06aa80125d8567ffc/USER', 953)
qcdempt050_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-fe31266d2609ab9f12aed53ac492ee89/USER', 1445)
qcdempt080_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-297761c5389f5a8a0ea8767487fdc04c/USER', 2070)
qcdempt120_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5ad9f7c83c360cfccc930c39fb6aad80/USER', 4117)
qcdempt170_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5ce770eddea9d55236971e025ff70a0d/USER', 2901)
qcdempt300_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-7cb7b175cfe7fce83ac80757360ce01a/USER', 3346)
qcdbctoept015_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-719a5959f3980e037755dee1a570a475/USER', 314)
qcdbctoept020_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-c62cb8f8842ab1a8729a9fe660da00c7/USER', 1809)
qcdbctoept030_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-2c7e24e63a81d6b07370112971910916/USER', 9357)
qcdbctoept080_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-e10d6e5493f9b71ce8f80072c35af532/USER', 11200)
qcdbctoept170_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-6543e0a84b4335d30661d2bc92d934df/USER', 17203)
qcdbctoept250_2017.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2017-0548157da1784efc47bc3bba69adb2d2/USER', 18289)
ttbar_lep_2017.add_dataset('ntupleulv12lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2017-7aa33d193a9cd7d2be8f105809d5cc82/USER', 62229104)
ttbar_semilep_2017.add_dataset('ntupleulv12lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2017-0e1dc4e1305c96cc7e2955e01cf5e80f/USER', 122206612)
ttbar_had_2017.add_dataset('ntupleulv12lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2017-e2dc1b89247cf696665bc7d122df607c/USER', 275997)
wjetstolnu_0j_2017.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2017-bbcffcda93fcba1b6131969cdde56d77/USER', 13758077)
wjetstolnu_1j_2017.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f097738944c0d690b03a3a8ea1585ef9/USER', 40076652)
wjetstolnu_2j_2017.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2017-c1fa1d6ca8f4afff4bfdedfd11dfeb42/USER', 23667883)
dyjetstollM10_2017.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2017-b92ecfb0e2e9616af200b368e01b4a88/USER', 340547)
dyjetstollM50_2017.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2017-329b9399726ccae0309d9fdc6293405b/USER', 22810974)
ww_2017.add_dataset('ntupleulv12lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-7ecb097191b8a871bed02c00d8be95e5/USER', 2402807)
zz_2017.add_dataset('ntupleulv12lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ac06764503793b66f22b9a4ce61a8984/USER', 237304)
wz_2017.add_dataset('ntupleulv12lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f9bcd5643bc08876bab00d5a6c5eb5d6/USER', 931264)  


mfv_stoplb_tau000100um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-74a0e2eaaeefadbaec7d356f3a7d6a6a/USER', 194928)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-54e3c63c7cdf12185d53322e6434bdb1/USER', 200301)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ea700fb079a448f1479169c6f3b13c29/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-9759a7e9cf395a37ac88f3122ccf2ec5/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-44dbbeeb5dbad3dc3c29d27d5560b11a/USER', 200668) 
mfv_stoplb_tau000100um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-7804b6e910d195ca49803e8c70665766/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-6871e3bcf716d81b310b14c40a4ea4c8/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-4c09d907789c8936af67c6cf13b2f3f5/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-41602b3f74623613ae5092ddbe8a4548/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2347b0bfec48f5549604354937f9a361/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-97157d107f889d020aaafaa4ec9af06c/USER', 199322)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-56b07d064f8b000d145f3f7845b26ae6/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-610dc5d4307f4860032230c0991259f7/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-70320567e31643c4ad8d7774117f4e0f/USER', 196297)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-aaade3760d254732cbcf010ea23f1032/USER', 198644)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-8c775a200e7318289a1b001dd417699c/USER', 202021)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-1c9b7e18c898b5bfafc46735b9e03bd1/USER', 199079)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-84edc6588e1d4c13e17ba2b4e38773a7/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a3f8d90bef0b7e81eeda1c413a021981/USER', 98921)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-fccc7952cb0197f9b0176783566bcb69/USER', 100284)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ab9e140b8815c9b7efef7e808a9ffb88/USER', 199639)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-31e8abe02a2abb4cbcf4a9cc9a3cff6a/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-30c77b1dffa0788c8acf95cfcb789f5d/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-259cdb14610875cab402ac20485e351c/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d6dfaf94d10451a7db99ea763daaf209/USER', 100172)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-c1e25dc8bd5a223e556f3cf78a8fa578/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-cd60ebb89b6efc72229befddc3ed4f90/USER', 198899)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-430faf0a6af56c90834e5e746885022a/USER', 199948)
mfv_stoplb_tau001000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-398b7cd723b725eb52604232c86e9ad9/USER', 196687)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-68505a1b5c54318a590ae08b261ffc62/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2f9cae7f2e7de5916c39402632e7fc0b/USER', 198231)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a431ee27545d2d5c1579bd1ca0e9d680/USER', 198170)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-1e9a1f1b1fdb9f73611dbaafca047e29/USER', 199832)
mfv_stoplb_tau001000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d55c68d4eb8f04cd64172a496500b617/USER', 200296)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d37a32f82a6a50765967ee7a93bcf8a9/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f858b5a946758c1c9a8e6c2eb482bf27/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2aaa6c41d9623c2c9274a3d6f0412818/USER', 200230)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d0b666bbefe2b1f6a0517fe617b10c4a/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-6ec2e31a0f3da57ec4e9b63d237439d2/USER', 197003)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-b104fd6cef85b7de922f8a1862a1390a/USER', 198930)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-6e4ad6682e6445cd94d1a924c86b41a7/USER', 201812)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-c8372860f638d80c023c81befe63a529/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-eafed95d3bb3e57b028330a59998c582/USER', 197409)
mfv_stoplb_tau001000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d62cb60fd27b0b4a8196cfcd603c16fa/USER', 195368)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ac683eb554913a47065ce4d3c7ae1b0d/USER', 200005)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-36402535a01fd4003a55ab05903dda12/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5bdccb5e956184a28ab122dff5e83cef/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-dcc284b547693973045ccf238eeb1b80/USER', 98799)
mfv_stoplb_tau001000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2905430020383c15407edc257099ea66/USER', 197479)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-88853e57f54e1e73a4b89888cc0822b9/USER', 201690)
mfv_stopld_tau000100um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-eddde1b505c599c077b7203268c2a171/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a699b966aa42f3f7b1c09c40c9b48ed4/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-719b6f629758565070853cd6ab820cc2/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2783cfcce97bbee6bab3789aeab08dd2/USER', 198608)
#mfv_stopld_tau030000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-441194fae661a5589e74acf101004068/USER', 199499)#one event didn't have mfvevent info stored
mfv_stopld_tau030000um_M1000_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-fac7b102e4ccd4d5c46880b4346687b9/USER', 199499)

mfv_stopld_tau000100um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a1e20fcc3dd6ee4f2fbf4fda1218fe91/USER', 198263)
mfv_stopld_tau000300um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-4ce4a560a23b6f82f52fef39949c22cb/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-7ec0003e80193e0a5c587ce965647bd3/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-0957db05161307f9e71b029b94e9482a/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5c485b0b40e44396faebcd8906d9912f/USER', 169592)
mfv_stopld_tau000100um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-00338a8fb4186539dab47f38869067ba/USER', 198812)
mfv_stopld_tau000300um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-735aebd1b22910a7fdcad16374b7dbb1/USER', 194591)
mfv_stopld_tau010000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f54af12c35404c145ba2d0164c2ff329/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-240ce3a0441ebaf2fe0ea786505eeab3/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-e1ad5976e76281af9241d9f100a19e3f/USER', 200714)
mfv_stopld_tau000100um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-4dee8cbf3df0c89bc14b661b363a6aab/USER', 201051)
mfv_stopld_tau000300um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-9bbdb3af7d2767eb6e10d7e3227f7b67/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ca2621691595cc81a696a78971fd1b1d/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-3e5c13c6d7c37c9afac0f5875b0ac207/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-bbce34da844f17241d8028e49384b03e/USER', 100345)
mfv_stopld_tau000100um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-b0e2aec8203cd175d5f71509a418c308/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-6c7607f6ea63f60d9d659fee71654783/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5bfe9eb4ffc60e3289af89e232cefcdc/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-9887558d87efb37c120e505b1d171f35/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d199da7f3114f00cebe55532411b5fc2/USER', 99787)
mfv_stopld_tau000100um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-c13b1b955a0f4ba927da0e636562f969/USER', 201843)
mfv_stopld_tau000300um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-466f6d3a66b81c46b5d904de35862cbf/USER', 199789)
mfv_stopld_tau010000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-968455d9e6746aaf413817be74fcb286/USER', 197403)
mfv_stopld_tau001000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-eb9dbaed8bf49efb8673725cc7b1503b/USER', 198275)
mfv_stopld_tau030000um_M0200_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-8c7f127fbcbd7b9ad28678286d2bc5db/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a60661e9d662199c8ed5cc2cbe4c7c56/USER', 197379)
mfv_stopld_tau000300um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-2b5c1c7fe0efdfffc328cdb55cf62120/USER', 197934)
mfv_stopld_tau010000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-1f2a7815d7d75f10b3cebdcdd41e3c29/USER', 197990)
mfv_stopld_tau001000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-56383436751a8989ecbd59d46cea009a/USER', 199705)
mfv_stopld_tau030000um_M0300_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-d237ad46d949c1911f1239384aea5099/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-1f4aef7ecc24e82b88bf1141e98fa433/USER', 202735)
mfv_stopld_tau000300um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-4cb828085c274d94025e4bf533c2143b/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f6867db8c606eaf0b1453919a015311c/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-f81b92ee2eefe07502b29453a583c48d/USER', 197130)
mfv_stopld_tau030000um_M0400_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-4e7643711c76580e709678f1fb70153e/USER', 198731)
mfv_stopld_tau000100um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-afa6afa79c915ae5884cbb75aea9340c/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-3a746582cbda53607832087f8705cd84/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-ba6c828e073f73ac8dd4765439e4c5ee/USER', 194815)
mfv_stopld_tau001000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a458c084b6c2c08b7d48c1b5a16e73df/USER', 203302)
mfv_stopld_tau030000um_M0600_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-3bcf5043fc95d0296e8a7d09ab618c90/USER', 199944)
mfv_stopld_tau000100um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-a437a98314102466d1d37421c880ea8d/USER', 200077)
mfv_stopld_tau000300um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-1a04b9807ee05e97d80e2b396d7c132f/USER', 200814)
mfv_stopld_tau010000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-bc446555cef351596306fa66bfbb7cac/USER', 99313)
mfv_stopld_tau001000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-5fdf7e1050f4750f83cc7b6bd27edf40/USER', 200829)
mfv_stopld_tau030000um_M0800_2017.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2017-64344efda5ef4f6498542e5076022415/USER', 200140)

qcdmupt15_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3da5b8424a291f6b87cfe461bceb365d/USER', 154960)
qcdempt015_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b8969c1d0ff4576799603c78b52f8374/USER', 115)
qcdempt020_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-db7aec6d69fc522ef37a48054247d556/USER', 627)
qcdempt030_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c1d93433913d7a1ede800426485d16c6/USER', 793)
qcdempt050_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-62a0f5bf65bac2491649b62afabdc81e/USER', 1593)
qcdempt080_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-69b2c0591cf20c69b58af5dd85e8b312/USER', 2113)
qcdempt120_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0937060e9afef740079f54bbaf65f8b2/USER', 3965)
qcdempt170_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-144ba29a87fb7765c568aa014c8db612/USER', 2915)
qcdempt300_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9d0070e0a7228754f38523e592397387/USER', 3218)
qcdbctoept015_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-f101f87c77eaadfe0358ab7b6d910aff/USER', 178)
qcdbctoept020_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-31bb12559560d6a6c096d4348378dbb4/USER', 1365)
qcdbctoept030_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-fbe44c2843978816ff9d149ee817c01f/USER', 8828)
qcdbctoept080_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-57adc1e0266680df99ed27415baafb13/USER', 11797)
qcdbctoept170_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-5855707b4cbb22e0ef650db2bd9901dc/USER', 17032)
qcdbctoept250_2018.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_2018-57e8bd19a8447cdc7eea27d7968bc6a1/USER', 5332)
ttbar_lep_2018.add_dataset('ntupleulv12lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e115a0474fbb7ab78c44a3cbb5315fad/USER', 85865941)
ttbar_semilep_2018.add_dataset('ntupleulv12lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-184e7cbdb1f9c954c5d26313aa83be70/USER', 166638822)
ttbar_had_2018.add_dataset('ntupleulv12lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_2018-84f3853ac3b41519f7903e82a8c2a89f/USER', 390556)
wjetstolnu_0j_2018.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2018-968e6c5d62669c914e261e0de6e0c14c/USER', 13379708)
wjetstolnu_1j_2018.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2018-32c87947dcdc46c973df70f8b630e8b6/USER', 41207787)
wjetstolnu_2j_2018.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0f8abd419fe6c26542317da76e9af316/USER', 23781342)
dyjetstollM10_2018.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-94d90ece68734ed0b357d6886784e000/USER', 486424)
dyjetstollM50_2018.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3b675b6be6a6a26fcb253a0d32c89265/USER', 20857731)
ww_2018.add_dataset('ntupleulv12lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8f7310b418dac0f60ee69021dde7fad4/USER', 2432849)
wz_2018.add_dataset('ntupleulv12lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ef8f01402bc1b3a959494159630da348/USER', 943162)
zz_2018.add_dataset('ntupleulv12lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_2018-356c6b805c08c5a96623537d499dde01/USER', 311187)

SingleMuon2017B.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2017-ccc8e36360bc270f11c8c19861747985/USER', 31942702)
SingleMuon2017C.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2017-e0c39d8595a7f2a30ab05065c0a60675/USER', 63085002)
SingleMuon2017D.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2017-a3c30b83a7570ad526149dad67893d99/USER', 28219236)
SingleMuon2017E.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2017-8ab035adba90f29e2d496db484555a51/USER', 70203674)
SingleMuon2017F.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2017-a287372a78657372b0d531f6af384fa2/USER', 112143201)
SingleElectron2017B.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_2017-e0fa3e30bd9f691fb42db2b35aabf64e/USER', 16875475)
SingleElectron2017C.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_2017-275cd6a44580bba6c1d0c304c22cf326/USER', 36590420)
SingleElectron2017D.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_2017-64948e12a5b36b118a0d3d2105c36ec4/USER', 16385241)
SingleElectron2017E.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_2017-717f08a9ddc234866c4ff31abc315681/USER', 35692155)
SingleElectron2017F.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_2017-15835387013d3f432acc96dc88591f2e/USER', 45959718)
SinglePhoton2017B.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_2017-b68a668ca68f7be4cad8790012431624/USER', 263891)
SinglePhoton2017C.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_2017-e3a39f8ed044227315c9404b3c4015b7/USER', 895521)
SinglePhoton2017D.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_2017-a72f445fabeeea0c4aee1a0e566cfb15/USER', 224902)
SinglePhoton2017E.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_2017-825855007efeac14bec016b622757cfe/USER', 405554)
SinglePhoton2017F.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_2017-f4af93a67c6601dca81b113ca0081c39/USER', 778992)

SingleMuon2018A.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-e32bb53a81a984278b549655fc58f44e/USER', 101542055)
SingleMuon2018B.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-036f6c701884de5b9cd1bd4cce785a77/USER', 50628630)
SingleMuon2018C.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-4a0838c4e28109e4857320546ad5a5ad/USER', 49668378)
# SingleMuon2018D.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-cd6e7ebd409eb3cc142fc7d8a49a817d/USER', 222864757) ##track rescaling as usual 
#SingleMuon2018D.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-1ebf3d5acdb53c28ed6656f881e7af51/USER', 191492484) ##turned off track rescaling entirely 
SingleMuon2018D.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_2018-5b0fb1973a6f56ae761adc3a8e39378c/USER', 190043221) #track rescaling ON but only 3tk SV saved

EGamma2018A.add_dataset('ntupleulv12lepm_wgen', '/EGamma/awarden-NtupleULV12Lepm_WGen_2018-cd351dda5f0cf904ba3eb800d7a0c82c/USER', 48501311)
EGamma2018B.add_dataset('ntupleulv12lepm_wgen', '/EGamma/awarden-NtupleULV12Lepm_WGen_2018-79bc67f0878ab05823a2d75712f9e9e0/USER', 23821556)
#EGamma2018C.add_dataset('ntupleulv12lepm_wgen', '/EGamma/awarden-NtupleULV12Lepm_WGen_2018-e9a942a3cf28dd175f37a986f31e6d20/USER', 23801542)
EGamma2018C.add_dataset('ntupleulv12lepm_wgen', '/EGamma/awarden-NtupleULV12Lepm_WGen_2018-130b469930222f7a0045add76090ceea/USER', 23612480) #saved explicitely track_dxyerr (track rescaling back on ...)

EGamma2018D.add_dataset('ntupleulv12lepm_wgen', '/EGamma/awarden-NtupleULV12Lepm_WGen_2018-b8726c3b11196581467c40c7365073be/USER', 108056280)


mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d3a799d1fd05bc5094e514117a8eff59/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7944377a398f86171c98a6a74a7484dc/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f0facba4ceaf751403d3a22b6568b893/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2a015010ef4e9e2f74ac73f235f7f68c/USER', 198147)
#mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f5335338f3093d734705265200444071/USER', 101153)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8ca67d2f8c0b9c4b2d431d2a7db5eaec/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ae733ba483e1c068160daeb50d78b8c1/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d2919288dd3ce8e5eb00da35972d5e5c/USER', 203023)
#mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-88573631f9a28b7938619a607e08d175/USER', 142026)
#mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-235e3a5ba990da5c65ccc647823ab1ff/USER', 54136)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8af71d9a9e75cc85d48f39188c1c6ce9/USER', 197602)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b079a708341bab3bc1a2fcb53fa7fedb/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8c548ecacf34f99dd9a262f5caff2578/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c3af08d165cf1dcc65d2038dfac6abc6/USER', 200505)
#mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-bba1ba9407a9f02778f20c425759990d/USER', 172844)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-62e5d9a2222d088882049905c1e8c1df/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2956a4c0d49827205ec25cabf3355e26/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1306e4caa30bf2b18705c71d89d70977/USER', 198963)
#mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6cdede780fd67ad45dc255af2e6b529d/USER', 52020)
#mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f27028f92b201f375e4630d59c0ddd3c/USER', 181255)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-215d49e5f12bcdebacdafe844069bbf4/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-83d9b1c97414d36704f8e989e64e486f/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-65945081375aef5c0052b3bcc6af2788/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-21bfa359d4fe46163047c4232978e38f/USER', 196032)
#mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-aaa956c6db54a0d1f2409840d526c60b/USER', 5066)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-82136a1d1513187b37926a5f5c0fc62b/USER', 195903)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-433c4aea70748c62cbf72a37dcbb06dc/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-74f502c1893a2aaeed6e93b49716ccaa/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3b3a0de2d09ef6fcc3384708e5684dc9/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-4802ab4b5f9210ece18069bea8e9e14d/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e68e6bd3055604411994d957b22ae32b/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-97ffbdd1e704fa4498a9c66b7bbb4f9f/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2f8826afa20ecdbd3d841aacf3fb0bf9/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8d896232d3cf29c0ad135b3f7c8e7516/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-938a6ef2a9a5a208794039b9711e9a81/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-72cb36881485d6d95eac1d747f3f5f1f/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-16223dfa3ef6fb28b881f48bf3167844/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5506b659f1adc8ea7a18dd7913fc2e9e/USER', 188958)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f575b551a8be28fb5f8195c85bd84b9b/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8673e4e78469ad6cfe94ff107d21f933/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9a0f2c075796db809ecab1f71594afa0/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-4ada0f26419ca1c9205688257c6ca620/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-aa678073087bc0f7862bfb119403a982/USER', 197312)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-642905ec00c01e0d5f98c24627af7ebb/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ab118aa840858d031d330974dca47a44/USER', 200807)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6c3b8de5f00953be3673d34eb4b21c1f/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1dbb32d6f53d420436d43088b235106b/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b0fef7810eae3220be5d89507e94cc2e/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-85bb424b53de2dd83de056714b802404/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d56a46838aee85bbde172c375158fa67/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-87951676c6a5d20eb29facd7ac83f7c2/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6b4aee1a5ae28f670e1bd2a99fc91e0e/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-3ae95335af5dd0a7e14ebc901d9b432c/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-98361eca9ca65d8970a942083c909f8e/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-90f9c07f91ec9dad64694b079ddfd451/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c592a2d8e1fff8506d922c95cc25457c/USER', 101211)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-18b9d449dbeb551ab04e8b019f8a664b/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2a089a4df82e381f188a1719191bdfac/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0c2daeac1a003df9cac54bdd8fa32ca1/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-613719893725643eb7d953ae82cfe0b1/USER', 200411)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b08341732b304510820d14642c9ba5bc/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-aadc532e95be89845ee7f9178fc4f5c6/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ec1ab63344dc772679089bdf85167af8/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b759fbbaf7ff915e5524b7fcf6258bae/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-38943f7315e207ac7bda879aeaed0093/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-253192baac18a11661d20af42ba4837c/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-805661564a4204c20ea2e6f530151f37/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6f1b284e9bc40cc53cb7867a7e5dcc7f/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7b36f57f67698e81457f6a201e1935e4/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-1b865b9f1469b135f187196c96d4bf43/USER', 200098)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-22583115fbad7cb13ee0b4a4d0530fbf/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-6f4af5f85a45481c50925601e1a49dd6/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-75f82f5454d79f4b407b01394b9a85ea/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0f6c482d4b9a82f6a5c4ebd6de5ae275/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0573f2b528f52936cbca97ae345cbe48/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-ee616fbea38fff511ed4b35e997d5d40/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9b235e9c93fc5c67993dd44e6825858c/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d74a50734057ed47fd9524304e12ab1f/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-927392ecee0291284098bb5e463c2273/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-d431319ce864af53e008f64dbe69cb1d/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-9f525023a2c13d94e76328dd72fc76e3/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-47b8a8de2c4e884f2f300cdd775c9284/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-82ead2591fa6efc770fbe43b9b87836f/USER', 194824)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-8cef1250407fcf59bb3980d1927e2d3f/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c0ab036aac262be00ee594d1bd5f56f8/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-524e4b10f46f1776eb5cd75ac193e8ba/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-2841d750f2f0fc178aa33b88fb5ef26f/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-deb26ee11b2a986b67317bbfba7f2faf/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-fd4d6b1a5faff54a38803b96199a9337/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-68af4131bf2a5ce00b8272a5e58f0074/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5945672d37e09bbd62b131643769af49/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-43951b8faa53f7b36cc49b4e5bc8fbef/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-64dae7b6b1a13960f424ad8c3ec7b74e/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-c260d9ce58c4772a247bf86ca2c70a71/USER', 202529)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7470ae8373ba1f08e03e1516feeefd7a/USER', 196708)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-e0ca9fda9e30495bae52308495fc22bf/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-5e4384ee950bdb0507150f4211bcfeb5/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-7ef3f524ae2b0d0dce96de5f5e49d799/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-f1445f90eef84c75945d0a23d28a1ac7/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-901d04f4799547f137a726390b35c3ca/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-58020e4ae4609ef52cdb852812c10356/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-02ad0b7a63a328851155b5c8a7f19ebf/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-eb6ac2025e73949b1dc165dc6721231f/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-457ebc22e9a80d7aaab79db1e0f0ead4/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-219a76b03ebc3b818f8a937e217bb364/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-b3c33d370db07adb958585768c162edc/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_2018-0a8e8e6ec22fc0dfa69c42054eccd264/USER', 98449)


qcdempt015_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1e2a0cf401e7dda55525e51543abb101/USER', 79)
qcdmupt15_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d42e0c4465c6d02e5d02bf90d529be5f/USER', 61292)
qcdempt020_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-acb995ef09f7f78b5d9b0afe8a7c9f4c/USER', 331)
qcdempt030_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-964d82e6e007cfe65b096ccfaf39f08f/USER', 392)
qcdempt050_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-46dd5e79bb883e85a46e57486ebc26ea/USER', 752)
qcdempt080_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1d532f3c8f9d9fbdc3ae03d14b06f54f/USER', 1157)
qcdempt120_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-e6f8bdd6b4ed77af77c9f2801513d19e/USER', 2407)
qcdempt170_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-75ac7b0767187514669a84293cd402cf/USER', 1711)
qcdempt300_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bf395399232780cea50a26cf57ef16ff/USER', 1904)
qcdbctoept015_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-9e0b13fb1114ae6c8c644c9c68b81ec4/USER', 61)
qcdbctoept020_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-828be6e0fdd87c2456a68435900f4815/USER', 514)
qcdbctoept030_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-85e6f631ba0ff0121bbd7f29d3ee5a26/USER', 3390)
qcdbctoept080_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-628c89413d3eb4c8c24f136c03328d2e/USER', 4538)
qcdbctoept170_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-e1b08860e682a6bbe1caa3cf3db94e4b/USER', 6754)
qcdbctoept250_20161.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20161-d5ac3c90bf4633b9c9371b838f303d20/USER', 6663)
wjetstolnu_0j_20161.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b305fb0fd8354d4958b5b78b65daa953/USER', 8276916)
wjetstolnu_1j_20161.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20161-29abc1798113d2a6bb1b3feb1666a47d/USER', 36128529)
wjetstolnu_2j_20161.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2f4f9d6fb002f7040417567d101defc6/USER', 20716459)
dyjetstollM10_20161.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_20161-a9f27fa16ba6342d8787b27fd0906263/USER', 113479)
dyjetstollM50_20161.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2e60dfef967f74feae9a5490de743601/USER', 15878928)
ttbar_lep_20161.add_dataset('ntupleulv12lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20161-05a109ae3831f3ca78822ae1cb8d95da/USER', 18897800)
ttbar_semilep_20161.add_dataset('ntupleulv12lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bb7b248696482cb709644bbd208db0f9/USER', 42963464)
ttbar_had_20161.add_dataset('ntupleulv12lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2412266ecbb90322a20479e48deb880c/USER', 90369)
ww_20161.add_dataset('ntupleulv12lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3fd95d5fd616b1f7014820076ecca331/USER', 2257496)
zz_20161.add_dataset('ntupleulv12lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bdb1800d61cd414cf966c581c4d1e722/USER', 105059)
wz_20161.add_dataset('ntupleulv12lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20161-199c0809efb8671ac4996c097352b0ac/USER', 870913)
mfv_stoplb_tau000100um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-25c0513ae54fd65a4a9eef10178e5a2c/USER', 98890)
mfv_stoplb_tau000300um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9853e9d6522130b6288f07a9b45df373/USER', 99090)
mfv_stoplb_tau010000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-98e953f05c3b9c6ed246fe60e0593600/USER', 49863)
mfv_stoplb_tau001000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9b273b7a5f2042335125fa5023621215/USER', 99632)
mfv_stoplb_tau030000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-c5edbc224317ca43ee6ad37f53c652f3/USER', 99612)
mfv_stoplb_tau000100um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bbceb6120ee8b605f75bb078bc30beae/USER', 99340)
mfv_stoplb_tau000300um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-f172d4e1c6b361cd5f92252e73328960/USER', 99010)
mfv_stoplb_tau010000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-a6c9e6171a550ff7ad6927f40aa6f647/USER', 49944)
mfv_stoplb_tau001000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-120030658fa99793d1da35a41c3bde6c/USER', 97995)
mfv_stoplb_tau030000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-c098b12a6a585f6617e29029a3d972ef/USER', 101825)
mfv_stoplb_tau000100um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1f7436ef6815cf4c5c560a0006ad196b/USER', 100444)
mfv_stoplb_tau000300um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ac4228943f1dda39e4b9710cfc08e76d/USER', 98629)
mfv_stoplb_tau010000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-78ad330d7a90b801c79b38a60508ffd0/USER', 49531)
mfv_stoplb_tau001000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-e2d4a1d114dde6b6520aeedde391d432/USER', 99778)
mfv_stoplb_tau030000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3e94b1b27ff8ee93f1e28790cf425e32/USER', 99896)
mfv_stoplb_tau000100um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b2beb021aefc2cc02c6beb1bd842ad51/USER', 99251)
mfv_stoplb_tau000300um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-0d99c34aa8df51397fefe5b48765c656/USER', 99184)
mfv_stoplb_tau010000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-baee2c6a464a771eb2a52c3cfd1d6720/USER', 50317)
mfv_stoplb_tau001000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-91da5b33b260f513178a49ef095578ca/USER', 49741)
mfv_stoplb_tau030000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ed8e8b5703b2f48e63926a580bc2cf3a/USER', 48712)
mfv_stoplb_tau000100um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bd216961c7e38fcf0a565f1122e364b6/USER', 100766)
mfv_stoplb_tau000300um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3dca2168a7c2f889be1df53a8c5a4f1e/USER', 81729)
mfv_stoplb_tau010000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-602551bbb8894d7c678dbeb24463b5bc/USER', 49090)
mfv_stoplb_tau001000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-8b6565af5fc91dd1b75f13d35785fd77/USER', 49049)
mfv_stoplb_tau030000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ff35c5538f3d89ef9ed813d613eb36ec/USER', 49438)
mfv_stoplb_tau000100um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3e4ae2f06d7edc61084044708bd2ea5f/USER', 99188)
mfv_stoplb_tau000300um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-e12713ed4707b1d1a85151e65a749f37/USER', 100726)
mfv_stoplb_tau010000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-595e6d556d58c0e7677417ae20f32f09/USER', 99023)
mfv_stoplb_tau001000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-04468ada9cb4efa957b37a63451eb482/USER', 99012)
mfv_stoplb_tau030000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-e6481cba34533c33350a5f92fb38e7b2/USER', 99812)
mfv_stoplb_tau000100um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ec9c95d23b3459603752be98dac34613/USER', 100222)
mfv_stoplb_tau000300um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1722e82d1999c6f5a398ff50ce2b9493/USER', 100150)
mfv_stoplb_tau010000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-6de8fb3259051d1b80078946dff4b0d6/USER', 98854)
mfv_stoplb_tau001000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-c46e05fb83e404608518b283ab1d4d0c/USER', 100049)
mfv_stoplb_tau030000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-65014510896956648f47835e60b0a724/USER', 99401)
mfv_stoplb_tau000100um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-0bf482fef29d0df0a0ee31cbeb940477/USER', 100672)
mfv_stoplb_tau000300um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3e1f8c9e205c9295cf47c6486cf96ee8/USER', 98457)
mfv_stoplb_tau010000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-7faa0ce41af46f26c6c278b771eed15d/USER', 99343)
mfv_stoplb_tau001000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-470889766ddb54243b20c643b2a9dda8/USER', 99760)
mfv_stoplb_tau030000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-52de142072bc9e2f1519a6ac530a0459/USER', 98676)
mfv_stoplb_tau000100um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4c0c279c4ba0d7bad84d081812c17fb3/USER', 100158)
mfv_stoplb_tau000300um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-7ba1b7f4274ca9de57bf66f51afb4d9d/USER', 98762)
mfv_stoplb_tau010000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-280e124b4a228b1de8d842c12b043c18/USER', 99264)
mfv_stoplb_tau001000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4c19ddb4b7f4883ab7b3e6e6a5d42d8b/USER', 101849)
mfv_stoplb_tau030000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2a854416a0dc603bf28245652627ab38/USER', 100390)
mfv_stoplb_tau000100um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-414b4dafcea7091eb39ee289e1c068f7/USER', 98204)
mfv_stoplb_tau000300um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9c8c4cae86560638771280583d3246a7/USER', 100784)
mfv_stoplb_tau010000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-544e8f7feec52bc60f122f1bc962d987/USER', 48963)
mfv_stoplb_tau001000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ee9dd0d1b34b008b0db2dd353352d9f4/USER', 100377)
mfv_stoplb_tau030000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d92a8ad75d0750dcbe46f3ee16035742/USER', 99164)
mfv_stopld_tau000100um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-bd3b7a5ee286c4af85d3de2e326c52bc/USER', 99017)
mfv_stopld_tau000300um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b5b8ca7690d2344976828fa059bc7575/USER', 99362)
mfv_stopld_tau010000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-643a5ade2ddfa4e16f852e124e298008/USER', 49856)
mfv_stopld_tau001000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-5ca125ea78bf7fec84fd5d9608fc71c4/USER', 98183)
mfv_stopld_tau030000um_M1000_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2d736bf5c939e397073900daee84dd7b/USER', 100852)
mfv_stopld_tau000100um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-362e28ae6a17b256719fe6ac18e757c4/USER', 99830)
mfv_stopld_tau000300um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d9445d29b2734dfb7dd9f287a720b3cb/USER', 99813)
mfv_stopld_tau010000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-f4a50dda28f4184ded139055fd3c73ab/USER', 49767)
mfv_stopld_tau001000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-5a1e6267b170dbdafd81ebdeb8592e79/USER', 100012)
mfv_stopld_tau030000um_M1200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1be31aa497a6a2fa94d9b02fa38eb79b/USER', 99996)
mfv_stopld_tau000100um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b6b997bd5421d07ac06c0c15f59e658d/USER', 100303)
mfv_stopld_tau000300um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1287ef9fa4b4d7783fcef981ac342007/USER', 98700)
mfv_stopld_tau010000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4b241dedad7b044e64c5c2522915c0a5/USER', 49501)
mfv_stopld_tau001000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ddb1afc58048ef6865e934bfa3a492b3/USER', 99221)
mfv_stopld_tau030000um_M1400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ea695469550822aa8fab5520405797a1/USER', 99706)
mfv_stopld_tau000100um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4c83cabcba52b142c70d71ca5763da98/USER', 98875)
mfv_stopld_tau000300um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-cdef3cb8ab11f3e9abec6f68a0cb0517/USER', 98632)
mfv_stopld_tau010000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4081c4a6034e019096c89252304a3658/USER', 49359)
mfv_stopld_tau001000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d8351e6e9d7f58d67f89698b40d06cdd/USER', 50121)
mfv_stopld_tau030000um_M1600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-ccdfde08142370eb92cc97f939594d3b/USER', 50681)
mfv_stopld_tau000100um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-c476fd1e4bb49a18b8c45c0eb1ed023d/USER', 99761)
mfv_stopld_tau000300um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-09c9a461098f5fb53d433dabc6bc011d/USER', 100032)
mfv_stopld_tau010000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4c2e59d4ba22bea7b0756bda220516c4/USER', 49884)
mfv_stopld_tau001000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-f2098deebf27e8609804b96e9cb5ca49/USER', 49871)
mfv_stopld_tau030000um_M1800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-1fb7689120c718be747c9d19a87d6ccf/USER', 49634)
mfv_stopld_tau000100um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d6c42c84522a36ea80c1fecc1dd86d03/USER', 101080)
mfv_stopld_tau000300um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-26b7662b6e5c876926ebc186a8cf11d4/USER', 98938)
mfv_stopld_tau010000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-2592f44e17263555c53fb66c1862a317/USER', 99845)
mfv_stopld_tau001000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-94308d62156a103486ae4ea672a109d5/USER', 99943)
mfv_stopld_tau030000um_M0200_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4d3e80c982bb58e1d2b2c41554bdb7d8/USER', 99418)
mfv_stopld_tau000100um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-24cd8e1b86aed74c408756578d292739/USER', 101171)
mfv_stopld_tau000300um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-e7a12a5985fa28d0da0f25a402892770/USER', 100455)
mfv_stopld_tau010000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-44fc958dfdef8d01c3fb68ee6b9bec89/USER', 100892)
mfv_stopld_tau001000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-77fa7ef74e2b0aed3a6d7ba9f42972b8/USER', 99556)
mfv_stopld_tau030000um_M0300_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9a5e73aaf1357480766828427e22d04c/USER', 99447)
mfv_stopld_tau000100um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-5d53b731431fb19f2b418ca0e3768dc4/USER', 100509)
mfv_stopld_tau000300um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-861ffcfec86beea8a870082de3434a11/USER', 99765)
mfv_stopld_tau010000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-79930ac76ad1d64c7351fe2c235fc9e8/USER', 99682)
mfv_stopld_tau001000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-324d5417c9cb41a418d2848066bc664d/USER', 99890)
mfv_stopld_tau030000um_M0400_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b4b6d85991dae90e6325e257effdd559/USER', 99531)
mfv_stopld_tau000100um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-367a0e37450d4cc10de70fbe7f53ce23/USER', 100034)
mfv_stopld_tau000300um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9811519adc953a2d287c5233b1b41cfd/USER', 99611)
mfv_stopld_tau010000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-7882d374974b5a6b4eddfa8a9c66cd7f/USER', 99643)
mfv_stopld_tau001000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-9a83a01730e8c10de8019d5219588f72/USER', 99924)
mfv_stopld_tau030000um_M0600_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-d8aeac987f1b887b3d934c280c90e7be/USER', 101612)
mfv_stopld_tau000100um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-6066728f00a350562d957f21e4480160/USER', 100466)
mfv_stopld_tau000300um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-4236e89fabd08512af3b1e6012f5a8d0/USER', 98676)
mfv_stopld_tau010000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-b554b162674aaf883b349e7296d1ebee/USER', 50147)
mfv_stopld_tau001000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-888f15bb63ff36ebf255e73f90075dc1/USER', 98387)
mfv_stopld_tau030000um_M0800_20161.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20161-3d48fe5b8bb446a0ea2434e5b3370bbe/USER', 99914)

qcdempt015_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-2768ac9b6378431e2046e6a543a85dfa/USER', 77)
qcdmupt15_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a60a7d2379d0aed4fd7ffcda02aca726/USER', 62952)
qcdempt020_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a162c752b63cb2a5e6548183eb77494a/USER', 264)
qcdempt030_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-31541e0fde919694ba31243efa91ce55/USER', 399)
qcdempt050_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-0ac36249f57a3d5e2a8d30fe16a1d260/USER', 788)
qcdempt080_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-eb1a217b5fb7d9ca402681e1814262e8/USER', 1175)
qcdempt120_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-27c4266f3c668266864f67725bf97c25/USER', 2511)
qcdempt170_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-5d8c8ce8d80d1ec20e7b7fada04d6656/USER', 1747)
qcdempt300_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a4cf1bad8afc247e18f15e1acea124ae/USER', 1986)
qcdbctoept015_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-bb9921235ea95d6c92a40127b8c7f477/USER', 86)
qcdbctoept020_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-2b67187357f0e7b75fe2223ee2df3ee5/USER', 508)
qcdbctoept030_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-29617f2a2431c9bc2d0a7ec3fe2491f2/USER', 3216)
qcdbctoept080_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-ad03741e4f1b18b70a8cbdb0cb20c0e6/USER', 4800)
qcdbctoept170_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-7ccc431641f6cb699dab5d43e020b776/USER', 7690)
qcdbctoept250_20162.add_dataset('ntupleulv12lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV12Lepm_WGen_20162-ea770102f166a77b7ace21d74ff095d9/USER', 8166)
wjetstolnu_0j_20162.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a154f71c3647d7c89d13c7daab1d3673/USER', 8944616)
wjetstolnu_1j_20162.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20162-be06e6ae65851ef92112fcb14bcb806e/USER', 35869126)
wjetstolnu_2j_20162.add_dataset('ntupleulv12lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e7d81a31e5e3ce7355fc4380916cbb4d/USER', 20659862)
dyjetstollM10_20162.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_20162-0a1ffca9b5673ab7992e5909bd2ffe6e/USER', 107239)
dyjetstollM50_20162.add_dataset('ntupleulv12lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV12Lepm_WGen_20162-4401e11302f0ae5df564c3e2df29c5d1/USER', 14563190)
ttbar_lep_20162.add_dataset('ntupleulv12lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e57abe4b657ea61a230583b0930c1efb/USER', 25094894)
ttbar_semilep_20162.add_dataset('ntupleulv12lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20162-d3491b0eca7b1798580356c7d920944c/USER', 48955656)
ttbar_had_20162.add_dataset('ntupleulv12lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV12Lepm_WGen_20162-515042cc33ce3993ffe37bedd758540b/USER', 41718)
ww_20162.add_dataset('ntupleulv12lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-d9d6d73db362171780eaefec35443e6f/USER', 2207993)
zz_20162.add_dataset('ntupleulv12lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-957a0860ce9e7003989106000952cf39/USER', 95892)
wz_20162.add_dataset('ntupleulv12lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV12Lepm_WGen_20162-b20ec5378dffd2a47381b7540c9d797d/USER', 847183)
mfv_stoplb_tau000100um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-91c2be9cb73c404fd64cb267e075f275/USER', 99539)
mfv_stoplb_tau000300um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-107c0726a532787e62598c3f7ac6a2da/USER', 99257)
mfv_stoplb_tau010000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-db0a0c5544288c2a23a3ca2c560e1004/USER', 47714)
mfv_stoplb_tau001000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-ec151b28f2f0de152ab68434b16ef619/USER', 98557)
mfv_stoplb_tau030000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-b3e7474604945d6cfee4cd2e5c13d325/USER', 99898)
mfv_stoplb_tau000100um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-f909cda9c587fa167745e2f49d71a6f3/USER', 100330)
mfv_stoplb_tau000300um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-0b30c440b4db1dd9fc5a27e6b3b6cb11/USER', 98676)
mfv_stoplb_tau010000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-94e44294efefb8f4b87773d0a8198816/USER', 49832)
mfv_stoplb_tau001000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-0c04a8214241abedb46f83a77638135e/USER', 98582)
mfv_stoplb_tau030000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-fbfa99eb29d5464e0dbbd6ae0ccf1ef7/USER', 100391)
mfv_stoplb_tau000100um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-c5759db48f8a4dab38f5e8b29e658a01/USER', 100112)
mfv_stoplb_tau000300um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-f5a8428f1d37b89334b0f7028fae7be5/USER', 99840)
mfv_stoplb_tau010000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-035ae3f41032ee341e0e94e3d6d9b9c7/USER', 49856)
mfv_stoplb_tau001000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-33f46ae49806dea4dc576c546a74bb60/USER', 99508)
mfv_stoplb_tau030000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-abf52d6fafa22ddd9fda72cdc0a3e0fd/USER', 99537)
mfv_stoplb_tau000100um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6173e6ed56c12fbc92fbdc079d69ee93/USER', 99744)
mfv_stoplb_tau000300um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-363a2f7eb30c585863fab0a775db9a97/USER', 99902)
mfv_stoplb_tau010000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-09a9e3228ab1ba5d8be6a4d334f05849/USER', 49227)
mfv_stoplb_tau001000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a915f2021e635f9226dabee01ce2edf2/USER', 50163)
mfv_stoplb_tau030000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e66009494d89b504f4fc12860fef3924/USER', 50181)
mfv_stoplb_tau000100um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6f64f6692070527f330ba6ab3ee15fcb/USER', 98144)
mfv_stoplb_tau000300um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-286c854833f8fecd0cbbf54c6509d693/USER', 101235)
mfv_stoplb_tau010000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-fb88b372f264b3788008b2fd3dd5f09f/USER', 50608)
mfv_stoplb_tau001000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-b80cf93851a081753a0214080c8a4a52/USER', 49712)
mfv_stoplb_tau030000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-7dd058ede7769a6b7d8ba09a406580e5/USER', 49799)
mfv_stoplb_tau000100um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-84e7df42351dfec08a624d1538b04d56/USER', 99793)
mfv_stoplb_tau000300um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-fbe12d0ccd3e11832588bbcade3d2082/USER', 99406)
mfv_stoplb_tau010000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-32cd7f32d1f62993b00180e5a6e70e78/USER', 99401)
mfv_stoplb_tau001000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-1af50ce431bacaaf15fd09c0a4ad2f4a/USER', 97820)
mfv_stoplb_tau030000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-12a21d19b016efef74260313e561bc91/USER', 101202)
mfv_stoplb_tau000100um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-7c16090b8bb5c42c8d9d34b444eb93b3/USER', 99857)
mfv_stoplb_tau000300um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-253fae03612a92d5647ca5b515340885/USER', 99010)
mfv_stoplb_tau010000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-9fc8067280a86aaf2ca5bb682056bddb/USER', 101044)
mfv_stoplb_tau001000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-71f73a14c2a224b18e549da457383d49/USER', 99219)
mfv_stoplb_tau030000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-aa972c080763709bc0f655ac6a1df758/USER', 99207)
mfv_stoplb_tau000100um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e7f846e7559040275bddc0fa6e28fb91/USER', 98268)
mfv_stoplb_tau000300um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6ffa69a9ced81f0c9b41825034e0909d/USER', 100008)
mfv_stoplb_tau010000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-5402b9c3790805d5c6958fbaa082ef6a/USER', 101168)
mfv_stoplb_tau001000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-669fe2c6f428ee0eb58c00053d7fe4fd/USER', 99255)
mfv_stoplb_tau030000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6ebf70031e12f8988a73301b93863cf6/USER', 99198)
mfv_stoplb_tau000100um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-9b628fd5c277c2db1ce935d86a25e347/USER', 100291)
mfv_stoplb_tau000300um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6df8bac4733f0bdd6607d90b1fe1a5a8/USER', 86231)
mfv_stoplb_tau010000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-32508f9e4bc4f248be9626e88ef71cf1/USER', 100170)
mfv_stoplb_tau001000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-f13a250a1850c6573567a0ed26cc2fb0/USER', 99575)
mfv_stoplb_tau030000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-074d70892775b12693d141d56f665dfb/USER', 100308)
mfv_stoplb_tau000100um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-1bb279c58db9a7159ccbc02586c87657/USER', 100987)
mfv_stoplb_tau000300um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-d4602d8b3bccd3e79020738583351e89/USER', 100012)
mfv_stoplb_tau010000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-25102b30831ef60c0ce797263df66512/USER', 50027)
mfv_stoplb_tau001000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-bf0bddd2bffb0b5e915c8b9003a41c8e/USER', 99440)
mfv_stoplb_tau030000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-103ec75ec38b7c8996319aa5bbe1128b/USER', 98586)
mfv_stopld_tau000100um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e949914ca9140c8913772f5fa6e5734b/USER', 99376)
mfv_stopld_tau000300um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-8f98d124eba944ff31fb9b85165e341d/USER', 100018)
mfv_stopld_tau010000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-7a72120cee0bde3b334aa63c705a4c83/USER', 49142)
mfv_stopld_tau001000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-c14b7d7d493a769223e7b1beb0c83620/USER', 100845)
mfv_stopld_tau030000um_M1000_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e70bb51635156f3bbd3e1204b4da945c/USER', 99794)
mfv_stopld_tau000100um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6d9ac268a0cc190492aa1e101e063eca/USER', 99574)
mfv_stopld_tau000300um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-daadcff0538d8b2859fbbf1503c35e13/USER', 99868)
mfv_stopld_tau010000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-381d533c1637e1b5663061b10d11a418/USER', 49886)
mfv_stopld_tau001000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-793a43544aac15f295fe51403143a7be/USER', 99291)
mfv_stopld_tau030000um_M1200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-36ff59d5b670d65e4e76d2d4bf9c63c1/USER', 99929)
mfv_stopld_tau000100um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-f6dcac49902a6957f7d0e470149b2179/USER', 99545)
mfv_stopld_tau000300um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-c257d6ea533b9d5f87f57b6abe8df2a5/USER', 99932)
mfv_stopld_tau010000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e01eae2bbc81b24a8858eff0aca2a303/USER', 49788)
mfv_stopld_tau001000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-49bfa4ccefa6e31053c56e23699dd5b2/USER', 98682)
mfv_stopld_tau030000um_M1400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-00d5236d455cb0aad4fb46cff7f5e6df/USER', 101616)
mfv_stopld_tau000100um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-4e86330b757e61fbbedd7c8d6e9e3051/USER', 100675)
mfv_stopld_tau000300um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-2dff1789dbadc1bb2e1e1d10072a5f5b/USER', 100486)
mfv_stopld_tau010000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-48d0acd98b5c468497a4ba90efccc0f8/USER', 49732)
mfv_stopld_tau001000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-9766dda0a10373403981818d1106550f/USER', 39669)
mfv_stopld_tau030000um_M1600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-46b70977a183a9b67c81005d34d7607e/USER', 49682)
mfv_stopld_tau000100um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-0fbc5abe1f65c1e49ad82df28b665b1a/USER', 93562)
mfv_stopld_tau000300um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-8b462477be78baf1b5fd81eac9b0502f/USER', 99749)
mfv_stopld_tau010000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-1836d537a12d87cfb201744723d8b29c/USER', 49663)
mfv_stopld_tau001000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-b83fdb41c0e596682a34994b86937c5e/USER', 49813)
mfv_stopld_tau030000um_M1800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-26920a20d2699a97b2a69f4cb3f7fd07/USER', 50468)
mfv_stopld_tau000100um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-9681769e82d7a39294f453095dd59e63/USER', 100260)
mfv_stopld_tau000300um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-527f297ea4299c733906315f62adfe76/USER', 99340)
mfv_stopld_tau010000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-a8479a1f41160bc293824cbd39073509/USER', 99542)
mfv_stopld_tau001000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6860d7e2ff6abed74cc03c08ce8d1c5e/USER', 97872)
mfv_stopld_tau030000um_M0200_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-868b54fbafaedaf413ccf49f82908257/USER', 98201)
mfv_stopld_tau000100um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-81ecd00dddf9aedc77193628fa2c8d90/USER', 100170)
mfv_stopld_tau000300um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-8578ac7bc869991fdc51af43af963c6b/USER', 100594)
mfv_stopld_tau010000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6d4a4a972bd6826505e004992212b1f2/USER', 99759)
mfv_stopld_tau001000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-847d0e687777d336d842d85cc645b7c7/USER', 99504)
mfv_stopld_tau030000um_M0300_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-1ac88ec793b289124c988c97deab6d60/USER', 99243)
mfv_stopld_tau000100um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-2a227e001d346db2866fafe4a8eda006/USER', 100052)
mfv_stopld_tau000300um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-8ffe1509c26eb19f3b33538c99cb9fac/USER', 99431)
mfv_stopld_tau010000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-04ec5522e8781ab4cca85f121ff48357/USER', 99314)
mfv_stopld_tau001000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-274763c272b354541d800cb1769123e8/USER', 100447)
mfv_stopld_tau030000um_M0400_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-b801de9d6d491b036f9ce7bcc75773fe/USER', 99547)
mfv_stopld_tau000100um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6bd8e9440a3c0801b4bd674ec489f484/USER', 100954)
mfv_stopld_tau000300um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-7a5001db2dc1f33648d7f8632c5f3cd4/USER', 99589)
mfv_stopld_tau010000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-7c928d757eb8733cb90449e5b59894c3/USER', 100599)
mfv_stopld_tau001000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-5b1ac8816373b1d104f70302cc51b56f/USER', 99859)
mfv_stopld_tau030000um_M0600_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-41d605c72d2794b715c0af2c7ce41000/USER', 100128)
mfv_stopld_tau000100um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-6991b8394190ea9ff931f0a51c48e302/USER', 99282)
mfv_stopld_tau000300um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-3b70e9055e75ee7728fde3034a4da39c/USER', 99263)
mfv_stopld_tau010000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-e5a904245868a93e02f20aaba7dfbee1/USER', 49387)
mfv_stopld_tau001000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-afd34738e1f35a7fdf4154f9ae378e8b/USER', 100038)
mfv_stopld_tau030000um_M0800_20162.add_dataset('ntupleulv12lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV12Lepm_WGen_20162-583e28e742d6130b2266ec64e7b8f847/USER', 100282)

SingleMuon20161B.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20161-dca4d5a86dfe53ad6c7192398b56f211/USER', 29464393)
SingleMuon20161C.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20161-f432fcdb4c033bda96a7656c7e88f499/USER', 13621479)
SingleMuon20161D.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20161-e3c3837d7e18ba930639ccb2eac3e5ab/USER', 22336062)
SingleMuon20161E.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20161-b012c194f1fc31e124b1bf3e664751bf/USER', 23496791)
SingleMuon20161F.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20161-03b76a69707813eee7064d95f79240be/USER', 15905137)
SingleElectron20161B2.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20161-a6f0701312f3b1ac976df33ad3e76988/USER', 21038786)
SingleElectron20161C.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20161-d49ddb76e498f2f22ca60f42e915de68/USER', 9411697)
SingleElectron20161D.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20161-c9693bac05a66534fe6c23e2ea69aafc/USER', 15439927)
SingleElectron20161E.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20161-443b35ff1f6c962acc969491cc0ff8c5/USER', 15215399)
SingleElectron20161F.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20161-cd6cfaa7bc72e2381f41b621007a5763/USER', 9853494)
SinglePhoton20161B.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20161-4a4ff72cd30c5ad496c1e7713b33b66a/USER', 2367665)
SinglePhoton20161C.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20161-9001073517e7820f96499fad104e9c5f/USER', 881454)
SinglePhoton20161D.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20161-33dce221ad9b904506f019c042b0d61f/USER', 1033532)
SinglePhoton20161E.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20161-c14587d4cb179f634b20ffb8c48df7bb/USER', 641047)
SinglePhoton20161F.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20161-eaeb39dfe0d2088e10f7edc425e8f06b/USER', 355558)
SingleMuon20162F.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20162-9692dcaa963cadb672c4aed9f98067d0/USER', 2345189)
SingleMuon20162G.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20162-f02a8ed9adbab5613a49bace0a6d3124/USER', 43810001)
SingleMuon20162H.add_dataset('ntupleulv12lepm_wgen', '/SingleMuon/awarden-NtupleULV12Lepm_WGen_20162-178bd5934664c12cc1ef46b649941ae7/USER', 52355266)
SingleElectron20162F.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20162-d96e0349efe35672f1f1731e311a16f9/USER', 1528087)
SingleElectron20162G.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20162-5f49b668dc47b93ff750e9f52ce43aa2/USER', 26972559)
SingleElectron20162H.add_dataset('ntupleulv12lepm_wgen', '/SingleElectron/awarden-NtupleULV12Lepm_WGen_20162-6c713230aa0ceeadd4e46af21c02861b/USER', 30128366)
SinglePhoton20162F.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20162-3a20cdd6270bd67b03f3e41895bb728f/USER', 54609)
SinglePhoton20162G.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20162-8e37fca25f7b87fad031c77d8be54c98/USER', 931022)
SinglePhoton20162H.add_dataset('ntupleulv12lepm_wgen', '/SinglePhoton/awarden-NtupleULV12Lepm_WGen_20162-5d6f0d6c6c016aacc827317cdfeb6ea0/USER', 986409)


qcdmupt15_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-65a41a5c2850f2a141a7bbe8b9ff696e/USER', 152202)
qcdempt015_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-512c639b69eb63148a092d1889db6c5e/USER', 118)
qcdempt020_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-14711c4079378c1dbcc857a7d0bcfb80/USER', 600)
qcdempt030_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f46440b83330ac7c9c3a7b007c2b0b52/USER', 781)
qcdempt050_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-c4c098cd2215e266592cd72a4c5b1587/USER', 1588)
qcdempt080_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-c74de1dcffcdcefa86c670600121e6cf/USER', 2109)
qcdempt120_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-8525cc1c547c2bb823cfba174f64c660/USER', 3964)
qcdempt170_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-25bf14a378763a99144be8add485b465/USER', 2915)
qcdempt300_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0ec30cb65d72eb3737f2b5227a800ad1/USER', 3218)
qcdbctoept015_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-8ed2d4eb4f9fb3be212fa0a8fdcc2bd7/USER', 163)
qcdbctoept020_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-ead0d7d1993d8d2138297cb970ce7ce5/USER', 1314)
qcdbctoept030_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-0fd822a41f987a96d6376a3141eae255/USER', 8690)
qcdbctoept080_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-eec4c0fcd6c4f6642ae51bc0ebab0753/USER', 11761)
qcdbctoept170_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-bcc1da0946207078cda1fa0154a4f86a/USER', 17031)
qcdbctoept250_2018.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2018-bb9278f71232018a4d6a99a00f640cb1/USER', 17521)
ttbar_lep_2018.add_dataset('ntupleulv13lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2018-9800e1aa139ee5c5660067584c1c7399/USER', 85846327)
ttbar_semilep_2018.add_dataset('ntupleulv13lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3e44ecc6bdeecf14494e0754045d6d38/USER', 166635537)
ttbar_had_2018.add_dataset('ntupleulv13lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2018-2545a52ec1232af37e1b606e6340e1f0/USER', 390542)
wjetstolnu_0j_2018.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2018-fe6ec4b34cefe042599930e75425efbe/USER', 13379708)
wjetstolnu_1j_2018.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2018-854e65285d7f85ce40d27a3f7625e419/USER', 40995141)
wjetstolnu_2j_2018.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0f120f3ac81610dca2fa0e04b08eb148/USER', 23781342)
dyjetstollM10_2018.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_2018-31737584d533d4987aba91dbae3d156d/USER', 454058)
dyjetstollM50_2018.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f2da2c677e5d51f8676a08a8c60847da/USER', 20857731)
ww_2018.add_dataset('ntupleulv13lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-4e88fb2b807275baaaeaf3aa3b4cde1a/USER', 2432849)
wz_2018.add_dataset('ntupleulv13lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-06756e29d86640b26c661303bb6708ee/USER', 943162)
zz_2018.add_dataset('ntupleulv13lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2018-ff2f70c118684d6ad2267e886ce76575/USER', 311187)
mfv_stoplb_tau000100um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-2203535916bdcabfb129fdd41962ace3/USER', 198986)
mfv_stoplb_tau000300um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0bb16c4bbe61fbcd38465fcf689e7b08/USER', 199542)
mfv_stoplb_tau001000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-821dc4a5c7173b6706984293a4924a04/USER', 198269)
mfv_stoplb_tau010000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-e028016ffa2f331914ce4656e206ec9c/USER', 198147)
mfv_stoplb_tau030000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a544628a72a210ba9a15f0d3fa604dd9/USER', 197780)
mfv_stoplb_tau000100um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-1e495360a6bd0ca4d221fa77385b614d/USER', 198372)
mfv_stoplb_tau000300um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-1244ee2198c156cea283cc09a29c4c8a/USER', 203023)
mfv_stoplb_tau001000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-cee9c5ef2e3a14cfcdae4817695e3392/USER', 197602)
mfv_stoplb_tau010000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-5e6baba9cd4252d1fb14888de931bb11/USER', 196154)
mfv_stoplb_tau030000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-736d9ae1c798a8d74df91f94de81c750/USER', 196763)
mfv_stoplb_tau000100um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a8c8675717ec87ca0134301fb84d1a50/USER', 200505)
mfv_stoplb_tau000300um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3349b05660551a1961df4667486c23fc/USER', 200842)
mfv_stoplb_tau001000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3e7fe533ec15d6f8f597f72287c76292/USER', 199860)
mfv_stoplb_tau010000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-cf911f1dea21b93cdd2a00b76262e83a/USER', 198963)
mfv_stoplb_tau030000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3d5269d43d87975011d9c1794b26e999/USER', 198368)
mfv_stoplb_tau000100um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-9b86a1cb8f2b7ab16c4a334d995c31b9/USER', 198211)
mfv_stoplb_tau000300um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-86037bb8a51805911d9b02889554e629/USER', 199368)
mfv_stoplb_tau001000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-4fcf411926050a88adc7e957b72bfe98/USER', 196032)
mfv_stoplb_tau010000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-e45338be234042d5d703c1e7f2d787e5/USER', 197845)
mfv_stoplb_tau030000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-24ecaa7e25bd235af33f12b44bedcaa2/USER', 201533)
mfv_stoplb_tau000100um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f52ad5c9fda48908595183b2821225fa/USER', 202319)
mfv_stoplb_tau000300um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-9934e2800e1e3133529b6958a08dfc8a/USER', 200738)
mfv_stoplb_tau001000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-876880f17859f5b70ba189c7a10e848d/USER', 202348)
mfv_stoplb_tau010000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-1fd6cc30e9a8685cd916e80afe46bb5a/USER', 99747)
mfv_stoplb_tau030000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-5f7a83a909014a1a5d887e19e510f82e/USER', 199087)
mfv_stoplb_tau000100um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-2e568434fecc244f7cebca7d5f66f958/USER', 202114)
mfv_stoplb_tau000300um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0e33184f368ca3f24c4ef4ba00bcc499/USER', 196665)
mfv_stoplb_tau001000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-1561a26b6b806a19d0f61442d64297f1/USER', 196748)
mfv_stoplb_tau010000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-480c8067ceb4d50a7d785869f3a150ac/USER', 99062)
mfv_stoplb_tau030000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-b95b700133ed136c17b4e1495a9fb0b8/USER', 199216)
mfv_stoplb_tau000100um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a383d1b75f0a80183c7aa89f42567ee2/USER', 197949)
mfv_stoplb_tau000300um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-6ed688b5defb80f7649140275399cd29/USER', 198241)
mfv_stoplb_tau001000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-cc21cecea4e00c9b44f51e7754330166/USER', 199473)
mfv_stoplb_tau010000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-cc66ad3d6e48f2d099e12d4914b67509/USER', 98201)
mfv_stoplb_tau030000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f04a4eff031f0d24e4847b5297a20530/USER', 199458)
mfv_stoplb_tau000100um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-c31a87edc625cc9f1408d4034664a7fe/USER', 199272)
mfv_stoplb_tau000300um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f55d8f419ce4196faec385f91ea9ddf2/USER', 200098)
mfv_stoplb_tau001000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-7d34b706a6828f32801ab39a48ac848f/USER', 200807)
mfv_stoplb_tau010000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-048e69cb90d32cf4aca392fac5e615d2/USER', 99970)
mfv_stoplb_tau030000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-01fe99d94a0f2d8b459f1db943964995/USER', 200816)
mfv_stoplb_tau000100um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f4516fce18677b102b9b44c0542a21a8/USER', 199366)
mfv_stoplb_tau000300um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-96bbbefc891d3035235dcfea35f8ba8c/USER', 202756)
mfv_stoplb_tau001000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-4d484d0e986dfac0f3af24898bb272d0/USER', 99806)
mfv_stoplb_tau010000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a15958f0102050b77b3894d91de9362d/USER', 101586)
mfv_stoplb_tau030000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-966423c518d4b09859ef2c8a1d54df8d/USER', 100560)
mfv_stoplb_tau000100um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-be276a48c990847100390a26c8f3e6f1/USER', 200523)
mfv_stoplb_tau000300um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-57f2dbea809e317598c50d8fa2ae0821/USER', 199868)
mfv_stoplb_tau001000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-de37b0e377d6492cc06ffee0bbc39948/USER', 100171)
mfv_stoplb_tau010000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-e39d966ebe0b5776854a9640dbc22c14/USER', 101211)
mfv_stoplb_tau030000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-758ba3248b56c1c1e0c1dcca03c2a8c5/USER', 100346)
mfv_stopld_tau000100um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a0e4dfcbe9b8a7a1e1a3082ea993812b/USER', 197970)
mfv_stopld_tau000300um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-40ef888e64f71c2623026a8ab504fa9a/USER', 198800)
mfv_stopld_tau001000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-ec06f5b6d29089d99b66309f5343f914/USER', 200411)
mfv_stopld_tau010000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-084426d9adc5b5ec0b738a512fc2bcb1/USER', 199856)
mfv_stopld_tau030000um_M0200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-eefb4ead34dee2fd518c9f23dbcef647/USER', 202558)
mfv_stopld_tau000100um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-8c66198e6e4e89460158fcbbb95d0b7c/USER', 196635)
mfv_stopld_tau000300um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3380c21c1dd55c357c0e5a8578aec9b6/USER', 198796)
mfv_stopld_tau001000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-b3a55482be0875775bfb636aa55b65bd/USER', 200543)
mfv_stopld_tau010000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0678eab7911587bd607f565d9a9df4c7/USER', 197769)
mfv_stopld_tau030000um_M0300_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-d561803ffe8317b64c4e104958ab0694/USER', 198495)
mfv_stopld_tau000100um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f916fd08b24933b32051ea5c97eb134d/USER', 201643)
mfv_stopld_tau000300um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-3b750f50f78d670421d6954c550d3620/USER', 197079)
mfv_stopld_tau001000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-9a3fd0af52bd4525739f1cd1f0ce5d4c/USER', 200098)
mfv_stopld_tau010000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f8519ce7492776a86f942b7ebb11bac5/USER', 198270)
mfv_stopld_tau030000um_M0400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f3bab314b100a0b6e6a841e5e10bc431/USER', 203160)
mfv_stopld_tau000100um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-38d2c2cd99e7087890af1683a7cf7b4e/USER', 198964)
mfv_stopld_tau000300um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-0605cd7f37e425dd040920c8508a96e6/USER', 198408)
mfv_stopld_tau001000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-b11d7133db4ef026fb68c8d8a18b73a1/USER', 199759)
mfv_stopld_tau010000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-717e7c76daba71655cd8323c8b4ff03f/USER', 200404)
mfv_stopld_tau030000um_M0600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-12f3edc09e62272b2194fd9c85925343/USER', 200030)
mfv_stopld_tau000100um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-5eae9f2db3d34d11fbb49e0a4ecaf47f/USER', 197872)
mfv_stopld_tau000300um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-674528beb3900983fcbc778f8fea7914/USER', 202036)
mfv_stopld_tau001000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a13b8cc51bc579601c85b6fe0e764f4d/USER', 199217)
mfv_stopld_tau010000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-6bc07623ea9e7f6c063c4c3acdb0f32f/USER', 100507)
mfv_stopld_tau030000um_M0800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-63e7a5697dde99cc9fc71bcd74781f99/USER', 197136)
mfv_stopld_tau000100um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-c6d923633a7324024699bbebfa465ed6/USER', 198858)
mfv_stopld_tau000300um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-daef69d78b32236b2337496053d62d12/USER', 199006)
mfv_stopld_tau001000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-071f7e2cb3a2b54ecb39f2383468a435/USER', 196285)
mfv_stopld_tau010000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-15707caca737545f1c5bc72e9584c43a/USER', 98581)
mfv_stopld_tau030000um_M1000_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-1f82a3c809601d5f8f142ec87a93d877/USER', 197592)
mfv_stopld_tau000100um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-634342480c6ac24e89c98a53a3bcb3c3/USER', 195354)
mfv_stopld_tau000300um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-873de95ff2710b28581bfa24af94c204/USER', 199435)
mfv_stopld_tau001000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-7a1c09788987b0d55c8544d2a0431739/USER', 200103)
mfv_stopld_tau010000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f5e0e639b288227a9e31d569083fd720/USER', 98617)
mfv_stopld_tau030000um_M1200_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-321f7080bbeededaba9c6473daa4022b/USER', 200964)
mfv_stopld_tau000100um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-88328b3783617bd29eb1cf57088b1678/USER', 200045)
mfv_stopld_tau000300um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-36b30f7c36781c73b454dc6e0c16f6f9/USER', 202529)
mfv_stopld_tau001000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-a55e1c079a8223bd3ae9b5eb2e1b0ece/USER', 196708)
mfv_stopld_tau010000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-8cc52bc71736b1e6c158ccb85e76eb0b/USER', 100228)
mfv_stopld_tau030000um_M1400_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-f804069a6b94cdacc000745f81a21685/USER', 201992)
mfv_stopld_tau000100um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-4324ef781f07e3224a768b760e1097f0/USER', 201300)
mfv_stopld_tau000300um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-33ddff010a3b9705b30f11efe01d052d/USER', 197421)
mfv_stopld_tau001000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-6f6a62f6a09c9413b91a81c0e307a8dd/USER', 100838)
mfv_stopld_tau010000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-424afb8ee4f2d33e81fd51010b520117/USER', 99387)
mfv_stopld_tau030000um_M1600_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-02de7a47115836934e7e7d7864072477/USER', 97752)
mfv_stopld_tau000100um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-487c3225292f2c42163d34f88898da54/USER', 202746)
mfv_stopld_tau000300um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-673fc015d025b2e8ba17262696843c88/USER', 199924)
mfv_stopld_tau001000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-05216fe08c2e4d1230f9ca7b048aed47/USER', 99515)
mfv_stopld_tau010000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-25a85c062bb937e491c9cb35a3c1cd70/USER', 99400)
mfv_stopld_tau030000um_M1800_2018.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2018-ec73969f243dd80a38065a5edcce5892/USER', 98449)
SingleMuon2018A.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2018-0e0c81fbe36b9d77dbc973325ab0d014/USER', 101542055)
SingleMuon2018B.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2018-bc9515c2ef4affbf71f7bcff8d882ee9/USER', 50628630)
SingleMuon2018C.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2018-9ce76329a2b872e7eee0205cd4a33924/USER', 49668378)
SingleMuon2018D.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2018-a1abaa1ba1c3ce0a2fa2665f5e11bb70/USER', 222864757)
EGamma2018A.add_dataset('ntupleulv13lepm_wgen', '/EGamma/awarden-NtupleULV13Lepm_WGen_2018-8ab0ee13d8fa917030583f83a702a2da/USER', 48501311)
EGamma2018B.add_dataset('ntupleulv13lepm_wgen', '/EGamma/awarden-NtupleULV13Lepm_WGen_2018-8c475a12ad5a2bc78f5482922317875c/USER', 23809358)
EGamma2018C.add_dataset('ntupleulv13lepm_wgen', '/EGamma/awarden-NtupleULV13Lepm_WGen_2018-4eed39286f06712a28da16c719cf9143/USER', 23801542)
EGamma2018D.add_dataset('ntupleulv13lepm_wgen', '/EGamma/awarden-NtupleULV13Lepm_WGen_2018-5d9e324fa4f4496f9b6323aed4ca15e2/USER', 108056280)

qcdmupt15_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f86d75b665b50290d4406b6e1c5bab28/USER', 160715)
qcdempt015_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-b7dac92c27395c698c286cd8eb6a0bd4/USER', 225)
qcdempt020_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-d6021b773ed8432b7c6b4b41f07add32/USER', 752)
qcdempt030_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f3ae54c9e520ec4f61d9874e5ac9c8ac/USER', 953)
qcdempt050_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-0357c0700c0fc047840e1f5a4ef788ff/USER', 1445)
qcdempt080_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-0e51518ed918bd44b37b4efb203c4c14/USER', 2070)
qcdempt120_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-e208efe2a1b9b4ea99e08ce7c61e5005/USER', 4117)
qcdempt170_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f55d28af4aed87a7bd0dd885d19b89f7/USER', 2901)
qcdempt300_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-06897c50c725e565276cb55b52fa265d/USER', 3346)
qcdbctoept015_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-9eb1541657137bfa135f5675d349e316/USER', 314)
qcdbctoept020_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-de4ae1689c3db7f6a42beb57351680d5/USER', 1809)
qcdbctoept030_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-0680d28e9e77081160e9ddcf73ab6259/USER', 9357)
qcdbctoept080_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-80ff6b34b025f00b3436a574b03e6ff6/USER', 11200)
qcdbctoept170_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-1e030724a6d35286d294c59c9e00f30c/USER', 17203)
qcdbctoept250_2017.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_2017-3aa460ecbaefa64e80c6e60fe1788857/USER', 18289)
ttbar_lep_2017.add_dataset('ntupleulv13lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2017-ea1cbbcebc952bfe8fb90ad431761b45/USER', 59002156)
ttbar_semilep_2017.add_dataset('ntupleulv13lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2017-2b8948cb9fd5ffa708edee62d0331bcf/USER', 119703854)
ttbar_had_2017.add_dataset('ntupleulv13lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_2017-df62034bb37b42692ab991252d7c96c8/USER', 275997)
wjetstolnu_0j_2017.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2017-27f2b5445cc945230301808c723c66e4/USER', 13758077)
wjetstolnu_1j_2017.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2017-29d270f6baadc410d36d2f62cc29c664/USER', 40076652)
wjetstolnu_2j_2017.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_2017-8f975607246a3977fdbb4f07de14ec0b/USER', 23667883)
dyjetstollM10_2017.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_2017-248260236475d1912c71371dd87af3fe/USER', 340547)
dyjetstollM50_2017.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_2017-b4554539022cb0d4c3e8353a7ecb000a/USER', 22813073)
ww_2017.add_dataset('ntupleulv13lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-478be41f5e50abdab2eab1b85e9b93ec/USER', 2402807)
zz_2017.add_dataset('ntupleulv13lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-e228e547ebc3214749781cdf7fcafd94/USER', 237304)
wz_2017.add_dataset('ntupleulv13lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f37e27c5e9b7df60919856d468d66eb4/USER', 931264)
mfv_stoplb_tau000100um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-92d2d902f089268e8538dae4855d093c/USER', 194928)
mfv_stoplb_tau000300um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a6d8dc5660d08dcc301fd7faf1127486/USER', 200301)
mfv_stoplb_tau010000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6e8406a6c970c63f2a03cc5b639a561c/USER', 98261)
mfv_stoplb_tau001000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-76cf2bd132d60168613c3ed1716f1be2/USER', 197193)
mfv_stoplb_tau030000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-59e4cea0b566878805cffe529bd157fb/USER', 200668)
mfv_stoplb_tau000100um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-67b3a62f8343e7b4d2ef07ff15c15ac6/USER', 199921)
mfv_stoplb_tau000300um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-3fcb407a1d44ad9352f3fc2b68011d50/USER', 195189)
mfv_stoplb_tau010000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-35bdea8e1f113376f29fe9aeea08a680/USER', 100156)
mfv_stoplb_tau001000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-85ba8a111d693d33b1e6a7040f3e0dc8/USER', 197902)
mfv_stoplb_tau030000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-7b04f4333b602044eecebb4f02bcdb68/USER', 200464)
mfv_stoplb_tau000100um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-21e8d78a2ff05997ba2006a959812a1b/USER', 199322)
mfv_stoplb_tau000300um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fbd797d8ef5b20062180a64e9427b1f2/USER', 200304)
mfv_stoplb_tau010000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6b1ae40728d4a1293fd5cd299483e973/USER', 98900)
mfv_stoplb_tau001000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-1afb6b2da2af83aa3b4e21adddf75568/USER', 196297)
mfv_stoplb_tau030000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-1524735ec2dc0a029ef3af2609730590/USER', 198644)
mfv_stoplb_tau000100um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-e18088c0fc55b1fecd92dd593055450e/USER', 202021)
mfv_stoplb_tau000300um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-d2bf738b58920cf2e05823048a661b75/USER', 199079)
mfv_stoplb_tau010000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fec9271d73c6d004a7214d12325aab60/USER', 98745)
mfv_stoplb_tau001000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fb98a68791d5563c534d14dcd4313e39/USER', 98921)
mfv_stoplb_tau030000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a21e2449f94dc2b6f58ac159212f83e7/USER', 100284)
mfv_stoplb_tau000100um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-45899340d61324084f1328db5eeec521/USER', 199639)
mfv_stoplb_tau000300um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-3bdc7d3d99dc361001be1e507063fae4/USER', 200792)
mfv_stoplb_tau010000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-5bf78d062ad33b89feab5da89cb9c114/USER', 101386)
mfv_stoplb_tau001000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-67fed6370af0feb8a5a7dd4c98dc018b/USER', 98858)
mfv_stoplb_tau030000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-70f9b521c6b3e4995956ea322609fcd5/USER', 100172)
mfv_stoplb_tau000100um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-bfb5df607a888a6c78d9283151b07cba/USER', 198760)
mfv_stoplb_tau000300um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fb3614e486e42426463053cd7bca1287/USER', 198899)
mfv_stoplb_tau010000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6b126fbb0c7162a2d9cf019ab8491518/USER', 199948)
mfv_stoplb_tau001000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6e04331a21618f1284dc43d4531a1eda/USER', 196687)
mfv_stoplb_tau030000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-3da9611c72711e06b5063bfb37107fcf/USER', 199267)
mfv_stoplb_tau000100um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-7a6e3664c9fd9b945e09ff4e60d77688/USER', 198231)
mfv_stoplb_tau000300um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-af006c1bf921ba1ae77a1084e2955c3e/USER', 198170)
mfv_stoplb_tau010000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-b4637e0156e39d6b592b7cddcd5fe79f/USER', 199832)
mfv_stoplb_tau001000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f1e5a0e429f7a10758e259064401ac05/USER', 200296)
mfv_stoplb_tau030000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-0eff33029101f925bd7044c65350bc35/USER', 200170)
mfv_stoplb_tau000100um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a61d1e8010fd6e99caebfa54df57ca67/USER', 197597)
mfv_stoplb_tau000300um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a824e2b5ed405da00af47063eb3708cd/USER', 200230)
mfv_stoplb_tau010000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-54069676d2239cf4e3c9697c57f182f1/USER', 198737)
mfv_stoplb_tau001000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fa62bf11770bcb48f101264bfa24e7ea/USER', 197003)
mfv_stoplb_tau030000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-395c37691b0431ae517ace8610c36b3c/USER', 198930)
mfv_stoplb_tau000100um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-13bb174116ec070ff541b3a6109c1e80/USER', 201812)
mfv_stoplb_tau000300um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-41b70fc8b4bc17e812d2b57eba13448a/USER', 201839)
mfv_stoplb_tau010000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a1de78e44817126962bd7de6699189da/USER', 197409)
mfv_stoplb_tau001000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-1245f6771d091b39da4a5fdd4e17b33e/USER', 195368)
mfv_stoplb_tau030000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-c3539038603057fed8858bdfc6165b43/USER', 200005)
mfv_stoplb_tau000100um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-981ef471a7a039333138733f6f1b4d4f/USER', 198566)
mfv_stoplb_tau000300um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-47ef32fd5eb3f7503f8dd179c8e3b58b/USER', 197615)
mfv_stoplb_tau010000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-40d5abd48cbf376d3e5b7e1a948bbb26/USER', 98799)
mfv_stoplb_tau001000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6a174fc57e04cdf7aa8a44bc3e1dc183/USER', 197479)
mfv_stoplb_tau030000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a292e3da925f6bf5dec6b9f5b6433aa2/USER', 201690)

mfv_stopld_tau000100um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-e783ee5a9df6df3063aad92e2cfd43c5/USER', 199076)
mfv_stopld_tau000300um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-62843d4e002c22430c229ee1d24882d9/USER', 198992)
mfv_stopld_tau010000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-65799d6be30111ccec801e65c1f9b02b/USER', 98679)
mfv_stopld_tau001000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-9b9540da98b441476de3e6c533222163/USER', 198608)
mfv_stopld_tau030000um_M1000_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-1ae1a209d78659e324b40d88dda7a624/USER', 199499)
mfv_stopld_tau000100um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-7908941434f06876d1e21200642b90fe/USER', 198263)
mfv_stopld_tau000300um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-7c01e230f53f6c8ff25c2e47cd925cfa/USER', 195508)
mfv_stopld_tau010000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-444fdfe4aa86e352ffb02d1f027ba49c/USER', 100349)
mfv_stopld_tau001000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-cdb4c2dde30b389990f1d32dfc2df037/USER', 201191)
mfv_stopld_tau030000um_M1200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-fa8b5b4ce13fa0c8f79d9738171c6539/USER', 200851)
mfv_stopld_tau000100um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-eae3a3c4e29ca2c377ebeeeaf9c5442c/USER', 198812)
mfv_stopld_tau000300um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-aef602f99a96fc2def5e213c577d0256/USER', 194591)
mfv_stopld_tau010000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-1cb689deaf8b3843b1e2bc0915d1fe4f/USER', 98583)
mfv_stopld_tau001000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-45537dc069243aa409ed7b87ffbd123e/USER', 198538)
mfv_stopld_tau030000um_M1400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-7ecdfb4d1d443dd7eeb6d89c0541c342/USER', 200714)
mfv_stopld_tau000100um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-d7524eb4d6119b6011367603cbd0fbcd/USER', 201051)
mfv_stopld_tau000300um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-5f60a0b27452ee7cf80c51c2fdf9ae73/USER', 196540)
mfv_stopld_tau010000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-63e1c552bdffe3555aede9569bc5cb2d/USER', 100274)
mfv_stopld_tau001000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f40a579e7bdda2d0ffcb54161c78e43c/USER', 99126)
mfv_stopld_tau030000um_M1600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-23634bb05ea538aaaa2f5a1dabe5206b/USER', 100345)
mfv_stopld_tau000100um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-edf4c075ce5e8636a0cfc2bb755d6c96/USER', 200828)
mfv_stopld_tau000300um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-c6c94c65d36d832a315f6e108efd86e9/USER', 198147)
mfv_stopld_tau010000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-32337bce8d0ad97f243a0bb444f7e89e/USER', 99667)
mfv_stopld_tau001000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-86fa5c45dcf0c7731f6087b61a99f27b/USER', 101005)
mfv_stopld_tau030000um_M1800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-47c23f8022e0c2fdfa0411bac6f434cd/USER', 99787)
mfv_stopld_tau000100um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-8f3040608928484fdec5978c3448ce97/USER', 201843)
mfv_stopld_tau000300um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-67b45bdd3ce98e27f81f5fc612a038e4/USER', 199789)
mfv_stopld_tau010000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-18d8215ef5bf59501ee07d64b215cb5e/USER', 197403)
mfv_stopld_tau001000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-903ec86b2ebbb9bead501a7d91328c6d/USER', 198275)
mfv_stopld_tau030000um_M0200_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-5a0766e6d732f0968b5e954d0e1e6538/USER', 198511)
mfv_stopld_tau000100um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6c70027cfaf43c6d41537566c54dfe92/USER', 197379)
mfv_stopld_tau000300um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-e5a6ac160dfc6c3bbaeab4c3483c6bae/USER', 197934)
mfv_stopld_tau010000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-6b97776c91a8b1eda71c0fa745bf63ed/USER', 197990)
mfv_stopld_tau001000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f5405f5b277377079f35b1f4eb3ce831/USER', 199705)
mfv_stopld_tau030000um_M0300_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-88a6ff6bd154fa7f30534084f5e35c86/USER', 199931)
mfv_stopld_tau000100um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f6eaaa314d8648a1105de1ccd0fe1b66/USER', 202735)
mfv_stopld_tau000300um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-87b3586a53cdb62a79c5d9497780b22b/USER', 199890)
mfv_stopld_tau010000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-c2584c44ec1e145c1fc06ec38a946f3e/USER', 201845)
mfv_stopld_tau001000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-a558d7063292a20759e8aa56fe7e722d/USER', 197130)
mfv_stopld_tau030000um_M0400_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-2663db4cf3aad3cd2292dbe856a6267f/USER', 198731)
mfv_stopld_tau000100um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-80849d592fea7c0aea9548dbd3954b92/USER', 203406)
mfv_stopld_tau000300um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-90d3dc50f240875c9db1c17bb8fb58e6/USER', 199321)
mfv_stopld_tau010000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-0412e74d1b34071809bdb54cdcb26bfa/USER', 194815)
mfv_stopld_tau001000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-74121a278f73439812f8d5ef5bea60c7/USER', 203302)
mfv_stopld_tau030000um_M0600_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f2cbfe2f1ace34d7c8b5ff1d8bda347e/USER', 199944)
mfv_stopld_tau000100um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-019982b3c6fe6c02a22d3ded132debfd/USER', 200077)
mfv_stopld_tau000300um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-f2f4ceb10908f7844369108db59b00eb/USER', 200814)
mfv_stopld_tau010000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-d53cf7b50739b45bac6a1a6980593be6/USER', 99313)
mfv_stopld_tau001000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-eec90a335998a986f0e96e8548f1a94a/USER', 200829)
mfv_stopld_tau030000um_M0800_2017.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_2017-611b81dc8365063de6180bda45758967/USER', 200140)
SingleMuon2017B.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2017-bff400dfc9d6647ae1c184c0b904a261/USER', 31942702)
SingleMuon2017C.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2017-2c429bd19703f96ba7ff7195820d82ff/USER', 63065893)
SingleMuon2017D.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2017-d79d852efef19d6fb872cd07fec5b448/USER', 28219236)
SingleMuon2017E.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2017-caeb5930edd538584fe627352350fe81/USER', 70203674)
SingleMuon2017F.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_2017-7b8247e07a6422241d08d0f34734a242/USER', 112143201)
SingleElectron2017B.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_2017-93852986c96273984544db1e4d49635a/USER', 16875475)
SingleElectron2017C.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_2017-a7e53f8f5f975edfcad5036240591f79/USER', 36590420)
SingleElectron2017D.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_2017-3c9a4aa63b5eda5cb2c80aaf58a281c2/USER', 16385241)
SingleElectron2017E.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_2017-5d253d7b4f743b38d9c13040bd0e9dba/USER', 35692155)
SingleElectron2017F.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_2017-b7ea70c558a18e0d08d2ee528b94b344/USER', 45959718)
SinglePhoton2017B.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_2017-8eeb9919ae6d16ef13750e66ce47f953/USER', 263891)
SinglePhoton2017C.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_2017-4396691286a6a6e1b68669710cbee738/USER', 895521)
SinglePhoton2017D.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_2017-73fb5a41a61520d3bb018994e0b98d7f/USER', 224902)
SinglePhoton2017E.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_2017-25773c255a4d6194e27e03798fd33afa/USER', 405554)
SinglePhoton2017F.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_2017-a7d027ad9b95f0d5e751057561ac1208/USER', 778992)

mfv_stoplb_tau000100um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-2d6c9e19162ccdb405e06e658649a518/USER', 98890)
mfv_stoplb_tau000300um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-7848978bdf9e035bd2225d0f3c5af84b/USER', 99090)
mfv_stoplb_tau010000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a237846027faf2d80456e8dea2658f3d/USER', 49863)
mfv_stoplb_tau001000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-ad00fa9f02ad6f176eeecd17c2328610/USER', 99632)
mfv_stoplb_tau030000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-d2da9a7ee66e46c5b332384a6c26e099/USER', 99612)
mfv_stoplb_tau000100um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-2747829a63a2116f2e65fc1456d8911b/USER', 99340)
mfv_stoplb_tau000300um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3803b78197b27c837a1491aa5c408696/USER', 99010)
mfv_stoplb_tau010000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-2ba9dfe05b6d2477079bf7b9766fcca7/USER', 49944)
mfv_stoplb_tau001000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-d02e4b20b75747bc650a542616838f30/USER', 97995)
mfv_stoplb_tau030000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-97be7a79db41ebb4ac4e6055c1ffdec8/USER', 101825)
mfv_stoplb_tau000100um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-56c5de6ab17ee0fd6d4d25c1aab69a33/USER', 100444)
mfv_stoplb_tau000300um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-4cb1f35df96c2f029f7b94f6145e62e4/USER', 98629)
mfv_stoplb_tau010000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9e21a7a07c0d96646a8e214d726fd3f8/USER', 49531)
mfv_stoplb_tau001000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-0b58b6560d542a2dfd92f3244946c4fa/USER', 99778)
mfv_stoplb_tau030000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a8e6780e061ac4210e44c20e5e09d32c/USER', 99896)
mfv_stoplb_tau000100um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-2649fcea97fbc027ecaac2a1cc837587/USER', 99251)
mfv_stoplb_tau000300um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-6c0b0f44435ca92fd02ab7788e30ea9e/USER', 99184)
mfv_stoplb_tau010000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-0fb820e613c4902150e4559f089072e8/USER', 50317)
mfv_stoplb_tau001000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-764f55747b0ef5adc1c446866101b99d/USER', 49741)
mfv_stoplb_tau030000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-51734baedf646442fed3d692d9a21600/USER', 48712)
mfv_stoplb_tau000100um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-cf293bfde3f85944d2a6ebac8438897a/USER', 100766)
mfv_stoplb_tau000300um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3863a2533a984d3681f9d7dbfe62b026/USER', 81729)
mfv_stoplb_tau010000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-f6811ba85d81cda442faf2f799fd342d/USER', 49090)
mfv_stoplb_tau001000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a43262f126509dfee35635bae3f36029/USER', 49049)
mfv_stoplb_tau030000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3da7b07efde3c3c7df74dd70c0b4cd0e/USER', 49438)
mfv_stoplb_tau000100um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-50e5826121b4bde06c271a8099c7fd30/USER', 99188)
mfv_stoplb_tau000300um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-26d54514261bb8a0946c8e9385fba299/USER', 100726)
mfv_stoplb_tau010000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3f57614309feea6bd2ad6c4b43ff9ba9/USER', 99023)
mfv_stoplb_tau001000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-4aa832580180adf72e7a2ceb88096161/USER', 99012)
mfv_stoplb_tau030000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9f162a610e020c1b8f7dcce83b2f1960/USER', 99812)
mfv_stoplb_tau000100um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-0e87616e728b23bd49d5070ef15134e0/USER', 100222)
mfv_stoplb_tau000300um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-12effc6549ecdaa484acd5006f544a69/USER', 100150)
mfv_stoplb_tau010000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-95c6ad12d6b2ba08230ed55ec0167efd/USER', 98854)
mfv_stoplb_tau001000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-04393c086d93388d92203d22da915686/USER', 100049)
mfv_stoplb_tau030000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-11d984ae86d11ff7ecc00842cd80c2dd/USER', 99401)
mfv_stoplb_tau000100um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-8996f4f6147312cd848c23115f847c66/USER', 100672)
mfv_stoplb_tau000300um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-c0cab0ceed276631f9c45cb760ecb963/USER', 98457)
mfv_stoplb_tau010000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-29c2c949f9446dc2a66e405969f0c59d/USER', 99343)
mfv_stoplb_tau001000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-f406cf8a6324710a1fda7e3b0a9d1817/USER', 99760)
mfv_stoplb_tau030000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-c601f58db545733068fb23e51a2c4bce/USER', 98676)
mfv_stoplb_tau000100um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-138e07a85e689758d22d7631086b0588/USER', 100158)
mfv_stoplb_tau000300um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-7d03dbb1daa24a6534d4f305ce221c65/USER', 98762)
mfv_stoplb_tau010000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-d83d0a9e04eccce53addf11289441a83/USER', 99264)
mfv_stoplb_tau001000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-81869ac95129efac9c4569d4da8fdfbf/USER', 101849)
mfv_stoplb_tau030000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-dfdca31f22a0e4271ffbca9922bab3aa/USER', 100390)
mfv_stoplb_tau000100um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-704e354a054a68b83c6eb8cf19799a08/USER', 98204)
mfv_stoplb_tau000300um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-bbf1cdf325fad9cf3b47bbcc45a01fdc/USER', 100784)
mfv_stoplb_tau010000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-fc6a10c57a70bcb099edc07c631494b8/USER', 48963)
mfv_stoplb_tau001000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-4fb9ea46fd73e0481ccf52b2c03a646d/USER', 100377)
mfv_stoplb_tau030000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-7b729826a6fad24d826d9e29aa575757/USER', 99164)
mfv_stopld_tau000100um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9aa80197a760599808f53b7446c27e39/USER', 99017)
mfv_stopld_tau000300um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-6e109f697fa5f557e7ab67ccab676b5f/USER', 99362)
mfv_stopld_tau010000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-baf20bbb374f1c8a73f8e0f4f65909f2/USER', 49856)
mfv_stopld_tau001000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-d5d7138804b2591f35a4883de87caeb8/USER', 98183)
mfv_stopld_tau030000um_M1000_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-6f7c860ec31c1effb1c7498cc6f4f370/USER', 100852)
mfv_stopld_tau000100um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-f1fb915da4f3b4c4cc9ad7da1eed36a2/USER', 99830)
mfv_stopld_tau000300um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-e2de4f2070988576850f2f696becaf3d/USER', 99813)
mfv_stopld_tau010000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b18af3f8e92df5ca0514404ded3b1701/USER', 49767)
mfv_stopld_tau001000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-69e2b182beb0e8f62e280c19edc08b67/USER', 100012)
mfv_stopld_tau030000um_M1200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-0b57344b276b73a0b43288633f5a7c63/USER', 99996)
mfv_stopld_tau000100um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-c7b4f56c48239483699770df8eb9b091/USER', 100303)
mfv_stopld_tau000300um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-09d48f437b167d0c52f46fd2bafa7f57/USER', 98700)
mfv_stopld_tau010000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-1468a4daf3eee50cff345a1478e868ba/USER', 49501)
mfv_stopld_tau001000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-af18bb39e73a3360c2d16130833b97e0/USER', 99221)
mfv_stopld_tau030000um_M1400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b46580b43f80dea8b474effea1c04a54/USER', 99706)
mfv_stopld_tau000100um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-bcddac6abdfeccfe6151ec517241470c/USER', 98875)
mfv_stopld_tau000300um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a398306a6f2d32679c249e79071ab5d1/USER', 98632)
mfv_stopld_tau010000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-bdca4c0c90060eda55bd9eb59fe8567a/USER', 49359)
mfv_stopld_tau001000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-1772fd81decf195aac51ac93a30474ce/USER', 50121)
mfv_stopld_tau030000um_M1600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-4b2d43b7735390bacba8a0c3bcca2281/USER', 50681)
mfv_stopld_tau000100um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b030451a3ef639d1fc49a5415a455ebe/USER', 99761)
mfv_stopld_tau000300um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-8c0bd3b55b3489393bd2300e7dec9d08/USER', 100032)
mfv_stopld_tau010000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9b0efa4e641d27d9c3461a2324296ab7/USER', 49884)
mfv_stopld_tau001000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b86f876b9e2dbd00fa06337d5c57e127/USER', 49871)
mfv_stopld_tau030000um_M1800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-1f3a5972d0180d641071cc5ecde1bca2/USER', 49634)
mfv_stopld_tau000100um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-264a6be32138946cdffd9c9e7b745674/USER', 101080)
mfv_stopld_tau000300um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-ac31748dfb4aa9023cd8f899b3eeaa7d/USER', 98938)
mfv_stopld_tau010000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-73241c4f6c203f1e70050e15b61332b3/USER', 99845)
mfv_stopld_tau001000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-57ebad86a6db07ce37774a82ff00bfec/USER', 99943)
mfv_stopld_tau030000um_M0200_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-4fc1e176b5ba1b451e3cf915b0fa448d/USER', 99418)
mfv_stopld_tau000100um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a58fc8a10923f1d14a52adac5fc944a1/USER', 101171)
mfv_stopld_tau000300um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-768f6b77bbbcd454317189e77b66197e/USER', 100455)
mfv_stopld_tau010000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-1b48aea68e312c3c5344bd2d3973b72d/USER', 100892)
mfv_stopld_tau001000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-78e342b745ec67975764f79a50b5bde3/USER', 99556)
mfv_stopld_tau030000um_M0300_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b54d4e7d78065b041cfba3b034c2749b/USER', 99447)
mfv_stopld_tau000100um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-7b3bb80c56526da3ba0af76cd69e1af4/USER', 100509)
mfv_stopld_tau000300um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-d489fae58771a959c1cdc04ce7055c69/USER', 99765)
mfv_stopld_tau010000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-793922b9460f9f055652db5d435ae84b/USER', 99682)
mfv_stopld_tau001000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-01d1e395dfc63d4481b6f56832c6b0f0/USER', 99890)
mfv_stopld_tau030000um_M0400_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9c61d69c6b1fa99cd60cbc2c4ab51143/USER', 99531)
mfv_stopld_tau000100um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-cca35e6a6728511d1726f59134dcdc27/USER', 100034)
mfv_stopld_tau000300um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-31961e241f9c2617c8728aed0ca5eea0/USER', 99611)
mfv_stopld_tau010000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3220f94ed173cfdcaad996ca989643a2/USER', 99643)
mfv_stopld_tau001000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-c978bd900cf0a77ace29d1880eaf4ea4/USER', 99924)
mfv_stopld_tau030000um_M0600_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-5fd5ce599dd0250d893676c8e726bf1b/USER', 101612)
mfv_stopld_tau000100um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-7ea156b1c723fc057dc29e96bd2d256c/USER', 100466)
mfv_stopld_tau000300um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-1fd6474cfc1927c4697f345c68b13e05/USER', 98676)
mfv_stopld_tau010000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-9079d1d551eee207f82be811224f7482/USER', 50147)
mfv_stopld_tau001000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-3d66c8d033bbd45f177f7010cfdd2eee/USER', 98387)
mfv_stopld_tau030000um_M0800_20161.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20161-ec393078c9a2f757b29fe3288b77576f/USER', 99914)
qcdempt015_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-49b881416adadd2be0ef875994c7446a/USER', 79)
qcdmupt15_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-5aa7714bc223c7067d75fa2d30d55d74/USER', 61292)
qcdempt020_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-fdadca3742943a8dc9d4dc0ed3ac1379/USER', 331)
qcdempt030_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-5e3d1f478e9adb62eab70b7850fdd0d7/USER', 392)
qcdempt050_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-50abdb72a12e37b7996a07aa8dce2c73/USER', 752)
qcdempt080_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-70f84adbf725c7ea9c03864f445ca722/USER', 1157)
qcdempt120_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-dd613c1de26f57b7f46e11f9178ed609/USER', 2407)
qcdempt170_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-830958cdca50bd66ef5692afd98722bb/USER', 1711)
qcdempt300_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-253602841ff68e93ffd876556860a689/USER', 1904)
qcdbctoept015_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20161-980237d78fe22319e81b9f64cd6ec902/USER', 61)
qcdbctoept020_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20161-1841f8002a75840a55800b9b24a5ded7/USER', 514)
qcdbctoept030_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20161-1e0aefa8a89b40c28318fb85635372de/USER', 3390)
qcdbctoept080_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20161-aca34ffa2007b6ab9a798226b9470212/USER', 4538)
qcdbctoept250_20161.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20161-f2e6eaf945be694da22d0ffcfd91a9fc/USER', 6663)
wjetstolnu_0j_20161.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20161-142f54ea86cc9de02a958560f46bc056/USER', 8276916)
wjetstolnu_1j_20161.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20161-55c84064f7de83c10df97a5ffb60d56b/USER', 36194552)
wjetstolnu_2j_20161.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20161-8c612b36afffdf481d67ea8abeb3749b/USER', 20716459)
dyjetstollM10_20161.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_20161-b7795350d146589d89051dd9d7357885/USER', 113479)
dyjetstollM50_20161.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_20161-dd0e6e4db834665be3b94fab41294e55/USER', 16619811)
ttbar_lep_20161.add_dataset('ntupleulv13lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20161-edf01ea3db896e5af5b9f87919e845a1/USER', 21241090)
ttbar_semilep_20161.add_dataset('ntupleulv13lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20161-efc5a1b9edf28e26ee367ec2c0761398/USER', 43866176)
ttbar_had_20161.add_dataset('ntupleulv13lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20161-f28b4b97ab83941cf0a6e1b30146cbdf/USER', 90369)
ww_20161.add_dataset('ntupleulv13lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-c4a76e7f7431eddc77f62cd43f146e56/USER', 2257496)
zz_20161.add_dataset('ntupleulv13lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-a9d36970c0996ec532432f841a9388ef/USER', 105059)
wz_20161.add_dataset('ntupleulv13lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20161-843580990d5c33f93506cb1920054467/USER', 870913)
SingleMuon20161B.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20161-21d9785c05df4636513382a227f697db/USER', 29464393)
SingleMuon20161C.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20161-f31fdcb6c3d8a788d0501567e5ba594d/USER', 13621479)
SingleMuon20161D.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20161-45256a3d1a5759dd76483af4cf50c1b6/USER', 22336062)
SingleMuon20161E.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20161-763b8652268593f02ea92f16c7539469/USER', 23496791)
SingleMuon20161F.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20161-8503370f38d015668975c99bdf3af8a9/USER', 15905137)
SingleElectron20161B2.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20161-d31b0f6eb4f7085468e31f03687636dc/USER', 21038786)
SingleElectron20161C.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20161-5327ff27e81ad1af6e198c4737f94d2d/USER', 9411697)
SingleElectron20161D.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20161-f608273d32f5b1d6785b36cd90c6b27a/USER', 15439927)
SingleElectron20161E.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20161-523c86aff33e270da60b0d54f490476b/USER', 15215399)
SingleElectron20161F.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20161-079c9ed22759a8cf7556c28da37670a0/USER', 9853494)
SinglePhoton20161B.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20161-8bb70cc9cb9a894b7a619d217f8efa86/USER', 2367665)
SinglePhoton20161C.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20161-627c867a94099eeb5d2a68083bf4c4c7/USER', 881454)
SinglePhoton20161D.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20161-c8c21e83422582d42ea2b87f48b8206c/USER', 1033532)
SinglePhoton20161E.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20161-693547c4168a7238e838fcfa26a5fc3d/USER', 641047)
SinglePhoton20161F.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20161-3b7b8615bd0147dbc617303366fcb256/USER', 355558)

qcdempt015_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-4c3e7943764fad4ccbb376cb1a966d75/USER', 77)
qcdmupt15_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-0f3f5374ff98c286588fddbeabaa264c/USER', 62952)
qcdempt020_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e0f3a957adc1e8ace05c0c350a889c7b/USER', 264)
qcdempt030_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-20fef3151ad76db7c9e788eabf5668f5/USER', 399)
qcdempt050_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ece3a335f20aa9d58125bfe5fadecbb9/USER', 788)
qcdempt080_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-668e16e9a1444f638721398560e6b382/USER', 1175)
qcdempt120_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-b3124f39a7e9d425b54a29cfda84bf57/USER', 2511)
qcdempt170_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f6b2b1b87e7b67166bbc00692c8d503b/USER', 1747)
qcdempt300_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-142ec65b3e51d6905b45f2e8c43e122c/USER', 1986)
qcdbctoept015_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-e93ac1fb2bfb293303f634161c144ae1/USER', 86)
qcdbctoept020_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-23450b0a82649bcaca1d3ced87b9a141/USER', 508)
qcdbctoept030_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-a391977bd713b651e1e0759a545ba906/USER', 3216)
qcdbctoept080_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-f6ad8ceb3941bc372d4d8e3b3987d4e6/USER', 4800)
qcdbctoept170_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-0bc7642f7476849eecc0b9d76eb6282a/USER', 7690)
qcdbctoept250_20162.add_dataset('ntupleulv13lepm_wgen', '/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/awarden-NtupleULV13Lepm_WGen_20162-42f0221708fdb9d5dc046d2b2e2f49fc/USER', 8166)
wjetstolnu_0j_20162.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20162-6229886bfb10b0a787020d44b609b428/USER', 8944616)
wjetstolnu_1j_20162.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20162-28874c3de701d43d85694bd96af18009/USER', 35869126)
wjetstolnu_2j_20162.add_dataset('ntupleulv13lepm_wgen', '/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/awarden-NtupleULV13Lepm_WGen_20162-7dd54ac75cf10152d03f56f9081fdcf9/USER', 20659862)
dyjetstollM10_20162.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_20162-afab77dda4336a99499177b51454b834/USER', 107239)
dyjetstollM50_20162.add_dataset('ntupleulv13lepm_wgen', '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/awarden-NtupleULV13Lepm_WGen_20162-b4595e889fd19b60e6099264561a7e2e/USER', 14563190)
ttbar_lep_20162.add_dataset('ntupleulv13lepm_wgen', '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20162-1c98815406eaa193237682f95e04df5c/USER', 25094894)
ttbar_semilep_20162.add_dataset('ntupleulv13lepm_wgen', '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ebaca356890453292def3309ae1a9c83/USER', 49127316)
ttbar_had_20162.add_dataset('ntupleulv13lepm_wgen', '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/awarden-NtupleULV13Lepm_WGen_20162-58d8769061808f4f76a2034e071a9ef4/USER', 103282)
ww_20162.add_dataset('ntupleulv13lepm_wgen', '/WW_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-08219970d86272bb0b209960121fae71/USER', 2301748)
zz_20162.add_dataset('ntupleulv13lepm_wgen', '/ZZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-34eef680912f61c811a68efb5112457b/USER', 95892)
wz_20162.add_dataset('ntupleulv13lepm_wgen', '/WZ_TuneCP5_13TeV-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e628faa1fb5ba00aa24eaf01e63ae8da/USER', 847183)
mfv_stoplb_tau000100um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-04f923425de002d344a56ef4f1ed9b86/USER', 99539)
mfv_stoplb_tau000300um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-314d45172c13a1d9ea7bd67d4efb3a12/USER', 99257)
mfv_stoplb_tau010000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-02f5237dac814236e8cb0d4c4370f9f9/USER', 47714)
mfv_stoplb_tau001000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f51ea6ff5e1d4da0ac48684881f10549/USER', 98557)
mfv_stoplb_tau030000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-bdd47668c7482079b3767e20694fae8b/USER', 99898)
mfv_stoplb_tau000100um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-670ab8aae40227252ec4de08674de85e/USER', 100330)
mfv_stoplb_tau000300um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-3aaf563aa4d997dc31d6bde89c328198/USER', 98676)
mfv_stoplb_tau010000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-dfac387659d218aa5ddf0226ebf421d0/USER', 49832)
mfv_stoplb_tau001000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-06734a6ef95abc1a3c96d5c7025f449e/USER', 98582)
mfv_stoplb_tau030000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e6719052872f26d092c4344110126f36/USER', 100391)
mfv_stoplb_tau000100um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-07c13092e5b1d92e89393a918261affb/USER', 100112)
mfv_stoplb_tau000300um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-d2a7958d473f6ad72079371066df4dfd/USER', 99840)
mfv_stoplb_tau010000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e666b28046605e98cb5e048bcbb21b5c/USER', 49856)
mfv_stoplb_tau001000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-0eeff46a423bd2b8a688674175bb418c/USER', 99508)
mfv_stoplb_tau030000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-1182520828559a89a6f7f55395465f55/USER', 99537)
mfv_stoplb_tau000100um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-3538d35ed400c97e1760e0ee96b95dcc/USER', 99744)
mfv_stoplb_tau000300um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f20951e1993552df5ca1527ed0d27078/USER', 99902)
mfv_stoplb_tau010000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-329075683560329a9d3461326c745da8/USER', 49227)
mfv_stoplb_tau001000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-84a7b116d6781efb99eee002942f7ab2/USER', 50163)
mfv_stoplb_tau030000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-a976644b02913f900bbac7939720ee2d/USER', 50181)
mfv_stoplb_tau000100um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-3e03bc8cb00f2895f5c3267e3a765ae1/USER', 98144)
mfv_stoplb_tau000300um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-bb8f2380c15bde9f5d9452a3e783e3fa/USER', 101235)
mfv_stoplb_tau010000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ae0e569dced8b45e9d34572168b969e3/USER', 50608)
mfv_stoplb_tau001000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-a81dcbefe73cb049f29003899b9996da/USER', 49712)
mfv_stoplb_tau030000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f359ccbfc04fd271a4d5f5208d29be99/USER', 49799)
mfv_stoplb_tau000100um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-43277928745f14bec22875f83eb29fce/USER', 99793)
mfv_stoplb_tau000300um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-1b9c85af06a0e7e480645d958cc3a1d2/USER', 99406)
mfv_stoplb_tau010000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e6f0112f9d81c4ce74c4d7066740a2a5/USER', 99401)
mfv_stoplb_tau001000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-026ce7ff1416fd86bea01811add4228d/USER', 97820)
mfv_stoplb_tau030000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-a9a4e243843dc4f8fe86314126ed8ee7/USER', 101202)
mfv_stoplb_tau000100um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-cac8636e6458b98e8e3cd4689cd84b4d/USER', 99857)
mfv_stoplb_tau000300um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-c388537479df4e3fd9f0bee09cf9b720/USER', 99010)
mfv_stoplb_tau010000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-d749b2e01cd09a0bc4f282bd9e435e3d/USER', 101044)
mfv_stoplb_tau001000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-36817c367bcc62063ea113f8a6666fa7/USER', 99219)
mfv_stoplb_tau030000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-899c5e14c122819819b54daaea0d96d0/USER', 99207)
mfv_stoplb_tau000100um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-93d73de21efebb223fba25bc53b555a0/USER', 98268)
mfv_stoplb_tau000300um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-206715a6d708db76cdb089b61e0f5f67/USER', 100008)
mfv_stoplb_tau010000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-29a0b251435f8221725440f5a451ed84/USER', 101168)
mfv_stoplb_tau001000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-a1eaa49868b461961e967a1b048dab3e/USER', 99255)
mfv_stoplb_tau030000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-2b5ba6ef9494711296d61bcfe6913b1a/USER', 99198)
mfv_stoplb_tau000100um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-a7d24a2b209eb388e919aa023adab874/USER', 100291)
mfv_stoplb_tau000300um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-348c99777a65dd4c7e6b99586600a35d/USER', 86231)
mfv_stoplb_tau010000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-287c46e50667a04fe6ba95886d7a458a/USER', 100170)
mfv_stoplb_tau001000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-aa74f213d2daf21cd5a8fa4ae02bf678/USER', 99575)
mfv_stoplb_tau030000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-1c61fd00d98bf1899d0619cab6af72de/USER', 100308)
mfv_stoplb_tau000100um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-43ee6ceaf9e8ebe98c89702020aa1fd8/USER', 100987)
mfv_stoplb_tau000300um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-758fdbe9b4056c5bb297c43bc9ef361f/USER', 100012)
mfv_stoplb_tau010000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-67dcff476e802063eb5b23a9f5f4f7d2/USER', 50027)
mfv_stoplb_tau001000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e5771f7fc9a28552ef5129effbb996dd/USER', 99440)
mfv_stoplb_tau030000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e3789bbc052537f2bedc7b75ca7b59ee/USER', 98586)
mfv_stopld_tau000100um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ad92819dfd89ba6d185c7db492c6b2e5/USER', 99376)
mfv_stopld_tau000300um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-965c9e29aeb5a491d85dbbac2c874098/USER', 100018)
mfv_stopld_tau010000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-3b7a161ad976a1b08c6a8233c966ad88/USER', 49142)
mfv_stopld_tau001000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-65a9ccade5d1c3cf05333e1b2dae8d1f/USER', 100845)
mfv_stopld_tau030000um_M1000_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-455f44e3370b156b70a89b405537c41c/USER', 99794)
mfv_stopld_tau000100um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-4c551cebf57f8f04f43e4f2382595121/USER', 99574)
mfv_stopld_tau000300um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-cfc8b3f9f185088dc9ab0d85c16a5d5e/USER', 99868)
mfv_stopld_tau010000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-201b674e61a7dd8793fc0a5daea564da/USER', 49886)
mfv_stopld_tau001000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-9012e6644b6cf575896eddc60252d9ff/USER', 99291)
mfv_stopld_tau030000um_M1200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ff2060a6bd2b7949a2851c9fe70ac7cb/USER', 99929)
mfv_stopld_tau000100um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-559c6cb924e9ffb57f1dac563f630b1f/USER', 99545)
mfv_stopld_tau000300um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-626d58c2e6dbba8991226a3f6791c042/USER', 99932)
mfv_stopld_tau010000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-518f1d94512d863fa7fa64ca7ef8e23b/USER', 49788)
mfv_stopld_tau001000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-757c4e936ada31b297d33e227b1273f7/USER', 98682)
mfv_stopld_tau030000um_M1400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-882d13c6a9dff6b2687c5db81b8c86ad/USER', 101616)
mfv_stopld_tau000100um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-4d0768a8cc79ccc17959629f5f429c06/USER', 100675)
mfv_stopld_tau000300um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-3744f72c5e73d9a6b070f056a3e043da/USER', 100486)
mfv_stopld_tau010000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-5b54ae6d855f1001090b94eab94015da/USER', 49732)
mfv_stopld_tau001000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-921e71ba8f17fd18e43990e4402cc4b5/USER', 50045)
mfv_stopld_tau030000um_M1600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-8db279aa252766c1965d97d32837190c/USER', 49682)
mfv_stopld_tau000100um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-ca6bbdc0786ec223ca7408a015164124/USER', 99094)
mfv_stopld_tau000300um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f860d857f36a0f7fb4f3051131f9cf76/USER', 99749)
mfv_stopld_tau010000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-d91782cf3eb78829a13cf22a937dff15/USER', 49663)
mfv_stopld_tau001000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-fac8bc28f97f68394957908e3ab63aa1/USER', 49813)
mfv_stopld_tau030000um_M1800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-9026a809415b475c3aa351bb46d752c2/USER', 50468)
mfv_stopld_tau000100um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-6626531a859ab1f5ad8cba9781fbacd5/USER', 100260)
mfv_stopld_tau000300um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-fdf3f82cc9acb4e6592b01bf37d440cd/USER', 99340)
mfv_stopld_tau010000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-b3c31984d5d3d32c7721221dc611c5c6/USER', 99542)
mfv_stopld_tau001000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-52e1385526e2ebf0def1acbd9acd6ac1/USER', 97872)
mfv_stopld_tau030000um_M0200_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-5a356a3ffbff56b918488755f6718986/USER', 100076)
mfv_stopld_tau000100um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e07a05ccd4b504c6939a260e80a547fe/USER', 100170)
mfv_stopld_tau000300um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-bae36f866bb8e4851cb52c044eea9ec0/USER', 100594)
mfv_stopld_tau010000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e1666e407b9f792acc2fffd74ec906b4/USER', 99759)
mfv_stopld_tau001000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-7449700ee216b586fc48cf0fecdfac1e/USER', 99504)
mfv_stopld_tau030000um_M0300_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-82e0f75cc6f6ccb2d2dc191030ab9eb9/USER', 99243)
mfv_stopld_tau000100um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-62836fdb4ffec72b4ba189437e221266/USER', 100052)
mfv_stopld_tau000300um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-31b2f06a85430da0aeacf25707616178/USER', 99431)
mfv_stopld_tau010000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f44fe48decedb5ed98288bcb6e486db2/USER', 99314)
mfv_stopld_tau001000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-97d84b870ac405735d3aaeb6698ee84a/USER', 100447)
mfv_stopld_tau030000um_M0400_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-e758a18230383b1f85c8cda1d6a87510/USER', 99547)
mfv_stopld_tau000100um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-22553848810e7075364d39b03d1c8aa6/USER', 100954)
mfv_stopld_tau000300um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-6b53c76528fbab6d4d7f1f074585831f/USER', 99589)
mfv_stopld_tau010000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-776791f608b1783e4fce4185d0767fd1/USER', 100599)
mfv_stopld_tau001000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f55feb8f51d64a87a4dab8232cc607ff/USER', 99859)
mfv_stopld_tau030000um_M0600_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-5dbf5e7340e19936ec73cdabb1088573/USER', 100128)
mfv_stopld_tau000100um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-00cc34bed099232be2e259a34d6d2cd1/USER', 99282)
mfv_stopld_tau000300um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-f52a2eb8bb2d7f4da0ad4bf0710c1a00/USER', 99263)
mfv_stopld_tau010000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-c7c0ab0ec7de5605a34c12e92358bf1d/USER', 49387)
mfv_stopld_tau001000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-8fa2ae6eb63cc0b9fccd415b672d0316/USER', 100038)
mfv_stopld_tau030000um_M0800_20162.add_dataset('ntupleulv13lepm_wgen', '/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/awarden-NtupleULV13Lepm_WGen_20162-65e30e7d45f2afde50e4dd9cc86d4752/USER', 100282)
SingleMuon20162F.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20162-84707917ebae82dd7ad926ec526aef35/USER', 2345189)
SingleMuon20162G.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20162-f20522d66154c437a0e118de7caaaf51/USER', 43810001)
SingleMuon20162H.add_dataset('ntupleulv13lepm_wgen', '/SingleMuon/awarden-NtupleULV13Lepm_WGen_20162-36fdf3ff749b2b5ae8cdd941bc50d623/USER', 52355266)
SingleElectron20162F.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20162-5022c07727402952cb42f4be56b498a5/USER', 1528087)
SingleElectron20162G.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20162-f3790e9947ff53019b5b0706c158b8fe/USER', 26972559)
SingleElectron20162H.add_dataset('ntupleulv13lepm_wgen', '/SingleElectron/awarden-NtupleULV13Lepm_WGen_20162-5426ecdf1047f40c7bd64b950685eddb/USER', 30128366)
SinglePhoton20162F.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20162-efc324224458a342e950723a6b16ad96/USER', 54609)
SinglePhoton20162G.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20162-a53a1904041229eda79da33ac1a2cfd4/USER', 931022)
SinglePhoton20162H.add_dataset('ntupleulv13lepm_wgen', '/SinglePhoton/awarden-NtupleULV13Lepm_WGen_20162-cbe053aada457c2b50c27f98b27e3a4c/USER', 986409)

### testing if data-mc discrepancy in assoc lepton pT is due to not dropping lepton tracks at deltaz stage; impatient and moving on without full EGamma2018D
SingleMuon2018A.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/SingleMuon/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-12e2744868d665382268f915f4f709df/USER', 20409606)
SingleMuon2018B.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/SingleMuon/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-7173e8913e804cfa888cef3bc22abb7c/USER', 10245563)
SingleMuon2018C.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/SingleMuon/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-4d7a6c36e8d50dc04a8f05d49e203d40/USER', 9375737)
SingleMuon2018D.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/SingleMuon/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-7fa03ec5aacd52188a31948a1d643934/USER', 44952696)
EGamma2018A.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/EGamma/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-078ad0ed6be05e81360b531843126879/USER', 9744036)
EGamma2018B.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/EGamma/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-7650b8cd94a0bfdab7925d4159646acb/USER', 4821789)
EGamma2018C.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/EGamma/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-1394d68290d91383e5fc92c005b6e66a/USER', 4486232)
EGamma2018D.add_dataset('ntupleulv12_ogdeltazlepm_wgen', '/EGamma/awarden-NtupleULV12_ogdeltazLepm_WGen_2018-d9a44855f94b84f1d0ed6b212499fe84/USER', 21683783)



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
#wjetstolnu_2017.add_dataset('trackingtreerulv2_lepm', '/FakeDataset/fakefile-FakePublish-b7c9637ef3610c24dea4766ba4184da4/USER', -1)
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


##now for track mover : 
#fixed the flight axis (to be jet + lepton) and not just lepton

#limited ttbar 
# ttbar_lep_2018.add_dataset('trackmoverulv13lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-33a5f6e8fe19e1fb5e04b7c7f30d3cdc/USER', -1)
# ttbar_semilep_2018.add_dataset('trackmoverulv13lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-a969080899ac145f4d989a62523ec24b/USER', -1)
# ttbar_had_2018.add_dataset('trackmoverulv13lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-bce04236a2e57c1c59216eed5b5fd7dc/USER', -1)

# mfv_stoplb_tau001000um_M0200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-4eaa688e3af9fe9e22c979c10fe10be7/USER', 141007)
# mfv_stoplb_tau010000um_M0200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-3ec90b54ec738e828f1d45204d6bad79/USER', 114719)
# mfv_stoplb_tau010000um_M0300_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-16775497dc0caddaa0aab989433df06d/USER', 130176)
# mfv_stoplb_tau010000um_M0400_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-c7e2f8f98c91e39cfbae4fa2d3b0ca2c/USER', 143787)
# mfv_stoplb_tau010000um_M0600_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-a0415d26207e1a50664bdeed8a3c25fe/USER', 153473)
# mfv_stoplb_tau010000um_M0800_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-13656207a0c6d350b58284c5be5f8d04/USER', 79366)
# mfv_stoplb_tau000300um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-ea16a6ebd49c4c894ce9338d0f49b2bf/USER', 170885)
# mfv_stoplb_tau001000um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-e6752dc5c4cbaba4dc5eb97b8ae0b55e/USER', 169644)
# mfv_stoplb_tau010000um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-8b1cf93fde455ab2a4f4ad44a1ab0354/USER', 80058)
# mfv_stoplb_tau010000um_M1200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-5027a3250cacddf862788a96e0f7d3ef/USER', 79689)
# mfv_stoplb_tau010000um_M1400_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-7041369aace9ab0a709222965d8338ee/USER', 81448)
# mfv_stoplb_tau010000um_M1600_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-77289f16e6deb317b08b0bdbcc0db409/USER', 83224)
# mfv_stoplb_tau010000um_M1800_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-b3c559c0eb2f1534dcf9aeaa4b27f5f9/USER', 82589)
# mfv_stopld_tau000300um_M0200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-48f1e306122993a9074e66ad746f7e98/USER', 149916)
# mfv_stopld_tau001000um_M0200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-4820cb7d4431f3a640828edda28803aa/USER', 141884)
# mfv_stopld_tau010000um_M0200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-f36884ecbd31bba1ebc2667caff2a1ea/USER', 115408)
# mfv_stopld_tau010000um_M0300_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-337991a54d08380124fbeecf7f29d33f/USER', 129901)
# mfv_stopld_tau010000um_M0400_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-7cda1645d2ec1171f3c536e396837117/USER', 141334)
# mfv_stopld_tau010000um_M0600_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-91ebb706ed9b688ff8241f1ffde3db65/USER', 153749)
# mfv_stopld_tau010000um_M0800_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-48a5b265cd8a019ebb7f5474c8bfc9d0/USER', 78952)
# mfv_stopld_tau000300um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-f47020af583a1c0cfb022e166f5fa06b/USER', 172358)
# mfv_stopld_tau001000um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-22cc81ae848b1800680a3451391c73ec/USER', 168399)
# mfv_stopld_tau010000um_M1000_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-9474526dc2eb38c73b8e702c3b6b19d9/USER', 78740)
# mfv_stopld_tau010000um_M1200_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-718107539f721506ea9c3a295a883ab6/USER', 79277)
# mfv_stopld_tau010000um_M1400_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-5ec41d50f67430257214726732e767b7/USER', 80858)
# mfv_stopld_tau010000um_M1600_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-62f7b4ae24181c618feaba2c0cdb93f6/USER', 80659)
# mfv_stopld_tau010000um_M1800_2018.add_dataset('trackmovermctruthulv13lepmv6', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV13Lepmv6_2018-cbfa94a5efefe8c939f8f337e9200634/USER', 80334)

ttbar_lep_2018.add_dataset('trackmoverulv14lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-b646e578395019f18d8af0dab85c73c8/USER', -1)
ttbar_semilep_2018.add_dataset('trackmoverulv14lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-0ec094596e7bea532473d218c03fc4da/USER', -1)
ttbar_had_2018.add_dataset('trackmoverulv14lepm1jet1lep', '/FakeDataset/fakefile-FakePublish-658b1ede7671ef61587674cfedd959ce/USER', -1)

# mfv_stoplb_tau001000um_M0200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-ba1c176a474b5fcf5c31dc198c3b1198/USER', 129889)
# mfv_stoplb_tau010000um_M0200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-768fb60d59b94c9b5cf521e0b5a09f9e/USER', 105724)
# mfv_stoplb_tau010000um_M0300_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-66969833fb08f3e6794560390f8251c1/USER', 118149)
# mfv_stoplb_tau010000um_M0400_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-8897e09f3a373223c7f8ed3a3029aa0a/USER', 130145)
# mfv_stoplb_tau010000um_M0600_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-ccf4ebadb9864eb7710d3dc5c74e5d8f/USER', 141116)
# mfv_stoplb_tau010000um_M0800_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-8071bed8dfaac412b53eda486a6b203a/USER', 73622)
# mfv_stoplb_tau010000um_M1000_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-eb6a2ad5ba13c53b55996f065abf71c4/USER', 74839)
# mfv_stoplb_tau010000um_M1200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-3a7885d10e5e41c55bc3a74fc248d470/USER', 74565)
# mfv_stoplb_tau010000um_M1400_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-6d59c6e6961cc6b3a52358fe457f356e/USER', 76393)
# mfv_stoplb_tau010000um_M1600_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-b980f97bf716e06526298a77264c37a0/USER', 78190)
# mfv_stoplb_tau010000um_M1800_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-61aeb611e3bb1388f9a6d806a08a5c07/USER', 77564)
mfv_stopld_tau001000um_M0200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-33fa491dbd607817fdcf92d972c3a96f/USER', 130489)
mfv_stopld_tau010000um_M0200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-d162fe0e2af9e5a42a7c02da89489f9e/USER', 106359)
# mfv_stopld_tau010000um_M0300_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-0b751d5ed306fab4be5717b776504c9f/USER', 118051)
# mfv_stopld_tau010000um_M0400_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-e2f910d2815610c76b3125448bbdd8eb/USER', 128270)
# mfv_stopld_tau010000um_M0600_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-fc62d12ab6cbe0b97a05472d1125392b/USER', 141238)
mfv_stopld_tau010000um_M0800_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-23c5bd64733e3a0533fa4d301dd4fcd8/USER', 73160)
mfv_stopld_tau010000um_M1000_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-7d7ed6ced437671757f7eb30886708e8/USER', 73185)
# mfv_stopld_tau010000um_M1200_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-9876cddb639c8cafa82231f3568dde09/USER', 74008)
# mfv_stopld_tau010000um_M1400_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-5bb56650719f64be8a15abb647966324/USER', 75643)
# mfv_stopld_tau010000um_M1600_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-d507f04e4f8efc92dbb8a1309df65c22/USER', 75455)
# mfv_stopld_tau010000um_M1800_2018.add_dataset('trackmovermctruthulv14lepmv6', '/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/awarden-TrackMoverMCTruthULV14Lepmv6_2018-b03010d6f77106feacc72c5af47b8107/USER', 75207)

########
# automatic condor declarations for ntuples
########

for s in registry.all():
    for ds in s.datasets.keys():
        for ds4 in 'ntuple', 'nr_':
            if ds.startswith(ds4):
                s.datasets[ds].condor = True
                #s.datasets[ds].xrootd_url = xrootd_sites['T3_US_FNALLPC']
                s.datasets[ds].xrootd_url = xrootd_sites['T2_US_Wisconsin']
                

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
        #"miniaod": Lepton_data_samples_20161 + mfv_stopdbardbar_samples_2017  #+ diboson_samples_2017 + leptonic_samples_2017 + qcd_lep_samples_2017 + met_samples_2017 # SingleElectron2017B, SingleElectron2017D, SingleElectron2017E, 
        
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
        #for year in 2017, 2018:
        #    for line in file(str(year)):
        #WIP
        for s in all_signal_samples_2018:
             l = DBS.datasets('/Z*MS-15_ctauS-3*/*UL18*/MINIAODSIM') # % s.primary_dataset)
             year = 2018
             #print(l)
             for line in l:
                if line.startswith('/GluinoGluinoToNeutralinoNeutralinoTo2T2B2S'):
                    model = 'mfv_neu'
                elif line.startswith('/StopStopbarTo2Dbar2D'):
                    model = 'mfv_stopdbardbar'
                elif line.startswith('/WplusH_HToSSTodddd_WToLNu'):
                    model = 'WplusHToSSTodddd'
                elif line.startswith('/WminusH_HToSSTodddd_WToLNu'):
                    model = 'WminusHToSSTodddd'
                elif line.startswith('/ZH_HToSSTodddd_ZToLL'):
                    model = 'ZHToSSTodddd'
                else:
                    print 'unrecognized line %r' % line
                    continue
                dataset = line.strip()
                if '0p' in line :
                    mass, tau_s = re.search(r'MS-(\d+)_ctauS-0p(.*)Tune', line).groups()
                    mass, tau, tau_unit = int(mass), int(tau_s[:-1]), tau_s[-1]
                    if mass in [15,40,55] and tau in [1,3]:
                        nevents = DBS.numevents_in_dataset(dataset)
                        print "    MCSample('%s_tau%i00um_M%i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)
                    else:
                        print '    no MCSample'
                        continue
                else:
                    mass, tau_s = re.search(r'MS-(\d+)_ctauS-(.*)Tune', line).groups()
                    mass, tau, tau_unit = int(mass), int(tau_s[:-1]), tau_s[-1]
                    if mass in [15,40,55] and tau in [1,3,30]:
                        nevents = DBS.numevents_in_dataset(dataset)
                        print "    MCSample('%s_tau%imm_M%i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)
                    else:
                        print '    no MCSample'
                        continue
                #mass, tau, tau_unit = int(mass), int(tau_s[:-2]), tau_s[-2:]
                #if tau_unit == 'mm':
                #    tau *= 1000 
                #else:
                #    assert tau_unit == 'um'
                #print(mass, tau) 
                #if mass in [400,600,800,1200,1600,3000] and tau in [100,300,1000,10000,30000]:
                #    nevents = DBS.numevents_in_dataset(dataset)
                #    print "    MCSample('%s_tau%06ium_M%04i_%s', '%s', %i)," % (model, tau, mass, year, dataset, nevents)

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
