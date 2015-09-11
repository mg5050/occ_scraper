"""
OCC Scraper:
    occs_test.py:
        automated testing of occ_scraper

Author: Mike Gonzalez (mgonz50@rutgers.edu)
"""

import sys
from os import path, getcwd
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

this_file_dir   = path.dirname(path.abspath(__file__)) # get paths regardless of current directory
parent_dir      = path.abspath(path.join(this_file_dir, ".."))
input_dir       = path.join(this_file_dir, "html")
correct_dir     = path.join(this_file_dir, "output/correct")
tests_fname     = path.join(this_file_dir, "output/test_desc")
default_input   = path.join(input_dir, "site_pycurl.html")
TEST_link_count = 9

sys.path.append(parent_dir) # add parent "main" file path first, regardless of c.d.

from occ_scraper import src_dir # ask "main" for source directory
sys.path.append(src_dir) # append src_dir to sys.path

import occ_vars, scrape # import source

soup = BeautifulSoup(open(default_input, encoding = occ_vars.encoding).read(), 'html.parser') # test link grabbing
print("\n---Testing link scrape---\n")
count = len(scrape.grab_Links(soup, False))
if (count + 1) == TEST_link_count: print("\tresult: PASS - Grabbed " + str(count) + " links + 1 starting url")
else: print("\tresult: FAIL - Grabbed " + str(count) + " links + 1 starting url")

with open(tests_fname, 'r') as f: # test with local html files
    print("\n---Testing data scrape---\n")
    for line in f:
        fname, desc = line.split(occ_vars.delim) # parse input fname and description of test
        print(fname + ":\n\ttest: " + desc.strip())
        result = (scrape.local_Scrape(path.join(input_dir, fname), False))
        base_fname, ext = fname.split('.')
        f = open(path.join(correct_dir, (base_fname + ".good")), 'rb')
        correct_res = f.read()
        f.close()
        ratio = SequenceMatcher(None, result, correct_res).ratio()
        if(ratio == 1.0):
            print("\tresult: PASS - " + str(float("{0:.3f}".format(ratio)) * 100) + "% match")
        else:
            print("\tresult: FAIL - " + str(float("{0:.3f}".format(ratio)) * 100) + "% match")
    print("")