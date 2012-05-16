from ROOT import *
from array import array
import FileCollections

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
        self.tlegend = TLegend(0.6, 0.5, 0.82, 0.8)
        self.title_g = TLatex()
        self.title_g.SetTextFont(52);
        self.title_g.SetTextAlign(32); # see page 130 in the user guide
        self.title_g.SetTextSize(0.05);
        self.title_g.SetNDC();
        self.title_g.SetTextColor(1);
        self._caption = r""
        
        self.content = []
        self.goption = goption
        self.tstack = THStack()
        
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
    
    def stack(self):
        """docstring for drawAsStack"""
        self.tcanvas.cd(0)
        self.tstack.Draw("nostack")
    
    def yrange(self, miny, maxy):
        """docstring for yrange"""
        self.content[0].th.GetYaxis().SetRangeUser(miny, maxy)

    def xrange(self, minx, maxx):
        """docstring for yrange"""
        self.content[0].th.GetXaxis().SetRangeUser(minx, maxx)
        
    def logx(self):
        """docstring for logx"""
        self.cd()
        if self._logx: 
            self._logx = False
        else:
            self._logx = True
        gPad.SetLogx(self._logx)
        self.tcanvas.Update()

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
        self.tcanvas.Update()

    def logz(self):
        """docstring for logx"""
        self.cd()
        if self._logz: 
            self._logz = False
        else:
            self._logz = True
        gPad.SetLogz(self._logz)
        self.tcanvas.Update()
        
        
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
        if not isinstance(self.content[0].th, TH2):
            max_y = self.content[0].th.GetMaximum()
            min_y = self.content[0].th.GetBinContent(self.content[0].th.GetMinimumBin())
        elif isinstance(self.content[0].th, TGraph) or isinstance(self.content[0].th, TCutG):
            minx = Double()
            miny = Double()
            maxx = Double()
            maxy = Double()
            self.content[0].th.ComputeRange(minx, miny, maxx, maxy) # Get the ranges, transfer the, to a histogram if it is the first object on stack
            max_y = maxy
            min_y = miny
            
        else:
            max_y = self.content[0].th.GetYaxis().GetXmax()            
            min_y = self.content[0].th.GetYaxis().GetXmin()
            
        for c in self.content:
            if isinstance(c.th, TGraph) or isinstance(c.th, TCutG):
                minx = Double()
                miny = Double()
                maxx = Double()
                maxy = Double()
                c.th.ComputeRange(minx, miny, maxx, maxy) # Get the ranges, transfer the, to a histogram if it is the first object on stack
                max_y = max(maxy, max_y)
                min_y = min(miny, min_y)
                
            elif isinstance(c.th, TH2):
                max_y = max(c.th.GetYaxis().GetXmax(), max_y)             
                min_y = min(c.th.GetYaxis().GetXmin(), min_y)
            else:
                max_y = max(c.th.GetMaximum(), max_y)
                min_y = min(c.th.GetBinContent(c.th.GetMinimumBin()), min_y)
                
                

        self.content[0].th.GetYaxis().SetRangeUser(min_y, max_y+(0.01*max_y))
        
    def update(self):
        """docstring for update"""
        self.resize()
        self.tlegend.Draw()
        self.title_g.DrawLatex(0.82,0.87, self.title);
        self.tcanvas.Update()
        
    
    def save(self, path):
        """docstring for saveas"""
        # Todo fix with a sanitiser path that returns a variable to be used in the generator methods
        self.tcanvas.SaveAs(path)
        
    def add(self, hist, goption ="", canvas_n=0, normalize=False, leg_option="l"):
        """docstring for add"""
        self.cd(canvas_n)
        
        if isinstance(hist.th, TGraph) or isinstance(hist.th, TCutG):
            xmin = Double()
            ymin = Double()
            xmax = Double()
            ymax = Double()
            hist.th.ComputeRange(xmin, ymin, xmax, ymax) # Get the ranges, transfer the, to a histogram if it is the first object on stack
            if len(self.content) == 0:
                tmp = TH1F("resizerhist", "resizerhist", 100, xmin, xmax)
                tmp.GetYaxis().SetRangeUser(ymin, ymax)
                t = FileCollections.Hist(tmp)
                self.content.append(t)
                t.draw(self.goption)
                
        if isinstance(hist, FileCollections.Hist):
            if normalize:
                hist.th.Scale(1.0/hist.th.Integral())
            
            hist.draw(self.goption + goption, color=self.color.next())
            if leg_option: self.tlegend.AddEntry(hist.th, hist.th.GetTitle(), leg_option)
            self.content.append(hist)
        
        
        if len(self.content) == 1: # stack
            self.goption += "SAME"
            
        # self.tstack.Add(hist.th, goption)
            
        self.update()
        
    def draw(self, *args):
        """add histogram and draw"""
        self.add(*args)
    
    def caption(self, text):
        """docstring for caption"""
        self._caption = text

    # Report generators
    def tex_ref(self):
        """docstring for tex_ref"""
        return r"fig:%s" % self.title.replace(" ", "_").replace("#", "")
        
    def plain_text(self, output_folder, output_folder_img, format="png"):
        """docstring for fname"""
        filepath = output_folder_img + self.name.replace(" ","_").replace("#", "").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        self.save(filepath)
        relative_dir = output_folder_img.replace(output_folder, "")  + self.name.replace(" ","_").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        
        return "figure: %s (%s)" % (self.title, relative_dir)

    def __str__(self):
        """docstring for __str__"""
        return "Figure: See the canvas named: '%s'." % self.title
        
    def latex(self, output_folder, output_folder_img, format="pdf"):
        """docstring for latex"""
        filepath = output_folder_img + self.name.replace(" ","_").replace("#", "").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        self.save(filepath)
        relative_dir = output_folder_img.replace(output_folder, "")  + self.name.replace(" ","_").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        output = r'''
\begin{figure}[!h]
  \begin{center}
      \includegraphics[width=1.0\textwidth]{%s}
    \caption{\textbf{%s} %s}
    \label{%s}
  \end{center}
\end{figure}
        ''' % (relative_dir, self.title.replace("#", ""), self._caption, self.tex_ref())
        return output

    def html(self, output_folder, output_folder_img, format="png"):
        """docstring for latex"""
        filepath = output_folder_img + self.name.replace(" ","_").replace("#", "").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        self.save(filepath)
        relative_dir = output_folder_img.replace(output_folder, "")  + self.name.replace(" ","_").replace("#", "").replace("(","").replace(")","") + ".%s" % format
        output = r'''<p class="figure" id="%s"><img src="%s" alt="%s"/><small>%s</small></p>''' % (self.tex_ref(), relative_dir, self.title.replace("#", ""), self._caption)
        return output
    def report(self):
        """Information for the Report class to add the convas"""
        return self.__str__()

        
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