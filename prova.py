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

# %%
with open(nb_path, "r") as f:
    nb = json.load(f)
# %%
headers = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':  
        for line in cell["source"]:
            if re.match("[#]+.*", line) :
                head_order, title = re.search("([#]+) (.*)", line).groups()
                headers.append((len(head_order), title, i))
                cell["source"].append(f"\n<a id='{i}'></a>\n")

# %%
toc_text = []
for elem in headers:
    toc_text.append( "\t"*(elem[0]-1) + f"* [{elem[1]}](#{elem[2]})" + "  \n")
toc_text.insert(0, "**TOC**  \n  ")
# %%
toc_cell = dict(source = toc_text, cell_type = 'markdown', metadata = {})
nb['cells'].insert(1, toc_cell)

# %%
with open(out_path, "w") as f:
    json.dump(nb, f, indent=True)

# %%
