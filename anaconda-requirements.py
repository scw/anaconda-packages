# anaconda-requirements.py
# Generate a package list of Anaconda requirements based on the listed
# packages included on the website. Set Python version in line 9, and
# platform in line 10.

import requests
import sys
from lxml import html

PY_MAJOR = sys.version_info[0]
PY_MINOR = sys.version_info[1]

PLATFORM = 'Windows'  # Also: 'Linux', 'Mac'
OUTPUT_FILE = 'anaconda-packages-py{}{}.txt'.format(
        PY_MAJOR, PY_MINOR)
pkg_list_url = 'https://docs.continuum.io/anaconda/' + \
               'pkg-docs#python-{}-{}'.format(PY_MAJOR, PY_MINOR)


r = requests.get(pkg_list_url)

tree = html.fromstring(r.content)
table_path = '//div[@id="python-{}-{}"]/table[1]'.format(PY_MAJOR, PY_MINOR)
pkgs_table = tree.xpath(table_path)[0]

package_list = []
# versions of packages
pkg_versions = pkgs_table.xpath('./tr/td[2]')
pkg_names = pkgs_table.xpath('./tr/td[1]')

# first column contains names and platform info
for (pos, pkg) in enumerate(pkg_names):
    if len(pkg) == 0:
        continue
    pkg_name = pkg[0].text
    pkg_envs = None
    if len(pkg) > 1:
        pkg_plat = pkg[1].text_content()
        pkg_envs = set(pkg_plat.split('\xa0'))
    if pkg_envs is None or PLATFORM in pkg_envs:
        if len(pkg_versions) >= pos:
            pkg_version = pkg_versions[pos].text_content()
            package_list.append("{}={}".format(pkg_name, pkg_version))

with open(OUTPUT_FILE, 'wt') as f:
    header = ("# This file may be used to add packages to an "
              "environment with:\n# $ conda install --file <this file>\n"
              "# platform: win-64\n")
    f.write(header)
    for pkg in package_list:
        f.write("{}\n".format(pkg))
