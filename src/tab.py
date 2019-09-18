import sys
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

# Local Imports
from util import new_widget

# Constant Defintions
FRAME = tkinter.ttk.Frame
SCROLLED_TEXT = tkinter.scrolledtext.ScrolledText

class Tab(FRAME):

    def __init__(self, root, tab_key, **kwargs):

        # Class variable initialization
        self._root = root
        self._scrolled_text = None
        self._tab_key = tab_key

        # Create frame widget
        new_widget(root, super(), **kwargs)

        return None

    def add_scrolling_text(self, **kwargs):
        s_scrolled_text = {"pack": {"expand": True, "fill": "both"},
                           "wrap": "word"}
        self._scrolled_text = new_widget(self, SCROLLED_TEXT, **s_scrolled_text,
                                         **kwargs)

        return None

    