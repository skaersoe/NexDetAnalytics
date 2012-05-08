#!/usr/bin/env python
# encoding: utf-8
"""
FileCollections.py

Created by Morten Dam Jørgensen on 2011-11-06.
Copyright (c) 2011 . All rights reserved.
"""

import sys
import os
from ROOT import *
import re
import Plotting

color = Plotting.new_color() # new color iterator

class HistCollection(object):
    """Collection of histograms"""
    def __init__(self, hist_array = []):
        super(HistCollection, self).__init__()
        self.hist_array = hist_array

    
    
    def merge(self, i=0, j=None):
        """docstring for merge"""
        if not j:
            j = len(self.hist_array)-1
        tmpHist = self.hist_array[i].th.Clone("new_%s" % self.hist_array[i].th.GetName())
        for h in self.hist_array[i+1:j]:
            tmpHist.Add(h.th)
        return Hist(tmpHist)
    
    
    def draw(self, goption="", color=None):
        """docstring for draw"""
        fout = self.merge()
        fout.draw(goption, color)        
        return fout.th
    
    
    
    ### Generic function overloading ####
    def __add__(self, other):
        """docstring for __add__"""
        if type(other) == type(self):        
            tmpHist = HistCollection()
            tmpHist.hist_array = self.hist_array + other.hist_array
            return tmpHist
        else:
            raise TypeError

    def __getitem__(self, key):
        """Return the file on key"""
        return self.hist_array[key]

    def __setitem__(self, key, item):
        """docstring for __setitem__"""
        if type(item) == type(self.hist_array[key]):
            self.hist_array[key] = item
        else:
            raise TypeError

    def __len__(self):
        """docstring for __len__"""
        return len(self.hist_array)

    def __iter__(self):
        """docstring for __iter__"""
        return self.hist_array.__iter__()

    def __str__(self):
        """docstring for __str__"""
        names = []
        for f in self.hist_array:
            names.append(f.th.GetName())

        return "\n".join(names)

    
   

class Hist(object):
    """docstring for Hist"""
    def __init__(self, th, parent=None):
        super(Hist, self).__init__()
        self.th = th
        self.parent_file = parent
        self.color = color.next()
        
    def title(self, _title=None):
        """docstring for title"""
        if _title:
            self.th.SetTitle(_title)
            
        return self.th.GetTitle()
    def hist(self):
        """docstring for hist"""
        return self.th
        
    def parent(self):
        """docstring for parent"""
        return self.parent_file
        

    def draw(self, goption="", color=None):
        """docstring for draw"""
        self.th.Draw(goption)
        if color:
            self.color = color
            
        self.th.SetLineColor(self.color)
        # fout.th.SetFillColor(c)
        
        return self.th
        
class File(object):
    """A TFile object wrapper"""
    def __init__(self, fileobj, parent=None):
        super(File, self).__init__()
        self.fileobj = fileobj
        self.parent_collection = parent
        
    def name(self):
        """docstring for name"""
        return self.fileobj.GetName()
        
    def __str__(self):
        """docstring for __str__"""
        return self.name()
        
    def __repr__(self):
        """docstring for __repr__"""
        return "<File %s>" % (self.name())
        
    def keys(self):
        """Return all the keys in the TFile as strings, for easy use with get"""
        return [k.GetName() for k in self.fileobj.GetListOfKeys()]
    
    def entries(self, ttree):
        """docstring for entries"""
        return self.fileobj.Get(ttree).GetEntries()
        
        
    def get_ttree(self, key):
        """ return TTree """
        if isinstance(self.fileobj.Get(key),TTree): # in case of a TTree just return the raw object
            return self.fileobj.Get(key)
        else:
            raise TypeError
            
    def get(self, key):
        """docstring for get"""
        if isinstance(key, list):
            objs = []
            for k in key:
                if self.fileobj.Get(k):
                    # print self.fileobj.Get(k)
                    objs.append(Hist(self.fileobj.Get(k), self))
            return HistCollection(objs)
        
        if self.fileobj.Get(key):
            if isinstance(self.fileobj.Get(key),TTree): # in case of a TTree just return the raw object
                return self.fileobj.Get(key)
                
            return Hist(self.fileobj.Get(key), self)
            
        return None
        
    def parent(self):
        """docstring for parentCollection"""
        return self.parent_collection
    

class FileCollection(object):
    """A collection of TFiles and methods to handle them"""
    def __init__(self, path = None, nameMatch="(.*).root"):
        super(FileCollection, self).__init__()
        self.tfileobjs = []
        self.tfilepaths = []
        self.verbose = False
        if path:
            self.import_from_directory(path=path, nameMatch=nameMatch)
        
    
    def import_from_directory(self, path = ".", nameMatch="(.*).root"):
        """Import all root files from a directory matching the regular expression nameMatch"""
        path = os.path.abspath(path)
        dirList=os.listdir(path)

        for fname in dirList:
            if re.match(nameMatch, fname):
                if self.verbose: print "Importing %s" % fname
                self.tfileobjs.append(File(TFile("/".join([path,fname]),"read"), self))
                self.tfilepaths.append("/".join([path,fname]))
                
    def files(self, fid = -1):
        """Return the File objects"""
        if fid >= 0: 
            return self.tfileobjs[fid]
        else: 
            return self.tfileobjs

    def get_ttree(self, key):
        """docstring for get_ttree
            Returns a TChain
        """
        if isinstance(self.tfileobjs[0].get(key), TTree):
            self.tchain = TChain(key)
            for fp in self.tfilepaths:
                self.tchain.AddFile(fp)
            return self.tchain
        else:
            raise TypeError
            
    def get(self, key):
        """docstring for get"""
        tobjects = []
        
        # TTree are handled a bit different
        # If the variable is a TTree, we create a chain and return that
        if isinstance(self.tfileobjs[0].get(key), TTree):
            return self.get_ttree(key)
        
        for f in self.tfileobjs:
            tobjects.append(f.get(key))
        
        return HistCollection(tobjects)
        
    def append(self, f):
        """Append new file"""
        self.tfileobjs.append(f)
    
    def append_file(self, filepath):
        """Add a specific file to the File collection"""
        self.append(File(TFile(filepath,"read"), self))
        
    def __add__(self, other):
        """docstring for __add__"""
        if type(other) == type(self):        
            tmpFilecollection = FileCollection()
            tmpFilecollection.verbose = self.verbose
            tmpFilecollection.tfileobjs = self.tfileobjs + other.tfileobjs
            tmpFilecollection.tfilepaths = self.tfilepaths + other.tfilepaths
            return tmpFilecollection
        else:
            raise TypeError
            
    def __getitem__(self, key):
        """Return the file on key"""
        return self.tfileobjs[key]
    
    def __setitem__(self, key, item):
        """docstring for __setitem__"""
        if type(item) == type(self.tfileobjs[key]):
            self.tfileobjs[key] = item
        else:
            raise TypeError
            
    def __len__(self):
        """docstring for __len__"""
        return len(self.tfileobjs)
        
    def __iter__(self):
        """docstring for __iter__"""
        return self.tfileobjs.__iter__()
        
    def __str__(self):
        """docstring for __str__"""
        names = []
        for f in self.tfileobjs:
            names.append(f.fileobj.GetName())
        
        return "\n".join(names)
    
        
        