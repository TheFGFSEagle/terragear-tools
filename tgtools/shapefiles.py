#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
import glob
import re

def find(src):
	osm_shapefiles = []
	shapefiles = glob.glob(os.path.join(src, "**", "**.shp")
	for file in files:
		if "osm" in os.path.split(file):
			osm_shapefiles.append(file)
	return sorted(osm_shapefiles)

def categorize(shapefiles):
	catnames = ["buildings", "landuse", "natural", "places", "pofw", "pois", "railways", "roads", "traffic", "transport", "water", "waterways"]
	categorized = []
	
	for shapefile in shapefiles:
		name = os.path.split(shapefile)[-1].split(".")[0]
		
		# Skip if the name is of the form gis_osm_landuse_a_free_1
		# these files are much smaller than the ones without _a_, probably contain less data.
		if "_a_" in name: 
			continue
		
		name = re.sub(r"gis|osm|a|free|_|(1-9)", "", name) # gis_osm_landuse_a_free_1 becomes just landuse
		# Skip if the name is not a recognized catname
		if not name in catnames:
			continue
		
		categorized.append({"path": shapefile, "category": name})
	return categorized

def get_extents(categorized):
	for shapefile in categorized:
		cmd = f"ogrinfo -al -so -ro -nocount -nomd {shapefile['path']}"
		query = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = list(map(lambda s: s.decode(), query.stdout.splitlines())) # subprocess.Popen.stdout is a binary file - we need normal strings
		
		extents = [s for s in output  if "Extent" in s]
		feature_count = [s for s in output  if "Feature Count" in s]
		
		if len(extents) != 1 or len(feature_count) != 1:
			print("ERROR: Fetching shapefile information using ogrinfo failed.")
			print("               Try reinstalling it through your package manager.")
			print("               If that doesn't help, please file a bug report at <github.com/TheFGFSEagle/terragear-tools/issues>.")
			print("               If you do that, please attach the process-shapefiles-bugreport.md file in order for the maintainers to be able to help you.")
			
			with open("process-shapefile-bugreport.md", "w") as f:
				f.write(f"### Output of `{cmd}`")
				f.writelines(output)
				f.write(f"### ogrinfo version:")
				f.write(subprocess.run("ogrinfo --version", stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True).stdout.deocde())
			sys.exit(2)
		
		# convert "Extent: (10.544425, 51.500000) - (11.500000, 52.500000)" to {"xll": 10.544425, "yll": 51.5, "xur": 11.5, "yur": 52,5]
		extents = dict(zip(["xll", "yll", "yur", "yur"], map(float, re.sub(r"Extent:\s\(|\)", "", extents[0]).replace(") - (", ", ").split(", "))))
		shapefile["extents"] = extents
		

def merge_slice(shapefiles, coords):
	pass

def decode(shapefiles, dest):
	pass

