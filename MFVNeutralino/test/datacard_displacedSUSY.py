#original author : Ang Li 

#This script reads from ROOT files including BDT score distribution for SRs and CRs 
#and will convert those numbers into datacard for limit plot 
# Make sure to run this with env with ROOT 
import ROOT 
import pandas as pd 
import ctypes 
import math 
year = '2017'

#TODO : Get ABCDSystematics; below are from Ang
def getABCDSyst(year):
  #For BDT score = ; requiring leading lepton and isolation < 0.1
  s = {
    '20161': 0.090,
    '20162': 0.491,
    '2017': 0.058,
    '2018': 0.070,
  }

  return s[str(year)]

#TODO : get systematic sources in csv format; may be a mix of dependent and independent of signal model so keeping independent/dependent for now
# dm == decay mode
def getSystUncert(dm, year):
    '''
    This function retuns a dictionary that includes systematic sources
    '''
    csv_path = '/afs/hep.wisc.edu/home/acwarden/work/llp/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/sig_syst_unc.csv'
    df = pd.read_csv(csv_path, index_col=0)
    
    #source_dm_dependent = ["vtxreco", "BDT"] #TODO : determine vtxreco and BDT systematics 
    source_dm_independent = ["intlumi"] #TODO : trigger, l1 among others...?
    s = {}
    # for source in source_dm_dependent:
    #     s[source] = df[str(year)][source+'_'+str(dm)]
    for source in source_dm_independent:
        s[source] = df[str(year)][source]

    return s

def getNumEvents(fn, regions, SF=1, BDTcut=(-1,-1), useData=True):
    '''
    This function return a dictionary including:
        raw: raw number of events in the region
        weighted: weighted number of events in the region
        stat_uncert: statistical uncertainty of number of events in the region
    '''
    d = {
        'raw': [],
        'weighted': [],
        'stat_uncert': [],
    }
    f = ROOT.TFile(filepath+fn+'.root')
    print(f)
    for r in regions:
      h = f.Get(r+'/BDT_score')
      nevt_uncert = ctypes.c_double(0)
      #binH = 100000 if MLcut[1]==-1 else h.GetXaxis().FindBin(MLcut[1]) 
      #binL = 0 if MLcut[0]==-1 else h.GetXaxis().FindBin(MLcut[0]) 
      binL = 0
      binH = h.GetXaxis().FindBin(1.0)-1 #BDT score 0.974 or similar
      # binH = h.GetXaxis().FindBin(0.974)-1 #BDT score 0.974 or similar
      nevt = h.IntegralAndError(binL,binH,nevt_uncert)
      print(nevt)
      if nevt<=0:
        nevt = 0.000001
      #nevt = 1
      nevt_raw = h.GetEntries()
      if useData and (r=='highBDT_4tk'):
          d['raw'].append(0)
          d['weighted'].append(0)
          d['stat_uncert'].append(0.00)
      else:
          print("raw, weighted, stat uncert : ", nevt_raw, nevt*SF, nevt_uncert.value*SF)
          d['raw'].append(int(nevt_raw))
          d['weighted'].append(nevt*SF)
          d['stat_uncert'].append(nevt_uncert.value*SF)
    return d

def getNumEvents_multi(fna, fnb, regions, SF=1, BDTcut=(-1,-1), useData=True):
    '''
    This function return a dictionary including:
        raw: raw number of events in the region
        weighted: weighted number of events in the region
        stat_uncert: statistical uncertainty of number of events in the region
    '''
    d = {
        'raw': [],
        'weighted': [],
        'stat_uncert': [],
    }
    raw = 0
    weighted = 0
    stat_uncert = 0
    fa = ROOT.TFile(filepath+fna+'.root')
    fb = ROOT.TFile(filepath+fnb+'.root')
    files = [fa, fb]
    print(fa)
    for r in regions:
      for f in files :
        h = f.Get(r+'/BDT_score')
        nevt_uncert = ctypes.c_double(0)
        #binH = 100000 if MLcut[1]==-1 else h.GetXaxis().FindBin(MLcut[1]) 
        #binL = 0 if MLcut[0]==-1 else h.GetXaxis().FindBin(MLcut[0]) 
        binL = 0
        binH = h.GetXaxis().FindBin(1.0)-1 #BDT score 0.974 or similar
        # binH = h.GetXaxis().FindBin(0.974)-1 #BDT score 0.974 or similar
        nevt = h.IntegralAndError(binL,binH,nevt_uncert)
        print(nevt)
        if nevt<=0:
          nevt = 0.000001
        #nevt = 1
        nevt_raw = h.GetEntries()
        raw += int(nevt_raw)
        weighted += nevt*SF
        stat_uncert += nevt_uncert.value*SF
      
    
      d['raw'].append(raw)
      d['weighted'].append(weighted)
      d['stat_uncert'].append(stat_uncert)
    return d
  
def getYield(nevt):
  err = math.sqrt(nevt)
  lo_bound = int(round(max(0, nevt - 5*err)))
  hi_bound = int(round(nevt + 5*err))
  return "{} [{},{}]".format(nevt, lo_bound, hi_bound)

def getYield_multi(nevta, nevtb):
  nevt = nevta + nevtb
  err = math.sqrt(nevt)
  lo_bound = int(round(max(0, nevt - 5*err)))
  hi_bound = int(round(nevt + 5*err))
  return "{} [{},{}]".format(nevt, lo_bound, hi_bound)

template = '''
# Signal sample: _SIGNAL_
# Expected limit datacard for MC
imax _NCHANNELS_  number of channels
jmax 1  number of backgrounds
kmax _NUNCERT_  number of nuisance parameters (sources of systematic uncertainty)
------------
# adding treating datacard as if it were a shape-based model
shapes * * FAKE
------------
# Analysis channel and observed number of events
bin _CHANNELNAME_ 
observation _OBSERVATION_
------------
# now we list the expected number of events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
bin              _CHANNELNAMERATE_
process          _PROCESSNAMERATE_ 
process          _PROCESSIDXRATE_
rate             _PROCESSRATE_
----STATISTICAL UNCERTAINTIES-----
_STATUNCERTSIG_
_STATUNCERTBKG_
-----SYSTEMATIC UNCERTAINTIES----- 
_SYSTUNCERT_
_SYSTUNCERTSIG_
-----ABCD IMPLEMENTATION----- 
_ABCD_
'''

useData = False
channels = ['highBDT_4tk'+year, 'midBDT_4tk'+year, 'lowBDT_4tk'+year, 'highBDT_3tk'+year, 'midBDT_3tk'+year, 'lowBDT_3tk'+year]
dirs = ['highBDT_4tk', 'midBDT_4tk', 'lowBDT_4tk', 'highBDT_3tk', 'midBDT_3tk', 'lowBDT_3tk']
processes = ['signal','background']
processidx = ['0','1']
channelnamerate = ''
for _ in channels:
  channelnamerate += ('\t'+_)*len(processes)
processnamerate = ('\t'+'\t'.join(processes))*len(channels)
processidxrate = ('\t'+'\t'.join(processidx))*len(channels)


filepath = '/afs/hep.wisc.edu/home/acwarden/BDT/BDT0p90_sellep/' 
#filepath = '/afs/hep.wisc.edu/home/acwarden/BDT/ABCD_BDT0p966_sellep/sig1fbxsec/'
#filepath = '/afs/hep.wisc.edu/home/acwarden/BDT/ABCD_BDT_selmuele/'

ctaus = [100, 300, 1000, 10000, 30000]
mstop = [200, 300, 400, 600, 800, 1000, 1200, 1400, 1600, 1800]
#mstop = [600, 800, 1600]

decay = ['ld', 'lb']


bkg = 'bkgmqcd_Histos_'+year
data = 'data_Histos_'+year

# bkg_mu = 'bkgmqcd_Histos_'+year+'_mu'
# bkg_ele = 'bkgmqcd_Histos_'+year+'_ele'

if useData:
  d_bkg = getNumEvents(data,dirs,SF=1,useData=True)
else:
  d_bkg = getNumEvents(bkg,dirs,SF=1,useData=False)
  #d_bkg = getNumEvents_multi(bkg_mu, bkg_ele,dirs,SF=1,useData=False)



n_uncerts_bkg = 0
bkg_stat_uncert = ''
# for i in range(len(channels)):
#  uncert_i = 1.0
#  if not d_bkg['weighted'][i]==0:
#    uncert_i += d_bkg['stat_uncert'][i]/d_bkg['weighted'][i]
#  bkg_stat_uncert += 'background_stat_{0}\tlnN'.format(channels[i]) \
#                    +'\t-'*(i*len(processes)) \
#                    +'\t-\t{:.3g}'.format(uncert_i) \
#                    +'\t-'*((len(channels)-i-1)*len(processes))+'\n'
#  n_uncerts_bkg += 1
# bkg_stat_uncert += 'syst_uncert\tlnN' + '\t2.0'*(len(channels)*len(processes))
# n_uncerts_bkg += 1

syst_uncert = ''

#TODO : calculate ABCD syst uncertainty 
# syst_uncert += 'ABCD_syst\tlnN' \
#               +'\t-\t{:.5g}'.format(getABCDSyst(year)+1) \
#               +'\t-'*((len(channels)-1)*len(processes))+'\n'
# n_uncerts_bkg += 1

abcd = '''
a__YEAR_    rateParam   highBDT_4tk_YEAR_   background    ((@0*@1)/@2)  b__YEAR_,e__YEAR_,f__YEAR_
b__YEAR_    rateParam    midBDT_4tk_YEAR_   background    _BYIELD_
c__YEAR_    rateParam    lowBDT_4tk_YEAR_   background    _CYIELD_
d__YEAR_    rateParam   highBDT_3tk_YEAR_   background    _DYIELD_
e__YEAR_    rateParam    midBDT_3tk_YEAR_   background    _EYIELD_
f__YEAR_    rateParam    lowBDT_3tk_YEAR_   background    _FYIELD_
'''.replace('_YEAR_',year)
yield_label = ['_BYIELD_','_CYIELD_','_DYIELD_','_EYIELD_','_FYIELD_']
for i in range(len(yield_label)):
  abcd = abcd.replace(yield_label[i],getYield(d_bkg['weighted'][i+1]))

for ctau in ctaus:
  for m in mstop:
     for d in decay:
        signal = "mfv_stop%s_tau0%05ium_M%i_Histos_%s" % (d, ctau,m,year)
        # signal_ele = "mfv_stop%s_tau0%05ium_M%i_Histos_%s_ele" % (d, ctau,m,year)
        # signal_mu = "mfv_stop%s_tau0%05ium_M%i_Histos_%s_mu" % (d, ctau,m,year)

        signal_output = "mfv_stop%s_tau0%05ium_M%i_%s" % (d, ctau,m,year)
        #if signal == "mfv_splitSUSY_tau000000300um_M1800_1600_%s_METtrigger" % (year): #skipping one? 
            #continue

        syst = getSystUncert(d,year) #TODO : set up systematics, what we have...
        #sf = 1-syst['vtxreco'] #TODO : get vertex reco systematics; right now have it be 1 
        sf = 1
        d_sig = getNumEvents(signal,dirs,SF=sf,useData=False)
        #d_sig = getNumEvents_multi(signal_mu, signal_ele,dirs,SF=sf,useData=False)


        n_uncerts_sig = 0
        rate = ''
        sig_stat_uncert = ''
        sig_syst_uncert = ''
        #syst_sources = ["intlumi"] #TODO: add vtxreco, BDT, trigger, l1? anything else? pu 
        syst_sources = []
        for i in range(len(channels)):
          rate += '\t{:.5g}'.format(d_sig['weighted'][i]) 
          rate += '\t'+'1.0'
          uncert_i = 0.0
          
          if not d_sig['raw'][i]==0:
            uncert_i = ((d_sig['weighted'][i])/d_sig['raw'][i])
          sig_stat_uncert += 'signal_stat_{}\tgmN\t{:d}'.format(channels[i], d_sig['raw'][i]) \
                          +'\t-'*(i*len(processes)) \
                          +'\t{:.5g}'.format(uncert_i)+'\t-'*(len(processes)-1) \
                          +'\t-'*((len(channels)-i-1)*len(processes))+'\n'

          n_uncerts_sig += 1
        for isource in syst_sources: 
          sig_syst_uncert += 'signal_syst_{}\tlnN'.format(isource) \
                          +('\t{:.5g}'.format(1+syst[isource])+'\t-'*(len(processes)-1))*len(channels) +'\n'
          n_uncerts_sig += 1

        template_new = template.replace('_SIGNAL_',signal)
        #template_new = template.replace('_SIGNAL_', signal_ele+' & '+signal_mu)
        template_new = template_new.replace('_NCHANNELS_',str(len(channels)))
        template_new = template_new.replace('_NUNCERT_',str(n_uncerts_bkg+n_uncerts_sig))
        template_new = template_new.replace('_CHANNELNAME_',str('\t'.join(channels)))
        template_new = template_new.replace('_CHANNELNAMERATE_',channelnamerate)
        template_new = template_new.replace('_PROCESSNAMERATE_',processnamerate)
        template_new = template_new.replace('_PROCESSIDXRATE_',processidxrate)
        template_new = template_new.replace('_PROCESSRATE_',rate)
        template_new = template_new.replace('_STATUNCERTSIG_',sig_stat_uncert)
        template_new = template_new.replace('_STATUNCERTBKG_',bkg_stat_uncert)
        template_new = template_new.replace('_SYSTUNCERT_',syst_uncert)
        template_new = template_new.replace('_SYSTUNCERTSIG_',sig_syst_uncert)
        template_new = template_new.replace('_ABCD_',abcd)
        template_new = template_new.replace('_OBSERVATION_','\t'.join(map(lambda x:"{:.2f}".format(x), d_bkg['weighted'])))
        #if useData:
        #  template_new = template_new.replace('_OBSERVATION_','\t'.join(map(lambda x:"{:.2f}".format(x),d_data['raw'])))
        #else:
        #  template_new = template_new.replace('_OBSERVATION_','\t'.join(map(lambda x:"{:.2f}".format(x),d_bkg['weighted'])))
        f_datacard = open(signal_output+'_datacard.txt','w')
        f_datacard.write(template_new)
        f_datacard.close()