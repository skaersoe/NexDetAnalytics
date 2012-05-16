'''
    Statistical Limit setting
    Morten Dam Joergensen 2012 <mdj@mdj.dk>


'''

from ROOT import *




def significance(signal, backgrounds, histoname, draw=True, reverse=False, method="s_b", symmetry=False, normalise=False):
    """Calculate S/sqrt(S+B) for histogram histoname
    
    signal, the signal sample HistogramCollection
    backgrounds, list of backgrounds in HistogramCollection classes
    draw, create canvas and draw
    reverse, integrate from right to left, instead of left to right
    method, the significance caluclation, s_b, s_bs, or sLR
    symmetry, integrate from the center and out (or from out to the center if reverse)     [ not implemented ]
    
    """
    
    def s_b(s, b):
      """docstring for sb"""

      if s > 0.0 and b > 0.0:
        return s/sqrt(b)
      else:
        return 0.0
      
    def s_bs(s,b):
      """docstring for s_bs"""

      if s> 0.0 and b > 0.0:  
        return s/sqrt(s+b)
      else:
        return 0.0

    def sLR(s,b):
      """docstring for sLR"""

      if s > 0.0 and b > 0.0:
        return sqrt(2*(s + b) * log(1.0 + s/b) - s)
      else:
        return 0.0
      
    methods = {"s_b" : s_b, "s_bs" : s_bs, "sLR" : sLR}

    maxsig = 0.0
    max_val = 0.0
    sig_hist = signal.get(str(histoname)).th.Clone("sig")
    bg_hist = backgrounds[0].get(str(histoname)).th.Clone("bg")
    for bg in xrange(1, len(backgrounds)):
            bg_hist.Add(backgrounds[bg].get(str(histoname)).th)

    if str(signal.get(str(histoname)).th.__class__).find("TH2") > 0: # If 2D histogram
        xbin = sig_hist.GetNbinsX()
        ybin = sig_hist.GetNbinsY()
        
        th2 = TH2F(sig_hist.Clone("signiout"))
        
        if normalise:
            sig_hist.Scale(1.0/sig_hist.Integral())
            bg_hist.Scale(1.0/bg_hist.Integral())
        
        
        for x in xrange(1, xbin):
            for y in xrange(1, ybin):
                
                if reverse:
                    S = sig_hist.Integral(1, x,1, y)
                    B = bg_hist.Integral(1, x, 1, y)
                    x_val = sig_hist.GetXaxis().GetBinUpEdge(x)
                    y_val = sig_hist.GetYaxis().GetBinUpEdge(y)
                    
                else:                    
                    S = sig_hist.Integral(x, xbin, y, ybin)
                    B = bg_hist.Integral(x, xbin, y, ybin)
                    x_val = sig_hist.GetXaxis().GetBinLowEdge(x)
                    y_val = sig_hist.GetYaxis().GetBinLowEdge(y)
                    

                sig = methods[method](S,B)
                    
                
                i = (ybin * (x-1)) + (y-1)

                th2.SetBinContent(x, y, sig)
                if sig > maxsig:
                    maxsig = sig
                    max_val = [x_val,y_val]

                if i % 1000 == 0:
                    print "%d of %d (%0.2f%%)" %(i, xbin*ybin, (float(i)/float(xbin*ybin)) * 100.0)
            
        return th2, maxsig, max_val
        
    else:    # if 1D histogram
        xbin = sig_hist.GetNbinsX()
        g = TGraph(sig_hist.GetNbinsX())
        
        if normalise:
            if sig_hist.Integral() > 0.0:
                sig_hist.Scale(1.0/sig_hist.Integral())
            if bg_hist.Integral() > 0.0:
                bg_hist.Scale(1.0/bg_hist.Integral())
            
        for i in xrange(1, xbin):
            
            if reverse:
                S = sig_hist.Integral(1, i)
                B = bg_hist.Integral(1, i)
                x_val = sig_hist.GetXaxis().GetBinUpEdge(i)
            else:
                S = sig_hist.Integral(i,sig_hist.GetNbinsX())
                B = bg_hist.Integral(i,bg_hist.GetNbinsX())
                x_val = sig_hist.GetXaxis().GetBinLowEdge(i)

            sig = methods[method](S,B)
            g.SetPoint(i-1, x_val ,sig)

            if sig > maxsig:
                maxsig = sig
                max_val = x_val

                
        if draw:
            g.Draw("AP")
            g.GetYaxis().SetTitle("#frac{S}{#sqrt{B}}")
            g.GetXaxis().SetTitle(histoname)
        return g, maxsig, max_val
        
def significance_hist(signal, backgrounds, histoname, draw=True, reverse=False, method="s_bs", symmetry=False, normalise=True):
    """Calculate S/sqrt(S+B) for histogram histoname

    signal, the signal sample HistogramCollection
    backgrounds, list of backgrounds in HistogramCollection classes
    draw, create canvas and draw
    reverse, integrate from right to left, instead of left to right
    method, the significance caluclation, s_b, s_bs, or sLR
    symmetry, integrate from the center and out (or from out to the center if reverse)     [ not implemented ]

    """

    def s_b(s, b):
      """docstring for sb"""

      if s > 0.0 and b > 0.0:
        return s/sqrt(b)
      else:
        return 0.0

    def s_bs(s,b):
      """docstring for s_bs"""

      if s> 0.0 and b > 0.0:  
        return s/sqrt(s+b)
      else:
        return 0.0

    def sLR(s,b):
      """docstring for sLR"""

      if s > 0.0 and b > 0.0:
        return sqrt(2*(s + b) * log(1.0 + s/b) - s)
      else:
        return 0.0

    methods = {"s_b" : s_b, "s_bs" : s_bs, "sLR" : sLR}

    maxsig = 0.0
    max_val = 0.0
    sig_hist = signal.Clone("sig_s")
    bg_hist = backgrounds.Clone("bg_s")

    if str(sig_hist.__class__).find("TH2") > 0: # If 2D histogram
        xbin = sig_hist.GetNbinsX()
        ybin = sig_hist.GetNbinsY()

        th2 = TH2F(sig_hist.Clone("signiout"))

        if normalise:
            sig_hist.Scale(1.0/sig_hist.Integral())
            bg_hist.Scale(1.0/bg_hist.Integral())


        for x in xrange(1, xbin):
            for y in xrange(1, ybin):

                if reverse:
                    S = sig_hist.Integral(1, x,1, y)
                    B = bg_hist.Integral(1, x, 1, y)
                    x_val = sig_hist.GetXaxis().GetBinUpEdge(x)
                    y_val = sig_hist.GetYaxis().GetBinUpEdge(y)

                else:                    
                    S = sig_hist.Integral(x, xbin, y, ybin)
                    B = bg_hist.Integral(x, xbin, y, ybin)
                    x_val = sig_hist.GetXaxis().GetBinLowEdge(x)
                    y_val = sig_hist.GetYaxis().GetBinLowEdge(y)


                sig = methods[method](S,B)


                i = (ybin * (x-1)) + (y-1)

                th2.SetBinContent(x, y, sig)
                if sig > maxsig:
                    maxsig = sig
                    max_val = [x_val,y_val]

                if i % 10000 == 0:
                    print "%d of %d (%0.2f%%)" %(i, xbin*ybin, (float(i)/float(xbin*ybin)) * 100.0)

        return th2, maxsig, max_val

    else:    # if 1D histogram
        xbin = sig_hist.GetNbinsX()
        g = TGraph()

        if normalise:
            if sig_hist.Integral() > 0.0:
                sig_hist.Scale(1.0/sig_hist.Integral())
            if bg_hist.Integral() > 0.0:
                bg_hist.Scale(1.0/bg_hist.Integral())

        for i in xrange(1, xbin):

            if reverse:
                S = sig_hist.Integral(1, i)
                B = bg_hist.Integral(1, i)
                x_val = sig_hist.GetXaxis().GetBinUpEdge(i)
            else:
                S = sig_hist.Integral(i,sig_hist.GetNbinsX())
                B = bg_hist.Integral(i,bg_hist.GetNbinsX())
                x_val = sig_hist.GetXaxis().GetBinLowEdge(i)

            sig = methods[method](S,B)
            g.SetPoint(g.GetN(), x_val ,sig)

            if sig > maxsig:
                maxsig = sig
                max_val = x_val


        if draw:
            g.Draw("AL")
            g.GetYaxis().SetTitle("#frac{S}{#sqrt{S+B}}")
            g.GetXaxis().SetTitle(histoname)
        return g, maxsig, max_val