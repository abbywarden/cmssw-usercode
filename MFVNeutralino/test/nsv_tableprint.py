#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools import Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

year = '2018'
version = 'V30Lepm'
root_file_dir = '/afs/hep.wisc.edu/home/acwarden/crabdirs/MiniTree%s' % version
#ntks = ('mfvMiniTreeMinNtk3', 'mfvMiniTreeMinNtk4', 'mfvMiniTree')
ntks = ('mfvMiniTreeMinNtk3_loose', 'mfvMiniTreeMinNtk4_loose', 'mfvMiniTree_loose')
#ntks = ('mfvMiniTreeMinNtk3_dxy', 'mfvMiniTreeMinNtk4_dxy', 'mfvMiniTree_dxy')
#ntks = ('mfvMiniTreeMinNtk3_seldxy', 'mfvMiniTreeMinNtk4_seldxy', 'mfvMiniTree_seldxy')

stoplb_samples = Samples.mfv_stoplb_samples_2018
stopld_samples = Samples.mfv_stopld_samples_2018

qcd_samples = Samples.qcd_samples_2018
#only getting the inclusive bk samples
ttbar_samples = Samples.ttbar_samples_2018[:1]
wjet_samples = Samples.wjet_samples_2018[:1]

diboson_samples = Samples.diboson_samples_2018
leptonic_samples = Samples.leptonic_samples_2018
dy_samples = Samples.drellyan_samples_2018

signal_samples = Samples.mfv_stoplb_samples_2018 + Samples.mfv_stopld_samples_2018
data_samples = [] # Samples.data_samples_2017
lumi = ac.int_lumi_2018 * ac.scale_factor_2018
lumi_nice = ac.int_lumi_nice_2018

sample_list = [stoplb_samples, stopld_samples, ttbar_samples, wjet_samples, diboson_samples, leptonic_samples, dy_samples]

sample_title = ["Signal Samples : Stoplb", "Signal Samples: Stopld", "TTbar Background", "WJet Background", "Diboson Background", "QCD Lepton-Enriched Background", "Drellyan Background"]


#sample_list = [ttbar_samples, wjet_samples, diboson_samples, leptonic_samples, dy_samples]

#sample_title = ["TTbar Background", "WJet Background", "Diboson Background", "QCD Lepton-Enriched Background", "Drellyan Background"]

def getit(fn, ntk):
    f = ROOT.TFile.Open(fn)
    t = f.Get('%s/t' % ntk)
    if not t:
        return (-1,-1,-1), (-1,-1,-1)
    hr = draw_hist_register(t, True)
    def c(cut):
        h,n = hr.draw('weight', cut, binning='1,0,1', get_n=True, goff=True)
        return (n,) + get_integral(h)
    n1v = c('nvtx==1')
    n2v = c('nvtx>=2')
    return n1v, n2v


print 'MC scaled to int. lumi. %.3f/fb' % (lumi/1000)
#\usepackage{multirow}
begin_document = r'''
\documentclass{article}
\usepackage[landscape]{geometry}
\usepackage{longtable}

\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{textcomp}

\begin{document}
'''

print begin_document

for ntk in ntks:
    print
    
    latex_table = r''' 

\begin{longtable}[c]{ |p{7cm}||p{5cm}|p{5cm}|  }
\hline
\multicolumn{3}{|c|}{ Weighted (Unweighted) N\string_SV; %s } \\ 
\hline 
Sample Name& 1vtx & 2vtx \\
\hline
'''

    latex_table_end = '''
\end{longtable}
    '''

       
    weighted = []
    table_entries = ''

    ## test
   # for title, sample in zip(sample_title, sample_list):
    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0,0,0,0,0,0
    
    for title,samples in zip(sample_title, sample_list):
        
        table_entries += '%s& & \\\ \n' % (title)
        table_entries += "\hline \n"
        
        for sample in samples:
            sname = sample.name
            fn = os.path.join(root_file_dir, sname + '.root')
            if not os.path.exists(fn):
                continue

            # print getit(fn, ntk)
            (r1v, n1v, en1v), (r2v, n2v, en2v) = getit(fn, ntk)
        
            name = sname.replace('_', '\string_')
       
            if hasattr(Samples, sname):
                sample = getattr(Samples, sname)
                w = lumi * sample.partial_weight(fn)
            
                x = (r1v, w*n1v, w*en1v), (r2v, w*n2v, w*en2v)
                weighted.append((w*n1v, w*en1v, w*n2v, w*en2v))
            
                #new print to immediately be placed in a latex table
                # table_entries += '%s& & ' % (title)
                # if want raw values instead of weighted :
                #table_entries += "%s & %.2f & %.2f \\\ \n" % (name, x[0][0], x[1][0])
                table_entries += "%s & %.2f $\pm$ %.2f (%d) & %.2f $\pm$ %.2f (%d) \\\ \n" % (name, x[0][1], x[0][2], x[0][0], x[1][1], x[1][2], x[1][0])
                table_entries += "\hline \n"


                if sname.startswith('mfv_') == False:
                    raw_n1v += r1v
                    sum_n1v += n1v * w
                    var_n1v += (en1v * w)**2
                    raw_n2v += r2v
                    sum_n2v += n2v * w
                    var_n2v += (en2v * w)**2
    sum_bkg = r'''
 & & \\
\hline 
total bkg& %.2f $\pm$ %.2f (%d) & %.2f $\pm$ %.2f (%d)  \\
\hline
'''

    #if want raw total background : (raw_n1v, raw_n2v)
    # also change above sum_bkg to : %.2f & %.2f 
    print latex_table % (ntk) + table_entries + sum_bkg % (sum_n1v, var_n1v**0.5, raw_n1v, sum_n2v, var_n2v**0.5, raw_n2v) + latex_table_end
    

end_document = '\end{document}'

print end_document
