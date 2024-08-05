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
    #print(_d.keys())
    fns = _d[(name, ds)][1]
    if num > 0:
        #test: trying [15:num+15] because having issues only at a particular ntuple; want to investigate PLEASE CHANGE back to [:num]
        #fns = fns[15:num+15]
        fns = fns[:num]
    #return [('root://cmseos.fnal.gov/' + fn) if fn.startswith('/store/user') else fn for fn in fns]
    return [('root://cmsxrootd.hep.wisc.edu/' + fn) if fn.startswith('/store/user') else fn for fn in fns]

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

_add_ds("miniaod", {
    'qcdmupt15_2017': (1, ['/store/mc/RunIISummer20UL17MiniAOD/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/100000/034AE4F2-7180-7F40-81D6-740D15738CBA.root'])
})

_add_ds("miniaod",{
    'qcdmupt15_20161': (1, ['/store/mc/RunIISummer20UL16MiniAODAPVv2/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/2430000/07BCE353-B2FE-7A4A-B700-CB56348CBE18.root'])
})


_add_ds("miniaod", {
    'mfv_stoplb_tau000300um_M0800_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/30000/1140EC5A-A7C4-794C-9557-D64D8D5AFFC1.root'])
})

_add_ds("miniaod", {
    'mfv_stoplb_tau000300um_M0300_2018' : (1, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/0EB41A7B-C4C5-8840-9C29-10249902A9DB.root'])
})

# _add_ds("miniaod", {
#     'mfv_stopld_tau010000um_M0800_2018' : (3, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/181536B9-11E5-2344-9E8E-BACCD7482A0A.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/21602664-E4E1-3E48-A244-2D131F063685.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/27A92C07-345E-1B48-98D9-F1C966151362.root'])
# })

_add_ds("miniaod", {
    'mfv_stopld_tau010000um_M0800_2018' : (2, ['/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/21602664-E4E1-3E48-A244-2D131F063685.root', '/store/mc/RunIISummer20UL18MiniAODv2/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/40000/27A92C07-345E-1B48-98D9-F1C966151362.root'])
})


_add_ds("miniaod", {
    'ttbar_semilep_2018' : (3, ['/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/016D5B69-2F13-A94D-8A61-91551911BFBD.root',
                                '/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/01292B43-5A7A-164B-92B7-292369F64D70.root',
                                '/store/mc/RunIISummer20UL18MiniAODv2/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/120000/0120869B-F7FD-C24C-A083-924B2F01BB88.root'
                                ])
})

_add_ds("ntupleulv9lepm", {
    'test' : (1, ['file:/afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/MFVNeutralino/test/ntuple.root'])
 })


# _add_ds("miniaod", {
#     'mfv_stopld_tau000100um_M0200_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074408/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000300um_M0200_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074523/0000", 10, fnbase="MiniAOD", numbereddirs=False),
#     #'mfv_stopld_tau000100um_M0600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074432/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000300um_M0600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074542/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000100um_M1000_2018':_fromnum2("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074449/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000300um_M1000_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074558/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau001000um_M1000_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_073950/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000100um_M1600_2018':_fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074506/0000", 5, fnbase="MiniAOD", numbereddirs=False),
#     'mfv_stopld_tau000300um_M1600_2018':_fromnum2("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/RunIISummer20UL18_MiniAOD/220518_074615/0000", 5, fnbase="MiniAOD", numbereddirs=False),
# })

# private samples 
# _add_ds("ntupleulv1lepm", {
# 'mfv_stopld_tau000100um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063334", 21),
# 'mfv_stopld_tau000300um_M0200_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063335", 21),
# 'mfv_stopld_tau000100um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063336", 15),
# 'mfv_stopld_tau000300um_M0600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063337", 15),
# 'mfv_stopld_tau000100um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093252", 11),
# 'mfv_stopld_tau000300um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063339", 14),
# 'mfv_stopld_tau001000um_M1000_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063340", 13),
# 'mfv_stopld_tau000100um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_063341", 12),
# 'mfv_stopld_tau000300um_M1600_2018': _fromnum0("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-pythia8/NtupleULV1Lepm_2018/220523_093256", 10),
# })


#TrackingTreer with good lepton sel tracks + tracks matched to good leptons; event filter and trigger filter were applied
_add_ds("trackingtreerulv1_lepm_wsellep", {
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094341", 35, fnbase="trackingtreer"),
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094356", 142, fnbase="trackingtreer"),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094410", 103, fnbase="trackingtreer"),
'qcdempt030_2017': (33, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094427/0000/trackingtreer_%i.root' % i for i in chain(xrange(3,35), [1])]),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094441", 38, fnbase="trackingtreer"),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094456", 34, fnbase="trackingtreer"),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094511", 41, fnbase="trackingtreer"),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094527", 25, fnbase="trackingtreer"),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094543", 17, fnbase="trackingtreer"),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094558", 51, fnbase="trackingtreer"),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094613", 48, fnbase="trackingtreer"),
'qcdbctoept080_2017': (33, ['/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094629/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,5), xrange(6,35))]),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094645", 46, fnbase="trackingtreer"),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094700", 32, fnbase="trackingtreer"),
'wjetstolnu_2017': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094805", 106, fnbase="trackingtreer"),
'dyjetstollM10_2017': (93, ['/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094821/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,10), xrange(11,63), xrange(64,96))]),
'dyjetstollM50_2017': (60, ['/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094836/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,7), xrange(9,17), xrange(18,23), xrange(24,35), xrange(36,41), xrange(44,52), xrange(53,55), xrange(60,67), xrange(68,72), [42, 56, 58, 74])]),
'ttbar_2017': (254, ['/store/user/awarden/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_123503/0000/trackingtreer_%i.root' % i for i in chain(xrange(106), xrange(107,255))]),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094852", 21, fnbase="trackingtreer"),
'zz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094908", 13, fnbase="trackingtreer"),
'wz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV1_Lepm_wsellep_2017/221004_094923", 14, fnbase="trackingtreer"),
'SingleMuon2017B': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044926", 60, fnbase="trackingtreer"),
'SingleMuon2017C': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_094716", 78, fnbase="trackingtreer"),
'SingleMuon2017D': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044927", 34, fnbase="trackingtreer"),
'SingleMuon2017E': _fromnum0("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_044928", 86, fnbase="trackingtreer"),
'SingleMuon2017F': _fromnum1("/store/user/awarden/SingleMuon/TrackingTreerULV1_Lepm_wsellep_2017/221004_094732", 109, fnbase="trackingtreer"),
'SingleElectron2017B': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044929", 32, fnbase="trackingtreer"),
'SingleElectron2017C': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044930", 64, fnbase="trackingtreer"),
'SingleElectron2017D': _fromnum0("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044931", 25, fnbase="trackingtreer"),
'SingleElectron2017E': (59, ['/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_044932/0000/trackingtreer_%i.root' % i for i in chain(xrange(9), xrange(10,60))]),
'SingleElectron2017F': _fromnum1("/store/user/awarden/SingleElectron/TrackingTreerULV1_Lepm_wsellep_2017/221004_094749", 89, fnbase="trackingtreer"),
})


## ntuple v9 : relax min_r = 2, but with lost hits = 1 (recover tracks going through the dead pixel layer) & all the lepton changes thus far and Peace's vertexer 
## which uses sigmaz in the deltaz stage - no special consideration for leptons. also pt ordering for seed tracks & seed vertices 
_add_ds("ntupleulv9lepm", {
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_085903", 29),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090006", 14),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090109", 17),
'qcdempt030_2018': (14, ['/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090210/0000/ntuple_%i.root' % i for i in chain(xrange(1,7), xrange(8,16))]),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090312", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090417", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090546", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_090650", 5),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_090754", 19),
'qcdbctoept020_2018': (31, ['/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_090856/0000/ntuple_%i.root' % i for i in chain(xrange(1,14), xrange(15,33))]),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_091002", 28),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_091106", 41),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_091207", 44),
'qcdbctoept250_2018': (42, ['/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV9Lepm_2018/240413_091309/0000/ntuple_%i.root' % i for i in chain(xrange(1,38), xrange(39,44))]),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_091412", 4),
# 'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240413_091515", 310),
# 'ttbar_semilep_2018': (1005, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240413_091619' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,32), xrange(33,42), xrange(43,81), xrange(82,97), xrange(98,167), xrange(168,1011))]),
#'ttbar_had_2018': (720, ['/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240413_091721/0000/ntuple_%i.root' % i for i in chain(xrange(1,619), xrange(620,648), xrange(649,660), xrange(661,724))]),
#'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240504_082822", 310),
#'ttbar_semilep_2018': (1005, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240504_082930' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,540), xrange(541,553), xrange(554,734), xrange(735,1009))]),
#'ttbar_had_2018': (720, ['/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_2018/240504_083032/0000/ntuple_%i.root' % i for i in chain(xrange(1,611), xrange(612,676), xrange(678,724))]),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Lepm_2018/240413_110651", 99),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Lepm_2018/240413_110755", 114),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV9Lepm_2018/240413_110859", 110),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_111003", 23),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_111109", 17),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV9Lepm_2018/240413_111216", 5),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_091827", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_091935", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092037", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092144", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092250", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092354", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092456", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092559", 200),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092706", 201),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092815", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_092917", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093020", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093123", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093225", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093329", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093432", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093534", 200),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093636", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093739", 201),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093843", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_093945", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094048", 200),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094152", 201),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094255", 100),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094358", 201),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094500", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094602", 201),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094705", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094810", 101),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_094914", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095016", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095120", 201),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095223", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095325", 101),
'mfv_stoplb_tau030000um_M1200_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095428/0000/ntuple_%i.root' % i for i in chain(xrange(1,71), xrange(72,81), xrange(82,202))]),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095531", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095634", 201),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095737", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095843", 101),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_095946", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100048", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100152", 201),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100257", 101),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100401", 101),
'mfv_stoplb_tau030000um_M1600_2018': (100, ['/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100504/0000/ntuple_%i.root' % i for i in chain(xrange(1,71), xrange(72,102))]),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100610", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100712", 201),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100815", 101),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_100919", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101022", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101124", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101228", 201),
'mfv_stopld_tau001000um_M0200_2018': (199, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101332/0000/ntuple_%i.root' % i for i in chain(xrange(1,102), xrange(103,106), xrange(107,202))]),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101437", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101540", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101642", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101745", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101850", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_101953", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102058", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102202", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102306", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102410", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102513", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102618", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_102931", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103034", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103138", 200),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103242", 201),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103346", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103449", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103600", 201),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103702", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103804", 101),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_103909", 201),
'mfv_stopld_tau000100um_M1000_2018': (200, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104013/0000/ntuple_%i.root' % i for i in chain(xrange(1,107), xrange(108,202))]),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104116", 201),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104220", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104323", 101),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104427", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104531", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104633", 201),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104737", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104840", 101),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_104941", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105043", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105147", 200),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105249", 201),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105355", 101),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105459", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105602", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105705", 201),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105809", 101),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_105912", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110020", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110129", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110234", 201),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110340", 101),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110444", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV9Lepm_2018/240413_110547", 101),
})

_add_ds("ntupleulv9lepm_wgen", {
'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_WGen_2018/240505_141029", 310),
'ttbar_semilep_2018': (1004, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_WGen_2018/240505_141134' + '/%04i/ntuple_%i.root' % (i/1000,i) for i in chain(xrange(1,39), xrange(40,796), xrange(797,873), xrange(874,890), xrange(891,1009))]),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV9Lepm_WGen_2018/240505_141249", 723),
})

_add_ds("ntupleulv10lepm_wgen", {
'qcdempt015_2017': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115135", 10),
'qcdmupt15_2017': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115244", 32),
'qcdempt020_2017': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115352", 20),
'qcdempt030_2017': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115501", 9),
'qcdempt050_2017': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115609", 18),
'qcdempt080_2017': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115716", 22),
'qcdempt120_2017': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115824", 24),
'qcdempt170_2017': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_115937", 7),
'qcdempt300_2017': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_120045", 5),
'qcdbctoept015_2017': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2017/240522_120153", 39),
'qcdbctoept020_2017': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2017/240522_120305", 30),
'qcdbctoept030_2017': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2017/240522_120412", 30),
'qcdbctoept170_2017': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2017/240522_120626", 28),
'qcdbctoept250_2017': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2017/240522_120733", 24),
'ttbar_lep_2017': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2017/240522_120841", 136),
'ttbar_semilep_2017': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2017/240522_120957", 436),
'ttbar_had_2017': (182, ['/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2017/240717_140955/0000/ntuple_%i.root' % i for i in chain(xrange(1,6), xrange(7,12), xrange(15,21), xrange(24,26), xrange(27,30), xrange(31,42), xrange(43,45), xrange(47,49), xrange(50,57), xrange(58,64), xrange(65,67), xrange(68,70), xrange(72,85), xrange(87,89), xrange(90,93), xrange(95,109), xrange(111,116), xrange(117,121), xrange(122,137), xrange(138,141), xrange(146,148), xrange(154,156), xrange(157,160), xrange(161,166), xrange(167,172), xrange(173,180), xrange(181,186), xrange(187,191), xrange(199,201), xrange(207,209), xrange(231,233), xrange(253,255), xrange(270,272), xrange(275,279), xrange(281,285), xrange(286,288), xrange(291,294), [13, 22, 149, 193, 203, 214, 218, 241, 250, 256, 268, 289, 295, 299])]),
'wjetstolnu_2017': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2017/240522_152255", 107),
'dyjetstollM10_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2017/240522_152732", 90),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2017/240522_152955", 129),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_153106", 23),
'zz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_153226", 4),
'wz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2017/240522_153403", 15),
'mfv_stoplb_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121235", 201),
'mfv_stoplb_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121345", 201),
'mfv_stoplb_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121454", 101),
'mfv_stoplb_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121602", 201),
'mfv_stoplb_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121710", 201),
'mfv_stoplb_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121819", 201),
'mfv_stoplb_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_121934", 200),
'mfv_stoplb_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122054", 101),
'mfv_stoplb_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122234", 201),
'mfv_stoplb_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122402", 201),
'mfv_stoplb_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122514", 201),
'mfv_stoplb_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122636", 201),
'mfv_stoplb_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122754", 101),
'mfv_stoplb_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_122905", 201),
'mfv_stoplb_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123057", 201),
'mfv_stoplb_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123243", 201),
'mfv_stoplb_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123411", 201),
'mfv_stoplb_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123526", 101),
'mfv_stoplb_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123639", 101),
'mfv_stoplb_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123750", 101),
'mfv_stoplb_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_123859", 201),
'mfv_stoplb_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124014", 201),
'mfv_stoplb_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124232", 101),
'mfv_stoplb_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124353", 101),
'mfv_stoplb_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124514", 101),
'mfv_stoplb_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124710", 201),
'mfv_stoplb_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_124930", 201),
'mfv_stoplb_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125100", 201),
'mfv_stoplb_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125212", 199),
'mfv_stoplb_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125323", 201),
'mfv_stoplb_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125438", 201),
'mfv_stoplb_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125546", 200),
'mfv_stoplb_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125659", 201),
'mfv_stoplb_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125811", 201),
'mfv_stoplb_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_125920", 201),
'mfv_stoplb_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130035", 201),
'mfv_stoplb_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130150", 201),
'mfv_stoplb_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130303", 201),
'mfv_stoplb_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130421", 201),
'mfv_stoplb_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130528", 201),
'mfv_stoplb_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130643", 201),
'mfv_stoplb_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_130819", 201),
'mfv_stoplb_tau010000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_131004", 201),
'mfv_stoplb_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_131220", 201),
'mfv_stoplb_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_131417", 201),
'mfv_stoplb_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_131803", 201),
'mfv_stoplb_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_131931", 201),
'mfv_stoplb_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_132055", 101),
'mfv_stoplb_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_132218", 201),
'mfv_stoplb_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_132342", 201),
'mfv_stopld_tau000100um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_132704", 201),
'mfv_stopld_tau000300um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133002", 201),
'mfv_stopld_tau010000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133202", 101),
'mfv_stopld_tau001000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133343", 201),
#'mfv_stopld_tau030000um_M1000_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133614", 201),
'mfv_stopld_tau030000um_M1000_2017': (199, ["/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133614/0000/ntuple_%i.root" % i for i in chain(xrange(1,46), xrange(47,201))]),
'mfv_stopld_tau000100um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_133757", 201),
'mfv_stopld_tau000300um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134103", 201),
'mfv_stopld_tau010000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134242", 101),
'mfv_stopld_tau001000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134351", 201),
'mfv_stopld_tau030000um_M1200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134506", 201),
'mfv_stopld_tau000100um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134622", 201),
'mfv_stopld_tau000300um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_134835", 201),
'mfv_stopld_tau010000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_135141", 101),
'mfv_stopld_tau001000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_135407", 201),
'mfv_stopld_tau030000um_M1400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_135606", 201),
'mfv_stopld_tau000100um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_135717", 201),
'mfv_stopld_tau000300um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_135853", 201),
'mfv_stopld_tau010000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140006", 101),
'mfv_stopld_tau001000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140125", 101),
'mfv_stopld_tau030000um_M1600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140240", 101),
'mfv_stopld_tau000100um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140410", 200),
'mfv_stopld_tau000300um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140526", 201),
'mfv_stopld_tau010000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140658", 101),
'mfv_stopld_tau001000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140830", 101),
'mfv_stopld_tau030000um_M1800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_140953", 101),
'mfv_stopld_tau000100um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141118", 201),
'mfv_stopld_tau000300um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141235", 201),
'mfv_stopld_tau010000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141359", 200),
'mfv_stopld_tau001000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141513", 201),
'mfv_stopld_tau030000um_M0200_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141633", 201),
'mfv_stopld_tau000100um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_141817", 201),
'mfv_stopld_tau000300um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_142022", 201),
'mfv_stopld_tau010000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_142219", 201),
'mfv_stopld_tau001000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_142501", 201),
'mfv_stopld_tau030000um_M0300_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_142820", 201),
'mfv_stopld_tau000100um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_142958", 201),
'mfv_stopld_tau000300um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_143138", 201),
'mfv_stopld_tau010000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_143259", 201),
'mfv_stopld_tau001000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_143432", 199),
'mfv_stopld_tau030000um_M0400_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_143653", 201),
'mfv_stopld_tau000100um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_144037", 201),
'mfv_stopld_tau000300um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_144613", 200),
'mfv_stopld_tau010000um_M0600_2017': (40, ['/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240717_141614/0000/ntuple_%i.root' % i for i in chain(xrange(2,4), xrange(10,12), xrange(29,31), xrange(44,46), xrange(60,62), xrange(70,72), xrange(74,76), xrange(90,92), xrange(114,116), xrange(123,125), xrange(133,135), [20, 41, 82, 86, 98, 107, 121, 144, 147, 153, 156, 159, 162, 173, 186, 189, 192, 194])]),
'mfv_stopld_tau001000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_145810", 201),
'mfv_stopld_tau030000um_M0600_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_150020", 201),
'mfv_stopld_tau000100um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_150214", 201),
'mfv_stopld_tau000300um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_150538", 201),
'mfv_stopld_tau010000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_150950", 101),
'mfv_stopld_tau001000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_151442", 201),
'mfv_stopld_tau030000um_M0800_2017': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2017/240522_151648", 201),
'qcdmupt15_2018': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_150356", 29),
'qcdempt015_2018': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_150516", 13),
'qcdempt020_2018': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_150638", 17),
'qcdempt030_2018': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_150753", 15),
'qcdempt050_2018': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_150916", 14),
'qcdempt080_2018': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_151033", 12),
'qcdempt120_2018': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_151256", 14),
'qcdempt170_2018': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_151507", 5),
'qcdbctoept015_2018': _fromnum1("/store/user/awarden/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_151707", 19),
'qcdbctoept020_2018': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_151921", 31),
'qcdbctoept030_2018': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_152130", 28),
'qcdbctoept080_2018': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_152351", 41),
'qcdbctoept170_2018': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_152554", 44),
'qcdbctoept250_2018': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/NtupleULV10Lepm_WGen_2018/240517_152729", 43),
'qcdempt300_2018': _fromnum1("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_152850", 4),
'ttbar_lep_2018': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2018/240517_153005", 310),
'ttbar_semilep_2018': _fromnum1("/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2018/240517_153124", 1008),
'ttbar_had_2018': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/NtupleULV10Lepm_WGen_2018/240517_153239", 723),
'wjetstolnu_2018': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2018/240517_174622", 99),
'wjetstolnu_ext_2018': (200, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2018/240620_173654/0000/ntuple_%i.root' % i for i in chain(xrange(1,60), xrange(61,106), xrange(107,203))]),
'dyjetstollM10_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2018/240517_174738", 114),
'dyjetstollM50_2018': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NtupleULV10Lepm_WGen_2018/240517_174849", 110),
'ww_2018': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_174958", 23),
'wz_2018': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_175106", 17),
'zz_2018': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/NtupleULV10Lepm_WGen_2018/240517_175216", 5),
'mfv_stoplb_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_153401", 201),
'mfv_stoplb_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_153528", 201),
'mfv_stoplb_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_153650", 201),
'mfv_stoplb_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_153806", 201),
'mfv_stoplb_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_153928", 201),
'mfv_stoplb_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_154047", 201),
'mfv_stoplb_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_154205", 201),
'mfv_stoplb_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_154453", 200),
'mfv_stoplb_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_154734", 201),
'mfv_stoplb_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_154941", 201),
'mfv_stoplb_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155108", 201),
'mfv_stoplb_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155225", 201),
'mfv_stoplb_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155352", 201),
'mfv_stoplb_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155519", 201),
'mfv_stoplb_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155635", 200),
'mfv_stoplb_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155756", 201),
'mfv_stoplb_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_155915", 200),
'mfv_stoplb_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160029", 200),
'mfv_stoplb_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160151", 201),
'mfv_stoplb_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160322", 200),
'mfv_stoplb_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160440", 200),
'mfv_stoplb_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160606", 200),
'mfv_stoplb_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160740", 201),
'mfv_stoplb_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_160855", 100),
'mfv_stoplb_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161017", 201),
'mfv_stoplb_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161135", 201),
'mfv_stoplb_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161255", 201),
'mfv_stoplb_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161410", 201),
'mfv_stoplb_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161533", 101),
'mfv_stoplb_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161650", 201),
'mfv_stoplb_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161817", 201),
'mfv_stoplb_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_161940", 201),
'mfv_stoplb_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162104", 201),
'mfv_stoplb_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162224", 101),
'mfv_stoplb_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162345", 201),
'mfv_stoplb_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162509", 201),
'mfv_stoplb_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162633", 201),
'mfv_stoplb_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162756", 201),
'mfv_stoplb_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_162910", 101),
'mfv_stoplb_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163027", 200),
'mfv_stoplb_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163142", 201),
'mfv_stoplb_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163300", 201),
'mfv_stoplb_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163417", 101),
'mfv_stoplb_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163536", 101),
'mfv_stoplb_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163659", 101),
'mfv_stoplb_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163820", 200),
'mfv_stoplb_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_163934", 201),
'mfv_stoplb_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164046", 101),
'mfv_stoplb_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164157", 101),
'mfv_stoplb_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLBottom_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164310", 101),
'mfv_stopld_tau000100um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164422", 201),
'mfv_stopld_tau000300um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164541", 201),
'mfv_stopld_tau001000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164652", 201),
'mfv_stopld_tau010000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_164926", 201),
'mfv_stopld_tau030000um_M0200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165041", 201),
'mfv_stopld_tau000100um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165150", 201),
'mfv_stopld_tau000300um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165306", 201),
'mfv_stopld_tau001000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165416", 201),
'mfv_stopld_tau010000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165531", 201),
'mfv_stopld_tau030000um_M0300_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_300_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165644", 201),
'mfv_stopld_tau000100um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165755", 201),
'mfv_stopld_tau000300um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_165905", 201),
'mfv_stopld_tau001000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170016", 201),
'mfv_stopld_tau010000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170125", 201),
'mfv_stopld_tau030000um_M0400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170238", 201),
'mfv_stopld_tau000100um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170357", 201),
'mfv_stopld_tau000300um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170507", 201),
'mfv_stopld_tau001000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170625", 200),
'mfv_stopld_tau010000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170742", 201),
'mfv_stopld_tau030000um_M0600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_170853", 201),
'mfv_stopld_tau000100um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171003", 200),
'mfv_stopld_tau000300um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171117", 201),
'mfv_stopld_tau001000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171231", 201),
'mfv_stopld_tau010000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171339", 101),
'mfv_stopld_tau030000um_M0800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171455", 201),
'mfv_stopld_tau000100um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171613", 201),
'mfv_stopld_tau000300um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171722", 201),
'mfv_stopld_tau001000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171837", 201),
'mfv_stopld_tau010000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_171949", 101),
'mfv_stopld_tau030000um_M1000_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1000_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172100", 201),
'mfv_stopld_tau000100um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172212", 201),
'mfv_stopld_tau000300um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172324", 201),
'mfv_stopld_tau001000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172438", 201),
'mfv_stopld_tau010000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172554", 101),
'mfv_stopld_tau030000um_M1200_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1200_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172708", 201),
'mfv_stopld_tau000100um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172821", 201),
'mfv_stopld_tau000300um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_172931", 200),
'mfv_stopld_tau001000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173045", 201),
'mfv_stopld_tau010000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173158", 101),
'mfv_stopld_tau030000um_M1400_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1400_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173310", 201),
'mfv_stopld_tau000100um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173427", 201),
'mfv_stopld_tau000300um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173544", 201),
'mfv_stopld_tau001000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173657", 101),
'mfv_stopld_tau010000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173807", 101),
'mfv_stopld_tau030000um_M1600_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1600_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_173916", 100),
'mfv_stopld_tau000100um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_174025", 201),
'mfv_stopld_tau000300um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_0p3mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_174138", 201),
'mfv_stopld_tau001000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_1mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_174247", 101),
'mfv_stopld_tau010000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_10mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_174358", 101),
'mfv_stopld_tau030000um_M1800_2018': _fromnum1("/store/user/awarden/DisplacedSUSY_stopToLD_M_1800_30mm_TuneCP5_13TeV-madgraph-pythia8/NtupleULV10Lepm_WGen_2018/240517_174507", 101),
})
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


#TrackingTreer 2018 

_add_ds("trackingtreerulv2_lepm", {
# 'qcdempt015_20161': _fromnum1("/store/user/awarden/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171542", 32, fnbase="trackingtreer"),
# 'qcdmupt15_20161': _fromnum1("/store/user/awarden/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093128", 13, fnbase="trackingtreer"),
# 'qcdempt020_20161': _fromnum1("/store/user/awarden/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171748", 8, fnbase="trackingtreer"),
# 'qcdempt030_20161': _fromnum1("/store/user/awarden/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093230", 8, fnbase="trackingtreer"),
# 'qcdempt050_20161': _fromnum1("/store/user/awarden/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_171953", 8, fnbase="trackingtreer"),
# 'qcdempt080_20161': _fromnum1("/store/user/awarden/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172057", 8, fnbase="trackingtreer"),
# 'qcdempt120_20161': _fromnum1("/store/user/awarden/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172200", 10, fnbase="trackingtreer"),
# 'qcdempt170_20161': _fromnum1("/store/user/awarden/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_172303", 5, fnbase="trackingtreer"),
# 'qcdempt300_20161': _fromnum0("/store/user/awarden/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093352", 5, fnbase="trackingtreer"),
# 'qcdbctoept020_20161': _fromnum1("/store/user/awarden/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172508", 13, fnbase="trackingtreer"),
# 'qcdbctoept030_20161': _fromnum1("/store/user/awarden/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172613", 13, fnbase="trackingtreer"),
# 'qcdbctoept080_20161': _fromnum1("/store/user/awarden/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172720", 16, fnbase="trackingtreer"),
# 'qcdbctoept170_20161': _fromnum1("/store/user/awarden/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172821", 13, fnbase="trackingtreer"),
# 'qcdbctoept250_20161': _fromnum1("/store/user/awarden/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/TrackingTreerULV2_Lepm_20161/240803_172922", 16, fnbase="trackingtreer"),
# 'wjetstolnu_20161': (90, ['/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173333/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,13), xrange(14,17), xrange(18,62), xrange(63,85), xrange(86,95))]),
# 'dyjetstollM10_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173438", 33, fnbase="trackingtreer"),
# 'dyjetstollM50_20161': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_20161/240803_173540", 103, fnbase="trackingtreer"),
# 'ttbar_lep_20161': _fromnum1("/store/user/awarden/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173027", 66, fnbase="trackingtreer"),
# 'ttbar_semilep_20161': (201, ['/store/user/awarden/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173129/0000/trackingtreer_%i.root' % i for i in chain(xrange(1,135), xrange(136,181), xrange(182,193), xrange(194,205))]),
# 'ttbar_had_20161': _fromnum1("/store/user/awarden/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/TrackingTreerULV2_Lepm_20161/240803_173231", 153, fnbase="trackingtreer"),
# 'ww_20161': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240804_093522", 22, fnbase="trackingtreer"),
# 'zz_20161': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_173748", 5, fnbase="trackingtreer"),
# 'wz_20161': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_20161/240803_173850", 13, fnbase="trackingtreer"),
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
'wjetstolnu_2017': _fromnum1("/store/user/awarden/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101353", 107, fnbase="trackingtreer"),
'dyjetstollM10_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101449", 90, fnbase="trackingtreer"),
'dyjetstollM50_2017': _fromnum1("/store/user/awarden/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/TrackingTreerULV2_Lepm_2017/240514_101545", 129, fnbase="trackingtreer"),
'ww_2017': _fromnum1("/store/user/awarden/WW_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101647", 23, fnbase="trackingtreer"),
'zz_2017': _fromnum1("/store/user/awarden/ZZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101745", 4, fnbase="trackingtreer"),
'wz_2017': _fromnum1("/store/user/awarden/WZ_TuneCP5_13TeV-pythia8/TrackingTreerULV2_Lepm_2017/240514_101840", 15, fnbase="trackingtreer"),

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
