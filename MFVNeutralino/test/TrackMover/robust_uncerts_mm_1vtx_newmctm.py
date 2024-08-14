import ROOT
import numpy as np


# FUNCTIONS USED
#############################################################################################

def shiftTOC(num, den, sint, fr):
    s_num = ROOT.TH1D("shifted_num", "", 80, 0, 80)
    s_den = ROOT.TH1D("shifted_den", "", 80, 0, 80)

    fr = 1.0-fr

    for b in range(0,80):
        s_num.SetBinContent(b, fr*num.GetBinContent(b+sint) + (1-fr)*num.GetBinContent(b+1+sint))
        s_num.SetBinError(b, np.hypot(fr*num.GetBinError(b+sint), (1-fr)*num.GetBinError(b+1+sint)))

        s_den.SetBinContent(b, fr*den.GetBinContent(b+sint) + (1-fr)*den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot(fr*den.GetBinError(b+sint), (1-fr)*den.GetBinError(b+1+sint)))

    s_num.Divide(s_den)
    return s_num

def scaledTOC(sig_curve, data_curve, mc_curve):
    s_curve = sig_curve.Clone()
    
    #### invalid with the identity test

    #factors = mc_curve.Clone()
    #divisor = data_curve.Clone()
    #s_curve.Scale(factors.Integral()/sig_curve.Integral())
    #divisor.Scale(1.0/divisor.Integral())
    #factors.Divide(divisor)
    #s_curve.Multiply(factors)
    
    for b in range(0,s_curve.GetNbinsX()):
        if (mc_curve.GetBinContent(b) != 0):
            scale = 1*(sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) > 1) + (data_curve.GetBinContent(b)/mc_curve.GetBinContent(b))*( sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/mc_curve.GetBinContent(b) < 1)
            s_curve.SetBinContent(b, sig_curve.GetBinContent(b)*scale)
            s_curve.SetBinError(b, sig_curve.GetBinError(b)*scale)
    return s_curve
    
def cutZero(original, max_n):
    curve = original.Clone()
    for b in range(0,max_n):
        curve.SetBinContent(b, 0)
        curve.SetBinError(b, 0)
    return curve

#############################################################################################

def shiftDIST(den, sint, fr):
    s_den = den.Clone() #ROOT.TH1D("placeholder", "", 80, 0, 80)

    fr = 1.0-fr

    for b in range(0,den.GetNbinsX()):
        s_den.SetBinContent(b, fr*den.GetBinContent(b+sint) + (1-fr)*den.GetBinContent(b+1+sint))
        s_den.SetBinError(b, np.hypot(fr*den.GetBinError(b+sint), (1-fr)*den.GetBinError(b+1+sint)))

    return s_den

################################################################################################

def assessMCToDataUncerts(slide_uncerts, scale_uncerts, toc_uncerts, tkscl_uncerts, mc_unc, stat_unc):

    sys_dist_val = max(abs(slide_uncerts), abs(scale_uncerts))
    print("01 TMMC-TMData : slide n scale distr", slide_uncerts, scale_uncerts)
    total = np.sqrt (sys_dist_val**2 + toc_uncerts**2 + 0.0**2 + tkscl_uncerts**2 + stat_unc**2)

    print( " 1-vtx Unc. by SF_{nclsedtks,non} : %.2f (sys_distr) +/- %.2f (sys_scale_toc) +/- %.2f (sys_stat) +/- %.2f (sys_reweight) +/- %.2f (sys_tkrescl) : %.2f %% " % (sys_dist_val, toc_uncerts, stat_unc, 0.0, tkscl_uncerts, total) )

    return total

################################################################################################

def assessRatioEffUncerts(eff_num, err_eff_num, eff_den, err_eff_den):

    tot_err_one = 2*err_eff_num/eff_den 
    tot_err_two = 2*eff_num*err_eff_den/(eff_den**2)

    rat_err = round (100*np.hypot(tot_err_one, tot_err_two), 2)  

    return rat_err

################################################################################################


def assessSigToTMMCUncerts(eff_slide, err_slide, eff_scale, err_scale, eff_toc, err_toc, eff_sig, err_sig):

    slide_uncerts = round(100*(1-(eff_slide/eff_sig)), 2)
    err_slide_uncerts = assessRatioEffUncerts(eff_slide, err_slide, eff_sig, err_sig)
    scale_uncerts = round(100*(1-(eff_scale/eff_sig)), 2)
    err_scale_uncerts = assessRatioEffUncerts(eff_scale, err_scale, eff_sig, err_sig)
    toc_uncerts = round(100*(1-(eff_toc/eff_sig)), 2)
    err_toc_uncerts = assessRatioEffUncerts(eff_toc, err_toc, eff_sig, err_sig)
    
    dist_uncerts = max(abs(slide_uncerts), abs(scale_uncerts))
    if (slide_uncerts > scale_uncerts):
       err_dist_uncerts = err_slide_uncerts
    else:
       err_dist_uncerts = err_scale_uncerts
    print("02 sigMC-TMMC : slide n scale distr", slide_uncerts, scale_uncerts)
    total = np.sqrt (dist_uncerts**2 + toc_uncerts**2)
    err_total = np.sqrt(err_dist_uncerts**2 + err_toc_uncerts**2)

    print( " 1-vtx Unc. by SF_{TMMC-to-signalMC} : %.2f +/- %.2f (sys_distr) +/- %.2f +/- %.2f (sys_scale_toc) : %.2f +/- %.2f %% " % (dist_uncerts, err_dist_uncerts, toc_uncerts, err_toc_uncerts, total, err_total) )

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

year = '20161p2'
doShift  = True
reweight = True
#toc_shift = 0.0   # How much to move the turn-on curve by
#shift_fr  = 0.0   # How much to slide the closeseedtk dist by (decimal part)
#shift_val = 0     # How much to slide the closeseedtk dist by (integer part)

masses = ['55']  #['15','40','55']
ctaus       = ['1000'] #['1000', '3000', '30000'] 
psd_methods = ['none', 'slide_distr', 'scale_distr', 'scale_toc',] # 'trackrescl']

"""
if year == '2018': 
    shift_val = 2 #FIXME
    shift_fr  = 0.0 #FIXME
    toc_shift = 1.0 #FIXME 
if year == '2017': 
    shift_val = 0 #FIXME
    shift_fr  = 0.037 #FIXME 
    toc_shift = 1.0 #FIXME
"""

# Start actually doing stuff

uncertArray = []
all_stat_uncerts = {}
all_overlap_uncerts = {}

for mass in masses:
            
    for ctau in ctaus:

        effArray = []
        errArray = []
        stat_uncerts = 0.0
        overlap_uncerts = 0.0
        tm_unc = 0.0
        mc_unc = 0.0

        for psd_method in psd_methods:
                
                sim_str = ''
                dat_str = ''
                sig_non_str = ''

                if not reweight:
                    sim_str = "~/nobackup/crabdirs/TrackMover_StudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/background_leptonpresel_%s.root" % (int(ctau), year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_SrudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_noCorrection/SingleMuon%s.root" % (int(ctau), year)
                else:
                    sim_str = "~/nobackup/crabdirs/TrackMover_StudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2Dmovedist3movedistjetdrllpsumpcoarse60Correction/background_leptonpresel_%s.root" % (int(ctau), int(mass), year)
                    dat_str = "~/nobackup/crabdirs/TrackMover_StudyV2p4_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau%06ium_M%i_2Dmovedist3movedistjetdrllpsumpcoarse60Correction/SingleMuon%s.root" % (int(ctau), int(mass), year)
                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                
                if mass == '15': 
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'
                elif mass == '40':
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'
                else :
                    sig_non_str  = '~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root'


                signal_non = ROOT.TFile(sig_non_str)

                signal  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')

                signal_ht  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijetsV2p4_LowEta_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                
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

                if psd_method == "none" :
                    foutsim_c = ROOT.TFile(psd_method+"sim_curve.root", "recreate")
                    sim_curve.Write()
                    foutsim_c.Close()
                    foutsim_d = ROOT.TFile(psd_method+"sim_dist.root", "recreate")
                    sim_den.Write()
                    foutsim_d.Close()


                dat_curve = dat_num.Clone()
                dat_den = dat_den.Clone()
                dat_curve.Divide(dat_den)

                if psd_method == "none" :
                    foutdat_c = ROOT.TFile(psd_method+"dat_curve.root", "recreate")
                    dat_curve.Write()
                    foutdat_c.Close()
                    foutdat_d = ROOT.TFile(psd_method+"dat_dist.root", "recreate")
                    dat_den.Write()
                    foutdat_d.Close()

                sig_dist = signal.Get('nocuts_closeseedtks_den')
                print( "intergral : ", sig_dist.Integral())
                #sig_dist = cutZero(sig_dist, 5)
                signon_dist = signal_non.Get('nocuts_closeseedtks_den')
                #signon_dist = cutZero(signon_dist, 5)
                simtmslidedistr_dist = signon_dist.Clone()  
                simtmscaledistr_dist = signon_dist.Clone()  
                simtmscaletoc_dist = signon_dist.Clone()  
                shift_val = int(signon_dist.GetMean()-sim_den.GetMean())
                shift_fr = round(signon_dist.GetMean()-sim_den.GetMean(),2) - int(signon_dist.GetMean()-sim_den.GetMean())

                simtmslidedistr_dist = shiftDIST(simtmslidedistr_dist, shift_val, shift_fr) # psd_dist to sig_dist
               
                #print(" sig sim - TM sim shift ", round(signon_dist.GetMean()-sim_den.GetMean(),2))   
                #print (shift_val, shift_fr)

                simscale_factors = sim_den.Clone()
                simscale_divisor = signon_dist.Clone()
                simscale_factors.Scale(1.0/simscale_factors.Integral())
                simscale_divisor.Scale(1.0/simscale_divisor.Integral())
                simscale_factors.Divide(simscale_divisor)
                simtmscaledistr_dist.Multiply(simscale_factors)

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
                sig_non_m3d_curve = signal_non.Get('all_vtxunc_num') #FIXME
                sig_non_m3d_curve.Divide(sig_non_m3d_denom)
                sig_non_m3d_curve_tm = sig_non_m3d_curve.Clone()
                sig_non_m3d_denom_tm = sig_non_m3d_denom.Clone()
                
                sig_dvv_denom = signal.Get('all_lspdist3_den') 
                sig_dvv_curve = signal.Get('all_lspdist3_num')
                sig_dvv_curve.Divide(sig_dvv_denom)
                sig_dvv_curve_tm = sig_dvv_curve.Clone()
                sig_dvv_denom_tm = sig_dvv_denom.Clone()
                sig_dvv_curve_tm2 = sig_dvv_curve.Clone()
                sig_dvv_denom_tm2 = sig_dvv_denom.Clone()
                sig_dvv_denom_copy = sig_dvv_denom.Clone()
                sig_m3d_denom = signal.Get('all_vtxunc_den') #FIXME 
                sig_m3d_curve = signal.Get('all_vtxunc_num') #FIXME
                sig_m3d_curve.Divide(sig_m3d_denom)
                sig_m3d_curve_tm = sig_m3d_curve.Clone()
                sig_m3d_denom_tm = sig_m3d_denom.Clone()
                sig_m3d_denom_copy = sig_m3d_denom.Clone()
                sig_non_m3d_denom_copy = sig_non_m3d_denom.Clone()

                sig_non_m3d_curve_ideal = shiftDIST(sig_non_m3d_curve, 0, 0.0)
                fout_non0 = ROOT.TFile("nonm3dcurve0.root", "recreate")
                sig_non_m3d_curve_ideal.Write()
                fout_non0.Close()
                fout_non0_den = ROOT.TFile("nonm3dden0.root", "recreate")
                sig_non_m3d_denom.Write()
                fout_non0_den.Close()
                sig_non_m3d_denom.Multiply(sig_non_m3d_curve_ideal)
                eff_non_ideal = sig_non_m3d_denom.Integral()/sig_non_m3d_denom_copy.Integral()

                sig_non_m3d_curve_shift = shiftDIST(sig_non_m3d_curve_tm, 1, 0.0)
                fout_non1 = ROOT.TFile("nonm3dcurve1.root", "recreate")
                sig_non_m3d_curve_shift.Write()
                fout_non1.Close()
                fout_non1_den = ROOT.TFile("nonm3dden1.root", "recreate")
                sig_non_m3d_denom_tm.Write()
                fout_non1_den.Close()
                sig_non_m3d_denom_tm.Multiply(sig_non_m3d_curve_shift)
                eff_non_shift = sig_non_m3d_denom_tm.Integral()/sig_non_m3d_denom_copy.Integral()


                sig_m3d_curve_ideal = shiftDIST(sig_m3d_curve, 0, 0.0)
                fout_0 = ROOT.TFile("m3dcurve0.root", "recreate")
                sig_m3d_curve_ideal.Write()
                fout_0.Close()
                fout_0_den = ROOT.TFile("m3dden0.root", "recreate")
                sig_m3d_denom.Write()
                fout_0_den.Close()
                sig_m3d_denom.Multiply(sig_m3d_curve_ideal)
                eff_ideal = sig_m3d_denom.Integral()/sig_m3d_denom_copy.Integral()
                
                sig_m3d_curve_shift = shiftDIST(sig_m3d_curve_tm, 1, 0.0)
                fout_1 = ROOT.TFile("m3dcurve1.root", "recreate")
                sig_m3d_curve_shift.Write()
                fout_1.Close()
                fout_1_den = ROOT.TFile("m3dden1.root", "recreate")
                sig_m3d_denom_tm.Write()
                fout_1_den.Close()
                sig_m3d_denom_tm.Multiply(sig_m3d_curve_shift)
                eff_shift = sig_m3d_denom_tm.Integral()/sig_m3d_denom_copy.Integral()

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
                tm_unc = 100*(1 - (eff_shift/eff_non_shift)*(eff_non_ideal/eff_ideal)) 
                
                # FIXME shift sim to look like dat
                # shift_val = int(sim_den.GetMean()-dat_den.GetMean())
                # shift_fr = round(sim_den.GetMean()-dat_den.GetMean(),3) - int(sim_den.GetMean()-dat_den.GetMean())
                # sim_den = shiftDIST(sim_den, shift_val, shift_fr+0.5)


                # Calculate the scale factors
                scale_factors = dat_den.Clone()
                scale_divisor = sim_den.Clone()
                scale_factors.Scale(1.0/scale_factors.Integral())
                scale_divisor.Scale(1.0/scale_divisor.Integral())
                scale_factors.Divide(scale_divisor)

                # Fill pseudodata distribution
                psd_dist = sig_dist.Clone()


                if psd_method == 'slide_distr':
                    shift_val = int(sim_den.GetMean()-dat_den.GetMean())
                    shift_fr = round(sim_den.GetMean()-dat_den.GetMean(),3) - int(sim_den.GetMean()-dat_den.GetMean())
                    #print(" TM dat- TM sim shift ", round(sim_den.GetMean()-dat_den.GetMean(),2))   
                    
                    psd_dist = shiftDIST(psd_dist, shift_val, shift_fr) # psd_dist to sig_dist
                    
                if psd_method == 'scale_distr':
                    psd_dist = sig_dist.Clone()
                    psd_dist.Multiply(scale_factors)
                
                fout = ROOT.TFile(psd_method+"_dist.root", "recreate")
                psd_dist.Write()
                fout.Close()

                # Make the TM data and TM sim turn-on curves

                dat_num.Divide(dat_den)
                sim_num.Divide(sim_den)
                # Make the pseudodata turn-on curve
                #temp_shift = toc_shift
                #temp_shift *= -1
                
                #psd_curve = shiftTOC(temp_sig_num, temp_sig_den, int(temp_shift//1), (temp_shift % 1) )
                # Make the signal turn-on curve

                psd_curve = sig_curve
                if psd_method == 'scale_toc':
                    psd_curve = scaledTOC(sig_curve, dat_num, sim_num)
               
                fout2 = ROOT.TFile(psd_method+"_curve.root", "recreate")
                psd_curve.Write()
                fout2.Close()
                
                possible_sim = sig_dist.Integral()
                possible_signon = signon_dist.Integral()
                possible_simtmslidedistr =  simtmslidedistr_dist.Integral()
                possible_simtmscaledistr =  simtmscaledistr_dist.Integral()
                possible_simtmscaletoc =  simtmscaletoc_dist.Integral()
                possible_psd = psd_dist.Integral()

                sig_dist.Multiply(sig_curve)
                signon_dist.Multiply(signon_curve)
                simtmscaledistr_dist.Multiply(signon_curve) 
                simtmslidedistr_dist.Multiply(signon_curve) 
                simtmscaletoc_dist.Multiply(sim_curve) 
                

                psd_dist.Multiply(psd_curve)

                fout3 = ROOT.TFile(psd_method+"_"+mass+"_"+ctau+"_distcurve.root", "recreate")
                psd_dist.Write()
                fout3.Close()

                pass_sim = sig_dist.Integral()
                pass_signon = signon_dist.Integral()
                pass_simtmscaledistr = simtmscaledistr_dist.Integral() 
                pass_simtmslidedistr = simtmslidedistr_dist.Integral() 
                pass_simtmscaletoc = simtmscaletoc_dist.Integral() 
                pass_psd = psd_dist.Integral()
                
                psd_dist.Scale(pass_sim/pass_psd)
                
                eff_sim = pass_sim/possible_sim
                eff_signon = pass_signon/possible_signon
                eff_simtmscaledistr = pass_simtmscaledistr/possible_simtmscaledistr
                eff_simtmslidedistr = pass_simtmslidedistr/possible_simtmscaledistr
                eff_simtmscaletoc = pass_simtmscaletoc/possible_simtmscaletoc
                eff_psd = (pass_psd/possible_psd)

                err_sim = np.sqrt(eff_sim * (1-eff_sim)/possible_sim)
                err_psd = np.sqrt(eff_psd * (1-eff_psd)/possible_psd)
                err_signon = np.sqrt(eff_signon * (1-eff_signon)/possible_signon)
                err_simtmscaledistr = np.sqrt(eff_simtmscaledistr * (1-eff_simtmscaledistr)/possible_simtmscaledistr)
                err_simtmslidedistr = np.sqrt(eff_simtmslidedistr * (1-eff_simtmslidedistr)/possible_simtmslidedistr)
                err_simtmscaletoc = np.sqrt(eff_simtmscaletoc * (1-eff_simtmscaletoc)/possible_simtmscaletoc)
                

                effArray.append(round(100*(1-eff_psd/eff_sim), 2))
      
                if psd_method == 'none':
                     stat_uncerts = assessRatioEffUncerts(eff_psd, err_psd, eff_sim, err_sim)
                overlap_uncerts = round (100*overlap_right_unc,2) 
        print("Mass: %s   Ctau: %s  1-vtx Eff: %.2f " % (mass, ctau, 100*eff_sim*eff_sim))
        datsim_unc = assessMCToDataUncerts( effArray[1], effArray[2], effArray[3], 0.0, mc_unc, stat_uncerts) #FIXME tkrecl unc is fixed at 6% 
        mc_unc = assessSigToTMMCUncerts(eff_simtmslidedistr, err_simtmslidedistr, eff_simtmscaledistr, err_simtmscaledistr, eff_simtmscaletoc, err_simtmscaletoc, eff_signon, err_signon)
        print( " 1-vtx Unc. by TMMC-to-signalMC : %.2f %%" % (mc_unc) )
        print( " 1-vtx Unc. by SF_{GEN3DdVV, mix}: %.2f %%" % (overlap_uncerts) )
        print( " 1-vtx Unc. by SF_{nclsedtks, mix} x SF_{GEN3DdVV, mix} / SF_{nclsedtks, non}: %.2f %%" % (tm_unc) )
        print( " Total : %.2f %%" % (np.sqrt(datsim_unc**2 + mc_unc**2 + tm_unc**2)))
        print("\n")
