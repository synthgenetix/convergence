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

# Ensure Sphinx can find all files
source_encoding = 'utf-8'

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

# Configure MyST to handle relative links
myst_heading_anchors = 3
myst_substitutions = {}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'requirements.txt']

# Tell Sphinx to look in subdirectories
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Use the beautiful Furo theme
html_theme = 'furo'

# Theme options
html_theme_options = {
    "sidebar_hide_name": True,  # Hide name since we have logo
    "navigation_with_keys": True,
    "light_css_variables": {
        "color-brand-primary": "#5B4FFF",
        "color-brand-content": "#5B4FFF",
        "color-api-background": "#FAFAFA",
        "color-api-background-hover": "#F0F0F0",
        "font-stack": "'Lexend', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "font-stack-monospace": "'JetBrains Mono', 'Fira Code', monospace",
        "color-foreground-primary": "#1A1A1A",
        "color-foreground-secondary": "#4A4A4A",
        "color-background-primary": "#FFFFFF",
        "color-background-secondary": "#FAFAFA",
    },
    "dark_css_variables": {
        "color-brand-primary": "#7A6FFF",
        "color-brand-content": "#7A6FFF",
        "color-api-background": "#1E1E1E",
        "color-api-background-hover": "#2A2A2A",
        "color-foreground-primary": "#E4E4E4",
        "color-foreground-secondary": "#B0B0B0",
        "color-background-primary": "#0A0A0A",
        "color-background-secondary": "#141414",
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