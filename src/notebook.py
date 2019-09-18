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
        self.configuration = root.configuration
        self.var_map = root.var_map
        self._tabs = {}

        # Initialize notebook widget
        new_widget(root, super(), **kwargs)

        # Add tabs to notebook
        for tab in self.configuration.get_tab_names():
            self._tabs[tab] = Tab(self, tab, **kwargs)
            self.add(self._tabs[tab], text=tab)

        # Add event bindings
        self.bind("<<NotebookTabChanged>>", self._on_tab_change)
        
        return None

    def _on_tab_change(self, event):
        tab_key = self.tab(self.select(), "text")
        filepath = self.configuration.get_filepath(tab_key)
        self.var_map.filepath.set(filepath)

        return None

    def add_tool_tab(self, tab_key):
        return None