"""Docs config settings."""
import datetime
from pathlib import PurePath
import sys

# pylint: disable=invalid-name,redefined-builtin

pkg_dir = str(PurePath(__file__).parent.parent)
sys.path.insert(0, pkg_dir)


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinxcontrib.details.directive",
    # "sphinx_paramlinks",
    "sphinx_immaterial",
    "sphinx_immaterial.graphviz",
]

# silence warning on Windows from sphinx_immaterial theme
graphviz_ignore_incorrect_font_metrics = True

# Uncomment the below if you use native CircuitPython modules such as
# digitalio, micropython and busio. List the modules you use. Without it, the
# autodoc module docs will fail to generate with a warning.
# autodoc_mock_imports = ["digitalio", "busio"]


intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "CircuitPython": ("https://docs.circuitpython.org/en/latest/", None),
    "adafruit_circuitpython_minimqtt": (
        "https://docs.circuitpython.org/projects/minimqtt/en/latest/",
        None,
    ),
    "adafruit_datatime": (
        "https://docs.circuitpython.org/projects/datetime/en/latest/",
        None,
    ),
    "adafruit_ntp": (
        "https://docs.circuitpython.org/projects/ntp/en/latest/",
        None,
    ),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# General information about the project.
project = "CircuitPython Homie Library"
creation_year = "2022"
current_year = str(datetime.datetime.now().year)
year_duration = (
    current_year
    if current_year == creation_year
    else creation_year + " - " + current_year
)
copyright = year_duration + " Brendan Doherty"
author = "Brendan Doherty"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "1.0"
# The full version, including alpha/beta/rc tags.
release = "1.0"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".env",
    "CODE_OF_CONDUCT.md",
]

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
default_role = "any"

# If true, '()' will be appended to :func: etc. cross-reference text.
#
add_function_parentheses = True

# -- Options for HTML output ----------------------------------------------

html_theme = "sphinx_immaterial"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["extra_css.css"]

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"

# Output file base name for HTML help builder.
htmlhelp_basename = "CircuitPython_Homie_Librarydoc"
html_title = "CircuitPython-Homie"

html_theme_options = {
    "repo_url": "https://github.com/2bndy5/CircuitPython_Homie",
    "repo_name": "CircuitPython_Homie",
    "repo_type": "Github",
    "icon": {
        "repo": "fontawesome/brands/github",
        "admonition": {
            "note": "material/note-edit-outline",
            "tip": "material/school",
            "warning": "octicons/alert-16",
        },
    },
    "features": [
        "navigation.tabs",
        "navigation.top",
        "search.share",
        "toc.follow",
        "toc.sticky",
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "green",
            "accent": "blue",
            "toggle": {
                "icon": "material/lightbulb-outline",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "light-green",
            "accent": "blue",
            "toggle": {
                "icon": "material/lightbulb",
                "name": "Switch to light mode",
            },
        },
    ],
    "toc_title_is_page_title": True,
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/2bndy5/CircuitPython_Homie",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/circuitpython-homie/",
        },
        {
            "icon": "fontawesome/brands/discord",
            "link": "https://adafru.it/discord",
        },
        {
            "icon": "simple/adafruit",
            "link": "https://www.adafruit.com/",
        },
        {
            "icon": "simple/sparkfun",
            "link": "https://www.sparkfun.com/",
        },
        {
            "name": "CircuitPython Downloads",
            "icon": "octicons/download-24",
            "link": "https://circuitpython.org",
        },
    ],
}

object_description_options = [
    ("py:parameter", dict(include_in_toc=False)),
]
rst_prolog = """
.. role:: python(code)
   :language: python
   :class: highlight
.. role:: homie-dev(literal)
   :class: homie-dev
.. role:: homie-attr(literal)
   :class: homie-attr
.. role:: homie-val(literal)
   :class: homie-val
.. role:: homie-prop(literal)
   :class: homie-prop
.. role:: homie-node(literal)
   :class: homie-node
.. _OpenHAB: https://www.openhab.org/
"""

master_doc = "index"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "CircuitPython_Homie_Library.tex",
        "CircuitPython Homie Library Documentation",
        author,
        "manual",
    ),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "CircuitPython_Homie_Library",
        "CircuitPython Homie Library Documentation",
        [author],
        1,
    ),
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "CircuitPython_Homie_Library",
        "CircuitPython Homie Library Documentation",
        author,
        "CircuitPython_Homie_Library",
        "One line description of project.",
        "Miscellaneous",
    ),
]
