import sys
import tkinter
import tkinter.ttk
import tkinter.scrolledtext

# Local Imports
from tree import Tree
from util import new_widget

# Constant Defintions
FRAME = tkinter.ttk.Frame
BUTTON = tkinter.ttk.Button
SCROLLED_TEXT = tkinter.scrolledtext.ScrolledText

class Tab(FRAME):

    def __init__(self, root, tab_key, **kwargs):

        # Class variable initialization
        self._root = root
        self._tab_key = tab_key
        self.configuration = root.configuration
        self._scroll_text = None
        self._edit_save_btn = None
        self._tree = None

        # Create frame widget
        new_widget(root, super(), **kwargs)

        # Create specific tab based on tab key
        if tab_key == self.configuration.DOC_TAB:
            self._create_doc_tab()
        elif tab_key == self.configuration.HISTORY_TAB:
            self._create_history_tab()
        elif tab_key == self.configuration.SAVED_TAB:
            self._create_saved_tab()
        else:
            self._create_tool_tab()

        return None

    def __call__(self):
        return self

    def _doc_edit(self):

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

    def _create_saved_tab(self):
        return None

    def _create_history_tab(self):

        #TODO: on click change date order to "Earliest" date
        # Adding tree to history tab
        s_tree = {"pack": {"side": "left", "fill": "y"}, "width": 150,
                  "heading": "Latest", "show": "tree headings",
                  "selectmode": "browse"}
        dates = self.configuration.get_history_dates()
        self._tree = Tree(self, **s_tree).add_items(dates)
        
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
                      "command": self._doc_edit}
        btn_frm = new_widget(self, FRAME, **s_btn_frm)
        self._edit_save_btn = new_widget(btn_frm, BUTTON, **s_edit_btn)

        return None

    def _create_tool_tab(self):
        return None

    