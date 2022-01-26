from JMTucker.Tools.ROOTTools import *

#This persignal is specifically for the notation used for hnl samples.
#additionally, can  make it to where empty bins are not drawn
class PerSignal_hnl:
    #couplings are quite long; try scientific notation

    #for trilepton samples
    coupling_names = {316: '3.16e-4', 370: '3.70e-4', 836: '8.36e-4', 1414: '1.41e-3'}

    #for semilepton samples
   # coupling_names = {147: '1.47e-4', 793: '7.93e-4', 662: '6.62e-4', 478: '4.78e-4', 21: '2.13e-5', 47: '4.77e-5', 94973: '0.0949', 212367: '0.2123', 19: '1.93e-5', 8: '8.64e-6', 9736: '9.73e-3', 11090: '1.10e-2', 21771: '2.17e-2', 3138: '3.13e-3', 9929: '9.92e-3', 1300: '0.0013', 2511: '2.51e-3', 7218: '7.21e-3', 650: '6.50e-4', 1260: '1.26e-3', 4636: '4.36e-3', 370: '3.7e-4', 716: '7.16e-4', 2118: '2.11e-3', 633: '6.33e-4', 294: '2.94e-4', 2572: '2.57e-3'}
    
    @classmethod
    def clear_samples(_, samples):
        for s in samples:
            if hasattr(s, 'y' ): del s.y
            if hasattr(s, 'yl'): del s.yl
            if hasattr(s, 'yh'): del s.yh
            if hasattr(s, 'ye'): del s.ye

    class curve:
        def __init__(self):
            self.v = {}
        def set(self, coupling, mass, y, eyl, eyh):
            self.v[(coupling, mass)] = (y,eyl,eyh)
        def get(self, coupling, mass):
            return self.v.get((coupling,mass), None)

    def __init__(self, y_title='', y_range=(0.,1.), decay_paves_at_top=True):
        self.masses = set()
        self.couplings = set()
        self.y_title = y_title
        self.y_range = y_range
        self.y_span = y_range[1] - y_range[0]
        self.decay_paves_at_top = decay_paves_at_top
        self.curves = []

    def add(self, samples, title='', color=ROOT.kRed, style=1, in_legend=True):
        # samples already has members y, ye or yl,yh for the ordinate
        # values, or will be marked absent on plot. This is why add
        # separate from TGraph creation in draw, have to know all the
        # (coupling,mass) points first.

        samples = sorted(samples, key=lambda s: s.name)
        tm = [(s.coupling, s.mass) for s in samples]
        if len(tm) != len(set(tm)):
            raise ValueError('duplicate (coupling,mass) seen')

        c = PerSignal_hnl.curve()
        c.title = title
        c.color = color
        c.style = style
        c.in_legend = in_legend
        self.curves.append(c)
        for s in samples:
            self.couplings.add(s.coupling)
            self.masses.add(s.mass)
            if hasattr(s, 'y') and s.y is not None:
                if any((hasattr(s, 'yl') and not hasattr(s, 'yh'),
                        hasattr(s, 'yh') and not hasattr(s, 'yl'),
                        hasattr(s, 'ye') and (hasattr(s, 'yh') or hasattr(s, 'yl')))):
                    raise ValueError('may only specify y,yl,yh or y,ye')
                if hasattr(s, 'yl') and hasattr(s, 'yh') and s.yl is not None and s.yh is not None:
                    eyl = s.y - s.yl
                    eyh = s.yh - s.y
                elif hasattr(s, 'ye') and s.ye is not None:
                    eyl = eyh = s.ye
                else:
                    eyl = eyh = 0.
                c.set(s.coupling, s.mass, s.y, eyl, eyh)

    #adding draw_empty to skip drawing points (mass, coupling) that is not in samples ? 
    def draw(self, draw_missing=False, draw_empty = False, canvas='c_per_signal', size=(1200,600),
             do_coupling_paves=True, do_decay_paves=True):
        if type(canvas) == str:
            canvas = ROOT.TCanvas(canvas, '', *size)
        self.canvas = canvas
        self.canvas.cd()

        couplings   = sorted(self.couplings)
        masses = sorted(self.masses)
        points = self.points = [(coupling, mass) for coupling in couplings for mass in masses]

        #brute force; creating a list of the coupling, mass to draw and not all possibilities

        #this is for semilepton mu
       # cm = [(19, 20), (47, 15), (147, 10), (370, 6), (633, 7), (716, 6), (793, 10), (1260, 5), (1300, 4), (2118, 6), (2511, 4), (3138, 3), (4636, 5), (7218, 4), (9736, 2), (9929, 3), (11090, 2), (21771, 2), (212367, 1)]

        #this is for semilepton e
       # cm = [(19, 20), (21, 15), (147, 10), (370, 6), (478, 13.5), (633, 7), (662, 11.5), (716, 6), (793, 10), (1260, 5), (1300, 4), (2118, 6), (2511, 4), (4636, 5), (7218, 4), (9736, 2), (9929, 3), (11090, 2), (94973, 1), (212367, 1)]

       #this is for trilept mu
        cm = [(316, 7), (316, 9), (370, 6), (836, 12.2), (836, 12.4), (836, 12.6), (836, 12.8), (1414, 13), (1414, 13.2), (1414, 13.4), (1414, 13.8), (1414, 14), (1414, 14.2), (1414, 14.4), (1414, 14.8), (1414, 15)]
        
        if not draw_empty:
            #slim points down to just have what is given in samples i.e. no zero bins
            points = [value for value in points if value in cm]
                             
        npoints = self.npoints = len(points)

        for curve in self.curves:
            x,y,eyl,eyh = [], [], [], []
            x_missing = []
            for i, (coupling, mass) in enumerate(points):
                p = curve.get(coupling, mass)
                if p:
                    x.append(i+0.5)
                    y.append(p[0])
                    eyl.append(p[1])
                    eyh.append(p[2])
                else:
                    x_missing.append(i+0.5)

            n = len(x)
            curve.g = g = ROOT.TGraphAsymmErrors(n)
            for j in xrange(n):
                g.SetPoint(j, x[j], y[j])
                g.SetPointEXlow (j, 0.5)
                g.SetPointEXhigh(j, 0.5)
                g.SetPointEYlow (j, eyl[j])
                g.SetPointEYhigh(j, eyh[j])

            if x_missing:
                g = curve.g_missing = ROOT.TGraph(len(x_missing), to_array(x_missing), to_array([self.y_range[0] + self.y_span*0.01]*len(x_missing)))
                g.SetMarkerColor(curve.color)
                g.SetMarkerStyle(29)
                g.SetMarkerSize(2.0)
            else:
                curve.g_missing = None

        for ic, curve in enumerate(self.curves):
            g = curve.g
            g.SetTitle('')
            g.SetLineWidth(2)
            g.SetLineColor(curve.color)
            g.SetLineStyle(curve.style)
            g.Draw('APZ' if ic == 0 else 'PZ')
            # these must come after the draw because a TGraph* doesn't have an axis until it is drawn (when will I remember this the first time?)
            xax, yax = g.GetXaxis(), g.GetYaxis()
            xax.SetNdivisions(npoints, False)
            xax.SetLabelSize(0)
            xax.SetRangeUser(0, npoints)
            yax.SetRangeUser(*self.y_range)
            yax.SetTitle(self.y_title)
            yax.SetLabelSize(0.03)
#            yax.SetTitleSize(0.032)

            if curve.g_missing and draw_missing:
                curve.g_missing.Draw('P')

        # now draw the accoutrements
        ncouplings   = self.ncouplings = len(couplings)
        nmasses = self.nmasses = len(masses)
        self.coupling_paves = []
        self.coupling_lines = []
        y_coupling = self.y_range[1] + 0.025 * self.y_span
        ccl = [2, 3, 7]
        ccnl = [0, 2, 5, 11]
       # ccl = [3]
      #  ccnl = [1, 4] 
        for i, coupling in enumerate(couplings):
            if do_coupling_paves:
                coupling_name = PerSignal_hnl.coupling_names[coupling]
                ymin = y_coupling
                # if '#mu' not in tau_name:
                #     ymin += 0.006 * self.y_span
                #p = ROOT.TPaveText(i*nmasses+1, ymin, (i+1)*nmasses-1, ymin + 0.07*self.y_span)

                #trilept ... 
                p = ROOT.TPaveText(ccnl[i], ymin, (ccnl[i]+1)*1, ymin + 0.07*self.y_span)
                #this is for semilept
               # p = ROOT.TPaveText(i*1, ymin, (i+1)*1, ymin + 0.07*self.y_span)
                p.SetTextFont(42)
                p.SetFillColor(ROOT.kWhite)
                p.AddText(coupling_name)
                #was 0.042
                #was 0.032 for semilept
                p.SetTextSize(0.028)
                p.SetBorderSize(0)
                p.Draw()
                self.coupling_paves.append(p)
            #custom coupling line for mu 2 for 1st coupling, 1 for 2nd, 4 for 3rd, and 9 for 4th coupling -- don't think need last one 
            if i > 0:
                for z in xrange(2):
                    #for trilept
                    l = ROOT.TLine(ccl[i-1], self.y_range[0], ccl[i-1], self.y_range[1])
                    #for semilept
                    #l = ROOT.TLine(i, self.y_range[0], i, self.y_range[1])
                    #l = ROOT.TLine(i*nmasses, self.y_range[0], i*nmasses, self.y_range[1])
                    l.SetLineWidth(1)
                    if z == 0:
                        l.SetLineColor(ROOT.kWhite)
                    else:
                        l.SetLineStyle(2)
                    l.Draw()
                    self.coupling_lines.append(l)

        self.mass_paves = []
        for i, (_, mass) in enumerate(points):
            ymax = self.y_range[0]-0.04*self.y_span
            p = ROOT.TPaveText(i, ymax-0.02*self.y_span, i+1, ymax)
            p.SetFillColor(ROOT.kWhite)
            t = p.AddText(str(mass))
            t.SetTextAngle(90)
            p.SetTextFont(42)
            p.SetTextSize(0.025)
            p.SetBorderSize(0)
            p.Draw()
            self.mass_paves.append(p)

        self.decay_paves = []
        if do_decay_paves:
            for ic, curve in enumerate([c for c in self.curves if c.in_legend]):
                if self.decay_paves_at_top:
                    decay_pave_loc = 0.5, self.y_range[0]+self.y_span*(0.97-(ic+1)*0.05), nmasses, self.y_range[0]+self.y_span*(0.97-ic*0.05)
                else:
                    decay_pave_loc = 0.5, self.y_range[0]+self.y_span*(0.03+ic*0.05), nmasses, self.y_range[0]+self.y_span*(0.03+(ic+1)*0.05)
                p = ROOT.TPaveText(*decay_pave_loc)
                p.AddText(curve.title)
                p.SetTextFont(42)
                p.SetTextColor(curve.color) #if len(self.curves) > 1 else ROOT.kBlack)
                p.SetFillColor(ROOT.kWhite)
                p.SetBorderSize(0)
                p.Draw()
                self.decay_paves.append(p)

        self.lifetime_pave = ROOT.TPaveText(-3, y_coupling, -0.01, y_coupling + 0.07*self.y_span)
        self.lifetime_pave.SetTextFont(42)
        self.lifetime_pave.SetTextSize(0.048)
        self.lifetime_pave.AddText('V')
        self.lifetime_pave.SetFillColor(ROOT.kWhite)
        self.lifetime_pave.SetBorderSize(0)
        self.lifetime_pave.Draw()

        self.mass_pave = ROOT.TPaveText(0.013, 0.007, 0.105, 0.080, 'NDC')
        self.mass_pave.SetFillColor(ROOT.kWhite)
        self.mass_pave.SetTextFont(42)
        self.mass_pave.SetTextSize(0.03)
        self.mass_pave.AddText('M')
        self.mass_pave.AddText('(GeV)')
        self.mass_pave.SetBorderSize(0)
        self.mass_pave.Draw()

if __name__ == '__main__':
    import argparse, os, sys
    parser = argparse.ArgumentParser(description = 'PerSignal: given a dir of root files, plot a specified statistic for each signal point')
                                  #   usage = '%(prog)s [statistic options] dir histogram plotdir')
    parser.add_argument('rootdir', help='Path to root files.')
    parser.add_argument('hist', help='Path to histogram in the root files.')
    parser.add_argument('plotpath', help='Where to save plots.')
    parser.add_argument('--ytitle', default='changeme', help='Title for y-axis.')
    parser.add_argument('--yrange', nargs=2, type=float, metavar=('YMIN', 'YMAX'), default=None, help='Range for y-axis.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--integral', nargs=2, type=float, metavar=('A','B'), help='Statistic plotted is the integral with the specified range (A and B are floats that will be converted to inclusive bin indices), with Poisson uncertainty from #entries.')
    group.add_argument('-j', '--integral-ratio', nargs=4, type=float, metavar=('A','B', 'C', 'D'), help='Statistic plotted is the ratio of the integrals with the specified ranges AB / CD (A,B,C,D are floats that will be converted to inclusive bin indices), with Poisson uncertainty from #entries.')
    group.add_argument('-m', '--mean', action='store_true', help='Statistic plotted is the mean.')
    group.add_argument('-r', '--rms', action='store_true', help='Statistic plotted is the rms.')
    options = parser.parse_args()

    set_style()
    ps = plot_saver(options.plotpath, size=(600,600))
    
    from JMTucker.Tools import Samples

    multijet = [s for s in Samples.mfv_signal_samples]
    dijet = Samples.mfv_ddbar_samples
    samples = multijet + dijet

    for sample in samples:
        fn = os.path.join(options.rootdir, sample.name + '.root')
        if not os.path.exists(fn):
            continue
        f = ROOT.TFile(fn)
        h = f.Get(options.hist)
        if options.integral:
            sample.y, sample.ye = get_integral(h, *options.integral)
        if options.integral_ratio:
            n, en = get_integral(h, *options.integral_ratio[:2])
            d, ed = get_integral(h, *options.integral_ratio[2:])
            neff = (n/en)**2 if en > 0 else 0
            deff = (d/ed)**2 if ed > 0 else 0
            sample.y, sample.yl, sample.yh = clopper_pearson_poisson_means(neff,deff)
        elif options.mean:
            sample.y = h.GetMean()
            sample.ye = h.GetMeanError()
            sample.ye = h.GetMeanError()
        elif options.rms:
            sample.y = h.GetRMS()
            sample.ye = h.GetRMSError()

        if hasattr(sample, 'ye'):
            print '%26s: %12.6f +- %12.6f' % (sample.name, sample.y, sample.ye)
        else:
            print '%26s: %12.6f [%12.6f, %12.6f]' % (sample.name, sample.y, sample.yl, sample.yh)

    def _g(s,l):
        if hasattr(s, 'ye'):
            return s.y - l*s.ye
        else:
            return s.yl if l else s.yh

    if not options.yrange:
        l = [_g(s, 1) for s in samples]; l = min(l) - max(abs(x) for x in l)*0.05
        h = [_g(s,-1) for s in samples]; h = max(h) + max(abs(x) for x in h)*0.05
        options.yrange = l,h

    per = PerSignal_hnl(options.ytitle, options.yrange)
    per.add(multijet,  title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('plot')
