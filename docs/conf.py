"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
    https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from datetime import datetime

import xul

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Xul"
copyright = f"2013-{datetime.now().year}, Peter Adrichem"
author = "Peter Adrichem"
release = xul.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]

html_theme_options = {
    "description": "XML Utilities",
    "font_size": "16px",
    "code_font_size": "13px",
    "fixed_sidebar": True,
    "extra_nav_links": {"Index": "genindex.html"},
}
