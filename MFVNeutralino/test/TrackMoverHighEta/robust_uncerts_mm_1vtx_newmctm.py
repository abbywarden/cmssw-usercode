import ROOT
import numpy as np
import math

# FUNCTIONS USED
#############################################################################################

def shiftTOC(num, den, sint, fr):
    s_num = num.Clone()
    s_den = den.Clone()
    s_curve = num.Clone()
    s_curve.Divide(s_den)
    n_num = num.Integral()
    n_den = den.Integral() 
    
    for b in range(0,s_den.GetNbinsX()):
      if (fr + sint + 1 < 0): 
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b+sint) + (fr)*s_num.GetBinContent(b+1+sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
      else:
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b-sint) + (fr)*s_num.GetBinContent(b-1-sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b-sint) + (fr)*s_den.GetBinContent(b-1-sint))
      
      if s_den.GetBinContent(b) == 0:
        continue
      if (s_num.GetBinContent(b)/s_den.GetBinContent(b) < 0.0 or s_den.GetBinContent(b) < 0.0 ) : 
        bincontent_err = 0.0
        bincontent = 0.0
      elif (s_num.GetBinContent(b)/s_den.GetBinContent(b) > 1.0):
        bincontent_err = 0.0
        bincontent = 1.0
      else:
        bincontent = s_num.GetBinContent(b)/s_den.GetBinContent(b)
        bincontent_err = math.sqrt(bincontent*(1-bincontent)/s_den.GetBinContent(b))
        
      s_curve.SetBinContent(b, bincontent)
      s_curve.SetBinError(b, bincontent_err)
   
    return s_curve

def scaledDist(dist):
    ### OBSOLETE ###
    s_dist = dist.Clone()
    for b in range(0,dist.GetNbinsX()):
        if (s_dist.GetBinContent(b) != 0):
          if (b == 1):
            s_dist.SetBinContent(1, 0.0)
            s_dist.SetBinError(1, 0.0)
          elif (b == 2):
            s_dist.SetBinContent(2, 0.01)
            s_dist.SetBinError(2, 0.01)
          else:
            s_dist.SetBinContent(b, dist.GetBinContent(b)*0.99/dist.Integral(3,100))
            s_dist.SetBinError(b, dist.GetBinError(b)*0.99/dist.Integral(3,100))
    return s_dist


def scaledTOC(sig_num, sig_den, data_curve, mc_curve):
    s_num = sig_num.Clone()
    s_den = sig_den.Clone()
    s_curve = s_num.Clone()
    s_curve.Divide(s_den)
    
    
    for b in range(0,s_den.GetNbinsX()):
        if (mc_curve.GetBinContent(b) != 0 and sig_den.GetBinContent(b) != 0 ):
            #scale = 1*(sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) > 1) + (data_curve.GetBinContent(b)/mc_curve.GetBinContent(b))*( sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) < 1)
            scale = data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) 
           
            if (sig_num.GetBinContent(b)/sig_den.GetBinContent(b) > 1.0):
              bincontent_err = 0.0
              bincontent = 1.0
            elif (sig_num.GetBinContent(b)/sig_den.GetBinContent(b) < 0.0 or sig_den.GetBinContent(b) < 0.0):
              bincontent_err = 0.0
              bincontent = 0.0
            else:
              bincontent = sig_num.GetBinContent(b)/sig_den.GetBinContent(b)
              bincontent_err = math.sqrt(bincontent*(1-bincontent)/sig_den.GetBinContent(b));

            s_curve.SetBinContent(b, bincontent*scale)
            s_curve.SetBinError(b, bincontent_err*scale)
    return s_curve
    
def cutZero(original, max_n):
    ### OBSOLETE ###
    curve = original.Clone()
    for b in range(0,max_n):
        curve.SetBinContent(b, 0)
        curve.SetBinError(b, 0)
    return curve

#############################################################################################

def shiftDIST(den, sint, fr):
    s_den = den.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)
    #n_den = s_den.Integral()
    #s_den.Scale(1/s_den.Integral())
    for b in range(1, den.GetNbinsX()):
        #s_den.SetBinContent(b, fr*den.GetBinContent(b+sint) + (1-fr)*den.GetBinContent(b+1+sint))
        #s_den.SetBinError(b, np.hypot(fr*den.GetBinError(b+sint), (1-fr)*den.GetBinError(b+1+sint)))
      if (fr + sint + 1 > 0): 
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot((1-fr)*s_den.GetBinError(b+sint), (fr)*s_den.GetBinError(b+1+sint)))
      else:
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b-sint) + (fr)*s_den.GetBinContent(b-1-sint))
        s_den.SetBinError(b, np.hypot((1-fr)*s_den.GetBinError(b-sint), (fr)*s_den.GetBinError(b-1-sint)))
    #s_den.Scale(n_den)
    return s_den

#############################################################################################

def FindshiftTOC(dat, sim):
    dat_curve = dat.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)
    sim_curve = sim.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)
    
    dat_blow = 0.0
    dat_bhigh = 0.0
    sim_blow = 0.0
    sim_bhigh = 0.0
    for b in range(0,dat_curve.GetNbinsX()):
      if dat_curve.GetBinContent(b) > 0.65:
           dat_bhigh = b 
           dat_blow = b-1
           break
    for b in range(0,sim_curve.GetNbinsX()):
      if sim_curve.GetBinContent(b) > 0.65:
           sim_bhigh = b 
           sim_blow = b-1
           break
    dat_b = dat_blow + ((0.65-dat_curve.GetBinContent(dat_blow))/(dat_curve.GetBinContent(dat_bhigh)-dat_curve.GetBinContent(dat_blow)))
    sim_b = sim_blow + ((0.65-sim_curve.GetBinContent(sim_blow))/(sim_curve.GetBinContent(sim_bhigh)-sim_curve.GetBinContent(sim_blow)))
    shift = dat_b - sim_b
    return shift

################################################################################################

def assessRatioEffPropagateUncerts(den, num): #To report pseudo-data efficiency error 
    d_den = den.Clone() 
    n_num = num.Clone()

    es0 = ROOT.Double(0) 
    is0 = d_den.IntegralAndError(0,200,es0)
    es1 = ROOT.Double(0) 
    is1 = n_num.IntegralAndError(0,200,es1)
    rat_err = (is1/is0)*np.hypot(es0/is0, es1/is1) 
    
    return rat_err

def assessCorrelatedDiffEffUncerts(eff_pseudo, eff_sig, denominator): #To report difference error in pseudo-data efficiency and signal efficiency that are correlated 
    # eff is normalized to 1 
    rat_err = round (math.sqrt(math.fabs(eff_pseudo*denominator - eff_sig*denominator))/denominator, 2)  

    return rat_err


def assessSignalEffUncerts(den, num): #To report signal efficiency error from a binomial distributionof events 
    # eff is normalized to 1
    d_den = den.Clone() 
    n_num = num.Clone()
    eff_sig = n_num.Integral()/d_den.Integral()
    denominator = den.Integral()  
    rat_err = round (math.sqrt(eff_sig*(1-eff_sig)/denominator), 2)  

    return rat_err

def assessRatioEffUncerts(eff_num, err_eff_num, eff_den, err_eff_den):
    # eff is normalzied to 1
    tot_err_one = err_eff_num/eff_den #FIXME needs a factor of two 
    tot_err_two = eff_num*err_eff_den/(eff_den**2) #FIXME needs a factor of two 

    rat_err = round (np.hypot(tot_err_one, tot_err_two), 2)  

    return rat_err


################################################################################################

def assessMCToDataUncerts(eff_slide, err_slide, eff_scale, err_scale, eff_toc, err_toc, tkscl_uncerts, stat_unc, eff_sig, err_sig):

    slide_uncerts = round(100*(1-(eff_slide/eff_sig)), 2)
    err_slide_uncerts = assessRatioEffUncerts(eff_slide, err_slide, eff_sig, err_sig)
    scale_uncerts = round(100*(1-(eff_scale/eff_sig)), 2)
    err_scale_uncerts = assessRatioEffUncerts(eff_scale, err_scale, eff_sig, err_sig)
    toc_uncerts = round(100*(1-(eff_toc/eff_sig)), 2)
    err_toc_uncerts = assessRatioEffUncerts(eff_toc, err_toc, eff_sig, err_sig)
    
    print("01 TMMC-TMData : slide distr %.2f +/- %.2f and scale distr %.2f +/- %.2f" % (slide_uncerts, err_slide_uncerts, scale_uncerts, err_scale_uncerts))
    total = np.sqrt (slide_uncerts**2 + toc_uncerts**2 + tkscl_uncerts**2 + stat_unc**2) #FIXME tkrescl
    err_total = np.sqrt(err_slide_uncerts**2 + err_toc_uncerts**2)
    
    print( " 1-vtx Unc. by SF_{nclsedtks,non} : %.2f +/- %.2f (sys_distr) +/- %.2f +/- %.2f (sys_scale_toc) +/- %.2f (sys_stat) +/- %.2f (sys_tkrescl) : %.2f +/- %.2f%% " % (slide_uncerts, err_slide_uncerts, toc_uncerts, err_toc_uncerts, stat_unc, tkscl_uncerts, total, err_total) )

    return total

################################################################################################

def assessSigToTMMCUncerts(eff_slide, err_slide, eff_scale, err_scale, eff_toc, err_toc, eff_sig, err_sig):

    slide_uncerts = round(100*(1-(eff_slide/eff_sig)), 2)
    err_slide_uncerts = assessRatioEffUncerts(eff_slide, err_slide, eff_sig, err_sig)
    scale_uncerts = round(100*(1-(eff_scale/eff_sig)), 2)
    err_scale_uncerts = assessRatioEffUncerts(eff_scale, err_scale, eff_sig, err_sig)
    toc_uncerts = round(100*(1-(eff_toc/eff_sig)), 2)
    err_toc_uncerts = assessRatioEffUncerts(eff_toc, err_toc, eff_sig, err_sig)
    
    print("02 sigMC-TMMC :  slide distr %.2f +/- %.2f and toc %.2f +/- %.2f" % (slide_uncerts, err_slide_uncerts, toc_uncerts, err_toc_uncerts))
    total = np.sqrt (toc_uncerts**2)
    err_total = np.sqrt(err_toc_uncerts**2)
    
    print( " 1-vtx Unc. by SF_{TMMC-to-signalMC} : %.2f +/- %.2f (sys_scale_toc)%% " % (total, err_total) )

    return total

################################################################################################

def calcTocShiftUncert(low, cent, hi):

    outRmsVals = []

    for i in range(0, len(low)):
        rms =  np.sqrt( ((cent[i] - low[i])**2 + (cent[i]-hi[i])**2)/2 )
        rms = round(rms, 2)
        outRmsVals.append(rms)

    return outRmsVals



################################################################################################


# Initialize stuff:

year = '2017p8'
wm = 'alleta'
doShift  = True
reweight = True
#toc_shift = 0.0   # How much to move the turn-on curve by
#shift_fr  = 0.0   # How much to slide the closeseedtk dist by (decimal part)
#shift_val = 0     # How much to slide the closeseedtk dist by (integer part)

masses = ['55']  #['15','40','55']
ctaus       = ['1000'] #['1000', '3000', '30000'] 
psd_methods = ['none', 'slide_distr', 'scale_distr', 'slide_toc', 'scale_toc'] # 'trackrescl']

# Start actually doing stuff

uncertArray = []
all_stat_uncerts = {}
all_overlap_uncerts = {}

for mass in masses:
            
    for ctau in ctaus:

        effArray = []
        errArray = []
        effArray_emu = []
        errArray_emu = []
        DiffeffArray = []
        DifferrArray = []
        DiffeffArray_emu = []
        DifferrArray_emu = []
        none_sig_integral = 0.0
        none_tmdat_integral = 0.0
        none_tmmc_integral = 0.0
        err_none_tmdat_integral = 0.0
        err_none_tmmc_integral = 0.0
        none_tmdat_eff = 0.0
        none_tmmc_eff = 0.0
        err_none_tmdat_eff = 0.0
        err_none_tmmc_eff = 0.0
        stat_uncerts = 0.0
        overlap_uncerts = 0.0
        eff_pseudo_shift_novp = 0.0
        eff_pseudo_shift_incl = 0.0
        eff_pseudo_noshift_novp = 0.0
        eff_pseudo_noshift_incl = 0.0
        err_eff_pseudo_shift_novp = 0.0
        err_eff_pseudo_shift_incl = 0.0
        dataMC_unc = 0.0
        stat_unc = 0.0
        emulate_unc = 0.0
        for psd_method in psd_methods:
                
                sim_str = ''
                dat_str = ''
                sig_non_str = ''

                if not reweight:
                    sim_str = "~/nobackup/crabdirs/TrackMover_StudyV2p5_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/background_leptonpresel_%s.root" % (int(ctau), year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_StudyV2p5_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/SingleMuon%s.root" % (int(ctau), year)
                else:
                    sim_str = "~/nobackup/crabdirs/TrackMover_StudyV2p5_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2Dmovedist3movedist2jetdrllpsumpcoarse60%sCorrection/background_leptonpresel_%s.root" % (int(ctau), int(mass), wm, year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_StudyV2p5_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2Dmovedist3movedist2jetdrllpsumpcoarse60%sCorrection/SingleMuon%s.root" % (int(ctau), int(mass), wm, year)
                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                
                if mass == '15': 
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'
                elif mass == '40':
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'
                else :
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_HighEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'


                signal_non = ROOT.TFile(sig_non_str)

                signal  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_HighEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')

                signal_ht  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p5_HighEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')  
                
                dat_den = tm_dat.Get('all_closeseedtks_den')
                #dat_den = cutZero(dat_den, 5)
                sim_den = tm_sim.Get('all_closeseedtks_den')
                #sim_den = cutZero(sim_den, 5)

                dat_num = tm_dat.Get('all_closeseedtks_num')
                #dat_num = cutZero(dat_num, 5)
                sim_num = tm_sim.Get('all_closeseedtks_num')
                #sim_num = cutZero(sim_num, 5)
                sim_curve = sim_num.Clone()
                sim_den = sim_den.Clone()
                sim_curve.Divide(sim_den)


                dat_curve = dat_num.Clone()
                dat_den = dat_den.Clone()
                dat_curve.Divide(dat_den)

                sig_dist = signal.Get('nocuts_closeseedtks_den')
                signon_dist = signal_non.Get('nocuts_closeseedtks_den')

                sig_denom = signal.Get('all_closeseedtks_den') 
                sig_aaaaa = signal.Get('all_closeseedtks_num')
                sig_curve = sig_aaaaa.Clone()
                temp_sig_num = sig_curve.Clone()
                temp_sig_den = sig_denom.Clone()
                psd_dist = ROOT.TH1D("psd_dist", "M"+mass+"ctau"+ctau+"um", 80, 0, 80)
                sig_curve.Divide(sig_denom)

                fouttt = ROOT.TFile("sig_curve.root", "recreate")
                sig_curve.Write()
                fouttt.Close()

                
                non_denom = signal_non.Get('all_closeseedtks_den') 
                non_aaaaa = signal_non.Get('all_closeseedtks_num')
                signon_curve = non_aaaaa.Clone()
                signon_curve.Divide(non_denom)

                foutttt = ROOT.TFile("signon_curve.root", "recreate")
                signon_curve.Write()
                foutttt.Close()

                sig_non_dvv_denom = signal_non.Get('all_lspdist3_den') 
                sig_non_dvv_curve = signal_non.Get('all_lspdist3_num')
                sig_non_dvv_curve.Divide(sig_non_dvv_denom)
                sig_non_dvv_curve_tm = sig_non_dvv_curve.Clone()
                sig_non_dvv_denom_tm = sig_non_dvv_denom.Clone()
                sig_non_m3d_denom = signal_non.Get('all_vtxunc_den') #FIXME 
                sig_non_m3d_num = signal_non.Get('all_vtxunc_num') #FIXME
                
                sig_dvv_denom = signal.Get('all_lspdist3_den') 
                sig_dvv_curve = signal.Get('all_lspdist3_num')
                sig_dvv_curve.Divide(sig_dvv_denom)
                sig_dvv_curve_tm = sig_dvv_curve.Clone()
                sig_dvv_denom_tm = sig_dvv_denom.Clone()
                sig_dvv_curve_tm2 = sig_dvv_curve.Clone()
                sig_dvv_denom_tm2 = sig_dvv_denom.Clone()
                sig_dvv_denom_copy = sig_dvv_denom.Clone()
                sig_m3d_denom = signal.Get('all_vtxunc_den') #FIXME 
                sig_m3d_num = signal.Get('all_vtxunc_num') #FIXME

                sig_non_m3d_curve = shiftTOC(sig_non_m3d_num, sig_non_m3d_denom, 0, 0.0) #shiftDIST(sig_non_m3d_curve, 0, 0.0)
                fout_non0 = ROOT.TFile("nonm3d_none_curve.root", "recreate")
                sig_non_m3d_curve.Write()
                fout_non0.Close()
                sig_non_m3d_curvedist = sig_non_m3d_denom.Clone()
                sig_non_m3d_curvedist.Scale(1/sig_non_m3d_denom.Integral())
                sig_non_m3d_curvedist.Multiply(sig_non_m3d_curve)
                fout_non0_den = ROOT.TFile("nonm3d_none_curvedist.root", "recreate")
                sig_non_m3d_curvedist.Write()
                fout_non0_den.Close()
                eff_non_noshift = sig_non_m3d_curvedist.Integral()

                sig_non_m3d_curve_shift =  shiftTOC(sig_non_m3d_num, sig_non_m3d_denom, -1, 0.0) #shiftDIST(sig_non_m3d_curve_tm, 1, 0.0)
                fout_non1 = ROOT.TFile("nonm3d_slide_toc_curve.root", "recreate")
                sig_non_m3d_curve_shift.Write()
                fout_non1.Close()
                sig_non_m3d_shift_curvedist = sig_non_m3d_denom.Clone()
                sig_non_m3d_shift_curvedist.Scale(1/sig_non_m3d_denom.Integral())
                sig_non_m3d_shift_curvedist.Multiply(sig_non_m3d_curve_shift)
                fout_non1_den = ROOT.TFile("nonm3d_slide_toc_curvedist.root", "recreate")
                sig_non_m3d_shift_curvedist.Write()
                fout_non1_den.Close()
                eff_non_shift = sig_non_m3d_shift_curvedist.Integral()
                err_eff_non_shift = assessRatioEffPropagateUncerts(shiftDIST(sig_non_m3d_num,-1,0.0),shiftDIST(sig_non_m3d_denom,-1,0.0))
                
                sig_m3d_curve = shiftTOC(sig_m3d_num, sig_m3d_denom, 0, 0.0) 
                fout_0 = ROOT.TFile("m3d_none_curve.root", "recreate")
                sig_m3d_curve.Write()
                fout_0.Close()
                sig_m3d_curvedist = sig_m3d_denom.Clone()
                sig_m3d_curvedist.Scale(1/sig_m3d_denom.Integral())
                sig_m3d_curvedist.Multiply(sig_m3d_curve)
                fout_0_den = ROOT.TFile("m3d_none_curvedist.root", "recreate")
                sig_m3d_curvedist.Write()
                fout_0_den.Close()
                eff_noshift = sig_m3d_curvedist.Integral()
                
                sig_m3d_curve_shift =  shiftTOC(sig_m3d_num, sig_m3d_denom, -1, 0.0) 
                fout_1 = ROOT.TFile("m3d_slide_toc_curve.root", "recreate")
                sig_m3d_curve_shift.Write()
                fout_1.Close()
                sig_m3d_shift_curvedist = sig_m3d_denom.Clone()
                sig_m3d_shift_curvedist.Scale(1/sig_m3d_denom.Integral())
                sig_m3d_shift_curvedist.Multiply(sig_m3d_curve_shift)
                fout_1_den = ROOT.TFile("m3d_slide_toc_curvedist.root", "recreate")
                sig_m3d_shift_curvedist.Write()
                fout_1_den.Close()
                eff_shift = sig_m3d_shift_curvedist.Integral()
                err_eff_shift = assessRatioEffPropagateUncerts(shiftDIST(sig_m3d_num,-1,0.0),shiftDIST(sig_m3d_denom,-1,0.0))

                sig_dvv_curve_ideal = shiftDIST(sig_dvv_curve, 0, 0.0)
                fout_dvv0 = ROOT.TFile("dvvcurve0.root", "recreate")
                sig_dvv_curve_ideal.Write()
                fout_dvv0.Close()
                fout_dvvden0 = ROOT.TFile("dvvden0.root", "recreate")
                sig_dvv_denom.Write()
                fout_dvvden0.Close()
                sig_dvv_denom.Multiply(sig_dvv_curve_ideal)
                eff = sig_dvv_denom.Integral()/sig_dvv_denom_copy.Integral()
                
                sig_dvv_curve_lefttm = shiftDIST(sig_dvv_curve_tm, 3, 0.0) #FIXME
                fout_dvvl = ROOT.TFile("dvvcurvel.root", "recreate")
                sig_dvv_curve_lefttm.Write()
                fout_dvvl.Close()
                sig_dvv_denom_tm.Multiply(sig_dvv_curve_lefttm)
                eff_tm = sig_dvv_denom_tm.Integral()/sig_dvv_denom_copy.Integral()
              
                sig_dvv_curve_righttm = shiftDIST(sig_dvv_curve_tm2, -3, 0.0)
                fout_dvvr = ROOT.TFile("dvvcurver.root", "recreate")
                sig_dvv_curve_righttm.Write()
                fout_dvvr.Close()
                sig_dvv_denom_tm2.Multiply(sig_dvv_curve_righttm)
                eff_tm2 = sig_dvv_denom_tm2.Integral()/sig_dvv_denom_copy.Integral()

                overlap_right_unc = abs((1.0 - (eff_tm2/eff)))
                overlap_left_unc = abs((1.0 - (eff_tm/eff)))
                eff_pseudo_shift_incl = eff_shift    
                eff_pseudo_shift_novp = eff_non_shift 
                eff_pseudo_noshift_incl = eff_noshift    
                eff_pseudo_noshift_novp = eff_non_noshift 
                err_pseudo_shift_incl = err_eff_shift    
                err_pseudo_shift_novp = err_eff_non_shift
                # FIXME shift sim to look like dat
                # shift_val = int(sim_den.GetMean()-dat_den.GetMean())
                # shift_fr = round(sim_den.GetMean()-dat_den.GetMean(),3) - int(sim_den.GetMean()-dat_den.GetMean())
                # sim_den = shiftDIST(sim_den, shift_val, shift_fr+0.5)


                # Calculate the scale factors
                scale_factors = dat_den.Clone()
                scale_divisor = sim_den.Clone()
                scale_factors.Scale(1.0/scale_factors.Integral()) #FIXME
                scale_divisor.Scale(1.0/scale_divisor.Integral()) #FIXME
                #scale_factors = scaledDist(scale_factors) #FIXME
                #scale_divisor = scaledDist(scale_divisor) #FIXME
                scale_factors.Divide(scale_divisor)

                scale_factors_emu = sim_den.Clone()
                scale_divisor_emu = signon_dist.Clone()
                scale_factors_emu.Scale(1.0/scale_factors_emu.Integral()) #FIXME
                scale_divisor_emu.Scale(1.0/scale_divisor_emu.Integral()) #FIXME
                #scale_factors_emu = scaledDist(scale_factors_emu) #FIXME
                #scale_divisor_emu = scaledDist(scale_divisor_emu) #FIXME
                scale_factors_emu.Divide(scale_divisor_emu)

                # Fill pseudodata distribution
                psd_dist = sig_dist.Clone()
                psd_emu_dist = signon_dist.Clone()
                psdtmmc_dist = sim_den.Clone()
                
                if psd_method == 'slide_distr':
                    shift_val = sim_den.GetMean()-dat_den.GetMean()
                    shift_int = int(shift_val) - 1
                    shift_fr = shift_val - shift_int
                    print(" Dist shift (red) : ", -1*round(shift_val,2))  #negative means shifting signal distr. to the left and positive means shifting signal distr. to the right  
                    #print(" sig mean : ", sig_dist.GetMean())
                    #print(" TM data mean : ", dat_den.GetMean())
                    #print(" TM MC mean : ", sim_den.GetMean())
                    psd_dist = shiftDIST(psd_dist, shift_int, shift_fr) 
                    #print(" psd mean : ", psd_dist.GetMean())
                    psdtmmc_dist = shiftDIST(psdtmmc_dist, shift_int, shift_fr)
                    #print(" psdtmmc mean : ", psdtmmc_dist.GetMean())
                    
                    shift_emu_val = signon_dist.GetMean()-sim_den.GetMean() 
                    shift_emu_int = int(shift_emu_val) - 1 
                    shift_emu_fr = shift_emu_val - shift_emu_int
                    print(" Dist shift (green) : ", -1*round(shift_emu_val,2)) #negative means shifting signal distr. to the left and positive means shifting signal distr. to the right   
                    #print(" novp sig mean : ", signon_dist.GetMean())
                    #print(" TM MC mean : ", sim_den.GetMean())
                    psd_emu_dist = shiftDIST(psd_emu_dist, shift_emu_int, shift_emu_fr) 
                    #print(" psd emu mean : ", psd_emu_dist.GetMean())
                
                if psd_method == 'scale_distr':
                    psd_dist.Multiply(scale_factors)
                    psdtmmc_dist.Multiply(scale_factors)
                    psd_emu_dist.Multiply(scale_factors_emu)
                    #psd_dist.Scale(sig_dist.Integral()/psd_dist.Integral())
                    #psdtmmc_dist.Scale(sim_den.Integral()/psdtmmc_dist.Integral())
                    #psd_emu_dist.Scale(signon_dist.Integral()/psd_emu_dist.Integral())
                
                fpsdout = ROOT.TFile("psdsig_"+psd_method+"_"+wm+"_dist.root", "recreate")
                psd_dist.Scale(1.0/psd_dist.Integral())
                psd_dist.Write()
                fpsdout.Close()

                fpsdtmmcout = ROOT.TFile("psdtmmc_"+psd_method+"_"+wm+"_dist.root", "recreate")
                psdtmmc_dist.Scale(1.0/psdtmmc_dist.Integral())
                psdtmmc_dist.Write()
                fpsdtmmcout.Close()

                fpsdemuout = ROOT.TFile("psdsig_emu_"+psd_method+"_"+wm+"_dist.root", "recreate")
                psd_emu_dist.Scale(1.0/psd_emu_dist.Integral())
                psd_emu_dist.Write()
                fpsdemuout.Close()
                # Make the TM data and TM sim turn-on curves
                none_tmdat_eff = dat_num.Integral()/dat_den.Integral()
                none_tmmc_eff = sim_num.Integral()/sim_den.Integral()
                pre_tmdat_dist = dat_den.Clone()
                pre_tmmc_dist = sim_den.Clone()
                
                if psd_method == 'none':
                    psdtmdat_dist = dat_den.Clone()
                    fpsdtmdatout = ROOT.TFile("psdtmdat_"+psd_method+"_dist.root", "recreate")
                    psdtmdat_dist.Scale(1.0/psdtmdat_dist.Integral())
                    psdtmdat_dist.Write()
                    fpsdtmdatout.Close()
                
                tmdat_dist = dat_num.Clone()
                tmmc_dist = sim_num.Clone()
                dat_num.Divide(dat_den)
                sim_num.Divide(sim_den)
                
                if psd_method == 'none':
                    psdtmdat_curve = dat_num.Clone()
                    fpsdtmdatout2 = ROOT.TFile("psdtmdat_"+psd_method+"_curve.root", "recreate")
                    psdtmdat_curve.Write()
                    fpsdtmdatout2.Close()
                
                # Make the pseudodata turn-on curve
                
                psd_curve = shiftTOC(sig_aaaaa, sig_denom, 0, 0.0) #sig_curve
                psdtmmc_curve = shiftTOC(tmmc_dist, pre_tmmc_dist, 0, 0.0) #sim_num
                psd_emu_curve = shiftTOC(non_aaaaa, non_denom, 0, 0.0) #signon_curve
                if psd_method == 'scale_toc':
                    psd_curve = scaledTOC(sig_aaaaa, sig_denom, dat_num, sim_num)
                    psdtmmc_curve = scaledTOC(tmmc_dist, pre_tmmc_dist, dat_num, sim_num)
                    psd_emu_curve = scaledTOC(non_aaaaa, non_denom, sim_num, signon_curve)
                    #psd_curve.Scale(sig_curve.Integral()/psd_curve.Integral())
                    #psdtmmc_curve.Scale(sim_num.Integral()/psdtmmc_curve.Integral())
                    #psd_emu_curve.Scale(signon_curve.Integral()/psd_emu_curve.Integral())
                if psd_method == 'slide_toc':
                    shift = FindshiftTOC(dat_num, sim_num)
                    shift_int = int(shift) - 1
                    shift_fr = shift - shift_int
                    print(" TOC shift (red) : ", round(shift,3))   #negative means shifting signal TOC. to the left and positive means shifting signal TOC. to the right because pseudo TOC should turn on before/after signal TOC 
                    psd_curve = shiftTOC(sig_aaaaa, sig_denom, shift_int, shift_fr)   
                    psdtmmc_curve = shiftTOC(tmmc_dist, pre_tmmc_dist, shift_int, shift_fr)
                    
                    
                    shift_emu = FindshiftTOC(sim_num, signon_curve)
                    shift_int_emu = int(shift_emu) - 1
                    shift_fr_emu = shift_emu - shift_int_emu
                    print(" TOC shift (green) : ", round(shift_emu,3))  #negative means shifting signal TOC. to the left and positive means shifting signal TOC. to the right because pseudo TOC should turn on before/after signal TOC 
                    psd_emu_curve = shiftTOC(non_aaaaa, non_denom, shift_int_emu, shift_emu_fr)
                
                
                fpsdout2 = ROOT.TFile("psdsig_"+psd_method+"_"+wm+"_curve.root", "recreate")
                psd_curve.Write()
                fpsdout2.Close()
                fpsdtmmcout2 = ROOT.TFile("psdtmmc_"+psd_method+"_"+wm+"_curve.root", "recreate")
                psdtmmc_curve.Write()
                fpsdtmmcout2.Close()
                fpsdemuout2 = ROOT.TFile("psdsig_emu_"+psd_method+"_"+wm+"_curve.root", "recreate")
                psd_emu_curve.Write()
                fpsdemuout2.Close()

                possible_sig = sig_dist.Integral()
                possible_signon = signon_dist.Integral()
                possible_psd = psd_dist.Integral()
                possible_psd_emu = psd_emu_dist.Integral()
                
                pre_sig_dist = sig_dist.Clone()
                pre_signon_dist = signon_dist.Clone()
                pre_psd_dist = psd_dist.Clone()
                pre_psd_emu_dist = psd_emu_dist.Clone()
                
                sig_dist.Multiply(sig_curve)
                signon_dist.Multiply(signon_curve)
                psd_dist.Multiply(psd_curve)
                psd_emu_dist.Multiply(psd_emu_curve)
                
                fpsdout3 = ROOT.TFile(psd_method+"_"+wm+"_"+mass+"_"+ctau+"_distcurve.root", "recreate")
                psd_dist.Write()
                fpsdout3.Close()
                fpsdemuout3 = ROOT.TFile(psd_method+"_"+wm+"_"+mass+"_"+ctau+"_emulation_distcurve.root", "recreate")
                psd_emu_dist.Write()
                fpsdemuout3.Close()
                if psd_method=="none":
                    es = ROOT.Double(0) 
                    inl = psd_emu_dist.IntegralAndError(0,200,es)
                    print(inl, es)
                
                pass_sig = sig_dist.Integral()
                pass_signon = signon_dist.Integral()
                pass_psd = psd_dist.Integral()
                pass_psd_emu = psd_emu_dist.Integral()
                
                
                eff_sig = pass_sig/possible_sig
                eff_signon = pass_signon/possible_signon
                eff_psd = (pass_psd/possible_psd)
                eff_psd_emu = (pass_psd_emu/possible_psd_emu)
                
                
                err_sig = assessSignalEffUncerts(pre_sig_dist, sig_dist)#assessRatioEffPropagateUncerts(pre_sig_dist, sig_dist) #FIXME NOW
                err_signon = assessSignalEffUncerts(pre_signon_dist, signon_dist)#assessRatioEffPropagateUncerts(pre_signon_dist, signon_dist) #FIXME NOW
                err_psd =   assessRatioEffPropagateUncerts(pre_psd_dist, psd_dist)
                err_psd_emu =   assessRatioEffPropagateUncerts(pre_psd_emu_dist, psd_emu_dist)
                
                effArray.append(eff_psd)
                errArray.append(err_psd)
                effArray_emu.append(eff_psd_emu)
                errArray_emu.append(err_psd_emu)

                if psd_method == 'none':
                    none_sig_integral = round(possible_sig,2)
                    none_signon_integral = round(possible_signon,2) 
                    print("Mass: %s   Ctau: %s  \n" % (mass, ctau))
                    print("1-vtx incl. Eff of total %.2f : %.2f +/- %.2f (or %.2f +/- %.2f via error propagation)\n" % (none_sig_integral, 100*eff_sig, 100*err_sig, 100*effArray[-1], 100*errArray[-1]))
                    print("1-vtx novp Eff of total %.2f : %.2f +/- %.2f (or %.2f +/- %.2f via error propagation)\n" % (none_signon_integral, 100*eff_signon, 100*err_signon, 100*effArray_emu[-1], 100*errArray_emu[-1]))
                    #stat_uncerts = assessRatioEffUncerts(eff_psd, err_psd, eff_sig, err_sig)
                    overlap_uncerts = round (100*overlap_right_unc,2)
                    es0 = ROOT.Double(0) 
                    is0 = dat_den.IntegralAndError(0,200,es0)
                    none_tmdat_integral = round(is0,2)
                    err_none_tmdat_integral = round(es0,2)
                    err_none_tmdat_eff = assessRatioEffPropagateUncerts(pre_tmdat_dist, tmdat_dist) #FIXME NOW
                    es1 = ROOT.Double(0) 
                    is1 = sim_den.IntegralAndError(0,200,es1)
                    none_tmmc_integral = round(is1,2)
                    err_none_tmmc_integral = round(es1,2)
                    err_none_tmmc_eff = assessRatioEffPropagateUncerts(pre_tmmc_dist, tmmc_dist) #FIXME NOW

                else:
                    DiffeffArray.append(eff_psd - effArray[0])
                    DifferrArray.append(assessCorrelatedDiffEffUncerts(eff_psd, effArray[0], none_sig_integral))
                    DiffeffArray_emu.append(eff_psd_emu - effArray_emu[0])
                    DifferrArray_emu.append(assessCorrelatedDiffEffUncerts(eff_psd_emu, effArray_emu[0], none_signon_integral))

        print("Probe Data-to-MC Overall effciency difference \n")
        print("Total TM MC %.2f +/- %.2f (w/ Eff. %.2f +/- %.2f) and Total TM Data %.2f +/- %.2f (w/ Eff. %.2f +/- %.2f)\n" % (none_tmmc_integral, err_none_tmmc_integral, 100*none_tmmc_eff, 100*err_none_tmmc_eff, none_tmdat_integral, err_none_tmdat_integral, 100*none_tmdat_eff, 100*err_none_tmdat_eff))
        for i in range(1,len(psd_methods)):
            if (i == 1 or i==4):
               dataMC_unc +=  (-100*DiffeffArray[i-1]/effArray[0])**2
            print("%s pseudo eff %.2f +/- %.2f \t pseudo eff - incl. sig eff %.2f +/- %.2f \t 1-ratio %.2f +/- %.2f \n" % (psd_methods[i], 100*effArray[i], 100*errArray[i], 100*DiffeffArray[i-1], 100*DifferrArray[i-1], -100*DiffeffArray[i-1]/effArray[0], -100*DifferrArray[i-1]/effArray[0]))
        print("Probe how well TM MC emulating signal MC \n")
        for i in range(1,len(psd_methods)):
            if (i == 4):
               emulate_unc +=  (-100*DiffeffArray_emu[i-1]/effArray_emu[0])**2
               stat_unc = (-100*DifferrArray_emu[i-1]/effArray_emu[0])**2 
            print("%s pseudo emulating eff %.2f +/- %.2f \t pseudo emulating eff - novp. sig eff %.2f +/- %.2f \t 1-ratio %.2f +/- %.2f \n" % (psd_methods[i],100*effArray_emu[i], 100*errArray_emu[i], 100*DiffeffArray_emu[i-1], 100*DifferrArray_emu[i-1], -100*DiffeffArray_emu[i-1]/effArray_emu[0], -100*DifferrArray_emu[i-1]/effArray_emu[0]))
        print("Probe the eff. difference between novp and incl. signal MC \n")


        print("pseudo shift m3d incl. eff %.2f +/- %.2f \t pseudo shiftm3d incl. eff - incl. sig eff %.2f \t 1-ratio %.2f \n" % (100*eff_pseudo_shift_incl, 100*err_pseudo_shift_incl, 100*(eff_pseudo_shift_incl-eff_pseudo_noshift_incl), 100*(1-(eff_pseudo_shift_incl/eff_pseudo_noshift_incl))))
        print("pseudo shift m3d novp. eff %.2f +/- %.2f\t pseudo shiftm3d novp. eff - novp. sig eff %.2f \t 1-ratio %.2f \n" % (100*(eff_pseudo_shift_novp), 100*err_pseudo_shift_novp, 100*(eff_pseudo_shift_novp-eff_pseudo_noshift_novp), 100*(1-(eff_pseudo_shift_novp/eff_pseudo_noshift_novp))))
        print("additional uncertainty by quadratic-sum based is %.2f"% (math.sqrt(abs((100*(1-(eff_pseudo_shift_incl/eff_pseudo_noshift_incl)))**2 - (100*(1-(eff_pseudo_shift_novp/eff_pseudo_noshift_novp)))**2)))) 
        print("additional uncertainty by formula-based is %.2f"% (100*(1 - (eff_pseudo_shift_incl*eff_pseudo_noshift_novp/(eff_pseudo_shift_novp*eff_pseudo_noshift_incl))))) 
        #datsim_unc = assessMCToDataUncerts( effArray[1], errArray[1], effArray[2], errArray[2], effArray[3], errArray[3], 0.0, stat_uncerts, eff_sig, err_sig) #FIXME tkrescl 
        #mc_unc = assessSigToTMMCUncerts(eff_simtmslidedistr, err_simtmslidedistr, eff_simtmscaledistr, err_simtmscaledistr, eff_simtmscaletoc, err_simtmscaletoc, eff_signon, err_signon)
        print( " 1-vtx Emulate Unc. or |non-overlapped signalMC eff. - non-overlapped TMMC eff.|/(non-overlapped signalMC eff.) : %.2f %%" % np.sqrt(emulate_unc) )
        print( " 1-vtx Data-to-MC Unc or |incl. signalMC eff. - incl. signaldata eff.|/(incl. signalMC eff.) : %.2f %%" % np.sqrt(dataMC_unc) )
        print( " 1-vtx Stat. Unc from Emulate Unc.: %.2f %%" % np.sqrt(stat_unc) )
        #print( " 1-vtx Unc. by SF_{nclsedtks, mix} x SF_{GEN3DdVV, mix} / SF_{nclsedtks, non}: %.2f %%" % (tm_unc) )
        tot_unc = np.sqrt(dataMC_unc + stat_unc + emulate_unc*((effArray_emu[0]/(effArray[0]))**2))  
        print( " Total : %.2f (sqrt(Data-to-MC Unc,Stat. Unc)) +/- %.2f (Emulate Unc. x eff_novp/eff_incl) %% or %.2f %%" % (np.sqrt(dataMC_unc + stat_unc), (np.sqrt(emulate_unc)*effArray_emu[0]/(effArray[0])), tot_unc))
        print("\n")
