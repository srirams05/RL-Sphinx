# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'My Test Book'
copyright = '2025, Ess Ess'
author = 'Ess Ess'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'myst_parser',
    'sphinx_rtd_theme',
    'sphinx.ext.mathjax',
    'sphinx_math_dollar'
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown', # Explicitly map .md to 'markdown'
}

root_doc = 'index'
# master_doc = 'index' # Use this line instead if your Sphinx version is older than 4.0


templates_path = ['_templates']
exclude_patterns = []


# Add custom CSS
# html_css_files = ['custom.css']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add these lines for GitHub Pages
html_baseurl = '/RL-Sphinx/'  # Replace with your repository name
html_use_index = True
html_copy_source = False


myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    # Add others if you enabled them or plan to use them (e.g., "colon_fence", "deflist", etc.)
]





# Simple MathJax 3 configuration
# This focuses only on defining the TeX input delimiters
# Comprehensive MathJax 3 configuration for all delimiters and scanning



mathjax3_config = {
  "tex": {
    "inlineMath": [['\\(', '\\)']],
    "displayMath": [["\\[", "\\]"]],
  }
}

# Leave out loader, options, startup unless absolutely necessary later
# Remove or comment out the old mathjax_config
# mathjax_config = { ... }

# Options for HTML sidebars
html_sidebars = {
    '**': [ # Apply to all pages
        'sidebar/return_link.html', # Our custom template file
        'globaltoc.html',           # The main TOC based on toctree
        'relations.html',           # Prev/Next links
        'sourcelink.html',          # Link to source file (optional)
        'searchbox.html',           # Search box
    ]
}



