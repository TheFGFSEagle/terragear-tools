#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
import glob

def find(src):
	osmshps = []
	shps = glob.glob(os.path.join(src, "**", "**.shp")
	for file in files:
		if "osm" in os.path.split(file):
			osmshps.append(file)
	return osmshps

def categorize(shapefiles):
	for shapefile in shapefiles:
		name = os.path.split()[-1]
		

def get_extents(categorized, cache):
	pass

def merge_slice(shapefiles, categories, extents, coords, cache):
	pass

def decode(shapefiles, dest, cache):
	pass

