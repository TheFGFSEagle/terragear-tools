#!/usr/bin/env python3
#-*- coding:utf-8 -*-

# Installer script for the main scripts and modules of terragear-tools
import os
import sys
import argparse

from tgtools import constants


argp = argparse.ArgumentParser(description="install.py - installs the TerraGear tools so that they can be run like any other executable")

argp.add_argument(
	"-p", "--prefix",
	help="Installation prefix (default: %(default)s)",
	default=os.env.get("TGINSTALLPREFIX", os.path.join(constants.HOME, ".local")))
)

argp.add_argument(
	"--add-to-path",
	help="whether to modify your $HOME/.profile file to have the folder containing the scripts in your path (default: %(default)s",
	default="yes",
	choices=["yes", "no"]
)

argp.add_argument(
	"--add-to-pythonpath",
	help="whether to modify your $HOME/.profile file to have the folder containing the modules in your python path (default: %(default)s",
	default="yes",
	choices=["yes", "no"]
)

args = argp.parse_args()


