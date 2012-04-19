#!/usr/bin/env python


"""
    Author: Morten Dam Joergensen, 2012
    
    This example loads histograms from multiple files. 
    
    - The collections are divided into three dictionaries, signals, backgrounds and data.
    - Each entry in a dictionary is a FileCollection object.
    - Each FileCollection contains files from a common filepath and a specific name that is parsed by RegEx to collect multiple files with slightly different names (masses in this example)
    
    - The collections can be treated as normal lists in many instances, as illustrated below.
    - Histograms in a specific FileCollection can be requested by <FileCollection>.get(<string>), the returned object is a <HistCollection>
    - HistCollections can be drawn, merged and acts like a list of Hist objects.
    

"""
from ROOT import *

# Only needed if LAGPlottingSuite is not in the python path already
import sys
sys.path.append("../")

from LAGPlottingSuite.FileCollections import FileCollection


# Collect input files
filepath="/Users/mdj/Data/Selection"

signals = {

    # R-Hadrons
    "R-Hadron_gener_gluino_0p1" : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gener_gluino_0p1_(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gen_gl_ffb_0p1"   : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gen_gl_ffb_0p1(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gener_gluino_0p5" : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gener_gluino_0p5(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gen_gl_ffb_0p5"   : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gen_gl_ffb_0p5(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gener_gluino_1p0" : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gener_gluino_1p0(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gen_gl_ffb_1p0"   : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gen_gl_ffb_1p0(.*)GeV_SUSYLLP.root"),            
    "R-Hadron_regge_gluino_0p1" : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_regge_gluino_0p1(.*)GeV_SUSYLLP.root"),
    "R-Hadron_inter_gluino_0p1" : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_inter_gluino_0p1(.*)GeV_SUSYLLP.root"),
    "R-Hadron_gener_stop"       : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_gener_stop(.*)GeV_SUSYLLP.root"),
    "R-Hadron_regge_sbottom"    : FileCollection(path=filepath, nameMatch="(.*)mc11_7TeV.(.*)_Pythia_R-Hadron_regge_sbottom(.*)GeV_SUSYLLP.root")
        }
backgrounds = {
    "BackgroundEstimator.data.periodD"      : FileCollection(path=filepath, nameMatch="Selection.bkg.BackgroundEstimator.data.periodD.root"),
    "BackgroundEstimator.data.periodEFGH"   : FileCollection(path=filepath, nameMatch="Selection.bkg.BackgroundEstimator.data.periodEFGH.root"),
    "BackgroundEstimator.data.periodIJK"    : FileCollection(path=filepath, nameMatch="Selection.bkg.BackgroundEstimator.data.periodIJK.root"),
    "BackgroundEstimator.data.periodLM"     : FileCollection(path=filepath, nameMatch="Selection.bkg.BackgroundEstimator.data.periodLM.root")
}
data = {
    "data.periodD_physics_JetTauEtmiss_SUSYLLP_RPVLL"       : FileCollection(path=filepath, nameMatch="Selection.data.periodD_physics_JetTauEtmiss_SUSYLLP_RPVLL.root"),
    "data.periodEFGH_physics_JetTauEtmiss_SUSYLLP_RPVLL"    : FileCollection(path=filepath, nameMatch="Selection.data.periodEFGH_physics_JetTauEtmiss_SUSYLLP_RPVLL.root"),
    "data.periodIJK_physics_JetTauEtmiss_SUSYLLP_RPVLL"     : FileCollection(path=filepath, nameMatch="Selection.data.periodIJK_physics_JetTauEtmiss_SUSYLLP_RPVLL.root"),
    "data.periodLM_physics_JetTauEtmiss_SUSYLLP_RPVLL"      : FileCollection(path=filepath, nameMatch="Selection.data.periodLM_physics_JetTauEtmiss_SUSYLLP_RPVLL.root")
}


# List the number of files in each signal collection
for key in signals.iterkeys():
    print "%s contains: %d files" % (key, len(signals[key]))

# List the number of files in each background collection    
for key in backgrounds.iterkeys():
    print "%s contains: %d files" % (key, len(backgrounds[key]))
    
# List the number of files in each data collection
for key in data.iterkeys():
    print "%s contains: %d files" % (key, len(data[key]))


# Print all histograms in the first file in the data.periodD_physics_JetTauEtmiss_SUSYLLP_RPVLL file
print data["data.periodD_physics_JetTauEtmiss_SUSYLLP_RPVLL"][0].keys()

# for i in signals["R-Hadron_gener_gluino_0p1"]:
    # print i

# Draw  the "masspass" histogram for the first mass hypothesis in the R-Hadron_gener_gluino_0p1 collection
sig = signals["R-Hadron_gener_gluino_0p1"][4].get("masspass").draw("HIST") # draw() returns the ROOT::TH* object to allow for easy manipulation
sig.SetFillColor(kRed) # Colour it red.

allbg = backgrounds["BackgroundEstimator.data.periodD"] + backgrounds["BackgroundEstimator.data.periodEFGH"] + backgrounds["BackgroundEstimator.data.periodIJK"] + backgrounds["BackgroundEstimator.data.periodLM"]
bg = allbg.get("masspass").draw("SAME HIST")
bg.SetFillColor(kYellow)

alldata = data["data.periodD_physics_JetTauEtmiss_SUSYLLP_RPVLL"] + data["data.periodEFGH_physics_JetTauEtmiss_SUSYLLP_RPVLL"] + data["data.periodIJK_physics_JetTauEtmiss_SUSYLLP_RPVLL"] + data["data.periodLM_physics_JetTauEtmiss_SUSYLLP_RPVLL"]
dat = alldata.get("masspass").draw("SAME")


 
raw_input("Done.. ") # Due to garbage collection, the histograms will be deleted if the script is allowed to return