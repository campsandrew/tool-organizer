import sys
import tkinter
import tkinter.ttk

# Local Imports
from tab import Tab
from util import new_widget

# Constant Defintions
NOTEBOOK = tkinter.ttk.Notebook

class Notebook(NOTEBOOK):

    def __init__(self, root, **kwargs):

        # Class variable initialization
        self._root = root
        self._config = root._config
        self._tabs = {}

        # Initialize notebook widget
        new_widget(root, super(), **kwargs)

        # Add tabs to notebook
        for tab in self._config.get_tab_names():
            self._tabs[tab] = Tab(self, **kwargs)
            self.add(self._tabs[tab], text=tab)
        
        return None

    def add_saved_tab(self):
        return None

    def add_history_tab(self):
        return None

    def add_documentation_tab(self):
        return None

    def add_tool_tab(self):
        return None