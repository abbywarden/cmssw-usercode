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

def scaledTOC(sig_curve, data_curve, sim_curve):
    s_curve = ROOT.TH1D("scaled_curve", "", 80, 0, 80)
    fout = ROOT.TFile("scaledtoc.root", "recreate")
    for b in range(0,80):
        if (sim_curve.GetBinContent(b) > 0):
            s_curve.SetBinContent(b, sig_curve.GetBinContent(b)*data_curve.GetBinContent(b)/sim_curve.GetBinContent(b))
            s_curve.SetBinError(b, sig_curve.GetBinError(b)*data_curve.GetBinContent(b)/sim_curve.GetBinContent(b))
    s_curve.Write()
    return s_curve

def cutZero(original, name):
    curve = original.Clone()
    for b in range(0,80):
        curve.SetBinContent(1, 0)
        curve.SetBinError(1, 0)
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
    #print("slide n scale distr", slide_uncerts, scale_uncerts)
    total = np.sqrt (sys_dist_val**2 + toc_uncerts**2 + 0.0**2 + stat_unc**2)

    print( " 1-vtx Unc. by SF_{nclsedtks,non} : %.3f (sys_distr) +/- %.3f (sys_scale_toc) +/- %.3f (sig_stat) +/- %.3f (sys_reweight) (+/- %.3f (sys_tkrescl)?) : %.3f %% " % (sys_dist_val, toc_uncerts, stat_unc, 0.0, tkscl_uncerts, total) )

    return total

################################################################################################

def calcTocShiftUncert(low, cent, hi):

    outRmsVals = []

    for i in range(0, len(low)):
        rms =  np.sqrt( ((cent[i] - low[i])**2 + (cent[i]-hi[i])**2)/2 )
        rms = round(rms, 3)
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

masses = ['55'] # ['15','40','55']
ctaus       = ['1000'] #['1000','3000','30000'] 
psd_methods = ['none', 'slide_distr', 'scale_distr', 'scale_toc', 'trackrescl']

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

                if not reweight:
                    sim_str = "~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_noCorrection/background_leptonpresel_%i.root" % (int(ctau), int(year))
                    dat_str = "~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_noCorrection/SingleMuon%i.root" % (int(ctau), int(year))
                else:
                    sim_str = "~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_M%i_2Dmovedist3movedist2jetdrjet1sumpCorrection/background_leptonpresel_%i.root" % (int(ctau), int(mass), int(year))
                    dat_str = "~/nobackup/crabdirs/TrackMoverNoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv7_20_tau%06ium_M%i_2Dmovedist3movedist2jetdrjet1sumpCorrection/SingleMuon%i.root" % (int(ctau), int(mass), int(year))

                tm_sim  = ROOT.TFile(sim_str)
                tm_dat  = ROOT.TFile(dat_str)
                signal  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/WplusHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                signal_jetht  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/WplusHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                if mass == '15': 
                    signal_non  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVV0p5JetByMiniJetHistsOnnormdzUlv30lepmumv6/WplusHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                elif mass == '40':
                    signal_non  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVV0p25JetByMiniJetHistsOnnormdzUlv30lepmumv6/WplusHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                else :
                    signal_non  = ROOT.TFile('~/nobackup/crabdirs/TrackMoverMCTruth_StudyMinijets_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkVetoOdVVJetByMiniJetHistsOnnormdzUlv30lepmumv6/WplusHToSSTodddd_tau'+str(int(ctau)/1000)+'mm_M'+ mass +'_'+ year +'.root')
                dat_den = tm_dat.Get('all_closeseedtks_den')
                sim_den = tm_sim.Get('all_closeseedtks_den')
                
                dat_num = tm_dat.Get('all_closeseedtks_num')
                sim_num = tm_sim.Get('all_closeseedtks_num')
                sim_curve = sim_num.Clone()
                sim_den = sim_den.Clone()
                
                sig_dist = signal.Get('nocuts_closeseedtks_den')
                sig_jetht_dist = signal_jetht.Get('nocuts_closeseedtks_den')
                sim_dist = sig_dist.Clone()
                
                sig_denom = signal.Get('all_closeseedtks_den') 
                sig_aaaaa = signal.Get('all_closeseedtks_num')
                sig_curve = sig_aaaaa.Clone()
                temp_sig_num = sig_curve.Clone()
                temp_sig_den = sig_denom.Clone()
                psd_dist = ROOT.TH1D("psd_dist", "M"+mass+"ctau"+ctau+"um", 80, 0, 80)

                sig_jetht_denom = signal_jetht.Get('all_closeseedtks_den') 
                sig_jetht_aaaaa = signal_jetht.Get('all_closeseedtks_num')
                sig_jetht_curve = sig_jetht_aaaaa.Clone()


                sig_non_dvv_denom = signal_non.Get('all_lspdist3_den') 
                sig_non_dvv_curve = signal_non.Get('all_lspdist3_num')
                sig_non_dvv_curve.Divide(sig_non_dvv_denom)
                sig_non_dvv_curve_tm = sig_non_dvv_curve.Clone()
                sig_non_dvv_denom_tm = sig_non_dvv_denom.Clone()
                sig_non_m3d_denom = signal_non.Get('all_vtxunc_den') 
                sig_non_m3d_curve = signal_non.Get('all_vtxunc_num')
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
                sig_m3d_denom = signal.Get('all_vtxunc_den') 
                sig_m3d_curve = signal.Get('all_vtxunc_num')
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
                    #print(" shift : ", shift_val + shift_fr)
                    psd_dist = shiftDIST(psd_dist, shift_val, shift_fr) # psd_dist to sig_dist
                if psd_method == 'scale_distr':
                    psd_dist = sig_dist.Clone()
                    psd_dist.Multiply(scale_factors)
                if psd_method == 'trackrescl':
                    psd_dist = sig_jetht_dist.Clone()
                
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
                sig_curve.Divide(sig_denom)
                sig_jetht_curve.Divide(sig_jetht_denom)
                sim_curve.Divide(sim_den)

                psd_curve = sig_curve
                if psd_method == 'scale_toc':
                    psd_curve = scaledTOC(sig_curve, dat_num, sim_num)
                if psd_method == 'trackrescl':
                    psd_curve = sig_jetht_curve.Clone()
               
                fout2 = ROOT.TFile(psd_method+"_curve.root", "recreate")
                psd_curve.Write()
                fout2.Close()
                
                possible_sim = sig_dist.Integral()
                possible_simtm = sim_dist.Integral()
                possible_psd = psd_dist.Integral()
                sig_dist.Multiply(sig_curve)
                sim_dist.Multiply(sim_curve)

                if doShift:
                    psd_dist.Multiply(psd_curve)
                else:
                    psd_dist.Multiply(sig_curve)

                fout3 = ROOT.TFile(psd_method+"_"+mass+"_"+ctau+"_distcurve.root", "recreate")
                psd_dist.Write()
                fout3.Close()

                pass_sim = sig_dist.Integral()
                pass_simtm = sim_dist.Integral()
                pass_psd = psd_dist.Integral()

                psd_dist.Scale(pass_sim/pass_psd)
                
                eff_sim = pass_sim/possible_sim
                eff_simtm = pass_simtm/possible_simtm
                eff_psd = (pass_psd/possible_psd)

                err_sim = np.sqrt(eff_sim * (1-eff_sim)/possible_sim)
                err_psd = np.sqrt(eff_psd * (1-eff_psd)/possible_psd)
        
                tot_err_one = 2*err_psd/eff_sim 
                tot_err_two = 2*eff_psd*err_sim/(eff_sim**2)

                effArray.append(round(100*(1-eff_psd/eff_sim), 3))
      
                if psd_method == 'none':
                     stat_uncerts = round (100*np.hypot(tot_err_one, tot_err_two), 3)  
                overlap_uncerts = round (100*overlap_right_unc,3)  
                mc_unc = round(100*(1-eff_sim/eff_simtm), 3) 
        print("Mass: %s   Ctau: %s  1-vtx Eff: %.3f " % (mass, ctau, 100*eff_sim))
        datsim_unc = assessMCToDataUncerts( effArray[1], effArray[2], effArray[3], effArray[4], mc_unc, stat_uncerts)
        print( " 1-vtx Unc. by TMMC-to-signalMC : %.3f %%" % (mc_unc) )
        print( " 1-vtx Unc. by SF_{GEN3DdVV, mix}: %.3f %%" % (overlap_uncerts) )
        print( " 1-vtx Unc. by SF_{nclsedtks, mix} x SF_{GEN3DdVV, mix} / SF_{nclsedtks, non}: %.3f %%" % (tm_unc) )
        print( " Total : %.3f %%" % (np.sqrt(datsim_unc**2 + mc_unc**2 + tm_unc**2)))
        print("\n")
