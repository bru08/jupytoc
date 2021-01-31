# JUPYTOC

Short python script to create a markdown table of contents (TOC) cell at the top of a notebook, from parsed headings.
The TOC cell generated will also have hyperlinks, to referenced cells


## Usage
`python jupytoc.jupytoc -n <path-to-notebook> -o <output-path>`

Example:

`python jupytoc.jupytoc -n ./example.ipynb -o ./example_toc_out.ipynb`