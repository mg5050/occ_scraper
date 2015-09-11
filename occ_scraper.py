"""
OCC Scraper:
    occ_scraper.py:
        entry point for occ_scraper & testing suite

Desc:       Scraper for http://www.oldclassiccar.co.uk/ forum threads
Depends:    Python3.4, PycURL7, BeautifulSoup4
Author:     Mike Gonzalez (mgonz50@rutgers.edu)
"""

src_dir = "core/" # directory containing source code, defined only here

import sys
from os import path

if __name__ == '__main__': # executed as main
    src_dir = path.abspath(src_dir)
    sys.path.append(src_dir) # append src_dir to sys.path
    import occ_vars, scrape # import everything
    scrape.remote_Scrape(occ_vars.start_url, True)
else: # imported elsewhere, make it simple for test framework to locate source
    this_path = path.dirname(path.abspath(__file__))
    src_dir = path.join(this_path, src_dir)