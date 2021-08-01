# terragear-tools
Python scripts that make using TerraGear easier

## Scripts

### process-elevations.py
Simple wrapper script for `gdalchop` that can be run without arguments

### process-shapefiles.py
Merges, slices, and decodes OSM shapefiles

**IMPORTANT: CORINE shapefiles are NOT YET SUPPORTED !!!**

This script recursively searches the specified input directory for files containing `osm` and ending with `.shp`.
All that are found are then categorized into multiple categories - one for landuse, one for landmass, one for roads, etc.
**For this reason, you may only remove the `gis_` and `_free_1` parts from the shapefile's names !!!**
***Everything else in the name must be conserved in order for your resulting scenery not to have giant holes !!!!!''***

Then, for each shapefile in each category the extents will be queried using `ogrinfo`. To reduce processing time on subsequent runs, the results will be cached.
Then, the script will decide whether to merge or slice the shapefiles for each category based on the coordinates you input.
It will merge / slice the files accordingly with `ogr2ogr`.
As the final step, the resulting shapefiles will be decoded into files that `tg-construct` can read using `ogr-decode`.

## Installation
1. Clone the GitHub repository:
	`git clone https://github.com/TheFGFSEagle/terragear-tools.git`
2. Go into the resulting directory `terragear-tools`:
	`./install.py`
	or
	`python3 install.py`
3. Done ! You can now run these scripts like any other executable: Example:
	`~/scenery-workspace$ process-shapefiles.py`

## License
All files in this repository are released under the GNU General Public License; for more details see the [LICENSE file](LICENSE)

## Contributors
The scripts were written entirely by me, but [Fahim Dalvi](https://forum.flightgear.org/memberlist.php?mode=viewprofile&u=699) from the FlightGear forum gave me some helpful tips.
