#!/usr/bin/env python
# encoding: utf-8


import time
import datetime
import FileCollections
import Plotting
import Tables

import sys, os
import random
import string
import subprocess

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    # Reset
    Color_Off='\033[0m'       # Text Reset

    # Regular Colors
    Black='\033[0;30m'        # Black
    Red='\033[0;31m'          # Red
    Green='\033[0;32m'        # Green
    Yellow='\033[0;33m'       # Yellow
    Blue='\033[0;34m'         # Blue
    Purple='\033[0;35m'       # Purple
    Cyan='\033[0;36m'         # Cyan
    White='\033[0;37m'        # White

    # Bold
    BBlack='\033[1;30m'       # Black
    BRed='\033[1;31m'         # Red
    BGreen='\033[1;32m'       # Green
    BYellow='\033[1;33m'      # Yellow
    BBlue='\033[1;34m'        # Blue
    BPurple='\033[1;35m'      # Purple
    BCyan='\033[1;36m'        # Cyan
    BWhite='\033[1;37m'       # White

    # Underline
    UBlack='\033[4;30m'       # Black
    URed='\033[4;31m'         # Red
    UGreen='\033[4;32m'       # Green
    UYellow='\033[4;33m'      # Yellow
    UBlue='\033[4;34m'        # Blue
    UPurple='\033[4;35m'      # Purple
    UCyan='\033[4;36m'        # Cyan
    UWhite='\033[4;37m'       # White

    # Background
    On_Black='\033[40m'       # Black
    On_Red='\033[41m'         # Red
    On_Green='\033[42m'       # Green
    On_Yellow='\033[43m'      # Yellow
    On_Blue='\033[44m'        # Blue
    On_Purple='\033[45m'      # Purple
    On_Cyan='\033[46m'        # Cyan
    On_White='\033[47m'       # White

    # High Intensty
    IBlack='\033[0;90m'       # Black
    IRed='\033[0;91m'         # Red
    IGreen='\033[0;92m'       # Green
    IYellow='\033[0;93m'      # Yellow
    IBlue='\033[0;94m'        # Blue
    IPurple='\033[0;95m'      # Purple
    ICyan='\033[0;96m'        # Cyan
    IWhite='\033[0;97m'       # White

    # Bold High Intensty
    BIBlack='\033[1;90m'      # Black
    BIRed='\033[1;91m'        # Red
    BIGreen='\033[1;92m'      # Green
    BIYellow='\033[1;93m'     # Yellow
    BIBlue='\033[1;94m'       # Blue
    BIPurple='\033[1;95m'     # Purple
    BICyan='\033[1;96m'       # Cyan
    BIWhite='\033[1;97m'      # White

    # High Intensty backgrounds
    On_IBlack='\033[0;100m'   # Black
    On_IRed='\033[0;101m'     # Red
    On_IGreen='\033[0;102m'   # Green
    On_IYellow='\033[0;103m'  # Yellow
    On_IBlue='\033[0;104m'    # Blue
    On_IPurple='\033[10;95m'  # Purple
    On_ICyan='\033[0;106m'    # Cyan


    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        

class Report(object):
    """docstring for Report"""
    def __init__(self, title=u"An example report", author=u"Morten Dam Joergensen", rdate=datetime.date.today(), path=None):
        super(Report, self).__init__()
        self.title = title
        self.author = author
        self.date = rdate
        self.sections = []
        self.path = path

        if self.path:
            d = os.path.dirname(self.path)
            if not os.path.exists(d):
                os.makedirs(d)
        
        if not self.path:
            self.path = "/tmp"
            self.folder = 'lag_report_' + ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(10)) + "_" + datetime.date.today().strftime("%d_%m_%Y")
            self.path = "/".join([self.path, self.folder])
        
        print Colors.Blue +"\nReport folder: %s"  % self.path + Colors.Color_Off
        
        
    # Add new content
    def section(self, title = "a new section"):
        """docstring for new_section"""
        section = Section(title)
        self.sections.append(section)
        return section
        
        
        
        
        
        
    # Generate output methods
    def generate_tex(self):
        """docstring for generatetex"""
        # Create directories
        output_folder = "%s/tex/" % self.path
        output_folder_img = output_folder + "illustrations/"
        d = os.path.dirname(output_folder_img)
        if not os.path.exists(d):
            os.makedirs(d)
        
        filename = output_folder + "%s.tex" % self.title
        # Generate output
        with open(filename, "w") as out:
            preample = r'''
\documentclass[]{article}
\usepackage[utf8]{inputenc}
\usepackage{fullpage}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{ifpdf}
\usepackage{booktabs}
\ifpdf
\usepackage[pdftex]{graphicx}
\else
\usepackage{graphicx}
\fi
'''
            out.write(preample)
            out.write(r"\title{%s}"%self.title + "\n")
            out.write(r"\date{%s}" % str(self.date) + "\n")
            out.write(r"\author{%s}" % self.author + "\n")
                        
            out.write(r'''
\begin{document}

\ifpdf
\DeclareGraphicsExtensions{.pdf, .jpg, .tif}
\else
\DeclareGraphicsExtensions{.eps, .jpg}
\fi

\maketitle
            ''')
            for part in self.sections:
                out.write(r"%s" % part.latex(output_folder, output_folder_img))
        
        
        
            out.write(r'''
%\bibliographystyle{plain}
%\bibliography{}
\end{document}
''')

        
        # # Create PDF
        os.chdir( output_folder )
        retcode = subprocess.call(["pdflatex","-interaction=batchmode", filename])
        retcode = subprocess.call(["pdflatex","-interaction=batchmode", filename])
        retcode = subprocess.call(["pdflatex","-interaction=batchmode", filename])
        retcode = subprocess.call(["pdflatex","-interaction=batchmode", filename])

        # 
        # # Remove LaTex debris
        retcode = os.system("rm *.aux *.log *.toc *.out *.fdb_latexmk")

        print Colors.Blue +"\nLaTeX Report: %s"  % output_folder + "%s.pdf" % self.title + Colors.Color_Off
    
    def generate_html(self):
        """docstring for generate_html"""
        # Create directories
        output_folder = "%s/html/" % self.path
        output_folder_img = output_folder + "illustrations/"
        d = os.path.dirname(output_folder_img)
        if not os.path.exists(d):
            os.makedirs(d)

        filename = output_folder + "%s.html" % self.title
        # Generate output
        with open(filename, "w") as out:
            preample = r'''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
	"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<body>
<head>
'''
            out.write(preample)
            out.write(r"<title>%s</title>"%self.title + "\n")
            out.write(r'''
            
<style type="text/css">
@import url("http://s.wordpress.org/style/codex-wp4.css?3");
@import url("http://s.wordpress.org/style/wp4.css?10");
</style>
<link media="only screen and (max-device-width: 480px)" href="http://wordpress.org/style/iphone.css" type="text/css" rel="stylesheet" >
<!--[if IE]>
<style type="text/css">
@import url("http://wordpress.org/style/ie.css?9");
</style>
<![endif]-->

<style>
.main_content {
text-align: center;
}
table {
	border-width: 1px;
	border-spacing: 2px;
	border-style: outset;
	border-color: gray;
	border-collapse: collapse;
	background-color: white;
}
table th {
	border-width: 1px;
	padding: 3px;
	border-style: dashed;
	border-color: gray;
	background-color: white;
	-moz-border-radius: ;
}
table td {
	border-width: 1px;
	padding: 3px;
	border-style: dashed;
	border-color: gray;
	background-color: white;
	-moz-border-radius: ;
}
.caption {
font-style: italic;
text-align: center;
}
body {
    margin: 20px;
}

h1 {
 font-size: 300%;
 margin: 15px;
}
h2  { 
margin: 10px;
font-size: 200%}
h3 {
margin: 10px;
font-size: 150%;
}
</style>

<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']],
  displayMath: [ ['$$','$$'], ['\[','\]'] ]
  }
});
</script>
<script type="text/javascript"
  src="https://d3eoax9i5htok0.cloudfront.net/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
</head>
<body>
<div class="main_content">''')
            out.write(r"<h1>%s</h1>"%self.title + "\n")
            out.write(r"<i>%s</i>" % str(self.date) + "\n")
            out.write(r"<b>%s</b>" % self.author + "\n")
            

            for part in self.sections:
                out.write(r"%s" % part.html(output_folder, output_folder_img))

            out.write(r'''</div></body></html>''')


        print Colors.Blue +"\nHTML Report: %s"  % output_folder + "%s.html" % self.title + Colors.Color_Off
        
    def generate_text(self):
        """docstring for generate_plain_text"""
        
        # Create directories
        output_folder = "%s/text/" % self.path
        output_folder_img = output_folder + "illustrations/"
        d = os.path.dirname(output_folder_img)
        if not os.path.exists(d):
            os.makedirs(d)
            
        # Generate output
        with open(output_folder + "%s.txt" % self.title, "w") as out:
            out.write(self.title + "\n")
            out.write(str(self.date) + "\n")
            out.write(self.author + "\n")
            
            for part in self.sections:
                out.write("\n%s" % part.plain_text(output_folder, output_folder_img))

            
        print Colors.Blue +"Text report: %s"  % output_folder + "%s.txt" % self.title + Colors.Color_Off
        
        
    def generate_doc(self):
        """docstring for generate_doc"""
        print "Not Implemented"
        
    def generate_rtf(self):
        """docstring for generate_rtf"""
        print "Not Implemented"
        
    def __str__(self):
        """Return the report to screen"""
        out = ["\n"]
        out.append(Colors.BYellow + self.title + Colors.Color_Off)
        out.append(Colors.White + str(self.date) + Colors.Color_Off)
        out.append(Colors.White + self.author + Colors.Color_Off)
        for part in self.sections:
            out.append(str(part))
        return "\t\n".join(out)
        

class Text(object):
    """Container holding text information"""
    def __init__(self, p):
        super(Text, self).__init__()
        self.p = p
        
    def __str__(self):
        """docstring for __str)"""
        return self.p
        
    def plain_text(self, output_folder, output_folder_img):
        """docstring for plain_text"""
        return self.p
        
    def latex(self, output_folder, output_folder_img):
        """docstring for plain_text"""
        return "\n\n" + self.p + "\n"
        
    def html(self, output_folder, output_folder_img):
        """HTML output"""
        return r'<p>%s</p>' % self.p
    
class Equation(Text):
    """docstring for Equation"""
    def __init__(self, eq):
        super(Equation, self).__init__()
        self.p = eq
        
class Section(object):
    """A report section"""
    def __init__(self, title="A section"):
        super(Section, self).__init__()
        self.title = title
        self.parts = []

    def tex_ref(self):
        """docstring for tex_ref"""
        return r"sec:%s" % self.title.replace(" ", "_").replace("#", "")
    
    # Add new content
    def section(self, title = "a new section"):
        """docstring for new_section"""
        subsection = SubSection(title)
        self.parts.append(subsection)
        return subsection
        
    def add(self, content):
        """docstring for add"""
        
        if isinstance(content, str):
            self.parts.append(Text(content))

        if isinstance(content, Plotting.Canvas):
            self.parts.append(content)
        
        if isinstance(content, FileCollections.HistCollection):
            self.parts.append(content)
            
            
        if isinstance(content, FileCollections.Hist):
            self.parts.append(content)

        if isinstance(content, FileCollections.FileCollection):
            self.parts.append(content)
            

        if isinstance(content, FileCollections.File):
            self.parts.append(content)
            
        if isinstance(content, Tables.CutflowTable):
            self.parts.append(content)

    def __str__(self):
        """docstring for __str__"""
        out = ["\n"]
        out.append(Colors.HEADER + self.title + Colors.ENDC)
        for part in self.parts:
            out.append(str(part))
        return "\n".join(out)
        
    def plain_text(self, output_folder, output_folder_img):
        """docstring for plain_text"""
        out = ["\n"]
        out.append(self.title)
        for part in self.parts:
            out.append(part.plain_text(output_folder, output_folder_img))
        return "\n".join(out)

    def latex(self, output_folder, output_folder_img):
        """docstring for plain_text"""
        out = ["\n"]
        out.append(r"\section{%s}" %self.title)
        out.append(r"\label{%s}" % self.tex_ref())
        for part in self.parts:
            out.append(part.latex(output_folder, output_folder_img))
        return "\n".join(out)
        
    def html(self, output_folder, output_folder_img):
        """docstring for html"""
        out = ["\n"]
        out.append(r'<h2 id="%s">%s</h2>' %( self.tex_ref(), self.title))
        for part in self.parts:
            out.append(part.html(output_folder, output_folder_img))
        return "\n".join(out)

class SubSection(Section):
    """A sub section"""
    def __init__(self, title="A subsection"):
        super(SubSection, self).__init__(title)

    def tex_ref(self):
        """docstring for tex_ref"""
        return r"subsec:%s" % self.title.replace(" ", "_").replace("#", "")

        
    def latex(self, output_folder, output_folder_img):
        """docstring for plain_text"""
        out = ["\n"]
        out.append(r"\subsection{%s}" %self.title)
        out.append(r"\label{%s}" % self.tex_ref())
        for part in self.parts:
            out.append(part.latex(output_folder, output_folder_img))
        return "\n".join(out)
        
        
        
    def html(self, output_folder, output_folder_img):
        """docstring for html"""
        out = ["\n"]
        out.append(r'<h3 id="%s">%s</h3>' %( self.tex_ref(), self.title))
        for part in self.parts:
            out.append(part.html(output_folder, output_folder_img))
        return "\n".join(out)


















