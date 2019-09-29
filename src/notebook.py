import sys
import tkinter
import tkinter.ttk

# Local Imports
from tab import Tab
from utils import new_widget

# Constant Variables
MENU = tkinter.Menu
NOTEBOOK = tkinter.ttk.Notebook

class Notebook(NOTEBOOK):

    #################
    # Special Methods
    #################
    def __init__(self, root, **kwargs):

        # Public Class Variables
        self.configuration = root.configuration
        self.var_map = root.var_map
        self.defaults = [
            self.configuration.SAVED_TAB,
            self.configuration.HISTORY_TAB,
            self.configuration.DOC_TAB
        ]

        # Private Class Variables
        self._root = root
        self._tabs = {}

        # Initialize notebook widget
        new_widget(root, super(), **kwargs)

        # Add tabs to notebook
        tab_names = root.configuration.get_tab_names()
        for tab_name in tab_names + self.defaults:

            # Create tab and add it to notebook
            tab = Tab(self, tab_name, **kwargs)
            self.add(tab, text=tab_name)

            # Save tab 
            tab_id = self.tabs()[-1]         # name associated with notebook.tab(tab_id)
            tab.tab_id = tab_id              
            self._tabs[tab_id] = tab_name    # tab_name is the tab label

        # Example getting tab information
        # self.tab(tab_id)                      - gets tab info 
        # self.children[tab_id.split(".")[-1]]  - gets tab object

        # Add event bindings
        self.bind("<Button-2>", self._on_right_click)
        self.bind("<<NotebookTabChanged>>", self._on_tab_change)
        
        return None

    def __call__(self):
        return self

    #######################
    # Event/Binding Methods
    #######################
    def _on_tab_change(self, event):
        tab_id = self.select()
        tab_name = self._tabs[tab_id]
        filepath = self.configuration.get_filepath(tab_name)
        self.var_map.filepath.set(filepath)

        return None

    def _on_right_click(self, event):

        # Only create popup if on tab label
        if self.identify(event.x, event.y) != "label":
            return None

        # Give tab focus if right clicked
        index = self.index("@{},{}".format(event.x, event.y))
        cur_tab = self.tab(index, "text")
        self.select(self.tabs()[index])
        self.update()

        # Checks if tab can be deleted
        if cur_tab not in self.defaults:

            # Create menu
            popup_menu = new_widget(self, MENU, **{"tearoff": 0})
            popup_menu.add_command(label="Delete", command=self._on_tab_delete)

            # Cause menu to popup
            try: popup_menu.tk_popup(event.x_root, event.y_root + 30, 0)
            finally: popup_menu.grab_release()

        return None

    def _on_tab_delete(self):
        tab_id = self.select()

        # Remove from Notebook and configuration file
        del self._tabs[tab_id]
        self.configuration.delete_user_tab(self.tab(tab_id, "text"))
        self.forget(tab_id)

        return None

    ################
    # Public Methods
    ################
    def add_tool_tab(self, new_tab_name):
        self.configuration.add_user_tab(new_tab_name)

        # Forget all tabs to reorder
        tab_order = []
        insert_index = None
        for i, tab_id in enumerate(list(self.tabs())):
            tab_order.append(self._tabs[tab_id])
            del self._tabs[tab_id]
            self.forget(tab_id)

            # Find index where default tabs begin
            if tab_order[-1] in self.defaults \
                    and insert_index is None:
                insert_index = i

        # Add tabs back to notebook in correct order
        s_tab = {"pack": {"expand": True, "fill": "both"}}
        tab_order.insert(insert_index, new_tab_name)
        for tab_name in tab_order:

            # Create tab and add it to notebook
            tab = Tab(self, tab_name, **s_tab)
            self.add(tab, text=tab_name)

            # Save tab 
            tab_id = self.tabs()[-1]         # name associated with notebook.tab(tab_id)
            tab.tab_id = tab_id              
            self._tabs[tab_id] = tab_name    # tab_name is the tab label

            # Set tab focus to new tab
            if tab_name == new_widget:
                self.select(tab_id)

        return None