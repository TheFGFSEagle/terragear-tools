#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# Script that merges, slices, and decodes OSM shapefiles as needed by parsing the coordinates input and the extent of all shapefiles.

import os
import sys
import argparse
import subprocess

from tgtools import constants, shapefiles

DESCRIPTION = """
process-shapefiles.py - merges, slices, and decodes OSM shapefiles

IMPORTANT: CORINE shapefiles are NOT YET SUPPORTED !!!

This script recursively searches the specified input directory for files containing 'osm' and ending with '.shp'.
All that are found are then categorized into multiple categories - one for landuse, one for landmass, one for roads, etc.
For this reason, you may only remove the 'gis_' and '_free_1' parts from the shapefile's names !!!
Everything else in the name must be conserved in order for your resulting scenery not to have giant holes !!!!!''

Then, for each shapefile in each category the extents will be queried using ogrinfo. To reduce processing time on subsequent runs, the results will be cached.
Then, the script will decide whether to merge or slice the shapefiles for each category based on the coordinates you input.
It will merge / slice the files accordingly with ogr2ogr.
As the final step, the resulting shapefiles will be decoded into files that tg-constrcut can read using ogr-decode.
"""

if __name__ == "__main__":
	argp = argparse.ArgumentParser(description="process-shapefiles.py - merges, slices, and decodes OSM shapefiles")
	
	argp.add_argument(
		"-v", "--version",
		action="version",
		version=f"TerraGear tools {'.'.join(map(str, constants.__version__))}"
	)
	
	argp.add_argument(
		"-d", "--description",
		help="display an extended description of what this script does and exit"
	)
	
	argp.add_argument(
		"-i", "--input-folder",
		help="folder containing folder 'shapefiles_raw' containing folders containing unprocessed shapefiles(default: %(default)s)",
		default="./data",
		metavar="FOLDER"
	)

	argp.add_argument(
		"-o", "--output-folder",
		help="folder to put ogr-decode result into (default: %(default)s)",
		default="./work",
		metavar="FOLDER"
	)
	
	argp.add_argument(
		"-c", "--cache-folder",
		help="where to put cache folder (default: %(default)s)",
		default=os.path.join(constants.HOME, ".cache", "tgtools")
	)
	
	argp.add_argument(
		"-l", "--lower-left",
		help="coordinates of the lower left corner of the bounding box of the region that shapefiles should be processed for (default: %(default)s)",
		default="-180,-90"
	)
	
	argp.add_argument(
		"-u", "--upper-right",
		help="coordinates of the upper-right corner of the bounding box of the region that shapefiles should be processed for (default: %(default)s)",
		default="180,90"
	)
	
	args = argp.parse_args()
	
	if args.description:
		print(DESCRIPTION)
		sys.exit(0)

	src = args.input_folder
	dest = args.output_folder
	cache = args.cache_folder
	xll, yll = args.lower_left.split(",")
	xur, yur = args.upper_right.split(",")
	coors = {"xll": xll, "yll": yll, "xur": xur, "yur": yur}
	
	if not os.path.isdir(src):
		print(f"ERROR: input folder {args.input_folder} does not exist, exiting")
		sys.exit(1)
	
	if not os.path.isdir(dst):
		os.mkdirs(dst)
	
	if not os.path.isdir(cache):
		os.mkdirs(cache)
	
	shapefiles = shapefiles.find(src)
	categories = shapefiles.categorize(shapefiles)
	extents = shapefiles.get_extents(categorized)
	shapefiles = shapefiles.merge_slice(extents, coords)
	result = shapefiles.decode(shapefiles, dest)
