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

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/peteradrichem/Xul/",
    "source_branch": "main",
    "source_directory": "docs/",
}
html_title = "XML Utilities"
html_short_title = "Xul"

pygments_style = "default"
pygments_dark_style = "lightbulb"
