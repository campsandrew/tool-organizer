import sys
import json
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

# Local Imports
from map import Map
from tree import Tree
from util import new_widget

# Constant Defintions
FRAME = tkinter.ttk.Frame
BUTTON = tkinter.ttk.Button
SCROLLED_TEXT = tkinter.scrolledtext.ScrolledText

class Tab(FRAME):

    def __init__(self, root, tab_name, **kwargs):

        # Class variable initialization
        self._root = root
        self._name = tab_name
        self._tree = None
        self._scroll_text = None
        self._edit_save_btn = None
        self.tab_id = None
        self.var_map = root.var_map
        self.configuration = root.configuration

        # Create frame widget
        new_widget(root, super(), **kwargs)

        # Create specific tab based on tab key
        if tab_name == self.configuration.DOC_TAB:
            self._create_doc_tab()
        elif tab_name == self.configuration.HISTORY_TAB:
            self._create_history_tab()
        elif tab_name == self.configuration.SAVED_TAB:
            self._create_saved_tab()
        else:
            self._create_tool_tab()

        return None

    def __call__(self):
        return self

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

    def _on_delete_history(self, event):
        item = self._tree.deleted
        self.configuration.delete_history_date(item)
        self._tree.deleted = None

        return None

    def _on_new_history(self, *args):
        item = self.var_map.new_history.get()
        hist = Map(json.loads(item))

        # Add date to tree if new date
        if hist.date not in self._tree:
            self._tree.add(hist.date)

        return None

    def _create_saved_tab(self):
        return None

    def _create_history_tab(self):

        # Adding tree to history tab
        s_tree = {"pack": {"side": "left", "fill": "y"}, "width": 150,
                  "headings": ("Latest", "Earliest"), "show": "tree headings",
                  "selectmode": "browse", "addable": False}
        dates = self.configuration.get_history_dates()
        self._tree = Tree(self, **s_tree).add_items(dates)

        # Tree bindings and variable traces
        self._tree.bind("<<DeleteItem>>", self._on_delete_history)
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

    def _create_tool_tab(self):
        return None

    