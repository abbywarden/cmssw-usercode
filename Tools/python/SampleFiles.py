import os, base64, zlib, cPickle as pickle
from collections import defaultdict
from fnmatch import fnmatch
from itertools import chain
from pprint import pprint
from JMTucker.Tools.CRAB3ToolsBase import decrabify_list
from JMTucker.Tools.CMSSWTools import cmssw_base

_d = {}
_added_from_enc = {}

def _enc(d):
    return base64.b64encode(zlib.compress(pickle.dumps(d)))

def _denc(encd):
    return pickle.loads(zlib.decompress(base64.b64decode(encd)))

def _add(d, allow_overwrite=False, _enced_call=[0]):
    global _d
    enced = type(d) == str
    if enced:
        d = _denc(d)
        _enced_call[0] += 1
    if not allow_overwrite:
        for k in d:
            if _d.has_key(k):
                raise ValueError('already have key %s' % repr(k))
            if len(d[k][1]) != d[k][0]:
                raise ValueError('length check problem: %s %s supposed to be %i but is %i' % (k[0], k[1], d[k][0], len(d[k][1])))
    _d.update(d)
    if enced:
        for k in d.keys():
            _added_from_enc[k] = _enced_call[0]

def _remove_file(sample, ds, fn):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    _d[(sample,ds)] = (n-1, fns)

def _replace_file(sample, ds, fn, fn2):
    n, fns = _d[(sample,ds)]
    fns.remove(fn)
    fns.append(fn2)
    _d[(sample,ds)] = (n, fns)

def _add_ds(ds, d, allow_overwrite=False):
    d2 = {}
    for k in d:
        d2[(k,ds)] = d[k]
    _add(d2, allow_overwrite)

def _add_single_files(ds, path, l, allow_overwrite=False):
    d = {}
    for sample in l:
        d[(sample,ds)] = (1, [os.path.join(path, sample + '.root')])
    _add(d, allow_overwrite)

def _fromnumlist(path, numlist, but=[], fnbase='ntuple', add=[], numbereddirs=True):
    return add + [path + ('/%04i' % (i/1000) if numbereddirs else '') + '/%s_%i.root' % (fnbase, i) for i in numlist if i not in but]

def _fromnum1(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # crab starts job numbering at 1
    l = _fromnumlist(path, xrange(1,n+1), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _fromnum0(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # condorsubmitter starts at 0
    l = _fromnumlist(path, xrange(n), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _fromnum2(path, n, but=[], fnbase='ntuple', add=[], numbereddirs=True): # messed up crab job 
    l = _fromnumlist(path, xrange(2,n+1), but, fnbase, add, numbereddirs)
    return (len(l), l)

def _frommerge(path, n):
    assert path.endswith('/merge') and path.count('/merge') == 1
    return (n, [path.replace('/merge', '/merge%s_0.root') % s for s in [''] + ['%03i' % x for x in xrange(1,n)]])

def _join(*l):
    ns, ls = zip(*l)
    return (sum(ns), sum(ls, []))

def keys():
    return _d.keys()

def dump():
    pprint(_d)

def allfiles():
    return (fn for (sample, ds), (n, fns) in _d.iteritems() for fn in fns)

def summary():
    d = defaultdict(list)
    for k in _d.iterkeys():
        a,b = k
        d[a].append((b, _d[k][0]))
    for a in sorted(d.keys()):
        for b,n in d[a]:
            print a.ljust(40), b.ljust(20), '%5i' % n

def has(name, ds):
    return _d.has_key((name, ds))

def get(name, ds):
    return _d.get((name, ds), None)

def get_fns(name, ds):
    return _d[(name,ds)][1]

def get_local_fns(name, ds, num=-1):
    fns = _d[(name, ds)][1]
    if num > 0:
        fns = fns[:num]
    #return [('root://cmseos.fnal.gov/' + fn) if (fn.startswith('/store/user') or fn.startswith('/store/group')) else fn for fn in fns]
    return [('root://cmsxrootd.hep.wisc.edu/' + fn) if fn.startswith('/store/user') else fn for fn in fns] #TODO : CLEANUP wisc usage

def set_process(process, name, ds, num=-1):
    process.source.fileNames = get_local_fns(name, ds, num)

def who(name, ds):
    nfns, fns = _d[(name,ds)]
    users = set()
    for fn in fns:
        assert fn.startswith('/store')
        if fn.startswith('/store/user'):
            users.add(fn.split('/')[3])
    return tuple(sorted(users))

__all__ = [
    'dump',
    'get',
    'summary',
    ]

################################################################################

#execfile(cmssw_base('src/JMTucker/Tools/python/enc_SampleFiles.py'))

_removed = [
    ]

for name, ds, fns in _removed:
    for fn in fns:
        _remove_file(name, ds, fn)

################################################################################

##For local testing
_add_ds("miniaod", {
    'qcdmupt15_2017': (1, ['/store/mc/RunIISummer20UL17MiniAOD/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/100000/034AE4F2-7180-7F40-81D6-740D15738CBA.root'])
})

 
_add_ds("miniaod", {
    'qcdbctoept030_2017': (4, ['/store/mc/RunIISummer20UL17MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/FA5F6137-E1C6-1745-9D33-087EAC283CCE.root', '/store/mc/RunIISummer20UL17MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/FA2D3652-472A-2B4C-B099-DB3EC4E6B0A4.root', '/store/mc/RunIISummer20UL17MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/CFBCA5F9-AFE6-AE47-846C-29EA95421EA1.root', '/store/mc/RunIISummer20UL17MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/BF5B595E-285F-814C-BF78-E62F2F9A04E4.root'])
})

_add_ds("miniaod", {
    'qcdbctoept030_2018': (2, ['/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/0CFD3824-3C62-5945-8194-1C3732910388.root', '/store/mc/RunIISummer20UL18MiniAODv2/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/322E81BE-2BC9-F841-9F04-F4A1FE78EA2C.root'])
})

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0800_2018' : (2, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/21602664-E4E1-3E48-A244-2D131F063685.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/27A92C07-345E-1B48-98D9-F1C966151362.root'])
})

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0800_2017' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/181536B9-11E5-2344-9E8E-BACCD7482A0A.root'])
})

#have tried 36004, 4060...?

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0600_2017' : (1, ['/store/mc/RunIISummer20UL17MiniAODv2/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/30000/FD91D346-416F-844D-8D16-E7AD31FEAB93.root'])
})

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0800_20161' : (1, ['/store/mc/RunIISummer20UL16MiniAODAPVv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v2/2560000/40A1FE31-85A4-7A48-A51F-33B10923F4F4.root'])
})

_add_ds("miniaod", {
    'ttbar_semilep_2018' : (3, ['/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/016D5B69-2F13-A94D-8A61-91551911BFBD.root',
                                '/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/01292B43-5A7A-164B-92B7-292369F64D70.root',
                                '/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/0120869B-F7FD-C24C-A083-924B2F01BB88.root'
                                ])
})

_add_ds("miniaod", {
    'mfv_stoplb_tau000300um_M0800_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/30000/1140EC5A-A7C4-794C-9557-D64D8D5AFFC1.root'])
})

_add_ds("miniaod", {
    'mfv_stopld_tau000100um_M1400_20162' : (1, ['/store/mc/RunIISummer20UL16MiniAODv2/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/40000/1E7C7490-8DF9-6D45-97CB-1C7EA533B30C.root'])
})

_add_ds("miniaod", {
    'ttbar_semilep_2017' : (1, ['/store/mc/RunIISummer20UL17MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/00000/005708B7-331C-904E-88B9-189011E6C9DD.root'])
})

_add_ds("ntupleulv12lepm_wgen", {
#_add_ds("miniaod", {
    # 'test' : (1, ['file:/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/pickevents.root']) #one singular data event SingleMuon2018B
    'test' : (1, ['file:/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/ntuple.root']) #one singular data event SingleMuon2018B

 })

_add_ds("miniaod", {
    'SingleMuon2018D' : (1, ['/store/data/Run2018D/SingleMuon/MINIAOD/UL2018_MiniAODv2-v3/120000/000464E1-1144-1641-BE88-4600BD58923C.root'])
})

_add_ds("miniaod", {
    'EGamma2018A' : (1, ['/store/data/Run2018A/EGamma/MINIAOD/UL2018_MiniAODv2_GT36-v1/2820000/015BEACB-338C-894D-8EB5-B5AB2A7B8E81.root'])
})
##################################################################################


#trackmover 


#fixed flight axis to include the lepton momentum; ttbar is limited 
#need to redo
# _add_ds("trackmoverulv13lepm1bjet1lep", {

# })

# _add_ds("trackmoverulv13lepm1jet1lep", {
# 'ttbar_lep_2018': (4, ['/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV13Lepm1jet1lep_2018/250518_112006/0000/movedtree_%i.root' % i for i in chain(xrange(1,4), [7])]),
# 'ttbar_semilep_2018': (19, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV13Lepm1jet1lep_2018/250518_112153/0000/movedtree_%i.root' % i for i in chain(xrange(1,10), xrange(11,14), xrange(15,22))]),
# 'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV13Lepm1jet1lep_2018/250518_112338", 17, fnbase="movedtree"),
# })

#back to og dz (keep lep w/ pt >= 20) + pt ordering 
##track rescaling applied 2018
_add_ds("ntupleulv11lepm_wgen", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_085759", 34),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_085905", 13),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090010", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090117", 15),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090223", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090328", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090433", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_090537", 5),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_090644", 19),
'qcdbctoept020_2018': (40, ['/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_090748/0000/ntuple_%i.root' % i for i in chain(xrange(1,38), xrange(39,42))]),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_090853", 34),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_091000", 45),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_091107", 52),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV11Lepm_WGen_2018/240801_091212", 47),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_091317", 4),
'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV11Lepm_WGen_2018/240801_091422", 310),
'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV11Lepm_WGen_2018/240801_091527", 1007),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV11Lepm_WGen_2018/240801_091633", 723),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV11Lepm_WGen_2018/240801_111117", 99),
'wjetstolnu_ext_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV11Lepm_WGen_2018/240801_111225", 180),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV11Lepm_WGen_2018/240801_111330", 114),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV11Lepm_WGen_2018/240801_111434", 110),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_111539", 23),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_111645", 17),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV11Lepm_WGen_2018/240801_111750", 5),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_091737", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_091843", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_091950", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092055", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092203", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092311", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092419", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092526", 200),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092630", 201),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092735", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092841", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_092946", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093050", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093154", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093302", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093410", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093514", 200),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093622", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093727", 201),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093836", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_093943", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094048", 200),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094151", 201),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094303", 100),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094426", 201),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094530", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094636", 201),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094743", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094850", 101),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_094957", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095102", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095209", 201),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095314", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095418", 101),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095522", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095628", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095733", 201),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095837", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_095943", 101),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100048", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100159", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100303", 201),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100411", 101),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100515", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100620", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100723", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100827", 201),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_100932", 101),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101035", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101140", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101244", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101350", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101454", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101606", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101712", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101817", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_101921", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102026", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102131", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102236", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102342", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102446", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102552", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102659", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102805", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_102910", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103014", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103120", 200),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103224", 201),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103332", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103436", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103550", 201),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103656", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103802", 101),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_103908", 201),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104015", 201),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104120", 201),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104225", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104332", 101),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104439", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_104543", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105023", 201),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105133", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105239", 101),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105344", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105451", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105555", 200),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105700", 201),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105805", 101),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_105909", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110015", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110120", 201),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110232", 101),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110340", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110447", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110551", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110657", 201),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110803", 101),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_110906", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV11Lepm_WGen_2018/240801_111012", 101),
})

#fixed track_dxy to include correction of beam slope 
_add_ds("ntupleulv13lepm_wgen", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_203618", 43),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_203719", 28),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_203819", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_203919", 20),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_204020", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_204120", 13),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_204222", 17),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_204323", 7),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_204424", 6),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_204527", 19),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_204628", 65),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_204730", 46),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_204831", 63),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_204932", 63),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2018/250318_205032", 55),
'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2018/250318_205133", 310),
'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2018/250318_205232", 1005),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2018/250318_205333", 723),
'wjetstolnu_0j_2018': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2018/250318_224920", 206),
'wjetstolnu_1j_2018': (223, ['/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2018/250318_225020/0000/ntuple_%i.root' % i for i in chain(xrange(1,74), xrange(75,98), xrange(99,144), xrange(145,227))]),
'wjetstolnu_2j_2018': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2018/250318_225121", 201),
'dyjetstollM10_2018': (110, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_2018/250318_225222/0000/ntuple_%i.root' % i for i in chain(xrange(1,89), xrange(90,93), xrange(99,101), xrange(102,118), [96])]),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_2018/250318_225321", 110),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_225421", 23),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_225522", 17),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2018/250318_225625", 7),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205432", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205533", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205633", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205731", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205835", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_205935", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210036", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210137", 200),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210237", 201),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210338", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210439", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210542", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210642", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210748", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210848", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_210947", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211047", 200),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211148", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211248", 201),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211350", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211450", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211552", 200),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211651", 201),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211752", 100),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211853", 201),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_211954", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212054", 201),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212154", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212254", 101),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212354", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212454", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212553", 201),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212653", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212755", 101),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212856", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_212957", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213057", 201),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213158", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213300", 101),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213400", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213500", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213600", 201),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213701", 101),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213802", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_213902", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214004", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214104", 201),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214203", 101),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214302", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214403", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214506", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214607", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214707", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214806", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_214908", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215113", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215214", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215315", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215414", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215514", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215614", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215714", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_215812", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220331", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220430", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220529", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220631", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220731", 200),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220835", 201),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_220934", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221034", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221135", 201),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221236", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221336", 101),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221436", 201),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221536", 201),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221643", 201),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221743", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221846", 101),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_221949", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222050", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222153", 201),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222257", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222358", 101),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222458", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222600", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222701", 200),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222802", 201),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_222902", 101),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223003", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223103", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223201", 201),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223301", 101),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223400", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223500", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223604", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223705", 201),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223806", 101),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_223908", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2018/250318_224009", 101),
'SingleMuon2018A': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2018/250318_224109", 410),
'SingleMuon2018B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2018/250318_224211", 191),
'SingleMuon2018C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2018/250318_224311", 185),
'SingleMuon2018D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2018/250318_224413", 798),
'EGamma2018A': _fromnum1("/store/user/awarden/EGamma/NtupleULV13Lepm_WGen_2018/250318_224516", 713),
'EGamma2018B': _fromnum1("/store/user/awarden/EGamma/NtupleULV13Lepm_WGen_2018/250318_224617", 295),
'EGamma2018C': _fromnum1("/store/user/awarden/EGamma/NtupleULV13Lepm_WGen_2018/250318_224718", 310),
'EGamma2018D': _fromnum1("/store/user/awarden/EGamma/NtupleULV13Lepm_WGen_2018/250318_224818", 1438),

#2017
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054322", 50),
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054423", 15),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054526", 33),
'qcdempt030_2017': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054628", 9),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054733", 19),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054840", 25),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_054947", 35),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_055048", 7),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_055149", 6),
'qcdbctoept015_2017': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055252", 66),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055354", 59),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055456", 58),
'qcdbctoept080_2017': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055557", 47),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055700", 49),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_2017/250319_055803", 34),
'ttbar_lep_2017': (129, ['/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2017/250319_055904/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,16), xrange(17,57), xrange(58,79), xrange(80,92), xrange(93,110), xrange(111,113), xrange(114,137))]),
'ttbar_semilep_2017': (427, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2017/250319_060005/0000/ntuple_%i.root' % i for i in chain(xrange(1,208), xrange(209,294), xrange(297,316), xrange(319,323), xrange(324,332), xrange(333,361), xrange(362,380), xrange(381,437), [295, 317])]),
'ttbar_had_2017': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_2017/250319_060107", 310),
'wjetstolnu_0j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2017/250319_085246", 220),
'wjetstolnu_1j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2017/250319_085347", 242),
'wjetstolnu_2j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_2017/250319_085449", 119),
'dyjetstollM10_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_2017/250319_085551", 96),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_2017/250319_085652", 129),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_085753", 26),
'zz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_085855", 4),
'wz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_2017/250319_085959", 17),

'mfv_stoplb_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060209", 201),
'mfv_stoplb_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060312", 201),
'mfv_stoplb_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060414", 101),
'mfv_stoplb_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060516", 201),
'mfv_stoplb_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060619", 201),
'mfv_stoplb_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060721", 201),
'mfv_stoplb_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060823", 200),
'mfv_stoplb_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_060925", 101),
'mfv_stoplb_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061027", 201),
'mfv_stoplb_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061128", 201),
'mfv_stoplb_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061229", 201),
'mfv_stoplb_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061335", 201),
'mfv_stoplb_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061436", 101),
'mfv_stoplb_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061538", 201),
'mfv_stoplb_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061639", 201),
'mfv_stoplb_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061741", 201),
'mfv_stoplb_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061844", 201),
'mfv_stoplb_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_061947", 101),
'mfv_stoplb_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062050", 101),
'mfv_stoplb_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062153", 101),
'mfv_stoplb_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062256", 201),
'mfv_stoplb_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062357", 201),
'mfv_stoplb_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062500", 101),
'mfv_stoplb_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_062602", 101),
'mfv_stoplb_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_064425", 101),
'mfv_stoplb_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_065825", 201),
'mfv_stoplb_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_065929", 201),
'mfv_stoplb_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070034", 201),
'mfv_stoplb_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070135", 199),
'mfv_stoplb_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070237", 201),
'mfv_stoplb_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070341", 201),
'mfv_stoplb_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070443", 200),
'mfv_stoplb_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070545", 201),
'mfv_stoplb_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070646", 201),
'mfv_stoplb_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070748", 201),
'mfv_stoplb_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070849", 201),
'mfv_stoplb_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_070952", 201),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071055", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071157", 201),
'mfv_stoplb_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071300", 201),
'mfv_stoplb_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071402", 201),
'mfv_stoplb_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071504", 201),
'mfv_stoplb_tau010000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071606", 201),
'mfv_stoplb_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071708", 201),
'mfv_stoplb_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071811", 201),
'mfv_stoplb_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_071914", 201),
'mfv_stoplb_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072017", 201),
'mfv_stoplb_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072120", 101),
'mfv_stoplb_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072222", 201),
'mfv_stoplb_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072324", 201),
'mfv_stopld_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072428", 201),
'mfv_stopld_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072532", 201),
'mfv_stopld_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072633", 101),
'mfv_stopld_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072735", 201),
'mfv_stopld_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_072912", 201),
'mfv_stopld_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073014", 201),
'mfv_stopld_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073117", 201),
'mfv_stopld_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073218", 101),
'mfv_stopld_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073319", 201),
'mfv_stopld_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073420", 201),
'mfv_stopld_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073522", 201),
'mfv_stopld_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073628", 201),
'mfv_stopld_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073729", 101),
'mfv_stopld_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073834", 201),
'mfv_stopld_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_073936", 201),
'mfv_stopld_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074041", 201),
'mfv_stopld_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074143", 201),
'mfv_stopld_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074245", 101),
'mfv_stopld_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074347", 101),
'mfv_stopld_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074449", 101),
'mfv_stopld_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074552", 200),
'mfv_stopld_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074653", 201),
'mfv_stopld_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074756", 101),
'mfv_stopld_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074857", 101),
'mfv_stopld_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_074958", 101),
'mfv_stopld_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075100", 201),
'mfv_stopld_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075203", 201),
'mfv_stopld_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075305", 200),
'mfv_stopld_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075406", 201),
'mfv_stopld_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075508", 201),
'mfv_stopld_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075610", 201),
'mfv_stopld_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075712", 201),
'mfv_stopld_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075813", 201),
'mfv_stopld_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_075915", 201),
'mfv_stopld_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080016", 201),
'mfv_stopld_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080118", 201),
'mfv_stopld_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080220", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080321", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080423", 199),
'mfv_stopld_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080526", 201),
'mfv_stopld_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080628", 201),
'mfv_stopld_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080731", 200),
'mfv_stopld_tau010000um_M0600_2017': (195, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080833/0000/ntuple_%i.root' % i for i in chain(xrange(1,59), xrange(60,197))]),
'mfv_stopld_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_080937", 201),
'mfv_stopld_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082128", 201),
'mfv_stopld_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082231", 201),
'mfv_stopld_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082333", 201),
'mfv_stopld_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082435", 101),
'mfv_stopld_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082537", 201),
'mfv_stopld_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_2017/250319_082640", 201),
'SingleMuon2017B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2017/250319_082752", 180),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2017/250319_082854", 232),
'SingleMuon2017D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2017/250319_082956", 109),
'SingleMuon2017E': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2017/250319_083059", 215),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_2017/250319_122407", 347),
'SingleElectron2017B': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_2017/250319_122508", 83),
'SingleElectron2017C': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_2017/250319_122610", 188),
'SingleElectron2017D': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_2017/250319_122713", 92),
'SingleElectron2017E': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_2017/250319_122815", 171),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_2017/250319_122918", 225),
'SinglePhoton2017B': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_2017/250319_123021", 18),
'SinglePhoton2017C': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_2017/250319_123124", 56),
'SinglePhoton2017D': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_2017/250319_123226", 11),
'SinglePhoton2017E': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_2017/250319_123328", 42),
'SinglePhoton2017F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_2017/250319_085141", 58),

'mfv_stoplb_tau000100um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100148", 108),
'mfv_stoplb_tau000300um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100251", 108),
'mfv_stoplb_tau010000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100355", 54),
'mfv_stoplb_tau001000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100500", 108),
'mfv_stoplb_tau030000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100603", 108),
'mfv_stoplb_tau000100um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100711", 108),
'mfv_stoplb_tau000300um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100826", 108),
'mfv_stoplb_tau010000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_100928", 54),
'mfv_stoplb_tau001000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101031", 106),
'mfv_stoplb_tau030000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101155", 108),
'mfv_stoplb_tau000100um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101257", 108),
'mfv_stoplb_tau000300um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101357", 107),
'mfv_stoplb_tau010000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101459", 54),
'mfv_stoplb_tau001000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101601", 108),
'mfv_stoplb_tau030000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101705", 107),
'mfv_stoplb_tau000100um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101826", 108),
'mfv_stoplb_tau000300um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_101930", 108),
'mfv_stoplb_tau010000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102032", 54),
'mfv_stoplb_tau001000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102136", 54),
'mfv_stoplb_tau030000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102239", 54),
'mfv_stoplb_tau000100um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102343", 108),
'mfv_stoplb_tau000300um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102446", 88),
'mfv_stoplb_tau010000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102550", 53),
'mfv_stoplb_tau001000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102705", 53),
'mfv_stoplb_tau030000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102805", 54),
'mfv_stoplb_tau000100um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_102909", 108),
'mfv_stoplb_tau000300um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_103013", 108),
'mfv_stoplb_tau010000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_103115", 108),
'mfv_stoplb_tau001000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_103218", 108),
'mfv_stoplb_tau030000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_104412", 108),
'mfv_stoplb_tau000100um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_104937", 108),
'mfv_stoplb_tau000300um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105039", 108),
'mfv_stoplb_tau010000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105141", 107),
'mfv_stoplb_tau001000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105246", 108),
'mfv_stoplb_tau030000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105350", 108),
'mfv_stoplb_tau000100um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105455", 108),
'mfv_stoplb_tau000300um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105605", 107),
'mfv_stoplb_tau010000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105708", 108),
'mfv_stoplb_tau001000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105813", 108),
'mfv_stoplb_tau030000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_105915", 108),
'mfv_stoplb_tau000100um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110019", 108),
'mfv_stoplb_tau000300um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110121", 108),
'mfv_stoplb_tau010000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110227", 107),
'mfv_stoplb_tau001000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110332", 108),
'mfv_stoplb_tau030000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110437", 108),
'mfv_stoplb_tau000100um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110549", 108),
'mfv_stoplb_tau000300um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110659", 108),
'mfv_stoplb_tau010000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110800", 54),
'mfv_stoplb_tau001000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_110903", 108),
'mfv_stoplb_tau030000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_111011", 108),
'mfv_stopld_tau000100um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_112214", 108),
'mfv_stopld_tau000300um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_112735", 108),
'mfv_stopld_tau010000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_112836", 54),
'mfv_stopld_tau001000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_112938", 108),
'mfv_stopld_tau030000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113043", 108),
'mfv_stopld_tau000100um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113147", 108),
'mfv_stopld_tau000300um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113250", 108),
'mfv_stopld_tau010000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113357", 54),
'mfv_stopld_tau001000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113501", 108),
'mfv_stopld_tau030000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113602", 108),
'mfv_stopld_tau000100um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113702", 108),
'mfv_stopld_tau000300um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113807", 108),
'mfv_stopld_tau010000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_113913", 54),
'mfv_stopld_tau001000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114015", 108),
'mfv_stopld_tau030000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114117", 108),
'mfv_stopld_tau000100um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114219", 108),
'mfv_stopld_tau000300um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114320", 108),
'mfv_stopld_tau010000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114427", 54),
'mfv_stopld_tau001000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114528", 54),
'mfv_stopld_tau030000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114631", 54),
'mfv_stopld_tau000100um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114734", 108),
'mfv_stopld_tau000300um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114836", 108),
'mfv_stopld_tau010000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_114940", 54),
'mfv_stopld_tau001000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115043", 54),
'mfv_stopld_tau030000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115157", 54),
'mfv_stopld_tau000100um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115304", 108),
'mfv_stopld_tau000300um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115407", 108),
'mfv_stopld_tau010000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115509", 108),
'mfv_stopld_tau001000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115609", 108),
'mfv_stopld_tau030000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115712", 108),
'mfv_stopld_tau000100um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115812", 108),
'mfv_stopld_tau000300um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_115916", 108),
'mfv_stopld_tau010000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120017", 108),
'mfv_stopld_tau001000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120123", 108),
'mfv_stopld_tau030000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120226", 108),
'mfv_stopld_tau000100um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120331", 108),
'mfv_stopld_tau000300um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120448", 108),
'mfv_stopld_tau010000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120553", 107),
'mfv_stopld_tau001000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120653", 108),
'mfv_stopld_tau030000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120758", 108),
'mfv_stopld_tau000100um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_120903", 108),
'mfv_stopld_tau000300um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121006", 108),
'mfv_stopld_tau010000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121109", 108),
'mfv_stopld_tau001000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121210", 108),
'mfv_stopld_tau030000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121316", 108),
'mfv_stopld_tau000100um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121418", 108),
'mfv_stopld_tau000300um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121527", 108),
'mfv_stopld_tau010000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121628", 54),
'mfv_stopld_tau001000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121730", 108),
'mfv_stopld_tau030000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20161/250325_121836", 108),
'qcdempt015_20161': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130427", 32),
'qcdmupt15_20161': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130531", 13),
'qcdempt020_20161': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130635", 8),
'qcdempt030_20161': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130739", 10),
'qcdempt050_20161': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130844", 8),
'qcdempt080_20161': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_130952", 9),
'qcdempt120_20161': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_131056", 11),
'qcdempt170_20161': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_131201", 5),
'qcdempt300_20161': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250321_131304", 8),
'qcdbctoept015_20161': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20161/250321_131415", 25),
'qcdbctoept020_20161': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20161/250321_131517", 13),
'qcdbctoept030_20161': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20161/250321_131621", 13),
'qcdbctoept080_20161': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20161/250321_131724", 16),
'qcdbctoept250_20161': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20161/250325_095740", 19),
'wjetstolnu_0j_20161': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20161/250325_121937", 172),
'wjetstolnu_1j_20161': _fromnum1("/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20161/250325_122046", 200),
'wjetstolnu_2j_20161': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20161/250325_122147", 108),
'dyjetstollM10_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_20161/250325_122252", 35),
'dyjetstollM50_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_20161/250325_122355", 103),
'ttbar_lep_20161': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20161/250325_095842", 66),
'ttbar_semilep_20161': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20161/250325_095945", 217),
'ttbar_had_20161': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20161/250325_100047", 172),
'ww_20161': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250325_122500", 22),
'zz_20161': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250325_122614", 5),
'wz_20161': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20161/250325_123809", 13),
'SingleMuon20161B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20161/250320_210823", 142),
'SingleMuon20161C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20161/250320_210925", 65),
'SingleMuon20161D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20161/250320_211040", 90),
'SingleMuon20161E': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20161/250320_211142", 93),
'SingleMuon20161F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20161/250320_211244", 64),
'SingleElectron20161B2': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20161/250320_211346", 275),
'SingleElectron20161C': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20161/250320_211451", 120),
'SingleElectron20161D': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20161/250320_211553", 164),
'SingleElectron20161E': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20161/250320_211654", 147),
'SingleElectron20161F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20161/250320_211756", 84),
'SinglePhoton20161B': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20161/250320_211857", 41),
'SinglePhoton20161C': (21, ['/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20161/250320_211958/0000/ntuple_%i.root' % i for i in chain(xrange(1,17), xrange(18,23))]),
'SinglePhoton20161D': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20161/250320_212100", 27),
'SinglePhoton20161E': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20161/250320_212204", 21),
'SinglePhoton20161F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20161/250320_212307", 19),

'qcdempt015_20162': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211420", 16),
'qcdmupt15_20162': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211522", 11),
'qcdempt020_20162': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211623", 11),
'qcdempt030_20162': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211726", 4),
'qcdempt050_20162': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211827", 7),
'qcdempt080_20162': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_211929", 8),
'qcdempt120_20162': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_212101", 6),
'qcdempt170_20162': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_212204", 3),
'qcdempt300_20162': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_212311", 5),
'qcdbctoept015_20162': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212412", 28),
'qcdbctoept020_20162': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212515", 15),
'qcdbctoept030_20162': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212617", 23),
'qcdbctoept080_20162': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212720", 16),
'qcdbctoept170_20162': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212829", 17),
'qcdbctoept250_20162': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV13Lepm_WGen_20162/250327_212931", 22),
'wjetstolnu_0j_20162': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20162/250327_234340", 194),
'wjetstolnu_1j_20162': _fromnum1("/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20162/250327_234443", 198),
'wjetstolnu_2j_20162': (126, ['/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV13Lepm_WGen_20162/250327_234545/0000/ntuple_%i.root' % i for i in chain(xrange(1,61), xrange(62,128))]),
'dyjetstollM10_20162': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_20162/250327_234648", 31),
'dyjetstollM50_20162': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV13Lepm_WGen_20162/250327_234752", 95),
'ttbar_lep_20162': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20162/250327_213033", 122),
'ttbar_semilep_20162': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20162/250327_213134", 340),
'ttbar_had_20162': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV13Lepm_WGen_20162/250327_213238", 260),
'ww_20162': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_234854", 26),
'zz_20162': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_234957", 12),
'wz_20162': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV13Lepm_WGen_20162/250327_235100", 15),
'mfv_stoplb_tau000100um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213339", 107),
'mfv_stoplb_tau000300um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213441", 107),
'mfv_stoplb_tau010000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213556", 53),
'mfv_stoplb_tau001000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213658", 107),
'mfv_stoplb_tau030000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213820", 107),
'mfv_stoplb_tau000100um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_213922", 107),
'mfv_stoplb_tau000300um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214023", 107),
'mfv_stoplb_tau010000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214126", 54),
'mfv_stoplb_tau001000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214228", 106),
'mfv_stoplb_tau030000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214332", 107),
'mfv_stoplb_tau000100um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214434", 107),
'mfv_stoplb_tau000300um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214539", 107),
'mfv_stoplb_tau010000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214643", 54),
'mfv_stoplb_tau001000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214745", 107),
'mfv_stoplb_tau030000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214846", 107),
'mfv_stoplb_tau000100um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_214947", 107),
'mfv_stoplb_tau000300um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215049", 107),
'mfv_stoplb_tau010000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215150", 54),
'mfv_stoplb_tau001000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215251", 54),
'mfv_stoplb_tau030000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215352", 54),
'mfv_stoplb_tau000100um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215455", 107),
'mfv_stoplb_tau000300um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215558", 107),
'mfv_stoplb_tau010000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215700", 54),
'mfv_stoplb_tau001000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215804", 54),
'mfv_stoplb_tau030000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_215906", 54),
'mfv_stoplb_tau000100um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220008", 107),
'mfv_stoplb_tau000300um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220110", 107),
'mfv_stoplb_tau010000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220212", 107),
'mfv_stoplb_tau001000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220313", 106),
'mfv_stoplb_tau030000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220415", 107),
'mfv_stoplb_tau000100um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220517", 107),
'mfv_stoplb_tau000300um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220619", 107),
'mfv_stoplb_tau010000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220721", 107),
'mfv_stoplb_tau001000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220822", 107),
'mfv_stoplb_tau030000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_220923", 107),
'mfv_stoplb_tau000100um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221025", 107),
'mfv_stoplb_tau000300um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221127", 107),
'mfv_stoplb_tau010000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221229", 107),
'mfv_stoplb_tau001000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221330", 107),
'mfv_stoplb_tau030000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221432", 107),
'mfv_stoplb_tau000100um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221534", 107),
'mfv_stoplb_tau000300um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221636", 92),
'mfv_stoplb_tau010000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221738", 107),
'mfv_stoplb_tau001000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221840", 107),
'mfv_stoplb_tau030000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_221943", 107),
'mfv_stoplb_tau000100um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222044", 107),
'mfv_stoplb_tau000300um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222145", 107),
'mfv_stoplb_tau010000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222247", 54),
'mfv_stoplb_tau001000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222350", 107),
'mfv_stoplb_tau030000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222452", 107),
'mfv_stopld_tau000100um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222554", 107),
'mfv_stopld_tau000300um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222655", 107),
'mfv_stopld_tau010000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222758", 54),
'mfv_stopld_tau001000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_222901", 107),
'mfv_stopld_tau030000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223002", 107),
'mfv_stopld_tau000100um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223105", 107),
'mfv_stopld_tau000300um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223206", 107),
'mfv_stopld_tau010000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223309", 54),
'mfv_stopld_tau001000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223434", 107),
'mfv_stopld_tau030000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223535", 107),
'mfv_stopld_tau000100um_M1400_20162': (106, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223636/0000/ntuple_%i.root' % i for i in chain(xrange(1,54), xrange(55,108))]),
'mfv_stopld_tau000300um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223739", 107),
'mfv_stopld_tau010000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223841", 54),
'mfv_stopld_tau001000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_223943", 107),
'mfv_stopld_tau030000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224045", 107),
'mfv_stopld_tau000100um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224147", 107),
'mfv_stopld_tau000300um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224248", 107),
'mfv_stopld_tau010000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224350", 54),
'mfv_stopld_tau001000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224451", 54),
'mfv_stopld_tau030000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224553", 54),
'mfv_stopld_tau000100um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224657", 107),
'mfv_stopld_tau000300um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224759", 107),
'mfv_stopld_tau010000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_224900", 54),
'mfv_stopld_tau001000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225002", 54),
'mfv_stopld_tau030000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225104", 54),
'mfv_stopld_tau000100um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225205", 107),
'mfv_stopld_tau000300um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225307", 107),
'mfv_stopld_tau010000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225409", 107),
'mfv_stopld_tau001000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225510", 107),
'mfv_stopld_tau030000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225612", 107),
'mfv_stopld_tau000100um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225749", 107),
'mfv_stopld_tau000300um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225851", 107),
'mfv_stopld_tau010000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_225953", 107),
'mfv_stopld_tau001000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230056", 107),
'mfv_stopld_tau030000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230200", 107),
'mfv_stopld_tau000100um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230302", 107),
'mfv_stopld_tau000300um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230404", 107),
'mfv_stopld_tau010000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230508", 107),
'mfv_stopld_tau001000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230611", 107),
'mfv_stopld_tau030000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230715", 107),
'mfv_stopld_tau000100um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230820", 107),
'mfv_stopld_tau000300um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_230924", 107),
'mfv_stopld_tau010000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231029", 107),
'mfv_stopld_tau001000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231133", 107),
'mfv_stopld_tau030000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231237", 107),
'mfv_stopld_tau000100um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231340", 107),
'mfv_stopld_tau000300um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231444", 107),
'mfv_stopld_tau010000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231547", 54),
'mfv_stopld_tau001000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231650", 107),
'mfv_stopld_tau030000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV13Lepm_WGen_20162/250327_231754", 107),
'SingleMuon20162F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20162/250327_231858", 10),
'SingleMuon20162G': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20162/250327_232002", 158),
'SingleMuon20162H': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV13Lepm_WGen_20162/250327_232105", 195),
'SingleElectron20162F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20162/250327_232214", 21),
'SingleElectron20162G': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20162/250327_232320", 192),
'SingleElectron20162H': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV13Lepm_WGen_20162/250327_232423", 171),
'SinglePhoton20162F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20162/250327_232525", 6),
'SinglePhoton20162G': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20162/250327_232626", 34),
'SinglePhoton20162H': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV13Lepm_WGen_20162/250327_232728", 35),
})




_add_ds("ntupleulv12lepm_wgen", {

'qcdempt015_20161': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_213400", 32),
'qcdmupt15_20161': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_214652", 13),
'qcdempt020_20161': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_215104", 8),
'qcdempt030_20161': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_215302", 11),
'qcdempt050_20161': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_215458", 8),
'qcdempt080_20161': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_215656", 9),
'qcdempt120_20161': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_215855", 11),
'qcdempt170_20161': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_220111", 5),
'qcdempt300_20161': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250225_220311", 8),
'qcdbctoept015_20161': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_220528", 25),
'qcdbctoept020_20161': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_220726", 14),
'qcdbctoept030_20161': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_220922", 13),
'qcdbctoept080_20161': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_221120", 16),
'qcdbctoept170_20161': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_221316", 13),
'qcdbctoept250_20161': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20161/250225_221516", 19),
'wjetstolnu_0j_20161': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20161/250226_034003", 174),
'wjetstolnu_1j_20161': (202, ['/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20161/250226_035251/0000/ntuple_%i.root' % i for i in chain(xrange(1,102), xrange(103,204))]),
'wjetstolnu_2j_20161': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20161/250226_035919", 111),
'dyjetstollM10_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_20161/250226_040116", 35),
'dyjetstollM50_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_20161/250226_040314", 98),
'ttbar_lep_20161': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20161/250225_221716", 59),
'ttbar_semilep_20161': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20161/250225_221913", 217),
'ttbar_had_20161': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20161/250225_222111", 175),
'ww_20161': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250226_040558", 22),
'zz_20161': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250226_040755", 5),
'wz_20161': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20161/250226_040952", 13),

'SingleMuon20161B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20161/250226_031033", 142),
'SingleMuon20161C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20161/250226_031237", 65),
'SingleMuon20161D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20161/250226_031434", 90),
'SingleMuon20161E': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20161/250226_031631", 93),
'SingleMuon20161F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20161/250226_031829", 65),
'SingleElectron20161B2': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20161/250226_032026", 275),
'SingleElectron20161C': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20161/250226_032224", 120),
'SingleElectron20161D': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20161/250226_032419", 164),
'SingleElectron20161E': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20161/250226_032617", 147),
'SingleElectron20161F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20161/250226_032816", 84),
'SinglePhoton20161B': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20161/250226_033014", 41),
'SinglePhoton20161C': (21, ['/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20161/250226_033212/0000/ntuple_%i.root' % i for i in chain(xrange(1,9), xrange(10,23))]), #still waiting
'SinglePhoton20161D': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20161/250226_033409", 27),
'SinglePhoton20161E': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20161/250226_033607", 21),
'SinglePhoton20161F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20161/250226_033805", 19),


'mfv_stoplb_tau000100um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_222307", 108),
'mfv_stoplb_tau000300um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_222504", 108),
'mfv_stoplb_tau010000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_222700", 54),
'mfv_stoplb_tau001000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_222856", 108),
'mfv_stoplb_tau030000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_223056", 108),
'mfv_stoplb_tau000100um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_224348", 108),
'mfv_stoplb_tau000300um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225005", 108),
'mfv_stoplb_tau010000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225204", 54),
'mfv_stoplb_tau001000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225400", 106),
'mfv_stoplb_tau030000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225557", 108),
'mfv_stoplb_tau000100um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225753", 108),
'mfv_stoplb_tau000300um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_225952", 107),
'mfv_stoplb_tau010000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_230158", 54),
'mfv_stoplb_tau001000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_230355", 108),
'mfv_stoplb_tau030000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_230552", 107),
'mfv_stoplb_tau000100um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_230749", 108),
'mfv_stoplb_tau000300um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_230948", 108),
'mfv_stoplb_tau010000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_231153", 54),
'mfv_stoplb_tau001000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_231350", 54),
'mfv_stoplb_tau030000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_231546", 54),
'mfv_stoplb_tau000100um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_231743", 108),
'mfv_stoplb_tau000300um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_231940", 88),
'mfv_stoplb_tau010000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_232137", 53),
'mfv_stoplb_tau001000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_232332", 53),
'mfv_stoplb_tau030000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_232528", 54),
'mfv_stoplb_tau000100um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_232726", 108),
'mfv_stoplb_tau000300um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_232923", 108),
'mfv_stoplb_tau010000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_233118", 108),
'mfv_stoplb_tau001000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_233315", 108),
'mfv_stoplb_tau030000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_234604", 108),
'mfv_stoplb_tau000100um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_235223", 108),
'mfv_stoplb_tau000300um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_235420", 108),
'mfv_stoplb_tau010000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_235623", 107),
'mfv_stoplb_tau001000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250225_235825", 108),
'mfv_stoplb_tau030000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_000049", 108),
'mfv_stoplb_tau000100um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_000255", 108),
'mfv_stoplb_tau000300um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_000455", 107),
'mfv_stoplb_tau010000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_000652", 108),
'mfv_stoplb_tau001000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_000853", 108),
'mfv_stoplb_tau030000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_001050", 108),
'mfv_stoplb_tau000100um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_001248", 108),
'mfv_stoplb_tau000300um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_001445", 108),
'mfv_stoplb_tau010000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_001645", 107),
'mfv_stoplb_tau001000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_001842", 108),
'mfv_stoplb_tau030000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_002039", 108),
'mfv_stoplb_tau000100um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_002236", 108),
'mfv_stoplb_tau000300um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_002434", 108),
'mfv_stoplb_tau010000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_002632", 54),
'mfv_stoplb_tau001000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_002828", 108),
'mfv_stoplb_tau030000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_003036", 108),
'mfv_stopld_tau000100um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_003242", 108),
'mfv_stopld_tau000300um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_003448", 108),
'mfv_stopld_tau010000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_004738", 54),
'mfv_stopld_tau001000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_005358", 108),
'mfv_stopld_tau030000um_M1000_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_005556", 108),
'mfv_stopld_tau000100um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_005802", 108),
'mfv_stopld_tau000300um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_010003", 108),
'mfv_stopld_tau010000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_010207", 54),
'mfv_stopld_tau001000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_010427", 108),
'mfv_stopld_tau030000um_M1200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_010623", 108),
'mfv_stopld_tau000100um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_010823", 108),
'mfv_stopld_tau000300um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_011018", 108),
'mfv_stopld_tau010000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_011217", 54),
'mfv_stopld_tau001000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_011414", 108),
'mfv_stopld_tau030000um_M1400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_011611", 108),
'mfv_stopld_tau000100um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_011810", 108),
'mfv_stopld_tau000300um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_012009", 108),
'mfv_stopld_tau010000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_012206", 54),
'mfv_stopld_tau001000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_012404", 54),
'mfv_stopld_tau030000um_M1600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_012603", 54),
'mfv_stopld_tau000100um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_012800", 108),
'mfv_stopld_tau000300um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_013001", 108),
'mfv_stopld_tau010000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_013210", 54),
'mfv_stopld_tau001000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_013412", 54),
'mfv_stopld_tau030000um_M1800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_013609", 54),
'mfv_stopld_tau000100um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_013804", 108),
'mfv_stopld_tau000300um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014002", 108),
'mfv_stopld_tau010000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014200", 108),
'mfv_stopld_tau001000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014401", 108),
'mfv_stopld_tau030000um_M0200_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014558", 108),
'mfv_stopld_tau000100um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014755", 108),
'mfv_stopld_tau000300um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_014951", 108),
'mfv_stopld_tau010000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_015148", 108),
'mfv_stopld_tau001000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_015347", 108),
'mfv_stopld_tau030000um_M0300_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_015543", 108),
'mfv_stopld_tau000100um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_015740", 108),
'mfv_stopld_tau000300um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_015937", 108),
'mfv_stopld_tau010000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_020137", 107),
'mfv_stopld_tau001000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_020334", 108),
'mfv_stopld_tau030000um_M0400_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_020537", 108),
'mfv_stopld_tau000100um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_020733", 108),
'mfv_stopld_tau000300um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_022025", 108),
'mfv_stopld_tau010000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_022640", 108),
'mfv_stopld_tau001000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_022839", 108),
'mfv_stopld_tau030000um_M0600_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_023034", 108),
'mfv_stopld_tau000100um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_023232", 108),
'mfv_stopld_tau000300um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_023426", 108),
'mfv_stopld_tau010000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_023621", 54),
'mfv_stopld_tau001000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_023818", 108),
'mfv_stopld_tau030000um_M0800_20161': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20161/250226_025741", 108),

'qcdempt015_20162': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_212527", 16),
'qcdmupt15_20162': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_212727", 11),
'qcdempt020_20162': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_213001", 11),
'qcdempt030_20162': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_213208", 4),
'qcdempt050_20162': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_213410", 7),
'qcdempt080_20162': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_213609", 8),
'qcdempt120_20162': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_213809", 6),
'qcdempt170_20162': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_214007", 3),
'qcdempt300_20162': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250227_214208", 5),
'qcdbctoept015_20162': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_214408", 29),
'qcdbctoept020_20162': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_214609", 15),
'qcdbctoept030_20162': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_214809", 23),
'qcdbctoept080_20162': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_215006", 16),
'qcdbctoept170_20162': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_215206", 17),
'qcdbctoept250_20162': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_20162/250227_215407", 22),
'wjetstolnu_0j_20162': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20162/250228_150833", 194),
'wjetstolnu_1j_20162': _fromnum1("/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20162/250228_022125", 203),
'wjetstolnu_2j_20162': (130, ['/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_20162/250228_151035/0000/ntuple_%i.root' % i for i in chain(xrange(1,104), xrange(105,132))]),
'dyjetstollM10_20162': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_20162/250228_022536", 31),
'dyjetstollM50_20162': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_20162/250228_022737", 95),
'ttbar_lep_20162': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20162/250227_215609", 125),
'ttbar_semilep_20162': (347, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20162/250227_215809/0000/ntuple_%i.root' % i for i in chain(xrange(1,257), xrange(258,349))]),
'ttbar_had_20162': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_20162/250227_220006", 264), #failed at publication status, but is present on hdfs
'ww_20162': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250228_024120", 25),
'zz_20162': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250228_024915", 12),
'wz_20162': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_20162/250228_025116", 15),
'mfv_stoplb_tau000100um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_220205", 107),
'mfv_stoplb_tau000300um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_220404", 107),
'mfv_stoplb_tau010000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_220602", 53),
'mfv_stoplb_tau001000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_220759", 107),
'mfv_stoplb_tau030000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_220957", 107),
'mfv_stoplb_tau000100um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_221200", 107),
'mfv_stoplb_tau000300um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_221553", 107),
'mfv_stoplb_tau010000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_221750", 54),
'mfv_stoplb_tau001000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_221947", 106),
'mfv_stoplb_tau030000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_222146", 107),
'mfv_stoplb_tau000100um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_222346", 107),
'mfv_stoplb_tau000300um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_222543", 107),
'mfv_stoplb_tau010000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_222740", 54),
'mfv_stoplb_tau001000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_222939", 107),
'mfv_stoplb_tau030000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_223138", 107),
'mfv_stoplb_tau000100um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_223335", 107),
'mfv_stoplb_tau000300um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_223533", 107),
'mfv_stoplb_tau010000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_223730", 54),
'mfv_stoplb_tau001000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_225040", 54),
'mfv_stoplb_tau030000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_225704", 54),
'mfv_stoplb_tau000100um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_225901", 107),
'mfv_stoplb_tau000300um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_230106", 107),
'mfv_stoplb_tau010000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_230306", 54),
'mfv_stoplb_tau001000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_230503", 54),
'mfv_stoplb_tau030000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_230701", 54),
'mfv_stoplb_tau000100um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_230906", 107),
'mfv_stoplb_tau000300um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_231103", 107),
'mfv_stoplb_tau010000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_231302", 107),
'mfv_stoplb_tau001000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_231505", 106),
'mfv_stoplb_tau030000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_231707", 107),
'mfv_stoplb_tau000100um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_231906", 107),
'mfv_stoplb_tau000300um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_232105", 107),
'mfv_stoplb_tau010000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_232302", 107),
'mfv_stoplb_tau001000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_232501", 107),
'mfv_stoplb_tau030000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_232701", 107),
'mfv_stoplb_tau000100um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_232901", 107),
'mfv_stoplb_tau000300um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_233059", 107),
'mfv_stoplb_tau010000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_233310", 107),
'mfv_stoplb_tau001000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_233511", 107),
'mfv_stoplb_tau030000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_233740", 107),
'mfv_stoplb_tau000100um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_233951", 107),
'mfv_stoplb_tau000300um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_234149", 92),
'mfv_stoplb_tau010000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_234354", 107),
'mfv_stoplb_tau001000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_234552", 107),
'mfv_stoplb_tau030000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_234946", 107),
'mfv_stoplb_tau000100um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_235146", 107),
'mfv_stoplb_tau000300um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_235343", 107),
'mfv_stoplb_tau010000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_235543", 54),
'mfv_stoplb_tau001000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_235739", 107),
'mfv_stoplb_tau030000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250227_235939", 107),
'mfv_stopld_tau000100um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_000140", 107),
'mfv_stopld_tau000300um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_000451", 107),
'mfv_stopld_tau010000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_000651", 54),
'mfv_stopld_tau001000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_000851", 107),
'mfv_stopld_tau030000um_M1000_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_001048", 107),
'mfv_stopld_tau000100um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_001247", 107),
'mfv_stopld_tau000300um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_001452", 107),
'mfv_stopld_tau010000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_001651", 54),
'mfv_stopld_tau001000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_001851", 107),
'mfv_stopld_tau030000um_M1200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_002053", 107),
'mfv_stopld_tau000100um_M1400_20162': (106, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_002254/0000/ntuple_%i.root' % i for i in chain(xrange(1,54), xrange(55,108))]),
'mfv_stopld_tau000300um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_002454", 107),
'mfv_stopld_tau010000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_002653", 54),
'mfv_stopld_tau001000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_002855", 107),
'mfv_stopld_tau030000um_M1400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_003100", 107),
'mfv_stopld_tau000100um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_003302", 107),
'mfv_stopld_tau000300um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_003509", 107),
'mfv_stopld_tau010000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_003716", 54),
'mfv_stopld_tau001000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_004025", 43),
'mfv_stopld_tau030000um_M1600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_004229", 54),
'mfv_stopld_tau000100um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_004430", 101),
'mfv_stopld_tau000300um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_004634", 107),
'mfv_stopld_tau010000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_004839", 54),
'mfv_stopld_tau001000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_005038", 54),
'mfv_stopld_tau030000um_M1800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_005237", 54),
'mfv_stopld_tau000100um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_005444", 107),
'mfv_stopld_tau000300um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_005645", 107),
'mfv_stopld_tau010000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_005844", 107),
'mfv_stopld_tau001000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_010045", 107),
'mfv_stopld_tau030000um_M0200_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_010301", 105),
'mfv_stopld_tau000100um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_010501", 107),
'mfv_stopld_tau000300um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_010657", 107),
'mfv_stopld_tau010000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_010855", 107),
'mfv_stopld_tau001000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_011055", 107),
'mfv_stopld_tau030000um_M0300_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_011256", 107),
'mfv_stopld_tau000100um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_011456", 107),
'mfv_stopld_tau000300um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_011657", 107),
'mfv_stopld_tau010000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_011902", 107),
'mfv_stopld_tau001000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_012104", 107),
'mfv_stopld_tau030000um_M0400_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_012307", 107),
'mfv_stopld_tau000100um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_012518", 107),
'mfv_stopld_tau000300um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_012729", 107),
'mfv_stopld_tau010000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_012932", 107),
'mfv_stopld_tau001000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_013132", 107),
'mfv_stopld_tau030000um_M0600_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_013333", 107),
'mfv_stopld_tau000100um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_013533", 107),
'mfv_stopld_tau000300um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_013732", 107),
'mfv_stopld_tau010000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_013931", 54),
'mfv_stopld_tau001000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_014131", 107),
'mfv_stopld_tau030000um_M0800_20162': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_20162/250228_015423", 107),

'SingleMuon20162F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20162/250228_020111", 10),
'SingleMuon20162G': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20162/250228_020313", 158),
'SingleMuon20162H': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_20162/250228_020511", 195),
'SingleElectron20162F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20162/250228_020710", 21),
'SingleElectron20162G': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20162/250228_020917", 192),
'SingleElectron20162H': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_20162/250228_021114", 171),
'SinglePhoton20162F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20162/250228_021313", 6),
'SinglePhoton20162G': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20162/250228_021514", 34),
'SinglePhoton20162H': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_20162/250228_021721", 35),

'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_090313", 38),
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_090554", 15),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_090750", 19),
'qcdempt030_2017': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_090950", 9),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_091147", 18),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_091342", 22),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_091538", 29),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_091739", 7),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_091937", 6),
'qcdbctoept015_2017': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_092137", 52),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_092333", 45),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_092532", 38),
'qcdbctoept080_2017': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_092728", 33),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_092926", 27),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2017/250223_093124", 34),
'ttbar_lep_2017': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2017/250223_093326", 136),
'ttbar_semilep_2017': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2017/250223_093522", 436),
'ttbar_had_2017': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2017/250223_093718", 314),
'wjetstolnu_0j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2017/250223_144326", 207),
'wjetstolnu_1j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2017/250223_144526", 225),
'wjetstolnu_2j_2017': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2017/250223_144728", 119),
'dyjetstollM10_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_2017/250223_144929", 100),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_2017/250223_145128", 128),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_145324", 23),
'zz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_145521", 4),
'wz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2017/250223_145721", 17),

'mfv_stoplb_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_093916", 201),
'mfv_stoplb_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_094113", 201),
'mfv_stoplb_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_094311", 101),
'mfv_stoplb_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_094506", 201),
'mfv_stoplb_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_094704", 201),
'mfv_stoplb_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_094901", 201),
'mfv_stoplb_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_095058", 200),
'mfv_stoplb_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_095255", 101),
'mfv_stoplb_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_095452", 201),
'mfv_stoplb_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_095648", 201),
'mfv_stoplb_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_095843", 201),
'mfv_stoplb_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_100043", 201),
'mfv_stoplb_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_100241", 101),
'mfv_stoplb_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_101534", 201),
'mfv_stoplb_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_101734", 201),
'mfv_stoplb_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_101932", 201),
'mfv_stoplb_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_102129", 201),
'mfv_stoplb_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_102325", 101),
'mfv_stoplb_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_102522", 101),
'mfv_stoplb_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_102721", 101),
'mfv_stoplb_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_102918", 201),
'mfv_stoplb_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_103115", 201),
'mfv_stoplb_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_103312", 101),
'mfv_stoplb_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_103510", 101),
'mfv_stoplb_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_103707", 101),
'mfv_stoplb_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_103902", 201),
'mfv_stoplb_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_104059", 201),
'mfv_stoplb_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_104255", 201),
'mfv_stoplb_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_104450", 199),
'mfv_stoplb_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_104648", 201),
'mfv_stoplb_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_104847", 201),
'mfv_stoplb_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_105044", 200),
'mfv_stoplb_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_105240", 201),
'mfv_stoplb_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_105436", 201),
'mfv_stoplb_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_105633", 201),
'mfv_stoplb_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_105831", 201),
'mfv_stoplb_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_110027", 201),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_110225", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_110429", 201),
'mfv_stoplb_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_110626", 201),
'mfv_stoplb_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_110823", 201),
'mfv_stoplb_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_111019", 201),
'mfv_stoplb_tau010000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_111216", 201),
'mfv_stoplb_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_111416", 201),
'mfv_stoplb_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_111613", 201),
'mfv_stoplb_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_111814", 201),
'mfv_stoplb_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_112011", 201),
'mfv_stoplb_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_112209", 101),
'mfv_stoplb_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_113457", 201),
'mfv_stoplb_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_114113", 201),
'mfv_stopld_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_114310", 201),
'mfv_stopld_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_114508", 201),
'mfv_stopld_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_115758", 101),
'mfv_stopld_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_120414", 201),
#'mfv_stopld_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_120612", 201),
'mfv_stopld_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250225_165329", 201),
'mfv_stopld_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_120808", 201),
'mfv_stopld_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121004", 201),
'mfv_stopld_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121203", 101),
'mfv_stopld_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121402", 201),
'mfv_stopld_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121558", 170), #huh? why only 170? 
'mfv_stopld_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121755", 201),
'mfv_stopld_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_121951", 201),
'mfv_stopld_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_122149", 101),
'mfv_stopld_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_122345", 201),
'mfv_stopld_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_122542", 201),
'mfv_stopld_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_122740", 201),
'mfv_stopld_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_122937", 201),
'mfv_stopld_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_123556", 101),
'mfv_stopld_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_125515", 101),
'mfv_stopld_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_131502", 101),
'mfv_stopld_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_132117", 200),
'mfv_stopld_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_132313", 201),
'mfv_stopld_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_132509", 101),
'mfv_stopld_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_132705", 101),
'mfv_stopld_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_132901", 101),
'mfv_stopld_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_133057", 201),
'mfv_stopld_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_133253", 201),
'mfv_stopld_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_133505", 200),
'mfv_stopld_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_133707", 201),
'mfv_stopld_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_133903", 201),
'mfv_stopld_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_134102", 201),
'mfv_stopld_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_134300", 201),
'mfv_stopld_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_134459", 201),
'mfv_stopld_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_134700", 201),
'mfv_stopld_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_134902", 201),
'mfv_stopld_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_135100", 201),
'mfv_stopld_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_135259", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_135457", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_135653", 199),
'mfv_stopld_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_135853", 201),
'mfv_stopld_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_140049", 201),
'mfv_stopld_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_140344", 200),
'mfv_stopld_tau010000um_M0600_2017': (195, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_140657/0000/ntuple_%i.root' % i for i in chain(xrange(1,49), xrange(50,197))]), #one ntuple failed because an event has a duplicate(?) LLP -> should try and rerun this sometime? 
'mfv_stopld_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_140854", 201),
'mfv_stopld_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_141051", 201),
'mfv_stopld_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_141247", 201),
'mfv_stopld_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_141447", 201),
'mfv_stopld_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_141644", 101),
'mfv_stopld_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_141843", 201),
'mfv_stopld_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2017/250223_142046", 201),

'SingleMuon2017B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2017/250224_111418", 180),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2017/250224_111616", 232),
'SingleMuon2017D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2017/250304_082707", 109),
'SingleMuon2017E': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2017/250224_112018", 215),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2017/250224_112219", 347),
'SingleElectron2017B': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_2017/250224_112418", 83),
'SingleElectron2017C': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_2017/250224_112615", 188),
'SingleElectron2017D': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_2017/250224_112813", 93),
'SingleElectron2017E': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_2017/250224_114103", 171),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/NtupleULV12Lepm_WGen_2017/250224_114305", 225),
'SinglePhoton2017B': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_2017/250224_114504", 18),
'SinglePhoton2017C': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_2017/250224_114707", 49),
'SinglePhoton2017D': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_2017/250224_114906", 11),
'SinglePhoton2017E': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_2017/250224_115105", 35),
'SinglePhoton2017F': _fromnum1("/store/user/awarden/SinglePhoton/NtupleULV12Lepm_WGen_2017/250224_115305", 51),


'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_142720", 35),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_142918", 16),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_143116", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_143315", 16),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_143515", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_143725", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_143927", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_144125", 5),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_144322", 4),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_144536", 19),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_144732", 51),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_144931", 36),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_145148", 49),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_145557", 55),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV12Lepm_WGen_2018/250221_145801", 23),
'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2018/250221_150003", 310),
'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2018/250221_152451", 1005),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV12Lepm_WGen_2018/250221_152657", 723),
'wjetstolnu_0j_2018': _fromnum1("/store/user/awarden/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2018/250224_100928", 195),
'wjetstolnu_1j_2018': (218, ['/store/user/awarden/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2018/250221_154806/0000/ntuple_%i.root' % i for i in chain(xrange(1,115), xrange(116,188), xrange(189,221))]),
'wjetstolnu_2j_2018': _fromnum1("/store/user/awarden/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleULV12Lepm_WGen_2018/250221_155004", 194),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_2018/250221_155204", 117),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV12Lepm_WGen_2018/250221_155403", 110),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_155605", 23),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_155805", 17),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV12Lepm_WGen_2018/250221_160003", 5),

'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_182705", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_182901", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_183058", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_183254", 201),
#'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_183452", 102),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_200018", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_183650", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_183848", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_200217", 200),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_200415", 201),
#'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_184047", 143),
#'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_184245", 55),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_184444", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_082859", 201),
#'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_184839", 173),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_200613", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_185035", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_083059", 201),
#'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_185439", 52),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_200810", 200),
#'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_185639", 184),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_201007", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_185836", 200),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_083303", 200),
#'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_190229", 5),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1('/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_201202', 201),
#or? 
#'mfv_stoplb_tau010000um_M0600_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250225_201202/0000/ntuple_%i.root' % i for i in chain(xrange(1,77), xrange(78,108), xrange(109,202))]),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_083503", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_083659", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_083856", 200),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_084052", 201),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_084247", 100),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_084444", 201),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_084639", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_084837", 201),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_085035", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_085232", 101),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_085428", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_192552", 192),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_192747", 201),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_192943", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_193137", 101),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_193333", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_193528", 199),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_193724", 201),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_193919", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_194114", 101),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_194312", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_194508", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_194705", 201),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_194901", 101),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_195056", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_195252", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_195447", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_195643", 201),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_195839", 101),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_200034", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_200231", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_200431", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_200626", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_200821", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201016", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201212", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201406", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201601", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201756", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_201952", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_203239", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_203853", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_204050", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_204248", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_204443", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_204641", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_204836", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_205030", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_205239", 200),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_205437", 201),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_205630", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250221_085832", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_210022", 201),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_210218", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_210413", 101),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_210611", 201),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_210805", 197),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_212050", 201),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_212706", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_212906", 101),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_213104", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_213302", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_213500", 201),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_213657", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_213858", 101),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_215146", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_215807", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220002", 200),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220204", 201),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220359", 101),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220556", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220753", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_220948", 201),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_221145", 101),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_221341", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_221539", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_221734", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_221930", 201),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_222136", 101),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_222331", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV12Lepm_WGen_2018/250220_222530", 101),

'SingleMuon2018A': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250224_095209", 410),
#'SingleMuon2018B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250224_095406", 191),
'SingleMuon2018B': (1, ["/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250224_095406/0000/ntuple_4.root"]),

'SingleMuon2018C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250224_095604", 185),
# 'SingleMuon2018D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250224_095801", 798), #track rescaling as usual 
#'SingleMuon2018D': (689, ['/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250311_215931/0000/ntuple_%i.root' % i for i in chain(xrange(1,16), xrange(19,36), xrange(37,40), xrange(41,44), xrange(45,56), xrange(57,65), xrange(66,109), xrange(113,126), xrange(127,142), xrange(143,167), xrange(168,171), xrange(176,191), xrange(192,197), xrange(198,203), xrange(204,206), xrange(207,222), xrange(223,233), xrange(234,246), xrange(247,274), xrange(278,282), xrange(283,285), xrange(288,303), xrange(304,311), xrange(312,330), xrange(332,364), xrange(365,368), xrange(369,371), xrange(376,407), xrange(408,414), xrange(416,422), xrange(423,426), xrange(427,435), xrange(436,439), xrange(441,447), xrange(448,467), xrange(471,474), xrange(475,479), xrange(485,487), xrange(491,495), xrange(496,500), xrange(502,507), xrange(508,512), xrange(516,522), xrange(523,528), xrange(529,532), xrange(533,538), xrange(541,544), xrange(546,549), xrange(550,553), xrange(555,567), xrange(568,570), xrange(571,576), xrange(577,615), xrange(616,618), xrange(620,628), xrange(629,636), xrange(637,645), xrange(651,657), xrange(658,671), xrange(672,674), xrange(675,678), xrange(680,684), xrange(687,704), xrange(705,717), xrange(718,721), xrange(722,733), xrange(734,737), xrange(739,743), xrange(744,769), xrange(770,784), xrange(785,799), [17, 111, 172, 275, 373, 469, 480, 482, 514, 539, 685])]),
#above single muon 2018D has no track rescaling
'SingleMuon2018D': (692, ['/store/user/awarden/SingleMuon/NtupleULV12Lepm_WGen_2018/250313_084439/0000/ntuple_%i.root' % i for i in chain(xrange(1,32), xrange(33,37), xrange(38,41), xrange(44,52), xrange(53,60), xrange(61,117), xrange(118,195), xrange(198,202), xrange(203,205), xrange(207,227), xrange(228,231), xrange(232,238), xrange(240,242), xrange(243,245), xrange(252,261), xrange(263,276), xrange(277,281), xrange(282,316), xrange(317,321), xrange(322,327), xrange(328,330), xrange(331,367), xrange(369,383), xrange(384,403), xrange(406,408), xrange(409,414), xrange(415,423), xrange(426,438), xrange(439,448), xrange(449,469), xrange(472,475), xrange(476,490), xrange(498,501), xrange(507,510), xrange(511,513), xrange(517,523), xrange(526,532), xrange(534,536), xrange(539,544), xrange(547,549), xrange(560,563), xrange(565,571), xrange(575,577), xrange(581,587), xrange(588,590), xrange(591,594), xrange(595,597), xrange(598,602), xrange(603,614), xrange(619,622), xrange(623,628), xrange(629,631), xrange(634,643), xrange(644,696), xrange(697,707), xrange(708,745), xrange(746,752), xrange(755,772), xrange(773,781), xrange(782,789), xrange(790,799), [42, 196, 247, 404, 470, 491, 493, 495, 502, 504, 514, 524, 545, 554, 557, 572, 579, 615, 617, 632, 753])]),
#above is single muon w/ track rescaling but only 3tk SV being saved 

'EGamma2018A': _fromnum1("/store/user/awarden/EGamma/NtupleULV12Lepm_WGen_2018/250224_100002", 713),
'EGamma2018B': _fromnum1("/store/user/awarden/EGamma/NtupleULV12Lepm_WGen_2018/250224_100159", 295),
#'EGamma2018C': _fromnum1("/store/user/awarden/EGamma/NtupleULV12Lepm_WGen_2018/250224_100357", 310),
'EGamma2018C': (308, ['/store/user/awarden/EGamma/NtupleULV12Lepm_WGen_2018/250312_133054/0000/ntuple_%i.root' % i for i in chain(xrange(1,71), xrange(72,116), xrange(117,311))]), #saved explicitely track_dxyerr 
'EGamma2018D': _fromnum1("/store/user/awarden/EGamma/NtupleULV12Lepm_WGen_2018/250224_100554", 1438),

})

## testing if data-mc discrepancy in assoc lepton pT is due to not dropping lepton tracks at deltaz stage; impatient and moving on without full EGamma2018D
_add_ds("ntupleulv12_ogdeltazlepm_wgen", {
'SingleMuon2018A': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12_ogdeltazLepm_WGen_2018/241031_144408", 383),
'SingleMuon2018B': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12_ogdeltazLepm_WGen_2018/241031_150911", 179),
'SingleMuon2018C': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12_ogdeltazLepm_WGen_2018/241031_141357", 170),
'SingleMuon2018D': _fromnum1("/store/user/awarden/SingleMuon/NtupleULV12_ogdeltazLepm_WGen_2018/241031_141555", 755),
'EGamma2018A': _fromnum1("/store/user/awarden/EGamma/NtupleULV12_ogdeltazLepm_WGen_2018/241031_141752", 591),
'EGamma2018B': _fromnum1("/store/user/awarden/EGamma/NtupleULV12_ogdeltazLepm_WGen_2018/241031_141947", 259),
'EGamma2018C': _fromnum1("/store/user/awarden/EGamma/NtupleULV12_ogdeltazLepm_WGen_2018/241031_142143", 259),
'EGamma2018D': (1231, ['/store/user/awarden/EGamma/NtupleULV12_ogdeltazLepm_WGen_2018/241031_142339' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,397), xrange(398,448), xrange(449,1227), xrange(1228,1230), xrange(1235,1237), [1231, 1233, 1238])]),
})


#TrackingTreer
_add_ds("trackingtreerulv2_lepm", {
'qcdempt015_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171542", 32, fnbase="trackingtreer"),
'qcdmupt15_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093128", 13, fnbase="trackingtreer"),
'qcdempt020_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171748", 8, fnbase="trackingtreer"),
'qcdempt030_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093230", 8, fnbase="trackingtreer"),
'qcdempt050_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171953", 8, fnbase="trackingtreer"),
'qcdempt080_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172057", 8, fnbase="trackingtreer"),
'qcdempt120_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172200", 10, fnbase="trackingtreer"),
'qcdempt170_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172303", 5, fnbase="trackingtreer"),
'qcdempt300_2016APV': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093352", 6, fnbase="trackingtreer"),
'qcdbctoept020_2016APV': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172508", 13, fnbase="trackingtreer"),
'qcdbctoept030_2016APV': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172613", 13, fnbase="trackingtreer"),
'qcdbctoept080_2016APV': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172720", 16, fnbase="trackingtreer"),
'qcdbctoept170_2016APV': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172821", 13, fnbase="trackingtreer"),
'qcdbctoept250_2016APV': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172922", 16, fnbase="trackingtreer"),
'wjetstolnu_2016APV': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173333", 94, fnbase="trackingtreer"),
'dyjetstollM10_2016APV': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173438", 33, fnbase="trackingtreer"),
'dyjetstollM50_2016APV': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173540", 103, fnbase="trackingtreer"),
'ttbar_lep_2016APV': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173027", 66, fnbase="trackingtreer"),
'ttbar_semilep_2016APV': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173129", 204, fnbase="trackingtreer"),
'ttbar_had_2016APV': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173231", 153, fnbase="trackingtreer"),
'ww_2016APV': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093522", 22, fnbase="trackingtreer"),
'zz_2016APV': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_173748", 5, fnbase="trackingtreer"),
'wz_2016APV': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_173850", 13, fnbase="trackingtreer"),
'qcdempt015_2016': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154212", 12, fnbase="trackingtreer"),
'qcdmupt15_2016': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154314", 11, fnbase="trackingtreer"),
'qcdempt020_2016': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154415", 12, fnbase="trackingtreer"),
'qcdempt030_2016': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154516", 4, fnbase="trackingtreer"),
'qcdempt050_2016': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154619", 7, fnbase="trackingtreer"),
'qcdempt080_2016': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154723", 8, fnbase="trackingtreer"),
'qcdempt120_2016': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154825", 6, fnbase="trackingtreer"),
'qcdempt170_2016': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_154926", 3, fnbase="trackingtreer"),
'qcdempt300_2016': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_155027", 5, fnbase="trackingtreer"),
'qcdbctoept020_2016': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20162/240811_155127", 13, fnbase="trackingtreer"),
'qcdbctoept030_2016': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20162/240811_155232", 18, fnbase="trackingtreer"),
'qcdbctoept080_2016': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20162/240811_155334", 16, fnbase="trackingtreer"),
'qcdbctoept170_2016': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20162/240811_155435", 16, fnbase="trackingtreer"),
'qcdbctoept250_2016': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20162/240811_155537", 17, fnbase="trackingtreer"),
'wjetstolnu_2016': (99, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20162/240811_155954/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,37), xrange(38,101))]),
'dyjetstollM10_2016': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20162/240811_160056", 29, fnbase="trackingtreer"),
'dyjetstollM50_2016': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20162/240811_160157", 95, fnbase="trackingtreer"),
'ttbar_lep_2016': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20162/240811_155644", 107, fnbase="trackingtreer"),
'ttbar_semilep_2016': (324, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20162/240811_155746/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,182), xrange(183,326))]),
'ttbar_had_2016': (246, ['/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20162/240811_155849/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,88), xrange(89,248))]),
'ww_2016': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_160302", 25, fnbase="trackingtreer"),
'zz_2016': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_160405", 9, fnbase="trackingtreer"),
'wz_2016': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20162/240811_160506", 15, fnbase="trackingtreer"),
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_094641", 10, fnbase="trackingtreer"),
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_094744", 32, fnbase="trackingtreer"),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_094840", 20, fnbase="trackingtreer"),
'qcdempt030_2017': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_094942", 9, fnbase="trackingtreer"),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_095035", 18, fnbase="trackingtreer"),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_095131", 22, fnbase="trackingtreer"),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_095308", 24, fnbase="trackingtreer"),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_095408", 7, fnbase="trackingtreer"),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_095501", 5, fnbase="trackingtreer"),
'qcdbctoept015_2017': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_095558", 39, fnbase="trackingtreer"),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_095652", 30, fnbase="trackingtreer"),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_095754", 30, fnbase="trackingtreer"),
'qcdbctoept080_2017': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_095852", 29, fnbase="trackingtreer"),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_095946", 28, fnbase="trackingtreer"),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2017/240514_100043", 24, fnbase="trackingtreer"),
'ttbar_lep_2017': (133, ['/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2017/240730_115533/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,10), xrange(11,47), xrange(48,104), xrange(105,137))]),
'ttbar_semilep_2017': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2017/240514_100235", 436, fnbase="trackingtreer"),
'ttbar_had_2017': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2017/240514_100331", 299, fnbase="trackingtreer"),
#'wjetstolnu_2017': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101353", 107, fnbase="trackingtreer"),
'dyjetstollM10_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101449", 90, fnbase="trackingtreer"),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101545", 129, fnbase="trackingtreer"),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101647", 23, fnbase="trackingtreer"),
'zz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101745", 4, fnbase="trackingtreer"),
'wz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101840", 15, fnbase="trackingtreer"),

'SingleMuon2016APVB2': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20161/240811_100205", 99, fnbase="trackingtreer"),
'SingleMuon2016APVC': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20161/240808_081334", 44, fnbase="trackingtreer"),
'SingleMuon2016APVD': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20161/240808_081439", 62, fnbase="trackingtreer"),
'SingleMuon2016APVE': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20161/240808_081548", 62, fnbase="trackingtreer"),
'SingleMuon2016APVF': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20161/240808_081654", 43, fnbase="trackingtreer"),
'SingleElectron2016APVB2': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20161/240811_100309", 177, fnbase="trackingtreer"),
'SingleElectron2016APVC': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20161/240808_082012", 75, fnbase="trackingtreer"),
'SingleElectron2016APVD': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20161/240808_082125", 108, fnbase="trackingtreer"),
'SingleElectron2016APVE': (88, ['/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20161/240808_082230/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,75), xrange(78,91), [76])]),
'SingleElectron2016APVF': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20161/240808_082333", 55, fnbase="trackingtreer"),
'SingleMuon2016F': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20162/240811_152421", 8, fnbase="trackingtreer"),
'SingleMuon2016G': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20162/240811_152523", 107, fnbase="trackingtreer"),
'SingleMuon2016H': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_20162/240811_152628", 130, fnbase="trackingtreer"),
'SingleElectron2016F': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20162/240811_152730", 10, fnbase="trackingtreer"),
'SingleElectron2016G': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20162/240811_152832", 127, fnbase="trackingtreer"),
'SingleElectron2016H': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_20162/240811_152935", 116, fnbase="trackingtreer"),
'SingleMuon2017B': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2017/240514_100430", 105, fnbase="trackingtreer"),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2017/240514_100525", 145, fnbase="trackingtreer"),
'SingleMuon2017D': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2017/240514_100621", 66, fnbase="trackingtreer"),
'SingleMuon2017E': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2017/240514_100719", 140, fnbase="trackingtreer"),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2017/240514_100813", 214, fnbase="trackingtreer"),
'SingleElectron2017B': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_2017/240514_100907", 55, fnbase="trackingtreer"),
'SingleElectron2017C': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_2017/240514_101005", 126, fnbase="trackingtreer"),
'SingleElectron2017D': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_2017/240514_101101", 66, fnbase="trackingtreer"),
'SingleElectron2017E': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_2017/240514_101200", 115, fnbase="trackingtreer"),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV2_Lepm_2017/240514_101256", 148, fnbase="trackingtreer"),

# 'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240515_093233", 29, fnbase="trackingtreer"),
# 'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101104", 9, fnbase="trackingtreer"),
# 'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101204", 9, fnbase="trackingtreer"),
# 'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101308", 11, fnbase="trackingtreer"),
# 'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101407", 7, fnbase="trackingtreer"),
# 'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101505", 6, fnbase="trackingtreer"),
# 'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101603", 7, fnbase="trackingtreer"),
# 'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_101702", 3, fnbase="trackingtreer"),
# 'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_101757", 10, fnbase="trackingtreer"),
# 'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_101856", 17, fnbase="trackingtreer"),
# 'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_101957", 17, fnbase="trackingtreer"),
# 'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_102057", 24, fnbase="trackingtreer"),
# 'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_102159", 25, fnbase="trackingtreer"),
# 'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_2018/240501_102259", 24, fnbase="trackingtreer"),
# 'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_102356", 2, fnbase="trackingtreer"),
# 'ttbar_lep_2018': (147, ['/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2018/240501_102456/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,6), xrange(7,14), xrange(15,31), xrange(32,65), xrange(66,77), xrange(78,96), xrange(97,107), xrange(108,122), xrange(123,142), xrange(143, 157))]), #entered by hand. may contain mistakes

# 'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2018/240501_102556", 508, fnbase="trackingtreer"),
# 'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_2018/240501_102656", 364, fnbase="trackingtreer"),
# 'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2018/240501_103605", 52, fnbase="trackingtreer"),
# 'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2018/240501_103703", 59, fnbase="trackingtreer"),
# 'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2018/240501_103802", 59, fnbase="trackingtreer"),
# 'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_103907", 15, fnbase="trackingtreer"),
# 'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_104005", 13, fnbase="trackingtreer"),
# 'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2018/240501_104105", 3, fnbase="trackingtreer"),
# 'SingleMuon2018A': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2018/240501_102756", 112, fnbase="trackingtreer"),
# 'SingleMuon2018B': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2018/240501_102855", 51, fnbase="trackingtreer"),
# 'SingleMuon2018C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2018/240501_102954", 52, fnbase="trackingtreer"),
# 'SingleMuon2018D': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV2_Lepm_2018/240501_103056", 223, fnbase="trackingtreer"),
# 'EGamma2018A': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV2_Lepm_2018/240501_103156", 163, fnbase="trackingtreer"),
# 'EGamma2018B': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV2_Lepm_2018/240501_103254", 72, fnbase="trackingtreer"),
# 'EGamma2018C': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV2_Lepm_2018/240501_103352", 71, fnbase="trackingtreer"),
# 'EGamma2018D': _fromnum1("/store/user/awarden/EGamma/TrackingTreerULV2_Lepm_2018/240501_103457", 324, fnbase="trackingtreer"),

})

##for track mover : 
# _add_ds("trackmovermctruthulv12lepmv6", {
# 'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV12Lepmv6_2018/250218_085118", 201),
# 'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV12Lepmv6_2018/250218_085425", 201),
# 'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV12Lepmv6_2018/250218_085634", 201),
# 'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV12Lepmv6_2018/250218_085803", 201),
# })

# _add_ds("trackmovermctruthulv13lepmv6", {
# 'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250430_203740", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_074310", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_205811", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_205955", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_210138", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250507_092818", 100, fnbase="mctruth"),
# 'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_075018", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250430_203923", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_074455", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_210507", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_210747", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_210931", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_211153", 101, fnbase="mctruth"),
# 'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_075204", 201, fnbase="mctruth"),
# 'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250430_204107", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_074642", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_211339", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_211525", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_211713", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_211859", 101, fnbase="mctruth"),
# 'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_074831", 201, fnbase="mctruth"),
# 'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250430_204250", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_212046", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_212230", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_212414", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_212558", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV13Lepmv6_2018/250505_212741", 101, fnbase="mctruth"),
# })

_add_ds("trackmoverulv14lepm1jet1lep", {
'ttbar_lep_2018': _fromnum0("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV14Lepm1jet1lep_2018/250526_092417", 6, fnbase="movedtree"),
'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV14Lepm1jet1lep_2018/250526_092554", 21, fnbase="movedtree"),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackMoverULV14Lepm1jet1lep_2018/250526_092821", 17, fnbase="movedtree"),
})
_add_ds("trackmovermctruthulv14lepmv6", {
# 'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_093710", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_093529", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_093848", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094025", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094205", 201, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094342", 100, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094520", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094702", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_094853", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095032", 101, fnbase="mctruth"),
# 'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095214", 101, fnbase="mctruth"),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095530", 201, fnbase="mctruth"),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095353", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095727", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_095933", 201, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100110", 201, fnbase="mctruth"),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100247", 101, fnbase="mctruth"),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100424", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100612", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100753", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_100931", 101, fnbase="mctruth"),
# 'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/TrackMoverMCTruthULV14Lepmv6_2018/250526_101113", 101, fnbase="mctruth"),
})

################################################################################

if __name__ == '__main__':
    import sys, re

    def _printlist(l):
        for x in l:
            print x

    def _args(x, *names):
        n = len(names)
        i = sys.argv.index(x)
        if len(sys.argv) < i+n+1 or sys.argv[i+1] in ('-h','--help','help'):
            sys.exit('usage: %s %s %s' % (sys.argv[0], x, ' '.join(names)))
        return tuple(sys.argv[i+j] for j in xrange(1,n+1))
    def _arg(x,name):
        return _args(x,name)[0]

    if 'enc' in sys.argv:
        dataset, sample, listfn = _args('enc', 'dataset','sample','listfn')
        fns = [x.strip() for x in open(listfn).read().split('\n') if x.strip()]
        n = len(fns)
        print '# %s, %s, %i files' % (sample, dataset, n)
        print '_add(%r)' % _enc({(sample,dataset):(n,fns)})

    elif 'testfiles' in sys.argv:
        dataset, sample = _args('testfiles', 'dataset','sample')
        is_ntuple = dataset.startswith('ntuple')
        from JMTucker.Tools.ROOTTools import ROOT
        print sample, dataset
        nev, nev2 = 0, 0
        def get_n(f,p):
            try:
                return f.Get(p).GetEntries()
            except ReferenceError:
                return 1e99
        for fn in get(sample, dataset)[1]:
            n = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn), 'Events')
            nev += n
            if is_ntuple:
                n2 = get_n(ROOT.TFile.Open('root://cmseos.fnal.gov/' + fn.replace('ntuple', 'vertex_histos')), 'mfvVertices/h_n_all_tracks')
                nev2 += n2
                print fn, n, n2
            else:
                print fn, n
        print 'total:', nev, 'events',
        if is_ntuple:
            print nev2, 'in vertex_histos h_n_all_tracks',
        print

    elif 'forcopy' in sys.argv:
        dataset, sample = _args('forcopy', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('copy\n')
        for fn in get(sample, dataset)[1]:
            md5sum = eos.md5sum(fn)
            x = '%s  %s\n' % (md5sum, fn)
            out_f.write(x)
            print x,
        out_f.close()

    elif 'fordelete' in sys.argv:
        dataset, sample = _args('fordelete', 'dataset','sample')
        if not has(sample, dataset):
            raise KeyError('no key sample = %s dataset = %s' % (sample, dataset))
        print sample, dataset
        from JMTucker.Tools import eos
        out_fn = '%s_%s' % (sample, dataset)
        out_f = open(out_fn, 'wt')
        out_f.write('delete\n%s\n' % '\n'.join(get(sample, dataset)[1]))
        out_f.close()

    elif 'dump' in sys.argv:
        dump()

    elif 'summary' in sys.argv:
        summary()

    elif 'datasets' in sys.argv:
        _printlist(sorted(set(ds for _, ds in _d.keys())))

    elif 'samples' in sys.argv:
        _printlist(sorted(set(name for name, ds in _d.keys() if ds == _arg('samples', 'dataset'))))

    elif 'files' in sys.argv:
        dataset, sample = _args('files', 'dataset','sample')
        _printlist(sorted(get(sample, dataset)[1]))

    elif 'allfiles' in sys.argv:
        _printlist(sorted(allfiles()))

    elif 'otherfiles' in sys.argv:
        list_fn = _arg('otherfiles', 'list_fn')
        other_fns = set()
        for line in open(list_fn):
            line = line.strip()
            if line.endswith('.root'):
                assert '/store' in line
                other_fns.add(line.replace('/eos/uscms', ''))
        all_fns = set(allfiles())
        print 'root files in %s not in SampleFiles:' % list_fn
        _printlist(sorted(other_fns - all_fns))
        print 'root files in SampleFiles not in %s:' % list_fn
        _printlist(sorted(all_fns - other_fns))

    elif 'filematch' in sys.argv:
        pattern = _arg('filematch', 'pattern')
        for (sample, dataset), (_, fns) in _d.iteritems():
            for fn in fns:
                if fnmatch(fn, pattern):
                    print sample, dataset, fn

    elif 'dirs' in sys.argv:
        dataset, sample = _args('dirs', 'dataset','sample')
        fns = get(sample, dataset)[1]
        path_re = re.compile(r'(/store.*/\d{6}_\d{6})/')
        _printlist(sorted(set(path_re.search(fn).group(1) for fn in fns)))
        # for x in ttbar qcdht0700 qcdht1000 qcdht1500 qcdht2000 wjetstolnu dyjetstollM10 dyjetstollM50 qcdmupt15 ; echo $x $(eosdu $(samplefiles dirs  ntuplev18m ${x}_2017) )

    elif 'whosummary' in sys.argv:
        whosummary = defaultdict(list)
        for k in _d:
            users = who(*k)
            if users:
                whosummary[users].append(k)
        print 'by user(s):'
        for users, dses in whosummary.iteritems():
            dses.sort()
            print ' + '.join(users)
            for ds in dses:
                print '    ', ds

    elif 'who' in sys.argv:
        dataset, sample = _args('who', 'dataset','sample')
        print ' + '.join(who(sample, dataset))

    elif 'sync' in sys.argv:
        from JMTucker.Tools import Samples
        in_sf_not_s = []
        in_s_not_sf = []

        for k in _d.iterkeys():
            name, ds = k
            if not hasattr(Samples, name) or not getattr(Samples, name).has_dataset(ds):
                in_sf_not_s.append(k)

        for s in Samples.registry.all():
            for ds in s.datasets:
                k = s.name, ds
                if not _d.has_key(k):
                    in_s_not_sf.append(k)

        print '%-45s %25s %10s' % ('in SampleFiles but not Samples:', '', 'enced?')
        for k in sorted(in_sf_not_s):
            name, ds = k
            print '%-45s %25s %10i' % (name, ds, _added_from_enc.get(k, -1))
        print
        print '%-45s %25s' % ('in Samples but not SampleFiles:', '')
        for k in sorted(in_s_not_sf):
            print '%-45s %25s' % k

    elif 'removed' in sys.argv:
        import colors
        def ok(fn):
            assert fn.startswith('/store') and fn.endswith('.root')
            ret = os.system('xrdcp -sf root://cmsxrootd-site.fnal.gov/%s /dev/null' % fn)
            if ret != 0:
                ret = os.system('xrdcp -sf root://cmseos.fnal.gov/%s /dev/null' % fn)
            return ret == 0
        print colors.boldred('red means the file is OK,'), colors.green('green means it should stay in the removed list')
        for name, ds, fns in _removed:
            for fn in fns:
                print (colors.boldred if ok(fn) else colors.green)('%s %s %s' % (name, ds, fn))

    else:
        if not (len(sys.argv) == 1 and sys.argv[0].endswith('/SampleFiles.py')):
            sys.exit('did not understand argv %r' % sys.argv)
