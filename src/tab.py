import sys
import json
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

# Local Imports
from utils import Map
from tree import Tree
from table import Table
from utils import new_widget

# Constant Variables
FRAME = tkinter.ttk.Frame
BUTTON = tkinter.ttk.Button
SCROLLED_TEXT = tkinter.scrolledtext.ScrolledText

class Tab(FRAME):

    #################
    # Special Methods
    #################
    def __init__(self, root, label, **kwargs):

        # Public Class Variables
        self.tab_id = None
        self.var_map = root.var_map
        self.configuration = root.configuration

        # Private Class Variables
        self._tree = None
        self._table = None
        self._scroll_text = None
        self._edit_save_btn = None
        self._tree_selection = None
        self._root = root
        self._tab_label = label
        self._type = {
            root.configuration.SAVED_TAB: self._create_saved_tab,
            root.configuration.DOC_TAB: self._create_doc_tab,
            root.configuration.HISTORY_TAB: self._create_history_tab
        }

        # Create frame and tab structure
        new_widget(root, super(), **kwargs)
        if label in self._type: self._type[label]()
        else: self._create_tool_tab()

        return None

    def __call__(self):
        return self

    #################
    # Private Methods
    #################
    def _create_history_tab(self):

        # Adding tree for history dates
        s_tree = {"headings": ["Latest", "Earliest"], "addable": False}
        dates = self.configuration.get_history_dates()
        self._tree = Tree(self, **s_tree).add_items(dates)

        # Adding command history table
        s_table = {"addable": False}
        headings = [Map({"labels": ("Commands", None, None), "autosize": False}),
                    Map({"labels": ("Time", "Latest", "Earliest"), "autosize": True,
                         "anchor": tkinter.LEFT})]
        self._table = Table(self, headings, **s_table)

        # Tree bindings and variable traces
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)
        self._tree.bind("<<DeleteItems>>", self._on_tree_delete)
        self._table.bind("<<DeleteItems>>", self._on_table_delete)

        # Variable Traces
        self.var_map.new_history.trace("w", self._on_new_history)
        
        return None

    def _create_doc_tab(self):

        # Add scrollable text area
        s_scroll_text = {"pack": {"expand": True, "fill": "both"},
                         "wrap": "word"}
        self._scroll_text = new_widget(self, SCROLLED_TEXT, **s_scroll_text)
        self._scroll_text.insert(tkinter.INSERT, self.configuration.read_doc_file())
        self._scroll_text["state"] = tkinter.DISABLED # Disable after inserting text

        # Add edit/save button for documentation
        s_btn_frm = {"pack": {"side": "bottom", "fill": "x",
                              "padx": 5, "pady": (5, 0)}}
        s_edit_btn = {"pack": {"side": "left"}, "text": "Edit",
                      "command": self._on_doc_edit}
        btn_frm = new_widget(self, FRAME, **s_btn_frm)
        self._edit_save_btn = new_widget(btn_frm, BUTTON, **s_edit_btn)

        return None

    def _create_saved_tab(self):
        return None

    def _create_tool_tab(self):
        return None

    #######################
    # Event/Binding Methods
    #######################
    def _on_doc_edit(self):

        # Alternate edit/save button text on click
        if self._edit_save_btn["text"] == "Edit":
            self._edit_save_btn["text"] = "Save"
            self._scroll_text["state"] = tkinter.NORMAL
        else:
            doc = self._scroll_text.get(1.0, tkinter.END)[:-1] # Removes trailing newline character
            self._edit_save_btn["text"] = "Edit"
            self._scroll_text["state"] = tkinter.DISABLED
            self.configuration.edit_doc_file(doc)

        return None

    def _on_tree_delete(self, event):
        item = self._tree.deleted
        
        # Perform specific action for each tab to load items
        # to page
        if self._tab_label == self.configuration.DOC_TAB: pass
        elif self._tab_label == self.configuration.HISTORY_TAB:
            self.configuration.delete_history_date(item)
        elif self._tab_label == self.configuration.SAVED_TAB: pass
        else: pass

        self._tree.deleted = None

        return None

    def _on_table_delete(self, event):
        items = self._table.deleted
       
        # Perform specific action for each tab to load items
        # to page
        if self._tab_label == self.configuration.DOC_TAB: pass
        elif self._tab_label == self.configuration.HISTORY_TAB:
            date = self._tree.selection()[0]
            self.configuration.delete_history_items(date, items)
        elif self._tab_label == self.configuration.SAVED_TAB: pass
        else: pass

        self._table.deleted = None

        return None

    def _on_new_history(self, *args):
        item = self.var_map.new_history.get()
        hist = Map(json.loads(item))

        # Add date to tree if new date
        if hist.date not in self._tree:
            self._tree.add(hist.date)
            return None

        self._table.add(hist.commands[0])

        return None

    def _on_tree_select(self, event):
        item = self._tree.selection()[0]

        # Don't do anything if current tree item is clicked multiple times
        if self._tree_selection == item: return None
        else: self._tree_selection = item

        # Perform specific action for each tab to load items
        # to page
        if self._tab_label == self.configuration.DOC_TAB: pass
        elif self._tab_label == self.configuration.HISTORY_TAB:
            commands = self.configuration.get_history_commands(item)

            # Clear previous commands and add commnads to table
            self._table.delete(*self._table.get_children())
            self._table.add_items(commands)
        elif self._tab_label == self.configuration.SAVED_TAB: pass
        else: pass

        return None