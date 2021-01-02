#!/usr/bin/python3
# -*- coding: utf-8 -*-
# OP - object programming (docs/conf.py)
#
# this file is placed in the public domain

"sphinx conifguration file"

# imports

import doctest
import op
import sys
import unittest

sys.path.append(os.getcwd())

import op

# defines

needs_sphinx='1.1'
nitpick_ignore=[
                ('py:class', 'builtins.BaseException'),
               ]

extensions=[
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

autosummary_generate=True
autodoc_default_flags=['members', 'undoc-members', "imported-members", "show-inheritence"]
autodoc_member_order='bysource'
autodoc_docstring_signature=True
autoclass_content="class"
doctest_global_setup=""
doctest_global_cleanup=""
doctest_test_doctest_blocks="default"
trim_doctest_flags=True
doctest_default_flags=doctest.REPORT_NDIFF & doctest.ELLIPSIS
templates_path=['_templates',]
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
project = "object programming"
copyright = 'Public Domain'
version = '%s' % op.__version__
release = '%s' % op.__version__
language = ''
today = ''
today_fmt = '%B %d, %Y'
exclude_patterns = ['_build', "_sources", "_templates"]
default_role = ''
add_function_parentheses = True
add_module_names = False
show_authors = False
pygments_style = 'sphinx'
modindex_common_prefix = [""]
keep_warnings = True
html_theme = "haiku"
#html_theme_options = {
#     "nosidebar": True,
#}
html_theme_path = []
html_short_title = "OLIB %s" % op.__version__
html_short_title = ""
html_favicon = "opsmile.png"
html_static_path = []
html_extra_path = []
html_last_updated_fmt = '%Y-%b-%d'
html_additional_pages = {}
html_domain_indices = True
html_use_index = True
html_split_index = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
html_copy_source = False
html_use_opensearch = 'http://op.rtfd.io'
html_file_suffix = '.html'
rst_prolog = """.. image:: opline.png
    :height: 2.7cm
    :width: 100%

.. title:: placed in the public domain, no copyright, no license.

"""
htmlhelp_basename = 'pydoc'
intersphinx_mapping = {
                       'python': ('https://docs.python.org/3', None),
                      }
intersphinx_cache_limit=1
