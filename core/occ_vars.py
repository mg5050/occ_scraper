"""
OCC Scraper:
    occ_vars.py:
        occ-specific scraper variables

Author: Mike Gonzalez (mgonz50@rutgers.edu)
"""

from os import path

absolute_path   =   "REDACTED"                                                 # prefix for relative paths
date_trim       =   "Posted: "                                              # extra info found before data
delim           =   ';'                                                     # delimiter for output file
encoding        =   "iso-8859-1"                                            # website encoding
write_enc       =   "utf-8"                                                 # must specify explicitly for some OS
br              =   "<br/>"                                                 # line break representation
br_alt          =   "<br>"                                                  # line break representation
parent_dir      =   path.abspath(path.join(path.dirname(__file__), ".."))   # parent dir of this file, regardless of caller
par_rel_fname   =   "output/forum.csv"                                      # fname relative to parent dir
output_fname    =   path.join(parent_dir, par_rel_fname)                    # absolute fname regardless of caller
sig             =   "_________________"                                     # signature line
sig_trima       =   br+sig+br                                               # post signature
sig_trimb       =   br_alt+sig+br_alt                                       # post signature
start_url       =   absolute_path + "viewtopic.php?t=12591"                 # initial url