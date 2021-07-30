import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

settings = CMSSWSettings()
settings.is_mc = True
settings.is_miniaod = True
settings.cross = '' # 2017to2018' # 2017to2017p8'


#hnl_trilept_e_V001414_M0012p6_2018 failed
#hnl_trilept_e_V001414_M0012p8_2018 gave weird error (2nd time around)

#hnl_trilept_e_V000370_M0006_2018 file was not found in file catalog
#hnl_trilept_mu_V000316_M0011_2018 failed
#hnl_trilept_mu_V000836_M0012_2018 .... a little unsure if it was successful

#hnl_semilept_e_V000008_M0020_2018 failed
#hnl_semilept_e_V000047_M0015_2018 failed
#hnl_semilept_e_V002177_M0002_2018 failed
#hnl_semilept_e_V000650_M0005_2018 failed
#hnl_semilept_e_V000294_M0008_2018 failed
#hnl_semilept_e_V002572_M0008_2018 failed

#hnl_semilept_mu_V000021_M0015_2018 failed
#hnl_semilept_mu_V094973_M0001_2018 failed
#hnl_semilept_mu_V000008_M0020_2018 failed
#hnl_semilept_mu_V000650_M0005_2018 failed
#hnl_semilept_mu_V000294_M0008_2018 failed
#hnl_semilept_mu_V002572_M0008_2018 failed



sample_files(process, 'mfv_neu_tau030000um_M3000_2018', 'miniaod')
geometry_etc(process, settings)
tfileservice(process, 'mfv_neu_tau030000um_M3000_2018.root')
cmssw_from_argv(process)

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
sef = lambda *a,**kwa: setup_event_filter(process, *a, input_is_miniaod=True, **kwa)
sef('pTrigger', mode = 'trigger jets only')
sef('pTriggerBjets', mode = 'trigger bjets only',name_ex = 'bjets')
sef('pTriggerDispDijet', mode = 'trigger displaced dijet only',name_ex = 'displaced_dijet')
sef('pTriggerOR', mode = 'trigger HT OR bjets OR displaced dijet', name_ex = 'HT_OR_bjets_OR_displaced_dijet')
#sef('pJets',    mode = 'jets only novtx',   name_ex = 'NoVtx') # be sure to generate a different name for each subsequent use
#sef('pNoJESUp', mode = 'jets only novtx',   name_ex = 'NoJESUp', event_filter_jes_mult = 0)
#sef('pFull',    mode = 'jets only',         name_ex = 'Full') # uncomment to get efficiency of ntuple-level vertex filter
sef('pTriggerLeptons', mode = 'trigger leptons only', name_ex = 'leptons')
sef('pTriggerDispLeptons', mode = 'trigger displaced leptons', name_ex = 'displaced_leptons')
#sef('pTriggerCross', mode = 'trigger cross', name_ex = 'cross')
#sef('pTriggerCrossOnly', mode = 'trigger cross only', name_ex = 'cross_only')

#all the wonderful new additions...
#sef('pTriggerLepton2', mode = 'lepton slim 2', name_ex = 'lepton2')
#sef('pTriggerLepton3', mode = 'lepton slim 3', name_ex = 'lepton3')

sef('pTriggerDiLeptons', mode = 'trigger dileptons', name_ex = 'dileptons')
#sef('pTriggerDiLepton2', mode = 'dileptons slim 2', name_ex = 'dilepton2')
#sef('pTriggerDiLepton3', mode = 'dileptons slim 3', name_ex = 'dilepton3')

#sef('pTriggerDiLeptonsDZ', mode = 'trigger dileptons wDZ', name_ex = 'dileptons_wDZ')

sef('pTriggerDispLeptonsORLeptons', mode = 'DispLeptons OR Single Leptons', name_ex = 'displeptons_OR_lepton')
#sef('pTriggerDispLeptonsORLepton2', mode = 'DispLeptons OR Single Lepton2', name_ex = 'displeptons_OR_lepton2')
#sef('pTriggerDispLeptonsORLepton3', mode = 'DispLeptons OR Single Lepton3', name_ex = 'displeptons_OR_lepton3')

sef('pTriggerDispLeptonsORDiLeptons', mode = 'DispLeptons OR DiLeptons', name_ex = 'displeptons_OR_dileptons')
#sef('pTriggerDispLeptonsORDiLeptonsDZ', mode = 'DispLeptons OR DiLeptons wDZ', name_ex = 'displeptons_OR_dileptonswDZ')
sef('pTriggerLeptonsORDiLeptons', mode = 'SingleLeptons OR DiLeptons', name_ex = 'lepton_OR_dileptons')
#sef('pTriggerLepton2ORDiLeptons', mode = 'SingleLepton2 OR DiLeptons', name_ex = 'lepton2_OR_dileptons')
#sef('pTriggerLepton3ORDiLeptons', mode = 'SingleLepton3 OR DiLeptons', name_ex = 'lepton3_OR_dileptons')

#sef('pTriggerLeptonsORDiLepton2', mode = 'SingleLeptons OR DiLepton2', name_ex = 'lepton_OR_dilepton2')
#sef('pTriggerLeptonsORDiLepton3', mode = 'SingleLeptons OR DiLepton3', name_ex = 'lepton_OR_dilepton3')

#sef('pTriggerLepton2ORDiLepton2', mode = 'SingleLepton2 OR DiLepton2', name_ex = 'lepton2_OR_dilepton2')
#sef('pTriggerLepton2ORDiLepton3', mode = 'SingleLepton2 OR DiLepton3', name_ex = 'lepton2_OR_dilepton3')
#sef('pTriggerLepton3ORDiLepton2', mode = 'SingleLepton3 OR DiLepton2', name_ex = 'lepton3_OR_dilepton2')
#sef('pTriggerLepton3ORDiLepton3', mode = 'SingleLepton3 OR DiLepton3', name_ex = 'lepton3_OR_dilepton3')

sef('pTriggerDispLeptonsORHT', mode = 'DispLeptons OR HT', name_ex = 'displeptons_OR_HT')
sef('pTriggerLeptonsORHT', mode = 'Leptons OR HT', name_ex = 'leptons_OR_HT')
#sef('pTriggerLepton2ORHT', mode = 'Lepton2 OR HT', name_ex = 'lepton2_OR_HT')
#sef('pTriggerLepton3ORHT', mode = 'Lepton3 OR HT', name_ex = 'lepton3_OR_HT')


#sef('pTriggerLeptonsORDiLeptonsDZ', mode = 'SingleLeptons OR DiLeptons wDZ', name_ex = 'lepton_OR_dileptonswDZ')


#all the singles; first lepton
sef('pTriggerEle32', mode = 'Ele32', name_ex = 'ele32')
sef('pTriggerEle35', mode = 'Ele35', name_ex = 'ele35')
sef('pTriggerEle115', mode = 'Ele115', name_ex = 'ele115')
sef('pTriggerEle50', mode = 'Ele50', name_ex = 'ele50')
sef('pTriggerIsoMu24', mode = 'IsoMu24', name_ex = 'isomu24')
sef('pTriggerIsoMu27', mode = 'IsoMu27', name_ex = 'isomu27')
sef('pTriggerMu50', mode = 'Mu50', name_ex = 'mu50')

#displaced lepton
# sef('pTriggerMu43Photon43', mode = 'Mu43Photon43', name_ex = 'mu43photon43')
# sef('pTriggerDiPhoton30_22', mode = 'DiPhoton30_22', name_ex = 'diphoton30_22')
# sef('pTriggerDoublePhoton70', mode = 'DoublePhoton70', name_ex = 'doublephoton70')
# sef('pTriggerDoubleMu43', mode = 'DoubleMu43', name_ex = 'doublemu43')

# #dilepton
# sef('pTriggerEle23_12', mode = 'Ele23_12', name_ex = 'ele23_12')
# sef('pTriggerDoubleEle25', mode = 'DoubleEle25', name_ex = 'doubleele25')
# sef('pTriggerDoubleEle27', mode = 'DoubleEle27', name_ex = 'doubleele27')
# sef('pTriggerDoubleEle33', mode = 'DoubleEle33', name_ex = 'doubleele33')
# sef('pTriggerDoubleEle8', mode = 'DoubleEle8', name_ex = 'doubleele8')
# sef('pTriggerMu37_TkMu27', mode = 'Mu37_TkMu27', name_ex = 'mu37_tkmu27')
# sef('pTriggerDoubleL2Mu50', mode = 'DoubleL2Mu50', name_ex = 'doubleL2mu50')
# sef('pTriggerMu27_Ele37', mode = 'Mu27_Ele37', name_ex = 'mu27_ele37')
# sef('pTriggerMu8_Ele23', mode = 'Mu8_Ele23', name_ex = 'mu8_ele23')
# sef('pTriggerMu37_Ele27', mode = 'Mu37_Ele27', name_ex = 'mu37_ele27')
# sef('pTriggerMu23_Ele12', mode = 'Mu23_Ele12', name_ex = 'mu23_ele12')
# sef('pTriggerMu17_Photon30', mode = 'Mu17_Photon30', name_ex = 'mu17_photon30')

# #dilepton w DZ
# sef('pTriggerDZ_Ele23_12', mode = 'DZ_Ele23_12', name_ex = 'dz_ele23_12')
# sef('pTriggerDZ_DoubleEle8_PFHT350', mode = 'DZ_DoubleEle8_PFHT350', name_ex = 'dz_doubleele8_pfht350')
# sef('pTriggerDZ_Mu17_8', mode = 'DZ_Mu17_8', name_ex = 'dz_mu17_8')
# sef('pTriggerDZ_Mu19_9', mode = 'DZ_Mu19_9', name_ex = 'dz_mu19_9')
# sef('pTriggerDZ_Mu17_8', mode = 'DZ_Mu17_8', name_ex = 'dz_mu17_8')
# sef('pTriggerDZ_Mu12_Ele23', mode = 'DZ_Mu12_Ele23', name_ex = 'dz_mu12_ele23')
# sef('pTriggerDZ_Mu8_Ele8', mode = 'DZ_Mu8_Ele8', name_ex = 'dz_mu8_ele8')
# sef('pTriggerDZ_Mu8_Ele23', mode = 'DZ_Mu8_Ele23', name_ex = 'dz_mu8_ele23')




if len(process.mfvTriggerFilter.HLTPaths) > 1:
    for x in process.mfvTriggerFilter.HLTPaths:
        filt_name = ''.join(x.split('_')[1:-1])
        sef('p%s' % filt_name, name_ex=x)
        print x
        getattr(process, filt_name).HLTPaths = [x]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.mfv_stoplb_samples_2017 + Samples.mfv_stopld_samples_2017
        #have not yet added 2017 samples 
    elif year == 2018:
       ## samples = Samples.qcd_samples_2018 + Samples.data_samples_2018
        samples = Samples.mfv_stoplb_samples_2018 + Samples.mfv_stopld_samples_2018
        
    ms = MetaSubmitter('TrigFiltCheckV1', dataset='miniaod')
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), per_sample_pileup_weights_modifier(cross=settings.cross))
    ms.submit(samples)
