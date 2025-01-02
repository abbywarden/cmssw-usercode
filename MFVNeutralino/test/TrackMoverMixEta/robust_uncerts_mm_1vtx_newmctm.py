import ROOT
import numpy as np
import math

# FUNCTIONS USED
#############################################################################################

def shiftTOC(num, den, sint, fr):
    ### OBSOLETE ###
    s_num = num.Clone()
    s_den = den.Clone()
    s_curve = num.Clone()
    s_curve.Divide(s_curve, s_den, 1, 1, "B")
    n_num = num.Integral()
    n_den = den.Integral() 
    
    for b in range(0,s_den.GetNbinsX()):
      if (fr + sint + 1 < 0): 
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b+sint) + (fr)*s_num.GetBinContent(b+1+sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
      else:
        s_num.SetBinContent(b, (1-fr)*s_num.GetBinContent(b+sint) + (fr)*s_num.GetBinContent(b+1+sint))
        s_den.SetBinContent(b, (1-fr)*s_den.GetBinContent(b+sint) + (fr)*s_den.GetBinContent(b+1+sint))
      
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
    s_curve.Divide(s_curve, s_den, 1, 1, "B")
    
    
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
    s_den = den.Clone() 
    for b in range(0, den.GetNbinsX()):
        s_den.SetBinContent(b, (1-fr)*den.GetBinContent(b+sint) + (fr)*den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot((1-fr)*den.GetBinError(b+sint), (fr)*den.GetBinError(b+1+sint)))
    return s_den


#############################################################################################

def scaleDIST(den, fr):
    s_den = den.Clone() 
    for b in range(0, den.GetNbinsX()):
        s_den.SetBinContent(b, fr*den.GetBinContent(b))
        s_den.SetBinError(b, fr*den.GetBinError(b))
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
    is0 = d_den.IntegralAndError(0,den.GetNbinsX(),es0)
    es1 = ROOT.Double(0) 
    is1 = n_num.IntegralAndError(0,num.GetNbinsX(),es1)
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

year = '2017'
doShift  = True
reweight = True
#toc_shift = 0.0   # How much to move the turn-on curve by
#shift_fr  = 0.0   # How much to slide the closeseedtk dist by (decimal part)
#shift_val = 0     # How much to slide the closeseedtk dist by (integer part)

masses = ['55']  #['15','40','55']
ctaus       = ['30000',] #['1000', '3000', '30000'] 
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
        eff_psd_dvv = 0.0
        eff_dvv = 0.0
        err_psd_dvv = 0.0
        err_dvv = 0.0
        frac_vetoodvv = 0.0
        frac_vetopdvv = 0.0
        dataMC_unc = 0.0
        stat_unc = 0.0
        emulate_unc = 0.0
        dvv_unc = 0.0
        for psd_method in psd_methods:
                
                sim_str = ''
                dat_str = ''

                if not reweight:
                    sim_str = "~/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/background_leptonpresel_%s.root" % (year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection/SingleMuon%s.root" % (year)
                else:
                    sim_str = "~/nobackup/crabdirs/TrackMover_MoveExpGrid2_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2DCorrection/background_leptonpresel_%s.root" % (int(ctau), int(mass), year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_MoveExpGrid2_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2DCorrection/SingleMuon%s.root" % (int(ctau), int(mass), year)
                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                
                
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
                sim_curve.Divide(sim_curve, sim_den, 1, 1, "B")


                dat_curve = dat_num.Clone()
                dat_den = dat_den.Clone()
                dat_curve.Divide(dat_curve, dat_den, 1, 1, "B")

                signal  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'p8.root')
                
                sig_dist = signal.Get('nocuts_closeseedtks_den')
                sig_denom = sig_dist.Clone()
                sig_aaaaa = signal.Get('all_closeseedtks_num')
                sig_curve = sig_aaaaa.Clone()
                #psd_dist = ROOT.TH1D("psd_dist", "M"+mass+"ctau"+ctau+"um", 80, 0, 80)
                sig_curve.Divide(sig_curve, sig_denom, 1, 1, "B")
                
                fouttt = ROOT.TFile("sig_curve.root", "recreate")
                sig_curve.Write()
                fouttt.Close()
                
                signal_non  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'p8.root')  
                
                signon_dist = signal_non.Get('nocuts_closeseedtks_den')
                non_denom = signon_dist.Clone() 
                non_aaaaa = signal_non.Get('all_closeseedtks_num')
                signon_curve = non_aaaaa.Clone()
                signon_curve.Divide(signon_curve, non_denom, 1, 1, "B")
                
                foutttt = ROOT.TFile("signon_curve.root", "recreate")
                signon_curve.Write()
                foutttt.Close()

                signal_vetopdvv  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_MixEta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'p8.root')  
                
                sigovp_dist = signal_vetopdvv.Get('nocuts_closeseedtks_den')
                ovp_denom = sigovp_dist.Clone() 
                ovp_aaaaa = signal_vetopdvv.Get('all_closeseedtks_num')
                sigovp_curve = ovp_aaaaa.Clone()
                sigovp_curve.Divide(sigovp_curve, ovp_denom, 1, 1, "B")

                if psd_method == 'none':

                    sig_dvv_denom = signal_vetopdvv.Get('all_dvv_den')
                    sig_dvv_num = signal_vetopdvv.Get('all_dvv_num')
                    sig_dvv_curve = signal_vetopdvv.Get('all_dvv_num')
                    sig_dvv_curve.Divide(sig_dvv_curve, sig_dvv_denom, 1, 1, "B")
                    sig_psd_dvv_denom = sig_dvv_denom.Clone() 
                    sig_psd_dvv_num = sig_dvv_num.Clone() 
                    sig_psd_dvv_curve = sig_dvv_curve.Clone() 
                  
                    sig_dvv_curvedist = shiftDIST(sig_dvv_curve, 0, 0.0)  
                    fout_0 = ROOT.TFile("dvv_none_curve.root", "recreate")
                    sig_dvv_curvedist.Write()
                    fout_0.Close()
                    sig_dvv_norm = sig_dvv_denom.Clone()
                    sig_dvv_norm.Scale(1/sig_dvv_norm.Integral())
                    fout_00_den = ROOT.TFile("dvv_none_norm.root", "recreate")
                    sig_dvv_norm.Write()
                    fout_00_den.Close()
                    sig_dvv_curvedist.Multiply(sig_dvv_norm)
                    eff_dvv = sig_dvv_curvedist.Integral()
                    fout_0_den = ROOT.TFile("dvv_none_curvedist.root", "recreate")
                    sig_dvv_curvedist.Write()
                    fout_0_den.Close()
                   
                    sig_psd_dvv_curvedist = shiftDIST(sig_psd_dvv_curve,-4, 0.0) 
                    fout_1 = ROOT.TFile("dvv_slide_toc_curve.root", "recreate")
                    sig_psd_dvv_curvedist.Write()
                    fout_1.Close()
                    sig_psd_dvv_norm = sig_psd_dvv_denom.Clone()
                    sig_psd_dvv_norm.Scale(1/sig_psd_dvv_norm.Integral())
                    sig_psd_dvv_curvedist.Multiply(sig_psd_dvv_norm)
                    eff_psd_dvv = sig_psd_dvv_curvedist.Integral()
                    fout_1_den = ROOT.TFile("dvv_slide_toc_curvedist.root", "recreate")
                    sig_psd_dvv_curvedist.Write()
                    fout_1_den.Close()
                    err_psd_dvv = assessRatioEffPropagateUncerts(shiftDIST(sig_psd_dvv_denom,-4,0.0),shiftDIST(sig_psd_dvv_num,-4,0.0))
                    

                # Calculate the scale factors
                scale_factors = dat_den.Clone()
                scale_divisor = sim_den.Clone()
                scale_factors.Scale(1.0/scale_factors.Integral()) #FIXME
                scale_divisor.Scale(1.0/scale_divisor.Integral()) #FIXME
                #scale_factors = scaledDist(scale_factors) #FIXME
                #scale_divisor = scaledDist(scale_divisor) #FIXME
                scale_factors.Divide(scale_factors, scale_divisor, 1, 1, "B")

                scale_factors_emu = sim_den.Clone()
                scale_divisor_emu = signon_dist.Clone()
                scale_factors_emu.Scale(1.0/scale_factors_emu.Integral()) #FIXME
                scale_divisor_emu.Scale(1.0/scale_divisor_emu.Integral()) #FIXME
                #scale_factors_emu = scaledDist(scale_factors_emu) #FIXME
                #scale_divisor_emu = scaledDist(scale_divisor_emu) #FIXME
                scale_factors_emu.Divide(scale_factors_emu, scale_divisor_emu, 1, 1, "B")

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
                
                fpsdout = ROOT.TFile("psdsig_"+psd_method+"_"+"_dist.root", "recreate")
                psd_dist.Scale(1.0/psd_dist.Integral())
                psd_dist.Write()
                fpsdout.Close()

                fpsdtmmcout = ROOT.TFile("psdtmmc_"+psd_method+"_"+"_dist.root", "recreate")
                psdtmmc_dist.Scale(1.0/psdtmmc_dist.Integral())
                psdtmmc_dist.Write()
                fpsdtmmcout.Close()

                fpsdemuout = ROOT.TFile("psdsig_emu_"+psd_method+"_"+"_dist.root", "recreate")
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
                dat_num.Divide(dat_num, dat_den, 1, 1, "B")
                sim_num.Divide(sim_num, sim_den, 1, 1, "B")
                
                if psd_method == 'none':
                    psdtmdat_curve = dat_num.Clone()
                    fpsdtmdatout2 = ROOT.TFile("psdtmdat_"+psd_method+"_curve.root", "recreate")
                    psdtmdat_curve.Write()
                    fpsdtmdatout2.Close()
                
                # Make the pseudodata turn-on curve
                 
                psd_curve = shiftDIST(sig_curve, 0, 0.0) #sig_curve
                psdtmmc_curve = shiftDIST(sim_num, 0, 0.0) #sim_num
                psd_emu_curve = shiftDIST(signon_curve, 0, 0.0) #signon_curve
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
                    psd_curve = shiftDIST(sig_curve, shift_int, shift_fr)   
                    psdtmmc_curve = shiftDIST(sim_num, shift_int, shift_fr)
                    
                    
                    shift_emu = FindshiftTOC(sim_num, signon_curve)
                    shift_int_emu = int(shift_emu) - 1
                    shift_fr_emu = shift_emu - shift_int_emu
                    print(" TOC shift (green) : ", round(shift_emu,3))  #negative means shifting signal TOC. to the left and positive means shifting signal TOC. to the right because pseudo TOC should turn on before/after signal TOC 
                    psd_emu_curve = shiftDIST(signon_curve, shift_int_emu, shift_emu_fr)
                
                
                fpsdout2 = ROOT.TFile("psdsig_"+psd_method+"_"+"_curve.root", "recreate")
                psd_curve.Write()
                fpsdout2.Close()
                fpsdtmmcout2 = ROOT.TFile("psdtmmc_"+psd_method+"_"+"_curve.root", "recreate")
                psdtmmc_curve.Write()
                fpsdtmmcout2.Close()
                fpsdemuout2 = ROOT.TFile("psdsig_emu_"+psd_method+"_"+"_curve.root", "recreate")
                psd_emu_curve.Write()
                fpsdemuout2.Close()

                possible_sig = sig_dist.Integral()
                possible_signon = signon_dist.Integral()
                possible_sigovp = sigovp_dist.Integral()
                possible_psd = psd_dist.Integral()
                possible_psd_emu = psd_emu_dist.Integral()
                
                pre_sig_dist = sig_dist.Clone()
                pre_signon_dist = signon_dist.Clone()
                pre_sigovp_dist = sigovp_dist.Clone()
                pre_psd_dist = psd_dist.Clone()
                pre_psd_emu_dist = psd_emu_dist.Clone()
                
                sig_dist.Multiply(sig_curve)
                signon_dist.Multiply(signon_curve)
                sigovp_dist.Multiply(sigovp_curve)
                psd_dist.Multiply(psd_curve)
                psd_emu_dist.Multiply(psd_emu_curve)
                
                fpsdout3 = ROOT.TFile(psd_method+"_"+"_"+mass+"_"+ctau+"_distcurve.root", "recreate")
                psd_dist.Write()
                fpsdout3.Close()
                fpsdemuout3 = ROOT.TFile(psd_method+"_"+"_"+mass+"_"+ctau+"_emulation_distcurve.root", "recreate")
                psd_emu_dist.Write()
                fpsdemuout3.Close()
                
                pass_sig = sig_dist.Integral()
                pass_signon = signon_dist.Integral()
                pass_sigovp = sigovp_dist.Integral()
                pass_psd = psd_dist.Integral()
                pass_psd_emu = psd_emu_dist.Integral()
                
                
                eff_sig = (pass_signon+pass_sigovp)/(possible_signon+possible_sigovp)
                eff_signon = pass_signon/possible_signon
                eff_sigovp = pass_sigovp/possible_sigovp
                eff_psd = (pass_psd/possible_psd)
                eff_psd_emu = (pass_psd_emu/possible_psd_emu)
                
                
                err_sig = assessSignalEffUncerts(pre_sig_dist, sig_dist)#assessRatioEffPropagateUncerts(pre_sig_dist, sig_dist) #FIXME NOW
                err_signon = assessSignalEffUncerts(pre_signon_dist, signon_dist)#assessRatioEffPropagateUncerts(pre_signon_dist, signon_dist) #FIXME NOW
                err_sigovp = assessSignalEffUncerts(pre_sigovp_dist, sigovp_dist)#assessRatioEffPropagateUncerts(pre_signon_dist, signon_dist) #FIXME NOW
                err_psd =   assessRatioEffPropagateUncerts(pre_psd_dist, psd_dist)
                err_psd_emu =   assessRatioEffPropagateUncerts(pre_psd_emu_dist, psd_emu_dist)
                
                effArray.append(eff_psd)
                errArray.append(err_psd)
                effArray_emu.append(eff_psd_emu)
                errArray_emu.append(err_psd_emu)

                if psd_method == 'none':
                    none_sig_integral = round(possible_sig,2)
                    none_signon_integral = round(possible_signon,2) 
                    none_sigovp_integral = round(possible_sigovp,2) 
                    frac_vetopdvv = possible_sigovp/(possible_sigovp+possible_signon)
                    frac_vetoodvv = possible_signon/(possible_sigovp+possible_signon)
                  
                    print("Mass: %s   Ctau: %s  \n" % (mass, ctau))
                    print("1-vtx incl. Eff of total %.2f : %.2f +/- %.2f \n" % (none_signon_integral+none_sigovp_integral, 100*eff_sig, 100*err_sig))
                    print("1-vtx novp Eff of total %.2f : %.2f +/- %.2f (frac. %.2f) \n" % (none_signon_integral, 100*eff_signon, 100*err_signon, 100*frac_vetoodvv))
                    print("1-vtx ovp Eff of total %.2f : %.2f +/- %.2f (frac. %.2f) \n" % (none_sigovp_integral, 100*eff_sigovp, 100*err_sigovp, 100*frac_vetopdvv))
                    #stat_uncerts = assessRatioEffUncerts(eff_psd, err_psd, eff_sig, err_sig)
                    #overlap_uncerts = round (100*overlap_right_unc,2)
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
        print("Probe overlapped LLPs \n")

        iso_tot_unc = np.sqrt(dataMC_unc + stat_unc + emulate_unc) 

        dvv_unc = np.sqrt((100*(1-(eff_psd_dvv/eff_dvv)))**2 + (dataMC_unc) + emulate_unc) #FIXME
        print("pseudo slide dvv eff %.2f +/- %.2f \t pseudo slide dvv eff - dvv eff %.2f \t 1-ratio %.2f \n" % (100*eff_psd_dvv, 100*err_psd_dvv, 100*(eff_psd_dvv-eff_dvv), 100*(1-(eff_psd_dvv/eff_dvv))))

        print("\n")
        print( " Isolated-LLP Unc. : %.2f Data-to-MC Unc +/- %2.f Stat. Unc +/- %.2f Emulate Unc. %% or %.2f %%" % (np.sqrt(dataMC_unc), np.sqrt(stat_unc), np.sqrt(emulate_unc), iso_tot_unc))
        print( " Overlapped-LLP Unc. : %.2f %% " %dvv_unc)

        print("\n")

        print( " Weighted Iso. & Ovp. LLP Unc. : %.2f %%" %(np.sqrt((frac_vetopdvv*(dvv_unc**2)) + (frac_vetoodvv*(iso_tot_unc**2)))))

        print("\n")
