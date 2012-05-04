from ROOT import *
from array import array

def new_color(n=1):
    while True:
        yield n
        n += 1
        
    
class Canvas(object):
    """A TCanvas with a few automatic features, such as legend"""
    def __init__(self, name, title="", width=800, height=600, goption = ""):
        super(Canvas, self).__init__()
        self.name = name
        self.title = title
        self.width = width
        self.height = height
        self.tcanvas = TCanvas(name, title, width, height)
        self.tlegend = TLegend(0.55, 0.5, 0.82, 0.8)
        self.title_g = TLatex()
        self.title_g.SetTextFont(52);
        self.title_g.SetTextAlign(32); # see page 130 in the user guide
        self.title_g.SetTextSize(0.05);
        self.title_g.SetNDC();
        self.title_g.SetTextColor(1);

        
        self.content = []
        self.goption = goption
        
        self.color = new_color() # Color iterator
        
        self.tlegend.SetBorderSize(0)
        self.tlegend.SetFillStyle(0)
        self.tlegend.SetTextAlign(32); # see page 130 in the user guide
        
        self._logx = False
        self._logy = False
        self._logz = False
    
    def cd(self, n=None):
        """docstring for cd"""
        if n:
            self.tcanvas.cd(n)
        else:
            self.tcanvas.cd()
    
    def drawAsStack(self):
        """docstring for drawAsStack"""
        stack = THStack() # FIXME
        for c in self.content:
            stack.Add(c.th)
        return stack.Draw("HIST")
        
    def logx(self):
        """docstring for logx"""
        self.cd()
        if self._logx: 
            self._logx = False
        else:
            self._logx = True
        gPad.SetLogx(self._logx)

    def logy(self):
        """docstring for logx"""
        self.cd()
        if self._logy: 
            self._logy = False
        else:
            self._logy = True
        
        # fix log(0) problem.. the stupid way
        if self.content[0].th.GetMinimum() <= 0.0:
            self.content[0].th.GetYaxis().SetRangeUser(0.00001, self.content[0].th.GetMaximum()*2)
        gPad.SetLogy(self._logy)

    def logz(self):
        """docstring for logx"""
        self.cd()
        if self._logz: 
            self._logz = False
        else:
            self._logz = True
        gPad.SetLogz(self._logz)
        
        
    def xlabel(self, text=None):
        """docstring for xlabel"""            
        if len(self.content) > 0:
            if text:
                self.content[0].th.GetXaxis().SetTitle(text)
            return  self.content[0].th.GetXaxis().GetTitle()

    def ylabel(self, text=None):
        """docstring for xlabel"""
        if len(self.content) > 0:
            if text:
                self.content[0].th.GetYaxis().SetTitle(text)
            return  self.content[0].th.GetYaxis().GetTitle()
        
    def resize(self):
        """docstring for resize"""
        max_y = self.content[0].th.GetMaximum()
        min_y = self.content[0].th.GetBinContent(self.content[0].th.GetMinimumBin())
        for c in self.content:
            max_y = max(c.th.GetMaximum(), max_y)
            min_y = min(c.th.GetBinContent(c.th.GetMinimumBin()), min_y)
        

        self.content[0].th.GetYaxis().SetRangeUser(min_y, max_y+(0.01*max_y))
        
    def update(self):
        """docstring for update"""
        self.resize()
        self.tlegend.Draw()
        self.title_g.DrawLatex(0.82,0.87, self.title);
        self.tcanvas.Update()
        
    
    def saveAs(self, path):
        """docstring for saveas"""
        self.tcanvas.SaveAs(path)
        
    def add(self, hist, goption ="", n=None):
        """docstring for add"""
        self.cd(n)
        hist.draw(self.goption + goption, color=self.color.next())
        self.tlegend.AddEntry(hist.th, hist.title())#, "l")
        self.content.append(hist)
        
        if len(self.content) == 1: # stack
            self.goption += "SAME"
            
        self.update()
        
    def draw(self, *args):
        """add histogram and draw"""
        self.add(*args)
        
        
        
class LAGStyle(object):
    """docstring for ATLStyle"""
    def __init__(self):
        self.SetStyle()

    
    def SetStyle(self):
        """docstring for SetStyle"""
        lagStyle = self.getStyle()
        gROOT.SetStyle("LAGStyle")
        gStyle.SetPalette(1)   

        gROOT.ForceStyle()

        # openGL with anti-alising
        # gStyle.SetCanvasPreferGL(true)

        # beautiful contours
        NRGBs = 7
        NCont = 999
        gStyle.SetNumberContours(NCont)
        stops = array('d',[ 0.00, 0.10, 0.25, 0.45, 0.60, 0.75, 1.00 ])
        red  =  array('d',[1.00, 0.00, 0.00, 0.00, 0.97, 0.97, 0.10])
        green = array('d',[1.00, 0.97, 0.30, 0.40, 0.97, 0.00, 0.00])
        blue  = array('d',[1.00, 0.97, 0.97, 0.00, 0.00, 0.00, 0.00])
        TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
        
        
    def getStyle(self):
        """TStyle, derived from the official ATLAS Style"""
        lagStyle = TStyle("LAGStyle","LAG style")

        # use plain black on white colors
        icol=0 # WHITE
        lagStyle.SetFrameBorderMode(icol)
        lagStyle.SetFrameFillColor(icol)
        lagStyle.SetCanvasBorderMode(icol)
        lagStyle.SetCanvasColor(icol)
        lagStyle.SetPadBorderMode(icol)
        lagStyle.SetPadColor(icol)
        lagStyle.SetStatColor(icol)
        #lagStyle.SetFillColor(icol) # don't use: white fill color for *all* objects

        # set the paper & margin sizes
        lagStyle.SetPaperSize(20,26)

        # set margin sizes
        lagStyle.SetPadTopMargin(0.05)
        lagStyle.SetPadRightMargin(0.13)
        lagStyle.SetPadBottomMargin(0.16)
        lagStyle.SetPadLeftMargin(0.16)


        # lagStyle.SetPadTopMargin(0.018)
        # lagStyle.SetPadRightMargin(0.015)
        # lagStyle.SetPadBottomMargin(0.16)
        # lagStyle.SetPadLeftMargin(0.144)


        # set title offsets (for axis label)
        lagStyle.SetTitleXOffset(1.4)
        lagStyle.SetTitleYOffset(1.4)


        # use large fonts
        #Int_t font=72 # Helvetica italics
        font=42 # Helvetica
        tsize=0.04
        lagStyle.SetTextFont(font)

        lagStyle.SetTextSize(tsize)
        lagStyle.SetLabelFont(font,"x")
        lagStyle.SetTitleFont(font,"x")
        lagStyle.SetLabelFont(font,"y")
        lagStyle.SetTitleFont(font,"y")
        lagStyle.SetLabelFont(font,"z")
        lagStyle.SetTitleFont(font,"z")

        lagStyle.SetLabelSize(tsize,"x")
        lagStyle.SetTitleSize(tsize,"x")
        lagStyle.SetLabelSize(tsize,"y")
        lagStyle.SetTitleSize(tsize,"y")
        lagStyle.SetLabelSize(tsize,"z")
        lagStyle.SetTitleSize(tsize,"z")

        # use bold lines and markers
        lagStyle.SetMarkerStyle(20)
        lagStyle.SetMarkerSize(0.5)
        # lagStyle.SetHistLineWidth(0.7)
        lagStyle.SetLineStyleString(2,"[12 12]") # postscript dashes

        # get rid of X error bars 
        #lagStyle.SetErrorX(0.001)
        # get rid of error bar caps
        lagStyle.SetEndErrorSize(0.)

        # do not display any of the standard histogram decorations
        lagStyle.SetOptTitle(0)
        #lagStyle.SetOptStat(1111)
        lagStyle.SetOptStat(0)
        #lagStyle.SetOptFit(1111)
        lagStyle.SetOptFit(0)

        # put tick marks on top and RHS of plots
        lagStyle.SetPadTickX(1)
        lagStyle.SetPadTickY(1)

        return lagStyle