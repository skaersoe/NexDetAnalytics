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


class Hist(object):
    """docstring for Hist"""
    def __init__(self, th, parent=None):
        super(Hist, self).__init__()
        self.th = th
        self.parent_file = parent
        
    def hist(self):
        """docstring for hist"""
        return self.th
        
    def parent(self):
        """docstring for parent"""
        return self.parent_file
        
        
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
        
    def get(self, key):
        """docstring for get"""
        if isinstance(key, list):
            objs = []
            for k in key:
                if self.fileobj.Get(k):
                    objs.append(Hist(self.fileobj.Get(k), self))
            return objs
        
        if self.fileobj.Get(key):
            return Hist(self.fileobj.Get(key), self)
            
        return None
        
    def parent(self):
        """docstring for parentCollection"""
        return self.parent_collection
    

class FileCollection(object):
    """A collection of TFiles and methods to handle them"""
    def __init__(self):
        super(FileCollection, self).__init__()
        self.tfileobjs = []
        self.verbose = False
    
    def import_from_directory(self, path = ".", nameMatch="(.*).root"):
        """Import all root files from a directory matching the regular expression nameMatch"""
        path = os.path.abspath(path)
        dirList=os.listdir(path)

        for fname in dirList:
            if re.match(nameMatch, fname):
                if self.verbose: print "Importing %s" % fname
                self.tfileobjs.append(File(TFile("/".join([path,fname]),"read"), self))
                
                
    def import_file(self, filepath):
        """Add a specific file to the File collection"""
        self.tfileobjs.append(File(TFile(filepath,"read"), self))
        
    def files(self, fid = -1):
        """Return the File objects"""
        if fid >= 0: 
            return self.tfileobjs[fid]
        else: 
            return self.tfileobjs
            
    def get(self, key):
        """docstring for get"""
        tobjects = []
        for f in self.tfileobjs:
            tobjects.append(f.get(key))
        
        return tobjects
        
    def __str__(self):
        """docstring for __str__"""
        names = []
        for f in self.tfileobjs:
            names.append(f.fileobj.GetName())
        
        return "\n".join(names)
    
        
        