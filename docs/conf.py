# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
from datetime import datetime

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Convergence'
copyright = f'{datetime.now().year}, Aditya Patange (AdiPat)'
author = 'Aditya Patange (AdiPat)'
release = 'v0.0.1-alpha'
version = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'sphinx_copybutton',
    'myst_parser',
    'sphinx_design',
]

# Add support for Markdown files
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# MyST Parser configuration for better Markdown support
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "amsmath",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Use the beautiful Furo theme
html_theme = 'furo'

# Theme options
html_theme_options = {
    "light_logo": "convergence_logo_light.png",
    "dark_logo": "convergence_logo_dark.png",
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "announcement": "🚀 Welcome to Convergence - Where minds meet in the digital ether! ☀️",
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF",
        "color-api-background": "#F5F5FF",
        "color-api-background-hover": "#E8E8FF",
        "font-stack": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif",
    },
    "dark_css_variables": {
        "color-brand-primary": "#9C88FF",
        "color-brand-content": "#9C88FF",
        "color-api-background": "#1A1A2E",
        "color-api-background-hover": "#16213E",
    },
}

# Add custom CSS
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]

# Add custom JS if needed
html_js_files = [
    'custom.js',
]

# Logo and favicon
html_logo = "../assets/convergence_logo.png"
html_favicon = "../assets/convergence_logo.png"

# Show "Edit on GitHub" links
html_context = {
    "display_github": True,
    "github_user": "prodigaltech",
    "github_repo": "convergence",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

# -- Extension configuration -------------------------------------------------

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'fastapi': ('https://fastapi.tiangolo.com', None),
}

# Napoleon settings for Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Copy button settings
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True