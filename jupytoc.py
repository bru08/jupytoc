"""
# TODO add possibility to have numbered toc and sections
"""

# %%
import json
import re
from copy import copy
import argparse

# %%
parser = argparse.ArgumentParser(description='Add toc to notebooks')
parser.add_argument('-n', '--notebook_path', type=str)
parser.add_argument('-o', '--notebook_out_path', type=str)
args = parser.parse_args()
nb_path = args.notebook_path
out_path = args.notebook_out_path
toc_cell_id = None

# %%
with open(nb_path, "r") as f:
    nb = json.load(f)
# %%
headers = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown': 
        heading = False 
        top_link = True
        for line in cell["source"]:
            if "toc-cell-top" in line:
                toc_cell_id = i
            elif "toc-cell" in line:
                top_link = False
            if re.match("[#]+.*", line) :
                head_order, title = re.search("([#]+) (.*)", line).groups()
                headers.append((len(head_order), title, i))
                heading = True
        if heading and i > 0 and top_link:
            cell["source"].insert(0, f"\n<a id='{i}'></a>\n")
            cell["source"].insert(0, "----\n[Back to top](#toc-cell)\n")

# %%
toc_text = []
for elem in headers:
    toc_text.append( "    "*(elem[0]-1) + f"* [{elem[1]}](#{elem[2]})" + "\n")
toc_text.insert(0, "<a id='toc-cell' class='toc-cell-top'></a>\n")
toc_text.insert(0, "**TOC**  \n  ")
# %%
# If no toc cell present, create the cell, otherwise update it
if not toc_cell_id:
    toc_cell = dict(source = toc_text, cell_type = 'markdown', metadata = {})
    nb['cells'].insert(1, toc_cell)
else:
    nb['cells'][toc_cell_id]['source'] = toc_text

# %%
with open(out_path, "w") as f:
    json.dump(nb, f, indent=True)

# %%
