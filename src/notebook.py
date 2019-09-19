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
        self._tabs = {} #TODO: use tab_id to manage tabs

        # Initialize notebook widget
        new_widget(root, super(), **kwargs)

        # Add tabs to notebook
        for tab in self.configuration.get_tab_names():
            self._tabs[tab] = Tab(self, tab, **kwargs)
            self.add(self._tabs[tab], text=tab)

        # Add event bindings
        self.bind("<Button-2>", self._on_right_click)
        self.bind("<<NotebookTabChanged>>", self._on_tab_change)
        
        return None

    def _on_tab_change(self, event):
        tab_key = self.tab(self.select(), "text")
        filepath = self.configuration.get_filepath(tab_key)
        self.var_map.filepath.set(filepath)

        return None

    def _on_right_click(self, event):

        # Only create popup if on tab label
        if event.widget.identify(event.x, event.y) != "label":
            return None

        # Give tab focus if right clicked
        index = self.index("@{},{}".format(event.x, event.y))
        cur_tab = self.tab(index, "text")
        self.select(self.tabs()[index])

        # Checks if tab can be deleted
        if cur_tab not in self.configuration.DEFAULT_TABS:

            # Create menu
            popup_menu = tkinter.Menu(self, tearoff=0)
            popup_menu.add_command(label="Delete", command=self._on_tab_delete)

            # Cause menu to popup
            try:
                popup_menu.tk_popup(event.x_root, event.y_root + 30, 0)
            finally:
                popup_menu.grab_release()

        return None

    def _on_tab_delete(self):
        tab_key = self.select()

        # Remove from Notebook and configuration file
        self.configuration.delete_user_tab(self.tab(tab_key, "text"))
        self.forget(tab_key)

        return None

    def add_tool_tab(self, tab_key):
        s_tab = {"pack": {"expand": True, "fill": "both"}}
        self._tabs[tab_key] = Tab(self, tab_key, **s_tab)
        self.add(self._tabs[tab_key], text=tab_key)
        self.select(self.tabs()[-1])
        self.configuration.add_user_tab(tab_key)

        return None