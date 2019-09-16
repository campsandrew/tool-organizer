import sys
import tkinter
import tkinter.ttk

# Local Imports
from util import new_widget

# Constant Defintions
FRAME = tkinter.ttk.Frame

class Tab(FRAME):

    def __init__(self, root, **kwargs):

        # Class variable initialization
        self._root = root

        # Create frame widget
        new_widget(root, super(), **kwargs)

        return None