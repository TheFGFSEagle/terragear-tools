#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# Script that merges, slices, and decodes OSM shapefiles as needed by parsing the coordinates input and the extent of all shapefiles.

import os
import sys
import argparse
import subprocess

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
		"-i", "--input-folder",
		help="folder containing folders containing OSM shapefiles (default: %(default)s",
		default="./data/shapefiles",
		metavar="FOLDER"
	)

	argp.add_argument(
		"-o", "--output-folder",
		help="folder to put ogr-decode result into (default: %(default)s)",
		default=""
	)

	argp.add_argument(
		"--description",
		help="display an extended description of what this script does and exit"
	)

	args = argp.parse_args()

	if args.description:
		print(DESCRIPTION)
		sys.exit(0)

